from agent.utils.state import AgentState
from agent.utils.constants import MODEL
from agent.utils.prompts import AGENT_PROMPT
from agent.nodes.tool_node import tools
from langchain_openai import ChatOpenAI


def cc_agent(state: AgentState):
    messages = "".join([str(m.content) for m in state["messages"] if isinstance(m.content, str)])
    model_with_tools = ChatOpenAI(model=MODEL, temperature=0).bind_tools(tools)
    chain = AGENT_PROMPT | model_with_tools
    retrieved = state["similar_manual"]
    res = chain.invoke(
        {
            "messages": messages,
            "similar_input": retrieved["similar_input"],
            "manual": retrieved["manual"],
            "info": retrieved["info"],
        }
    )
    return {"messages": [res]}


if __name__ == "__main__":
    print("This is a CC agent.")
