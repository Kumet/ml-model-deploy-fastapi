# ML Model Deploy (FastAPI)

![CI](https://github.com/OWNER/ml-model-deploy-fastapi/actions/workflows/ci.yml/badge.svg)

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
| `/predict` | POST | `{"features": [数値...]}` を受け取り、`{"label": int, "proba": float}` を返します。 |

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
```

## 次のステップ
- 推論サービス (`src/backend/app/services/`) にビジネスロジックを追加
- モデル更新タスクをスケジュールや CI に組み込み
