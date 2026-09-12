from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from prompts.evaluatiom_prompt import EVALUATION_PROMPT
from utils.logger import logger

import streamlit as st

class EvaluationAgent:

    def __init__(self):
        st.write("モデル評価プロセス開始...")
        st.write("モデル評価プロセス実行中...")
        self.llm = ChatOpenAI(model="gpt-4.1", temperature=0)

    def run(self, state):

        logger.info("Evaluation Agent Running")

        if state.get("evaluation_result") is not None:
            logger.info("Skipping evaluation (already exists)")
            return state

        # prompt
        prompt = EVALUATION_PROMPT.format(
            dataset_path=state.get("dataset_path")
        )

        # LLM generates code
        response = self.llm.invoke([HumanMessage(content=prompt)])
        generated_code = response.content.strip()

        logger.info("Generated evaluation code from LLM")

        generated_code = response.content.strip()

        # clean LLM output
        if "```" in generated_code:
            generated_code = generated_code.split("```")[1]

            if generated_code.startswith("python"):
                generated_code = generated_code[len("python"):]

        generated_code = generated_code.strip()

        # execute code
        local_vars = {}

        try:
            exec(generated_code, {}, local_vars)

            evaluation_result = local_vars.get("evaluation_result")

            if evaluation_result is None:
                raise ValueError("LLM code did not produce evaluation_result")

            state["evaluation_result"] = evaluation_result

            logger.info("Evaluation completed successfully")

        except Exception as e:
            logger.error(f"Evaluation execution failed: {e}")
            raise e

        st.write("モデル評価完了...") 
        return state