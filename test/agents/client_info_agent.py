"""クライアント情報取得エージェント"""
import asyncio
import json
from typing import Dict, Any, Optional
from rich.console import Console

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser

from agents.base_agent import BaseAgent
from utils.data_schema import ClientData
from config.settings import settings


console = Console()


class ClientInfoAgent(BaseAgent):
    """OpenAI APIを使用してクライアント情報を取得するエージェント"""
    
    def __init__(self):
        """初期化"""
        super().__init__("ClientInfoAgent")
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.3,  # 事実ベースの情報取得のため低めに設定
            api_key=settings.openai_api_key
        )
        self.parser = JsonOutputParser(pydantic_object=ClientData)
        self.max_retries = 3
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        クライアント情報を取得（BaseAgentインターフェース実装）
        
        Args:
            data: プロジェクトデータ（client_name, industry, challenge含む）
        
        Returns:
            取得結果
        """
        try:
            client_name = data.get('client_name', '')
            industry = data.get('industry', '')
            challenge = data.get('challenge', '')
            
            client_data = await self.fetch_client_info(client_name, industry, challenge)
            
            return {
                'agent': self.agent_name,
                'status': 'success',
                'analysis_type': 'client_info',
                'result': client_data,
                'formatted_output': self._format_output(client_data)
            }
        except Exception as e:
            return self._format_error(e)
    
    async def fetch_client_info(
        self,
        client_name: str,
        industry: str,
        challenge: str
    ) -> Dict[str, Any]:
        """
        OpenAI APIを使用してクライアント情報を取得
        
        Args:
            client_name: クライアント名
            industry: 業界
            challenge: 課題
        
        Returns:
            構造化されたクライアントデータ
        """
        console.print(f"\n[yellow]OpenAI APIからクライアント情報を取得中...[/yellow]")
        console.print(f"  クライアント: {client_name}")
        console.print(f"  業界: {industry}")
        console.print(f"  課題: {challenge}\n")
        
        # プロンプトを構築
        system_prompt = """あなたは企業分析の専門家です。
指定された企業について、公開情報に基づいて詳細な分析データを提供してください。
データは戦略コンサルティングに使用されるため、できる限り具体的で正確な情報を提供してください。

データが不明な場合は、業界標準や合理的な推定値を使用してください。
すべての数値は日本円（JPY）で表記してください。"""
        
        human_prompt = f"""以下の企業について、戦略分析に必要な情報を収集してください：

企業名: {client_name}
業界: {industry}
課題: {challenge}

以下の形式でJSON形式のデータを返してください：

{{
  "customer_data": {{
    "market_size": <市場規模（円）>,
    "growth_rate": <年間成長率（%）>,
    "segments": [<主要な顧客セグメント>],
    "needs": [<顧客の主要なニーズ>],
    "buying_behavior": "<購買行動の特徴>"
  }},
  "competitor_data": {{
    "competitors": [
      {{
        "name": "<競合企業名>",
        "type": "direct",
        "revenue": <売上高（円）>,
        "strengths": [<強み>],
        "cost_advantage": true/false
      }}
    ]
  }},
  "company_data": {{
    "core_competencies": [<コアコンピタンス>],
    "resources": {{
      "employees": <従業員数>,
      "rd_budget": <研究開発予算（円）>
    }},
    "value_proposition": "<価値提案>",
    "market_position": "<市場ポジション>"
  }},
  "market_analysis_data": {{
    "market_size": <市場規模（円）>,
    "growth_rate": <成長率（%）>,
    "market_segments": [<セグメント>],
    "market_trends": [<トレンド>],
    "customer_segments": [
      {{
        "name": "<セグメント名>",
        "size": <規模（円）>,
        "growth_rate": <成長率（%）>,
        "characteristics": [<特性>]
      }}
    ],
    "market_share_data": {{
      "<企業名>": <シェア（%）>
    }}
  }},
  "financial_data": {{
    "revenue": <売上高（円）>,
    "cost_of_sales": <売上原価（円）>,
    "operating_expenses": <営業費用（円）>,
    "assets": <資産（円）>,
    "liabilities": <負債（円）>,
    "equity": <純資産（円）>,
    "cash_flow_operating": <営業CF（円）>,
    "cash_flow_investing": <投資CF（円）>,
    "cash_flow_financing": <財務CF（円）>
  }}
}}

できる限り具体的で正確なデータを提供してください。
データが不明な場合は、業界標準や合理的な推定値を使用してください。"""
        
        # リトライロジック付きでAPI呼び出し
        for attempt in range(self.max_retries):
            try:
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=human_prompt)
                ]
                
                response = await self.llm.ainvoke(messages)
                
                # JSONをパース
                try:
                    # レスポンスからJSONを抽出
                    content = response.content
                    
                    # マークダウンのコードブロックを除去
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()
                    
                    data = json.loads(content)
                    
                    # Pydanticモデルで検証
                    client_data = ClientData(**data)
                    
                    console.print("[green]✓ クライアント情報の取得に成功しました[/green]\n")
                    
                    return client_data.to_dict()
                    
                except json.JSONDecodeError as e:
                    console.print(f"[yellow]⚠ JSON解析エラー (試行 {attempt + 1}/{self.max_retries}): {str(e)}[/yellow]")
                    if attempt == self.max_retries - 1:
                        raise ValueError(f"JSON解析に失敗しました: {str(e)}")
                    await asyncio.sleep(1)  # リトライ前に待機
                    
            except Exception as e:
                console.print(f"[yellow]⚠ API呼び出しエラー (試行 {attempt + 1}/{self.max_retries}): {str(e)}[/yellow]")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(2)  # リトライ前に待機
        
        raise RuntimeError("クライアント情報の取得に失敗しました")
    
    def fetch_client_info_sync(
        self,
        client_name: str,
        industry: str,
        challenge: str
    ) -> Dict[str, Any]:
        """
        同期版のクライアント情報取得
        
        Args:
            client_name: クライアント名
            industry: 業界
            challenge: 課題
        
        Returns:
            構造化されたクライアントデータ
        """
        # 新しいイベントループを作成して実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self.fetch_client_info(client_name, industry, challenge)
            )
        finally:
            loop.close()
    
    def _format_output(self, client_data: Dict[str, Any]) -> str:
        """取得したデータをフォーマット"""
        lines = []
        lines.append("=" * 60)
        lines.append("取得したクライアント情報")
        lines.append("=" * 60)
        lines.append("")
        
        if 'customer_data' in client_data:
            lines.append("【顧客データ】")
            customer = client_data['customer_data']
            if 'market_size' in customer:
                lines.append(f"  市場規模: ¥{customer['market_size']:,.0f}")
            if 'growth_rate' in customer:
                lines.append(f"  成長率: {customer['growth_rate']}%")
            lines.append("")
        
        if 'competitor_data' in client_data:
            lines.append("【競合データ】")
            competitors = client_data['competitor_data'].get('competitors', [])
            lines.append(f"  競合企業数: {len(competitors)}")
            for comp in competitors[:3]:  # 最初の3社のみ表示
                lines.append(f"  - {comp.get('name', 'N/A')}")
            lines.append("")
        
        if 'financial_data' in client_data:
            lines.append("【財務データ】")
            financial = client_data['financial_data']
            if 'revenue' in financial:
                lines.append(f"  売上高: ¥{financial['revenue']:,.0f}")
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)
