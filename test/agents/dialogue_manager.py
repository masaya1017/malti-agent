"""エージェント間対話マネージャー"""
import asyncio
from typing import Dict, Any, List, Optional
from rich.console import Console

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from config.settings import settings


console = Console()


class DialogueManager:
    """エージェント間の対話を管理し、議論・合意形成を促進"""
    
    def __init__(self):
        """初期化"""
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.7,  # 対話では少し創造性を高める
            api_key=settings.openai_api_key
        )
        self.dialogue_history: List[Dict[str, Any]] = []
    
    async def facilitate_dialogue(
        self,
        agent_results: List[Dict[str, Any]],
        project_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        エージェント間の対話を促進
        
        Args:
            agent_results: 各エージェントの分析結果
            project_info: プロジェクト情報
        
        Returns:
            対話結果（合意事項、議論のサマリー等）
        """
        console.print("\n[bold cyan]エージェント間対話を開始します...[/bold cyan]\n")
        
        # 成功した分析結果のみを対象
        successful_results = [
            r for r in agent_results if r.get('status') == 'success'
        ]
        
        if len(successful_results) < 2:
            return {
                'dialogue_occurred': False,
                'message': '対話に必要な分析結果が不足しています'
            }
        
        # 対話のフェーズ
        phases = [
            self._phase1_share_insights(successful_results, project_info),
            self._phase2_identify_conflicts(successful_results, project_info),
            self._phase3_build_consensus(successful_results, project_info)
        ]
        
        # 各フェーズを順次実行
        phase_results = []
        for phase_coro in phases:
            result = await phase_coro
            phase_results.append(result)
            self.dialogue_history.append(result)
        
        # 対話結果を統合
        dialogue_summary = self._synthesize_dialogue(phase_results)
        
        console.print("[green]✓ エージェント間対話が完了しました[/green]\n")
        
        return {
            'dialogue_occurred': True,
            'phases': phase_results,
            'summary': dialogue_summary,
            'consensus_items': dialogue_summary.get('consensus_items', []),
            'action_items': dialogue_summary.get('action_items', [])
        }
    
    async def _phase1_share_insights(
        self,
        results: List[Dict[str, Any]],
        project_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        フェーズ1: 洞察の共有
        各エージェントの主要な発見を共有
        """
        console.print("[yellow]フェーズ1: 洞察の共有[/yellow]")
        
        # 各エージェントの主要な洞察を抽出
        insights = []
        for result in results:
            agent_name = result.get('agent', 'Unknown')
            analysis_type = result.get('analysis_type', 'unknown')
            
            # 主要な洞察を要約
            insight = self._extract_key_insights(result)
            insights.append({
                'agent': agent_name,
                'type': analysis_type,
                'insight': insight
            })
        
        # LLMで洞察を統合
        prompt = self._create_insight_sharing_prompt(insights, project_info)
        messages = [
            SystemMessage(content="あなたは戦略コンサルタントとして、複数の分析結果を統合する役割を担っています。"),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            'phase': 'insight_sharing',
            'insights': insights,
            'synthesis': response.content
        }
    
    async def _phase2_identify_conflicts(
        self,
        results: List[Dict[str, Any]],
        project_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        フェーズ2: 矛盾点の特定
        異なる分析結果間の矛盾や不一致を特定
        """
        console.print("[yellow]フェーズ2: 矛盾点の特定[/yellow]")
        
        # 矛盾の可能性がある領域を特定
        prompt = self._create_conflict_identification_prompt(results, project_info)
        messages = [
            SystemMessage(content="あなたは批判的思考を持つアナリストとして、分析結果間の矛盾や不一致を特定します。"),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            'phase': 'conflict_identification',
            'conflicts': response.content
        }
    
    async def _phase3_build_consensus(
        self,
        results: List[Dict[str, Any]],
        project_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        フェーズ3: 合意形成
        矛盾を解決し、統一された戦略的方向性を導出
        """
        console.print("[yellow]フェーズ3: 合意形成[/yellow]")
        
        # 前のフェーズの結果を参照
        previous_insights = self.dialogue_history[-2] if len(self.dialogue_history) >= 2 else None
        previous_conflicts = self.dialogue_history[-1] if len(self.dialogue_history) >= 1 else None
        
        prompt = self._create_consensus_building_prompt(
            results, project_info, previous_insights, previous_conflicts
        )
        messages = [
            SystemMessage(content="あなたは経験豊富な戦略コンサルタントとして、異なる視点を統合し、実行可能な合意事項を導出します。"),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            'phase': 'consensus_building',
            'consensus': response.content
        }
    
    def _extract_key_insights(self, result: Dict[str, Any]) -> str:
        """分析結果から主要な洞察を抽出"""
        analysis_type = result.get('analysis_type', 'unknown')
        analysis_result = result.get('result', {})
        
        if analysis_type == 'market':
            return f"市場魅力度: {analysis_result.get('market_attractiveness', 'N/A')}, " \
                   f"成長率: {analysis_result.get('growth_rate', 0)}%, " \
                   f"推奨: {', '.join(analysis_result.get('recommendations', [])[:2])}"
        
        elif analysis_type == 'financial':
            return f"総合評価: {analysis_result.get('overall_assessment', 'N/A')}, " \
                   f"営業利益率: {analysis_result.get('profitability_ratios', {}).get('operating_margin', 0):.1f}%, " \
                   f"推奨: {', '.join(analysis_result.get('recommendations', [])[:2])}"
        
        elif analysis_type == 'strategy':
            # 戦略分析の場合は出力から抽出
            output = result.get('result', {}).get('output', '')
            return output[:200] + "..." if len(output) > 200 else output
        
        return "詳細な分析結果を参照してください"
    
    def _create_insight_sharing_prompt(
        self,
        insights: List[Dict[str, Any]],
        project_info: Dict[str, Any]
    ) -> str:
        """洞察共有フェーズのプロンプトを作成"""
        prompt = f"""
# プロジェクト情報
- クライアント: {project_info.get('client_name', 'N/A')}
- 業界: {project_info.get('industry', 'N/A')}
- 課題: {project_info.get('challenge', 'N/A')}

# 各エージェントの主要な洞察

"""
        for insight in insights:
            prompt += f"## {insight['agent']} ({insight['type']})\n"
            prompt += f"{insight['insight']}\n\n"
        
        prompt += """
# タスク
上記の各エージェントの洞察を統合し、以下を提供してください：
1. 共通するテーマや発見
2. 相互に補完する洞察
3. 統合的な視点から見た主要な発見

簡潔に、箇条書きで回答してください。
"""
        return prompt
    
    def _create_conflict_identification_prompt(
        self,
        results: List[Dict[str, Any]],
        project_info: Dict[str, Any]
    ) -> str:
        """矛盾特定フェーズのプロンプトを作成"""
        prompt = f"""
# プロジェクト情報
- クライアント: {project_info.get('client_name', 'N/A')}
- 業界: {project_info.get('industry', 'N/A')}
- 課題: {project_info.get('challenge', 'N/A')}

# 分析結果の要約

"""
        for result in results:
            agent_name = result.get('agent', 'Unknown')
            recommendations = result.get('result', {}).get('recommendations', [])
            prompt += f"## {agent_name}\n"
            prompt += f"推奨事項: {', '.join(recommendations[:3])}\n\n"
        
        prompt += """
# タスク
上記の分析結果を比較し、以下を特定してください：
1. 矛盾する推奨事項や見解
2. 優先順位が異なる領域
3. 追加の検討が必要な不確実性

矛盾がない場合は「重大な矛盾は見られません」と回答してください。
簡潔に、箇条書きで回答してください。
"""
        return prompt
    
    def _create_consensus_building_prompt(
        self,
        results: List[Dict[str, Any]],
        project_info: Dict[str, Any],
        insights: Optional[Dict[str, Any]],
        conflicts: Optional[Dict[str, Any]]
    ) -> str:
        """合意形成フェーズのプロンプトを作成"""
        prompt = f"""
# プロジェクト情報
- クライアント: {project_info.get('client_name', 'N/A')}
- 業界: {project_info.get('industry', 'N/A')}
- 課題: {project_info.get('challenge', 'N/A')}

# 共有された洞察
{insights.get('synthesis', '') if insights else 'N/A'}

# 特定された矛盾
{conflicts.get('conflicts', '') if conflicts else 'N/A'}

# タスク
上記の情報を基に、以下を提供してください：

1. **合意事項**: 全てのエージェントが支持する戦略的方向性（3-5項目）
2. **優先アクション**: 最も重要な実行項目（3項目）
3. **リスクと緩和策**: 主要なリスクとその対応策（2-3項目）

実行可能で具体的な内容にしてください。
"""
        return prompt
    
    def _synthesize_dialogue(self, phase_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """対話結果を統合"""
        consensus_phase = phase_results[2] if len(phase_results) > 2 else {}
        consensus_text = consensus_phase.get('consensus', '')
        
        # 合意事項とアクション項目を抽出（簡易版）
        consensus_items = []
        action_items = []
        
        # テキストから項目を抽出（実際にはより洗練された解析が必要）
        lines = consensus_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if '合意事項' in line or 'consensus' in line.lower():
                current_section = 'consensus'
            elif '優先アクション' in line or 'action' in line.lower():
                current_section = 'action'
            elif line.startswith('-') or line.startswith('•') or (line and line[0].isdigit()):
                if current_section == 'consensus':
                    consensus_items.append(line.lstrip('-•0123456789. '))
                elif current_section == 'action':
                    action_items.append(line.lstrip('-•0123456789. '))
        
        return {
            'full_dialogue': consensus_text,
            'consensus_items': consensus_items[:5],  # 最大5項目
            'action_items': action_items[:3],  # 最大3項目
            'phases_completed': len(phase_results)
        }
    
    def format_dialogue_report(self, dialogue_result: Dict[str, Any]) -> str:
        """対話結果をレポート形式にフォーマット"""
        if not dialogue_result.get('dialogue_occurred'):
            return ""
        
        lines = []
        lines.append("## エージェント間対話の結果")
        lines.append("")
        lines.append("複数のエージェントが分析結果について議論し、以下の合意に達しました。")
        lines.append("")
        
        # 合意事項
        consensus_items = dialogue_result.get('consensus_items', [])
        if consensus_items:
            lines.append("### 合意事項")
            lines.append("")
            for i, item in enumerate(consensus_items, 1):
                if item:  # 空でない項目のみ
                    lines.append(f"{i}. {item}")
            lines.append("")
        
        # アクション項目
        action_items = dialogue_result.get('action_items', [])
        if action_items:
            lines.append("### 優先アクション")
            lines.append("")
            for i, item in enumerate(action_items, 1):
                if item:  # 空でない項目のみ
                    lines.append(f"{i}. {item}")
            lines.append("")
        
        # 詳細な対話内容
        summary = dialogue_result.get('summary', {})
        full_dialogue = summary.get('full_dialogue', '')
        if full_dialogue:
            lines.append("### 詳細な議論内容")
            lines.append("")
            lines.append(full_dialogue)
            lines.append("")
        
        return "\n".join(lines)
