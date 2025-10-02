# 火山引擎 Seedream 4.0 图像生成 MCP 服务器

基于火山引擎 Seedream 4.0 API 的 MCP (Model Context Protocol) 服务器，提供强大的图像生成功能。

## 功能特性

### 🎨 图像生成工具

1. **基础图像生成** (`generate_image`)
   - 根据文本描述生成高质量图像
   - 支持多种分辨率和模型选择
   - 可选择单图或组图模式

2. **参考图像生成** (`generate_image_with_reference`)
   - 基于参考图像和文本描述生成新图像
   - 支持图像风格转换和内容修改

3. **图像序列生成** (`generate_image_sequence`)
   - 生成一组相关联的图像（组图功能）
   - 最多支持15张图片的序列生成

### 📚 资源和提示词

- **模型信息资源** (`image-models://supported`)：获取支持的图像生成模型列表
- **智能提示词生成** (`create_image_prompt`)：根据主题、风格、情绪和构图自动生成优化的提示词

## 支持的模型

| 模型 | 功能 | 最大分辨率 |
|------|------|------------|
| Seedream 4.0 (ep-20251002170303-b2mr4) | 文生图、图生图、组图生成 | 4096x4096 |

## 安装和配置

### 1. 安装依赖

```bash
uv sync
```

### 2. 启动服务器

```bash
python main.py
```

### 3. MCP 客户端配置

在你的 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "seedream-4.0-image-mcp": {
      "command": "D:\\Desktop\\mcp-test\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Desktop\\mcp-test\\main.py"
      ],
      "env": {
        "ARK_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**注意：** 将 `your-api-key-here` 替换为你的实际API密钥。

## 使用示例

### 基础图像生成

```python
# 通过 MCP 客户端调用
generate_image(
    prompt="一只可爱的小猫坐在花园里，阳光明媚",
    model="ep-20251002170303-b2mr4",  # Seedream 4.0
    size="2048x2048"
)
```

### 使用智能提示词

```python
# 生成优化的提示词
create_image_prompt(
    subject="一只小猫",
    style="realistic",
    mood="peaceful",
    composition="centered"
)
# 输出: "一只小猫，高质量写实风格，宁静祥和的氛围，居中构图，高质量，细节丰富，专业摄影"
```

## 环境变量配置

### 方式1：MCP配置文件（推荐）

直接在MCP客户端配置文件的 `env` 字段中设置API密钥，如上面的配置示例所示。

### 方式2：系统环境变量

如果需要在系统级别设置环境变量：

**Windows (PowerShell):**
```powershell
$env:ARK_API_KEY = "your-api-key-here"
```

**Linux/Mac:**
```bash
export ARK_API_KEY="your-api-key-here"
```

### API 密钥获取

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通豆包大模型服务
3. 获取 API 密钥
4. 按上述方法设置环境变量

## 注意事项

- API密钥已在MCP配置文件中设置，无需额外配置环境变量
- 图像生成可能需要一些时间，请耐心等待
- 建议提示词不超过300个汉字或600个英文单词
- 生成的图像会通过 API 响应返回，包含图像URL或Base64数据
- API密钥通过MCP配置管理，不会暴露在代码中，确保安全性

## 技术支持

- 基于 FastMCP 框架构建
- 使用火山引擎 Seedream 4.0 API
- 支持多种图像生成模式和参数配置
- 通过环境变量安全管理API密钥

## 许可证

MIT License
