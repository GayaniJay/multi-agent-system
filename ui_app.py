import streamlit as st
from core.graph_builder import build_graph

# page config
st.set_page_config(
    page_title="AI Model Evaluation System",
    layout="centered"
)

# header
st.markdown("""
# モデル評価エージェントシステム
モデルの評価と性能報告書生成を行います
""")

st.divider()

import os

# input section
st.subheader("データセット選択")

BASE_DATASET_DIR = "datasets/test_dataset"

def get_dataset_folders(base_path):
    if not os.path.exists(base_path):
        return []
    
    return [
        name for name in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, name))
    ]

dataset_folders = get_dataset_folders(BASE_DATASET_DIR)

if not dataset_folders:
    st.warning("datasetsフォルダにデータセットが存在しません")
    dataset_path = ""
else:
    selected_folder = st.selectbox(
        "データセットを選択してください",
        dataset_folders
    )

    dataset_path = os.path.join(BASE_DATASET_DIR, selected_folder)


# button
col1, col2, col3 = st.columns([1,2,1])

with col2:
    run_button = st.button("評価開始", use_container_width=True)

st.divider()

# execution
if run_button:
    if dataset_path.strip() == "":
        st.warning("データセットのパスを選択してください")
    else:
        with st.status("エージェント処理フロー実行中...", expanded=True) as status:
            
            graph = build_graph()

            state = {
                "dataset_path": dataset_path,
                "evaluation_result": None,
                "final_result": None,
                "workflow_complete": False
            }

            # Only stream state (NO UI logging here)
            for event in graph.stream(state):
                for _, output in event.items():
                    state.update(output)

            # Final status update only
            status.update(
                label="評価プロセスが完了しました！",
                state="complete",
                expanded=False
            )

        # result
        if state.get("final_result"):

            report_path = state["final_result"]["report_path"]

            with open(report_path, "rb") as file:
                file_bytes = file.read()

            st.success("レポートが正常に生成されました！")
            st.subheader("出力結果")

            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                    st.download_button(
                        label="評価レポートをダウンロード",
                        data=file_bytes,
                        file_name="AIモデル性能報告.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )