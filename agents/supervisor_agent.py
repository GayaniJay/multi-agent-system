from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from prompts.supervisor_prompt import SUPERVISOR_PROMPT
from utils.logger import logger

class SupervisorAgent:

    def __init__(self):

        self.llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0
        )

    def run(self, state):

        if state.get("workflow_complete"):
            return state

        logger.info("Supervisor Agent Running")

        # extract current state variables
        dataset_path = state.get("dataset_path")
        evaluation_result = state.get("evaluation_result")
        final_result = state.get("final_result")

        # construct prompt for LLM decision - making
        prompt = f"""
        {SUPERVISOR_PROMPT}

        Current State:
        - dataset_path: {dataset_path}
        - evaluation_result: {evaluation_result}
        - final_result: {final_result}
        """

        # invoke LLM to determine next action
        response = self.llm.invoke(
            [HumanMessage(content=prompt)]
        )

        decision = response.content.strip()

        # validate LLM output to ensure it matches expected actions
        if decision not in ["run_evaluation", "generate_report", "finish"]:
            logger.info(f"LLM returned invalid decision '{decision}', defaulting to generate_report")
            decision = "generate_report"

        logger.info(f"Supervisor Decision: {decision}")

        # state next action in shared state
        state["next_action"] = decision

        state["workflow_complete"] = decision == "finish"

        # console logs for workflow visibility
        if decision == "run_evaluation":
            print("\nStarting evaluation...")

        elif decision == "generate_report":
            print("\nEvaluation completed. Sending results to Result Agent.")

        elif decision == "finish":
            print("\nFINAL REPORT GENERATED")
            # safty check : ensure final_result exists before printing path
            if final_result and not state.get("workflow_complete"):
                state["next_action"] = "finish"
                state["workflow_complete"] = True
                print("Report Path:", final_result["report_path"])
       
        return state