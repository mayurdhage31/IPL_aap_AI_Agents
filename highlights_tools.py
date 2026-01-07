import random
from typing import Dict, List, Any, Optional


class HighlightsAnalysisTools:
    """
    Tools for generating and analyzing ball-by-ball cricket match data.
    Creates realistic T20 match highlights and identifies key moments.
    """
    
    def __init__(self):
        """Initialize with match data."""
        self.match_data = self._generate_mi_vs_csk_match()
    
    def _generate_mi_vs_csk_match(self) -> Dict[str, Any]:
        """
        Generate realistic ball-by-ball data for MI vs CSK match.
        
        Returns:
            Complete match data structure with both innings
        """
        match = {
            "match_id": "MI_vs_CSK_2024",
            "venue": "Wankhede Stadium, Mumbai",
            "date": "2024-05-15",
            "toss": "Mumbai Indians won the toss and elected to bat",
            "result": "Chennai Super Kings won by 6 wickets",
            "innings": []
        }
        
        # First Innings: Mumbai Indians batting
        mi_innings = {
            "innings_number": 1,
            "batting_team": "Mumbai Indians",
            "bowling_team": "Chennai Super Kings",
            "total_runs": 185,
            "total_wickets": 6,
            "total_overs": 20.0,
            "run_rate": 9.25,
            "key_moments": [
                {
                    "over_number": 1,
                    "ball_number": 4,
                    "runs_in_over": 8,
                    "wickets_in_over": 0,
                    "score": "8/0",
                    "event_type": "boundary",
                    "description": "Rohit Sharma drives through covers for FOUR! Elegant timing.",
                    "impact": "positive",
                    "phase": "powerplay"
                },
                {
                    "over_number": 3,
                    "ball_number": 2,
                    "runs_in_over": 6,
                    "wickets_in_over": 1,
                    "score": "32/1",
                    "event_type": "wicket",
                    "description": "WICKET! Rohit Sharma c Gaikwad b Chahar 15(12). Edged to slip, early breakthrough for CSK!",
                    "impact": "negative",
                    "phase": "powerplay",
                    "batsman": "Rohit Sharma",
                    "runs": 15,
                    "balls": 12,
                    "dismissal": "caught"
                },
                {
                    "over_number": 5,
                    "ball_number": 6,
                    "runs_in_over": 14,
                    "wickets_in_over": 0,
                    "score": "58/1",
                    "event_type": "boundary",
                    "description": "Ishan Kishan pulls for SIX! Massive hit over mid-wicket, 89 meters!",
                    "impact": "positive",
                    "phase": "powerplay"
                },
                {
                    "over_number": 7,
                    "ball_number": 3,
                    "runs_in_over": 12,
                    "wickets_in_over": 0,
                    "score": "78/1",
                    "event_type": "milestone",
                    "description": "FIFTY for Ishan Kishan! Reaches his half-century off just 28 balls with a boundary.",
                    "impact": "positive",
                    "phase": "middle",
                    "batsman": "Ishan Kishan",
                    "runs": 50,
                    "balls": 28
                },
                {
                    "over_number": 10,
                    "ball_number": 4,
                    "runs_in_over": 4,
                    "wickets_in_over": 1,
                    "score": "95/2",
                    "event_type": "wicket",
                    "description": "WICKET! Ishan Kishan st Dhoni b Jadeja 64(38). Stumped by MS Dhoni, brilliant glovework!",
                    "impact": "negative",
                    "phase": "middle",
                    "batsman": "Ishan Kishan",
                    "runs": 64,
                    "balls": 38,
                    "dismissal": "stumped"
                },
                {
                    "over_number": 12,
                    "ball_number": 2,
                    "runs_in_over": 3,
                    "wickets_in_over": 2,
                    "score": "115/4",
                    "event_type": "collapse",
                    "description": "DOUBLE WICKET OVER! Tilak Varma and Suryakumar Yadav dismissed. MI in trouble!",
                    "impact": "negative",
                    "phase": "middle"
                },
                {
                    "over_number": 16,
                    "ball_number": 1,
                    "runs_in_over": 22,
                    "wickets_in_over": 0,
                    "score": "158/4",
                    "event_type": "big_over",
                    "description": "MASSIVE OVER! Hardik Pandya smashes 22 runs including 2 SIXES and a FOUR! Game-changing over!",
                    "impact": "positive",
                    "phase": "death",
                    "batsman": "Hardik Pandya",
                    "boundaries": "2x6, 1x4"
                },
                {
                    "over_number": 18,
                    "ball_number": 5,
                    "runs_in_over": 11,
                    "wickets_in_over": 1,
                    "score": "175/5",
                    "event_type": "wicket",
                    "description": "WICKET! Hardik Pandya c Jadeja b Pathirana 48(22). Brilliant catch at long-on!",
                    "impact": "negative",
                    "phase": "death",
                    "batsman": "Hardik Pandya",
                    "runs": 48,
                    "balls": 22,
                    "dismissal": "caught"
                },
                {
                    "over_number": 19,
                    "ball_number": 6,
                    "runs_in_over": 18,
                    "wickets_in_over": 0,
                    "score": "185/6",
                    "event_type": "big_over",
                    "description": "18 runs in the final over! Tim David finishes with a flourish, SIX off the last ball!",
                    "impact": "positive",
                    "phase": "death"
                }
            ],
            "batting_summary": [
                {"batsman": "Rohit Sharma", "runs": 15, "balls": 12, "fours": 2, "sixes": 0, "sr": 125.0},
                {"batsman": "Ishan Kishan", "runs": 64, "balls": 38, "fours": 6, "sixes": 3, "sr": 168.4},
                {"batsman": "Tilak Varma", "runs": 18, "balls": 15, "fours": 1, "sixes": 1, "sr": 120.0},
                {"batsman": "Suryakumar Yadav", "runs": 12, "balls": 10, "fours": 1, "sixes": 0, "sr": 120.0},
                {"batsman": "Hardik Pandya", "runs": 48, "balls": 22, "fours": 3, "sixes": 3, "sr": 218.2},
                {"batsman": "Tim David", "runs": 22, "balls": 11, "fours": 1, "sixes": 2, "sr": 200.0},
                {"batsman": "Romario Shepherd", "runs": 6, "balls": 4, "fours": 0, "sixes": 0, "sr": 150.0}
            ],
            "bowling_summary": [
                {"bowler": "Deepak Chahar", "overs": 4, "runs": 32, "wickets": 2, "economy": 8.0},
                {"bowler": "Tushar Deshpande", "overs": 4, "runs": 42, "wickets": 0, "economy": 10.5},
                {"bowler": "Ravindra Jadeja", "overs": 4, "runs": 28, "wickets": 2, "economy": 7.0},
                {"bowler": "Matheesha Pathirana", "overs": 4, "runs": 38, "wickets": 1, "economy": 9.5},
                {"bowler": "Moeen Ali", "overs": 4, "runs": 45, "wickets": 1, "economy": 11.25}
            ]
        }
        
        # Second Innings: Chennai Super Kings chasing
        csk_innings = {
            "innings_number": 2,
            "batting_team": "Chennai Super Kings",
            "bowling_team": "Mumbai Indians",
            "total_runs": 189,
            "total_wickets": 4,
            "total_overs": 19.3,
            "run_rate": 9.69,
            "target": 186,
            "key_moments": [
                {
                    "over_number": 2,
                    "ball_number": 4,
                    "runs_in_over": 12,
                    "wickets_in_over": 0,
                    "score": "24/0",
                    "event_type": "boundary",
                    "description": "Ruturaj Gaikwad cover drives for FOUR! Pure class from the CSK opener.",
                    "impact": "positive",
                    "phase": "powerplay"
                },
                {
                    "over_number": 5,
                    "ball_number": 6,
                    "runs_in_over": 16,
                    "wickets_in_over": 0,
                    "score": "52/0",
                    "event_type": "milestone",
                    "description": "CSK race to 52/0 in powerplay! Ruturaj Gaikwad 35*(22), dominant start!",
                    "impact": "positive",
                    "phase": "powerplay",
                    "batsman": "Ruturaj Gaikwad",
                    "runs": 35,
                    "balls": 22
                },
                {
                    "over_number": 8,
                    "ball_number": 2,
                    "runs_in_over": 8,
                    "wickets_in_over": 0,
                    "score": "82/0",
                    "event_type": "milestone",
                    "description": "FIFTY for Devon Conway! Reaches his half-century off 31 balls.",
                    "impact": "positive",
                    "phase": "middle",
                    "batsman": "Devon Conway",
                    "runs": 50,
                    "balls": 31
                },
                {
                    "over_number": 9,
                    "ball_number": 4,
                    "runs_in_over": 7,
                    "wickets_in_over": 1,
                    "score": "98/1",
                    "event_type": "wicket",
                    "description": "WICKET! Devon Conway c Rohit b Bumrah 48(35). Bumrah strikes! Partnership of 98 broken.",
                    "impact": "negative",
                    "phase": "middle",
                    "batsman": "Devon Conway",
                    "runs": 48,
                    "balls": 35,
                    "dismissal": "caught"
                },
                {
                    "over_number": 11,
                    "ball_number": 5,
                    "runs_in_over": 9,
                    "wickets_in_over": 1,
                    "score": "118/2",
                    "event_type": "wicket",
                    "description": "WICKET! Ruturaj Gaikwad lbw b Patel 58(42). Umpire's finger goes up! CSK lose their anchor.",
                    "impact": "negative",
                    "phase": "middle",
                    "batsman": "Ruturaj Gaikwad",
                    "runs": 58,
                    "balls": 42,
                    "dismissal": "lbw"
                },
                {
                    "over_number": 13,
                    "ball_number": 2,
                    "runs_in_over": 14,
                    "wickets_in_over": 0,
                    "score": "135/2",
                    "event_type": "dhoni_arrival",
                    "description": "MS DHONI walks in! The crowd erupts! Hits a boundary off his 2nd ball!",
                    "impact": "positive",
                    "phase": "middle",
                    "batsman": "MS Dhoni"
                },
                {
                    "over_number": 14,
                    "ball_number": 5,
                    "runs_in_over": 11,
                    "wickets_in_over": 0,
                    "score": "146/2",
                    "event_type": "boundary",
                    "description": "DHONI SPECIAL! Helicopter shot for SIX over deep mid-wicket! Vintage MSD!",
                    "impact": "positive",
                    "phase": "middle",
                    "batsman": "MS Dhoni"
                },
                {
                    "over_number": 16,
                    "ball_number": 1,
                    "runs_in_over": 24,
                    "wickets_in_over": 0,
                    "score": "168/3",
                    "event_type": "game_changer",
                    "description": "CARNAGE! Shivam Dube smashes 3 CONSECUTIVE SIXES! 24 runs in the over! Game tilting towards CSK!",
                    "impact": "positive",
                    "phase": "death",
                    "batsman": "Shivam Dube",
                    "boundaries": "4x6"
                },
                {
                    "over_number": 17,
                    "ball_number": 3,
                    "runs_in_over": 8,
                    "wickets_in_over": 1,
                    "score": "176/4",
                    "event_type": "wicket",
                    "description": "WICKET! MS Dhoni c David b Bumrah 28(15). Bumrah gets the big fish! But damage already done.",
                    "impact": "negative",
                    "phase": "death",
                    "batsman": "MS Dhoni",
                    "runs": 28,
                    "balls": 15,
                    "dismissal": "caught"
                },
                {
                    "over_number": 19,
                    "ball_number": 3,
                    "runs_in_over": 13,
                    "wickets_in_over": 0,
                    "score": "189/4",
                    "event_type": "match_winner",
                    "description": "FOUR! Ravindra Jadeja finishes it in style! CSK WIN by 6 wickets with 3 balls to spare!",
                    "impact": "positive",
                    "phase": "death",
                    "batsman": "Ravindra Jadeja",
                    "match_result": "CSK wins"
                }
            ],
            "batting_summary": [
                {"batsman": "Ruturaj Gaikwad", "runs": 58, "balls": 42, "fours": 7, "sixes": 1, "sr": 138.1},
                {"batsman": "Devon Conway", "runs": 48, "balls": 35, "fours": 5, "sixes": 1, "sr": 137.1},
                {"batsman": "Ajinkya Rahane", "runs": 15, "balls": 12, "fours": 2, "sixes": 0, "sr": 125.0},
                {"batsman": "Shivam Dube", "runs": 42, "balls": 18, "fours": 1, "sixes": 4, "sr": 233.3},
                {"batsman": "MS Dhoni", "runs": 28, "balls": 15, "fours": 2, "sixes": 2, "sr": 186.7},
                {"batsman": "Ravindra Jadeja", "runs": 12, "balls": 7, "fours": 2, "sixes": 0, "sr": 171.4}
            ],
            "bowling_summary": [
                {"bowler": "Jasprit Bumrah", "overs": 4, "runs": 28, "wickets": 2, "economy": 7.0},
                {"bowler": "Gerald Coetzee", "overs": 3.3, "runs": 45, "wickets": 0, "economy": 12.86},
                {"bowler": "Piyush Chawla", "overs": 4, "runs": 38, "wickets": 1, "economy": 9.5},
                {"bowler": "Hardik Pandya", "overs": 4, "runs": 42, "wickets": 0, "economy": 10.5},
                {"bowler": "Kumar Kartikeya", "overs": 4, "runs": 36, "wickets": 1, "economy": 9.0}
            ]
        }
        
        match["innings"].append(mi_innings)
        match["innings"].append(csk_innings)
        
        return match
    
    def get_match_bbb_data(self, match_id: str = "MI_vs_CSK_2024") -> Dict[str, Any]:
        """
        Fetch ball-by-ball data for the match.
        
        Args:
            match_id: Match identifier
            
        Returns:
            Complete ball-by-ball data structure
        """
        return self.match_data
    
    def identify_key_moments(self, bbb_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze BBB data to identify significant moments.
        
        Args:
            bbb_data: Ball-by-ball match data
            
        Returns:
            List of key moments with timestamps and impact
        """
        key_moments = []
        
        for innings in bbb_data["innings"]:
            for moment in innings["key_moments"]:
                key_moments.append({
                    "innings": innings["innings_number"],
                    "batting_team": innings["batting_team"],
                    "over": moment["over_number"],
                    "score": moment["score"],
                    "event_type": moment["event_type"],
                    "description": moment["description"],
                    "impact": moment["impact"],
                    "phase": moment["phase"]
                })
        
        return key_moments
    
    def calculate_phase_stats(self, bbb_data: Dict[str, Any], phase: str) -> Dict[str, Any]:
        """
        Calculate statistics for specific match phases.
        
        Args:
            bbb_data: Ball-by-ball match data
            phase: "powerplay" (1-6), "middle" (7-15), or "death" (16-20)
            
        Returns:
            Statistics for that phase
        """
        phase_ranges = {
            "powerplay": (1, 6),
            "middle": (7, 15),
            "death": (16, 20)
        }
        
        if phase not in phase_ranges:
            return {"error": "Invalid phase. Use 'powerplay', 'middle', or 'death'"}
        
        start_over, end_over = phase_ranges[phase]
        phase_stats = []
        
        for innings in bbb_data["innings"]:
            phase_moments = [m for m in innings["key_moments"] 
                           if start_over <= m["over_number"] <= end_over]
            
            total_runs = sum(m.get("runs_in_over", 0) for m in phase_moments)
            total_wickets = sum(m.get("wickets_in_over", 0) for m in phase_moments)
            
            phase_stats.append({
                "innings": innings["innings_number"],
                "batting_team": innings["batting_team"],
                "phase": phase,
                "overs": f"{start_over}-{end_over}",
                "runs": total_runs,
                "wickets": total_wickets,
                "key_moments_count": len(phase_moments)
            })
        
        return {"phase": phase, "stats": phase_stats}
    
    def generate_commentary_context(self, moment_type: str, stats: Dict[str, Any]) -> str:
        """
        Generate engaging commentary for key moments.
        
        Args:
            moment_type: Type of moment (wicket, boundary, milestone, etc.)
            stats: Statistics related to the moment
            
        Returns:
            Commentary-style description
        """
        commentary_templates = {
            "wicket": [
                "A crucial breakthrough! {description}",
                "The bowler strikes! {description}",
                "That's a massive wicket! {description}"
            ],
            "boundary": [
                "What a shot! {description}",
                "Brilliant batting! {description}",
                "That's gone to the boundary! {description}"
            ],
            "milestone": [
                "A special moment! {description}",
                "Well deserved! {description}",
                "The crowd is on its feet! {description}"
            ],
            "big_over": [
                "This over changes everything! {description}",
                "Carnage in the middle! {description}",
                "The momentum has shifted! {description}"
            ]
        }
        
        templates = commentary_templates.get(moment_type, ["{description}"])
        template = random.choice(templates)
        
        return template.format(**stats)
    
    def get_match_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive match summary.
        
        Returns:
            Match summary with key statistics
        """
        match = self.match_data
        
        summary = {
            "match_id": match["match_id"],
            "venue": match["venue"],
            "result": match["result"],
            "toss": match["toss"],
            "first_innings": {
                "team": match["innings"][0]["batting_team"],
                "score": f"{match['innings'][0]['total_runs']}/{match['innings'][0]['total_wickets']}",
                "overs": match["innings"][0]["total_overs"],
                "run_rate": match["innings"][0]["run_rate"],
                "top_scorer": max(match["innings"][0]["batting_summary"], key=lambda x: x["runs"]),
                "best_bowler": min(match["innings"][0]["bowling_summary"], key=lambda x: x["economy"])
            },
            "second_innings": {
                "team": match["innings"][1]["batting_team"],
                "score": f"{match['innings'][1]['total_runs']}/{match['innings'][1]['total_wickets']}",
                "overs": match["innings"][1]["total_overs"],
                "run_rate": match["innings"][1]["run_rate"],
                "target": match["innings"][1]["target"],
                "top_scorer": max(match["innings"][1]["batting_summary"], key=lambda x: x["runs"]),
                "best_bowler": min(match["innings"][1]["bowling_summary"], key=lambda x: x["economy"])
            },
            "turning_point": "Over 16 in the second innings - Shivam Dube's 24-run over",
            "player_of_match": {
                "name": "Shivam Dube",
                "performance": "42 runs off 18 balls with 4 sixes",
                "reason": "Match-winning knock that tilted the game in CSK's favor"
            }
        }
        
        return summary
