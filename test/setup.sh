#!/bin/bash
# セットアップのみを実行するスクリプト

echo "🔧 仮想環境をセットアップします..."
echo ""

# 仮想環境が存在しない場合は作成
if [ ! -d "venv" ]; then
    echo "📁 仮想環境を作成します..."
    python3 -m venv venv
fi

# 仮想環境をアクティベート
source venv/bin/activate

# 明示的にpython3とpip3を使用
echo "📦 依存関係をインストールします..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "✅ セットアップ完了！"
echo ""
echo "次のコマンドで分析を実行できます:"
echo "  source venv/bin/activate"
echo "  python3 cli.py analyze --client '企業名' --industry '業界' --challenge '課題' --data-file sample_data.json"
