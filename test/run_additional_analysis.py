#!/usr/bin/env python3
"""市場分析と財務分析を実行するスクリプト"""
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from frameworks.market_analysis import MarketAnalysis
from frameworks.financial_analysis import FinancialAnalysis


console = Console()


def run_market_analysis(data: dict):
    """市場分析を実行"""
    console.print("\n[bold cyan]市場分析を実行中...[/bold cyan]\n")
    
    market_data = data.get('market_analysis_data', {})
    
    analyzer = MarketAnalysis()
    result = analyzer.analyze(
        market_size=market_data.get('market_size', 0),
        growth_rate=market_data.get('growth_rate', 0),
        market_segments=market_data.get('market_segments', []),
        market_trends=market_data.get('market_trends', []),
        customer_segments=market_data.get('customer_segments', []),
        market_share_data=market_data.get('market_share_data', {})
    )
    
    formatted_result = analyzer.format_result(result)
    console.print(formatted_result)
    
    return result


def run_financial_analysis(data: dict):
    """財務分析を実行"""
    console.print("\n[bold cyan]財務分析を実行中...[/bold cyan]\n")
    
    financial_data = data.get('financial_data', {})
    
    analyzer = FinancialAnalysis()
    result = analyzer.analyze(
        revenue=financial_data.get('revenue', 0),
        cost_of_sales=financial_data.get('cost_of_sales', 0),
        operating_expenses=financial_data.get('operating_expenses', 0),
        assets=financial_data.get('assets', 0),
        liabilities=financial_data.get('liabilities', 0),
        equity=financial_data.get('equity', 0),
        cash_flow_operating=financial_data.get('cash_flow_operating', 0),
        cash_flow_investing=financial_data.get('cash_flow_investing', 0),
        cash_flow_financing=financial_data.get('cash_flow_financing', 0)
    )
    
    formatted_result = analyzer.format_result(result)
    console.print(formatted_result)
    
    return result


def main():
    """メイン処理"""
    console.print(Panel.fit(
        "[bold cyan]市場分析・財務分析エージェント[/bold cyan]",
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
    
    # 市場分析を実行
    market_result = run_market_analysis(data)
    
    # 財務分析を実行
    financial_result = run_financial_analysis(data)
    
    console.print("\n[green]✓ すべての分析が完了しました[/green]")


if __name__ == '__main__':
    main()
