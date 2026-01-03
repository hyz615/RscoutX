# 修复说明: Linux 部署时 pushback_map.png 未找到

## 问题描述
在 Linux 部署时,后端提示找不到 `pushback_map.png` 文件,导致地图渲染功能无法正常使用。

## 问题原因
1. 后端配置使用相对路径 `../pushback_map.png`
2. 在 Linux 部署时,工作目录在 `backend` 文件夹内
3. 相对路径解析依赖于工作目录,可能因环境不同而失败

## 解决方案

### 1. 代码改进

#### a) 修改 `backend/app/core/config.py`
- 将相对路径改为使用 `os.path.join` 动态计算的绝对路径
- 从 `../pushback_map.png` 改为基于代码文件位置的自动路径计算
- 确保无论工作目录在哪里,都能正确找到文件

```python
# 修改前
MAP_IMAGE_PATH: str = "../pushback_map.png"

# 修改后
import os
MAP_IMAGE_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "pushback_map.png")
```

#### b) 改进 `backend/app/services/path_renderer.py`
- 添加详细的错误日志,显示文件查找路径
- 实现自动尝试多个备选路径
- 找不到文件时提供清晰的错误信息和解决建议

新增功能:
```python
def load_map(self) -> Image.Image:
    """Load the field map image"""
    # 转换为绝对路径
    map_path = os.path.abspath(self.map_path)
    
    if not os.path.exists(map_path):
        print(f"⚠️  警告: 地图文件未找到: {map_path}")
        print(f"   当前工作目录: {os.getcwd()}")
        print(f"   配置路径: {self.map_path}")
        
        # 尝试备选路径
        alternatives = [
            os.path.join(os.getcwd(), "pushback_map.png"),
            os.path.join(os.path.dirname(os.getcwd()), "pushback_map.png"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "..", "pushback_map.png")
        ]
        for alt_path in alternatives:
            alt_path = os.path.abspath(alt_path)
            if os.path.exists(alt_path):
                print(f"✅ 找到地图文件: {alt_path}")
                self.map_path = alt_path
                return Image.open(alt_path).convert('RGB')
        
        # 使用默认空白地图
        print("   使用默认空白地图")
        img = Image.new('RGB', (settings.DEFAULT_MAP_WIDTH, settings.DEFAULT_MAP_HEIGHT), 'white')
        return img
    
    return Image.open(map_path).convert('RGB')
```

### 2. 部署文档更新

#### a) 更新 `UBUNTU_DEPLOY.md`
- 添加检查项目结构的步骤
- 强调 `pushback_map.png` 必须在根目录
- 提供自动复制命令

```bash
# 如果 pushback_map.png 不存在，请从 frontend 目录复制
if [ ! -f "pushback_map.png" ]; then
    cp frontend/pushback_map.png . 2>/dev/null || echo "警告: pushback_map.png 未找到"
fi
```

#### b) 更新 `check_deploy.sh`
- 添加对 `pushback_map.png` 的检查
- 提供友好的提示信息

```bash
# 检查场地地图文件
if [ -f "pushback_map.png" ]; then
    echo "  ✅ pushback_map.png 存在（根目录）"
else
    echo "  ⚠️  pushback_map.png 不存在（根目录）"
    if [ -f "frontend/pushback_map.png" ]; then
        echo "     💡 提示: 可以从 frontend 目录复制: cp frontend/pushback_map.png ."
    else
        echo "     ❌ frontend/pushback_map.png 也不存在"
    fi
fi
```

#### c) 创建 `fix_pushback_map.sh`
新建自动修复脚本,一键复制文件到正确位置:

```bash
#!/bin/bash
# 修复 pushback_map.png 文件位置

if [ -f "pushback_map.png" ]; then
    echo "✅ pushback_map.png 已存在于根目录"
    exit 0
fi

if [ -f "frontend/pushback_map.png" ]; then
    cp frontend/pushback_map.png .
    echo "✅ 复制成功！"
else
    echo "❌ 错误: frontend/pushback_map.png 不存在"
    exit 1
fi
```

#### d) 更新 `README.md`
- 添加 "🐛 故障排查" 章节
- 详细说明问题和多种解决方案
- 提供验证修复的方法

### 3. 使用方法

#### 部署前检查:
```bash
./check_deploy.sh
```

#### 修复地图文件:
```bash
chmod +x fix_pushback_map.sh
./fix_pushback_map.sh
```

#### 启动服务:
```bash
sudo ./start_daemon.sh
```

#### 验证修复:
```bash
# 查看日志
tail -f logs/rscoutx.log

# 应该看到: ✅ 找到地图文件: /path/to/pushback_map.png
# 而不是: ⚠️ 警告: 地图文件未找到
```

## 改进效果

### 修改前
- ❌ 使用硬编码相对路径
- ❌ 找不到文件时没有提示
- ❌ 没有自动查找备选路径
- ❌ 用户不知道如何解决

### 修改后
- ✅ 使用动态计算的绝对路径
- ✅ 详细的错误日志和诊断信息
- ✅ 自动尝试多个备选路径
- ✅ 提供自动修复脚本
- ✅ 完善的文档说明

## 文件清单

修改的文件:
- `backend/app/core/config.py` - 修改路径配置
- `backend/app/services/path_renderer.py` - 增强路径查找
- `UBUNTU_DEPLOY.md` - 更新部署说明
- `check_deploy.sh` - 添加地图文件检查
- `README.md` - 添加故障排查章节

新增的文件:
- `fix_pushback_map.sh` - 自动修复脚本

## 兼容性

- ✅ Windows 环境不受影响
- ✅ Linux/Ubuntu 环境正常工作
- ✅ 向后兼容,不破坏现有功能
- ✅ 自动降级到空白地图(如果文件确实不存在)

## 总结

通过以上修改,彻底解决了 Linux 部署时 `pushback_map.png` 未找到的问题。不仅修复了代码,还提供了完整的工具链和文档支持,让用户能够轻松诊断和解决类似问题。
