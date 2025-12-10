"""データスキーマ定義"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CompetitorInfo(BaseModel):
    """競合企業情報"""
    name: str = Field(description="企業名")
    type: str = Field(description="競合タイプ (direct/indirect)")
    revenue: Optional[float] = Field(default=None, description="売上高")
    strengths: List[str] = Field(default_factory=list, description="強み")
    cost_advantage: Optional[bool] = Field(default=None, description="コスト優位性")
    unique_features: Optional[List[str]] = Field(default=None, description="独自機能")
    niche_market: Optional[str] = Field(default=None, description="ニッチ市場")


class CustomerData(BaseModel):
    """顧客データ"""
    market_size: Optional[float] = Field(default=None, description="市場規模")
    growth_rate: Optional[float] = Field(default=None, description="成長率 (%)")
    segments: List[str] = Field(default_factory=list, description="市場セグメント")
    needs: List[str] = Field(default_factory=list, description="顧客ニーズ")
    buying_behavior: Optional[str] = Field(default=None, description="購買行動")


class CompetitorData(BaseModel):
    """競合データ"""
    competitors: List[CompetitorInfo] = Field(default_factory=list, description="競合企業リスト")


class CompanyData(BaseModel):
    """自社データ"""
    core_competencies: List[str] = Field(default_factory=list, description="コアコンピタンス")
    resources: Optional[Dict[str, Any]] = Field(default=None, description="リソース")
    value_proposition: Optional[str] = Field(default=None, description="価値提案")
    market_position: Optional[str] = Field(default=None, description="市場ポジション")


class CustomerSegment(BaseModel):
    """顧客セグメント"""
    name: str = Field(description="セグメント名")
    size: Optional[float] = Field(default=None, description="セグメント規模")
    growth_rate: Optional[float] = Field(default=None, description="成長率 (%)")
    characteristics: List[str] = Field(default_factory=list, description="特性")


class MarketAnalysisData(BaseModel):
    """市場分析データ"""
    market_size: Optional[float] = Field(default=None, description="市場規模")
    growth_rate: Optional[float] = Field(default=None, description="成長率 (%)")
    market_segments: List[str] = Field(default_factory=list, description="市場セグメント")
    market_trends: List[str] = Field(default_factory=list, description="市場トレンド")
    customer_segments: List[CustomerSegment] = Field(default_factory=list, description="顧客セグメント詳細")
    market_share_data: Optional[Dict[str, float]] = Field(default=None, description="市場シェアデータ")


class FinancialData(BaseModel):
    """財務データ"""
    revenue: Optional[float] = Field(default=None, description="売上高")
    cost_of_sales: Optional[float] = Field(default=None, description="売上原価")
    operating_expenses: Optional[float] = Field(default=None, description="営業費用")
    assets: Optional[float] = Field(default=None, description="資産")
    liabilities: Optional[float] = Field(default=None, description="負債")
    equity: Optional[float] = Field(default=None, description="純資産")
    cash_flow_operating: Optional[float] = Field(default=None, description="営業キャッシュフロー")
    cash_flow_investing: Optional[float] = Field(default=None, description="投資キャッシュフロー")
    cash_flow_financing: Optional[float] = Field(default=None, description="財務キャッシュフロー")


class ClientData(BaseModel):
    """クライアント情報の完全なスキーマ"""
    customer_data: Optional[CustomerData] = Field(default=None, description="顧客データ")
    competitor_data: Optional[CompetitorData] = Field(default=None, description="競合データ")
    company_data: Optional[CompanyData] = Field(default=None, description="自社データ")
    market_analysis_data: Optional[MarketAnalysisData] = Field(default=None, description="市場分析データ")
    financial_data: Optional[FinancialData] = Field(default=None, description="財務データ")
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換（Noneを除外）"""
        result = {}
        for field_name, field_value in self.model_dump().items():
            if field_value is not None:
                result[field_name] = field_value
        return result
