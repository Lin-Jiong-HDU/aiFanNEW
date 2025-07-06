
import os
import uuid

from langchain_community.chat_models import ChatZhipuAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from aiFanNEW.workflow.testpaper_generate import generate_test_paper
from aiFanNEW.tools.web_search import web_search

from dotenv import load_dotenv
load_dotenv()

class mainAgent:
    def __init__(self):
        self.memory = MemorySaver()
        self.model = ChatZhipuAI(
            model="glm-4-plus",
            temperature=0.7,
            api_key = os.getenv("API_KEY"),
        )
        self.system_message = SystemMessage(
            content="""你是一个专业的教学助手,你叫范小教，可以回答各种学科的问题。你的功能有：
            1. 回答学生的问题，提供详细的解答和解释。如果遇到复杂问题可以先使用web_search工具查找信息。
            2. 当被要求生成试卷时，使用generate_test_paper工具生成试卷。
            """
        )
        self.tools = [
            web_search,
            generate_test_paper
        ]
        self.app = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=self.memory,
        )

        self.thread_id = uuid.uuid4()
        self.config = {"configurable": {"thread_id": self.thread_id}}

    def get_app(self):
        return self.app, self.config
    
    def run(self, user_input):
        """
        运行主代理，处理用户输入并返回响应。
        
        参数：
        - user_input (str): 用户输入的消息内容
        
        """

        user_input = HumanMessage(content=user_input)
        for token, metadata in self.app.stream(
            {"messages": [self.system_message, user_input]},
            config=self.config,
            stream_mode="messages"
        ):
            if isinstance(token, AIMessage):    
                print(token.content, end="")
    
    
    def run_stream(self, user_input):
        """流式输出版本"""
        user_input = HumanMessage(content=user_input)
        for token, metadata in self.app.stream(
            {"messages": [self.system_message, user_input]},
            config=self.config,
            stream_mode="messages"
        ):
            if isinstance(token, AIMessage):    
                yield token.content

# if __name__ == "__main__":
#     agent = mainAgent()
#     print("欢迎使用范小教教学助手！请问有什么可以帮助您的？")
    
#     while True:
#         user_input = input("您: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("感谢使用范小教教学助手，再见！")
#             break
#         agent.run(user_input)
