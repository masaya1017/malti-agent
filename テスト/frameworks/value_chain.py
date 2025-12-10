"""バリューチェーン分析フレームワーク"""
from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum


class ActivityType(str, Enum):
    """活動タイプ"""
    PRIMARY = "主活動"
    SUPPORT = "支援活動"


class Activity(BaseModel):
    """活動"""
    name: str
    activity_type: ActivityType
    description: str
    cost_driver: Optional[str] = None
    value_added: Optional[str] = None
    competitive_advantage: Optional[str] = None


class ValueChainResult(BaseModel):
    """バリューチェーン分析結果"""
    primary_activities: List[Activity]
    support_activities: List[Activity]
    cost_structure: Dict[str, float]
    value_creation_points: List[str]
    competitive_advantages: List[str]
    improvement_opportunities: List[str]


class ValueChainAnalysis:
    """バリューチェーン分析フレームワーク"""
    
    def analyze(
        self,
        primary_activities_data: Dict,
        support_activities_data: Dict,
        cost_data: Optional[Dict] = None
    ) -> ValueChainResult:
        """
        バリューチェーン分析を実行
        
        Args:
            primary_activities_data: 主活動データ
            support_activities_data: 支援活動データ
            cost_data: コストデータ（オプション）
        
        Returns:
            バリューチェーン分析結果
        """
        # 主活動の分析
        primary_activities = self._analyze_primary_activities(primary_activities_data)
        
        # 支援活動の分析
        support_activities = self._analyze_support_activities(support_activities_data)
        
        # コスト構造の分析
        cost_structure = self._analyze_cost_structure(cost_data or {})
        
        # 価値創造ポイントの特定
        value_creation_points = self._identify_value_creation_points(
            primary_activities, support_activities
        )
        
        # 競争優位性の特定
        competitive_advantages = self._identify_competitive_advantages(
            primary_activities, support_activities
        )
        
        # 改善機会の特定
        improvement_opportunities = self._identify_improvement_opportunities(
            primary_activities, support_activities
        )
        
        return ValueChainResult(
            primary_activities=primary_activities,
            support_activities=support_activities,
            cost_structure=cost_structure,
            value_creation_points=value_creation_points,
            competitive_advantages=competitive_advantages,
            improvement_opportunities=improvement_opportunities
        )
    
    def _analyze_primary_activities(self, data: Dict) -> List[Activity]:
        """主活動を分析"""
        activities = []
        
        # 購買物流
        if "inbound_logistics" in data:
            activities.append(Activity(
                name="購買物流",
                activity_type=ActivityType.PRIMARY,
                description=data["inbound_logistics"].get("description", "原材料の受入・保管・配送"),
                cost_driver=data["inbound_logistics"].get("cost_driver"),
                value_added=data["inbound_logistics"].get("value_added")
            ))
        
        # 製造
        if "operations" in data:
            activities.append(Activity(
                name="製造",
                activity_type=ActivityType.PRIMARY,
                description=data["operations"].get("description", "製品・サービスの生産"),
                cost_driver=data["operations"].get("cost_driver"),
                value_added=data["operations"].get("value_added")
            ))
        
        # 出荷物流
        if "outbound_logistics" in data:
            activities.append(Activity(
                name="出荷物流",
                activity_type=ActivityType.PRIMARY,
                description=data["outbound_logistics"].get("description", "製品の保管・配送"),
                cost_driver=data["outbound_logistics"].get("cost_driver"),
                value_added=data["outbound_logistics"].get("value_added")
            ))
        
        # 販売・マーケティング
        if "marketing_sales" in data:
            activities.append(Activity(
                name="販売・マーケティング",
                activity_type=ActivityType.PRIMARY,
                description=data["marketing_sales"].get("description", "製品の販売促進"),
                cost_driver=data["marketing_sales"].get("cost_driver"),
                value_added=data["marketing_sales"].get("value_added")
            ))
        
        # サービス
        if "service" in data:
            activities.append(Activity(
                name="サービス",
                activity_type=ActivityType.PRIMARY,
                description=data["service"].get("description", "アフターサービス・保守"),
                cost_driver=data["service"].get("cost_driver"),
                value_added=data["service"].get("value_added")
            ))
        
        return activities
    
    def _analyze_support_activities(self, data: Dict) -> List[Activity]:
        """支援活動を分析"""
        activities = []
        
        # 企業インフラ
        if "infrastructure" in data:
            activities.append(Activity(
                name="企業インフラ",
                activity_type=ActivityType.SUPPORT,
                description=data["infrastructure"].get("description", "経営管理・財務・法務"),
                cost_driver=data["infrastructure"].get("cost_driver"),
                value_added=data["infrastructure"].get("value_added")
            ))
        
        # 人事・労務管理
        if "hrm" in data:
            activities.append(Activity(
                name="人事・労務管理",
                activity_type=ActivityType.SUPPORT,
                description=data["hrm"].get("description", "採用・育成・評価"),
                cost_driver=data["hrm"].get("cost_driver"),
                value_added=data["hrm"].get("value_added")
            ))
        
        # 技術開発
        if "technology" in data:
            activities.append(Activity(
                name="技術開発",
                activity_type=ActivityType.SUPPORT,
                description=data["technology"].get("description", "R&D・プロセス改善"),
                cost_driver=data["technology"].get("cost_driver"),
                value_added=data["technology"].get("value_added")
            ))
        
        # 調達
        if "procurement" in data:
            activities.append(Activity(
                name="調達",
                activity_type=ActivityType.SUPPORT,
                description=data["procurement"].get("description", "資材・設備の調達"),
                cost_driver=data["procurement"].get("cost_driver"),
                value_added=data["procurement"].get("value_added")
            ))
        
        return activities
    
    def _analyze_cost_structure(self, data: Dict) -> Dict[str, float]:
        """コスト構造を分析"""
        return {
            "購買物流": data.get("inbound_logistics_cost", 0),
            "製造": data.get("operations_cost", 0),
            "出荷物流": data.get("outbound_logistics_cost", 0),
            "販売・マーケティング": data.get("marketing_sales_cost", 0),
            "サービス": data.get("service_cost", 0),
            "企業インフラ": data.get("infrastructure_cost", 0),
            "人事・労務": data.get("hrm_cost", 0),
            "技術開発": data.get("technology_cost", 0),
            "調達": data.get("procurement_cost", 0),
        }
    
    def _identify_value_creation_points(
        self,
        primary: List[Activity],
        support: List[Activity]
    ) -> List[str]:
        """価値創造ポイントを特定"""
        points = []
        
        for activity in primary + support:
            if activity.value_added:
                points.append(f"{activity.name}: {activity.value_added}")
        
        return points
    
    def _identify_competitive_advantages(
        self,
        primary: List[Activity],
        support: List[Activity]
    ) -> List[str]:
        """競争優位性を特定"""
        advantages = []
        
        for activity in primary + support:
            if activity.competitive_advantage:
                advantages.append(f"{activity.name}: {activity.competitive_advantage}")
        
        return advantages
    
    def _identify_improvement_opportunities(
        self,
        primary: List[Activity],
        support: List[Activity]
    ) -> List[str]:
        """改善機会を特定"""
        opportunities = []
        
        # コストドライバーが高い活動を改善機会として特定
        for activity in primary + support:
            if activity.cost_driver and "高" in activity.cost_driver:
                opportunities.append(f"{activity.name}のコスト削減")
        
        return opportunities
    
    def format_result(self, result: ValueChainResult) -> str:
        """分析結果を整形して文字列で返す"""
        output = []
        output.append("=" * 60)
        output.append("バリューチェーン分析結果")
        output.append("=" * 60)
        
        # 主活動
        output.append("\n【主活動 (Primary Activities)】")
        for activity in result.primary_activities:
            output.append(f"\n  ■ {activity.name}")
            output.append(f"    {activity.description}")
            if activity.value_added:
                output.append(f"    付加価値: {activity.value_added}")
        
        # 支援活動
        output.append("\n【支援活動 (Support Activities)】")
        for activity in result.support_activities:
            output.append(f"\n  ■ {activity.name}")
            output.append(f"    {activity.description}")
            if activity.value_added:
                output.append(f"    付加価値: {activity.value_added}")
        
        # 価値創造ポイント
        if result.value_creation_points:
            output.append("\n【価値創造ポイント】")
            for i, point in enumerate(result.value_creation_points, 1):
                output.append(f"  {i}. {point}")
        
        # 競争優位性
        if result.competitive_advantages:
            output.append("\n【競争優位性】")
            for i, advantage in enumerate(result.competitive_advantages, 1):
                output.append(f"  {i}. {advantage}")
        
        # 改善機会
        if result.improvement_opportunities:
            output.append("\n【改善機会】")
            for i, opp in enumerate(result.improvement_opportunities, 1):
                output.append(f"  {i}. {opp}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
