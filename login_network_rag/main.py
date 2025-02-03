from langchain.globals import set_debug, set_verbose
from login_network_rag.agent.agent import get_graph
from login_network_rag.agent.utils.visualize import save_graph_as_png
from login_network_rag.agent.utils.state import initialize_state
import dotenv
import logging
from langchain_core.messages import HumanMessage

# TEST: 디버그 시
set_debug(True)
set_verbose(True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()


def main():
    graph = get_graph()
    save_graph_as_png(graph, "workflow.png")

    while True:
        try:
            question = input("질문을 입력하세요 (종료하려면 'q' 입력): ")
            if question.lower() == "q":
                break
            state = initialize_state([HumanMessage(content=[question])])
            result = graph.invoke(state)
            # 결과 출력 형식 개선
            print("\n검색 결과:")
            print(result)
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            logger.error(f"에러 발생: {e}")
            print("검색 중 오류가 발생했습니다. 다시 시도해주세요.")


if __name__ == "__main__":
    main()
