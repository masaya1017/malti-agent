# FastAPI HTTP通信 使用ガイド

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

## サーバーの起動

### 方法1: 起動スクリプトを使用

```bash
./start_server.sh
```

### 方法2: 直接起動

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

サーバーが起動すると、以下のURLでアクセスできます：
- **APIサーバー**: http://localhost:8000
- **APIドキュメント (Swagger UI)**: http://localhost:8000/docs
- **代替ドキュメント (ReDoc)**: http://localhost:8000/redoc

## API使用方法

### エンドポイント: POST /api/multi-analyze

マルチエージェント統合分析を実行します。

#### リクエスト例 (curl)

```bash
curl -X POST "http://localhost:8000/api/multi-analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "client": "楽天",
    "industry": "Eコマース",
    "auto_fetch": true,
    "save_data_path": "rakuten_data.json",
    "export_format": "md",
    "enable_dialogue": true
  }'
```

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 | デフォルト |
|-----------|-----|------|------|-----------|
| `client` | string | ✓ | クライアント名 | - |
| `industry` | string | | 業界 | 自動推定 |
| `challenge` | string | | 課題 | "市場競争力強化と持続的成長" |
| `data` | object | | 追加データ（JSON） | null |
| `auto_fetch` | boolean | | OpenAI APIから自動取得 | true |
| `save_data_path` | string | | データ保存パス | null |
| `export_format` | string | | 出力形式 (pdf/pptx/md/all) | null |
| `output_filename` | string | | 出力ファイル名（拡張子なし） | "{client}_multi_agent_analysis" |
| `output_dir` | string | | 出力ディレクトリ | "reports" |
| `enable_dialogue` | boolean | | エージェント間対話を有効化 | true |

#### レスポンス例

```json
{
  "status": "success",
  "message": "分析が正常に完了しました",
  "integrated_report": "# 統合戦略分析レポート\n\n...",
  "summary": {
    "total_agents": 3,
    "successful": 3,
    "skipped": 0,
    "failed": 0,
    "success_rate": 100.0
  },
  "agent_results": [...],
  "exported_files": [
    "/Users/masaya/Desktop/開発/test/reports/楽天_multi_agent_analysis.md"
  ],
  "saved_data_path": "rakuten_data.json"
}
```

## Python クライアント例

```python
import requests
import json

# APIエンドポイント
url = "http://localhost:8000/api/multi-analyze"

# リクエストデータ
payload = {
    "client": "楽天",
    "industry": "Eコマース",
    "auto_fetch": True,
    "save_data_path": "rakuten_data.json",
    "export_format": "md",
    "enable_dialogue": True
}

# POSTリクエスト送信
response = requests.post(url, json=payload)

# レスポンス確認
if response.status_code == 200:
    result = response.json()
    print(f"ステータス: {result['status']}")
    print(f"メッセージ: {result['message']}")
    print(f"\n統合レポート:\n{result['integrated_report']}")
    print(f"\nサマリー: {result['summary']}")
else:
    print(f"エラー: {response.status_code}")
    print(response.json())
```

## CLIとの比較

### CLI版（従来）
```bash
python3 cli.py multi-analyze \
  --client "楽天" \
  --industry "Eコマース" \
  --save-data rakuten_data.json \
  --export md
```

### HTTP API版（新規）
```bash
curl -X POST "http://localhost:8000/api/multi-analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "client": "楽天",
    "industry": "Eコマース",
    "save_data_path": "rakuten_data.json",
    "export_format": "md"
  }'
```

## その他のエンドポイント

### GET / - ルート
```bash
curl http://localhost:8000/
```

### GET /health - ヘルスチェック
```bash
curl http://localhost:8000/health
```

## トラブルシューティング

### ポートが既に使用されている場合

別のポートを指定してサーバーを起動：
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8080 --reload
```

### OpenAI APIキーが設定されていない場合

`.env`ファイルに以下を設定：
```
OPENAI_API_KEY=your-api-key-here
```
