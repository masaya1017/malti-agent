"""戦略分析エージェント（マルチエージェント対応版）"""
import asyncio
from typing import Dict, Any
from agents.base_agent import BaseAgent
from agents.strategy_agent import StrategyAgent


class StrategyAnalysisAgent(BaseAgent):
    """戦略分析に特化したエージェント"""
    
    def __init__(self):
        """初期化"""
        super().__init__("StrategyAnalysisAgent")
        self.strategy_agent = StrategyAgent()
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        戦略分析を実行
        
        Args:
            data: プロジェクトデータ
        
        Returns:
            戦略分析結果
        """
        try:
            # 必須データの確認
            if not data.get('customer_data') and not data.get('competitor_data'):
                return {
                    'agent': self.agent_name,
                    'status': 'skipped',
                    'message': '戦略分析に必要なデータが提供されていません'
                }
            
            # 非同期で分析を実行
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self.strategy_agent.analyze_sync,
                data
            )
            
            return {
                'agent': self.agent_name,
                'status': 'success',
                'analysis_type': 'strategy',
                'result': result,
                'formatted_output': self._format_strategy_output(result)
            }
            
        except Exception as e:
            return self._format_error(e)
    
    def _format_strategy_output(self, result: Dict[str, Any]) -> str:
        """
        戦略分析結果をフォーマット
        
        Args:
            result: 分析結果
        
        Returns:
            フォーマット済み出力
        """
        output = []
        output.append("=" * 60)
        output.append("戦略分析結果")
        output.append("=" * 60)
        output.append("")
        
        # 最終的な出力
        if 'output' in result:
            output.append(result['output'])
        
        # 中間ステップ
        if 'intermediate_steps' in result and result['intermediate_steps']:
            output.append("\n" + "-" * 60)
            output.append("実行された分析フレームワーク")
            output.append("-" * 60)
            
            for i, (action, observation) in enumerate(result['intermediate_steps'], 1):
                output.append(f"\n{i}. {action.tool}")
                if observation:
                    # 観察結果の最初の500文字のみ表示
                    obs_preview = str(observation)[:500]
                    if len(str(observation)) > 500:
                        obs_preview += "..."
                    output.append(obs_preview)
        
        output.append("\n" + "=" * 60)
        return "\n".join(output)
