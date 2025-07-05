# from aiFanNEW.agent.agent import mainAgent


from aiFanNEW.tools.web_search import web_search
from aiFanNEW.model.llms import get_model,model

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage,BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

def generate_test_paper():

    search_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="你是一个专业的网络搜索专家，你可以根据用户输入生成搜索词。你生成的搜索词将被用于网络搜索以获取相关信息。请确保搜索词简洁明了，足够全面，能够准确反映生成试卷所要的信息。"),
        HumanMessage(content="{user_input}"),
    ])
    model = get_model()
    search_agent = search_prompt | model | StrOutputParser()
    