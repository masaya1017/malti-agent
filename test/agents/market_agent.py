"""市場分析エージェント"""
import asyncio
from typing import Dict, Any
from agents.base_agent import BaseAgent
from frameworks.market_analysis import MarketAnalysis


class MarketAgent(BaseAgent):
    """市場分析に特化したエージェント"""
    
    def __init__(self):
        """初期化"""
        super().__init__("MarketAnalysisAgent")
        self.analyzer = MarketAnalysis()
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        市場分析を実行
        
        Args:
            data: プロジェクトデータ
        
        Returns:
            市場分析結果
        """
        try:
            # 市場分析データを取得
            market_data = data.get('market_analysis_data', {})
            
            # 必須データの確認
            if not market_data:
                return {
                    'agent': self.agent_name,
                    'status': 'skipped',
                    'message': '市場分析データが提供されていません'
                }
            
            # 非同期で分析を実行（CPUバウンドな処理をスレッドプールで実行）
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._run_analysis,
                market_data
            )
            
            return {
                'agent': self.agent_name,
                'status': 'success',
                'analysis_type': 'market',
                'result': result,
                'formatted_output': self.analyzer.format_result(result)
            }
            
        except Exception as e:
            return self._format_error(e)
    
    def _run_analysis(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        市場分析を実行（同期版）
        
        Args:
            market_data: 市場データ
        
        Returns:
            分析結果
        """
        return self.analyzer.analyze(
            market_size=market_data.get('market_size', 0),
            growth_rate=market_data.get('growth_rate', 0),
            market_segments=market_data.get('market_segments', []),
            market_trends=market_data.get('market_trends', []),
            customer_segments=market_data.get('customer_segments', []),
            market_share_data=market_data.get('market_share_data', {})
        )
