#!/usr/bin/env python3
"""戦略コンサルティングエージェント CLI"""
import asyncio
import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from agents.strategy_agent import StrategyAgent
from agents.multi_agent_orchestrator import MultiAgentOrchestrator
from config.settings import settings


console = Console()


@click.group()
def cli():
    """戦略コンサルティングエージェント"""
    pass


@cli.command()
@click.option('--client', '-c', required=True, help='クライアント名')
@click.option('--industry', '-i', required=True, help='業界')
@click.option('--challenge', '-ch', required=True, help='課題')
@click.option('--data-file', '-f', type=click.Path(exists=True), help='データファイル（JSON）')
@click.option('--export', '-e', type=click.Choice(['pdf', 'pptx', 'all'], case_sensitive=False), help='レポート出力形式')
@click.option('--output', '-o', type=click.Path(), help='出力ファイル名（拡張子なし）')
def analyze(client: str, industry: str, challenge: str, data_file: Optional[str], export: Optional[str], output: Optional[str]):
    """戦略分析を実行"""
    
    console.print(Panel.fit(
        f"[bold cyan]戦略コンサルティングエージェント[/bold cyan]\n"
        f"クライアント: {client}\n"
        f"業界: {industry}\n"
        f"課題: {challenge}",
        title="プロジェクト情報"
    ))
    
    # プロジェクトデータを構築
    project_data = {
        'client_name': client,
        'industry': industry,
        'challenge': challenge
    }
    
    # データファイルがある場合は読み込み
    if data_file:
        with open(data_file, 'r', encoding='utf-8') as f:
            additional_data = json.load(f)
            project_data.update(additional_data)
        console.print(f"[green]✓[/green] データファイルを読み込みました: {data_file}")
    
    # エージェントを初期化
    console.print("\n[yellow]エージェントを初期化中...[/yellow]")
    agent = StrategyAgent()
    
    # 分析を実行
    console.print("[yellow]戦略分析を実行中...[/yellow]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("分析中...", total=None)
        
        try:
            result = agent.analyze_sync(project_data)
            progress.update(task, completed=True)
        except Exception as e:
            console.print(f"[red]エラーが発生しました: {str(e)}[/red]")
            return
    
    # 結果を表示
    console.print("\n" + "=" * 80)
    console.print("[bold green]分析結果[/bold green]")
    console.print("=" * 80 + "\n")
    
    # 最終的な出力を表示
    if 'output' in result:
        console.print(result['output'])
    
    # 中間ステップを表示（詳細モード）
    if 'intermediate_steps' in result and result['intermediate_steps']:
        console.print("\n" + "-" * 80)
        console.print("[bold cyan]実行ステップ[/bold cyan]")
        console.print("-" * 80 + "\n")
        
        for i, (action, observation) in enumerate(result['intermediate_steps'], 1):
            console.print(f"[bold]ステップ {i}:[/bold] {action.tool}")
            if observation:
                console.print(f"{observation}\n")
    
    console.print("\n[green]✓ 分析完了[/green]")
    
    # レポート出力（--exportオプションが指定された場合）
    if export:
        from utils.report_generator import ReportGenerator
        from pathlib import Path
        
        console.print(f"\n[yellow]レポートを生成中...[/yellow]")
        
        # 出力ファイル名の決定
        base_name = output if output else f"{client}_analysis"
        base_path = Path.cwd()
        
        # レポートジェネレーターを初期化
        report_generator = ReportGenerator()
        
        # 分析結果を整形
        agent_results = [{
            'agent': 'StrategyAnalysisAgent',
            'status': 'success',
            'analysis_type': 'strategy',
            'result': result,
            'formatted_output': result.get('output', '')
        }]
        
        project_info = {
            'client_name': client,
            'industry': industry,
            'challenge': challenge
        }
        
        # 出力形式に応じてレポート生成
        if export == 'pdf' or export == 'all':
            try:
                pdf_path = base_path / f"{base_name}.pdf"
                report_generator.export_report(
                    project_info=project_info,
                    agent_results=agent_results,
                    output_path=str(pdf_path),
                    export_format='pdf'
                )
                console.print(f"[green]✓[/green] PDFレポートを保存しました: {pdf_path}")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] PDF生成エラー: {str(e)}")
        
        if export == 'pptx' or export == 'all':
            try:
                pptx_path = base_path / f"{base_name}.pptx"
                report_generator.export_report(
                    project_info=project_info,
                    agent_results=agent_results,
                    output_path=str(pptx_path),
                    export_format='pptx'
                )
                console.print(f"[green]✓[/green] PowerPointレポートを保存しました: {pptx_path}")
            except Exception as e:
                console.print(f"[yellow]⚠[/yellow] PowerPoint生成エラー: {str(e)}")


@cli.command()
@click.argument('output_file', type=click.Path())
def create_sample(output_file: str):
    """サンプルデータファイルを作成"""
    
    sample_data = {
        "customer_data": {
            "market_size": 500000000000,
            "growth_rate": 12.5,
            "segments": ["大企業", "中小企業", "スタートアップ"],
            "needs": ["コスト削減", "業務効率化", "DX推進"],
            "buying_behavior": "年次予算で一括購入"
        },
        "competitor_data": {
            "competitors": [
                {
                    "name": "A社",
                    "type": "direct",
                    "revenue": 150000000000,
                    "strengths": ["ブランド力", "営業力"],
                    "cost_advantage": True
                },
                {
                    "name": "B社",
                    "type": "direct",
                    "revenue": 100000000000,
                    "strengths": ["技術力", "カスタマイズ性"],
                    "unique_features": ["AI機能", "クラウド対応"]
                },
                {
                    "name": "C社",
                    "type": "indirect",
                    "revenue": 80000000000,
                    "strengths": ["価格競争力"],
                    "niche_market": "中小企業向け"
                }
            ]
        },
        "company_data": {
            "core_competencies": ["技術力", "顧客サポート", "セキュリティ"],
            "resources": {
                "employees": 500,
                "rd_budget": 5000000000
            },
            "value_proposition": "高セキュリティで使いやすいソリューション",
            "market_position": "業界3位"
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    console.print(f"[green]✓[/green] サンプルデータファイルを作成しました: {output_file}")
    console.print("\n使用方法:")
    console.print(f"  python cli.py analyze -c 'クライアント名' -i '業界' -ch '課題' -f {output_file}")


@cli.command()
def check_config():
    """設定を確認"""
    
    console.print(Panel.fit(
        f"[bold]OpenAI設定[/bold]\n"
        f"モデル: {settings.openai_model}\n"
        f"Temperature: {settings.openai_temperature}\n"
        f"Max Tokens: {settings.openai_max_tokens}\n"
        f"APIキー: {'設定済み' if settings.openai_api_key else '未設定'}",
        title="設定情報"
    ))
    
    if not settings.openai_api_key or settings.openai_api_key == "your-api-key-here":
        console.print("\n[red]警告: OpenAI APIキーが設定されていません[/red]")
        console.print("  .envファイルにOPENAI_API_KEYを設定してください")


if __name__ == '__main__':
    cli()
