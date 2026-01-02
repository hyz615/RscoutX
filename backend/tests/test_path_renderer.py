import pytest
from app.services.path_renderer import PathRenderer
from app.schemas.schemas import PathPoint, PathStyle


def test_path_renderer_polyline():
    """Test polyline rendering"""
    renderer = PathRenderer()
    points = [
        PathPoint(x=100, y=100),
        PathPoint(x=200, y=200),
        PathPoint(x=300, y=150)
    ]
    style = PathStyle(color="#FF0000", width=3)
    
    result = renderer.render(
        method="polyline",
        points=points,
        style=style,
        return_image=True,
        return_overlay=False
    )
    
    assert result["success"] == True
    assert "image_base64" in result


def test_path_renderer_bezier():
    """Test bezier curve rendering"""
    renderer = PathRenderer()
    points = [
        PathPoint(x=100, y=100),
        PathPoint(x=200, y=300),
        PathPoint(x=300, y=100),
        PathPoint(x=400, y=200)
    ]
    style = PathStyle(color="#0000FF", width=4)
    
    result = renderer.render(
        method="bezier",
        points=points,
        style=style,
        return_image=True,
        return_overlay=False
    )
    
    assert result["success"] == True
    assert "image_base64" in result


def test_coordinate_conversion():
    """Test coordinate system conversion"""
    renderer = PathRenderer()
    points = [
        PathPoint(x=1800, y=1800),  # Center of 3600x3600mm field
        PathPoint(x=3000, y=3000)
    ]
    
    # Assuming 600x600 pixel image for test
    img_size = (600, 600)
    converted = renderer.convert_coordinates(points, "field", img_size)
    
    # Center should map to ~300, 300 in pixels
    assert abs(converted[0][0] - 300) < 10
    assert abs(converted[0][1] - 300) < 10
