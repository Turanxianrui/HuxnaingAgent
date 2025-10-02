# -*- coding: utf-8 -*-  
"""
火山引擎图像生成 MCP 服务器
使用火山引擎 Seedream 4.0 API 进行图像生成
"""
import os
from openai import OpenAI
import requests
import json
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP 

# 创建一个 MCP 服务器实例，专门用于图像生成
mcp = FastMCP("火山引擎图像生成服务")

# 火山引擎 API 配置
VOLC_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
VOLC_API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

def _get_api_key(api_key: Optional[str] = None) -> Optional[str]:
    """
    获取API密钥的辅助函数
    
    参数:
    - api_key: 可选的API密钥
    
    返回:
    - API密钥字符串或None
    """
    if api_key is None:
        api_key = os.environ.get("ARK_API_KEY")
    return api_key

def _create_error_response(message: str) -> Dict[str, Any]:
    """
    创建错误响应的辅助函数
    
    参数:
    - message: 错误消息
    
    返回:
    - 标准化的错误响应字典
    """
    return {
        "success": False,
        "error": message,
        "message": "操作失败"
    }

@mcp.tool()
def generate_image(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "ep-20251002170303-b2mr4",
    size: str = "2K",
    watermark: bool = True
) -> Dict[str, Any]:
    """
    使用火山引擎 Seedream API 生成图像
    
    参数:
    - prompt: 图像生成的文本描述（建议不超过300个汉字或600个英文单词）
    - api_key: 火山引擎 API 密钥，如果不提供则从环境变量ARK_API_KEY读取
    - model: 使用的模型，默认为 ep-20251002170303-b2mr4
    - size: 图像尺寸，默认为 2K
    - watermark: 是否添加水印，默认为 True
    
    返回:
    - 包含生成图像信息的字典
    """
    
    # 从环境变量获取API密钥
    api_key = _get_api_key(api_key)
    if not api_key:
        return _create_error_response("API密钥未提供，请设置ARK_API_KEY环境变量或传入api_key参数")
    
    try:
        # 初始化OpenAI客户端
        client = OpenAI(
            base_url=VOLC_BASE_URL,
            api_key=api_key,
        )
        
        # 调用图像生成API
        images_response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            response_format="url",
            extra_body={
                "watermark": watermark,
            },
        )
        
        return {
            "success": True,
            "data": {
                "url": images_response.data[0].url,
                "model": model,
                "size": size,
                "watermark": watermark
            },
            "message": "图像生成成功"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "图像生成失败"
        }

@mcp.tool()
def generate_image_with_reference(
    prompt: str,
    reference_image_url: str,
    api_key: Optional[str] = None,
    model: str = "ep-20251002170303-b2mr4",
    size: str = "2048x2048"
) -> Dict[str, Any]:
    """
    使用参考图像生成新图像
    
    参数:
    - prompt: 图像生成的文本描述
    - reference_image_url: 参考图像的URL
    - api_key: 火山引擎 API 密钥，如果不提供则从环境变量ARK_API_KEY读取
    - model: 使用的模型，默认为 ep-20251002170303-b2mr4
    - size: 图像尺寸，默认为 2048x2048
    
    返回:
    - 包含生成图像信息的字典
    """
    
    # 从环境变量获取API密钥
    api_key = _get_api_key(api_key)
    if not api_key:
        return _create_error_response("API密钥未提供，请设置ARK_API_KEY环境变量或传入api_key参数")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "image": reference_image_url,
        "size": size,
        "sequential_image_generation": "disabled",
        "stream": False
    }
    
    try:
        response = requests.post(VOLC_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return {
            "success": True,
            "data": result,
            "message": "基于参考图像的图像生成成功"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "基于参考图像的图像生成失败"
        }

@mcp.tool()
def generate_image_sequence(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "ep-20251002170303-b2mr4",
    size: str = "2048x2048",
    max_images: int = 4
) -> Dict[str, Any]:
    """
    生成一组相关联的图像（组图功能）
    
    参数:
    - prompt: 图像生成的文本描述
    - api_key: 火山引擎 API 密钥，如果不提供则从环境变量ARK_API_KEY读取
    - model: 使用的模型，默认为 ep-20251002170303-b2mr4
    - size: 图像尺寸，默认为 2048x2048
    - max_images: 最多生成的图片数量，默认为4张
    
    返回:
    - 包含生成图像序列信息的字典
    """
    
    # 从环境变量获取API密钥
    api_key = _get_api_key(api_key)
    if not api_key:
        return _create_error_response("API密钥未提供，请设置ARK_API_KEY环境变量或传入api_key参数")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "sequential_image_generation": "auto",
        "sequential_image_generation_options": {
            "max_images": min(max_images, 15)  # 限制最大值为15
        },
        "stream": False
    }
    
    try:
        response = requests.post(VOLC_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return {
            "success": True,
            "data": result,
            "message": f"成功生成图像序列，最多{max_images}张图片"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "图像序列生成失败"
        }

@mcp.resource("image-models://supported")
def get_supported_models() -> str:
    """
    获取支持的图像生成模型列表
    """
    models_info = {
        "ep-20251002170303-b2mr4": {
            "description": "火山引擎 Seedream 4.0 图像生成模型",
            "capabilities": ["text-to-image", "image-to-image", "sequential-generation"],
            "max_resolution": "4096x4096"
        }
    }
    
    return json.dumps(models_info, ensure_ascii=False, indent=2)

@mcp.prompt()
def create_image_prompt(
    subject: str,
    style: str = "realistic",
    mood: str = "neutral",
    composition: str = "centered"
) -> str:
    """
    创建优化的图像生成提示词
    
    参数:
    - subject: 主题内容
    - style: 艺术风格（realistic, cartoon, oil_painting, watercolor等）
    - mood: 情绪氛围（happy, mysterious, dramatic, peaceful等）
    - composition: 构图方式（centered, rule_of_thirds, close_up, wide_shot等）
    """
    
    style_templates = {
        "realistic": "高质量写实风格",
        "cartoon": "卡通动画风格",
        "oil_painting": "油画艺术风格",
        "watercolor": "水彩画风格",
        "digital_art": "数字艺术风格",
        "photography": "摄影风格"
    }
    
    mood_templates = {
        "happy": "明亮愉快的氛围",
        "mysterious": "神秘朦胧氛围",
        "dramatic": "戏剧性的光影效果",
        "peaceful": "宁静祥和氛围",
        "energetic": "充满活力的氛围"
    }
    
    composition_templates = {
        "centered": "居中构图",
        "rule_of_thirds": "三分法构图",
        "close_up": "特写镜头",
        "wide_shot": "广角全景",
        "portrait": "肖像构图"
    }
    
    style_desc = style_templates.get(style, style)
    mood_desc = mood_templates.get(mood, mood)
    composition_desc = composition_templates.get(composition, composition)
    
    return f"{subject}，{style_desc}，{mood_desc}，{composition_desc}，高质量，细节丰富，专业摄影"

if __name__ == "__main__":
    # 运行 MCP 服务器
    # 这会启动服务器并等待来自 AI 客户端的连接
    mcp.run(transport="stdio")
