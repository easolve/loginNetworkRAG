from src.test_agent.agent import get_graph
from src.agent.utils.visualize import save_graph_as_png
from src.agent.utils.logger import logger
from langchain.globals import set_debug, set_verbose
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from typing import Optional

# 개인정보 오류 관련 알림톡이 왔습니다. 운송장번호는 324234 이고 통관번호는 2345346이에요.
# TEST: 디버그
set_debug(False)
set_verbose(False)


def main():
    graph = get_graph()
    config: Optional[RunnableConfig] = {"configurable": {"thread_id": "1"}}
    save_graph_as_png(graph, "workflow.png")

    while True:
        try:
            question = input("질문을 입력하세요 (종료하려면 'q' 입력): ").strip()
            if question.lower() == "q" or question.lower() == "quit":
                break
            if question == "":
                continue

            res = graph.invoke(
                {"messages": [HumanMessage(content=question)], "category": ""},
                config,
                stream_mode="values",
            )

            if isinstance(res["messages"][-1], AIMessage):
                print(f"답변: {res["messages"][-1].content}")
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            logger.error("에러 발생: %s", e)
            print("검색 중 오류가 발생했습니다. 다시 시도해주세요.")


if __name__ == "__main__":
    main()
