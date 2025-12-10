"""マルチエージェントオーケストレーター"""
import asyncio
from typing import Dict, Any, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from agents.market_agent import MarketAgent
from agents.financial_agent import FinancialAgent
from agents.strategy_analysis_agent import StrategyAnalysisAgent
from agents.dialogue_manager import DialogueManager
from utils.report_generator import ReportGenerator


console = Console()


class MultiAgentOrchestrator:
    """複数のエージェントを管理し、協調して分析を実行"""
    
    def __init__(self, enable_dialogue: bool = True):
        """
        初期化
        
        Args:
            enable_dialogue: エージェント間対話を有効にするか
        """
        self.market_agent = MarketAgent()
        self.financial_agent = FinancialAgent()
        self.strategy_agent = StrategyAnalysisAgent()
        self.dialogue_manager = DialogueManager() if enable_dialogue else None
        self.report_generator = ReportGenerator()
        self.enable_dialogue = enable_dialogue

    
    async def analyze(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        マルチエージェント分析を実行
        
        Args:
            project_data: プロジェクトデータ
        
        Returns:
            統合分析結果
        """
        console.print("\n[bold cyan]マルチエージェント分析を開始します...[/bold cyan]\n")
        
        # プログレスバーを表示
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            
            # 各エージェントのタスクを作成
            market_task = progress.add_task(
                "[cyan]市場分析エージェント", total=100
            )
            financial_task = progress.add_task(
                "[green]財務分析エージェント", total=100
            )
            strategy_task = progress.add_task(
                "[yellow]戦略分析エージェント", total=100
            )
            
            # 並列実行
            results = await asyncio.gather(
                self._run_with_progress(
                    self.market_agent.analyze(project_data),
                    progress,
                    market_task
                ),
                self._run_with_progress(
                    self.financial_agent.analyze(project_data),
                    progress,
                    financial_task
                ),
                self._run_with_progress(
                    self.strategy_agent.analyze(project_data),
                    progress,
                    strategy_task
                ),
                return_exceptions=True
            )
        
        # 結果を処理
        agent_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                console.print(f"[red]エージェント {i+1} でエラーが発生しました: {str(result)}[/red]")
                agent_results.append({
                    'agent': f'Agent_{i+1}',
                    'status': 'error',
                    'error': str(result)
                })
            else:
                agent_results.append(result)
        
        # 結果のサマリーを表示
        self._print_summary(agent_results)
        
        # エージェント間対話フェーズ（有効な場合）
        dialogue_result = None
        if self.enable_dialogue and self.dialogue_manager:
            try:
                dialogue_result = await self.dialogue_manager.facilitate_dialogue(
                    agent_results=agent_results,
                    project_info={
                        'client_name': project_data.get('client_name', 'N/A'),
                        'industry': project_data.get('industry', 'N/A'),
                        'challenge': project_data.get('challenge', 'N/A')
                    }
                )
            except Exception as e:
                console.print(f"[yellow]⚠ 対話フェーズでエラーが発生しました: {str(e)}[/yellow]")
                dialogue_result = {
                    'dialogue_occurred': False,
                    'error': str(e)
                }
        
        # 統合レポートを生成
        integrated_report = self.report_generator.generate_report(
            project_info={
                'client_name': project_data.get('client_name', 'N/A'),
                'industry': project_data.get('industry', 'N/A'),
                'challenge': project_data.get('challenge', 'N/A')
            },
            agent_results=agent_results
        )
        
        # 対話結果をレポートに追加
        if dialogue_result and dialogue_result.get('dialogue_occurred'):
            dialogue_section = self.dialogue_manager.format_dialogue_report(dialogue_result)
            if dialogue_section:
                # レポートの推奨事項の前に対話結果を挿入
                parts = integrated_report.split('## 統合的な推奨事項')
                if len(parts) == 2:
                    integrated_report = parts[0] + dialogue_section + "\n\n---\n\n## 統合的な推奨事項" + parts[1]
                else:
                    integrated_report += "\n\n" + dialogue_section
        
        return {
            'agent_results': agent_results,
            'dialogue_result': dialogue_result,
            'integrated_report': integrated_report,
            'summary': self._generate_summary(agent_results)
        }

    
    async def _run_with_progress(
        self,
        coro,
        progress: Progress,
        task_id
    ):
        """
        プログレスバー付きでコルーチンを実行
        
        Args:
            coro: コルーチン
            progress: Progressオブジェクト
            task_id: タスクID
        
        Returns:
            コルーチンの結果
        """
        # 開始
        progress.update(task_id, completed=10)
        
        # 実行
        result = await coro
        
        # 完了
        progress.update(task_id, completed=100)
        
        return result
    
    def _print_summary(self, agent_results: List[Dict[str, Any]]):
        """結果のサマリーを表示"""
        console.print("\n[bold]分析結果サマリー[/bold]")
        console.print("=" * 60)
        
        for result in agent_results:
            agent_name = result.get('agent', 'Unknown')
            status = result.get('status', 'unknown')
            
            if status == 'success':
                console.print(f"✓ {agent_name}: [green]成功[/green]")
            elif status == 'skipped':
                message = result.get('message', 'データなし')
                console.print(f"⊘ {agent_name}: [yellow]スキップ[/yellow] ({message})")
            elif status == 'error':
                error = result.get('error_message', 'Unknown error')
                console.print(f"✗ {agent_name}: [red]エラー[/red] ({error})")
        
        console.print("=" * 60 + "\n")
    
    def _generate_summary(self, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """サマリーを生成"""
        total = len(agent_results)
        successful = sum(1 for r in agent_results if r.get('status') == 'success')
        skipped = sum(1 for r in agent_results if r.get('status') == 'skipped')
        failed = sum(1 for r in agent_results if r.get('status') == 'error')
        
        return {
            'total_agents': total,
            'successful': successful,
            'skipped': skipped,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }
    
    def analyze_sync(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        マルチエージェント分析を実行（同期版）
        
        Args:
            project_data: プロジェクトデータ
        
        Returns:
            統合分析結果
        """
        return asyncio.run(self.analyze(project_data))
