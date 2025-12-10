# 戦略コンサルティングエージェント - プロトタイプ

戦略コンサルティングに特化したAIエージェントシステムのプロトタイプです。

## 機能

- **Strategy Agent**: 戦略立案エージェント（OpenAI GPT-4o統合）
- **3C分析**: 顧客・競合・自社の観点から戦略分析
- **SWOT分析**: 強み・弱み・機会・脅威を分析し、クロスSWOT戦略を導出
- **5Forces分析**: 業界構造を分析し、収益性と競争環境を評価
- **PEST分析**: 政治・経済・社会・技術の観点からマクロ環境を分析
- **バリューチェーン分析**: 主活動と支援活動を分析し、価値創造ポイントと競争優位性を特定
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
│   ├── three_c_analysis.py # 3C分析
│   ├── swot_analysis.py   # SWOT分析
│   ├── five_forces.py     # 5Forces分析
│   ├── pest_analysis.py   # PEST分析
│   └── value_chain.py     # バリューチェーン分析
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
- Function Callingによる各種フレームワークの実行
- イシュードリブン、MECE、ファクトベースの分析

### 分析フレームワーク

#### 3C分析
- **Customer（顧客）**: 市場規模、成長率、セグメント、ニーズ分析
- **Competitor（競合）**: 競合マッピング、市場シェア、競争優位性
- **Company（自社）**: コアコンピタンス、リソース、価値提案

#### SWOT分析
- **Strengths（強み）**: 内部の強みを特定
- **Weaknesses（弱み）**: 内部の弱みを特定
- **Opportunities（機会）**: 外部の機会を特定
- **Threats（脅威）**: 外部の脅威を特定
- **クロスSWOT戦略**: SO/WO/ST/WT戦略の導出

#### 5Forces分析
- **新規参入の脅威**: 参入障壁の分析
- **代替品の脅威**: 代替品の影響評価
- **買い手の交渉力**: 顧客の影響力分析
- **売り手の交渉力**: サプライヤーの影響力分析
- **業界内の競争**: 競争の激しさの評価

#### PEST分析
- **Political（政治）**: 政治的要因の影響分析
- **Economic（経済）**: 経済的要因の影響分析
- **Social（社会）**: 社会的要因の影響分析
- **Technological（技術）**: 技術的要因の影響分析

#### バリューチェーン分析
- **主活動**: 購買物流、製造、出荷物流、販売・マーケティング、サービス
- **支援活動**: 企業インフラ、人事・労務管理、技術開発、調達
- **価値創造ポイント**: 競争優位性の源泉を特定
- **改善機会**: コスト削減と価値向上の機会を特定

### CLI

- `analyze`: 戦略分析を実行
- `create-sample`: サンプルデータファイルを作成
- `check-config`: 設定を確認

## 次のステップ

このプロトタイプをベースに、以下の機能を追加できます:

1. **追加のエージェント**: 市場分析、財務分析エージェント
2. **Webインターフェース**: FastAPI + Reactでのダッシュボード
3. **データベース統合**: PostgreSQLでのプロジェクト管理
4. **レポート生成**: PowerPoint/PDF出力

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
