"""PDF形式のレポート生成ユーティリティ"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class PDFGenerator:
    """PDF形式のレポートを生成"""
    
    def __init__(self):
        """初期化"""
        # 日本語フォントの登録
        self._register_japanese_fonts()
        
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
        # カラーパレット
        self.colors = {
            'primary': HexColor('#0066CC'),
            'secondary': HexColor('#FF9900'),
            'success': HexColor('#4CAF50'),
            'text': HexColor('#212121'),
            'light': HexColor('#F5F5F5')
        }
    
    def _register_japanese_fonts(self):
        """日本語フォントを登録"""
        try:
            # macOSのシステムフォントを使用
            font_paths = [
                '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
                '/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc',
                '/Library/Fonts/Arial Unicode.ttf',
                '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
            ]
            
            # 利用可能なフォントを探す
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('Japanese', font_path))
                        pdfmetrics.registerFont(TTFont('Japanese-Bold', font_path))
                        return
                    except:
                        continue
            
            # フォントが見つからない場合はHelveticaを使用（文字化けする可能性あり）
            print("警告: 日本語フォントが見つかりません。一部の文字が正しく表示されない可能性があります。")
            
        except Exception as e:
            print(f"フォント登録エラー: {str(e)}")
    
    def _setup_styles(self):
        """カスタムスタイルを設定"""
        # タイトルスタイル
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontName='Japanese',
            fontSize=28,
            textColor=HexColor('#0066CC'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # 見出し1
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontName='Japanese-Bold',
            fontSize=20,
            textColor=HexColor('#0066CC'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # 見出し2
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontName='Japanese-Bold',
            fontSize=16,
            textColor=HexColor('#FF9900'),
            spaceAfter=10,
            spaceBefore=10
        ))
        
        # 本文
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontName='Japanese',
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # 箇条書き
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['BodyText'],
            fontName='Japanese',
            fontSize=11,
            leading=14,
            leftIndent=20,
            spaceAfter=6
        ))
    
    def generate_report(
        self,
        project_info: Dict[str, Any],
        agent_results: List[Dict[str, Any]],
        output_path: str,
        markdown_report: Optional[str] = None
    ) -> str:
        """
        PDFレポートを生成
        
        Args:
            project_info: プロジェクト情報
            agent_results: 各エージェントの分析結果
            output_path: 出力ファイルパス
            markdown_report: マークダウンレポート（指定された場合はこれを使用）
        
        Returns:
            生成されたファイルパス
        """
        # ドキュメント作成
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # コンテンツを構築
        story = []
        
        if markdown_report:
            # マークダウンレポートからPDFを生成
            story.extend(self._create_from_markdown(markdown_report, project_info))
        else:
            # 従来の方法でPDFを生成
            # タイトルページ
            story.extend(self._create_title_page(project_info))
            story.append(PageBreak())
            
            # エグゼクティブサマリー
            story.extend(self._create_executive_summary(agent_results))
            story.append(PageBreak())
            
            # 各分析結果
            for result in agent_results:
                if result.get('status') == 'success':
                    story.extend(self._create_analysis_section(result))
                    story.append(PageBreak())
            
            # 推奨事項
            story.extend(self._create_recommendations_section(agent_results))
            story.append(PageBreak())
            
            # アクションプラン
            story.extend(self._create_action_plan_section())
        
        # PDF生成
        doc.build(story)
        return output_path
        
        # コンテンツを構築
        story = []
        
        # タイトルページ
        story.extend(self._create_title_page(project_info))
        story.append(PageBreak())
        
        # エグゼクティブサマリー
        story.extend(self._create_executive_summary(agent_results))
        story.append(PageBreak())
        
        # 各分析結果
        for result in agent_results:
            if result.get('status') == 'success':
                story.extend(self._create_analysis_section(result))
                story.append(PageBreak())
        
        # 推奨事項
        story.extend(self._create_recommendations_section(agent_results))
        story.append(PageBreak())
        
        # アクションプラン
        story.extend(self._create_action_plan_section())
        
        # PDF生成
        doc.build(story)
        return output_path
    
    def _create_title_page(self, project_info: Dict[str, Any]) -> List:
        """タイトルページを作成"""
        elements = []
        
        # 空白
        elements.append(Spacer(1, 2*inch))
        
        # メインタイトル
        title = Paragraph(
            "戦略コンサルティング<br/>統合レポート",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # プロジェクト情報
        info_data = [
            ['クライアント:', project_info.get('client_name', 'N/A')],
            ['業界:', project_info.get('industry', 'N/A')],
            ['課題:', project_info.get('challenge', 'N/A')],
            ['分析日時:', datetime.now().strftime('%Y年%m月%d日')]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Japanese'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colors['primary']),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(info_table)
        
        return elements
    
    def _create_executive_summary(self, agent_results: List[Dict[str, Any]]) -> List:
        """エグゼクティブサマリーを作成"""
        elements = []
        
        # セクションタイトル
        elements.append(Paragraph("エグゼクティブサマリー", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        successful_analyses = [r for r in agent_results if r.get('status') == 'success']
        
        intro_text = f"本レポートでは、{len(successful_analyses)}つの観点から包括的な分析を実施しました。"
        elements.append(Paragraph(intro_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        # 各分析のサマリー
        for result in successful_analyses:
            analysis_type = result.get('analysis_type', 'unknown')
            
            if analysis_type == 'market':
                elements.append(Paragraph("📊 市場分析", self.styles['CustomHeading2']))
                market_result = result.get('result', {})
                
                summary_items = [
                    f"• 市場魅力度: <b>{market_result.get('market_attractiveness', 'N/A')}</b>",
                    f"• 市場規模: {market_result.get('market_size', 0):,.0f}円",
                    f"• 成長率: {market_result.get('growth_rate', 0)}%"
                ]
                
            elif analysis_type == 'financial':
                elements.append(Paragraph("💰 財務分析", self.styles['CustomHeading2']))
                financial_result = result.get('result', {})
                prof = financial_result.get('profitability_ratios', {})
                
                summary_items = [
                    f"• 総合評価: <b>{financial_result.get('overall_assessment', 'N/A')}</b>",
                    f"• 営業利益率: {prof.get('operating_margin', 0):.1f}% ({prof.get('operating_margin_rating', 'N/A')})"
                ]
                
            elif analysis_type == 'strategy':
                elements.append(Paragraph("🎯 戦略分析", self.styles['CustomHeading2']))
                summary_items = [
                    "• 複数の戦略フレームワーク（3C、SWOT、5Forces等）を用いた包括的分析を実施"
                ]
            
            else:
                continue
            
            for item in summary_items:
                elements.append(Paragraph(item, self.styles['CustomBullet']))
            
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_analysis_section(self, result: Dict[str, Any]) -> List:
        """分析セクションを作成"""
        elements = []
        
        analysis_type = result.get('analysis_type', 'unknown')
        
        # セクションタイトル
        if analysis_type == 'market':
            title = "市場分析結果"
        elif analysis_type == 'financial':
            title = "財務分析結果"
        elif analysis_type == 'strategy':
            title = "戦略分析結果"
        else:
            title = "分析結果"
        
        elements.append(Paragraph(title, self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # フォーマット済み出力を段落に変換
        formatted_output = result.get('formatted_output', '')
        
        # 簡略化のため、最初の1000文字程度を表示
        summary_text = formatted_output[:1000] + "..." if len(formatted_output) > 1000 else formatted_output
        
        # テキストを段落に分割
        for line in summary_text.split('\n'):
            if line.strip():
                # 見出しの検出
                if line.startswith('【') or line.startswith('##'):
                    elements.append(Paragraph(line, self.styles['CustomHeading2']))
                elif line.strip().startswith('-') or line.strip().startswith('•'):
                    elements.append(Paragraph(line, self.styles['CustomBullet']))
                else:
                    elements.append(Paragraph(line, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        note = Paragraph(
            "<i>詳細な分析結果はマークダウンレポートをご参照ください。</i>",
            self.styles['CustomBody']
        )
        elements.append(note)
        
        return elements
    
    def _create_recommendations_section(self, agent_results: List[Dict[str, Any]]) -> List:
        """推奨事項セクションを作成"""
        elements = []
        
        elements.append(Paragraph("統合的な推奨事項", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        intro = "各分析から得られた推奨事項を統合し、優先順位をつけて提示します。"
        elements.append(Paragraph(intro, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        all_recommendations = []
        
        # 各エージェントからの推奨事項を収集
        for result in agent_results:
            if result.get('status') != 'success':
                continue
            
            analysis_result = result.get('result', {})
            
            if result.get('analysis_type') == 'market':
                recs = analysis_result.get('recommendations', [])
                all_recommendations.extend([('市場', rec) for rec in recs])
            elif result.get('analysis_type') == 'financial':
                recs = analysis_result.get('recommendations', [])
                all_recommendations.extend([('財務', rec) for rec in recs])
        
        # 推奨事項を表示
        for i, (category, rec) in enumerate(all_recommendations, 1):
            rec_text = f"{i}. <b>[{category}]</b> {rec}"
            elements.append(Paragraph(rec_text, self.styles['CustomBullet']))
        
        return elements
    
    def _create_action_plan_section(self) -> List:
        """アクションプランセクションを作成"""
        elements = []
        
        elements.append(Paragraph("アクションプラン", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        intro = "推奨事項を実行するための具体的なアクションプランを以下に示します。"
        elements.append(Paragraph(intro, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        action_plans = [
            ("短期（1-3ヶ月）", [
                "データ収集と詳細分析の実施",
                "優先度の高い施策の計画立案",
                "ステークホルダーとの合意形成"
            ]),
            ("中期（3-6ヶ月）", [
                "優先施策の実行開始",
                "KPIの設定とモニタリング体制の構築",
                "中間評価と軌道修正"
            ]),
            ("長期（6-12ヶ月）", [
                "施策の効果測定と評価",
                "次フェーズの戦略立案",
                "継続的改善サイクルの確立"
            ])
        ]
        
        for period, actions in action_plans:
            elements.append(Paragraph(period, self.styles['CustomHeading2']))
            
            for action in actions:
                elements.append(Paragraph(f"• {action}", self.styles['CustomBullet']))
            
            elements.append(Spacer(1, 0.15*inch))
        
        # フッター
        elements.append(Spacer(1, 0.3*inch))
        footer = Paragraph(
            "<i>本レポートはマルチエージェントシステムにより自動生成されました</i>",
            self.styles['CustomBody']
        )
        elements.append(footer)
        
        return elements
    
    def _create_from_markdown(self, markdown_text: str, project_info: Dict[str, Any]) -> List:
        """マークダウンテキストからPDF要素を生成"""
        elements = []
        
        # タイトルページを追加
        elements.extend(self._create_title_page(project_info))
        elements.append(PageBreak())
        
        # マークダウンを行ごとに処理
        lines = markdown_text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # 空行をスキップ
            if not line:
                i += 1
                continue
            
            # メインタイトル（# で始まる）をスキップ（タイトルページで表示済み）
            if line.startswith('# '):
                i += 1
                continue
            
            # 区切り線
            if line.startswith('---'):
                elements.append(Spacer(1, 0.2*inch))
                i += 1
                continue
            
            # 見出し1（## で始まる）
            if line.startswith('## '):
                title = line[3:].strip()
                elements.append(Paragraph(title, self.styles['CustomHeading1']))
                elements.append(Spacer(1, 0.15*inch))
                i += 1
                continue
            
            # 見出し2（### で始まる）
            if line.startswith('### '):
                title = line[4:].strip()
                elements.append(Paragraph(title, self.styles['CustomHeading2']))
                elements.append(Spacer(1, 0.1*inch))
                i += 1
                continue
            
            # 箇条書き（- または • で始まる）
            if line.startswith('- ') or line.startswith('• ') or line.startswith('* '):
                bullet_text = line[2:].strip()
                # 太字の処理（**text** を <b>text</b> に変換）
                import re
                bullet_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', bullet_text)
                elements.append(Paragraph(f"• {bullet_text}", self.styles['CustomBullet']))
                i += 1
                continue
            
            # 番号付きリスト
            if len(line) > 2 and line[0].isdigit() and line[1:3] in ['. ', ') ']:
                list_text = line[3:].strip() if line[1] == '.' else line[2:].strip()
                # 太字の処理
                import re
                list_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', list_text)
                # 番号を保持
                prefix = line[:3] if line[1] == '.' else line[:2]
                elements.append(Paragraph(f"{prefix} {list_text}", self.styles['CustomBullet']))
                i += 1
                continue
            
            # 通常のテキスト
            # 太字の処理（**text** を <b>text</b> に変換）
            import re
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
            # イタリックの処理（*text* を <i>text</i> に変換、ただし**は除外）
            text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
            
            elements.append(Paragraph(text, self.styles['CustomBody']))
            i += 1
        
        return elements
