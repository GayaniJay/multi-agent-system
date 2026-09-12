from langgraph.graph import StateGraph, END

from agents.supervisor_agent import SupervisorAgent
from agents.evaluation_agent import EvaluationAgent
from agents.result_agent import ResultAgent

from core.state_manager import AgentState
from utils import logger


def build_graph():

    supervisor = SupervisorAgent()
    evaluation = EvaluationAgent()
    result = ResultAgent()

    workflow = StateGraph(AgentState)

    workflow.add_node("supervisor", supervisor.run)
    workflow.add_node("evaluation", evaluation.run)
    workflow.add_node("result", result.run)

    workflow.set_entry_point("supervisor")

    def route(state):
        action = state.get("next_action")
        if not action:
            return "supervisor"  # fallback
        elif action == "run_evaluation":
            return "evaluation"
        elif action == "generate_report":
            return "result"
        elif action == "finish":
            return END
        else:
            return END


    workflow.add_conditional_edges("supervisor", route)

    workflow.add_edge("evaluation", "supervisor")
    workflow.add_edge("result", "supervisor")

    compiled = workflow.compile()
    return compiled

def run_workflow(dataset_path):
    graph = build_graph()

    state = {
        "dataset_path": dataset_path,
        "evaluation_result": None,
        "final_result": None
    }

    MAX_ITERATIONS = 50  # prevent recursion errors

    for i in range(MAX_ITERATIONS):
        state = graph.invoke(state)

        if state.get("workflow_complete"):
            break
    else:
        logger.info("Workflow reached maximum iterations without finishing")

    return state