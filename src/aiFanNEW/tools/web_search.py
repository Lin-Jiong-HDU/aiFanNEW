import os

from zhipuai import ZhipuAI
from langchain_core.tools import tool

from dotenv import load_dotenv
load_dotenv()

@tool
def web_search(
    query:str | None=None,
    count:int | None=3
):
    """
    网络搜索工具
    
    参数：
    - query (str): 搜索关键词
    - count (int): 返回结果数量,默认为3非必要不修改
    
    返回：
    - ans (str): 搜索结果
    """
    client = ZhipuAI(api_key=os.getenv("API_KEY"))
    response = client.web_search.web_search(
        search_engine="search_pro",
        search_query=query,
        count=count,
        # search_domain_filter=domain,
        search_recency_filter='noLimit',
        content_size='high'
    )
    ans = ""
    for i in response.search_result:
        ans += f"标题: {i.title}\n链接: {i.link}\n内容: {i.content}\n\n"
    
    return ans

# print(web_search(query='2025年4月的财经新闻'))
# print(search_financial_news(query="2025年4月的财经新闻").search_result)