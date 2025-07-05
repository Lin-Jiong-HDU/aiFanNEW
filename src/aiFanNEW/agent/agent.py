
import os
import uuid

from langchain_community.chat_models import ChatZhipuAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from dotenv import load_dotenv
load_dotenv()

class mainAgent:
    def __init__(self):
        self.memory = MemorySaver()
        self.model = ChatZhipuAI(
            model="glm-4-plus",
            temperature=0.7,
            api_key = os.environ.get("ZHIPUAI_API_KEY"),  # 从环境变量中获取API密钥
        )
        self.system_message = SystemMessage(
            content="""你是一个专业的教学助手,你叫范小教，可以回答各种学科的问题。你的功能有：
            1. 回答学生的问题，提供详细的解答和解释。如果遇到复杂问题可以先使用web_search工具查找信息。
            2. 当被要求生成试卷时，使用web_search工具搜集相关题目内容，并按照标准格式生成试卷。
            3. 试卷应该包含标题、说明、题目列表（每题包含题干和选项或答题空间）。如果用户要求了试卷格式，请结合用户的要求生成合理格式的试卷。
            4. 以Markdown格式返回所有内容。
            """
        )
        self.app = create_react_agent(
            self.model,
            checkpointer=self.memory,
        )

        self.thread_id = uuid.uuid4()
        self.config = {"configurable": {"thread_id": self.thread_id}}

    def get_app(self):
        return self.app, self.config