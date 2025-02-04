from src.agent.agent import get_graph
from src.agent.utils.visualize import save_graph_as_png
from src.agent.utils.state import initialize_state
from src.agent.utils.logger import logger
from langchain_core.messages import HumanMessage
from langchain.globals import set_debug, set_verbose
import dotenv

# TEST: 디버그
set_debug(True)
set_verbose(True)

dotenv.load_dotenv()


def main():
    graph = get_graph()
    save_graph_as_png(graph, "workflow.png")

    while True:
        try:
            question = input("질문을 입력하세요 (종료하려면 'q' 입력): ")
            if question.lower() == "q":
                break
            state = initialize_state([HumanMessage(content=question)])
            result = graph.invoke(state)
            print("\n검색 결과:")
            print(result["messages"][-1].content)
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            logger.error(f"에러 발생: {e}")
            print("검색 중 오류가 발생했습니다. 다시 시도해주세요.")


if __name__ == "__main__":
    main()
