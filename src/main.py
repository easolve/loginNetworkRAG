# flake8: noqa
# pylint: disable=C0413

__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from typing import Optional

import streamlit as st
from langchain.globals import set_debug, set_verbose
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from agent.agent import get_graph
from agent.utils.logger import logger
from agent.utils.visualize import save_graph_as_png

# TEST: 디버그
set_debug(True)
set_verbose(True)


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "graph" not in st.session_state:
        st.session_state.graph = get_graph()
        save_graph_as_png(st.session_state.graph, "workflow.png")


def main():
    st.title("통관/특송 상담 챗봇")
    st.write("안녕하세요! 통관 및 특송 관련 문의사항을 편하게 물어보세요.")

    initialize_session_state()
    config: Optional[RunnableConfig] = {"configurable": {"thread_id": "1"}}

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message("user" if isinstance(message[1], HumanMessage) else "assistant"):
            st.write(message[0])

    # Chat input
    if prompt := st.chat_input("질문을 입력하세요"):
        # Add user message to chat history
        st.session_state.messages.append((prompt, HumanMessage(content=prompt)))
        with st.chat_message("user"):
            st.write(prompt)

        try:
            # Get response from graph
            with st.chat_message("assistant"):
                with st.spinner("답변을 생성하고 있습니다..."):
                    res = st.session_state.graph.invoke(
                        {"messages": [HumanMessage(content=prompt)]},
                        config,
                        stream_mode="values",
                    )

                    if isinstance(res["messages"][-1], AIMessage):
                        response = res["messages"][-1].content
                        st.write(response)
                        st.session_state.messages.append((response, res["messages"][-1]))

        except Exception as e:
            logger.error("에러 발생: %s", e)
            st.error("죄송합니다. 답변을 생성하는 중에 오류가 발생했습니다. 다시 시도해주세요.")


if __name__ == "__main__":
    main()
