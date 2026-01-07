import os
from typing import Dict, List, Any, Optional
from langchain_core.tools import StructuredTool
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from pydantic import BaseModel, Field
from tools_enhanced import EnhancedCricketAnalysisTools


class PlayerNameInput(BaseModel):
    """Input schema for player name."""
    player_name: str = Field(description="Name of the cricket player")


class EnhancedCricketAgent:
    """
    AI Agent for cricket analytics using LangChain and Claude Sonnet 4.5.
    Provides intelligent analysis of player statistics using ReAct pattern.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the cricket agent with Claude Sonnet 4.5.
        
        Args:
            api_key: Anthropic API key
        """
        self.tools_instance = EnhancedCricketAnalysisTools()
        
        self.llm = ChatAnthropic(
            model="claude-sonnet-4",
            anthropic_api_key=api_key,
            temperature=0
        )
        
        self.tools = self._create_tools()
        
        system_message = """You are an expert cricket analyst AI assistant specializing in IPL statistics.

You have access to THREE comprehensive datasets:
1. Overall Batting Statistics (2021-2024)
2. Line & Length Analysis
3. Wagon Wheel Data

CRITICAL INSTRUCTIONS:
- ALWAYS use tools to fetch data - Never make up statistics
- Only provide insights backed by actual data from the tools
- Include specific numbers and metrics in your analysis
- If data is missing for a player, clearly state "Insufficient data available"
- Provide actionable insights and comparisons
- Be concise but thorough in your analysis

When analyzing a player:
1. Start with overall statistics
2. Dive into line/length weaknesses
3. Examine scoring zones
4. Provide strategic recommendations

Answer the user's question using the tools available."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        self.conversation_history = []
    
    def _create_tools(self) -> List[StructuredTool]:
        """
        Convert tool methods to LangChain StructuredTools.
        
        Returns:
            List of LangChain tools
        """
        tools = [
            StructuredTool.from_function(
                func=self.tools_instance.get_player_stats,
                name="get_player_stats",
                description="Get comprehensive batting statistics for a player including runs, average, strike rate, and performance vs pace/spin. Use this to get overall player performance metrics.",
                args_schema=PlayerNameInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_player_line_length_analysis,
                name="get_player_line_length_analysis",
                description="Analyze player performance against different line and length combinations. Shows best and worst zones, helping identify technical weaknesses.",
                args_schema=PlayerNameInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_player_wagon_wheel_analysis,
                name="get_player_wagon_wheel_analysis",
                description="Analyze player's scoring zones and boundary distribution. Shows strong and weak scoring areas on the field.",
                args_schema=PlayerNameInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_player_strengths_weaknesses,
                name="get_player_strengths_weaknesses",
                description="Get top 2 strengths and weaknesses with data backing. Provides comprehensive analysis of player capabilities.",
                args_schema=PlayerNameInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_bowling_plan,
                name="get_bowling_plan",
                description="Generate comprehensive bowling plan with strategies, field placements, and key insights to dismiss the player.",
                args_schema=PlayerNameInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_all_players_list,
                name="get_all_players_list",
                description="Get list of all available players in the database. Use this to check player name availability or suggest similar names."
            )
        ]
        
        return tools
    
    def query(self, question: str, player_context: Optional[str] = None) -> str:
        """
        Query the agent with a cricket analytics question.
        
        Args:
            question: User's question
            player_context: Optional player name context
            
        Returns:
            Agent's response with analysis
        """
        try:
            if player_context:
                full_question = f"Analyze {player_context}: {question}"
            else:
                full_question = question
            
            self.conversation_history.append({
                "role": "user",
                "content": full_question
            })
            
            result = self.agent_executor.invoke({
                "input": full_question
            })
            
            response = result.get("output", "I couldn't generate a response. Please try again.")
            
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            return error_msg
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
