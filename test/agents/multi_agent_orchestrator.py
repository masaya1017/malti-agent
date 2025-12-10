"""マルチエージェントオーケストレーター"""
import asyncio
from typing import Dict, Any, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from agents.market_agent import MarketAgent
from agents.financial_agent import FinancialAgent
from agents.strategy_analysis_agent import StrategyAnalysisAgent
from utils.report_generator import ReportGenerator


console = Console()


class MultiAgentOrchestrator:
    """複数のエージェントを管理し、協調して分析を実行"""
    
    def __init__(self):
        """初期化"""
        self.market_agent = MarketAgent()
        self.financial_agent = FinancialAgent()
        self.strategy_agent = StrategyAnalysisAgent()
        self.report_generator = ReportGenerator()
    
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
        
        # 統合レポートを生成
        integrated_report = self.report_generator.generate_report(
            project_info={
                'client_name': project_data.get('client_name', 'N/A'),
                'industry': project_data.get('industry', 'N/A'),
                'challenge': project_data.get('challenge', 'N/A')
            },
            agent_results=agent_results
        )
        
        return {
            'agent_results': agent_results,
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
