"""財務分析エージェント"""
import asyncio
from typing import Dict, Any
from agents.base_agent import BaseAgent
from frameworks.financial_analysis import FinancialAnalysis


class FinancialAgent(BaseAgent):
    """財務分析に特化したエージェント"""
    
    def __init__(self):
        """初期化"""
        super().__init__("FinancialAnalysisAgent")
        self.analyzer = FinancialAnalysis()
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        財務分析を実行
        
        Args:
            data: プロジェクトデータ
        
        Returns:
            財務分析結果
        """
        try:
            # 財務データを取得
            financial_data = data.get('financial_data', {})
            
            # 必須データの確認
            if not financial_data:
                return {
                    'agent': self.agent_name,
                    'status': 'skipped',
                    'message': '財務データが提供されていません'
                }
            
            # 非同期で分析を実行
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._run_analysis,
                financial_data
            )
            
            return {
                'agent': self.agent_name,
                'status': 'success',
                'analysis_type': 'financial',
                'result': result,
                'formatted_output': self.analyzer.format_result(result)
            }
            
        except Exception as e:
            return self._format_error(e)
    
    def _run_analysis(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        財務分析を実行（同期版）
        
        Args:
            financial_data: 財務データ
        
        Returns:
            分析結果
        """
        return self.analyzer.analyze(
            revenue=financial_data.get('revenue', 0),
            cost_of_sales=financial_data.get('cost_of_sales', 0),
            operating_expenses=financial_data.get('operating_expenses', 0),
            assets=financial_data.get('assets', 0),
            liabilities=financial_data.get('liabilities', 0),
            equity=financial_data.get('equity', 0),
            cash_flow_operating=financial_data.get('cash_flow_operating', 0),
            cash_flow_investing=financial_data.get('cash_flow_investing', 0),
            cash_flow_financing=financial_data.get('cash_flow_financing', 0)
        )
