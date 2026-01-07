import os
from typing import Dict, List, Any, Optional
from langchain_core.tools import StructuredTool
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from pydantic import BaseModel, Field
from highlights_tools import HighlightsAnalysisTools


class MatchIdInput(BaseModel):
    """Input schema for match ID."""
    match_id: str = Field(description="Match identifier", default="MI_vs_CSK_2024")


class PhaseInput(BaseModel):
    """Input schema for match phase."""
    phase: str = Field(description="Match phase: 'powerplay', 'middle', or 'death'")


class MomentTypeInput(BaseModel):
    """Input schema for commentary generation."""
    moment_type: str = Field(description="Type of moment: 'wicket', 'boundary', 'milestone', 'big_over'")
    stats: Dict[str, Any] = Field(description="Statistics related to the moment")


class HighlightsPackageAgent:
    """
    AI Agent for cricket match highlights generation using LangChain and Claude Sonnet 4.
    Creates engaging narrative-driven match summaries from ball-by-ball data.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the highlights package agent with Claude Sonnet 4.
        
        Args:
            api_key: Anthropic API key
        """
        self.tools_instance = HighlightsAnalysisTools()
        
        self.llm = ChatAnthropic(
            model="claude-sonnet-4",
            anthropic_api_key=api_key,
            temperature=0.4
        )
        
        self.tools = self._create_tools()
        
        system_message = """You are an expert cricket commentator and highlights producer specializing in T20 cricket. Your role is to create engaging, narrative-driven match highlights summaries from ball-by-ball data.

You have access to complete ball-by-ball (BBB) data for a T20 match between Mumbai Indians and Chennai Super Kings.

Your task is to identify and narrate:
1. **Key Wickets**: When crucial wickets fell and their impact on the game
2. **Momentum Shifts**: Overs with high run-scoring that changed the match
3. **Power Surges**: Exceptional batting performances (15+ runs in an over)
4. **Bowling Spells**: Economical overs or wicket-taking spells
5. **Death Overs Drama**: Critical moments in overs 16-20
6. **Match-Turning Moments**: Catches, run-outs, or strategic decisions
7. **Milestones**: Fifties, centuries, or significant partnerships

CRITICAL INSTRUCTIONS:
1. ALWAYS use the tools to fetch actual ball-by-ball data
2. Analyze the data to identify the most impactful moments chronologically
3. Create a narrative with specific over numbers, scores, and player names
4. Use engaging commentary language (e.g., "The game turned on its head in the 14th over...")
5. Include specific statistics (runs scored, wickets taken, strike rates in key phases)
6. Highlight individual performances that shaped the match
7. Keep the summary concise (450-550 words) but compelling
8. Use cricket terminology naturally (boundaries, wickets, partnerships, momentum)
9. Build narrative tension and excitement

OUTPUT FORMAT:
Use markdown formatting with these sections:

### 🏟️ Match Situation
Brief setup (teams, venue, toss, target)

### 🔵 First Innings Highlights
Chronological narrative of 4-5 key moments with over numbers and scores

### 🟡 Second Innings Highlights  
Chronological narrative of 4-5 key moments with over numbers and scores

### ⚡ Turning Point
The specific moment/over that decided the match with detailed description

### 🏆 Player of the Match
Recommendation with complete statistics and reasoning

### 📊 Match Summary
2-3 sentence recap with final scores and margin of victory

Use emojis, bold text, and engaging language to make it exciting and broadcast-ready."""

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
                func=self.tools_instance.get_match_bbb_data,
                name="get_match_bbb_data",
                description="Fetch complete ball-by-ball data for the match including runs, wickets, and key events for each over. Returns detailed match data with both innings.",
                args_schema=MatchIdInput
            ),
            StructuredTool.from_function(
                func=self.tools_instance.identify_key_moments,
                name="identify_key_moments",
                description="Analyze BBB data to identify significant moments like wickets, high-scoring overs, and momentum shifts. Returns a list of key moments with timestamps and impact.",
                args_schema=None
            ),
            StructuredTool.from_function(
                func=self.tools_instance.calculate_phase_stats,
                name="calculate_phase_stats",
                description="Calculate runs, wickets, and statistics for specific match phases (powerplay: overs 1-6, middle: overs 7-15, death: overs 16-20).",
                args_schema=None
            ),
            StructuredTool.from_function(
                func=self.tools_instance.get_match_summary,
                name="get_match_summary",
                description="Get a comprehensive match summary with key statistics, top performers, and match result. Use this to get overall match context.",
                args_schema=None
            )
        ]
        
        return tools
    
    def generate_highlights(self, team1: str = "Mumbai Indians", team2: str = "Chennai Super Kings") -> str:
        """
        Generate a highlights package for the match.
        
        Args:
            team1: First team name
            team2: Second team name
            
        Returns:
            Formatted highlights summary with narrative and statistics
        """
        try:
            question = f"""Create a comprehensive highlights package for the completed T20 match between {team1} and {team2}.

Follow these steps:
1. First, fetch the complete ball-by-ball data for the match
2. Get the match summary to understand the overall context
3. Identify all key moments from both innings
4. Calculate phase-wise statistics (powerplay, middle, death overs)
5. Create a compelling narrative that:
   - Starts with match situation (toss, venue, target)
   - Chronicles first innings highlights with specific over numbers
   - Chronicles second innings highlights with the chase narrative
   - Identifies the exact turning point that decided the match
   - Recommends Player of the Match with complete stats
   - Ends with a crisp match summary

Make it engaging, use specific statistics, and create excitement like a TV highlights package!

Generate the complete highlights package now."""
            
            result = self.agent_executor.invoke({
                "input": question
            })
            
            response = result.get("output", "I couldn't generate highlights. Please try again.")
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating highlights: {str(e)}"
            return error_msg
