import os
from typing import Dict, List, Any, Optional
from langchain_core.tools import StructuredTool
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from pydantic import BaseModel, Field
from betting_tools import BettingAnalysisTools


class TeamNamesInput(BaseModel):
    """Input schema for two team names."""
    team1_name: str = Field(description="Name of the first cricket team")
    team2_name: str = Field(description="Name of the second cricket team")


class TeamNameInput(BaseModel):
    """Input schema for single team name."""
    team_name: str = Field(description="Name of the cricket team")


class BettingPreviewAgent:
    """
    AI Agent for cricket betting preview generation using LangChain and Claude Sonnet 4.
    Creates insightful match previews from a betting perspective.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the betting preview agent with Claude Sonnet 4.
        
        Args:
            api_key: Anthropic API key
        """
        self.tools_instance = BettingAnalysisTools()
        
        self.llm = ChatAnthropic(
            model="claude-sonnet-4",
            anthropic_api_key=api_key,
            temperature=0.3
        )
        
        self.tools = self._create_tools()
        
        system_message = """You are an expert cricket betting analyst specializing in IPL T20 matches. Your role is to create insightful, data-driven match previews from a betting perspective, similar to professional football betting previews.

You have access to comprehensive team batting statistics from IPL 2021-2024 including:
- Strike rates (overall, vs pace, vs spin, by innings, by phase)
- Boundary percentages and balls per boundary
- Batting averages and consistency metrics
- Performance in different match situations (powerplay, middle overs, death overs)
- Dot ball percentages and non-boundary strike rates

CRITICAL INSTRUCTIONS:
1. ALWAYS use the get_detailed_match_analysis tool to fetch comprehensive analysis
2. This tool provides:
   - Fixture analysis with team form and H2H context
   - Key statistics and trends
   - Betting recommendations with odds and reasoning
   - Detailed reasoning sections with multiple perspectives

3. Format the preview professionally with clear sections
4. Include specific odds for each betting recommendation
5. Provide detailed reasoning for each tip (similar to football previews)
6. Use betting terminology naturally (odds, value, form, momentum)
7. Be data-driven and specific with statistics

OUTPUT FORMAT - Use this exact structure:

### IPL Preview: [Team1] vs [Team2]

**Fixture Analysis:**
[Detailed analysis from the tool including team form, H2H context, and key differentiators]

**Key Stats & Trends:**
[Bullet points of important statistics and trends]
- Stat 1
- Stat 2
- Stat 3

**Recommended Bets & Odds:**

**1. [Bet Type]: [Selection] (Odds: X.XX)**
[Detailed reasoning for this bet]

**2. [Bet Type]: [Selection] (Odds: X.XX)**
[Detailed reasoning for this bet]

**3. [Bet Type]: [Selection] (Odds: X.XX)**
[Detailed reasoning for this bet]

**4. [Bet Type]: [Selection] (Odds: X.XX)**
[Detailed reasoning for this bet]

---

**Detailed Analysis:**

**[Section Title 1]**
[Detailed reasoning content]

**[Section Title 2]**
[Detailed reasoning content]

**[Section Title 3]**
[Detailed reasoning content]

**Final Prediction:**
[Comprehensive prediction with score ranges and match outcome]

Be specific, data-driven, and provide actionable betting insights with clear reasoning for each recommendation."""

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
    
    def _create_tools(self) -> List[StructuredTool]:
        """
        Convert tool methods to LangChain StructuredTools.
        
        Returns:
            List of LangChain tools
        """
        tools = [
            StructuredTool.from_function(
                func=self.tools_instance.get_team_batting_stats,
                name="get_team_batting_stats",
                description="Fetch comprehensive batting statistics for a team including strike rates, averages, boundary percentages, and phase-wise performance (powerplay, middle, death overs). Use this to get detailed team performance metrics.",
                args_schema=TeamNameInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.compare_team_stats,
                name="compare_team_stats",
                description="Compare two teams across all batting metrics and identify advantages/disadvantages. Returns detailed comparison with key differences in strike rates, averages, and phase-wise performance.",
                args_schema=TeamNamesInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_betting_insights,
                name="get_betting_insights",
                description="Generate betting insights based on team comparison including predicted scores, key matchups, betting angles, and value picks. Use this to get structured betting recommendations.",
                args_schema=TeamNamesInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.fetch_betting_preview_examples,
                name="fetch_betting_preview_examples",
                description="Fetch sample cricket betting match preview examples to understand the format, style, and structure. Use this to learn how professional betting previews are written."
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_all_teams_list,
                name="get_all_teams_list",
                description="Get list of all available teams in the database. Use this to check team name availability or suggest similar names."
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_detailed_match_analysis,
                name="get_detailed_match_analysis",
                description="Get comprehensive match analysis including fixture analysis, key stats & trends, betting recommendations with odds, and detailed reasoning sections. This is the PRIMARY tool to use for generating betting previews. Returns all data needed for a complete preview.",
                args_schema=TeamNamesInput
            )
        ]
        
        return tools
    
    def generate_preview_with_agent(self, team1_name: str, team2_name: str) -> str:
        """
        Generate a betting preview for a match between two teams.
        
        Args:
            team1_name: First team name
            team2_name: Second team name
            
        Returns:
            Formatted betting preview with analysis and recommendations
        """
        try:
            question = f"""Create a comprehensive betting preview for an upcoming IPL match between {team1_name} and {team2_name}.

Use the get_detailed_match_analysis tool to fetch all the necessary data including:
- Fixture analysis with team form and H2H context
- Key statistics and trends
- Betting recommendations with odds
- Detailed reasoning sections

Then format this data into a professional betting preview following the exact output format specified in your instructions.

Make sure to:
1. Use the fixture_analysis as the opening paragraph
2. List all key_stats_and_trends as bullet points
3. Present each betting recommendation with its odds and reasoning
4. Include all detailed reasoning sections
5. End with the final prediction

Generate the complete, well-formatted betting preview now."""
            
            result = self.agent_executor.invoke({
                "input": question
            })
            
            response = result.get("output", "I couldn't generate a preview. Please try again.")
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating betting preview: {str(e)}"
            return error_msg
    
    def generate_preview(self, team1_name: str, team2_name: str, venue: str = None) -> str:
        """
        Generate a betting preview directly using the detailed analysis tool.
        Faster and more reliable than using the agent.
        
        Args:
            team1_name: First team name
            team2_name: Second team name
            venue: Venue name (optional)
            
        Returns:
            Formatted betting preview with analysis and recommendations
        """
        try:
            # Get detailed analysis
            analysis = self.tools_instance.get_detailed_match_analysis(team1_name, team2_name, venue=venue)
            
            if "error" in analysis:
                return f"Error: {analysis['error']}"
            
            # Format the preview
            preview = f"### IPL Preview: {team1_name} vs {team2_name}\n\n"
            
            if venue:
                preview += f"**Venue:** {venue}\n\n"
            
            # Fixture Analysis (now a list of 3 points)
            preview += "**Fixture Analysis:**\n\n"
            if isinstance(analysis['fixture_analysis'], list):
                for point in analysis['fixture_analysis']:
                    preview += f"{point}\n\n"
            else:
                preview += f"{analysis['fixture_analysis']}\n\n"
            
            # Venue Insights (replaces Key Stats & Trends)
            if venue:
                preview += "**Venue Insights:**\n\n"
            else:
                preview += "**Key Stats & Trends:**\n\n"
            
            for insight in analysis['venue_insights']:
                preview += f"{insight}\n\n"
            
            # Recommended Bets & Odds
            preview += "**Recommended Bets & Odds:**\n\n"
            for i, bet in enumerate(analysis['recommended_bets'], 1):
                preview += f"**{i}. {bet['bet_type']}: {bet['selection']} (Odds: {bet['odds']})**\n"
                preview += f"{bet['reasoning']}\n\n"
            
            preview += "---\n\n"
            
            # Detailed Analysis
            preview += "**Detailed Analysis:**\n\n"
            reasoning = analysis['detailed_reasoning']
            
            for section in reasoning['sections']:
                preview += f"**{section['title']}**\n"
                preview += f"{section['content']}\n\n"
            
            # Final Prediction
            preview += "**Final Prediction:**\n"
            preview += f"{reasoning['final_prediction']}\n"
            
            return preview
            
        except Exception as e:
            error_msg = f"Error generating betting preview: {str(e)}"
            return error_msg
