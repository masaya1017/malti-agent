#!/usr/bin/env python3
"""マルチエージェント分析を実行するスクリプト"""
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from agents.multi_agent_orchestrator import MultiAgentOrchestrator


console = Console()


def main():
    """メイン処理"""
    console.print(Panel.fit(
        "[bold cyan]マルチエージェント統合分析[/bold cyan]",
        title="分析ツール"
    ))
    
    # データファイルを読み込み
    data_file = Path(__file__).parent / 'sample_data_extended.json'
    
    if not data_file.exists():
        console.print(f"[red]エラー: データファイルが見つかりません: {data_file}[/red]")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    console.print(f"[green]✓[/green] データファイルを読み込みました: {data_file.name}\n")
    
    # プロジェクト情報を追加
    project_data = {
        'client_name': 'サンプル企業',
        'industry': 'IT業界',
        'challenge': '市場シェア拡大と収益性向上',
        **data
    }
    
    # マルチエージェント分析を実行
    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.analyze_sync(project_data)
    
    # 統合レポートを表示
    console.print("\n" + "=" * 80)
    console.print("[bold green]統合レポート[/bold green]")
    console.print("=" * 80 + "\n")
    console.print(result['integrated_report'])
    
    # レポートをファイルに保存
    output_file = Path(__file__).parent / 'multi_agent_report.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result['integrated_report'])
    
    console.print(f"\n[green]✓[/green] レポートを保存しました: {output_file}")
    
    # サマリーを表示
    summary = result['summary']
    console.print(f"\n[bold]分析サマリー[/bold]")
    console.print(f"  総エージェント数: {summary['total_agents']}")
    console.print(f"  成功: {summary['successful']}")
    console.print(f"  スキップ: {summary['skipped']}")
    console.print(f"  失敗: {summary['failed']}")
    console.print(f"  成功率: {summary['success_rate']:.1f}%")
    
    console.print("\n[green]✓ すべての分析が完了しました[/green]")


if __name__ == '__main__':
    main()
