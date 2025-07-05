import os
from dotenv import load_dotenv

from langchain_community.chat_models import ChatZhipuAI

load_dotenv()

model = ChatZhipuAI(
    model="glm-4-plus",
    temperature=0.7,
    api_key = os.getenv("API_KEY"),
)
def get_model():
    """
    获取当前使用的语言模型实例。
    
    返回：
    - model: ChatZhipuAI 实例
    """
    return model