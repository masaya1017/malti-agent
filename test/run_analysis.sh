#!/bin/bash
# Strategy Agent セットアップ & 実行スクリプト

echo "🔧 仮想環境をセットアップします..."
echo ""

# 仮想環境をアクティベート
source venv/bin/activate

# 明示的にpython3とpip3を使用
echo "📦 依存関係をインストールします..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "✅ セットアップ完了"
echo ""
echo "🚀 戦略分析を実行します..."
echo ""

# 戦略分析を実行
python3 cli.py analyze \
  --client "テクノロジー株式会社" \
  --industry "SaaS業界" \
  --challenge "新規事業の市場参入戦略" \
  --data-file sample_data.json

echo ""
echo "✅ 分析完了"
