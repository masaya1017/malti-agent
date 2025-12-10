"""3C分析フレームワーク"""
from typing import Dict, List, Optional
from pydantic import BaseModel


class CustomerAnalysis(BaseModel):
    """顧客分析結果"""
    market_size: Optional[float] = None
    growth_rate: Optional[float] = None
    segments: List[str] = []
    needs: List[str] = []
    buying_behavior: Optional[str] = None


class CompetitorAnalysis(BaseModel):
    """競合分析結果"""
    direct_competitors: List[Dict] = []
    indirect_competitors: List[Dict] = []
    market_share: Dict[str, float] = {}
    competitive_advantages: Dict[str, Dict] = {}


class CompanyAnalysis(BaseModel):
    """自社分析結果"""
    core_competencies: List[str] = []
    resources: Dict = {}
    value_proposition: Optional[str] = None
    current_position: Optional[str] = None


class ThreeCAnalysisResult(BaseModel):
    """3C分析結果"""
    customer: CustomerAnalysis
    competitor: CompetitorAnalysis
    company: CompanyAnalysis
    insights: List[str] = []


class ThreeCAnalysis:
    """3C分析フレームワーク"""
    
    def analyze(
        self,
        customer_data: dict,
        competitor_data: dict,
        company_data: dict
    ) -> ThreeCAnalysisResult:
        """
        3C分析を実行
        
        Args:
            customer_data: 顧客データ（市場規模、ニーズ、セグメント等）
            competitor_data: 競合データ（競合企業、シェア、強み等）
            company_data: 自社データ（強み、弱み、リソース等）
        
        Returns:
            分析結果
        """
        customer = self._analyze_customer(customer_data)
        competitor = self._analyze_competitor(competitor_data)
        company = self._analyze_company(company_data)
        insights = self._derive_insights(customer_data, competitor_data, company_data)
        
        return ThreeCAnalysisResult(
            customer=customer,
            competitor=competitor,
            company=company,
            insights=insights
        )
    
    def _analyze_customer(self, data: dict) -> CustomerAnalysis:
        """顧客分析"""
        return CustomerAnalysis(
            market_size=data.get("market_size"),
            growth_rate=data.get("growth_rate"),
            segments=data.get("segments", []),
            needs=data.get("needs", []),
            buying_behavior=data.get("buying_behavior"),
        )
    
    def _analyze_competitor(self, data: dict) -> CompetitorAnalysis:
        """競合分析"""
        competitors = data.get("competitors", [])
        
        return CompetitorAnalysis(
            direct_competitors=[c for c in competitors if c.get("type") == "direct"],
            indirect_competitors=[c for c in competitors if c.get("type") == "indirect"],
            market_share=self._calculate_market_share(competitors),
            competitive_advantages=self._identify_advantages(competitors),
        )
    
    def _analyze_company(self, data: dict) -> CompanyAnalysis:
        """自社分析"""
        return CompanyAnalysis(
            core_competencies=data.get("core_competencies", []),
            resources=data.get("resources", {}),
            value_proposition=data.get("value_proposition"),
            current_position=data.get("market_position"),
        )
    
    def _derive_insights(
        self,
        customer: dict,
        competitor: dict,
        company: dict
    ) -> List[str]:
        """戦略的洞察の導出"""
        insights = []
        
        # 市場機会の特定
        growth_rate = customer.get("growth_rate", 0)
        if growth_rate > 10:
            insights.append(f"高成長市場（成長率{growth_rate}%）であり、積極的な投資機会がある")
        elif growth_rate < 0:
            insights.append(f"市場が縮小傾向（成長率{growth_rate}%）にあり、慎重な戦略が必要")
        
        # 競争優位性の評価
        company_strengths = set(company.get("core_competencies", []))
        competitor_strengths = set()
        for comp in competitor.get("competitors", []):
            competitor_strengths.update(comp.get("strengths", []))
        
        unique_strengths = company_strengths - competitor_strengths
        if unique_strengths:
            insights.append(f"独自の強み: {', '.join(unique_strengths)}")
        
        # 市場規模の評価
        market_size = customer.get("market_size")
        if market_size:
            if market_size > 100000000000:  # 1000億円以上
                insights.append(f"大規模市場（{market_size:,.0f}円）であり、スケールメリットを追求できる")
            elif market_size < 10000000000:  # 100億円未満
                insights.append(f"ニッチ市場（{market_size:,.0f}円）であり、特化戦略が有効")
        
        return insights
    
    def _calculate_market_share(self, competitors: List[dict]) -> Dict[str, float]:
        """市場シェア計算"""
        total_revenue = sum(c.get("revenue", 0) for c in competitors)
        
        if total_revenue == 0:
            return {}
        
        shares = {}
        for comp in competitors:
            name = comp.get("name")
            revenue = comp.get("revenue", 0)
            shares[name] = round((revenue / total_revenue * 100), 2)
        
        return shares
    
    def _identify_advantages(self, competitors: List[dict]) -> Dict[str, Dict]:
        """競争優位性の特定"""
        advantages = {}
        
        for comp in competitors:
            name = comp.get("name")
            advantages[name] = {
                "cost_leadership": comp.get("cost_advantage", False),
                "differentiation": comp.get("unique_features", []),
                "focus_strategy": comp.get("niche_market"),
            }
        
        return advantages
    
    def format_result(self, result: ThreeCAnalysisResult) -> str:
        """分析結果を整形して文字列で返す"""
        output = []
        output.append("=" * 60)
        output.append("3C分析結果")
        output.append("=" * 60)
        
        # 顧客分析
        output.append("\n【顧客分析 (Customer)】")
        if result.customer.market_size:
            output.append(f"  市場規模: {result.customer.market_size:,.0f}円")
        if result.customer.growth_rate is not None:
            output.append(f"  成長率: {result.customer.growth_rate}%")
        if result.customer.segments:
            output.append(f"  セグメント: {', '.join(result.customer.segments)}")
        if result.customer.needs:
            output.append(f"  顧客ニーズ: {', '.join(result.customer.needs)}")
        
        # 競合分析
        output.append("\n【競合分析 (Competitor)】")
        if result.competitor.direct_competitors:
            output.append(f"  直接競合: {len(result.competitor.direct_competitors)}社")
        if result.competitor.market_share:
            output.append("  市場シェア:")
            for name, share in result.competitor.market_share.items():
                output.append(f"    - {name}: {share}%")
        
        # 自社分析
        output.append("\n【自社分析 (Company)】")
        if result.company.core_competencies:
            output.append(f"  コアコンピタンス: {', '.join(result.company.core_competencies)}")
        if result.company.value_proposition:
            output.append(f"  価値提案: {result.company.value_proposition}")
        
        # 戦略的洞察
        if result.insights:
            output.append("\n【戦略的洞察】")
            for i, insight in enumerate(result.insights, 1):
                output.append(f"  {i}. {insight}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
