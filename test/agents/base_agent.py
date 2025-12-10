"""ベースエージェントクラス"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """全エージェントの基底クラス"""
    
    def __init__(self, agent_name: str):
        """
        初期化
        
        Args:
            agent_name: エージェント名
        """
        self.agent_name = agent_name
    
    @abstractmethod
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析を実行（非同期）
        
        Args:
            data: 分析対象データ
        
        Returns:
            分析結果
        """
        pass
    
    def get_agent_name(self) -> str:
        """
        エージェント名を取得
        
        Returns:
            エージェント名
        """
        return self.agent_name
    
    def _format_error(self, error: Exception) -> Dict[str, Any]:
        """
        エラーをフォーマット
        
        Args:
            error: 例外オブジェクト
        
        Returns:
            エラー情報
        """
        return {
            'agent': self.agent_name,
            'status': 'error',
            'error_type': type(error).__name__,
            'error_message': str(error)
        }
