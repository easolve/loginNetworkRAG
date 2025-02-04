from src.agent.agent import get_graph
from src.agent.utils.visualize import save_graph_as_png
from src.agent.utils.state import AgentState, initialize_state
from src.agent.utils.logger import logger
from langchain_core.messages import HumanMessage
from langchain.globals import set_debug, set_verbose
from langchain_core.runnables import RunnableConfig
from typing import Optional

# TEST: 디버그
set_debug(True)
set_verbose(True)


def main():
    graph = get_graph()
    config: Optional[RunnableConfig] = {"configurable": {"thread_id": "1"}}
    state: AgentState = initialize_state()
    save_graph_as_png(graph, "workflow.png")

    while True:
        try:
            question = input("질문을 입력하세요 (종료하려면 'q' 입력): ")
            if question.lower() == "q":
                break
            res = graph.invoke(
                {"messages": [HumanMessage(content=question)]},
                config,
                stream_mode="values",
            )
            print(f"답변: {res["messages"][-1].content}")
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            logger.error(f"에러 발생: {e}")
            print("검색 중 오류가 발생했습니다. 다시 시도해주세요.")


if __name__ == "__main__":
    main()
