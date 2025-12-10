"""市場分析フレームワーク"""
from typing import Dict, Any, List
import json


class MarketAnalysis:
    """市場分析を実行するクラス"""
    
    def __init__(self):
        """初期化"""
        pass
    
    def analyze(
        self,
        market_size: float,
        growth_rate: float,
        market_segments: List[str],
        market_trends: List[str],
        customer_segments: List[Dict[str, Any]],
        market_share_data: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        市場分析を実行
        
        Args:
            market_size: 市場規模（円）
            growth_rate: 成長率（%）
            market_segments: 市場セグメント
            market_trends: 市場トレンド
            customer_segments: 顧客セグメント情報
            market_share_data: 市場シェアデータ
        
        Returns:
            分析結果
        """
        # 市場魅力度を計算
        market_attractiveness = self._calculate_market_attractiveness(
            market_size, growth_rate
        )
        
        # セグメント分析
        segment_analysis = self._analyze_segments(
            customer_segments, market_segments
        )
        
        # 市場シェア分析
        share_analysis = self._analyze_market_share(market_share_data)
        
        # トレンド分析
        trend_insights = self._analyze_trends(market_trends)
        
        # 戦略的推奨事項
        recommendations = self._generate_recommendations(
            market_attractiveness,
            segment_analysis,
            share_analysis,
            trend_insights
        )
        
        return {
            'market_size': market_size,
            'growth_rate': growth_rate,
            'market_attractiveness': market_attractiveness,
            'segment_analysis': segment_analysis,
            'market_share_analysis': share_analysis,
            'trend_insights': trend_insights,
            'recommendations': recommendations
        }
    
    def _calculate_market_attractiveness(
        self, market_size: float, growth_rate: float
    ) -> str:
        """市場魅力度を計算"""
        if market_size > 100000000000 and growth_rate > 10:
            return "非常に高い"
        elif market_size > 50000000000 and growth_rate > 5:
            return "高い"
        elif market_size > 10000000000 and growth_rate > 3:
            return "中程度"
        else:
            return "低い"
    
    def _analyze_segments(
        self, customer_segments: List[Dict[str, Any]], market_segments: List[str]
    ) -> List[Dict[str, Any]]:
        """セグメント分析"""
        analysis = []
        for segment in customer_segments:
            segment_name = segment.get('name', '不明')
            size = segment.get('size', 0)
            growth = segment.get('growth_rate', 0)
            
            priority = "高" if growth > 10 and size > 10000000000 else "中" if growth > 5 else "低"
            
            analysis.append({
                'segment': segment_name,
                'size': size,
                'growth_rate': growth,
                'priority': priority,
                'characteristics': segment.get('characteristics', [])
            })
        
        return analysis
    
    def _analyze_market_share(
        self, market_share_data: Dict[str, float]
    ) -> Dict[str, Any]:
        """市場シェア分析"""
        total_share = sum(market_share_data.values())
        
        # HHI（ハーフィンダール指数）を計算
        hhi = sum(share ** 2 for share in market_share_data.values())
        
        # 市場集中度を判定
        if hhi > 2500:
            concentration = "高度に集中"
        elif hhi > 1500:
            concentration = "中程度に集中"
        else:
            concentration = "競争的"
        
        # トップ3のシェア
        top_players = sorted(
            market_share_data.items(), key=lambda x: x[1], reverse=True
        )[:3]
        
        return {
            'total_tracked_share': total_share,
            'hhi': hhi,
            'concentration_level': concentration,
            'top_players': [
                {'company': name, 'share': share} 
                for name, share in top_players
            ]
        }
    
    def _analyze_trends(self, market_trends: List[str]) -> List[Dict[str, str]]:
        """トレンド分析"""
        insights = []
        
        # キーワードベースの簡易分析
        tech_keywords = ['AI', 'DX', 'クラウド', 'IoT', '自動化', 'デジタル']
        social_keywords = ['ESG', 'サステナビリティ', '働き方改革', 'リモート']
        economic_keywords = ['コスト削減', '効率化', '生産性向上']
        
        for trend in market_trends:
            impact = "高"
            category = "その他"
            
            if any(keyword in trend for keyword in tech_keywords):
                category = "技術トレンド"
                impact = "高"
            elif any(keyword in trend for keyword in social_keywords):
                category = "社会トレンド"
                impact = "中"
            elif any(keyword in trend for keyword in economic_keywords):
                category = "経済トレンド"
                impact = "高"
            
            insights.append({
                'trend': trend,
                'category': category,
                'impact': impact
            })
        
        return insights
    
    def _generate_recommendations(
        self,
        market_attractiveness: str,
        segment_analysis: List[Dict[str, Any]],
        share_analysis: Dict[str, Any],
        trend_insights: List[Dict[str, str]]
    ) -> List[str]:
        """戦略的推奨事項を生成"""
        recommendations = []
        
        # 市場魅力度に基づく推奨
        if market_attractiveness in ["非常に高い", "高い"]:
            recommendations.append(
                "高成長市場であり、積極的な市場投資と拡大戦略を推奨します"
            )
        
        # セグメント分析に基づく推奨
        high_priority_segments = [
            s['segment'] for s in segment_analysis if s['priority'] == "高"
        ]
        if high_priority_segments:
            recommendations.append(
                f"優先セグメント（{', '.join(high_priority_segments)}）に注力したマーケティング戦略を展開してください"
            )
        
        # 市場集中度に基づく推奨
        if share_analysis['concentration_level'] == "競争的":
            recommendations.append(
                "競争が激しい市場です。差別化戦略とニッチ市場の開拓を検討してください"
            )
        elif share_analysis['concentration_level'] == "高度に集中":
            recommendations.append(
                "寡占市場です。戦略的提携やM&Aによる市場地位の強化を検討してください"
            )
        
        # トレンドに基づく推奨
        high_impact_trends = [
            t['trend'] for t in trend_insights if t['impact'] == "高"
        ]
        if high_impact_trends:
            recommendations.append(
                f"重要トレンド（{', '.join(high_impact_trends[:2])}）への対応を優先してください"
            )
        
        return recommendations
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """結果をフォーマット"""
        output = []
        output.append("=" * 60)
        output.append("市場分析結果")
        output.append("=" * 60)
        output.append("")
        
        # 市場概要
        output.append("【市場概要】")
        output.append(f"  市場規模: {result['market_size']:,.0f}円")
        output.append(f"  成長率: {result['growth_rate']}%")
        output.append(f"  市場魅力度: {result['market_attractiveness']}")
        output.append("")
        
        # セグメント分析
        output.append("【セグメント分析】")
        for segment in result['segment_analysis']:
            output.append(f"  {segment['segment']}:")
            output.append(f"    - 規模: {segment['size']:,.0f}円")
            output.append(f"    - 成長率: {segment['growth_rate']}%")
            output.append(f"    - 優先度: {segment['priority']}")
        output.append("")
        
        # 市場シェア分析
        share = result['market_share_analysis']
        output.append("【市場シェア分析】")
        output.append(f"  市場集中度: {share['concentration_level']}")
        output.append(f"  HHI指数: {share['hhi']:.0f}")
        output.append("  トッププレイヤー:")
        for player in share['top_players']:
            output.append(f"    - {player['company']}: {player['share']:.1f}%")
        output.append("")
        
        # トレンド分析
        output.append("【市場トレンド】")
        for trend in result['trend_insights']:
            output.append(f"  {trend['trend']}")
            output.append(f"    カテゴリ: {trend['category']}, インパクト: {trend['impact']}")
        output.append("")
        
        # 推奨事項
        output.append("【戦略的推奨事項】")
        for i, rec in enumerate(result['recommendations'], 1):
            output.append(f"  {i}. {rec}")
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)
