"""5Forces分析フレームワーク"""
from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum


class ForceLevel(str, Enum):
    """脅威レベル"""
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class ForceAnalysis(BaseModel):
    """各Forceの分析結果"""
    force_name: str
    level: ForceLevel
    factors: List[str]
    description: str


class FiveForcesResult(BaseModel):
    """5Forces分析結果"""
    new_entrants: ForceAnalysis  # 新規参入の脅威
    substitutes: ForceAnalysis  # 代替品の脅威
    buyer_power: ForceAnalysis  # 買い手の交渉力
    supplier_power: ForceAnalysis  # 売り手の交渉力
    rivalry: ForceAnalysis  # 業界内の競争
    overall_attractiveness: str  # 業界の総合的魅力度
    strategic_implications: List[str]  # 戦略的示唆


class FiveForcesAnalysis:
    """5Forces分析フレームワーク（ポーターの5つの力）"""
    
    def analyze(
        self,
        new_entrants_data: Dict,
        substitutes_data: Dict,
        buyer_data: Dict,
        supplier_data: Dict,
        rivalry_data: Dict
    ) -> FiveForcesResult:
        """
        5Forces分析を実行
        
        Args:
            new_entrants_data: 新規参入に関するデータ
            substitutes_data: 代替品に関するデータ
            buyer_data: 買い手に関するデータ
            supplier_data: 売り手に関するデータ
            rivalry_data: 業界内競争に関するデータ
        
        Returns:
            5Forces分析結果
        """
        # 各Forceを分析
        new_entrants = self._analyze_new_entrants(new_entrants_data)
        substitutes = self._analyze_substitutes(substitutes_data)
        buyer_power = self._analyze_buyer_power(buyer_data)
        supplier_power = self._analyze_supplier_power(supplier_data)
        rivalry = self._analyze_rivalry(rivalry_data)
        
        # 総合的な業界魅力度を評価
        attractiveness = self._evaluate_attractiveness(
            new_entrants, substitutes, buyer_power, supplier_power, rivalry
        )
        
        # 戦略的示唆を導出
        implications = self._derive_strategic_implications(
            new_entrants, substitutes, buyer_power, supplier_power, rivalry
        )
        
        return FiveForcesResult(
            new_entrants=new_entrants,
            substitutes=substitutes,
            buyer_power=buyer_power,
            supplier_power=supplier_power,
            rivalry=rivalry,
            overall_attractiveness=attractiveness,
            strategic_implications=implications
        )
    
    def _analyze_new_entrants(self, data: Dict) -> ForceAnalysis:
        """新規参入の脅威を分析"""
        factors = []
        score = 0
        
        # 参入障壁の評価
        if data.get("capital_requirements") == "high":
            factors.append("高い資本要件")
            score -= 1
        else:
            score += 1
        
        if data.get("economies_of_scale") == "important":
            factors.append("規模の経済が重要")
            score -= 1
        else:
            score += 1
        
        if data.get("brand_loyalty") == "strong":
            factors.append("強いブランドロイヤルティ")
            score -= 1
        else:
            score += 1
        
        if data.get("regulations") == "strict":
            factors.append("厳しい規制")
            score -= 1
        else:
            score += 1
        
        # レベル判定
        if score <= -2:
            level = ForceLevel.LOW
            description = "参入障壁が高く、新規参入の脅威は低い"
        elif score >= 2:
            level = ForceLevel.HIGH
            description = "参入障壁が低く、新規参入の脅威が高い"
        else:
            level = ForceLevel.MEDIUM
            description = "新規参入の脅威は中程度"
        
        return ForceAnalysis(
            force_name="新規参入の脅威",
            level=level,
            factors=factors,
            description=description
        )
    
    def _analyze_substitutes(self, data: Dict) -> ForceAnalysis:
        """代替品の脅威を分析"""
        factors = []
        score = 0
        
        if data.get("substitute_availability") == "many":
            factors.append("多くの代替品が存在")
            score += 1
        else:
            score -= 1
        
        if data.get("switching_cost") == "low":
            factors.append("低いスイッチングコスト")
            score += 1
        else:
            score -= 1
        
        if data.get("price_performance") == "better":
            factors.append("代替品の価格性能比が優れている")
            score += 1
        else:
            score -= 1
        
        # レベル判定
        if score >= 2:
            level = ForceLevel.HIGH
            description = "代替品の脅威が高い"
        elif score <= -2:
            level = ForceLevel.LOW
            description = "代替品の脅威は低い"
        else:
            level = ForceLevel.MEDIUM
            description = "代替品の脅威は中程度"
        
        return ForceAnalysis(
            force_name="代替品の脅威",
            level=level,
            factors=factors,
            description=description
        )
    
    def _analyze_buyer_power(self, data: Dict) -> ForceAnalysis:
        """買い手の交渉力を分析"""
        factors = []
        score = 0
        
        if data.get("buyer_concentration") == "high":
            factors.append("買い手の集中度が高い")
            score += 1
        else:
            score -= 1
        
        if data.get("switching_cost") == "low":
            factors.append("低いスイッチングコスト")
            score += 1
        else:
            score -= 1
        
        if data.get("price_sensitivity") == "high":
            factors.append("価格感度が高い")
            score += 1
        else:
            score -= 1
        
        # レベル判定
        if score >= 2:
            level = ForceLevel.HIGH
            description = "買い手の交渉力が強い"
        elif score <= -2:
            level = ForceLevel.LOW
            description = "買い手の交渉力は弱い"
        else:
            level = ForceLevel.MEDIUM
            description = "買い手の交渉力は中程度"
        
        return ForceAnalysis(
            force_name="買い手の交渉力",
            level=level,
            factors=factors,
            description=description
        )
    
    def _analyze_supplier_power(self, data: Dict) -> ForceAnalysis:
        """売り手の交渉力を分析"""
        factors = []
        score = 0
        
        if data.get("supplier_concentration") == "high":
            factors.append("売り手の集中度が高い")
            score += 1
        else:
            score -= 1
        
        if data.get("switching_cost") == "high":
            factors.append("高いスイッチングコスト")
            score += 1
        else:
            score -= 1
        
        if data.get("differentiation") == "high":
            factors.append("高い差別化")
            score += 1
        else:
            score -= 1
        
        # レベル判定
        if score >= 2:
            level = ForceLevel.HIGH
            description = "売り手の交渉力が強い"
        elif score <= -2:
            level = ForceLevel.LOW
            description = "売り手の交渉力は弱い"
        else:
            level = ForceLevel.MEDIUM
            description = "売り手の交渉力は中程度"
        
        return ForceAnalysis(
            force_name="売り手の交渉力",
            level=level,
            factors=factors,
            description=description
        )
    
    def _analyze_rivalry(self, data: Dict) -> ForceAnalysis:
        """業界内の競争を分析"""
        factors = []
        score = 0
        
        if data.get("number_of_competitors") == "many":
            factors.append("多数の競合企業")
            score += 1
        else:
            score -= 1
        
        if data.get("industry_growth") == "slow":
            factors.append("業界成長率が低い")
            score += 1
        else:
            score -= 1
        
        if data.get("product_differentiation") == "low":
            factors.append("製品差別化が低い")
            score += 1
        else:
            score -= 1
        
        if data.get("exit_barriers") == "high":
            factors.append("高い退出障壁")
            score += 1
        else:
            score -= 1
        
        # レベル判定
        if score >= 2:
            level = ForceLevel.HIGH
            description = "業界内の競争が激しい"
        elif score <= -2:
            level = ForceLevel.LOW
            description = "業界内の競争は穏やか"
        else:
            level = ForceLevel.MEDIUM
            description = "業界内の競争は中程度"
        
        return ForceAnalysis(
            force_name="業界内の競争",
            level=level,
            factors=factors,
            description=description
        )
    
    def _evaluate_attractiveness(
        self,
        new_entrants: ForceAnalysis,
        substitutes: ForceAnalysis,
        buyer_power: ForceAnalysis,
        supplier_power: ForceAnalysis,
        rivalry: ForceAnalysis
    ) -> str:
        """業界の総合的魅力度を評価"""
        # 各Forceのレベルをスコア化
        level_scores = {
            ForceLevel.HIGH: -1,
            ForceLevel.MEDIUM: 0,
            ForceLevel.LOW: 1
        }
        
        total_score = (
            level_scores[new_entrants.level] +
            level_scores[substitutes.level] +
            level_scores[buyer_power.level] +
            level_scores[supplier_power.level] +
            level_scores[rivalry.level]
        )
        
        if total_score >= 3:
            return "高い魅力度 - 収益性の高い業界"
        elif total_score <= -3:
            return "低い魅力度 - 厳しい競争環境"
        else:
            return "中程度の魅力度 - 戦略次第で収益確保可能"
    
    def _derive_strategic_implications(
        self,
        new_entrants: ForceAnalysis,
        substitutes: ForceAnalysis,
        buyer_power: ForceAnalysis,
        supplier_power: ForceAnalysis,
        rivalry: ForceAnalysis
    ) -> List[str]:
        """戦略的示唆を導出"""
        implications = []
        
        # 新規参入対策
        if new_entrants.level == ForceLevel.HIGH:
            implications.append("参入障壁の構築（ブランド強化、規模の経済の追求）")
        
        # 代替品対策
        if substitutes.level == ForceLevel.HIGH:
            implications.append("差別化戦略の強化、顧客ロイヤルティの向上")
        
        # 買い手対策
        if buyer_power.level == ForceLevel.HIGH:
            implications.append("製品差別化、スイッチングコストの向上")
        
        # 売り手対策
        if supplier_power.level == ForceLevel.HIGH:
            implications.append("サプライヤーの多様化、垂直統合の検討")
        
        # 競争対策
        if rivalry.level == ForceLevel.HIGH:
            implications.append("ニッチ市場への特化、コストリーダーシップの追求")
        
        return implications
    
    def format_result(self, result: FiveForcesResult) -> str:
        """分析結果を整形して文字列で返す"""
        output = []
        output.append("=" * 60)
        output.append("5Forces分析結果（ポーターの5つの力）")
        output.append("=" * 60)
        
        # 各Forceの分析結果
        for force in [result.new_entrants, result.substitutes, result.buyer_power, 
                      result.supplier_power, result.rivalry]:
            output.append(f"\n【{force.force_name}】")
            output.append(f"  脅威レベル: {force.level.value}")
            output.append(f"  {force.description}")
            if force.factors:
                output.append("  要因:")
                for factor in force.factors:
                    output.append(f"    - {factor}")
        
        # 総合評価
        output.append(f"\n【業界の総合的魅力度】")
        output.append(f"  {result.overall_attractiveness}")
        
        # 戦略的示唆
        if result.strategic_implications:
            output.append(f"\n【戦略的示唆】")
            for i, implication in enumerate(result.strategic_implications, 1):
                output.append(f"  {i}. {implication}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
