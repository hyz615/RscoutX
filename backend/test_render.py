"""
测试路径渲染坐标一致性
"""
import sys
sys.path.insert(0, '.')

from app.services.path_renderer import PathRenderer
from app.schemas.schemas import PathPoint, PathStyle, RobotState
from PIL import Image
import io
import base64

# 创建测试路径点（800x800 画布上的坐标）
test_points = [
    PathPoint(x=100, y=100, robot_state=RobotState(state='moving')),
    PathPoint(x=200, y=150, robot_state=RobotState(state='intaking')),
    PathPoint(x=300, y=100, robot_state=RobotState(state='wingpushing')),
    PathPoint(x=400, y=200, robot_state=RobotState(state='releasing'))
]

print("测试路径渲染...")
print(f"测试点: {[(p.x, p.y) for p in test_points]}")

renderer = PathRenderer()
style = PathStyle(
    color='#FF0000',
    width=3,
    opacity=0.8,
    arrow=True,
    show_state_labels=True,
    state_icon_size=20
)

result = renderer.render(
    method='polyline',
    points=test_points,
    style=style,
    coordinate_system='pixel',
    return_image=True,
    canvas_size=(800, 800)  # 匹配前端画布尺寸
)

if result['success']:
    # 解码图片
    img_data = base64.b64decode(result['image_base64'])
    img = Image.open(io.BytesIO(img_data))
    print(f"✓ 渲染成功！图片尺寸: {img.size}")
    
    # 保存测试图片
    img.save('test_render.png')
    print(f"✓ 测试图片已保存为 test_render.png")
    print(f"  请对比这个图片与前端画布上相同坐标点的位置")
else:
    print("✗ 渲染失败")
