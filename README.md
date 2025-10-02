# 火山引擎图像生成 MCP 服务器

基于火山引擎 Seedream API 的 MCP (Model Context Protocol) 服务器，提供强大的图像生成功能。

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
| doubao-seedream-4.0 | 文生图、图生图、组图生成 | 4096x4096 |
| doubao-seedream-3.0-t2i | 文本生成图像 | 2048x2048 |
| doubao-seededit-3.0-i2i | 图像编辑 | 2048x2048 |

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
    "volc-image-generator": {
      "command": "D:\\Desktop\\mcp-test\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Desktop\\mcp-test\\main.py"
      ]
    }
  }
}
```

## 使用示例

### 基础图像生成

```python
# 通过 MCP 客户端调用
generate_image(
    prompt="一只可爱的小猫坐在花园里，阳光明媚",
    api_key="your_volc_api_key",
    model="doubao-seedream-4.0",
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

## API 密钥获取

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通豆包大模型服务
3. 获取 API 密钥
4. 在调用工具时传入 `api_key` 参数

## 注意事项

- 请确保你有有效的火山引擎 API 密钥
- 图像生成可能需要一些时间，请耐心等待
- 建议提示词不超过300个汉字或600个英文单词
- 生成的图像会通过 API 响应返回，包含图像URL或Base64数据

## 技术支持

- 基于 FastMCP 框架构建
- 使用火山引擎 Seedream 4.0 API
- 支持多种图像生成模式和参数配置

## 许可证

MIT License