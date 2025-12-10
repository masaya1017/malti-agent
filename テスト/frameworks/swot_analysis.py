"""SWOT分析フレームワーク"""
from typing import List, Dict, Optional
from pydantic import BaseModel


class SWOTItem(BaseModel):
    """SWOT項目"""
    category: str  # strengths, weaknesses, opportunities, threats
    item: str
    description: Optional[str] = None
    impact: Optional[str] = None  # high, medium, low


class CrossSWOTStrategy(BaseModel):
    """クロスSWOT戦略"""
    strategy_type: str  # SO, ST, WO, WT
    strategy: str
    description: str


class SWOTAnalysisResult(BaseModel):
    """SWOT分析結果"""
    strengths: List[SWOTItem]
    weaknesses: List[SWOTItem]
    opportunities: List[SWOTItem]
    threats: List[SWOTItem]
    cross_swot_strategies: List[CrossSWOTStrategy]
    summary: str


class SWOTAnalysis:
    """SWOT分析フレームワーク"""
    
    def analyze(
        self,
        strengths: List[str],
        weaknesses: List[str],
        opportunities: List[str],
        threats: List[str]
    ) -> SWOTAnalysisResult:
        """
        SWOT分析を実行
        
        Args:
            strengths: 強み（内部要因・プラス）
            weaknesses: 弱み（内部要因・マイナス）
            opportunities: 機会（外部要因・プラス）
            threats: 脅威（外部要因・マイナス）
        
        Returns:
            SWOT分析結果
        """
        # 各要素を構造化
        strength_items = [SWOTItem(category="strengths", item=s) for s in strengths]
        weakness_items = [SWOTItem(category="weaknesses", item=w) for w in weaknesses]
        opportunity_items = [SWOTItem(category="opportunities", item=o) for o in opportunities]
        threat_items = [SWOTItem(category="threats", item=t) for t in threats]
        
        # クロスSWOT分析
        cross_strategies = self._generate_cross_swot_strategies(
            strengths, weaknesses, opportunities, threats
        )
        
        # サマリー生成
        summary = self._generate_summary(
            strength_items, weakness_items, opportunity_items, threat_items, cross_strategies
        )
        
        return SWOTAnalysisResult(
            strengths=strength_items,
            weaknesses=weakness_items,
            opportunities=opportunity_items,
            threats=threat_items,
            cross_swot_strategies=cross_strategies,
            summary=summary
        )
    
    def _generate_cross_swot_strategies(
        self,
        strengths: List[str],
        weaknesses: List[str],
        opportunities: List[str],
        threats: List[str]
    ) -> List[CrossSWOTStrategy]:
        """クロスSWOT戦略を生成"""
        strategies = []
        
        # SO戦略（強み×機会）: 強みを活かして機会を最大化
        if strengths and opportunities:
            strategies.append(CrossSWOTStrategy(
                strategy_type="SO",
                strategy="積極的攻勢戦略",
                description=f"強み「{strengths[0]}」を活かして、機会「{opportunities[0]}」を最大限に活用する"
            ))
        
        # ST戦略（強み×脅威）: 強みを活かして脅威を回避
        if strengths and threats:
            strategies.append(CrossSWOTStrategy(
                strategy_type="ST",
                strategy="差別化戦略",
                description=f"強み「{strengths[0]}」を活かして、脅威「{threats[0]}」の影響を最小化する"
            ))
        
        # WO戦略（弱み×機会）: 弱みを克服して機会を活用
        if weaknesses and opportunities:
            strategies.append(CrossSWOTStrategy(
                strategy_type="WO",
                strategy="弱点克服戦略",
                description=f"弱み「{weaknesses[0]}」を改善し、機会「{opportunities[0]}」を活用する"
            ))
        
        # WT戦略（弱み×脅威）: 弱みと脅威を最小化
        if weaknesses and threats:
            strategies.append(CrossSWOTStrategy(
                strategy_type="WT",
                strategy="防衛・撤退戦略",
                description=f"弱み「{weaknesses[0]}」と脅威「{threats[0]}」の影響を最小限に抑える"
            ))
        
        return strategies
    
    def _generate_summary(
        self,
        strengths: List[SWOTItem],
        weaknesses: List[SWOTItem],
        opportunities: List[SWOTItem],
        threats: List[SWOTItem],
        strategies: List[CrossSWOTStrategy]
    ) -> str:
        """サマリーを生成"""
        summary_parts = []
        
        # 内部環境
        summary_parts.append(f"【内部環境】強み{len(strengths)}項目、弱み{len(weaknesses)}項目")
        
        # 外部環境
        summary_parts.append(f"【外部環境】機会{len(opportunities)}項目、脅威{len(threats)}項目")
        
        # 推奨戦略
        if strategies:
            primary_strategy = strategies[0]
            summary_parts.append(f"【推奨戦略】{primary_strategy.strategy_type}戦略 - {primary_strategy.strategy}")
        
        return "。".join(summary_parts)
    
    def format_result(self, result: SWOTAnalysisResult) -> str:
        """分析結果を整形して文字列で返す"""
        output = []
        output.append("=" * 60)
        output.append("SWOT分析結果")
        output.append("=" * 60)
        
        # 強み（Strengths）
        output.append("\n【強み (Strengths)】- 内部要因・プラス")
        for i, item in enumerate(result.strengths, 1):
            output.append(f"  {i}. {item.item}")
        
        # 弱み（Weaknesses）
        output.append("\n【弱み (Weaknesses)】- 内部要因・マイナス")
        for i, item in enumerate(result.weaknesses, 1):
            output.append(f"  {i}. {item.item}")
        
        # 機会（Opportunities）
        output.append("\n【機会 (Opportunities)】- 外部要因・プラス")
        for i, item in enumerate(result.opportunities, 1):
            output.append(f"  {i}. {item.item}")
        
        # 脅威（Threats）
        output.append("\n【脅威 (Threats)】- 外部要因・マイナス")
        for i, item in enumerate(result.threats, 1):
            output.append(f"  {i}. {item.item}")
        
        # クロスSWOT戦略
        output.append("\n【クロスSWOT戦略】")
        for strategy in result.cross_swot_strategies:
            output.append(f"\n  ■ {strategy.strategy_type}戦略: {strategy.strategy}")
            output.append(f"    {strategy.description}")
        
        # サマリー
        output.append(f"\n【サマリー】")
        output.append(f"  {result.summary}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
    
    def create_swot_matrix(self, result: SWOTAnalysisResult) -> str:
        """SWOTマトリックスを作成"""
        matrix = []
        matrix.append("\n" + "=" * 80)
        matrix.append("SWOTマトリックス")
        matrix.append("=" * 80)
        matrix.append("")
        matrix.append("                    内部環境")
        matrix.append("              強み (S)         |      弱み (W)")
        matrix.append("-" * 80)
        matrix.append("外部  機会 (O) | SO戦略:          | WO戦略:")
        matrix.append("環境           | 強みで機会を活用 | 弱みを改善し機会活用")
        matrix.append("-" * 80)
        matrix.append("      脅威 (T) | ST戦略:          | WT戦略:")
        matrix.append("              | 強みで脅威を回避 | 影響を最小化")
        matrix.append("-" * 80)
        
        return "\n".join(matrix)
