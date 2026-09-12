# マルチエージェントモデル評価システム

## 概要

本プロジェクトは、複数のAIエージェントを連携させることで、機械学習パイプラインの主要な工程を自動化するマルチエージェントシステムを実装したものです。

本システムは、グラフベースのワークフローを活用して、監督・評価・結果生成を担当する各エージェントをオーケストレーションします。LLMの機能と従来の機械学習評価およびレポーティングを統合し、評価指標やPDFレポートなどの構造化された出力を生成します。

## アーキテクチャ

本システムはグラフベースのオーケストレーションモデルに基づいて構築されており、各エージェントが明確な役割を担いながら、状態（state）を次の処理段階へと受け渡します。

## エージェント
Supervisor Agent（監督エージェント）
- ワークフロー全体の制御
- 入力内容および実行フローの検証
- エージェント間の遷移（次に実行する処理）の決定

Evaluation Agent（評価エージェント）
- モデルの出力結果を処理
- 以下の評価指標を計算：
    - Accuracy（精度）
    - Precision（適合率）
    - Recall（再現率）
    - F1-score (F1スコア)
- 構造化された評価データを生成

Result Generation Agent（結果生成エージェント）
- 評価結果を人間が理解しやすいレポート形式に変換
- LLMを用いて説明文、評価指標、テーブルを生成
- 最終成果物の出力：
    - PDFレポート
    - 可視化（グラフ／チャート）

## プロジェクト構成
multi_agent_model_training_demo/
├── agents           # エージェント実装（Supervisor / Evaluation / Result）
├── core             # 状態管理およびグラフ制御
├── datasets         # 入力データセット
├── models           # 学習済みモデル
├── outputs          # 生成されたレポートおよび成果物
├── utils            # ログおよび共通ユーティリティ
├── main.py          # エントリーポイント
└── ui_app.py        # UI

## インストール
- フォルダ移動
    cd multi_agent_model_training_demo

- 仮想環境の作成
    python -m venv venv
    venv\Scripts\activate # Windows

- 依存関係のインストール
    pip install -r requirements.txt

- 設定
    Create a .env file in the root directory
    OPENAI_API_KEY=your_api_key_here

## 使用方法
- システムの実行
    python main.py

- Streamlit UIを使用する場合
    streamlit run ui_app.py



