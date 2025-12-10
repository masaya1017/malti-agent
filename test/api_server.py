#!/usr/bin/env python3
"""FastAPI サーバー - マルチエージェント分析API"""
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agents.multi_agent_orchestrator import MultiAgentOrchestrator
from agents.client_info_agent import ClientInfoAgent


# FastAPIアプリケーション
app = FastAPI(
    title="戦略コンサルティングエージェント API",
    description="マルチエージェント統合分析APIサーバー",
    version="1.0.0"
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# リクエストモデル
class AnalysisRequest(BaseModel):
    """分析リクエスト"""
    client: str = Field(..., description="クライアント名")
    industry: Optional[str] = Field(None, description="業界")
    challenge: Optional[str] = Field(None, description="課題")
    data: Optional[Dict[str, Any]] = Field(None, description="追加データ")
    auto_fetch: bool = Field(True, description="OpenAI APIから自動的にクライアント情報を取得")
    save_data_path: Optional[str] = Field(None, description="取得したデータを保存するファイルパス")
    export_format: Optional[str] = Field(None, description="レポート出力形式 (pdf, pptx, md, all)")
    output_filename: Optional[str] = Field(None, description="出力ファイル名（拡張子なし）")
    output_dir: str = Field("reports", description="出力ディレクトリ")
    enable_dialogue: bool = Field(True, description="エージェント間対話を有効化")

    class Config:
        json_schema_extra = {
            "example": {
                "client": "楽天",
                "industry": "Eコマース",
                "challenge": "市場競争力強化と持続的成長",
                "auto_fetch": True,
                "export_format": "md",
                "enable_dialogue": True
            }
        }


# レスポンスモデル
class AnalysisResponse(BaseModel):
    """分析レスポンス"""
    status: str = Field(..., description="ステータス (success, error)")
    message: str = Field(..., description="メッセージ")
    integrated_report: Optional[str] = Field(None, description="統合レポート")
    summary: Optional[Dict[str, Any]] = Field(None, description="分析サマリー")
    agent_results: Optional[list] = Field(None, description="各エージェントの結果")
    exported_files: Optional[list] = Field(None, description="エクスポートされたファイルのパス")
    saved_data_path: Optional[str] = Field(None, description="保存されたデータのパス")


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "戦略コンサルティングエージェント API",
        "version": "1.0.0",
        "endpoints": {
            "multi_analyze": "/api/multi-analyze",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/multi-analyze", response_model=AnalysisResponse)
async def multi_analyze(request: AnalysisRequest):
    """
    マルチエージェント統合分析を実行
    
    Args:
        request: 分析リクエスト
    
    Returns:
        分析結果
    """
    try:
        # プロジェクトデータを構築
        project_data = {
            'client_name': request.client,
            'industry': request.industry or '',
            'challenge': request.challenge or '市場競争力強化と持続的成長'
        }
        
        # 追加データがある場合はマージ
        if request.data:
            project_data.update(request.data)
        
        # auto-fetchが有効な場合はOpenAI APIから取得
        fetched_data = None
        if request.auto_fetch and not request.data:
            try:
                client_info_agent = ClientInfoAgent()
                # 非同期メソッドを直接await
                fetched_data = await client_info_agent.fetch_client_info(
                    client_name=request.client,
                    industry=project_data['industry'],
                    challenge=project_data['challenge']
                )
                project_data.update(fetched_data)
                
                # save_data_pathが指定されている場合はファイルに保存
                if request.save_data_path:
                    with open(request.save_data_path, 'w', encoding='utf-8') as f:
                        json.dump(fetched_data, f, ensure_ascii=False, indent=2)
                        
            except Exception as e:
                # クライアント情報の取得に失敗しても続行
                print(f"Warning: Failed to fetch client info: {str(e)}")
        
        # マルチエージェントオーケストレーターを初期化
        orchestrator = MultiAgentOrchestrator(enable_dialogue=request.enable_dialogue)
        
        # マルチエージェント分析を実行（非同期メソッドを直接await）
        result = await orchestrator.analyze(project_data)
        
        # エクスポート処理
        exported_files = []
        if request.export_format:
            output_path = Path(request.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            base_name = request.output_filename if request.output_filename else f"{request.client}_multi_agent_analysis"
            
            report_generator = orchestrator.report_generator
            project_info = {
                'client_name': project_data.get('client_name'),
                'industry': project_data.get('industry'),
                'challenge': project_data.get('challenge')
            }
            
            # Markdown形式
            if request.export_format in ['md', 'all']:
                try:
                    md_path = output_path / f"{base_name}.md"
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(result['integrated_report'])
                    exported_files.append(str(md_path.absolute()))
                except Exception as e:
                    print(f"Warning: Failed to export Markdown: {str(e)}")
            
            # PDF形式
            if request.export_format in ['pdf', 'all']:
                try:
                    pdf_path = output_path / f"{base_name}.pdf"
                    report_generator.export_report(
                        project_info=project_info,
                        agent_results=result['agent_results'],
                        output_path=str(pdf_path),
                        export_format='pdf'
                    )
                    exported_files.append(str(pdf_path.absolute()))
                except Exception as e:
                    print(f"Warning: Failed to export PDF: {str(e)}")
            
            # PowerPoint形式
            if request.export_format in ['pptx', 'all']:
                try:
                    pptx_path = output_path / f"{base_name}.pptx"
                    report_generator.export_report(
                        project_info=project_info,
                        agent_results=result['agent_results'],
                        output_path=str(pptx_path),
                        export_format='pptx'
                    )
                    exported_files.append(str(pptx_path.absolute()))
                except Exception as e:
                    print(f"Warning: Failed to export PowerPoint: {str(e)}")
        
        return AnalysisResponse(
            status="success",
            message="分析が正常に完了しました",
            integrated_report=result['integrated_report'],
            summary=result['summary'],
            agent_results=result['agent_results'],
            exported_files=exported_files if exported_files else None,
            saved_data_path=request.save_data_path if request.save_data_path and fetched_data else None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"分析中にエラーが発生しました: {str(e)}"
        )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
