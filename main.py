from dotenv import load_dotenv
load_dotenv()

from core.graph_builder import build_graph
from core.state_manager import AgentState

from utils.logger import logger
from utils.messages import SYSTEM_START


def main():

    print(SYSTEM_START)

    dataset_path = input("Enter test dataset path: ")

    state: AgentState = {
        "dataset_path": dataset_path,
        "evaluation_result": None,
        "final_result": None,
        "workflow_complete": False
    }

    graph = build_graph()

    state = graph.invoke(state)

    logger.info("System Finished")


if __name__ == "__main__":
    main()