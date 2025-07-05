import uuid

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_community.chat_models import ChatZhipuAI
from langchain.prompts import ChatPromptTemplate, Prompt, prompt
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from search_module import web_search

@tool
def get_user_age(name: str) -> str:
    """Use this tool to find the user's age."""
    # This is a placeholder for the actual implementation
    if "bob" in name.lower():
        return "42 years old"
    return "41 years old"

system_message = """你是一个专业的教学助手，可以回答各种学科的问题。
当遇到复杂或需要最新信息的问题时，你应该使用web_search工具查找信息。
当被要求生成试卷时，使用web_search工具搜集相关题目内容，并按照标准格式生成试卷。
试卷应该包含标题、说明、题目列表（每题包含题干和选项或答题空间）。
以Markdown格式返回所有内容。
"""

memory = MemorySaver()
model = ChatZhipuAI(
    model="glm-4-plus",
    temperature=0.7,
    api_key='0bddee9d3941472190afbf400421ce53.8uSHRUrJiQLnEmGi'
)



app = create_react_agent(
    model,
    tools=[web_search],
    checkpointer=memory,
)

# The thread id is a unique key that identifies
# this particular conversation.
# We'll just generate a random uuid here.
# This enables a single application to manage conversations among multiple users.

thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

# Tell the AI that our name is Bob, and ask it to use a tool to confirm
# that it's capable of working like an agent.
input_message = HumanMessage(content="你是谁？")

# for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
#     event["messages"][-1].pretty_print()

# input_message = HumanMessage(content="如何计算二重积分？")

# for event in app.stream({"messages": [input_message]}, config, stream_mode="custom"):
#     print(event)

for token, metadata in app.stream(
    {"messages": [{"role": "user", "content": "如何计算二重积分？"}]},
    config,
    stream_mode="messages"
):
    print(token.content, end = "")
