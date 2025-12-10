#!/bin/bash

# FastAPI サーバー起動スクリプト

echo "戦略コンサルティングエージェント APIサーバーを起動します..."
echo ""
echo "サーバーURL: http://localhost:8000"
echo "API ドキュメント: http://localhost:8000/docs"
echo ""

# Uvicornでサーバーを起動
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
