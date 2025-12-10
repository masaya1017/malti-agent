"""財務分析フレームワーク"""
from typing import Dict, Any, List
import json


class FinancialAnalysis:
    """財務分析を実行するクラス"""
    
    def __init__(self):
        """初期化"""
        pass
    
    def analyze(
        self,
        revenue: float,
        cost_of_sales: float,
        operating_expenses: float,
        assets: float,
        liabilities: float,
        equity: float,
        cash_flow_operating: float,
        cash_flow_investing: float,
        cash_flow_financing: float
    ) -> Dict[str, Any]:
        """
        財務分析を実行
        
        Args:
            revenue: 売上高
            cost_of_sales: 売上原価
            operating_expenses: 営業費用
            assets: 総資産
            liabilities: 負債
            equity: 純資産
            cash_flow_operating: 営業キャッシュフロー
            cash_flow_investing: 投資キャッシュフロー
            cash_flow_financing: 財務キャッシュフロー
        
        Returns:
            分析結果
        """
        # 損益計算
        gross_profit = revenue - cost_of_sales
        operating_profit = gross_profit - operating_expenses
        
        # 収益性指標
        profitability = self._calculate_profitability(
            revenue, gross_profit, operating_profit
        )
        
        # 財務健全性指標
        financial_health = self._calculate_financial_health(
            assets, liabilities, equity
        )
        
        # キャッシュフロー分析
        cash_flow_analysis = self._analyze_cash_flow(
            cash_flow_operating,
            cash_flow_investing,
            cash_flow_financing
        )
        
        # 総合評価
        overall_assessment = self._generate_assessment(
            profitability,
            financial_health,
            cash_flow_analysis
        )
        
        # 推奨事項
        recommendations = self._generate_recommendations(
            profitability,
            financial_health,
            cash_flow_analysis
        )
        
        return {
            'revenue': revenue,
            'gross_profit': gross_profit,
            'operating_profit': operating_profit,
            'profitability_ratios': profitability,
            'financial_health_ratios': financial_health,
            'cash_flow_analysis': cash_flow_analysis,
            'overall_assessment': overall_assessment,
            'recommendations': recommendations
        }
    
    def _calculate_profitability(
        self, revenue: float, gross_profit: float, operating_profit: float
    ) -> Dict[str, Any]:
        """収益性指標を計算"""
        gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
        operating_margin = (operating_profit / revenue * 100) if revenue > 0 else 0
        
        # 評価
        gross_margin_rating = "優秀" if gross_margin > 40 else "良好" if gross_margin > 25 else "要改善"
        operating_margin_rating = "優秀" if operating_margin > 15 else "良好" if operating_margin > 8 else "要改善"
        
        return {
            'gross_margin': gross_margin,
            'gross_margin_rating': gross_margin_rating,
            'operating_margin': operating_margin,
            'operating_margin_rating': operating_margin_rating
        }
    
    def _calculate_financial_health(
        self, assets: float, liabilities: float, equity: float
    ) -> Dict[str, Any]:
        """財務健全性指標を計算"""
        # 自己資本比率
        equity_ratio = (equity / assets * 100) if assets > 0 else 0
        
        # 負債比率
        debt_ratio = (liabilities / equity * 100) if equity > 0 else 0
        
        # 流動比率（簡易版：総資産の50%を流動資産と仮定）
        current_ratio = 150  # 仮の値
        
        # 評価
        equity_ratio_rating = "優秀" if equity_ratio > 50 else "良好" if equity_ratio > 30 else "要改善"
        debt_ratio_rating = "優秀" if debt_ratio < 100 else "良好" if debt_ratio < 200 else "要改善"
        
        return {
            'equity_ratio': equity_ratio,
            'equity_ratio_rating': equity_ratio_rating,
            'debt_ratio': debt_ratio,
            'debt_ratio_rating': debt_ratio_rating,
            'current_ratio': current_ratio
        }
    
    def _analyze_cash_flow(
        self,
        operating: float,
        investing: float,
        financing: float
    ) -> Dict[str, Any]:
        """キャッシュフロー分析"""
        total_cash_flow = operating + investing + financing
        
        # キャッシュフローパターンを判定
        pattern = self._determine_cash_flow_pattern(
            operating, investing, financing
        )
        
        # フリーキャッシュフロー
        free_cash_flow = operating + investing
        
        return {
            'operating_cf': operating,
            'investing_cf': investing,
            'financing_cf': financing,
            'total_cf': total_cash_flow,
            'free_cash_flow': free_cash_flow,
            'pattern': pattern,
            'health_status': "健全" if operating > 0 and free_cash_flow > 0 else "要注意"
        }
    
    def _determine_cash_flow_pattern(
        self, operating: float, investing: float, financing: float
    ) -> str:
        """キャッシュフローパターンを判定"""
        if operating > 0 and investing < 0 and financing < 0:
            return "優良企業型（本業で稼ぎ、投資と返済を実施）"
        elif operating > 0 and investing < 0 and financing > 0:
            return "成長企業型（本業で稼ぎつつ、資金調達して投資）"
        elif operating > 0 and investing > 0 and financing > 0:
            return "資産売却型（資産を売却して資金調達）"
        elif operating < 0 and investing > 0 and financing > 0:
            return "危機企業型（本業赤字、資産売却と資金調達）"
        elif operating > 0 and investing > 0 and financing < 0:
            return "リストラ型（資産売却で借入返済）"
        else:
            return "その他のパターン"
    
    def _generate_assessment(
        self,
        profitability: Dict[str, Any],
        financial_health: Dict[str, Any],
        cash_flow: Dict[str, Any]
    ) -> str:
        """総合評価を生成"""
        scores = []
        
        # 収益性スコア
        if profitability['gross_margin_rating'] == "優秀":
            scores.append(3)
        elif profitability['gross_margin_rating'] == "良好":
            scores.append(2)
        else:
            scores.append(1)
        
        # 財務健全性スコア
        if financial_health['equity_ratio_rating'] == "優秀":
            scores.append(3)
        elif financial_health['equity_ratio_rating'] == "良好":
            scores.append(2)
        else:
            scores.append(1)
        
        # キャッシュフロースコア
        if cash_flow['health_status'] == "健全":
            scores.append(3)
        else:
            scores.append(1)
        
        avg_score = sum(scores) / len(scores)
        
        if avg_score >= 2.5:
            return "財務状況は非常に良好です"
        elif avg_score >= 2.0:
            return "財務状況は良好ですが、一部改善の余地があります"
        elif avg_score >= 1.5:
            return "財務状況は中程度です。改善が必要な領域があります"
        else:
            return "財務状況に課題があります。早急な改善が必要です"
    
    def _generate_recommendations(
        self,
        profitability: Dict[str, Any],
        financial_health: Dict[str, Any],
        cash_flow: Dict[str, Any]
    ) -> List[str]:
        """推奨事項を生成"""
        recommendations = []
        
        # 収益性に関する推奨
        if profitability['gross_margin_rating'] == "要改善":
            recommendations.append(
                "売上総利益率が低いため、原価削減または価格戦略の見直しを検討してください"
            )
        
        if profitability['operating_margin_rating'] == "要改善":
            recommendations.append(
                "営業利益率が低いため、営業費用の最適化を検討してください"
            )
        
        # 財務健全性に関する推奨
        if financial_health['equity_ratio_rating'] == "要改善":
            recommendations.append(
                "自己資本比率が低いため、財務体質の強化（増資や利益剰余金の蓄積）を検討してください"
            )
        
        if financial_health['debt_ratio_rating'] == "要改善":
            recommendations.append(
                "負債比率が高いため、借入金の削減や資本増強を検討してください"
            )
        
        # キャッシュフローに関する推奨
        if cash_flow['health_status'] == "要注意":
            recommendations.append(
                "キャッシュフローに課題があります。営業活動からのキャッシュ創出力を強化してください"
            )
        
        if cash_flow['free_cash_flow'] < 0:
            recommendations.append(
                "フリーキャッシュフローがマイナスです。投資の優先順位を見直し、資金効率を改善してください"
            )
        
        # 推奨事項がない場合
        if not recommendations:
            recommendations.append(
                "財務状況は良好です。現在の戦略を継続しつつ、さらなる成長機会を探索してください"
            )
        
        return recommendations
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """結果をフォーマット"""
        output = []
        output.append("=" * 60)
        output.append("財務分析結果")
        output.append("=" * 60)
        output.append("")
        
        # 損益概要
        output.append("【損益概要】")
        output.append(f"  売上高: {result['revenue']:,.0f}円")
        output.append(f"  売上総利益: {result['gross_profit']:,.0f}円")
        output.append(f"  営業利益: {result['operating_profit']:,.0f}円")
        output.append("")
        
        # 収益性指標
        prof = result['profitability_ratios']
        output.append("【収益性指標】")
        output.append(f"  売上総利益率: {prof['gross_margin']:.1f}% ({prof['gross_margin_rating']})")
        output.append(f"  営業利益率: {prof['operating_margin']:.1f}% ({prof['operating_margin_rating']})")
        output.append("")
        
        # 財務健全性指標
        health = result['financial_health_ratios']
        output.append("【財務健全性指標】")
        output.append(f"  自己資本比率: {health['equity_ratio']:.1f}% ({health['equity_ratio_rating']})")
        output.append(f"  負債比率: {health['debt_ratio']:.1f}% ({health['debt_ratio_rating']})")
        output.append("")
        
        # キャッシュフロー分析
        cf = result['cash_flow_analysis']
        output.append("【キャッシュフロー分析】")
        output.append(f"  営業CF: {cf['operating_cf']:,.0f}円")
        output.append(f"  投資CF: {cf['investing_cf']:,.0f}円")
        output.append(f"  財務CF: {cf['financing_cf']:,.0f}円")
        output.append(f"  フリーCF: {cf['free_cash_flow']:,.0f}円")
        output.append(f"  パターン: {cf['pattern']}")
        output.append(f"  健全性: {cf['health_status']}")
        output.append("")
        
        # 総合評価
        output.append("【総合評価】")
        output.append(f"  {result['overall_assessment']}")
        output.append("")
        
        # 推奨事項
        output.append("【推奨事項】")
        for i, rec in enumerate(result['recommendations'], 1):
            output.append(f"  {i}. {rec}")
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)
