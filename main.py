from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from aiFanNEW.agent.agent import mainAgent
import os
from dotenv import load_dotenv
import asyncio

from uuid import UUID
import uuid as uuid_lib

from fastapi.middleware.cors import CORSMiddleware
# 加载环境变量（确保在FastAPI初始化前执行）
load_dotenv()

app = FastAPI(title="AI教学助手API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
agent_list = []

def get_agent(uuid: str | None = None):
    """获取当前的agent实例"""
    if uuid is None:
        uuid = str(uuid_lib.uuid4())
        agent = mainAgent(uuid=UUID(uuid))
        # uuid = str(agent.thread_id)
        agent_list.append([uuid,agent])
        return agent
    else:
        # 查找已有的agent实例
        for agent_info in agent_list:
            if agent_info[0] == uuid:
                return agent_info[1]
        # 如果没有找到，则创建新的agent实例
        agent = mainAgent(uuid=UUID(uuid))
        agent_list.append([uuid, agent])
        return agent


@app.post("/chat")
async def chat_endpoint(request: Request):
    """流式聊天接口"""
    data = await request.json()
    question = data.get("question")
    user_id = data.get("user_id")

    print(f"Received question: {question} from user_id: {user_id}")
    if user_id is None or user_id == "":
        agent = get_agent() 
    else:
        agent = get_agent(user_id)
        
    user_id = str(agent.thread_id)
    async def stream_generator():
        # 直接调用agent.run并捕获输出
        response_content = []
        for token in agent.run_stream(question):  
            response_content.append(token)
            yield f"event: content\ndata: {token}\n\n"
            await asyncio.sleep(0.01)  
        
        yield f"event: user_id\ndata: {user_id}\n\n"

    
    return StreamingResponse(stream_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)