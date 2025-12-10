# 戦略コンサルティングエージェント - プロトタイプ

戦略コンサルティングに特化したAIエージェントシステムのプロトタイプです。

## 機能

- **Strategy Agent**: 戦略立案エージェント（OpenAI GPT-4o統合）
- **3C分析**: 顧客・競合・自社の観点から戦略分析
- **CLIインターフェース**: コマンドラインから簡単に実行

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env`ファイルを作成してOpenAI APIキーを設定：

```bash
cp .env.example .env
```

`.env`ファイルを編集：

```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4o
LOG_LEVEL=INFO
```

### 3. 設定の確認

```bash
python cli.py check-config
```

## 使い方

### サンプルデータの作成

```bash
python cli.py create-sample sample_data.json
```

### 戦略分析の実行

```bash
python cli.py analyze \
  --client "テクノロジー株式会社" \
  --industry "SaaS業界" \
  --challenge "新規事業の市場参入戦略" \
  --data-file sample_data.json
```

短縮オプション：

```bash
python cli.py analyze -c "テクノロジー株式会社" -i "SaaS業界" -ch "新規事業の市場参入戦略" -f sample_data.json
```

## プロジェクト構成

```
.
├── agents/                 # エージェント実装
│   ├── __init__.py
│   └── strategy_agent.py  # 戦略エージェント
├── frameworks/            # 分析フレームワーク
│   ├── __init__.py
│   └── three_c_analysis.py # 3C分析
├── config/                # 設定
│   ├── __init__.py
│   └── settings.py        # 設定管理
├── cli.py                 # CLIインターフェース
├── requirements.txt       # 依存関係
├── .env.example          # 環境変数テンプレート
└── README.md             # このファイル
```

## 実装されている機能

### Strategy Agent

- OpenAI GPT-4oを使用した戦略思考
- Function Callingによる3C分析の実行
- イシュードリブン、MECE、ファクトベースの分析

### 3C分析フレームワーク

- **Customer（顧客）**: 市場規模、成長率、セグメント、ニーズ分析
- **Competitor（競合）**: 競合マッピング、市場シェア、競争優位性
- **Company（自社）**: コアコンピタンス、リソース、価値提案

### CLI

- `analyze`: 戦略分析を実行
- `create-sample`: サンプルデータファイルを作成
- `check-config`: 設定を確認

## 次のステップ

このプロトタイプをベースに、以下の機能を追加できます：

1. **追加のフレームワーク**: SWOT分析、5Forces分析など
2. **追加のエージェント**: 市場分析、財務分析エージェント
3. **Webインターフェース**: FastAPI + Reactでのダッシュボード
4. **データベース統合**: PostgreSQLでのプロジェクト管理
5. **レポート生成**: PowerPoint/PDF出力

## トラブルシューティング

### OpenAI APIエラー

```
Error: OpenAI API key not found
```

→ `.env`ファイルに正しいAPIキーを設定してください

### モジュールが見つからない

```
ModuleNotFoundError: No module named 'langchain'
```

→ 依存関係をインストールしてください: `pip install -r requirements.txt`

## ライセンス

MIT License
