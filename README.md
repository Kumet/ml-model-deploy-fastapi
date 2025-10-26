# ML Model Deploy (FastAPI)

[![CI](https://github.com/Kumet/ml-model-deploy-fastapi/actions/workflows/ci.yml/badge.svg)](https://github.com/Kumet/ml-model-deploy-fastapi/actions/workflows/ci.yml)
[![Auto Review](https://github.com/Kumet/ml-model-deploy-fastapi/actions/workflows/auto-review.yml/badge.svg)](https://github.com/Kumet/ml-model-deploy-fastapi/actions/workflows/auto-review.yml)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)

FastAPI と scikit-learn で学習済みモデルを提供する最小構成テンプレートです。
依存管理は `uv`、品質ゲートは `ruff` + `black` + `pytest`、配布は `Docker Compose` を想定しています。

## 主な構成
```
ml-model-deploy-fastapi/
├─ src/backend/app/        # FastAPI アプリ本体
│  ├─ api/                 # ルーティングとスキーマ
│  ├─ core/                # 設定・モデル読み込み
│  └─ services/            # 推論ロジック
├─ src/backend/tests/      # pytest
├─ models/                 # モデル生成スクリプトと成果物
└─ .github/workflows/ci.yml
```

## セットアップ
```bash
uv sync --frozen
cp .env.example .env
uv run python models/prepare_model.py
uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
ブラウザで http://localhost:8000/docs を開き、OpenAPI から動作確認できます。

## Docker Compose
```bash
docker compose up --build
```
初回起動時は `models/model.joblib` が生成され、Uvicorn が 8000 番ポートで公開されます。

## API 仕様
| Path | Method | 説明 |
|------|--------|------|
| `/health` | GET | 稼働確認。`{"status": "ok"}` を返します。 |
| `/model/info` | GET | モデル名・バージョン・パスを返します。 |
| `/auth/token` | POST | 認証用トークンを発行します。 |
| `/predict` | POST | `{"features": [数値...]}` を受け取り、`{"label": int, "proba": float}` を返します。Bearer トークン必須。 |

## 認証
```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "changeme"}'

# => {"access_token": "...", "token_type": "bearer"}

curl -X POST http://localhost:8000/predict \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

## ログ
`structlog` で JSON 形式のアクセスログを出力し、`request_id` / `input_id` / `latency_ms` を `/predict` のレスポンスログに付与します。`LOG_LEVEL` を変更すると詳細度を制御でき、可観測性基盤（CloudWatch Logs, Loki 等）での集計が容易です。

## テスト & 品質ゲート
```bash
uv run ruff check .
uv run black --check .
uv run pytest
```

## Makefile ショートカット
```bash
make install         # uv sync --frozen
make prepare-model   # Iris モデルの再生成
make qa              # ruff / black --check / pytest をまとめて実行
make serve           # Uvicorn でローカル起動
make docker-up       # Docker Compose で起動
```

## pre-commit
```bash
pre-commit install
pre-commit run --all-files
```

## CI
PR 作成時に GitHub Actions (`.github/workflows/ci.yml`) が以下を検証します。
- `uv sync --frozen`
- `models/prepare_model.py` によるモデル生成
- `ruff check .`
- `black --check .`
- `pytest`

また、`.github/workflows/auto-review.yml` が PR 上で `ruff` の指摘を reviewdog 経由で自動レビューします。

## 環境変数 (例: `.env`)
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
```

`*_FILE` 変数にパスを設定すると、Docker Secrets や Vault Agent などが配置したファイルから値を読み込みます。例：`API_PASSWORD_FILE=/run/secrets/ml_api_password`。クラウドの Secrets Manager を使用する場合は CI/CD でファイルを作成する、またはコンテナにバインドマウントすることで対応できます。


## 次のステップ
- 推論サービス (`src/backend/app/services/`) にビジネスロジックを追加
- モデル更新タスクをスケジュールや CI に組み込み
