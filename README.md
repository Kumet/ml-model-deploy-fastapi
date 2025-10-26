# ML Model Deploy (FastAPI)

[![CI](https://github.com/Kumet/ml-model-deploy-fastapi/actions/workflows/ci.yml/badge.svg)](https://github.com/Kumet/ml-model-deploy-fastapi/actions/workflows/ci.yml)
[![Auto Review](https://github.com/Kumet/ml-model-deploy-fastapi/actions/workflows/auto-review.yml/badge.svg)](https://github.com/Kumet/ml-model-deploy-fastapi/actions/workflows/auto-review.yml)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)

FastAPI と scikit-learn を組み合わせた **ML 推論 API のプロダクションテンプレート** です。`uv` ベースの軽量な開発体験、`ruff` / `black` / `pytest` による品質ゲート、`MLflow` 連携による実験管理、Render へのデプロイ Workflow まで揃えた「そのまま案件に持ち込める」構成を目指しています。

## 目次
- [特徴](#特徴)
- [プロジェクト構成](#プロジェクト構成)
- [クイックスタート](#クイックスタート)
- [API](#api)
- [品質とオブザーバビリティ](#品質とオブザーバビリティ)
- [Makefile コマンド](#makefile-コマンド)
- [GitHub Actions](#github-actions)
- [デプロイ (Render)](#デプロイ-render)
- [環境変数](#環境変数)

## 特徴
- ⚡️ **FastAPI + scikit-learn**: Iris モデルを教材に、最小で拡張しやすい推論 API を実装。
- 🔐 **Bearer 認証**: `/auth/token` で JWT を払い出し、 `/predict` を認証下に保護。
- 📈 **可観測性**: `structlog` で JSON ログ（`request_id` / `input_id` / `latency_ms`）を出力。MLflow で精度やモデルを履歴管理。
- 🧪 **品質ゲート**: Lint / Format / Test を CI で自動検証。pre-commit も同梱。
- 🚀 **デプロイ Workflow**: Render の Deploy Hook を叩く GitHub Actions を提供。

## プロジェクト構成
```
ml-model-deploy-fastapi/
├─ models/
│  ├─ prepare_model.py   # MLflow ログ付きのモデル学習スクリプト
│  └─ model.joblib       # 学習済みモデル (生成物)
├─ src/backend/app/
│  ├─ api/               # FastAPI ルーティング & スキーマ
│  ├─ core/              # 設定・認証・ロギング
│  └─ services/          # 推論ロジック
├─ src/backend/tests/    # pytest
├─ Makefile              # ショートカットコマンド
└─ .github/workflows/    # CI / Auto Review / Deploy
```

## クイックスタート
```bash
uv sync --frozen                 # 依存インストール
cp .env.example .env             # 環境変数テンプレート
uv run python models/prepare_model.py  # モデル学習 + MLflow 連携
uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
OpenAPI UI: http://localhost:8000/docs

### Docker Compose
```bash
docker compose up --build
```
初回起動時に `models/model.joblib` が生成され、8000 番ポートで API が公開されます。

## API
| Path | Method | 説明 |
|------|--------|------|
| `/health` | GET | ヘルスチェック。`{"status": "ok"}` を返却 |
| `/model/info` | GET | モデル名・バージョン・格納パスを返却 |
| `/auth/token` | POST | 認証用トークン (Bearer) を発行 |
| `/predict` | POST | 特徴量配列を受け取り、`{"label": int, "proba": float}` を返却 (要トークン) |

```bash
# トークン発行
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "changeme"}'

# 推論リクエスト
curl -X POST http://localhost:8000/predict \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

## 品質とオブザーバビリティ
- **QA コマンド**: `uv run ruff check .`, `uv run black --check .`, `uv run pytest`
- **ロギング**: `structlog` が JSON 形式で `request_id` / `input_id` / `latency_ms` を出力。`LOG_LEVEL` で詳細度を調整できます。
- **MLflow**:
  - `models/prepare_model.py` 実行時にメトリクス (accuracy) とモデルアーティファクトを記録。
  - `MLFLOW_TRACKING_URI` を切り替えるだけで外部トラッキングサーバーへ接続可能。
  - `make mlflow-ui` で `http://localhost:5000` に UI を起動。

## Makefile コマンド
```bash
make install         # uv sync --frozen
make prepare-model   # モデル再生成 + MLflow ログ
make qa              # ruff / black --check / pytest
make serve           # Uvicorn サーバー起動
make docker-up       # Docker Compose 起動
make docker-down     # Docker Compose 停止
make mlflow-ui       # MLflow UI を 0.0.0.0:5000 で起動
```

## GitHub Actions
- `ci.yml`: Lint / Format / Test を実行。
- `auto-review.yml`: reviewdog + ruff が PR に自動コメント。
- `deploy.yml`: Render の Deploy Hook をトリガー。`RENDER_DEPLOY_HOOK` シークレットを設定してください。

## デプロイ (Render)
- Render Dashboard で Deploy Hook URL を取得し、GitHub Secrets に `RENDER_DEPLOY_HOOK` として登録。
- main への push もしくは手動実行 (`gh workflow run deploy.yml -f environment=production`) でデプロイを開始。
- Workflow 内でヘルスチェック／推論テストを実行してから Render へ通知します。
- シークレット未設定のまま実行すると失敗ステータスになるため、利用前に Secrets を登録するか、必要になるまで Workflow を無効化してください。

## 環境変数
```
APP_ENV=local
PORT=8000
MODEL_PATH=models/model.joblib
LOG_LEVEL=INFO
API_USERNAME=admin
API_PASSWORD=changeme
API_USERNAME_FILE=
API_PASSWORD_FILE=
JWT_SECRET=super-secret-key
JWT_SECRET_FILE=
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
MLFLOW_TRACKING_URI=file:mlruns
MLFLOW_EXPERIMENT_NAME=iris-classifier
MLFLOW_RUN_NAME=logreg-iris
```

`*_FILE` 変数にファイルパスを設定すると、Docker Secrets や Vault Agent が配布したシークレットファイルを読み込みます。
