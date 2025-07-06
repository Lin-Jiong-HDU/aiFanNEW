# from aiFanNEW.agent.agent import mainAgent


from aiFanNEW.tools.web_search import web_search_tool
from aiFanNEW.model.llms import get_model,model

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage,BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

@tool
def generate_test_paper(user_input: str) -> str:
    """"
    生成试卷的函数，根据用户输入生成搜索词，并使用网络搜索工具获取相关信息。
    参数：
    - user_input (str): 用户输入的内容，用于生成搜索词。
    返回：
    - str: 生成的试卷内容，包含标题、说明和题目列表
    """

    search_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="你是一个专业的网络搜索专家，你可以根据用户输入生成搜索词。你生成的搜索词将被用于网络搜索以获取相关信息。请确保搜索词简洁明了，足够全面，能够准确反映生成试卷所要的信息。"),
        ('human','{user_input}'),
    ])
    model = get_model()

    # print(search_prompt.invoke({"user_input": user_input}))

    search_agent = search_prompt | model | StrOutputParser()

    webSearchResult = web_search_tool(search_agent.invoke({"user_input": user_input}))

    print(f"搜索结果：{webSearchResult}")

    testpaper_generate_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="你是一个专业的试卷生成专家，你可以根据用户提供的搜索结果和用户输入来生成试卷。试卷应包含标题、说明和题目列表。题目要有选择题、填空题、简答题等，请跟据试卷类型与用户输入灵活调整试卷格式。每个题目应包含题干和选项或答题空间。请确保试卷格式合理，内容清晰易懂。试卷应为markdownown格式。只输出试卷内容，不要包含其他信息。"),
        ('human', '请根据以下搜索结果和用户输入生成试卷：\n\n搜索结果：{web_search_result}\n\n用户输入：{user_input}'),
    ])

    testpaper_generate_agent = testpaper_generate_prompt | model | StrOutputParser()
    testpaper_content = testpaper_generate_agent.invoke({
        "web_search_result": webSearchResult,
        "user_input": user_input
    })

    return testpaper_content

# print(generate_test_paper("请生成一份关于Python编程的试卷，包含选择题和简答题。"))