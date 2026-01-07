import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class EnhancedCricketAnalysisTools:
    """
    Comprehensive cricket analysis tools for IPL player statistics.
    Provides detailed batting analysis including line/length, wagon wheel, and performance metrics.
    """
    
    def __init__(self):
        """Initialize and load all cricket datasets."""
        self.batting_df = pd.read_csv('IPL_21_24_Batting.csv')
        self.line_length_df = pd.read_csv('data/batter_line_length_SR_long.csv')
        self.wagon_wheel_df = pd.read_csv('data/Batter_WagonWheel.csv')
        
        self.batting_df.columns = self.batting_df.columns.str.strip()
        self.line_length_df.columns = self.line_length_df.columns.str.strip()
        self.wagon_wheel_df.columns = self.wagon_wheel_df.columns.str.strip()
        
        if 'Batter_Name' in self.line_length_df.columns:
            self.line_length_df.rename(columns={'Batter_Name': 'Batter'}, inplace=True)
        if 'batter' in self.line_length_df.columns:
            self.line_length_df.rename(columns={'batter': 'Batter'}, inplace=True)
        
        if 'Batter_Name' in self.wagon_wheel_df.columns:
            self.wagon_wheel_df.rename(columns={'Batter_Name': 'Batter'}, inplace=True)
        if 'field_zone' in self.wagon_wheel_df.columns:
            self.wagon_wheel_df.rename(columns={'field_zone': 'Zone'}, inplace=True)
        if 'n_boundaries' in self.wagon_wheel_df.columns:
            self.wagon_wheel_df.rename(columns={'n_boundaries': 'Boundaries'}, inplace=True)
            
        if 'line_bin' in self.line_length_df.columns:
            self.line_length_df.rename(columns={'line_bin': 'Line'}, inplace=True)
        if 'length_bin' in self.line_length_df.columns:
            self.line_length_df.rename(columns={'length_bin': 'Length'}, inplace=True)
            
        if 'SR' not in self.line_length_df.columns and 'Strike_Rate' in self.line_length_df.columns:
            self.line_length_df.rename(columns={'Strike_Rate': 'SR'}, inplace=True)
    
    def get_all_players_list(self) -> List[str]:
        """
        Get list of all available players.
        
        Returns:
            List of player names sorted alphabetically
        """
        return sorted(self.batting_df['Player'].unique().tolist())
    
    def get_player_stats(self, player_name: str) -> Dict[str, Any]:
        """
        Get comprehensive batting statistics for a player.
        
        Args:
            player_name: Name of the player
            
        Returns:
            Dictionary containing all batting metrics
        """
        player_data = self.batting_df[self.batting_df['Player'] == player_name]
        
        if player_data.empty:
            return {"error": f"Player '{player_name}' not found in database"}
        
        stats = player_data.iloc[0].to_dict()
        
        return {
            "player": player_name,
            "innings": int(stats.get('Innings', 0)),
            "runs": int(stats.get('Runs', 0)),
            "average": round(float(stats.get('Average', 0)), 2),
            "strike_rate": round(float(stats.get('Strike_Rate', 0)), 2),
            "boundary_percentage": round(float(stats.get('Boundary_Percentage', 0)), 2),
            "sr_vs_pace": round(float(stats.get('SR_vs_Pace', 0)), 2),
            "sr_vs_spin": round(float(stats.get('SR_vs_Spin', 0)), 2),
            "avg_vs_pace": round(float(stats.get('Avg_vs_Pace', 0)), 2),
            "avg_vs_spin": round(float(stats.get('Avg_vs_Spin', 0)), 2),
            "sr_balls_1_10": round(float(stats.get('SR_balls_1_10', 0)), 2),
            "sr_balls_11_20": round(float(stats.get('SR_balls_11_20', 0)), 2),
            "sr_balls_21_30": round(float(stats.get('SR_balls_21_30', 0)), 2),
            "sr_balls_31_40": round(float(stats.get('SR_balls_31_40', 0)), 2),
            "sr_balls_41_50": round(float(stats.get('SR_balls_41_50', 0)), 2)
        }
    
    def get_player_line_length_analysis(self, player_name: str) -> Dict[str, Any]:
        """
        Analyze player performance against different line and length combinations.
        
        Args:
            player_name: Name of the player
            
        Returns:
            Dictionary with line/length analysis including best and worst zones
        """
        player_data = self.line_length_df[self.line_length_df['Batter'].str.strip() == player_name.strip()]
        
        if player_data.empty:
            return {"error": f"Line/Length data not available for '{player_name}'"}
        
        player_data = player_data.copy()
        player_data['SR'] = pd.to_numeric(player_data['SR'], errors='coerce')
        player_data['Balls'] = pd.to_numeric(player_data['Balls'], errors='coerce')
        player_data['Runs'] = pd.to_numeric(player_data['Runs'], errors='coerce')
        
        player_data = player_data.dropna(subset=['SR', 'Balls', 'Runs'])
        
        if player_data.empty:
            return {"error": f"No valid line/length data for '{player_name}'"}
        
        analysis = []
        for _, row in player_data.iterrows():
            analysis.append({
                "line": str(row['Line']),
                "length": str(row['Length']),
                "strike_rate": round(float(row['SR']), 2),
                "balls": int(row['Balls']),
                "runs": int(row['Runs'])
            })
        
        sorted_by_sr = sorted(analysis, key=lambda x: x['strike_rate'], reverse=True)
        best_zones = sorted_by_sr[:3]
        worst_zones = sorted_by_sr[-3:]
        
        return {
            "player": player_name,
            "total_combinations": len(analysis),
            "all_zones": analysis,
            "best_zones": best_zones,
            "worst_zones": worst_zones,
            "average_sr": round(np.mean([x['strike_rate'] for x in analysis]), 2)
        }
    
    def get_player_wagon_wheel_analysis(self, player_name: str) -> Dict[str, Any]:
        """
        Analyze player's scoring zones and boundary distribution.
        
        Args:
            player_name: Name of the player
            
        Returns:
            Dictionary with wagon wheel data showing scoring patterns
        """
        player_data = self.wagon_wheel_df[self.wagon_wheel_df['Batter'].str.strip() == player_name.strip()]
        
        if player_data.empty:
            return {"error": f"Wagon wheel data not available for '{player_name}'"}
        
        player_data = player_data.copy()
        player_data['Boundaries'] = pd.to_numeric(player_data['Boundaries'], errors='coerce')
        
        total_boundaries = player_data['Boundaries'].sum()
        if total_boundaries > 0:
            player_data['Percentage'] = (player_data['Boundaries'] / total_boundaries * 100).round(2)
        else:
            player_data['Percentage'] = 0
        
        player_data = player_data.dropna(subset=['Boundaries'])
        
        zones = []
        for _, row in player_data.iterrows():
            zones.append({
                "zone": str(row['Zone']),
                "boundaries": int(row['Boundaries']),
                "percentage": round(float(row['Percentage']), 2)
            })
        
        sorted_zones = sorted(zones, key=lambda x: x['percentage'], reverse=True)
        strong_zones = sorted_zones[:3]
        weak_zones = sorted_zones[-3:]
        
        return {
            "player": player_name,
            "total_zones": len(zones),
            "all_zones": zones,
            "strong_zones": strong_zones,
            "weak_zones": weak_zones,
            "total_boundaries": sum([z['boundaries'] for z in zones])
        }
    
    def get_player_strengths_weaknesses(self, player_name: str) -> Dict[str, Any]:
        """
        Identify top 2 strengths and weaknesses with data backing.
        
        Args:
            player_name: Name of the player
            
        Returns:
            Dictionary with detailed strengths and weaknesses analysis
        """
        stats = self.get_player_stats(player_name)
        if "error" in stats:
            return stats
        
        line_length = self.get_player_line_length_analysis(player_name)
        wagon_wheel = self.get_player_wagon_wheel_analysis(player_name)
        
        strengths = []
        weaknesses = []
        
        if stats['strike_rate'] > 150:
            strengths.append({
                "category": "Explosive Strike Rate",
                "description": f"Outstanding strike rate of {stats['strike_rate']} - among the most aggressive batters",
                "data": f"SR: {stats['strike_rate']}, Death Overs SR: {stats['sr_balls_41_50']}"
            })
        elif stats['strike_rate'] > 140:
            strengths.append({
                "category": "Strong Strike Rate",
                "description": f"Excellent strike rate of {stats['strike_rate']} - maintains good scoring pace",
                "data": f"SR: {stats['strike_rate']}, Overall Runs: {stats['runs']}"
            })
        
        if stats['average'] > 40:
            strengths.append({
                "category": "Consistent Run Scorer",
                "description": f"Exceptional average of {stats['average']} - highly reliable batter",
                "data": f"Average: {stats['average']}, Total Runs: {stats['runs']} in {stats['innings']} innings"
            })
        elif stats['average'] > 35:
            strengths.append({
                "category": "Solid Consistency",
                "description": f"Strong average of {stats['average']} - dependable performer",
                "data": f"Average: {stats['average']}, Innings: {stats['innings']}"
            })
        
        if stats['boundary_percentage'] > 60:
            strengths.append({
                "category": "Boundary Hitting",
                "description": f"Excellent boundary percentage of {stats['boundary_percentage']}% - finds boundaries regularly",
                "data": f"Boundary %: {stats['boundary_percentage']}%, SR: {stats['strike_rate']}"
            })
        
        if stats['sr_vs_spin'] > stats['sr_vs_pace'] + 10:
            strengths.append({
                "category": "Spin Domination",
                "description": f"Superior against spin with SR of {stats['sr_vs_spin']} vs {stats['sr_vs_pace']} against pace",
                "data": f"SR vs Spin: {stats['sr_vs_spin']}, SR vs Pace: {stats['sr_vs_pace']}"
            })
        elif stats['sr_vs_pace'] > stats['sr_vs_spin'] + 10:
            strengths.append({
                "category": "Pace Mastery",
                "description": f"Excels against pace with SR of {stats['sr_vs_pace']} vs {stats['sr_vs_spin']} against spin",
                "data": f"SR vs Pace: {stats['sr_vs_pace']}, SR vs Spin: {stats['sr_vs_spin']}"
            })
        
        if stats['sr_balls_41_50'] > 180:
            strengths.append({
                "category": "Death Overs Specialist",
                "description": f"Devastating in death overs with SR of {stats['sr_balls_41_50']}",
                "data": f"Death SR: {stats['sr_balls_41_50']}, Overall SR: {stats['strike_rate']}"
            })
        
        if stats['strike_rate'] < 135:
            weaknesses.append({
                "category": "Below Par Strike Rate",
                "description": f"Strike rate of {stats['strike_rate']} is below modern T20 standards",
                "data": f"SR: {stats['strike_rate']}, Boundary %: {stats['boundary_percentage']}%"
            })
        
        if stats['average'] < 30:
            weaknesses.append({
                "category": "Consistency Issues",
                "description": f"Average of {stats['average']} indicates inconsistent performances",
                "data": f"Average: {stats['average']}, Innings: {stats['innings']}"
            })
        
        if stats['boundary_percentage'] < 55:
            weaknesses.append({
                "category": "Boundary Scoring",
                "description": f"Boundary percentage of {stats['boundary_percentage']}% is relatively low",
                "data": f"Boundary %: {stats['boundary_percentage']}%, SR: {stats['strike_rate']}"
            })
        
        if stats['sr_vs_spin'] < stats['sr_vs_pace'] - 10:
            weaknesses.append({
                "category": "Struggles vs Spin",
                "description": f"Vulnerable against spin - SR drops to {stats['sr_vs_spin']} from {stats['sr_vs_pace']} vs pace",
                "data": f"SR vs Spin: {stats['sr_vs_spin']}, SR vs Pace: {stats['sr_vs_pace']}"
            })
        elif stats['sr_vs_pace'] < stats['sr_vs_spin'] - 10:
            weaknesses.append({
                "category": "Struggles vs Pace",
                "description": f"Vulnerable against pace - SR drops to {stats['sr_vs_pace']} from {stats['sr_vs_spin']} vs spin",
                "data": f"SR vs Pace: {stats['sr_vs_pace']}, SR vs Spin: {stats['sr_vs_spin']}"
            })
        
        if stats['sr_balls_1_10'] < 130:
            weaknesses.append({
                "category": "Slow Starter",
                "description": f"Powerplay SR of {stats['sr_balls_1_10']} indicates slow starts",
                "data": f"Powerplay SR: {stats['sr_balls_1_10']}, Overall SR: {stats['strike_rate']}"
            })
        
        if "error" not in line_length and 'worst_zones' in line_length:
            worst_zone = line_length['worst_zones'][0]
            weaknesses.append({
                "category": "Line/Length Weakness",
                "description": f"Struggles against {worst_zone['length']} on {worst_zone['line']} line",
                "data": f"SR: {worst_zone['strike_rate']}, Balls: {worst_zone['balls']}"
            })
        
        strengths = sorted(strengths, key=lambda x: len(x['data']), reverse=True)[:2]
        weaknesses = sorted(weaknesses, key=lambda x: len(x['data']), reverse=True)[:2]
        
        if len(strengths) < 2:
            strengths.append({
                "category": "Experience",
                "description": f"Played {stats['innings']} innings with {stats['runs']} runs",
                "data": f"Innings: {stats['innings']}, Runs: {stats['runs']}"
            })
        
        if len(weaknesses) < 2:
            weaknesses.append({
                "category": "Areas for Improvement",
                "description": "Maintain consistency across all match phases",
                "data": f"Current Average: {stats['average']}, SR: {stats['strike_rate']}"
            })
        
        return {
            "player": player_name,
            "strengths": strengths[:2],
            "weaknesses": weaknesses[:2]
        }
    
    def get_bowling_plan(self, player_name: str) -> Dict[str, Any]:
        """
        Generate comprehensive bowling plan based on player weaknesses.
        
        Args:
            player_name: Name of the player
            
        Returns:
            Dictionary with bowling strategies, field placements, and key insights
        """
        stats = self.get_player_stats(player_name)
        if "error" in stats:
            return stats
        
        line_length = self.get_player_line_length_analysis(player_name)
        wagon_wheel = self.get_player_wagon_wheel_analysis(player_name)
        
        strategies = []
        field_placements = []
        key_insights = []
        
        if stats['sr_vs_spin'] < stats['sr_vs_pace'] - 5:
            strategies.append({
                "phase": "Middle Overs (7-15)",
                "approach": "Deploy spinners extensively",
                "reasoning": f"Player's SR vs spin ({stats['sr_vs_spin']}) is significantly lower than vs pace ({stats['sr_vs_pace']})"
            })
            key_insights.append(f"Spin weakness: SR drops by {round(stats['sr_vs_pace'] - stats['sr_vs_spin'], 1)} points against spin")
        elif stats['sr_vs_pace'] < stats['sr_vs_spin'] - 5:
            strategies.append({
                "phase": "Powerplay & Death",
                "approach": "Use pace bowlers with variations",
                "reasoning": f"Player struggles against pace (SR: {stats['sr_vs_pace']}) compared to spin (SR: {stats['sr_vs_spin']})"
            })
            key_insights.append(f"Pace vulnerability: SR {round(stats['sr_vs_spin'] - stats['sr_vs_pace'], 1)} points lower vs pace")
        
        if "error" not in line_length and 'worst_zones' in line_length:
            worst_zone = line_length['worst_zones'][0]
            strategies.append({
                "phase": "All Phases",
                "approach": f"Target {worst_zone['length']} length on {worst_zone['line']} line",
                "reasoning": f"Lowest SR of {worst_zone['strike_rate']} in this zone ({worst_zone['balls']} balls faced)"
            })
            key_insights.append(f"Exploitable zone: {worst_zone['length']} on {worst_zone['line']} (SR: {worst_zone['strike_rate']})")
            
            second_worst = line_length['worst_zones'][1] if len(line_length['worst_zones']) > 1 else worst_zone
            strategies.append({
                "phase": "Building Pressure",
                "approach": f"Alternate with {second_worst['length']} deliveries",
                "reasoning": f"Secondary weak zone with SR of {second_worst['strike_rate']}"
            })
        
        if "error" not in wagon_wheel and 'weak_zones' in wagon_wheel:
            weak_zone = wagon_wheel['weak_zones'][0]
            field_placements.append({
                "zone": weak_zone['zone'],
                "fielders": "Pack this area with 2-3 fielders",
                "reasoning": f"Only {weak_zone['percentage']}% of boundaries scored here - least productive zone"
            })
            
            strong_zone = wagon_wheel['strong_zones'][0]
            field_placements.append({
                "zone": strong_zone['zone'],
                "fielders": "Position boundary rider and sweeper",
                "reasoning": f"Primary scoring zone with {strong_zone['percentage']}% of boundaries - protect this area"
            })
            key_insights.append(f"Scoring pattern: {strong_zone['percentage']}% boundaries through {strong_zone['zone']}")
        
        if stats['sr_balls_1_10'] < 135:
            strategies.append({
                "phase": "Powerplay (1-6)",
                "approach": "Attack early with aggressive fields",
                "reasoning": f"Slow starter with powerplay SR of {stats['sr_balls_1_10']}"
            })
            key_insights.append(f"Early pressure opportunity: Powerplay SR only {stats['sr_balls_1_10']}")
        
        if stats['sr_balls_41_50'] > 170:
            strategies.append({
                "phase": "Death Overs (16-20)",
                "approach": "Wide yorkers and slower balls, defensive field",
                "reasoning": f"Dangerous finisher with death SR of {stats['sr_balls_41_50']}"
            })
            field_placements.append({
                "zone": "Boundary",
                "fielders": "All fielders on boundary in death overs",
                "reasoning": f"Death overs SR of {stats['sr_balls_41_50']} - prevent boundaries"
            })
            key_insights.append(f"Death threat: Accelerates to SR {stats['sr_balls_41_50']} in final overs")
        
        if stats['boundary_percentage'] > 60:
            field_placements.append({
                "zone": "Inner Ring",
                "fielders": "Minimize gaps in 30-yard circle",
                "reasoning": f"High boundary percentage ({stats['boundary_percentage']}%) - force rotation"
            })
        
        if len(strategies) < 3:
            strategies.append({
                "phase": "General",
                "approach": "Maintain tight lines and build dot ball pressure",
                "reasoning": f"Overall SR of {stats['strike_rate']} can be contained with disciplined bowling"
            })
        
        if len(field_placements) < 2:
            field_placements.append({
                "zone": "Standard T20 Field",
                "fielders": "Balanced field with protection in scoring zones",
                "reasoning": "Adapt based on match situation and bowler type"
            })
        
        if len(key_insights) < 2:
            key_insights.append(f"Career stats: {stats['runs']} runs at {stats['average']} average")
            key_insights.append(f"Boundary threat: {stats['boundary_percentage']}% of runs from boundaries")
        
        return {
            "player": player_name,
            "strategies": strategies,
            "field_placements": field_placements,
            "key_insights": key_insights[:5],
            "summary": f"Target weak zones, exploit {('spin' if stats['sr_vs_spin'] < stats['sr_vs_pace'] else 'pace')} vulnerability, and build pressure through tight bowling"
        }
