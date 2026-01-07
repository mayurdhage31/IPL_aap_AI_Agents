import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class FantasyAnalysisTools:
    """
    Fantasy cricket analysis tools for IPL.
    Provides venue intelligence, match situation analysis, and fantasy team recommendations.
    """
    
    def __init__(self):
        """Initialize and load all fantasy-related datasets."""
        self.batting_df = pd.read_csv('data/IPL_21_24_Batting.csv')
        self.team_batting_df = pd.read_csv('data/IPL_Team_BattingData_21_24.csv')
        self.venue_df = pd.read_csv('data/IPL_Venue_details.csv')
        self.batsman_venue_df = pd.read_csv('data/Batsmanvsvenue.csv')
        self.fantasy_df = pd.read_csv('data/IPL_FantasyData.csv')
        
        for df in [self.batting_df, self.team_batting_df, self.venue_df, 
                   self.batsman_venue_df, self.fantasy_df]:
            df.columns = df.columns.str.strip()
    
    def get_available_teams(self) -> List[str]:
        """
        Get list of all available IPL teams.
        
        Returns:
            List of team names
        """
        teams = self.team_batting_df['batting_team'].unique().tolist()
        return sorted(teams)
    
    def get_venue_intelligence(self, team1: str, team2: str) -> Dict[str, Any]:
        """
        Analyze venue conditions and identify specialists.
        
        Args:
            team1: First team name
            team2: Second team name
            
        Returns:
            Dictionary with venue analysis including pace/spin bias and top performers
        """
        venues_analysis = []
        
        for _, venue_row in self.venue_df.head(10).iterrows():
            venue_name = venue_row['venue']
            city = venue_row.get('city', 'Unknown')
            pace_pct = float(venue_row.get('Pace_Wicket_Percentage', 50))
            spin_pct = float(venue_row.get('Spin_Wicket_Percentage', 50))
            
            if pace_pct > 60:
                bias_type = "Pace-Dominant"
                fantasy_tip = "Pick fast bowlers and pace-hitters"
            elif spin_pct > 50:
                bias_type = "Spin-Heavy"
                fantasy_tip = "Load up on spinners and spin-players"
            else:
                bias_type = "Balanced"
                fantasy_tip = "Balanced team composition works best"
            
            venue_specialists = self.batsman_venue_df[
                self.batsman_venue_df['venue'].str.strip() == venue_name.strip()
            ].copy()
            
            if not venue_specialists.empty:
                venue_specialists['TotalBatsmenRuns_Venue'] = pd.to_numeric(
                    venue_specialists['TotalBatsmenRuns_Venue'], errors='coerce'
                )
                venue_specialists['BattingAverage_Venue'] = pd.to_numeric(
                    venue_specialists['BattingAverage_Venue'], errors='coerce'
                )
                venue_specialists['BattingStrikeRate_Venue'] = pd.to_numeric(
                    venue_specialists['BattingStrikeRate_Venue'], errors='coerce'
                )
                
                venue_specialists = venue_specialists.dropna(
                    subset=['TotalBatsmenRuns_Venue', 'BattingAverage_Venue', 'BattingStrikeRate_Venue']
                )
                
                top_specialists = venue_specialists.nlargest(3, 'TotalBatsmenRuns_Venue')
                
                specialists_list = []
                for _, spec in top_specialists.iterrows():
                    specialists_list.append({
                        "player": spec['BatsmanName'],
                        "runs": int(spec['TotalBatsmenRuns_Venue']),
                        "average": round(float(spec['BattingAverage_Venue']), 2),
                        "strike_rate": round(float(spec['BattingStrikeRate_Venue']), 2)
                    })
            else:
                specialists_list = []
            
            venues_analysis.append({
                "venue": venue_name,
                "city": city,
                "pace_percentage": round(pace_pct, 1),
                "spin_percentage": round(spin_pct, 1),
                "bias_type": bias_type,
                "fantasy_tip": fantasy_tip,
                "top_specialists": specialists_list
            })
        
        return {
            "total_venues": len(venues_analysis),
            "venues": venues_analysis[:3],
            "recommendation": f"Analyze venue conditions before finalizing team. Pace-dominant venues favor fast bowlers."
        }
    
    def get_match_situation_edge(self, team1: str, team2: str) -> Dict[str, Any]:
        """
        Analyze match situation advantages (toss, innings preference).
        
        Args:
            team1: First team name
            team2: Second team name
            
        Returns:
            Dictionary with toss preference and innings-wise performance
        """
        team1_data = self.team_batting_df[
            self.team_batting_df['batting_team'].str.strip() == team1.strip()
        ]
        team2_data = self.team_batting_df[
            self.team_batting_df['batting_team'].str.strip() == team2.strip()
        ]
        
        def analyze_team(team_data, team_name):
            if team_data.empty:
                return {
                    "team": team_name,
                    "first_innings_sr": 0,
                    "second_innings_sr": 0,
                    "first_innings_avg": 0,
                    "second_innings_avg": 0,
                    "toss_preference": "Unknown",
                    "death_overs_sr": 0
                }
            
            row = team_data.iloc[0]
            
            def clean_numeric(value):
                """Clean numeric values by removing %, ?, and other non-numeric characters."""
                if pd.isna(value):
                    return 0
                if isinstance(value, (int, float)):
                    return float(value)
                cleaned = str(value).replace('%', '').replace('?', '').strip()
                try:
                    return float(cleaned)
                except (ValueError, TypeError):
                    return 0
            
            first_sr = clean_numeric(row.get('strike_rate_1st_innings', 0))
            second_sr = clean_numeric(row.get('strike_rate_2nd_innings', 0))
            first_avg = clean_numeric(row.get('First.Innings.Average', 0))
            second_avg = clean_numeric(row.get('Second.Innings.Average', 0))
            death_sr = clean_numeric(row.get('strike_rate_balls_41_50', 0))
            
            sr_diff = first_sr - second_sr
            
            if abs(sr_diff) > 5:
                if sr_diff > 0:
                    toss_pref = "Bat First"
                    reason = f"Better SR batting first ({first_sr:.1f} vs {second_sr:.1f})"
                else:
                    toss_pref = "Chase"
                    reason = f"Better SR chasing ({second_sr:.1f} vs {first_sr:.1f})"
            else:
                toss_pref = "Flexible"
                reason = f"Similar performance in both innings (SR diff: {abs(sr_diff):.1f})"
            
            return {
                "team": team_name,
                "first_innings_sr": round(first_sr, 1),
                "second_innings_sr": round(second_sr, 1),
                "first_innings_avg": round(first_avg, 1),
                "second_innings_avg": round(second_avg, 1),
                "toss_preference": toss_pref,
                "preference_reason": reason,
                "death_overs_sr": round(death_sr, 1)
            }
        
        team1_analysis = analyze_team(team1_data, team1)
        team2_analysis = analyze_team(team2_data, team2)
        
        insights = []
        
        if team1_analysis['death_overs_sr'] > 170:
            insights.append(f"{team1} has explosive death overs (SR: {team1_analysis['death_overs_sr']}) - pick their finishers")
        
        if team2_analysis['death_overs_sr'] > 170:
            insights.append(f"{team2} has explosive death overs (SR: {team2_analysis['death_overs_sr']}) - pick their finishers")
        
        if team1_analysis['toss_preference'] == "Bat First" and team2_analysis['toss_preference'] == "Chase":
            insights.append("Contrasting toss preferences - match situation will favor one team")
        
        if not insights:
            insights.append("Both teams show balanced performance across innings")
        
        return {
            "team1_analysis": team1_analysis,
            "team2_analysis": team2_analysis,
            "key_insights": insights,
            "fantasy_advice": "Consider toss result and team batting order when finalizing captain/vice-captain"
        }
    
    def get_fantasy_picks(self, team1: str, team2: str) -> Dict[str, Any]:
        """
        Generate fantasy team recommendations with anchor and risk picks.
        
        Args:
            team1: First team name
            team2: Second team name
            
        Returns:
            Dictionary with anchor picks, risk picks, and example XI
        """
        team1_players = self.fantasy_df[
            self.fantasy_df['Current_Team'].str.strip() == team1.strip()
        ].copy()
        team2_players = self.fantasy_df[
            self.fantasy_df['Current_Team'].str.strip() == team2.strip()
        ].copy()
        
        all_players = pd.concat([team1_players, team2_players], ignore_index=True)
        
        if all_players.empty:
            all_players = self.fantasy_df.copy()
        
        for col in ['Consistency_Rating', 'ceiling_average', 'Total_FP', 'Upside_Score', 'Risk.Rating']:
            if col in all_players.columns:
                all_players[col] = pd.to_numeric(all_players[col], errors='coerce')
        
        all_players = all_players.dropna(subset=['Consistency_Rating', 'ceiling_average'])
        
        anchor_picks = all_players[
            (all_players['Consistency_Rating'] >= 60) & 
            (all_players['ceiling_average'] >= 50)
        ].nlargest(3, 'Total_FP')
        
        anchor_list = []
        anchor_player_names = set()
        for _, player in anchor_picks.iterrows():
            anchor_player_names.add(player['fullName'])
            anchor_list.append({
                "player": player['fullName'],
                "team": player['Current_Team'],
                "position": player['position'],
                "consistency": round(float(player['Consistency_Rating']), 1),
                "ceiling": round(float(player['ceiling_average']), 1),
                "total_fp": round(float(player['Total_FP']), 1),
                "why_pick": f"High consistency ({player['Consistency_Rating']:.0f}) with strong ceiling ({player['ceiling_average']:.0f})"
            })
        
        risk_candidates = all_players[
            (~all_players['fullName'].isin(anchor_player_names)) & 
            (all_players['Risk.Rating'] > 60)
        ].nlargest(2, 'Upside_Score')
        
        risk_list = []
        for _, player in risk_candidates.iterrows():
            risk_list.append({
                "player": player['fullName'],
                "team": player['Current_Team'],
                "position": player['position'],
                "upside": round(float(player['Upside_Score']), 1),
                "risk": round(float(player['Risk.Rating']), 1),
                "total_fp": round(float(player['Total_FP']), 1),
                "why_pick": f"High upside potential ({player['Upside_Score']:.0f}) - differential pick"
            })
        
        wk_players = all_players[all_players['position'] == 'Wicket-Keeper'].nlargest(1, 'Total_FP')
        bat_players = all_players[all_players['position'] == 'Batsman'].nlargest(4, 'Total_FP')
        all_players_pos = all_players[all_players['position'] == 'Allrounder'].nlargest(3, 'Total_FP')
        bowl_players = all_players[all_players['position'] == 'Bowler'].nlargest(3, 'Total_FP')
        
        example_xi = {
            "wicket_keepers": [p['fullName'] for _, p in wk_players.iterrows()],
            "batsmen": [p['fullName'] for _, p in bat_players.iterrows()],
            "allrounders": [p['fullName'] for _, p in all_players_pos.iterrows()],
            "bowlers": [p['fullName'] for _, p in bowl_players.iterrows()]
        }
        
        total_players = (len(example_xi['wicket_keepers']) + len(example_xi['batsmen']) + 
                        len(example_xi['allrounders']) + len(example_xi['bowlers']))
        
        return {
            "anchor_picks": anchor_list,
            "risk_picks": risk_list,
            "example_xi": example_xi,
            "team_composition": f"{len(example_xi['wicket_keepers'])} WK, {len(example_xi['batsmen'])} BAT, {len(example_xi['allrounders'])} ALL, {len(example_xi['bowlers'])} BOWL",
            "strategy_note": "Anchor picks for consistency, risk picks for differentiation. Adjust based on venue and match situation."
        }
    
    def get_complete_fantasy_analysis(self, team1: str, team2: str) -> Dict[str, Any]:
        """
        Get comprehensive fantasy analysis combining all tools.
        
        Args:
            team1: First team name
            team2: Second team name
            
        Returns:
            Complete fantasy analysis dictionary
        """
        return {
            "venue_intelligence": self.get_venue_intelligence(team1, team2),
            "match_situation": self.get_match_situation_edge(team1, team2),
            "fantasy_picks": self.get_fantasy_picks(team1, team2)
        }
