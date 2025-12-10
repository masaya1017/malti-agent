"""PEST分析フレームワーク"""
from typing import List, Dict
from pydantic import BaseModel
from enum import Enum


class ImpactLevel(str, Enum):
    """影響レベル"""
    POSITIVE = "プラス"
    NEGATIVE = "マイナス"
    NEUTRAL = "中立"


class PESTFactor(BaseModel):
    """PEST要因"""
    category: str  # Political, Economic, Social, Technological
    factor: str
    description: str
    impact: ImpactLevel
    timeframe: str  # short-term, medium-term, long-term


class PESTAnalysisResult(BaseModel):
    """PEST分析結果"""
    political_factors: List[PESTFactor]
    economic_factors: List[PESTFactor]
    social_factors: List[PESTFactor]
    technological_factors: List[PESTFactor]
    key_opportunities: List[str]
    key_threats: List[str]
    strategic_recommendations: List[str]


class PESTAnalysis:
    """PEST分析フレームワーク（マクロ環境分析）"""
    
    def analyze(
        self,
        political_data: List[Dict],
        economic_data: List[Dict],
        social_data: List[Dict],
        technological_data: List[Dict]
    ) -> PESTAnalysisResult:
        """
        PEST分析を実行
        
        Args:
            political_data: 政治的要因データ
            economic_data: 経済的要因データ
            social_data: 社会的要因データ
            technological_data: 技術的要因データ
        
        Returns:
            PEST分析結果
        """
        # 各要因を分析
        political = self._analyze_political(political_data)
        economic = self._analyze_economic(economic_data)
        social = self._analyze_social(social_data)
        technological = self._analyze_technological(technological_data)
        
        # 主要な機会と脅威を特定
        opportunities, threats = self._identify_opportunities_threats(
            political, economic, social, technological
        )
        
        # 戦略的推奨事項を導出
        recommendations = self._derive_recommendations(
            political, economic, social, technological, opportunities, threats
        )
        
        return PESTAnalysisResult(
            political_factors=political,
            economic_factors=economic,
            social_factors=social,
            technological_factors=technological,
            key_opportunities=opportunities,
            key_threats=threats,
            strategic_recommendations=recommendations
        )
    
    def _analyze_political(self, data: List[Dict]) -> List[PESTFactor]:
        """政治的要因を分析"""
        factors = []
        
        for item in data:
            factors.append(PESTFactor(
                category="Political",
                factor=item.get("factor", ""),
                description=item.get("description", ""),
                impact=ImpactLevel(item.get("impact", "中立")),
                timeframe=item.get("timeframe", "medium-term")
            ))
        
        return factors
    
    def _analyze_economic(self, data: List[Dict]) -> List[PESTFactor]:
        """経済的要因を分析"""
        factors = []
        
        for item in data:
            factors.append(PESTFactor(
                category="Economic",
                factor=item.get("factor", ""),
                description=item.get("description", ""),
                impact=ImpactLevel(item.get("impact", "中立")),
                timeframe=item.get("timeframe", "medium-term")
            ))
        
        return factors
    
    def _analyze_social(self, data: List[Dict]) -> List[PESTFactor]:
        """社会的要因を分析"""
        factors = []
        
        for item in data:
            factors.append(PESTFactor(
                category="Social",
                factor=item.get("factor", ""),
                description=item.get("description", ""),
                impact=ImpactLevel(item.get("impact", "中立")),
                timeframe=item.get("timeframe", "medium-term")
            ))
        
        return factors
    
    def _analyze_technological(self, data: List[Dict]) -> List[PESTFactor]:
        """技術的要因を分析"""
        factors = []
        
        for item in data:
            factors.append(PESTFactor(
                category="Technological",
                factor=item.get("factor", ""),
                description=item.get("description", ""),
                impact=ImpactLevel(item.get("impact", "中立")),
                timeframe=item.get("timeframe", "medium-term")
            ))
        
        return factors
    
    def _identify_opportunities_threats(
        self,
        political: List[PESTFactor],
        economic: List[PESTFactor],
        social: List[PESTFactor],
        technological: List[PESTFactor]
    ) -> tuple[List[str], List[str]]:
        """主要な機会と脅威を特定"""
        opportunities = []
        threats = []
        
        all_factors = political + economic + social + technological
        
        for factor in all_factors:
            if factor.impact == ImpactLevel.POSITIVE:
                opportunities.append(f"{factor.category}: {factor.factor}")
            elif factor.impact == ImpactLevel.NEGATIVE:
                threats.append(f"{factor.category}: {factor.factor}")
        
        return opportunities, threats
    
    def _derive_recommendations(
        self,
        political: List[PESTFactor],
        economic: List[PESTFactor],
        social: List[PESTFactor],
        technological: List[PESTFactor],
        opportunities: List[str],
        threats: List[str]
    ) -> List[str]:
        """戦略的推奨事項を導出"""
        recommendations = []
        
        # 機会への対応
        if opportunities:
            recommendations.append(f"機会の活用: {len(opportunities)}件の機会を戦略に組み込む")
        
        # 脅威への対応
        if threats:
            recommendations.append(f"脅威への対策: {len(threats)}件の脅威に対するリスク管理計画を策定")
        
        # 技術的要因への対応
        tech_positive = [f for f in technological if f.impact == ImpactLevel.POSITIVE]
        if tech_positive:
            recommendations.append("技術革新への投資: デジタルトランスフォーメーションの推進")
        
        # 社会的要因への対応
        social_positive = [f for f in social if f.impact == ImpactLevel.POSITIVE]
        if social_positive:
            recommendations.append("社会トレンドへの適応: 消費者ニーズの変化に対応した製品・サービス開発")
        
        return recommendations
    
    def format_result(self, result: PESTAnalysisResult) -> str:
        """分析結果を整形して文字列で返す"""
        output = []
        output.append("=" * 60)
        output.append("PEST分析結果（マクロ環境分析）")
        output.append("=" * 60)
        
        # Political（政治的要因）
        output.append("\n【Political - 政治的要因】")
        for factor in result.political_factors:
            output.append(f"\n  ■ {factor.factor}")
            output.append(f"    {factor.description}")
            output.append(f"    影響: {factor.impact.value} / 時間軸: {factor.timeframe}")
        
        # Economic（経済的要因）
        output.append("\n【Economic - 経済的要因】")
        for factor in result.economic_factors:
            output.append(f"\n  ■ {factor.factor}")
            output.append(f"    {factor.description}")
            output.append(f"    影響: {factor.impact.value} / 時間軸: {factor.timeframe}")
        
        # Social（社会的要因）
        output.append("\n【Social - 社会的要因】")
        for factor in result.social_factors:
            output.append(f"\n  ■ {factor.factor}")
            output.append(f"    {factor.description}")
            output.append(f"    影響: {factor.impact.value} / 時間軸: {factor.timeframe}")
        
        # Technological（技術的要因）
        output.append("\n【Technological - 技術的要因】")
        for factor in result.technological_factors:
            output.append(f"\n  ■ {factor.factor}")
            output.append(f"    {factor.description}")
            output.append(f"    影響: {factor.impact.value} / 時間軸: {factor.timeframe}")
        
        # 主要な機会
        if result.key_opportunities:
            output.append("\n【主要な機会】")
            for i, opp in enumerate(result.key_opportunities, 1):
                output.append(f"  {i}. {opp}")
        
        # 主要な脅威
        if result.key_threats:
            output.append("\n【主要な脅威】")
            for i, threat in enumerate(result.key_threats, 1):
                output.append(f"  {i}. {threat}")
        
        # 戦略的推奨事項
        if result.strategic_recommendations:
            output.append("\n【戦略的推奨事項】")
            for i, rec in enumerate(result.strategic_recommendations, 1):
                output.append(f"  {i}. {rec}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
