import os
import io
import base64
import numpy as np
from typing import List, Tuple, Optional, Any, Dict
from PIL import Image, ImageDraw, ImageFont
from scipy import interpolate
from scipy.spatial.distance import euclidean
import cv2

from app.core.config import settings
from app.schemas.schemas import PathPoint, PathStyle, RobotState


class PathRenderer:
    """Path rendering service for VEX V5 Pushback field map"""
    
    # State color mapping
    STATE_COLORS = {
        'wingpushing': '#FF4500',  # Orange-red
        'intaking': '#00FF00',      # Green
        'releasing': '#FFD700',     # Gold
        'moving': '#1E90FF',        # Dodger blue
        'idle': '#808080'           # Gray
    }
    
    # State icons (using Unicode symbols)
    STATE_ICONS = {
        'wingpushing': '➤',  # Right arrow
        'intaking': '⬇',     # Down arrow
        'releasing': '⬆',    # Up arrow
        'moving': '●',       # Circle
        'idle': '○'          # Empty circle
    }
    
    def __init__(self, map_path: Optional[str] = None):
        self.map_path = map_path or settings.MAP_IMAGE_PATH
        self.field_width = settings.FIELD_WIDTH_MM
        self.field_height = settings.FIELD_HEIGHT_MM
        try:
            # Try to load a font, fallback to default if not available
            self.font = ImageFont.truetype("arial.ttf", 14)
            self.font_large = ImageFont.truetype("arial.ttf", 20)
        except:
            self.font = ImageFont.load_default()
            self.font_large = ImageFont.load_default()
        
    def load_map(self) -> Image.Image:
        """Load the field map image"""
        if not os.path.exists(self.map_path):
            # Create blank map if not exists
            img = Image.new('RGB', (settings.DEFAULT_MAP_WIDTH, settings.DEFAULT_MAP_HEIGHT), 'white')
            return img
        return Image.open(self.map_path).convert('RGB')
    
    def convert_coordinates(self, points: List[PathPoint], 
                          coordinate_system: str, 
                          img_size: Tuple[int, int]) -> List[Tuple[float, float]]:
        """Convert field coordinates to pixel coordinates"""
        if coordinate_system == "pixel":
            return [(p.x, p.y) for p in points]
        
        # Convert from field coordinates (mm) to pixels
        img_w, img_h = img_size
        scale_x = img_w / self.field_width
        scale_y = img_h / self.field_height
        
        converted = []
        for p in points:
            px = p.x * scale_x
            py = p.y * scale_y
            converted.append((px, py))
        return converted
    
    def render_polyline(self, img: Image.Image, points: List[Tuple[float, float]], 
                       style: PathStyle) -> Image.Image:
        """Draw polyline connecting points"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        if len(points) < 2:
            return img
        
        # Convert color with opacity
        color = self._hex_to_rgba(style.color, style.opacity)
        
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=color, width=style.width)
        
        # Draw arrows if requested
        if style.arrow:
            for i in range(len(points) - 1):
                self._draw_arrow(draw, points[i], points[i + 1], color, style.width)
        
        return img
    
    def render_bezier(self, img: Image.Image, points: List[Tuple[float, float]], 
                     style: PathStyle) -> Image.Image:
        """Draw smooth Bezier curve through points"""
        if len(points) < 2:
            return img
        
        # Use scipy to create Bezier curve
        points_array = np.array(points)
        
        if len(points) == 2:
            # Simple line for 2 points
            return self.render_polyline(img, points, style)
        
        # Create parameter array
        t = np.linspace(0, 1, len(points))
        t_smooth = np.linspace(0, 1, len(points) * 20)
        
        # Interpolate x and y separately
        from scipy.interpolate import make_interp_spline
        spl_x = make_interp_spline(t, points_array[:, 0], k=min(3, len(points) - 1))
        spl_y = make_interp_spline(t, points_array[:, 1], k=min(3, len(points) - 1))
        
        x_smooth = spl_x(t_smooth)
        y_smooth = spl_y(t_smooth)
        
        smooth_points = list(zip(x_smooth, y_smooth))
        return self.render_polyline(img, smooth_points, style)
    
    def render_spline(self, img: Image.Image, points: List[Tuple[float, float]], 
                     style: PathStyle) -> Image.Image:
        """Draw Catmull-Rom spline through points"""
        if len(points) < 3:
            return self.render_polyline(img, points, style)
        
        points_array = np.array(points)
        
        # Catmull-Rom spline using scipy
        tck, u = interpolate.splprep([points_array[:, 0], points_array[:, 1]], s=0, k=min(3, len(points) - 1))
        u_fine = np.linspace(0, 1, len(points) * 20)
        x_fine, y_fine = interpolate.splev(u_fine, tck)
        
        smooth_points = list(zip(x_fine, y_fine))
        return self.render_polyline(img, smooth_points, style)
    
    def render_astar(self, img: Image.Image, points: List[Tuple[float, float]], 
                    style: PathStyle, obstacles: Optional[List[Any]] = None) -> Image.Image:
        """A* pathfinding and rendering"""
        if len(points) < 2:
            return img
        
        start = points[0]
        end = points[-1]
        
        # Simple implementation: if no obstacles, use straight line
        if not obstacles:
            return self.render_polyline(img, [start, end], style)
        
        # Create grid for A*
        img_w, img_h = img.size
        grid_resolution = 20
        grid = np.zeros((img_h // grid_resolution, img_w // grid_resolution), dtype=int)
        
        # Mark obstacles on grid
        for obstacle in obstacles:
            if isinstance(obstacle, dict):
                x, y, w, h = obstacle.get('x', 0), obstacle.get('y', 0), obstacle.get('w', 20), obstacle.get('h', 20)
                gx1, gy1 = int(x / grid_resolution), int(y / grid_resolution)
                gx2, gy2 = int((x + w) / grid_resolution), int((y + h) / grid_resolution)
                grid[gy1:gy2, gx1:gx2] = 1
        
        # Run A* algorithm
        path = self._astar_path(grid, 
                               (int(start[1] / grid_resolution), int(start[0] / grid_resolution)),
                               (int(end[1] / grid_resolution), int(end[0] / grid_resolution)))
        
        if path:
            # Convert grid path back to pixel coordinates
            pixel_path = [(p[1] * grid_resolution, p[0] * grid_resolution) for p in path]
            return self.render_spline(img, pixel_path, style)
        else:
            # Fallback to direct line if no path found
            return self.render_polyline(img, [start, end], style)
    
    def render_heatline(self, img: Image.Image, points: List[PathPoint], 
                       style: PathStyle) -> Image.Image:
        """Draw heatmap-style line with varying thickness/color based on speed"""
        if len(points) < 2:
            return img
        
        # Convert to numpy array for OpenCV
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        for i in range(len(points) - 1):
            p1 = (int(points[i].x), int(points[i].y))
            p2 = (int(points[i + 1].x), int(points[i + 1].y))
            
            # Use speed or default to create heat effect
            speed = points[i].speed or points[i].t or 1.0
            
            # Map speed to color (blue=slow, red=fast)
            normalized_speed = min(max(speed / 10.0, 0), 1)
            color_bgr = self._speed_to_color(normalized_speed)
            
            # Vary thickness based on speed
            thickness = int(style.width * (0.5 + normalized_speed))
            
            cv2.line(img_cv, p1, p2, color_bgr, thickness)
        
        # Convert back to PIL
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img_rgb)
    
    def draw_robot_states(self, img: Image.Image, points: List[PathPoint], 
                         pixel_points: List[Tuple[float, float]], 
                         style: PathStyle) -> Image.Image:
        """Draw robot state markers and labels on the path"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        for i, (point, pixel_pos) in enumerate(zip(points, pixel_points)):
            if not point.robot_state:
                continue
            
            state = point.robot_state.state.lower()
            px, py = int(pixel_pos[0]), int(pixel_pos[1])
            
            # Get state color (use custom color or default)
            if point.robot_state.color:
                state_color = point.robot_state.color
            else:
                state_color = self.STATE_COLORS.get(state, '#808080')
            
            rgba_color = self._hex_to_rgba(state_color, 0.9)
            
            # Draw state marker (larger circle with border)
            marker_size = style.state_icon_size
            draw.ellipse(
                [px - marker_size, py - marker_size, 
                 px + marker_size, py + marker_size],
                fill=rgba_color,
                outline=(255, 255, 255, 255),
                width=2
            )
            
            # Draw icon in the center
            icon = self.STATE_ICONS.get(state, '●')
            # Calculate text size
            bbox = draw.textbbox((px, py), icon, font=self.font_large)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Draw icon centered on the marker
            draw.text(
                (px - text_width // 2, py - text_height // 2),
                icon,
                fill=(255, 255, 255, 255),
                font=self.font_large
            )
            
            # Draw state label if enabled
            if style.show_state_labels:
                label_text = state.replace('_', ' ').title()
                label_bbox = draw.textbbox((0, 0), label_text, font=self.font)
                label_width = label_bbox[2] - label_bbox[0]
                label_height = label_bbox[3] - label_bbox[1]
                
                # Position label above the marker
                label_x = px - label_width // 2
                label_y = py - marker_size - label_height - 5
                
                # Draw label background
                padding = 3
                draw.rectangle(
                    [label_x - padding, label_y - padding,
                     label_x + label_width + padding, label_y + label_height + padding],
                    fill=(0, 0, 0, 180)
                )
                
                # Draw label text
                draw.text(
                    (label_x, label_y),
                    label_text,
                    fill=(255, 255, 255, 255),
                    font=self.font
                )
        
        return img
    
    def render(self, method: str, points: List[PathPoint], style: PathStyle,
               coordinate_system: str = "pixel", obstacles: Optional[List[Any]] = None,
               return_image: bool = True, return_overlay: bool = False,
               canvas_size: Tuple[int, int] = (800, 800)) -> Dict[str, Any]:
        """Main rendering method
        
        Args:
            canvas_size: Target canvas size (default 800x800 to match frontend)
        """
        
        # Load map and resize to match frontend canvas
        img = self.load_map()
        img = img.resize(canvas_size, Image.Resampling.LANCZOS)
        img_size = canvas_size
        
        # Convert coordinates - points are already in pixel coordinates relative to canvas_size
        pixel_points = self.convert_coordinates(points, coordinate_system, img_size)
        
        # Render based on method
        if method == "polyline":
            img = self.render_polyline(img, pixel_points, style)
        elif method == "bezier":
            img = self.render_bezier(img, pixel_points, style)
        elif method == "spline":
            img = self.render_spline(img, pixel_points, style)
        elif method == "astar":
            img = self.render_astar(img, pixel_points, style, obstacles)
        elif method == "heatline":
            img = self.render_heatline(img, points, style)
        else:
            raise ValueError(f"Unknown rendering method: {method}")
        
        # Draw robot states on top of the path
        img = self.draw_robot_states(img, points, pixel_points, style)
        
        result = {"success": True}
        
        # Return image as base64
        if return_image:
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            result["image_base64"] = img_base64
        
        # Return overlay JSON
        if return_overlay:
            overlay = {
                "method": method,
                "points": [{"x": p[0], "y": p[1]} for p in pixel_points],
                "style": style.dict()
            }
            result["overlay_json"] = overlay
        
        return result
    
    def _hex_to_rgba(self, hex_color: str, opacity: float) -> Tuple[int, int, int, int]:
        """Convert hex color to RGBA tuple"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        a = int(opacity * 255)
        return (r, g, b, a)
    
    def _speed_to_color(self, normalized_speed: float) -> Tuple[int, int, int]:
        """Map speed (0-1) to color (BGR for OpenCV)"""
        # Blue (slow) to Red (fast)
        if normalized_speed < 0.5:
            # Blue to Green
            b = int(255 * (1 - normalized_speed * 2))
            g = int(255 * normalized_speed * 2)
            r = 0
        else:
            # Green to Red
            b = 0
            g = int(255 * (2 - normalized_speed * 2))
            r = int(255 * (normalized_speed - 0.5) * 2)
        return (b, g, r)
    
    def _draw_arrow(self, draw: ImageDraw.Draw, start: Tuple[float, float], 
                   end: Tuple[float, float], color: Tuple, width: int):
        """Draw arrow head at the end of a line"""
        # Calculate arrow head
        angle = np.arctan2(end[1] - start[1], end[0] - start[0])
        arrow_length = width * 3
        arrow_angle = np.pi / 6
        
        # Arrow points
        p1 = (
            end[0] - arrow_length * np.cos(angle - arrow_angle),
            end[1] - arrow_length * np.sin(angle - arrow_angle)
        )
        p2 = (
            end[0] - arrow_length * np.cos(angle + arrow_angle),
            end[1] - arrow_length * np.sin(angle + arrow_angle)
        )
        
        draw.line([end, p1], fill=color, width=width)
        draw.line([end, p2], fill=color, width=width)
    
    def _astar_path(self, grid: np.ndarray, start: Tuple[int, int], 
                   end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """A* pathfinding algorithm"""
        from heapq import heappush, heappop
        
        rows, cols = grid.shape
        
        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            return None
        if not (0 <= end[0] < rows and 0 <= end[1] < cols):
            return None
        if grid[start] == 1 or grid[end] == 1:
            return None
        
        # Directions: up, down, left, right, and diagonals
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        while open_set:
            current = heappop(open_set)[1]
            
            if current == end:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]
            
            for d in directions:
                neighbor = (current[0] + d[0], current[1] + d[1])
                
                if not (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols):
                    continue
                if grid[neighbor] == 1:
                    continue
                
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heappush(open_set, (f_score, neighbor))
        
        return None
