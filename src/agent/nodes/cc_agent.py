from langchain_openai import ChatOpenAI

from agent.nodes.tool_node import tools
from agent.utils.constants import MODEL
from agent.utils.parse import message_to_text
from agent.utils.prompts import KNOWLEDGE_AGENT_PROMPT
from agent.utils.state import AgentState


def cc_agent(state: AgentState):
    messages = message_to_text(state["messages"])
    model_with_tools = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)
    chain = KNOWLEDGE_AGENT_PROMPT | model_with_tools
    retrieved = state["similar_manual"]
    res = chain.invoke(
        {
            "messages": messages,
            "similar_input": retrieved.get("similar_input", "없음"),
            "manual": retrieved.get("manual", "없음"),
            "info": retrieved.get("info", "없음"),
        }
    )

    return {"messages": [res]}
