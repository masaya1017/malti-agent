# 戦略コンサルティングエージェント

戦略コンサルティングに特化したマルチエージェントAIシステムです。市場分析、財務分析、戦略分析の3つの専門エージェントが協調して、包括的なコンサルティングレポートを自動生成します。

## 主な機能

### マルチエージェントシステム
- **市場分析エージェント**: 市場規模、成長率、セグメント、トレンド、市場シェアを分析
- **財務分析エージェント**: 収益性、財務健全性、キャッシュフローを分析
- **戦略分析エージェント**: 複数の戦略フレームワークを用いた包括的分析

### 分析フレームワーク（7種類）
- **3C分析**: 顧客・競合・自社の観点から戦略分析
- **SWOT分析**: 強み・弱み・機会・脅威を分析し、クロスSWOT戦略を導出
- **5Forces分析**: 業界構造を分析し、収益性と競争環境を評価
- **PEST分析**: 政治・経済・社会・技術の観点からマクロ環境を分析
- **バリューチェーン分析**: 主活動と支援活動を分析し、価値創造ポイントと競争優位性を特定
- **市場分析**: 市場魅力度、セグメント優先度、HHI指数、トレンド分析
- **財務分析**: 収益性指標、財務健全性指標、キャッシュフローパターン分析

### 統合レポート生成
- エグゼクティブサマリー
- 各分析の詳細結果
- 統合的な推奨事項
- 具体的なアクションプラン

---

## システムアーキテクチャ

### 全体構成

```
┌─────────────────────────────────────────────────────────────┐
│                         ユーザー                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  実行スクリプト / CLI                          │
│              (run_multi_agent.py / cli.py)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            Multi-Agent Orchestrator                         │
│         (agents/multi_agent_orchestrator.py)                │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  並列実行制御 (asyncio)                              │   │
│  │  - プログレスバー表示                                │   │
│  │  - エラーハンドリング                                │   │
│  │  - 結果の統合                                        │   │
│  └─────────────────────────────────────────────────────┘   │
└──────┬──────────────────┬──────────────────┬───────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Market    │   │  Financial  │   │  Strategy   │
│   Agent     │   │   Agent     │   │   Agent     │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Market    │   │  Financial  │   │  Strategy   │
│  Analysis   │   │  Analysis   │   │ Frameworks  │
│ Framework   │   │ Framework   │   │  (3C/SWOT/  │
│             │   │             │   │ 5Forces/etc)│
└─────────────┘   └─────────────┘   └─────────────┘
       │                  │                  │
       └──────────────────┴──────────────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Report Generator│
                 │   (統合レポート)  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  Markdown Report│
                 │ (multi_agent_   │
                 │  report.md)     │
                 └─────────────────┘
```

### コンポーネント詳細

#### 1. マルチエージェントオーケストレーター
**ファイル**: `agents/multi_agent_orchestrator.py`

**責務**:
- 3つのエージェントのライフサイクル管理
- 並列実行制御（asyncio使用）
- プログレスバー表示（Rich library）
- エラーハンドリング
- 結果の収集と統合

**主要メソッド**:
```python
async def analyze(project_data: Dict) -> Dict
    # 3つのエージェントを並列実行し、結果を統合
```

#### 2. 専門エージェント

##### 市場分析エージェント
**ファイル**: `agents/market_agent.py`

**分析内容**:
- 市場規模・成長率分析
- セグメント分析（優先度評価）
- 市場シェア分析（HHI指数計算）
- トレンド分析（技術/社会/経済）
- 戦略的推奨事項の生成

##### 財務分析エージェント
**ファイル**: `agents/financial_agent.py`

**分析内容**:
- 収益性分析（売上総利益率、営業利益率）
- 財務健全性分析（自己資本比率、負債比率）
- キャッシュフロー分析（パターン判定）
- 総合評価
- 推奨事項の生成

##### 戦略分析エージェント
**ファイル**: `agents/strategy_analysis_agent.py`

**分析内容**:
- 3C分析（顧客・競合・自社）
- SWOT分析（クロスSWOT戦略）
- 5Forces分析（業界構造）
- PEST分析（マクロ環境）
- バリューチェーン分析

#### 3. レポート生成
**ファイル**: `utils/report_generator.py`

**生成するセクション**:
1. プロジェクト情報
2. エグゼクティブサマリー
3. 市場分析結果
4. 財務分析結果
5. 戦略分析結果
6. 統合的な推奨事項
7. アクションプラン（短期/中期/長期）

### 実行フロー

```
1. ユーザーがスクリプトを実行
   ↓
2. オーケストレーターがプロジェクトデータを受け取る
   ↓
3. 3つのエージェントを並列実行（asyncio）
   ├─ 市場分析エージェント → 市場分析フレームワーク
   ├─ 財務分析エージェント → 財務分析フレームワーク
   └─ 戦略分析エージェント → 戦略フレームワーク群
   ↓
4. 各エージェントが分析結果を返す
   ↓
5. オーケストレーターが結果を収集
   ↓
6. レポート生成ユーティリティが統合レポートを作成
   ↓
7. マークダウンファイルとして保存
   ↓
8. コンソールに結果を表示
```

### 技術スタック

- **言語**: Python 3.9+
- **LLM**: OpenAI GPT-4o
- **非同期処理**: asyncio
- **LLMフレームワーク**: LangChain
- **CLI**: Click
- **UI**: Rich (プログレスバー、パネル表示)
- **設定管理**: pydantic-settings

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

### 1. セットアップ

初回のみ、仮想環境のセットアップと依存関係のインストールを実行：

```bash
sh setup.sh
```

### 2. マルチエージェント統合分析の実行

市場分析、財務分析、戦略分析を並列実行し、統合レポートを生成：

```bash
python3 run_multi_agent.py
```

**生成されるファイル**:
- ✅ `multi_agent_report.md` - マークダウン形式
- ✅ `multi_agent_report.pptx` - PowerPoint形式
- ✅ `multi_agent_report.pdf` - PDF形式（日本語対応、マークダウン内容を完全統合）

**実行結果の例**:
```
✓ マークダウンレポートを保存しました: multi_agent_report.md
✓ PowerPointレポートを保存しました: multi_agent_report.pptx
✓ PDFレポートを保存しました: multi_agent_report.pdf

分析サマリー
  総エージェント数: 3
  成功: 3
  スキップ: 0
  失敗: 0
  成功率: 100.0%
```

**実行される機能**:
- 🤖 **3つのエージェントによる並列分析**
  - 市場分析エージェント
  - 財務分析エージェント
  - 戦略分析エージェント
- 💬 **エージェント間対話**（3フェーズ）
  - フェーズ1: 洞察の共有
  - フェーズ2: 矛盾点の特定
  - フェーズ3: 合意形成
- 📄 **マルチフォーマット出力**
  - Markdown、PowerPoint、PDFの3形式で自動生成

---

市場・財務分析のみ実行

```bash
source venv/bin/activate
python3 run_additional_analysis.py
```

### 3. CLI経由でのマルチエージェント分析（推奨）

企業名を指定するだけで、OpenAI APIから自動的に企業情報を取得し、マルチエージェント分析を実行します。

#### 基本的な使い方

```bash
python3 cli.py multi-analyze --client "企業名"
```

**例: 任天堂の分析**
```bash
python3 cli.py multi-analyze --client "任天堂" --industry "ゲーム業界" --challenge "グローバル市場での競争力強化"
```

#### 主なオプション

- `--client` / `-c`: クライアント名（必須）
- `--industry` / `-i`: 業界（省略可、OpenAIが推定）
- `--challenge` / `-ch`: 課題（省略可、デフォルトで一般的な戦略分析）
- `--export` / `-e`: レポート出力形式（`pdf`, `pptx`, `md`, `all`）
- `--output` / `-o`: 出力ファイル名（拡張子なし）
- `--output-dir` / `-d`: 出力ディレクトリ（デフォルト: `reports`）
- `--save-data`: 取得したデータを保存するファイルパス
- `--auto-fetch` / `--no-auto-fetch`: OpenAI APIから自動取得（デフォルト: 有効）
- `--enable-dialogue` / `--no-dialogue`: エージェント間対話を有効化（デフォルト: 有効）

#### 使用例

**例1: 最小限のオプションで実行**
```bash
python3 cli.py multi-analyze --client "トヨタ自動車"
```

**例2: すべての形式でレポート出力**
```bash
python3 cli.py multi-analyze \
  --client "ソニー" \
  --industry "エレクトロニクス" \
  --challenge "グローバル競争力強化" \
  --export all \
  --output sony_analysis
```

生成されるファイル（`reports`ディレクトリ内）:
- `sony_analysis.md`
- `sony_analysis.pdf`
- `sony_analysis.pptx`

**例3: データを保存して再利用**

データを取得して保存:
```bash
python3 cli.py multi-analyze \
  --client "楽天" \
  --industry "Eコマース" \
  --save-data rakuten_data.json \
  --export md
```

保存したデータを再利用（OpenAI APIを呼び出さない）:
```bash
python3 cli.py multi-analyze \
  --client "楽天" \
  --no-auto-fetch \
  --data-file rakuten_data.json \
  --export pdf
```

**例4: カスタム出力ディレクトリを指定**
```bash
python3 cli.py multi-analyze \
  --client "パナソニック" \
  --export all \
  --output-dir analysis_results/panasonic
```

#### 実行される機能

- 🤖 **OpenAI APIによる自動データ取得**: 企業情報を自動収集
- 📊 **3つのエージェントによる並列分析**:
  - 市場分析エージェント
  - 財務分析エージェント
  - 戦略分析エージェント
- 💬 **エージェント間対話**: 分析結果の議論と合意形成
- 📄 **マルチフォーマット出力**: Markdown、PowerPoint、PDFの3形式で自動生成

---

### 4. サンプルデータの作成

```bash
python3 cli.py create-sample sample_data.json
```

## プロジェクト構成

```
.
├── agents/                          # エージェント実装
│   ├── __init__.py
│   ├── base_agent.py               # ベースエージェント（抽象クラス）
│   ├── market_agent.py             # 市場分析エージェント
│   ├── financial_agent.py          # 財務分析エージェント
│   ├── strategy_analysis_agent.py  # 戦略分析エージェント
│   ├── multi_agent_orchestrator.py # マルチエージェントオーケストレーター
│   └── strategy_agent.py           # 戦略エージェント（既存）
├── frameworks/                      # 分析フレームワーク
│   ├── __init__.py
│   ├── three_c_analysis.py         # 3C分析
│   ├── swot_analysis.py            # SWOT分析
│   ├── five_forces.py              # 5Forces分析
│   ├── pest_analysis.py            # PEST分析
│   ├── value_chain.py              # バリューチェーン分析
│   ├── market_analysis.py          # 市場分析
│   └── financial_analysis.py       # 財務分析
├── utils/                           # ユーティリティ
│   ├── __init__.py
│   └── report_generator.py         # 統合レポート生成
├── config/                          # 設定
│   ├── __init__.py
│   └── settings.py                 # 設定管理
├── cli.py                           # CLIインターフェース
├── run_multi_agent.py               # マルチエージェント実行スクリプト
├── run_additional_analysis.py       # 市場・財務分析実行スクリプト
├── setup.sh                         # セットアップスクリプト
├── sample_data_extended.json        # 拡張サンプルデータ
├── requirements.txt                 # 依存関係
├── .env.example                     # 環境変数テンプレート
└── README.md                        # このファイル
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

- `analyze`: 戦略分析を実行（オプション: `--export pdf/pptx/all` でレポート出力）
- `multi-analyze`: マルチエージェント統合分析を実行（OpenAI APIで自動データ取得）
- `create-sample`: サンプルデータファイルを作成
- `check-config`: 設定を確認

---

## 実装済み機能

✅ **マルチエージェントシステム**: 市場・財務・戦略の3つのエージェントが協調動作  
✅ **OpenAI自動データ取得**: 企業名を指定するだけで情報を自動収集 ✨  
✅ **7つの分析フレームワーク**: 3C、SWOT、5Forces、PEST、Value Chain、市場分析、財務分析  
✅ **並列実行**: asyncioによる高速な分析処理  
✅ **統合レポート生成**: マークダウン形式の包括的レポート  
✅ **マルチフォーマット出力**: PowerPoint/PDF形式でのレポートエクスポート ✨  
✅ **エージェント間対話**: 分析結果の議論と合意形成機能 ✨  
✅ **CLIインターフェース**: コマンドラインからの簡単実行  
✅ **レポート出力ディレクトリ**: 整理されたフォルダ構造でレポート管理 ✨  

## 今後の拡張可能性

1. **Webインターフェース**: FastAPI + Reactでのダッシュボード
3. **データベース統合**: PostgreSQLでのプロジェクト・履歴管理
4. **レポート出力**: PowerPoint/PDF形式でのエクスポート
5. **学習機能**: 過去の分析結果からの学習・改善
6. **リアルタイムデータ連携**: 外部APIからのデータ取得

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
