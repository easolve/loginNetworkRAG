from langchain_openai import ChatOpenAI

from agent.nodes.tool_node import tools
from agent.utils.constants import MODEL, Mode
from agent.utils.prompts import KNOWLEDGE_AGENT_PROMPT, TASK_AGENT_PROMPT
from agent.utils.state import AgentState


def cc_agent(state: AgentState):
    """
    LLM이 자체적으로 답변을 하거나 메뉴얼 기반의 답변을 제공하는 노드
    """

    messages = "".join([str(m.content) for m in state["messages"] if isinstance(m.content, str)])
    model_with_tools = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)
    mode = state["mode"]

    if mode == Mode.KNOWLEDGE:
        chain = KNOWLEDGE_AGENT_PROMPT | model_with_tools
        retrieved = state["similar_manual"]
        res = chain.invoke(
            {
                "messages": messages,
                "similar_input": retrieved["similar_input"],
                "manual": retrieved["manual"],
                "info": retrieved["info"],
            }
        )
    else:
        chain = TASK_AGENT_PROMPT | model_with_tools
        res = chain.invoke({"messages": messages})

    return {"messages": [res]}
