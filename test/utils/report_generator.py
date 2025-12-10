"""統合レポート生成ユーティリティ"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """複数のエージェント結果を統合してレポートを生成"""
    
    def __init__(self):
        """初期化"""
        self.pptx_generator = None
        self.pdf_generator = None

    
    def generate_report(
        self,
        project_info: Dict[str, Any],
        agent_results: List[Dict[str, Any]]
    ) -> str:
        """
        統合レポートを生成
        
        Args:
            project_info: プロジェクト情報
            agent_results: 各エージェントの分析結果
        
        Returns:
            マークダウン形式のレポート
        """
        sections = []
        
        # ヘッダー
        sections.append(self._generate_header(project_info))
        
        # エグゼクティブサマリー
        sections.append(self._generate_executive_summary(agent_results))
        
        # 各エージェントの詳細結果
        for result in agent_results:
            if result.get('status') == 'success':
                sections.append(self._generate_agent_section(result))
        
        # 統合的な推奨事項
        sections.append(self._generate_integrated_recommendations(agent_results))
        
        # アクションプラン
        sections.append(self._generate_action_plan(agent_results))
        
        # フッター
        sections.append(self._generate_footer())
        
        return "\n\n".join(sections)
    
    def export_report(
        self,
        project_info: Dict[str, Any],
        agent_results: List[Dict[str, Any]],
        output_path: str,
        export_format: str = 'markdown'
    ) -> str:
        """
        指定された形式でレポートをエクスポート
        
        Args:
            project_info: プロジェクト情報
            agent_results: 各エージェントの分析結果
            output_path: 出力ファイルパス
            export_format: 出力形式 ('markdown', 'pptx', 'pdf')
        
        Returns:
            生成されたファイルパス
        """
        if export_format == 'markdown':
            # マークダウン形式
            report_content = self.generate_report(project_info, agent_results)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return output_path
        
        elif export_format == 'pptx':
            # PowerPoint形式
            if self.pptx_generator is None:
                from utils.pptx_generator import PPTXGenerator
                self.pptx_generator = PPTXGenerator()
            
            return self.pptx_generator.generate_report(
                project_info, agent_results, output_path
            )
        
        elif export_format == 'pdf':
            # PDF形式（マークダウンレポートを統合）
            if self.pdf_generator is None:
                from utils.pdf_generator import PDFGenerator
                self.pdf_generator = PDFGenerator()
            
            # マークダウンレポートを生成
            markdown_report = self.generate_report(project_info, agent_results)
            
            # マークダウンレポートをPDFに変換
            return self.pdf_generator.generate_report(
                project_info, agent_results, output_path, markdown_report=markdown_report
            )
        
        else:
            raise ValueError(f"Unsupported export format: {export_format}")


    
    def _generate_header(self, project_info: Dict[str, Any]) -> str:
        """ヘッダーを生成"""
        lines = []
        lines.append("# 戦略コンサルティング統合レポート")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## プロジェクト情報")
        lines.append("")
        lines.append(f"- **クライアント**: {project_info.get('client_name', 'N/A')}")
        lines.append(f"- **業界**: {project_info.get('industry', 'N/A')}")
        lines.append(f"- **課題**: {project_info.get('challenge', 'N/A')}")
        lines.append(f"- **分析日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        lines.append("")
        
        return "\n".join(lines)
    
    def _generate_executive_summary(self, agent_results: List[Dict[str, Any]]) -> str:
        """エグゼクティブサマリーを生成"""
        lines = []
        lines.append("## エグゼクティブサマリー")
        lines.append("")
        
        # 実行された分析の概要
        successful_analyses = [
            r for r in agent_results if r.get('status') == 'success'
        ]
        
        if not successful_analyses:
            lines.append("分析を実行できませんでした。")
            return "\n".join(lines)
        
        lines.append(f"本レポートでは、{len(successful_analyses)}つの観点から包括的な分析を実施しました:")
        lines.append("")
        
        for result in successful_analyses:
            analysis_type = result.get('analysis_type', 'unknown')
            agent_name = result.get('agent', 'Unknown Agent')
            
            if analysis_type == 'market':
                lines.append("### 📊 市場分析")
                market_result = result.get('result', {})
                lines.append(f"- 市場魅力度: **{market_result.get('market_attractiveness', 'N/A')}**")
                lines.append(f"- 市場規模: {market_result.get('market_size', 0):,.0f}円")
                lines.append(f"- 成長率: {market_result.get('growth_rate', 0)}%")
                
            elif analysis_type == 'financial':
                lines.append("### 💰 財務分析")
                financial_result = result.get('result', {})
                lines.append(f"- 総合評価: **{financial_result.get('overall_assessment', 'N/A')}**")
                prof = financial_result.get('profitability_ratios', {})
                lines.append(f"- 営業利益率: {prof.get('operating_margin', 0):.1f}% ({prof.get('operating_margin_rating', 'N/A')})")
                
            elif analysis_type == 'strategy':
                lines.append("### 🎯 戦略分析")
                lines.append("- 複数の戦略フレームワーク（3C、SWOT、5Forces等）を用いた包括的分析を実施")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_agent_section(self, result: Dict[str, Any]) -> str:
        """各エージェントのセクションを生成"""
        lines = []
        lines.append("---")
        lines.append("")
        
        # フォーマット済み出力を使用
        formatted_output = result.get('formatted_output', '')
        if formatted_output:
            lines.append(formatted_output)
        
        return "\n".join(lines)
    
    def _generate_integrated_recommendations(self, agent_results: List[Dict[str, Any]]) -> str:
        """統合的な推奨事項を生成"""
        lines = []
        lines.append("---")
        lines.append("")
        lines.append("## 統合的な推奨事項")
        lines.append("")
        
        all_recommendations = []
        
        # 各エージェントからの推奨事項を収集
        for result in agent_results:
            if result.get('status') != 'success':
                continue
            
            analysis_result = result.get('result', {})
            
            # 市場分析の推奨事項
            if result.get('analysis_type') == 'market':
                recs = analysis_result.get('recommendations', [])
                all_recommendations.extend([('市場', rec) for rec in recs])
            
            # 財務分析の推奨事項
            elif result.get('analysis_type') == 'financial':
                recs = analysis_result.get('recommendations', [])
                all_recommendations.extend([('財務', rec) for rec in recs])
        
        if not all_recommendations:
            lines.append("推奨事項を生成できませんでした。")
        else:
            lines.append("各分析から得られた推奨事項を統合し、優先順位をつけて提示します:")
            lines.append("")
            
            for i, (category, rec) in enumerate(all_recommendations, 1):
                lines.append(f"{i}. **[{category}]** {rec}")
        
        lines.append("")
        return "\n".join(lines)
    
    def _generate_action_plan(self, agent_results: List[Dict[str, Any]]) -> str:
        """アクションプランを生成"""
        lines = []
        lines.append("## アクションプラン")
        lines.append("")
        lines.append("推奨事項を実行するための具体的なアクションプランを以下に示します:")
        lines.append("")
        
        lines.append("### 短期（1-3ヶ月）")
        lines.append("- データ収集と詳細分析の実施")
        lines.append("- 優先度の高い施策の計画立案")
        lines.append("- ステークホルダーとの合意形成")
        lines.append("")
        
        lines.append("### 中期（3-6ヶ月）")
        lines.append("- 優先施策の実行開始")
        lines.append("- KPIの設定とモニタリング体制の構築")
        lines.append("- 中間評価と軌道修正")
        lines.append("")
        
        lines.append("### 長期（6-12ヶ月）")
        lines.append("- 施策の効果測定と評価")
        lines.append("- 次フェーズの戦略立案")
        lines.append("- 継続的改善サイクルの確立")
        lines.append("")
        
        return "\n".join(lines)
    
    def _generate_footer(self) -> str:
        """フッターを生成"""
        lines = []
        lines.append("---")
        lines.append("")
        lines.append("*本レポートはマルチエージェントシステムにより自動生成されました*")
        lines.append("")
        
        return "\n".join(lines)
