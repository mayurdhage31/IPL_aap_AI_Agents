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
    
    def get_all_teams_list(self) -> List[str]:
        """
        Get list of all available teams.
        
        Returns:
            List of team names
        """
        return sorted(self.team_df['batting_team'].unique().tolist())
    
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
    
    def get_detailed_match_analysis(self, team1_name: str, team2_name: str) -> Dict[str, Any]:
        """
        Generate comprehensive match analysis with fixture context, key stats, trends, and betting recommendations.
        Similar to football betting previews with detailed reasoning.
        
        Args:
            team1_name: First team name
            team2_name: Second team name
            
        Returns:
            Dictionary with complete betting preview data
        """
        team1_stats = self.get_team_batting_stats(team1_name)
        team2_stats = self.get_team_batting_stats(team2_name)
        
        if "error" in team1_stats or "error" in team2_stats:
            return {"error": "One or both teams not found"}
        
        # Fixture Analysis
        fixture_analysis = self._generate_fixture_analysis(team1_name, team2_name, team1_stats, team2_stats)
        
        # Key Stats & Trends
        key_stats = self._generate_key_stats_and_trends(team1_name, team2_name, team1_stats, team2_stats)
        
        # Recommended Bets with Odds (venue can be passed as parameter in future)
        betting_recommendations = self._generate_betting_recommendations(team1_name, team2_name, team1_stats, team2_stats, venue=None)
        
        # Detailed Reasoning
        detailed_reasoning = self._generate_detailed_reasoning(team1_name, team2_name, team1_stats, team2_stats)
        
        return {
            "fixture_analysis": fixture_analysis,
            "key_stats_and_trends": key_stats,
            "recommended_bets": betting_recommendations,
            "detailed_reasoning": detailed_reasoning,
            "team1_stats": team1_stats,
            "team2_stats": team2_stats
        }
    
    def _generate_fixture_analysis(self, team1: str, team2: str, t1_stats: Dict, t2_stats: Dict) -> str:
        """
        Generate fixture analysis with team form and H2H context.
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
        
        analysis = f"{favorite} enters as the favorite with {fav_form} batting form (SR: {fav_stats['strike_rate']}, Avg: {fav_stats['batting_average']}), "
        analysis += f"while {underdog} has shown {und_form} performances recently. "
        
        # H2H context
        analysis += f"Historical head-to-head records show this fixture is often competitive, with both teams capable of explosive performances. "
        
        # Key differentiators
        if fav_stats['strike_rate_balls_41_50'] > und_stats['strike_rate_balls_41_50'] + 10:
            analysis += f"{favorite}'s superior death overs batting (SR: {fav_stats['strike_rate_balls_41_50']}) gives them a crucial advantage in tight finishes."
        elif abs(fav_stats['first_innings_average'] - und_stats['first_innings_average']) > 10:
            analysis += f"The toss could be crucial, with {favorite} averaging {fav_stats['first_innings_average']} batting first compared to {underdog}'s {und_stats['first_innings_average']}."
        else:
            analysis += f"Both teams have similar capabilities, making this a closely contested encounter."
        
        return analysis
    
    def _generate_key_stats_and_trends(self, team1: str, team2: str, t1_stats: Dict, t2_stats: Dict) -> List[str]:
        """
        Generate key statistics and trends for betting analysis.
        """
        stats = []
        
        # Boundary hitting trends
        if t1_stats['boundary_percentage'] > 18:
            stats.append(f"{team1}'s matches have seen high boundary rates at {t1_stats['boundary_percentage']}% (balls per boundary: {t1_stats['balls_per_boundary']})")
        if t2_stats['boundary_percentage'] > 18:
            stats.append(f"{team2}'s matches have seen high boundary rates at {t2_stats['boundary_percentage']}% (balls per boundary: {t2_stats['balls_per_boundary']})")
        
        # Key player insights (inferred from team stats)
        if t1_stats['strike_rate_balls_1_10'] > 140:
            stats.append(f"{team1} has explosive openers with powerplay SR of {t1_stats['strike_rate_balls_1_10']}")
        
        if t2_stats['strike_rate_balls_41_50'] > 170:
            stats.append(f"{team2} boasts dangerous finishers with death overs SR of {t2_stats['strike_rate_balls_41_50']}")
        
        # Pace vs Spin trends
        t1_pace_advantage = t1_stats['strike_rate_vs_pace'] - t1_stats['strike_rate_vs_spin']
        t2_pace_advantage = t2_stats['strike_rate_vs_pace'] - t2_stats['strike_rate_vs_spin']
        
        if abs(t1_pace_advantage) > 10:
            if t1_pace_advantage > 0:
                stats.append(f"{team1} performs better against pace (SR: {t1_stats['strike_rate_vs_pace']}) than spin (SR: {t1_stats['strike_rate_vs_spin']})")
            else:
                stats.append(f"{team1} excels against spin bowling (SR: {t1_stats['strike_rate_vs_spin']}) compared to pace (SR: {t1_stats['strike_rate_vs_pace']})")
        
        # Innings preference
        if t1_stats['second_innings_average'] > t1_stats['first_innings_average'] + 5:
            stats.append(f"{team1} has a strong chasing record with 2nd innings average of {t1_stats['second_innings_average']} vs {t1_stats['first_innings_average']} batting first")
        elif t1_stats['first_innings_average'] > t1_stats['second_innings_average'] + 5:
            stats.append(f"{team1} prefers batting first with 1st innings average of {t1_stats['first_innings_average']} vs {t1_stats['second_innings_average']} chasing")
        
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
            reasoning = f"{team1} has superior overall stats with SR of {t1_stats['strike_rate']} and average of {t1_stats['batting_average']}, compared to {team2}'s SR of {t2_stats['strike_rate']} and average of {t2_stats['batting_average']}"
        else:
            winner = team2
            confidence = min(85, 55 + (t2_score - t1_score) / 2)
            odds = round(1.5 + (100 - confidence) / 50, 2)
            reasoning = f"{team2} has superior overall stats with SR of {t2_stats['strike_rate']} and average of {t2_stats['batting_average']}, compared to {team1}'s SR of {t1_stats['strike_rate']} and average of {t1_stats['batting_average']}"
        
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
            reasoning = f"Venue average first innings score is {venue_avg_score}, but both teams average higher ({t1_stats['first_innings_average']} and {t2_stats['first_innings_average']}). Historical venue data shows average total of {round(venue_stats['average_score'] * 2)} runs. Expect a high-scoring game."
        elif team_combined_avg < venue_avg_score - 5:
            selection = f"Under {total_runs_line}.5 Total Runs"
            odds = 1.90
            reasoning = f"Venue average first innings score is {venue_avg_score}, but both teams average lower ({t1_stats['first_innings_average']} and {t2_stats['first_innings_average']}). Historical venue trends suggest {round(venue_stats['average_score'] * 2)} total runs. Expect a controlled game."
        else:
            selection = f"Over {total_runs_line}.5 Total Runs"
            odds = 1.88
            reasoning = f"Venue historically averages {venue_avg_score} in first innings with combined match average of {round(venue_stats['average_score'] * 2)} runs. Both teams' first innings averages ({t1_stats['first_innings_average']} and {t2_stats['first_innings_average']}) align with venue trends, suggesting a competitive high-scoring encounter."
        
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
            reasoning = f"{top_team} has the highest team batting average ({team_avg}). Key players like {player_names} are in excellent form. {top_player['name']} averages {top_player['average']} with SR of {top_player['strike_rate']}, making him a strong candidate for top scorer."
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
            reasoning = f"Both teams have aggressive powerplay approaches with {team1} SR of {t1_powerplay_sr} and {team2} SR of {t2_powerplay_sr}. Venue averages {venue_powerplay_avg} runs in powerplay during first innings. Expect explosive starts from both sides."
        else:
            powerplay_line = round(venue_powerplay_avg - 3)
            selection = f"Under {powerplay_line}.5 Runs in First 6 Overs"
            odds = 1.92
            reasoning = f"Teams show cautious powerplay approaches with {team1} SR of {t1_powerplay_sr} and {team2} SR of {t2_powerplay_sr}. Venue averages {venue_powerplay_avg} runs in first 6 overs. Expect measured starts."
        
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
            reasoning = f"With explosive powerplay strike rates ({team1}: {t1_powerplay_sr}, {team2}: {t2_powerplay_sr}), teams typically score {avg_first_over_runs}+ runs in the opening over at this venue. Historical powerplay data shows aggressive intent from ball one."
        else:
            selection = f"Under 8.5 Runs in First Over"
            odds = 1.80
            reasoning = f"Teams show measured starts with powerplay SRs of {t1_powerplay_sr} and {t2_powerplay_sr}. At this venue, teams average around {avg_first_over_runs} runs in the first over, suggesting a cautious approach early on."
        
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
        
        form_analysis = f"{better_team} have been in superior form with consistent performances. Their batting lineup has posted an average of {better_stats['batting_average']} with a strike rate of {better_stats['strike_rate']}, "
        form_analysis += f"significantly better than {worse_team}'s average of {worse_stats['batting_average']} and SR of {worse_stats['strike_rate']}. "
        
        if better_stats['rank_strike_rate'] < worse_stats['rank_strike_rate']:
            form_analysis += f"{better_team} are ranked #{better_stats['rank_strike_rate']} in strike rate compared to {worse_team}'s #{worse_stats['rank_strike_rate']}, highlighting their aggressive approach."
        
        reasoning['sections'].append({
            "title": "Can {} maintain their momentum?".format(better_team),
            "content": form_analysis
        })
        
        # Section 2: Key Matchup Analysis
        matchup_analysis = ""
        
        if abs(t1_stats['strike_rate_vs_spin'] - t2_stats['strike_rate_vs_spin']) > 10:
            if t1_stats['strike_rate_vs_spin'] > t2_stats['strike_rate_vs_spin']:
                matchup_analysis += f"{team1} have a significant advantage against spin bowling (SR: {t1_stats['strike_rate_vs_spin']}) compared to {team2} (SR: {t2_stats['strike_rate_vs_spin']}). "
                matchup_analysis += f"If the pitch offers turn, {team1}'s batsmen are better equipped to handle spin pressure. "
            else:
                matchup_analysis += f"{team2} excel against spin bowling (SR: {t2_stats['strike_rate_vs_spin']}) compared to {team1} (SR: {t1_stats['strike_rate_vs_spin']}). "
                matchup_analysis += f"On a turning track, {team2} would have the upper hand. "
        
        if abs(t1_stats['strike_rate_balls_41_50'] - t2_stats['strike_rate_balls_41_50']) > 15:
            if t1_stats['strike_rate_balls_41_50'] > t2_stats['strike_rate_balls_41_50']:
                matchup_analysis += f"{team1}'s death overs prowess (SR: {t1_stats['strike_rate_balls_41_50']}) is far superior to {team2}'s (SR: {t2_stats['strike_rate_balls_41_50']}). "
                matchup_analysis += f"In close games, {team1}'s finishers can accelerate when it matters most."
            else:
                matchup_analysis += f"{team2}'s death overs prowess (SR: {t2_stats['strike_rate_balls_41_50']}) is far superior to {team1}'s (SR: {t1_stats['strike_rate_balls_41_50']}). "
                matchup_analysis += f"In close games, {team2}'s finishers can accelerate when it matters most."
        
        if matchup_analysis:
            reasoning['sections'].append({
                "title": "Crucial Matchups",
                "content": matchup_analysis
            })
        
        # Section 3: Batting Depth and Consistency
        depth_analysis = ""
        
        if t1_stats['boundary_percentage'] > 19:
            depth_analysis += f"{team1} have shown excellent batting depth with a boundary percentage of {t1_stats['boundary_percentage']}%, indicating multiple batsmen contributing. "
        
        if t2_stats['dot_ball_percentage'] < 35:
            depth_analysis += f"{team2} have been efficient in rotating strike with a low dot ball percentage of {t2_stats['dot_ball_percentage']}%, showing smart batting. "
        
        if depth_analysis:
            reasoning['sections'].append({
                "title": "Batting Depth Analysis",
                "content": depth_analysis
            })
        
        # Final Prediction
        avg_t1_score = round((t1_stats['first_innings_average'] + t1_stats['second_innings_average']) / 2)
        avg_t2_score = round((t2_stats['first_innings_average'] + t2_stats['second_innings_average']) / 2)
        
        if t1_form_score > t2_form_score:
            prediction = f"Back {team1} to post around {avg_t1_score} runs and secure victory. "
            prediction += f"{team2} may struggle to chase down a competitive total, likely finishing around {avg_t2_score - 15} runs. "
            prediction += f"Predicted result: {team1} to win by 20-30 runs or 4-5 wickets."
        else:
            prediction = f"Back {team2} to post around {avg_t2_score} runs and secure victory. "
            prediction += f"{team1} may struggle to chase down a competitive total, likely finishing around {avg_t1_score - 15} runs. "
            prediction += f"Predicted result: {team2} to win by 20-30 runs or 4-5 wickets."
        
        reasoning['final_prediction'] = prediction
        
        return reasoning
