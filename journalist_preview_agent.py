import pandas as pd
import numpy as np
from typing import Dict, List, Any
from langchain_anthropic import ChatAnthropic
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool


class JournalistPreviewAgent:
    """
    Generates pre-match previews for IPL matches using ball-by-ball data and player statistics.
    Creates accessible, data-driven content for general cricket audiences.
    """
    
    def __init__(self, llm):
        """Initialize the journalist preview agent with LLM and load datasets."""
        self.llm = llm
        
        self.matches_df = pd.read_csv('data/Sample_IPL_Matches.csv')
        self.batting_df = pd.read_csv('data/IPL_21_24_Batting.csv')
        self.team_batting_df = pd.read_csv('data/IPL_Team_BattingData_21_24.csv')
        self.venue_df = pd.read_csv('data/IPL_Venue_details.csv')
        self.batsman_venue_df = pd.read_csv('data/Batsmanvsvenue.csv')
        self.fantasy_df = pd.read_csv('data/IPL_FantasyData.csv')
        self.line_length_df = pd.read_csv('data/batter_line_length_SR_long.csv')
        self.wagon_wheel_df = pd.read_csv('data/Batter_WagonWheel.csv')
        
        for df in [self.matches_df, self.batting_df, self.team_batting_df, 
                   self.venue_df, self.batsman_venue_df, self.fantasy_df,
                   self.line_length_df, self.wagon_wheel_df]:
            df.columns = df.columns.str.strip()
        
        self.tools = self._create_tools()
        self.agent_executor = self._create_agent()
    
    def _create_tools(self):
        """Create tools for the journalist agent to access cricket data."""
        
        @tool
        def get_team_batting_stats(team_name: str) -> str:
            """
            Get comprehensive batting statistics for a team including strike rates, 
            averages, boundary percentages, and phase-wise performance.
            
            Args:
                team_name: Name of the IPL team
            """
            team_data = self.team_batting_df[self.team_batting_df['batting_team'] == team_name]
            
            if team_data.empty:
                return f"No data found for team: {team_name}"
            
            row = team_data.iloc[0]
            
            stats = f"""Team: {team_name}
Overall Stats:
- Batting Average: {row['batting_average']:.2f}
- Strike Rate: {row['strike_rate']}
- Boundary %: {row['boundary_percentage']}
- Balls per Boundary: {row['balls_per_boundary']:.2f}

vs Bowling Types:
- SR vs Pace: {row['strike_rate_vs_pace']}
- SR vs Spin: {row['strike_rate_vs_spin']}
- Avg vs Spin: {row['batting_average_vs_spin']:.2f}

Phase-wise Strike Rates:
- Powerplay (1-10): {row['strike_rate_balls_1_10']}
- Middle (11-30): {row['strike_rate_balls_11_20']} to {row['strike_rate_balls_21_30']}
- Death (41-50): {row['strike_rate_balls_41_50']}

Innings Performance:
- 1st Innings Avg: {row['First.Innings.Average']:.2f}
- 2nd Innings Avg: {row['Second.Innings.Average']:.2f}"""
            
            return stats
        
        @tool
        def get_top_players_for_team(team_name: str, count: int = 3) -> str:
            """
            Get top performing batsmen for a specific team based on runs, average, and strike rate.
            
            Args:
                team_name: Name of the IPL team
                count: Number of top players to return (default 3)
            """
            team_players = self.batting_df[self.batting_df['Player'].str.contains(team_name, case=False, na=False)]
            
            if team_players.empty:
                all_players = self.batting_df.copy()
                all_players['score'] = (
                    all_players['Runs'] * 0.4 + 
                    all_players['Average'] * 0.3 + 
                    all_players['Strike_Rate'] * 0.3
                )
                top_players = all_players.nlargest(count, 'score')
            else:
                team_players['score'] = (
                    team_players['Runs'] * 0.4 + 
                    team_players['Average'] * 0.3 + 
                    team_players['Strike_Rate'] * 0.3
                )
                top_players = team_players.nlargest(count, 'score')
            
            result = f"Top {count} players:\n\n"
            for idx, (_, player) in enumerate(top_players.iterrows(), 1):
                result += f"{idx}. {player['Player']}\n"
                result += f"   Runs: {int(player['Runs'])} | Avg: {player['Average']:.2f} | SR: {player['Strike_Rate']:.2f}\n"
                result += f"   SR vs Pace: {player['SR_vs_Pace']:.2f} | SR vs Spin: {player['SR_vs_Spin']:.2f}\n"
                result += f"   Boundary %: {player['Boundary_Percentage']:.2f}%\n"
                result += f"   Powerplay SR: {player['SR_balls_1_10']:.2f} | Death SR: {player['SR_balls_41_50']:.2f}\n\n"
            
            return result
        
        @tool
        def get_venue_characteristics(venue_name: str) -> str:
            """
            Get detailed venue characteristics including pace/spin friendliness, 
            average scores, and boundary dimensions.
            
            Args:
                venue_name: Name of the venue
            """
            venue_data = self.venue_df[self.venue_df['venue'].str.contains(venue_name, case=False, na=False)]
            
            if venue_data.empty:
                return f"No data found for venue: {venue_name}"
            
            row = venue_data.iloc[0]
            
            pace_pct = float(row.get('Pace_Wicket_Percentage', 50))
            spin_pct = 100 - pace_pct
            
            venue_type = "pace-friendly" if pace_pct > 55 else "spin-friendly" if spin_pct > 55 else "balanced"
            
            stats = f"""Venue: {row['venue']}
City: {row.get('city', 'Unknown')}

Bowling Conditions:
- Pace Wicket %: {pace_pct:.1f}%
- Spin Wicket %: {spin_pct:.1f}%
- Venue Type: {venue_type}

Batting Conditions:
- Average 1st Innings Score: {row.get('Average_1st_Innings_Score', 'N/A')}
- Average 2nd Innings Score: {row.get('Average_2nd_Innings_Score', 'N/A')}
- Boundaries per Match: {row.get('Boundaries_per_Match', 'N/A')}

Dimensions:
- Straight Boundary: {row.get('Straight_Boundary', 'N/A')}m
- Square Boundary: {row.get('Square_Boundary', 'N/A')}m"""
            
            return stats
        
        @tool
        def get_player_venue_performance(player_name: str, venue_name: str) -> str:
            """
            Get a player's historical performance at a specific venue.
            
            Args:
                player_name: Name of the player
                venue_name: Name of the venue
            """
            player_data = self.batsman_venue_df[
                (self.batsman_venue_df['Batter'].str.contains(player_name, case=False, na=False)) &
                (self.batsman_venue_df['venue'].str.contains(venue_name, case=False, na=False))
            ]
            
            if player_data.empty:
                return f"No venue-specific data found for {player_name} at {venue_name}"
            
            row = player_data.iloc[0]
            
            stats = f"""{player_name} at {venue_name}:
- Innings: {row.get('Innings', 0)}
- Runs: {row.get('Runs', 0)}
- Average: {row.get('Average', 0):.2f}
- Strike Rate: {row.get('Strike_Rate', 0):.2f}
- Highest Score: {row.get('Highest_Score', 'N/A')}"""
            
            return stats
        
        @tool
        def get_player_technical_analysis(player_name: str) -> str:
            """
            Get player's technical strengths and weaknesses based on line/length analysis.
            Shows which bowling zones the player scores well against and struggles with.
            
            Args:
                player_name: Name of the player
            """
            player_data = self.line_length_df[
                self.line_length_df['Batter'].str.strip().str.contains(player_name, case=False, na=False)
            ]
            
            if player_data.empty:
                return f"No technical data found for {player_name}"
            
            player_data = player_data.copy()
            player_data['SR'] = pd.to_numeric(player_data['SR'], errors='coerce')
            player_data = player_data.dropna(subset=['SR'])
            
            if player_data.empty:
                return f"No valid technical data for {player_name}"
            
            sorted_data = player_data.sort_values('SR', ascending=False)
            best_zones = sorted_data.head(3)
            worst_zones = sorted_data.tail(3)
            
            result = f"{player_name} - Technical Analysis:\n\n"
            result += "Strength Zones (High SR):\n"
            for _, zone in best_zones.iterrows():
                result += f"- {zone['Length']} on {zone['Line']}: SR {zone['SR']:.1f} ({int(zone['Balls'])} balls)\n"
            
            result += "\nWeakness Zones (Low SR):\n"
            for _, zone in worst_zones.iterrows():
                result += f"- {zone['Length']} on {zone['Line']}: SR {zone['SR']:.1f} ({int(zone['Balls'])} balls)\n"
            
            return result
        
        @tool
        def get_player_scoring_zones(player_name: str) -> str:
            """
            Get player's preferred scoring zones and boundary-hitting patterns.
            
            Args:
                player_name: Name of the player
            """
            player_data = self.wagon_wheel_df[
                self.wagon_wheel_df['Batter'].str.contains(player_name, case=False, na=False)
            ]
            
            if player_data.empty:
                return f"No scoring zone data found for {player_name}"
            
            sorted_zones = player_data.sort_values('Boundaries', ascending=False)
            
            result = f"{player_name} - Scoring Zones:\n\n"
            result += "Top Boundary Zones:\n"
            for _, zone in sorted_zones.head(5).iterrows():
                result += f"- {zone['Zone']}: {int(zone['Boundaries'])} boundaries\n"
            
            return result
        
        @tool
        def get_head_to_head_match_data(team1: str, team2: str) -> str:
            """
            Get historical match data between two teams from ball-by-ball records.
            
            Args:
                team1: First team name
                team2: Second team name
            """
            h2h_matches = self.matches_df[
                ((self.matches_df['batting_team'] == team1) & (self.matches_df['bowling_team'] == team2)) |
                ((self.matches_df['batting_team'] == team2) & (self.matches_df['bowling_team'] == team1))
            ]
            
            if h2h_matches.empty:
                return f"No head-to-head data found between {team1} and {team2}"
            
            match_ids = h2h_matches['match_id'].unique()
            
            result = f"Head-to-Head: {team1} vs {team2}\n"
            result += f"Total matches in dataset: {len(match_ids)}\n\n"
            
            for match_id in match_ids[:3]:
                match_data = h2h_matches[h2h_matches['match_id'] == match_id]
                
                if not match_data.empty:
                    first_row = match_data.iloc[0]
                    result += f"Match at {first_row['venue']} ({first_row['start_date']}):\n"
                    result += f"- {first_row['batting_team']} innings total: {first_row['innings1_total']}\n"
                    
                    if pd.notna(first_row['innings2_total']):
                        result += f"- Target: {first_row['target']}\n"
                    result += "\n"
            
            return result
        
        @tool
        def get_fantasy_form_data(player_name: str) -> str:
            """
            Get player's recent fantasy performance and form indicators.
            
            Args:
                player_name: Name of the player
            """
            player_data = self.fantasy_df[
                self.fantasy_df['Player'].str.contains(player_name, case=False, na=False)
            ]
            
            if player_data.empty:
                return f"No fantasy data found for {player_name}"
            
            row = player_data.iloc[0]
            
            stats = f"""{player_name} - Fantasy Form:
- Total Fantasy Points: {row.get('Total_Fantasy_Points', 'N/A')}
- Average Points per Match: {row.get('Avg_Points_per_Match', 'N/A')}
- Consistency Rating: {row.get('Consistency', 'N/A')}
- Recent Form: {row.get('Recent_Form', 'N/A')}"""
            
            return stats
        
        return [
            get_team_batting_stats,
            get_top_players_for_team,
            get_venue_characteristics,
            get_player_venue_performance,
            get_player_technical_analysis,
            get_player_scoring_zones,
            get_head_to_head_match_data,
            get_fantasy_form_data
        ]
    
    def _create_agent(self):
        """Create the LangChain agent with journalist-specific prompt."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional cricket journalist writing pre-match previews for IPL matches. 
Your audience is general cricket fans seeking accessible, bird's-eye view analysis.

CRITICAL REQUIREMENTS:
- Maximum 500 words total
- Data-driven: Use statistics from the tools to support every claim
- Accessible language for general audiences
- Focus on how the game is expected to unfold and who will play starring roles

STRUCTURE YOUR PREVIEW:
1. Opening (50-75 words): Set the scene, match context, key storyline
2. Team Form & Strengths (50-75 words): Brief overview of both teams
3. Players to Watch - Team 1 (75-100 words): Profile 1-2 key players with data
4. Players to Watch - Team 2 (75-100 words): Profile 1-2 key players with data
5. Venue Profile (75-100 words): Pitch characteristics, historical trends
6. Key Talking Points (75-100 words): Major factors that could decide the match
7. Prediction (50 words): Data-informed expectation

FORBIDDEN CONTENT:
- NO press conference quotes
- NO practice session reports
- NO team news or injury updates
- NO information not available in the datasets

ALLOWED EXTERNAL INFO:
- Weather in the city (general knowledge)
- Basic cricket concepts

TONE: Professional, engaging, informative - like ESPNcricinfo previews

Use the available tools to gather all necessary data before writing. Make multiple tool calls to build a comprehensive picture."""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])
        
        agent = create_tool_calling_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True, max_iterations=15)
    
    def generate_preview(self, team1: str, team2: str, venue: str) -> str:
        """
        Generate a comprehensive pre-match preview.
        
        Args:
            team1: First team name
            team2: Second team name
            venue: Venue name
            
        Returns:
            Formatted match preview (max 500 words)
        """
        query = f"""Generate a pre-match preview for the IPL match between {team1} and {team2} at {venue}.

Follow the structure exactly:
1. Opening paragraph with match context
2. Brief team form analysis for both teams
3. Players to Watch section for {team1} (1-2 players)
4. Players to Watch section for {team2} (1-2 players)
5. Venue Profile for {venue}
6. Key Talking Points
7. Match Prediction

Use all available tools to gather comprehensive data. Maximum 500 words total."""
        
        try:
            result = self.agent_executor.invoke({"input": query})
            return result['output']
        except Exception as e:
            return f"Error generating preview: {str(e)}"
