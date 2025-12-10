"""戦略エージェント"""
import json
from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import StructuredTool

from frameworks.three_c_analysis import ThreeCAnalysis
from frameworks.swot_analysis import SWOTAnalysis
from frameworks.five_forces import FiveForcesAnalysis
from frameworks.pest_analysis import PESTAnalysis
from frameworks.value_chain import ValueChainAnalysis
from config.settings import settings


class StrategyAgent:
    """戦略立案エージェント"""
    
    def __init__(self):
        """初期化"""
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.openai_temperature,
            max_tokens=settings.openai_max_tokens,
            api_key=settings.openai_api_key
        )
        
        self.system_prompt = """あなたは経験豊富な戦略コンサルタントです。
以下の原則に従って戦略立案を支援してください：

1. イシュードリブン: 本質的な課題を特定する
2. MECE: 漏れなくダブりなく分析する
3. ファクトベース: データに基づいた提案を行う
4. アクショナブル: 実行可能な施策を提示する

使用可能なフレームワーク:
- 3C分析: 顧客(Customer)、競合(Competitor)、自社(Company)の観点から分析
- SWOT分析: 強み、弱み、機会、脅威を分析し、クロスSWOT戦略を導出
- 5Forces分析: 業界構造を分析し、収益性と競争環境を評価
- PEST分析: 政治、経済、社会、技術の観点からマクロ環境を分析
- バリューチェーン分析: 主活動と支援活動を分析し、価値創造ポイントと競争優位性を特定

分析結果は具体的で実行可能な戦略提案にまとめてください。
"""
        
        self.tools = [
            self._create_3c_analysis_tool(),
            self._create_swot_analysis_tool(),
            self._create_5forces_analysis_tool(),
            self._create_pest_analysis_tool(),
            self._create_value_chain_analysis_tool(),
        ]
        
        self.agent = self._create_agent()
    
    def _create_agent(self) -> AgentExecutor:
        """エージェントを作成"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True
        )
    
    def _create_3c_analysis_tool(self) -> StructuredTool:
        """3C分析ツールを作成"""
        
        def execute_3c(
            customer_data: str,
            competitor_data: str,
            company_data: str
        ) -> str:
            """
            3C分析を実行
            
            Args:
                customer_data: 顧客データ（JSON文字列）
                competitor_data: 競合データ（JSON文字列）
                company_data: 自社データ（JSON文字列）
            
            Returns:
                分析結果（文字列）
            """
            try:
                # JSON文字列をパース
                customer = json.loads(customer_data)
                competitor = json.loads(competitor_data)
                company = json.loads(company_data)
                
                # 3C分析を実行
                analyzer = ThreeCAnalysis()
                result = analyzer.analyze(customer, competitor, company)
                
                # 結果を整形
                formatted_result = analyzer.format_result(result)
                
                return formatted_result
            except json.JSONDecodeError as e:
                return f"JSONパースエラー: {str(e)}"
            except Exception as e:
                return f"分析エラー: {str(e)}"
        
        return StructuredTool.from_function(
            func=execute_3c,
            name="execute_3c_analysis",
            description="""3C分析（顧客・競合・自社）を実行して戦略的洞察を得る。
            
引数はすべてJSON文字列形式で渡してください：
- customer_data: {"market_size": 数値, "growth_rate": 数値, "segments": [リスト], "needs": [リスト]}
- competitor_data: {"competitors": [{"name": "企業名", "type": "direct/indirect", "revenue": 数値, "strengths": [リスト]}]}
- company_data: {"core_competencies": [リスト], "value_proposition": "文字列", "market_position": "文字列"}
"""
        )
    
    def _create_swot_analysis_tool(self) -> StructuredTool:
        """SWOT分析ツールを作成"""
        
        def execute_swot(
            strengths: str,
            weaknesses: str,
            opportunities: str,
            threats: str
        ) -> str:
            """
            SWOT分析を実行
            
            Args:
                strengths: 強み（JSON配列文字列）
                weaknesses: 弱み（JSON配列文字列）
                opportunities: 機会（JSON配列文字列）
                threats: 脅威（JSON配列文字列）
            
            Returns:
                分析結果（文字列）
            """
            try:
                # JSON文字列をパース
                s_list = json.loads(strengths)
                w_list = json.loads(weaknesses)
                o_list = json.loads(opportunities)
                t_list = json.loads(threats)
                
                # SWOT分析を実行
                analyzer = SWOTAnalysis()
                result = analyzer.analyze(s_list, w_list, o_list, t_list)
                
                # 結果を整形
                formatted_result = analyzer.format_result(result)
                
                return formatted_result
            except json.JSONDecodeError as e:
                return f"JSONパースエラー: {str(e)}"
            except Exception as e:
                return f"分析エラー: {str(e)}"
        
        return StructuredTool.from_function(
            func=execute_swot,
            name="execute_swot_analysis",
            description="""SWOT分析を実行してクロスSWOT戦略を導出する。

引数はすべてJSON配列文字列形式で渡してください：
- strengths: ["強み1", "強み2", ...]
- weaknesses: ["弱み1", "弱み2", ...]
- opportunities: ["機会1", "機会2", ...]
- threats: ["脅威1", "脅威2", ...]
"""
        )
    
    def _create_5forces_analysis_tool(self) -> StructuredTool:
        """5Forces分析ツールを作成"""
        
        def execute_5forces(
            new_entrants_data: str,
            substitutes_data: str,
            buyer_data: str,
            supplier_data: str,
            rivalry_data: str
        ) -> str:
            """
            5Forces分析を実行
            
            Args:
                new_entrants_data: 新規参入データ（JSON文字列）
                substitutes_data: 代替品データ（JSON文字列）
                buyer_data: 買い手データ（JSON文字列）
                supplier_data: 売り手データ（JSON文字列）
                rivalry_data: 競争データ（JSON文字列）
            
            Returns:
                分析結果（文字列）
            """
            try:
                # JSON文字列をパース
                new_entrants = json.loads(new_entrants_data)
                substitutes = json.loads(substitutes_data)
                buyer = json.loads(buyer_data)
                supplier = json.loads(supplier_data)
                rivalry = json.loads(rivalry_data)
                
                # 5Forces分析を実行
                analyzer = FiveForcesAnalysis()
                result = analyzer.analyze(
                    new_entrants, substitutes, buyer, supplier, rivalry
                )
                
                # 結果を整形
                formatted_result = analyzer.format_result(result)
                
                return formatted_result
            except json.JSONDecodeError as e:
                return f"JSONパースエラー: {str(e)}"
            except Exception as e:
                return f"分析エラー: {str(e)}"
        
        return StructuredTool.from_function(
            func=execute_5forces,
            name="execute_5forces_analysis",
            description="""5Forces分析を実行して業界の魅力度を評価する。

引数はすべてJSON文字列形式で渡してください：
- new_entrants_data: {"capital_requirements": "high/low", "economies_of_scale": "important/not", ...}
- substitutes_data: {"substitute_availability": "many/few", "switching_cost": "high/low", ...}
- buyer_data: {"buyer_concentration": "high/low", "switching_cost": "high/low", ...}
- supplier_data: {"supplier_concentration": "high/low", "switching_cost": "high/low", ...}
- rivalry_data: {"number_of_competitors": "many/few", "industry_growth": "fast/slow", ...}
"""
        )
    
    def _create_pest_analysis_tool(self) -> StructuredTool:
        """PEST分析ツールを作成"""
        
        def execute_pest(
            political_data: str,
            economic_data: str,
            social_data: str,
            technological_data: str
        ) -> str:
            """
            PEST分析を実行
            
            Args:
                political_data: 政治的要因データ（JSON配列文字列）
                economic_data: 経済的要因データ（JSON配列文字列）
                social_data: 社会的要因データ（JSON配列文字列）
                technological_data: 技術的要因データ（JSON配列文字列）
            
            Returns:
                分析結果（文字列）
            """
            try:
                # JSON文字列をパース
                political = json.loads(political_data)
                economic = json.loads(economic_data)
                social = json.loads(social_data)
                technological = json.loads(technological_data)
                
                # PEST分析を実行
                analyzer = PESTAnalysis()
                result = analyzer.analyze(political, economic, social, technological)
                
                # 結果を整形
                formatted_result = analyzer.format_result(result)
                
                return formatted_result
            except json.JSONDecodeError as e:
                return f"JSONパースエラー: {str(e)}"
            except Exception as e:
                return f"分析エラー: {str(e)}"
        
        return StructuredTool.from_function(
            func=execute_pest,
            name="execute_pest_analysis",
            description="""PEST分析を実行してマクロ環境を分析する。

引数はすべてJSON配列文字列形式で渡してください：
- political_data: [{"factor": "要因名", "description": "説明", "impact": "プラス/マイナス/中立", "timeframe": "short-term/medium-term/long-term"}]
- economic_data: [{"factor": "要因名", "description": "説明", "impact": "プラス/マイナス/中立", "timeframe": "short-term/medium-term/long-term"}]
- social_data: [{"factor": "要因名", "description": "説明", "impact": "プラス/マイナス/中立", "timeframe": "short-term/medium-term/long-term"}]
- technological_data: [{"factor": "要因名", "description": "説明", "impact": "プラス/マイナス/中立", "timeframe": "short-term/medium-term/long-term"}]
"""
        )
    
    def _create_value_chain_analysis_tool(self) -> StructuredTool:
        """バリューチェーン分析ツールを作成"""
        
        def execute_value_chain(
            primary_activities_data: str,
            support_activities_data: str,
            cost_data: str = "{}"
        ) -> str:
            """
            バリューチェーン分析を実行
            
            Args:
                primary_activities_data: 主活動データ（JSON文字列）
                support_activities_data: 支援活動データ（JSON文字列）
                cost_data: コストデータ（JSON文字列、オプション）
            
            Returns:
                分析結果（文字列）
            """
            try:
                # JSON文字列をパース
                primary_activities = json.loads(primary_activities_data)
                support_activities = json.loads(support_activities_data)
                cost = json.loads(cost_data) if cost_data else {}
                
                # バリューチェーン分析を実行
                analyzer = ValueChainAnalysis()
                result = analyzer.analyze(primary_activities, support_activities, cost)
                
                # 結果を整形
                formatted_result = analyzer.format_result(result)
                
                return formatted_result
            except json.JSONDecodeError as e:
                return f"JSONパースエラー: {str(e)}"
            except Exception as e:
                return f"分析エラー: {str(e)}"
        
        return StructuredTool.from_function(
            func=execute_value_chain,
            name="execute_value_chain_analysis",
            description="""バリューチェーン分析を実行して価値創造ポイントと競争優位性を特定する。

引数はすべてJSON文字列形式で渡してください：
- primary_activities_data: {"inbound_logistics": {"description": "...", "value_added": "..."}, "operations": {...}, "outbound_logistics": {...}, "marketing_sales": {...}, "service": {...}}
- support_activities_data: {"infrastructure": {"description": "...", "value_added": "..."}, "hrm": {...}, "technology": {...}, "procurement": {...}}
- cost_data: {"inbound_logistics_cost": 数値, "operations_cost": 数値, ...} (オプション)
"""
        )
    
    async def analyze(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        戦略分析を実行
        
        Args:
            project_data: プロジェクトデータ
                - client_name: クライアント名
                - industry: 業界
                - challenge: 課題
                - customer_data: 顧客データ（オプション）
                - competitor_data: 競合データ（オプション）
                - company_data: 自社データ（オプション）
        
        Returns:
            分析結果
        """
        # 入力テキストを構築
        input_text = f"""
以下のプロジェクトについて戦略分析を行ってください。

【基本情報】
クライアント: {project_data.get('client_name', '不明')}
業界: {project_data.get('industry', '不明')}
課題: {project_data.get('challenge', '不明')}
"""
        
        # データが提供されている場合は追加
        if 'customer_data' in project_data:
            input_text += f"\n【顧客データ】\n{json.dumps(project_data['customer_data'], ensure_ascii=False, indent=2)}"
        
        if 'competitor_data' in project_data:
            input_text += f"\n【競合データ】\n{json.dumps(project_data['competitor_data'], ensure_ascii=False, indent=2)}"
        
        if 'company_data' in project_data:
            input_text += f"\n【自社データ】\n{json.dumps(project_data['company_data'], ensure_ascii=False, indent=2)}"
        
        input_text += """

【分析手順】
1. 提供されたデータを使って適切なフレームワーク（3C、SWOT、5Forces、PEST、バリューチェーン）を実行してください
2. 分析結果から戦略的洞察を導出してください
3. 具体的で実行可能な戦略提案をまとめてください
"""
        
        # エージェントを実行
        result = await self.agent.ainvoke({"input": input_text})
        
        return result
    
    def analyze_sync(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        戦略分析を実行（同期版）
        
        Args:
            project_data: プロジェクトデータ
        
        Returns:
            分析結果
        """
        # 入力テキストを構築
        input_text = f"""
以下のプロジェクトについて戦略分析を行ってください。

【基本情報】
クライアント: {project_data.get('client_name', '不明')}
業界: {project_data.get('industry', '不明')}
課題: {project_data.get('challenge', '不明')}
"""
        
        # データが提供されている場合は追加
        if 'customer_data' in project_data:
            input_text += f"\n【顧客データ】\n{json.dumps(project_data['customer_data'], ensure_ascii=False, indent=2)}"
        
        if 'competitor_data' in project_data:
            input_text += f"\n【競合データ】\n{json.dumps(project_data['competitor_data'], ensure_ascii=False, indent=2)}"
        
        if 'company_data' in project_data:
            input_text += f"\n【自社データ】\n{json.dumps(project_data['company_data'], ensure_ascii=False, indent=2)}"
        
        input_text += """

【分析手順】
1. 提供されたデータを使って適切なフレームワーク（3C、SWOT、5Forces、PEST、バリューチェーン）を実行してください
2. 分析結果から戦略的洞察を導出してください
3. 具体的で実行可能な戦略提案をまとめてください
"""
        
        # エージェントを実行
        result = self.agent.invoke({"input": input_text})
        
        return result
