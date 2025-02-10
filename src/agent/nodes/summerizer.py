from langchain_core.messages import RemoveMessage
from langchain_openai import ChatOpenAI

from agent.utils.constants import MODEL
from agent.utils.parse import message_to_text
from agent.utils.prompts import SUMMARIZE_PROMPT
from agent.utils.state import AgentState


# TODO: 이 노드 붙이기
def summarizer(state: AgentState):
    messages = state["messages"]
    if len(state["messages"]) > 10:
        llm = ChatOpenAI(model=MODEL, temperature=0)
        chain = SUMMARIZE_PROMPT | llm
        conversation = message_to_text(messages)
        res = chain.invoke({"conversation": conversation})
        return {
            "messages": [RemoveMessage(id=m.id) for m in messages[:-3]],
            "summary": res.content,
        }
