import os
import re

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from prompts.result_prompt import RESULT_PROMPT
from prompts.metrics_code_prompt import METRICS_CODE_PROMPT
from tools.pdf_report_tool import PDFReportTool
from utils.logger import logger

import streamlit as st

class ResultAgent:

    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0.2
        )
        self.pdf_tool = PDFReportTool()

    def run(self, state):
        st.write("レポート生成開始...")
        st.write("レポート生成実行中...")

        logger.info("Result Agent Running")

        evaluation_result = state.get("evaluation_result")
        if evaluation_result is None:
            raise ValueError("evaluation_result is missing")

        # LLM generates code (metrics + charts + tables)
        code_prompt = METRICS_CODE_PROMPT.format(
            evaluation_result=evaluation_result
        )

        llm_code = self.llm.invoke([HumanMessage(content=code_prompt)]).content

        local_vars = {}
        try:
            exec(llm_code, {}, local_vars)
        except Exception as e:
            logger.error(f"LLM code execution failed: {e}")
            raise e

        # extract results from LLM-generated code
        accuracy = local_vars.get("accuracy", 0)
        precision = local_vars.get("precision", 0)
        recall = local_vars.get("recall", 0)
        f1 = local_vars.get("f1", 0)
        class_distribution = local_vars.get("class_distribution", {})
        cm = local_vars.get("cm", [])
        metrics_table_data = local_vars.get("metrics_table_data", [])

        metric_chart = "outputs/reports/metrics.png"
        confusion_chart = "outputs/reports/confusion_matrix.png"

        # LLM analysis 
        prompt = RESULT_PROMPT.format(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1,
            confusion_matrix=cm,
            total_images=evaluation_result.get("total_images"),
            class_distribution=class_distribution
        )

        response = self.llm.invoke([HumanMessage(content=prompt)])
        analysis_raw = response.content

        parts = re.split(r'\*\*(.+?)\*\*', analysis_raw)
        section_map = {}
        for i in range(1, len(parts), 2):
            section_map[parts[i].strip()] = parts[i+1].strip()

        # PDF generation via TOOL
        os.makedirs("outputs/reports", exist_ok=True)

        pdf_path = "outputs/reports/evaluation_report.pdf"

        self.pdf_tool.generate(
            pdf_path=pdf_path,
            section_map=section_map,
            metrics_table_data=metrics_table_data,
            class_distribution=class_distribution,
            total_images=evaluation_result.get("total_images", "該当データなし"),
            metric_chart=metric_chart,
            confusion_chart=confusion_chart
        )

        state["final_result"] = {"report_path": pdf_path}
        logger.info("PDF Report Generated")

        st.write("レポート生成完了...")
        return state