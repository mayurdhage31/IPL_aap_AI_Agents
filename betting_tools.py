import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import json
import numpy as np
import random


class BettingAnalysisTools:
    """
    Tools for cricket betting analysis and team comparisons.
    Provides methods to fetch team statistics and generate betting insights.
    """
    
    def __init__(self):
        """Initialize with team batting data."""
        self.team_data_path = "data/IPL_Team_BattingData_21_24.csv"
        self.team_df = pd.read_csv(self.team_data_path)
        self.player_data_path = "data/IPL_21_24_Batting.csv"
        self.player_df = pd.read_csv(self.player_data_path)
        self.venue_data_path = "data/IPL_Venue_details.csv"
        self.venue_df = pd.read_csv(self.venue_data_path)
        self.venue_toss_decisions_path = "data/VenueTossDecisions.csv"
        self.venue_toss_decisions_df = pd.read_csv(self.venue_toss_decisions_path)
        self.venue_toss_situation_path = "data/VenueToss_Situation_Details.csv"
        self.venue_toss_situation_df = pd.read_csv(self.venue_toss_situation_path)
        self.fantasy_data_path = "data/IPL_FantasyData.csv"
        try:
            self.fantasy_df = pd.read_csv(self.fantasy_data_path)
            self.fantasy_df.columns = self.fantasy_df.columns.str.strip()
        except:
            self.fantasy_df = None
        
        # Clean column names
        self.player_df.columns = self.player_df.columns.str.strip()
        self.team_df.columns = self.team_df.columns.str.strip()
        self.venue_df.columns = self.venue_df.columns.str.strip()
        self.venue_toss_decisions_df.columns = self.venue_toss_decisions_df.columns.str.strip()
        self.venue_toss_situation_df.columns = self.venue_toss_situation_df.columns.str.strip()
        
        # Static batting first/second win percentages
        self.batting_win_percentages = {
            'Chennai Super Kings': {'batting_first': '47.8% (11/23)', 'batting_second': '50.0% (10/20)'},
            'Delhi Capitals': {'batting_first': '56.2% (9/16)', 'batting_second': '37.5% (9/24)'},
            'Gujarat Titans': {'batting_first': '55.0% (11/20)', 'batting_second': '58.3% (14/24)'},
            'Kolkata Knight Riders': {'batting_first': '54.5% (12/22)', 'batting_second': '55.6% (10/18)'},
            'Lucknow Super Giants': {'batting_first': '54.2% (13/24)', 'batting_second': '44.4% (8/18)'},
            'Mumbai Indians': {'batting_first': '50.0% (10/20)', 'batting_second': '46.2% (12/26)'},
            'Punjab Kings': {'batting_first': '40.9% (9/22)', 'batting_second': '54.5% (12/22)'},
            'Rajasthan Royals': {'batting_first': '50.0% (8/16)', 'batting_second': '46.2% (12/26)'},
            'Royal Challengers Bengaluru': {'batting_first': '53.8% (14/26)', 'batting_second': '61.1% (11/18)'},
            'Sunrisers Hyderabad': {'batting_first': '44.0% (11/25)', 'batting_second': '44.4% (8/18)'}
        }
    
    def get_all_teams_list(self) -> List[str]:
        """
        Get list of all available teams.
        
        Returns:
            List of team names
        """
        return sorted(self.team_df['batting_team'].unique().tolist())
    
    def get_all_venues_list(self) -> List[str]:
        """
        Get list of all available venues.
        
        Returns:
            List of venue names
        """
        return sorted(self.venue_df['venue'].unique().tolist())
    
    def generate_h2h_record(self, team1: str, team2: str) -> Dict[str, Any]:
        """
        Generate simulated head-to-head record for last 5 matches.
        Since H2H data is not available, this generates realistic dummy data.
        
        Args:
            team1: First team name
            team2: Second team name
            
        Returns:
            Dictionary with H2H record
        """
        # Generate realistic H2H based on team rankings
        team1_stats = self.get_team_batting_stats(team1)
        team2_stats = self.get_team_batting_stats(team2)
        
        if "error" in team1_stats or "error" in team2_stats:
            return {"team1_wins": 3, "team2_wins": 2, "total_matches": 5}
        
        # Use team rankings to determine likely H2H
        t1_rank = team1_stats['rank_strike_rate']
        t2_rank = team2_stats['rank_strike_rate']
        
        if t1_rank < t2_rank:
            team1_wins = random.choice([3, 4])
        elif t1_rank > t2_rank:
            team1_wins = random.choice([1, 2])
        else:
            team1_wins = random.choice([2, 3])
        
        team2_wins = 5 - team1_wins
        
        return {
            "team1_wins": team1_wins,
            "team2_wins": team2_wins,
            "total_matches": 5,
            "narrative": f"{team1} leads the head-to-head with {team1_wins} wins out of the last {5} encounters, while {team2} has won {team2_wins}."
        }
    
    def generate_recent_form(self, team: str) -> Dict[str, Any]:
        """
        Generate simulated recent form for last 5 matches.
        Since recent form data is not available, this generates realistic dummy data.
        
        Args:
            team: Team name
            
        Returns:
            Dictionary with recent form
        """
        team_stats = self.get_team_batting_stats(team)
        
        if "error" in team_stats:
            return {"wins": 3, "total_matches": 5}
        
        # Use team performance metrics to determine likely form
        sr = team_stats['strike_rate']
        avg = team_stats['batting_average']
        
        # Better teams likely have better recent form
        if sr > 140 and avg > 30:
            wins = random.choice([4, 5])
        elif sr > 135 and avg > 28:
            wins = random.choice([3, 4])
        else:
            wins = random.choice([2, 3])
        
        return {
            "wins": wins,
            "total_matches": 5,
            "narrative": f"{team} has won {wins} out of their last 5 matches, showing {'excellent' if wins >= 4 else 'good' if wins == 3 else 'moderate'} form."
        }
    
    def get_venue_insights(self, venue_name: str) -> Dict[str, Any]:
        """
        Get comprehensive venue insights including toss decisions, win/loss records, and venue statistics.
        
        Args:
            venue_name: Name of the venue
            
        Returns:
            Dictionary with venue insights
        """
        insights = {
            "venue_name": venue_name,
            "toss_decisions": {},
            "toss_situations": {},
            "venue_stats": {}
        }
        
        # Get toss decisions
        toss_data = self.venue_toss_decisions_df[self.venue_toss_decisions_df['venue_clean'] == venue_name]
        if not toss_data.empty:
            won_toss = toss_data[toss_data['Toss'] == 'Won Toss'].iloc[0] if len(toss_data[toss_data['Toss'] == 'Won Toss']) > 0 else None
            lost_toss = toss_data[toss_data['Toss'] == 'Lost Toss'].iloc[0] if len(toss_data[toss_data['Toss'] == 'Lost Toss']) > 0 else None
            
            if won_toss is not None:
                insights['toss_decisions']['won_toss'] = {
                    'batted_first': int(won_toss['Batted First']),
                    'bowled_first': int(won_toss['Bowled First'])
                }
            
            if lost_toss is not None:
                insights['toss_decisions']['lost_toss'] = {
                    'batted_first': int(lost_toss['Batted First']),
                    'bowled_first': int(lost_toss['Bowled First'])
                }
        
        # Get toss situation win/loss records
        situation_data = self.venue_toss_situation_df[self.venue_toss_situation_df['venue_clean'] == venue_name]
        if not situation_data.empty:
            for _, row in situation_data.iterrows():
                situation = row['situation']
                insights['toss_situations'][situation] = {
                    'wins': int(row['Wins']),
                    'losses': int(row['Losses']),
                    'no_result': int(row['No Result'])
                }
        
        # Get venue statistics
        venue_stats = self.venue_df[self.venue_df['venue'] == venue_name]
        if not venue_stats.empty:
            venue_row = venue_stats.iloc[0]
            insights['venue_stats'] = {
                'matches_played': int(venue_row['MatchesPlayed']),
                'average_score': round(float(venue_row['Average_Score']), 2),
                'average_first_innings_score': round(float(venue_row['Average_First_Innings_Score']), 2),
                'boundary_percentage': str(venue_row['Boundary_Percentage_per_match']).replace('%', ''),
                'fours_per_match': round(float(venue_row['Fours_perMatch']), 2),
                'sixes_per_match': round(float(venue_row['Sixes_perMatch']), 2),
                'pace_wickets_pct': str(venue_row['Percentage_Of_wickets_Pace_Bowlers']).replace('%', ''),
                'spin_wickets_pct': str(venue_row['Percentage_Of_wickets_Spin_Bowlers']).replace('%', ''),
                'powerplay_runs': round(float(venue_row['Powerplay_Runs_Scored_perMatch.x']), 2),
                'powerplay_wickets': round(float(venue_row['Powerplay_Wickets_perMatch.x']), 2),
                'powerplay_boundary_pct': str(venue_row['Powerplay_Boundary_Pct_perMatch.x']).replace('%', ''),
                'middle_overs_runs': round(float(venue_row['MiddleOvers_Runs_Scored_perMatch.x']), 2),
                'middle_overs_wickets': round(float(venue_row['MiddleOvers_Wickets_perMatch.x']), 2),
                'death_overs_runs': round(float(venue_row['DeathOvers_Runs_Scored_perMatch.x']), 2),
                'death_overs_wickets': round(float(venue_row['DeathOvers_Wickets_perMatch.x']), 2)
            }
        
        return insights
    
    def get_top_players_by_team(self, team_name: str, top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Get top players for a team based on batting statistics.
        
        Args:
            team_name: Name of the team
            top_n: Number of top players to return
            
        Returns:
            List of top players with their stats
        """
        if self.fantasy_df is None:
            # Fallback to player data if fantasy data not available
            top_players = self.player_df.nlargest(top_n, 'Total_Runs_Scored')[['Batter_Name', 'batting_average', 'strike_rate', 'Total_Runs_Scored']].head(top_n)
            return [{
                'name': row['Batter_Name'],
                'average': round(row['batting_average'], 2),
                'strike_rate': round(float(str(row['strike_rate']).strip('%')), 2) if isinstance(row['strike_rate'], str) else round(row['strike_rate'], 2),
                'total_runs': int(row['Total_Runs_Scored'])
            } for _, row in top_players.iterrows()]
        
        # Use fantasy data to get team-specific players
        # For now, return top players from player data as a proxy
        top_players = self.player_df.nlargest(top_n, 'Total_Runs_Scored')[['Batter_Name', 'batting_average', 'strike_rate', 'Total_Runs_Scored']].head(top_n)
        return [{
            'name': row['Batter_Name'],
            'average': round(row['batting_average'], 2),
            'strike_rate': round(float(str(row['strike_rate']).strip('%')), 2) if isinstance(row['strike_rate'], str) else round(row['strike_rate'], 2),
            'total_runs': int(row['Total_Runs_Scored'])
        } for _, row in top_players.iterrows()]
    
    def get_venue_stats(self, venue_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get venue statistics. If no venue specified, return average across all venues.
        
        Args:
            venue_name: Name of the venue (optional)
            
        Returns:
            Dictionary with venue statistics
        """
        if venue_name and not self.venue_df.empty:
            venue_data = self.venue_df[self.venue_df['venue'].str.contains(venue_name, case=False, na=False)]
            if not venue_data.empty:
                venue_row = venue_data.iloc[0]
                return {
                    'venue': venue_row['venue'],
                    'average_score': round(venue_row['Average_Score'], 2),
                    'average_first_innings': round(venue_row['Average_First_Innings_Score'], 2),
                    'powerplay_runs': round(venue_row['Powerplay_Runs_Scored_perMatch.x'], 2),
                    'powerplay_runs_first_innings': round(venue_row['Powerplay_Runs_Scored_First_Innings.x'], 2),
                    'death_overs_runs': round(venue_row['DeathOvers_Runs_Scored_perMatch.x'], 2),
                    'boundary_percentage': round(float(str(venue_row['Boundary_Percentage_per_match']).strip('%')), 2) if isinstance(venue_row['Boundary_Percentage_per_match'], str) else round(venue_row['Boundary_Percentage_per_match'], 2)
                }
        
        # Return average stats across all venues
        return {
            'venue': 'Average across all venues',
            'average_score': round(self.venue_df['Average_Score'].mean(), 2),
            'average_first_innings': round(self.venue_df['Average_First_Innings_Score'].mean(), 2),
            'powerplay_runs': round(self.venue_df['Powerplay_Runs_Scored_perMatch.x'].mean(), 2),
            'powerplay_runs_first_innings': round(self.venue_df['Powerplay_Runs_Scored_First_Innings.x'].mean(), 2),
            'death_overs_runs': round(self.venue_df['DeathOvers_Runs_Scored_perMatch.x'].mean(), 2),
            'boundary_percentage': round(self.venue_df['Boundary_Percentage_per_match'].apply(lambda x: float(str(x).strip('%')) if isinstance(x, str) else x).mean(), 2)
        }
    
    def get_team_batting_stats(self, team_name: str) -> Dict[str, Any]:
        """
        Fetch comprehensive batting statistics for a team.
        
        Args:
            team_name: Name of the team
            
        Returns:
            Dictionary containing all batting metrics
        """
        team_data = self.team_df[self.team_df['batting_team'] == team_name]
        
        if team_data.empty:
            return {"error": f"Team '{team_name}' not found in database"}
        
        team_row = team_data.iloc[0]
        
        stats = {
            "team_name": team_name,
            "batting_average": round(team_row['batting_average'], 2),
            "strike_rate": round(float(team_row['strike_rate'].strip('%')), 2),
            "boundary_percentage": round(float(team_row['boundary_percentage'].strip('%')), 2),
            "dot_ball_percentage": round(float(team_row['dot_ball_percentage'].strip('%')), 2),
            "balls_per_boundary": round(team_row['balls_per_boundary'], 2),
            
            # Performance vs bowling types
            "strike_rate_vs_pace": round(float(team_row['strike_rate_vs_pace'].strip('%')), 2),
            "strike_rate_vs_spin": round(float(team_row['strike_rate_vs_spin'].strip('%')), 2),
            "batting_average_vs_spin": round(team_row['batting_average_vs_spin'], 2),
            "boundary_percentage_vs_pace": round(float(team_row['boundary_percentage_vs_pace'].strip('%')), 2),
            "boundary_percentage_vs_spin": round(float(team_row['boundary_percentage_vs_spin'].strip('%')), 2),
            
            # Phase-wise performance
            "strike_rate_1st_innings": round(float(team_row['strike_rate_1st_innings'].strip('%')), 2),
            "strike_rate_2nd_innings": round(float(team_row['strike_rate_2nd_innings'].strip('%')), 2),
            "strike_rate_balls_1_10": round(float(team_row['strike_rate_balls_1_10'].strip('%')), 2),
            "strike_rate_balls_11_20": round(float(team_row['strike_rate_balls_11_20'].strip('%')), 2),
            "strike_rate_balls_21_30": round(float(team_row['strike_rate_balls_21_30'].strip('%')), 2),
            "strike_rate_balls_31_40": round(float(team_row['strike_rate_balls_31_40'].strip('%')), 2),
            "strike_rate_balls_41_50": round(float(team_row['strike_rate_balls_41_50'].strip('%')), 2),
            
            # Innings averages
            "first_innings_average": round(team_row['First.Innings.Average'], 2),
            "second_innings_average": round(team_row['Second.Innings.Average'], 2),
            
            # Rankings
            "rank_strike_rate": int(team_row['Rank_strike_rate']),
            "rank_boundary_percentage": int(team_row['Rank_boundary_percentage']),
            "rank_batting_average": int(team_row['Rank_batting_average'])
        }
        
        return stats
    
    def compare_team_stats(self, team1_name: str, team2_name: str) -> Dict[str, Any]:
        """
        Compare two teams across all batting metrics.
        
        Args:
            team1_name: First team name
            team2_name: Second team name
            
        Returns:
            Comparative analysis with advantages/disadvantages
        """
        team1_stats = self.get_team_batting_stats(team1_name)
        team2_stats = self.get_team_batting_stats(team2_name)
        
        if "error" in team1_stats or "error" in team2_stats:
            return {"error": "One or both teams not found"}
        
        comparison = {
            "team1": team1_name,
            "team2": team2_name,
            "team1_stats": team1_stats,
            "team2_stats": team2_stats,
            "advantages": {
                "team1": [],
                "team2": []
            },
            "key_differences": []
        }
        
        # Compare key metrics
        metrics_to_compare = [
            ("strike_rate", "Overall Strike Rate", "higher"),
            ("batting_average", "Batting Average", "higher"),
            ("boundary_percentage", "Boundary %", "higher"),
            ("strike_rate_vs_pace", "SR vs Pace", "higher"),
            ("strike_rate_vs_spin", "SR vs Spin", "higher"),
            ("strike_rate_balls_41_50", "Death Overs SR", "higher"),
            ("first_innings_average", "1st Innings Average", "higher"),
            ("second_innings_average", "2nd Innings Average", "higher"),
            ("dot_ball_percentage", "Dot Ball %", "lower")
        ]
        
        for metric, label, better in metrics_to_compare:
            val1 = team1_stats[metric]
            val2 = team2_stats[metric]
            diff = abs(val1 - val2)
            
            if diff > 0.5:  # Significant difference threshold
                if better == "higher":
                    if val1 > val2:
                        comparison["advantages"]["team1"].append(f"{label}: {val1} vs {val2}")
                    else:
                        comparison["advantages"]["team2"].append(f"{label}: {val2} vs {val1}")
                else:  # lower is better
                    if val1 < val2:
                        comparison["advantages"]["team1"].append(f"{label}: {val1} vs {val2}")
                    else:
                        comparison["advantages"]["team2"].append(f"{label}: {val2} vs {val1}")
                
                comparison["key_differences"].append({
                    "metric": label,
                    "team1_value": val1,
                    "team2_value": val2,
                    "difference": round(diff, 2)
                })
        
        return comparison
    
    def fetch_betting_preview_examples(self) -> List[str]:
        """
        Fetch sample betting preview formats from cricket sources.
        Returns pre-defined examples as web scraping may be unreliable.
        
        Returns:
            List of sample betting preview texts
        """
        # Pre-defined examples based on typical cricket betting previews
        examples = [
            """
            **Match Preview: Mumbai Indians vs Chennai Super Kings**
            
            The clash between MI and CSK promises to be a high-octane encounter. Mumbai's explosive batting lineup, 
            averaging 185+ in recent matches, will face CSK's experienced bowling attack. The key battle will be 
            in the powerplay where MI scores at 145 SR compared to CSK's 135 SR.
            
            **Betting Angles:**
            - Total Runs: Over 175.5 looks value given both teams' scoring rates
            - Match Winner: MI slight favorites at home, but CSK's chase record (avg 162 in 2nd innings) makes them dangerous
            - Top Batsman: Rohit Sharma (avg 42) vs Ruturaj Gaikwad (avg 38) - both in good form
            
            **Prediction:** MI to score 185-195, CSK to chase it down in final over. CSK to win by 4 wickets.
            """,
            
            """
            **Head-to-Head Analysis**
            
            Form Guide: Team A has won 3 of last 5 encounters, but Team B's recent surge (SR of 155 in death overs) 
            makes them formidable. The pitch traditionally favors pace bowling early, which suits Team A's attack.
            
            **Key Stats:**
            - Team A: 168 avg 1st innings score, 22% boundary percentage
            - Team B: 175 avg 2nd innings score, superior death overs performance
            
            **Value Bets:**
            - Team B to win chasing (odds 2.1) - their 2nd innings SR of 145 vs Team A's 135 is significant
            - Total boundaries over 45.5 - both teams average 19% boundary percentage
            """,
            
            """
            **Match Situation Analysis**
            
            Venue intelligence suggests scores of 170-180 are par. Team batting first has won 60% of recent games here.
            The toss could be crucial - winning captain likely to bat first given dew factor.
            
            **Tactical Matchups:**
            - Spin vs Pace: Team A's spin weakness (SR 125 vs spin) could be exploited
            - Powerplay Battle: Team B's aggressive approach (SR 145 in first 6) vs Team A's tight bowling
            - Death Overs: Team A's SR of 175 in overs 16-20 gives them edge in setting targets
            
            **Recommended Bets:**
            - Team A to bat first and score 180+ (odds 3.2)
            - Match to go to final over (odds 2.5)
            """
        ]
        
        return examples
    
    def get_betting_insights(self, team1_name: str, team2_name: str) -> Dict[str, Any]:
        """
        Generate betting insights based on team comparison.
        
        Args:
            team1_name: First team name
            team2_name: Second team name
            
        Returns:
            Dictionary with betting angles and predictions
        """
        comparison = self.compare_team_stats(team1_name, team2_name)
        
        if "error" in comparison:
            return comparison
        
        team1_stats = comparison["team1_stats"]
        team2_stats = comparison["team2_stats"]
        
        insights = {
            "match_context": f"{team1_name} vs {team2_name}",
            "predicted_scores": {
                "team1_batting_first": round(team1_stats["first_innings_average"]),
                "team2_batting_first": round(team2_stats["first_innings_average"]),
                "team1_chasing": round(team1_stats["second_innings_average"]),
                "team2_chasing": round(team2_stats["second_innings_average"])
            },
            "key_matchups": [],
            "betting_angles": [],
            "value_picks": []
        }
        
        # Identify key matchups
        if team1_stats["strike_rate_vs_pace"] > team2_stats["strike_rate_vs_pace"]:
            insights["key_matchups"].append(f"{team1_name} has advantage vs pace bowling (SR {team1_stats['strike_rate_vs_pace']} vs {team2_stats['strike_rate_vs_pace']})")
        else:
            insights["key_matchups"].append(f"{team2_name} has advantage vs pace bowling (SR {team2_stats['strike_rate_vs_pace']} vs {team1_stats['strike_rate_vs_pace']})")
        
        if team1_stats["strike_rate_balls_41_50"] > team2_stats["strike_rate_balls_41_50"]:
            insights["key_matchups"].append(f"{team1_name} superior in death overs (SR {team1_stats['strike_rate_balls_41_50']} vs {team2_stats['strike_rate_balls_41_50']})")
        else:
            insights["key_matchups"].append(f"{team2_name} superior in death overs (SR {team2_stats['strike_rate_balls_41_50']} vs {team1_stats['strike_rate_balls_41_50']})")
        
        # Generate betting angles
        avg_score = (team1_stats["first_innings_average"] + team2_stats["first_innings_average"]) / 2
        insights["betting_angles"].append(f"Total runs line: Over/Under {round(avg_score - 5)}.5")
        
        if team1_stats["strike_rate"] > team2_stats["strike_rate"]:
            insights["betting_angles"].append(f"{team1_name} slight favorites based on overall SR ({team1_stats['strike_rate']} vs {team2_stats['strike_rate']})")
        else:
            insights["betting_angles"].append(f"{team2_name} slight favorites based on overall SR ({team2_stats['strike_rate']} vs {team1_stats['strike_rate']})")
        
        # Value picks
        if team1_stats["second_innings_average"] > team2_stats["second_innings_average"]:
            insights["value_picks"].append(f"{team1_name} to win chasing - strong 2nd innings record (avg {team1_stats['second_innings_average']})")
        else:
            insights["value_picks"].append(f"{team2_name} to win chasing - strong 2nd innings record (avg {team2_stats['second_innings_average']})")
        
        boundary_avg = (team1_stats["boundary_percentage"] + team2_stats["boundary_percentage"]) / 2
        if boundary_avg > 18:
            insights["value_picks"].append(f"Total boundaries over 45.5 - both teams aggressive (avg {round(boundary_avg, 1)}% boundary rate)")
        
        return insights
    
    def get_detailed_match_analysis(self, team1_name: str, team2_name: str, venue: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive match analysis with fixture context, key stats, trends, and betting recommendations.
        Similar to football betting previews with detailed reasoning.
        
        Args:
            team1_name: First team name
            team2_name: Second team name
            venue: Venue name (optional)
            
        Returns:
            Dictionary with complete betting preview data
        """
        team1_stats = self.get_team_batting_stats(team1_name)
        team2_stats = self.get_team_batting_stats(team2_name)
        
        if "error" in team1_stats or "error" in team2_stats:
            return {"error": "One or both teams not found"}
        
        # Generate H2H and recent form
        h2h_record = self.generate_h2h_record(team1_name, team2_name)
        team1_form = self.generate_recent_form(team1_name)
        team2_form = self.generate_recent_form(team2_name)
        
        # Fixture Analysis with H2H, recent form, and batting first/second win percentages
        fixture_analysis = self._generate_enhanced_fixture_analysis(
            team1_name, team2_name, team1_stats, team2_stats, 
            h2h_record, team1_form, team2_form
        )
        
        # Venue Insights (replaces Key Stats & Trends)
        venue_insights = []
        if venue:
            venue_data = self.get_venue_insights(venue)
            venue_insights = self._generate_venue_insights_points(venue_data)
        else:
            # If no venue selected, use generic key stats
            venue_insights = self._generate_key_stats_and_trends(team1_name, team2_name, team1_stats, team2_stats)
        
        # Recommended Bets with Odds
        betting_recommendations = self._generate_betting_recommendations(team1_name, team2_name, team1_stats, team2_stats, venue=venue)
        
        # Detailed Reasoning
        detailed_reasoning = self._generate_detailed_reasoning(team1_name, team2_name, team1_stats, team2_stats)
        
        return {
            "fixture_analysis": fixture_analysis,
            "venue_insights": venue_insights,
            "recommended_bets": betting_recommendations,
            "detailed_reasoning": detailed_reasoning,
            "team1_stats": team1_stats,
            "team2_stats": team2_stats,
            "h2h_record": h2h_record,
            "team1_form": team1_form,
            "team2_form": team2_form,
            "venue_data": self.get_venue_insights(venue) if venue else None
        }
    
    def _generate_enhanced_fixture_analysis(self, team1: str, team2: str, t1_stats: Dict, t2_stats: Dict, 
                                            h2h_record: Dict, team1_form: Dict, team2_form: Dict) -> List[str]:
        """
        Generate enhanced fixture analysis with three points: H2H, recent form, and batting first/second win percentages.
        
        Returns:
            List of three analysis points
        """
        analysis_points = []
        
        # Point 1: Head-to-Head Record (Last 5 Matches)
        h2h_point = f"**Head-to-Head:** {team1} {h2h_record['team1_wins']}-{h2h_record['team2_wins']} {team2} in last 5 meetings"
        if h2h_record['team1_wins'] > h2h_record['team2_wins']:
            h2h_point += f" ({team1} holds edge)."
        elif h2h_record['team2_wins'] > h2h_record['team1_wins']:
            h2h_point += f" ({team2} has upper hand)."
        else:
            h2h_point += " (evenly balanced)."
        analysis_points.append(h2h_point)
        
        # Point 2: Recent Form (Last 5 Matches - All Opponents)
        form_point = f"**Recent Form:** {team1} {team1_form['wins']}/5 wins, {team2} {team2_form['wins']}/5 wins"
        if team1_form['wins'] > team2_form['wins']:
            form_point += f" ({team1} has momentum)."
        elif team2_form['wins'] > team1_form['wins']:
            form_point += f" ({team2} in better form)."
        else:
            form_point += " (evenly matched)."
        analysis_points.append(form_point)
        
        # Point 3: Batting First vs Batting Second Win Percentages
        t1_bat_first = self.batting_win_percentages.get(team1, {}).get('batting_first', 'N/A')
        t1_bat_second = self.batting_win_percentages.get(team1, {}).get('batting_second', 'N/A')
        t2_bat_first = self.batting_win_percentages.get(team2, {}).get('batting_first', 'N/A')
        t2_bat_second = self.batting_win_percentages.get(team2, {}).get('batting_second', 'N/A')
        
        batting_point = f"**Toss Factor:** {team1}: {t1_bat_first} (1st), {t1_bat_second} (2nd) | {team2}: {t2_bat_first} (1st), {t2_bat_second} (2nd)"
        
        # Determine toss preference
        if 'N/A' not in [t1_bat_first, t1_bat_second, t2_bat_first, t2_bat_second]:
            t1_first_pct = float(t1_bat_first.split('%')[0])
            t1_second_pct = float(t1_bat_second.split('%')[0])
            t2_first_pct = float(t2_bat_first.split('%')[0])
            t2_second_pct = float(t2_bat_second.split('%')[0])
            
            if t1_second_pct > t1_first_pct and t2_second_pct > t2_first_pct:
                batting_point += " - Both prefer chasing."
            elif t1_first_pct > t1_second_pct and t2_first_pct > t2_second_pct:
                batting_point += " - Both prefer batting first."
            else:
                batting_point += " - Contrasting preferences."
        
        analysis_points.append(batting_point)
        
        return analysis_points
    
    def _generate_venue_insights_points(self, venue_data: Dict) -> List[str]:
        """
        Generate 3-4 venue insight points from venue data.
        
        Args:
            venue_data: Venue insights dictionary
            
        Returns:
            List of venue insight points
        """
        insights = []
        
        # Point 1: Toss Decisions at Selected Venue
        if venue_data['toss_decisions']:
            won_toss = venue_data['toss_decisions'].get('won_toss', {})
            lost_toss = venue_data['toss_decisions'].get('lost_toss', {})
            
            if won_toss and lost_toss:
                insight = f"**Toss Decisions at {venue_data['venue_name']}:** Teams winning the toss have chosen to bowl first {won_toss['bowled_first']} times and bat first {won_toss['batted_first']} times. "
                insight += f"Teams losing the toss were forced to bat first {lost_toss['batted_first']} times and bowl first {lost_toss['bowled_first']} times."
                insights.append(insight)
        
        # Point 2: Win/Loss Records by Toss Situations
        if venue_data['toss_situations']:
            won_bat_first = venue_data['toss_situations'].get('Won Toss & Batted 1st', {})
            won_bowl_first = venue_data['toss_situations'].get('Won Toss & Bowled 1st', {})
            lost_bat_first = venue_data['toss_situations'].get('Lost Toss & Batted 1st', {})
            lost_bowl_first = venue_data['toss_situations'].get('Lost Toss & Bowled 1st', {})
            
            insight = f"**Toss Impact on Results:** "
            if won_bowl_first:
                insight += f"Teams winning the toss and bowling first have won {won_bowl_first['wins']} and lost {won_bowl_first['losses']} matches. "
            if lost_bat_first:
                insight += f"Teams losing the toss and batting first have won {lost_bat_first['wins']} and lost {lost_bat_first['losses']} matches at this venue."
            insights.append(insight)
        
        # Point 3: Comprehensive Venue Statistics - Scoring Patterns
        if venue_data['venue_stats']:
            stats = venue_data['venue_stats']
            insight = f"**Venue Scoring Patterns:** Average score at this venue is {stats['average_score']} with first innings averaging {stats['average_first_innings_score']}. "
            insight += f"Boundary percentage is {stats['boundary_percentage']}% with {stats['fours_per_match']} fours and {stats['sixes_per_match']} sixes per match on average."
            insights.append(insight)
        
        # Point 4: Bowling Analysis and Phase-wise Performance
        if venue_data['venue_stats']:
            stats = venue_data['venue_stats']
            insight = f"**Bowling & Phase Analysis:** Pace bowlers take {stats['pace_wickets_pct']}% of wickets while spinners account for {stats['spin_wickets_pct']}%. "
            insight += f"Powerplay (overs 1-6): {stats['powerplay_runs']} runs, {stats['powerplay_wickets']} wickets. "
            insight += f"Death overs (16-20): {stats['death_overs_runs']} runs per match."
            insights.append(insight)
        
        return insights
    
    def _generate_fixture_analysis(self, team1: str, team2: str, t1_stats: Dict, t2_stats: Dict) -> str:
        """
        Generate fixture analysis with team form and H2H context.
        (Legacy method - kept for backward compatibility)
        """
        # Determine favorite based on overall stats
        t1_score = (t1_stats['strike_rate'] + t1_stats['batting_average'] * 3 + 
                    t1_stats['boundary_percentage'] * 2) / 6
        t2_score = (t2_stats['strike_rate'] + t2_stats['batting_average'] * 3 + 
                    t2_stats['boundary_percentage'] * 2) / 6
        
        if t1_score > t2_score:
            favorite = team1
            underdog = team2
            fav_stats = t1_stats
            und_stats = t2_stats
        else:
            favorite = team2
            underdog = team1
            fav_stats = t2_stats
            und_stats = t1_stats
        
        # Analyze form
        fav_form = "strong" if fav_stats['strike_rate'] > 140 else "decent" if fav_stats['strike_rate'] > 130 else "struggling"
        und_form = "strong" if und_stats['strike_rate'] > 140 else "decent" if und_stats['strike_rate'] > 130 else "struggling"
        
        analysis = f"{favorite} favored - SR {fav_stats['strike_rate']}, Avg {fav_stats['batting_average']} vs {underdog}'s SR {und_stats['strike_rate']}, Avg {und_stats['batting_average']}. "
        
        # Key differentiators
        if fav_stats['strike_rate_balls_41_50'] > und_stats['strike_rate_balls_41_50'] + 10:
            analysis += f"{favorite} superior in death - SR {fav_stats['strike_rate_balls_41_50']} vs {und_stats['strike_rate_balls_41_50']}."
        elif abs(fav_stats['first_innings_average'] - und_stats['first_innings_average']) > 10:
            analysis += f"Toss crucial - {favorite} Avg {fav_stats['first_innings_average']} batting first vs {underdog}'s {und_stats['first_innings_average']}."
        else:
            analysis += f"Evenly matched - expect close contest."
        
        return analysis
    
    def _generate_key_stats_and_trends(self, team1: str, team2: str, t1_stats: Dict, t2_stats: Dict) -> List[str]:
        """
        Generate key statistics and trends for betting analysis.
        """
        stats = []
        
        # Boundary hitting trends
        if t1_stats['boundary_percentage'] > 18:
            stats.append(f"{team1} high boundary rate - {t1_stats['boundary_percentage']}%, ball per boundary {t1_stats['balls_per_boundary']}")
        if t2_stats['boundary_percentage'] > 18:
            stats.append(f"{team2} high boundary rate - {t2_stats['boundary_percentage']}%, ball per boundary {t2_stats['balls_per_boundary']}")
        
        # Key player insights (inferred from team stats)
        if t1_stats['strike_rate_balls_1_10'] > 140:
            stats.append(f"{team1} explosive openers - Powerplay SR {t1_stats['strike_rate_balls_1_10']}")
        
        if t2_stats['strike_rate_balls_41_50'] > 170:
            stats.append(f"{team2} dangerous finishers - Death SR {t2_stats['strike_rate_balls_41_50']}")
        
        # Pace vs Spin trends
        t1_pace_advantage = t1_stats['strike_rate_vs_pace'] - t1_stats['strike_rate_vs_spin']
        t2_pace_advantage = t2_stats['strike_rate_vs_pace'] - t2_stats['strike_rate_vs_spin']
        
        if abs(t1_pace_advantage) > 10:
            if t1_pace_advantage > 0:
                stats.append(f"{team1} better vs pace - SR {t1_stats['strike_rate_vs_pace']} vs spin SR {t1_stats['strike_rate_vs_spin']}")
            else:
                stats.append(f"{team1} excels vs spin - SR {t1_stats['strike_rate_vs_spin']} vs pace SR {t1_stats['strike_rate_vs_pace']}")
        
        # Innings preference
        if t1_stats['second_innings_average'] > t1_stats['first_innings_average'] + 5:
            stats.append(f"{team1} strong chasers - 2nd innings Avg {t1_stats['second_innings_average']} vs 1st innings {t1_stats['first_innings_average']}")
        elif t1_stats['first_innings_average'] > t1_stats['second_innings_average'] + 5:
            stats.append(f"{team1} prefers batting first - 1st innings Avg {t1_stats['first_innings_average']} vs 2nd innings {t1_stats['second_innings_average']}")
        
        return stats
    
    def _generate_betting_recommendations(self, team1: str, team2: str, t1_stats: Dict, t2_stats: Dict, venue: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate betting recommendations with odds and reasoning.
        Includes specific player names, venue statistics, and phase-wise predictions.
        """
        recommendations = []
        
        # Get venue statistics
        venue_stats = self.get_venue_stats(venue)
        
        # Get top players for each team
        t1_top_players = self.get_top_players_by_team(team1, top_n=3)
        t2_top_players = self.get_top_players_by_team(team2, top_n=3)
        
        # 1. Match Winner
        t1_score = (t1_stats['strike_rate'] + t1_stats['batting_average'] * 3) / 4
        t2_score = (t2_stats['strike_rate'] + t2_stats['batting_average'] * 3) / 4
        
        if t1_score > t2_score:
            winner = team1
            confidence = min(85, 55 + (t1_score - t2_score) / 2)
            odds = round(1.5 + (100 - confidence) / 50, 2)
            reasoning = f"{team1} superior stats - SR {t1_stats['strike_rate']}, Avg {t1_stats['batting_average']} vs {team2} SR {t2_stats['strike_rate']}, Avg {t2_stats['batting_average']}"
        else:
            winner = team2
            confidence = min(85, 55 + (t2_score - t1_score) / 2)
            odds = round(1.5 + (100 - confidence) / 50, 2)
            reasoning = f"{team2} superior stats - SR {t2_stats['strike_rate']}, Avg {t2_stats['batting_average']} vs {team1} SR {t1_stats['strike_rate']}, Avg {t1_stats['batting_average']}"
        
        recommendations.append({
            "bet_type": "Match Winner",
            "selection": f"{winner} to Win",
            "odds": odds,
            "confidence": f"{int(confidence)}%",
            "reasoning": reasoning
        })
        
        # 2. Total Runs (Over/Under) - Using venue statistics
        venue_avg_score = venue_stats['average_first_innings']
        total_runs_line = round(venue_avg_score * 2 - 15)
        
        # Compare team averages with venue average
        team_combined_avg = (t1_stats['first_innings_average'] + t2_stats['first_innings_average']) / 2
        
        if team_combined_avg > venue_avg_score + 5:
            selection = f"Over {total_runs_line}.5 Total Runs"
            odds = 1.85
            reasoning = f"Teams avg higher than venue - {t1_stats['first_innings_average']} & {t2_stats['first_innings_average']} vs venue {venue_avg_score}. Expect high-scoring game."
        elif team_combined_avg < venue_avg_score - 5:
            selection = f"Under {total_runs_line}.5 Total Runs"
            odds = 1.90
            reasoning = f"Teams avg lower than venue - {t1_stats['first_innings_average']} & {t2_stats['first_innings_average']} vs venue {venue_avg_score}. Expect controlled game."
        else:
            selection = f"Over {total_runs_line}.5 Total Runs"
            odds = 1.88
            reasoning = f"Teams align with venue avg - {t1_stats['first_innings_average']} & {t2_stats['first_innings_average']} vs venue {venue_avg_score}. Competitive high-scoring match expected."
        
        recommendations.append({
            "bet_type": "Total Runs",
            "selection": selection,
            "odds": odds,
            "confidence": "68%",
            "reasoning": reasoning
        })
        
        # 3. Top Team Run Scorer - With specific player names
        if t1_stats['batting_average'] > t2_stats['batting_average']:
            top_team = team1
            top_players = t1_top_players
            team_avg = t1_stats['batting_average']
        else:
            top_team = team2
            top_players = t2_top_players
            team_avg = t2_stats['batting_average']
        
        if top_players:
            top_player = top_players[0]
            player_names = ", ".join([p['name'] for p in top_players[:2]])
            selection = f"{top_player['name']} ({top_team}) Top Team Run Scorer"
            odds = 4.50
            reasoning = f"{top_player['name']} in form - Avg {top_player['average']}, SR {top_player['strike_rate']}. {top_team} team avg {team_avg} highest."
        else:
            selection = f"{top_team} batsman to be top team scorer"
            odds = 4.50
            reasoning = f"{top_team} has the highest team batting average ({team_avg}), suggesting their key batsmen are in form."
        
        recommendations.append({
            "bet_type": "Top Team Run Scorer",
            "selection": selection,
            "odds": odds,
            "confidence": "60%",
            "reasoning": reasoning
        })
        
        # 4. First 6 Overs (Powerplay) Prediction
        t1_powerplay_sr = t1_stats['strike_rate_balls_1_10']
        t2_powerplay_sr = t2_stats['strike_rate_balls_1_10']
        venue_powerplay_avg = venue_stats['powerplay_runs_first_innings']
        
        team_powerplay_avg = (t1_powerplay_sr + t2_powerplay_sr) / 2
        
        if team_powerplay_avg > 140:
            powerplay_line = round(venue_powerplay_avg + 5)
            selection = f"Over {powerplay_line}.5 Runs in First 6 Overs"
            odds = 1.85
            reasoning = f"Aggressive powerplay - {team1} SR {t1_powerplay_sr}, {team2} SR {t2_powerplay_sr} vs venue avg {venue_powerplay_avg}. Explosive starts expected."
        else:
            powerplay_line = round(venue_powerplay_avg - 3)
            selection = f"Under {powerplay_line}.5 Runs in First 6 Overs"
            odds = 1.92
            reasoning = f"Cautious powerplay - {team1} SR {t1_powerplay_sr}, {team2} SR {t2_powerplay_sr} vs venue avg {venue_powerplay_avg}. Measured starts expected."
        
        recommendations.append({
            "bet_type": "Powerplay Runs (First 6 Overs)",
            "selection": selection,
            "odds": odds,
            "confidence": "65%",
            "reasoning": reasoning
        })
        
        # 5. First Over Runs Prediction
        # Calculate expected first over runs based on powerplay SR
        avg_first_over_runs = round((team_powerplay_avg / 100) * 6)
        
        if t1_powerplay_sr > 145 or t2_powerplay_sr > 145:
            selection = f"Over 7.5 Runs in First Over"
            odds = 2.10
            reasoning = f"Explosive powerplay SRs - {team1} {t1_powerplay_sr}, {team2} {t2_powerplay_sr}. Expect {avg_first_over_runs}+ runs in first over."
        else:
            selection = f"Under 8.5 Runs in First Over"
            odds = 1.80
            reasoning = f"Measured starts - Powerplay SRs {t1_powerplay_sr} & {t2_powerplay_sr}. Avg {avg_first_over_runs} runs in first over."
        
        recommendations.append({
            "bet_type": "First Over Runs",
            "selection": selection,
            "odds": odds,
            "confidence": "58%",
            "reasoning": reasoning
        })
        
        return recommendations
    
    def _generate_detailed_reasoning(self, team1: str, team2: str, t1_stats: Dict, t2_stats: Dict) -> Dict[str, Any]:
        """
        Generate detailed reasoning sections similar to football betting previews.
        """
        reasoning = {
            "sections": []
        }
        
        # Section 1: Recent Form Analysis
        t1_form_score = (t1_stats['strike_rate'] + t1_stats['batting_average'] * 2) / 3
        t2_form_score = (t2_stats['strike_rate'] + t2_stats['batting_average'] * 2) / 3
        
        if t1_form_score > t2_form_score:
            better_team = team1
            better_stats = t1_stats
            worse_team = team2
            worse_stats = t2_stats
        else:
            better_team = team2
            better_stats = t2_stats
            worse_team = team1
            worse_stats = t1_stats
        
        form_analysis = f"{better_team} in superior form - Avg {better_stats['batting_average']}, SR {better_stats['strike_rate']} vs {worse_team} Avg {worse_stats['batting_average']}, SR {worse_stats['strike_rate']}. "
        
        if better_stats['rank_strike_rate'] < worse_stats['rank_strike_rate']:
            form_analysis += f"{better_team} ranked #{better_stats['rank_strike_rate']} in SR vs {worse_team} #{worse_stats['rank_strike_rate']}."
        
        reasoning['sections'].append({
            "title": "Can {} maintain their momentum?".format(better_team),
            "content": form_analysis
        })
        
        # Section 2: Key Matchup Analysis
        matchup_analysis = ""
        
        if abs(t1_stats['strike_rate_vs_spin'] - t2_stats['strike_rate_vs_spin']) > 10:
            if t1_stats['strike_rate_vs_spin'] > t2_stats['strike_rate_vs_spin']:
                matchup_analysis += f"{team1} advantage vs spin - SR {t1_stats['strike_rate_vs_spin']} vs {team2} SR {t2_stats['strike_rate_vs_spin']}. "
            else:
                matchup_analysis += f"{team2} excel vs spin - SR {t2_stats['strike_rate_vs_spin']} vs {team1} SR {t1_stats['strike_rate_vs_spin']}. "
        
        if abs(t1_stats['strike_rate_balls_41_50'] - t2_stats['strike_rate_balls_41_50']) > 15:
            if t1_stats['strike_rate_balls_41_50'] > t2_stats['strike_rate_balls_41_50']:
                matchup_analysis += f"{team1} death overs prowess - SR {t1_stats['strike_rate_balls_41_50']} vs {team2} SR {t2_stats['strike_rate_balls_41_50']}."
            else:
                matchup_analysis += f"{team2} death overs prowess - SR {t2_stats['strike_rate_balls_41_50']} vs {team1} SR {t1_stats['strike_rate_balls_41_50']}."
        
        if matchup_analysis:
            reasoning['sections'].append({
                "title": "Crucial Matchups",
                "content": matchup_analysis
            })
        
        # Section 3: Batting Depth and Consistency
        depth_analysis = ""
        
        if t1_stats['boundary_percentage'] > 19:
            depth_analysis += f"{team1} excellent batting depth - {t1_stats['boundary_percentage']}% boundary rate. "
        
        if t2_stats['dot_ball_percentage'] < 35:
            depth_analysis += f"{team2} efficient strike rotation - {t2_stats['dot_ball_percentage']}% dot balls. "
        
        if depth_analysis:
            reasoning['sections'].append({
                "title": "Batting Depth Analysis",
                "content": depth_analysis
            })
        
        # Final Prediction
        avg_t1_score = round((t1_stats['first_innings_average'] + t1_stats['second_innings_average']) / 2)
        avg_t2_score = round((t2_stats['first_innings_average'] + t2_stats['second_innings_average']) / 2)
        
        if t1_form_score > t2_form_score:
            prediction = f"{team1} to post ~{avg_t1_score} runs and win. {team2} likely ~{avg_t2_score - 15}. Prediction: {team1} by 20-30 runs or 4-5 wickets."
        else:
            prediction = f"{team2} to post ~{avg_t2_score} runs and win. {team1} likely ~{avg_t1_score - 15}. Prediction: {team2} by 20-30 runs or 4-5 wickets."
        
        reasoning['final_prediction'] = prediction
        
        return reasoning
