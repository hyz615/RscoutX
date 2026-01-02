from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import base64

from app.schemas.schemas import PathRenderRequest, PathRenderResponse
from app.services.path_renderer import PathRenderer

router = APIRouter(prefix="/path", tags=["path"])


@router.post("/render", response_model=PathRenderResponse)
async def render_path(request: PathRenderRequest):
    """Render path on field map"""
    try:
        renderer = PathRenderer(request.map_filename)
        
        result = renderer.render(
            method=request.method,
            points=request.points,
            style=request.style,
            coordinate_system=request.coordinate_system,
            obstacles=request.obstacles,
            return_image=request.return_image,
            return_overlay=request.return_overlay
        )
        
        return PathRenderResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/render/image")
async def render_path_image(request: PathRenderRequest):
    """Render path and return as PNG image"""
    try:
        renderer = PathRenderer(request.map_filename)
        
        result = renderer.render(
            method=request.method,
            points=request.points,
            style=request.style,
            coordinate_system=request.coordinate_system,
            obstacles=request.obstacles,
            return_image=True,
            return_overlay=False
        )
        
        if result.get("image_base64"):
            image_bytes = base64.b64decode(result["image_base64"])
            return Response(content=image_bytes, media_type="image/png")
        else:
            raise HTTPException(status_code=500, detail="Failed to generate image")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
