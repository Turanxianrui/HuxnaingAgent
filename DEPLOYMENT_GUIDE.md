# 火山引擎图像生成 MCP 服务器 - 部署使用教程

## 📋 目录

1. [项目概述](#项目概述)
2. [系统要求](#系统要求)
3. [环境准备](#环境准备)
4. [安装部署](#安装部署)
5. [配置说明](#配置说明)
6. [启动服务](#启动服务)
7. [客户端集成](#客户端集成)
8. [功能使用](#功能使用)
9. [故障排除](#故障排除)
10. [最佳实践](#最佳实践)

## 🎯 项目概述

本项目是一个基于火山引擎 Seedream API 的 MCP (Model Context Protocol) 服务器，提供强大的 AI 图像生成功能。支持文本生成图像、图像编辑、组图生成等多种功能。

### 主要功能
- **文本生成图像**：根据文本描述生成高质量图像
- **参考图像生成**：基于参考图像和文本描述生成新图像
- **图像序列生成**：生成一组相关联的图像（组图功能）
- **智能提示词生成**：自动优化图像生成提示词
- **多模型支持**：支持多种火山引擎图像生成模型

## 💻 系统要求

### 硬件要求
- **CPU**: 双核及以上
- **内存**: 4GB 及以上
- **存储**: 1GB 可用空间
- **网络**: 稳定的互联网连接

### 软件要求
- **操作系统**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 18.04+)
- **Python**: 3.13 及以上版本
- **包管理器**: uv (推荐) 或 pip

## 🛠️ 环境准备

### 1. 安装 Python 3.13+

#### Windows
```powershell
# 从官网下载安装包
# https://www.python.org/downloads/windows/

# 或使用 winget
winget install Python.Python.3.13
```

#### macOS
```bash
# 使用 Homebrew
brew install python@3.13

# 或使用 pyenv
pyenv install 3.13.0
pyenv global 3.13.0
```

#### Linux (Ubuntu/Debian)
```bash
# 添加 deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-pip
```

### 2. 安装 uv 包管理器（推荐）

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. 获取火山引擎 API 密钥

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 注册并登录账户
3. 开通豆包大模型服务
4. 在 API 管理页面创建并获取 API 密钥
5. 记录您的 API 密钥，后续配置时需要使用

## 📦 安装部署

### 1. 克隆或下载项目

```bash
# 如果项目在 Git 仓库中
git clone <repository-url>
cd mcp-test

# 或直接下载项目文件到本地目录
```

### 2. 创建虚拟环境

```bash
# 使用 uv（推荐）
uv venv

# 或使用 Python 内置 venv
python -m venv .venv
```

### 3. 激活虚拟环境

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 4. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
# 如果没有 requirements.txt，手动安装依赖
pip install "mcp[cli]>=1.15.0" "requests>=2.31.0" "openai>=2.0.0"
```

## ⚙️ 配置说明

### 1. 环境变量配置

创建 `.env` 文件（可选）：

```bash
# .env 文件
ARK_API_KEY=your_volc_api_key_here
```

### 2. MCP 客户端配置

#### 方法一：使用配置文件
编辑 `json/mcp_config.json` 文件：

```json
{
  "mcpServers": {
    "volc-image-generator": {
      "command": "/path/to/your/project/.venv/Scripts/python.exe",
      "args": [
        "/path/to/your/project/main.py"
      ],
      "env": {
        "ARK_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

#### 方法二：直接在 MCP 客户端中配置
如果您使用的是 Claude Desktop 或其他 MCP 客户端，在其配置文件中添加：

```json
{
  "mcpServers": {
    "volc-image-generator": {
      "command": "D:\\Desktop\\mcp-test\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Desktop\\mcp-test\\main.py"
      ],
      "env": {
        "ARK_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

**重要提示**：
- 将 `your_actual_api_key_here` 替换为您的真实 API 密钥
- 将路径替换为您的实际项目路径
- Windows 路径使用双反斜杠 `\\` 或正斜杠 `/`

## 🚀 启动服务

### 1. 测试运行

```bash
# 激活虚拟环境
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 运行服务器
python main.py
```

如果配置正确，您应该看到服务器启动信息。

### 2. 验证安装

创建一个测试脚本 `test_server.py`：

```python
import os
import sys
sys.path.append('.')

from main import generate_image

# 测试基础图像生成功能
result = generate_image(
    prompt="一只可爱的小猫坐在花园里",
    api_key="your_api_key_here"  # 替换为您的 API 密钥
)

print("测试结果:", result)
```

运行测试：
```bash
python test_server.py
```

## 🔌 客户端集成

### 1. Claude Desktop 集成

1. 找到 Claude Desktop 的配置文件：
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. 编辑配置文件，添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "volc-image-generator": {
      "command": "D:\\Desktop\\mcp-test\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\Desktop\\mcp-test\\main.py"
      ],
      "env": {
        "ARK_API_KEY": "your_actual_api_key_here"
      }
    }
  }
}
```

3. 重启 Claude Desktop

### 2. 其他 MCP 客户端

对于其他支持 MCP 的客户端，请参考其文档进行配置。基本配置格式相同。

## 🎨 功能使用

### 1. 基础图像生成

```python
# 通过 MCP 客户端调用
generate_image(
    prompt="一只可爱的小猫坐在花园里，阳光明媚，高质量摄影",
    model="ep-20251002170303-b2mr4",
    size="2K",
    watermark=True
)
```

### 2. 参考图像生成

```python
generate_image_with_reference(
    prompt="将这张图片转换为油画风格",
    reference_image_url="https://example.com/image.jpg",
    model="ep-20251002170303-b2mr4",
    size="2048x2048"
)
```

### 3. 图像序列生成

```python
generate_image_sequence(
    prompt="一个故事的四个场景：春夏秋冬",
    model="ep-20251002170303-b2mr4",
    size="2048x2048",
    max_images=4
)
```

### 4. 智能提示词生成

```python
create_image_prompt(
    subject="一只小猫",
    style="realistic",
    mood="peaceful",
    composition="centered"
)
```

### 5. 获取支持的模型

```python
# 通过资源获取
get_supported_models()
```

## 🔧 故障排除

### 常见问题及解决方案

#### 1. API 密钥错误
**问题**: `API密钥未提供，请设置ARK_API_KEY环境变量`

**解决方案**:
- 检查 API 密钥是否正确设置
- 确认环境变量 `ARK_API_KEY` 已配置
- 验证 API 密钥是否有效

#### 2. 依赖安装失败
**问题**: 安装依赖时出现错误

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 清理缓存重新安装
pip cache purge
pip install -r requirements.txt

# 或使用 uv
uv sync --reinstall
```

#### 3. 服务器启动失败
**问题**: 运行 `python main.py` 时出错

**解决方案**:
- 检查 Python 版本是否为 3.13+
- 确认所有依赖已正确安装
- 查看错误日志，根据具体错误信息解决

#### 4. MCP 客户端连接失败
**问题**: 客户端无法连接到 MCP 服务器

**解决方案**:
- 检查配置文件路径是否正确
- 确认 Python 可执行文件路径正确
- 验证 main.py 文件路径正确
- 重启 MCP 客户端

#### 5. 图像生成失败
**问题**: 调用图像生成功能时失败

**解决方案**:
- 检查网络连接
- 验证 API 密钥权限
- 确认提示词格式正确
- 检查模型参数是否支持

### 日志调试

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 最佳实践

### 1. 安全性
- **不要在代码中硬编码 API 密钥**
- 使用环境变量或配置文件管理敏感信息
- 定期轮换 API 密钥
- 限制 API 密钥的访问权限

### 2. 性能优化
- **合理设置图像尺寸**：根据需求选择合适的分辨率
- **优化提示词**：使用 `create_image_prompt` 函数生成优化的提示词
- **批量处理**：对于多张图片，考虑使用图像序列生成功能
- **缓存结果**：对于相同的请求，可以缓存生成结果

### 3. 提示词优化
- 保持提示词简洁明确
- 使用具体的描述词汇
- 包含风格、情绪、构图等关键信息
- 避免过于复杂的描述

### 4. 错误处理
- 始终检查 API 响应的 `success` 字段
- 实现重试机制处理临时网络错误
- 记录错误日志便于调试
- 为用户提供友好的错误信息

### 5. 监控和维护
- 监控 API 使用量和成本
- 定期更新依赖包
- 备份重要的配置文件
- 监控服务器运行状态

## 📞 技术支持

如果您在部署或使用过程中遇到问题，可以：

1. 查看项目的 README.md 文件
2. 检查火山引擎官方文档
3. 查看 MCP 协议相关文档
4. 在项目仓库中提交 Issue

## 📄 许可证

本项目采用 MIT 许可证，详情请查看 LICENSE 文件。

---

**祝您使用愉快！** 🎉