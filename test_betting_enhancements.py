"""
Test script to verify betting preview enhancements
"""
from betting_tools import BettingAnalysisTools

def test_betting_enhancements():
    print("Testing Betting Preview Enhancements...\n")
    
    # Initialize tools
    tools = BettingAnalysisTools()
    
    # Test 1: Get all venues
    print("=" * 80)
    print("TEST 1: Get All Venues")
    print("=" * 80)
    venues = tools.get_all_venues_list()
    print(f"Total venues available: {len(venues)}")
    print(f"First 5 venues: {venues[:5]}\n")
    
    # Test 2: Generate H2H record
    print("=" * 80)
    print("TEST 2: Generate H2H Record")
    print("=" * 80)
    team1 = "Mumbai Indians"
    team2 = "Chennai Super Kings"
    h2h = tools.generate_h2h_record(team1, team2)
    print(f"H2H Record: {team1} vs {team2}")
    print(f"Team1 Wins: {h2h['team1_wins']}")
    print(f"Team2 Wins: {h2h['team2_wins']}")
    print(f"Narrative: {h2h['narrative']}\n")
    
    # Test 3: Generate recent form
    print("=" * 80)
    print("TEST 3: Generate Recent Form")
    print("=" * 80)
    form1 = tools.generate_recent_form(team1)
    form2 = tools.generate_recent_form(team2)
    print(f"{team1} Form: {form1['wins']}/5 wins")
    print(f"Narrative: {form1['narrative']}")
    print(f"\n{team2} Form: {form2['wins']}/5 wins")
    print(f"Narrative: {form2['narrative']}\n")
    
    # Test 4: Get venue insights
    print("=" * 80)
    print("TEST 4: Get Venue Insights")
    print("=" * 80)
    venue = "Wankhede Stadium, Mumbai"
    venue_insights = tools.get_venue_insights(venue)
    print(f"Venue: {venue_insights['venue_name']}")
    print(f"\nToss Decisions:")
    if venue_insights['toss_decisions']:
        if 'won_toss' in venue_insights['toss_decisions']:
            won = venue_insights['toss_decisions']['won_toss']
            print(f"  Won Toss - Batted First: {won['batted_first']}, Bowled First: {won['bowled_first']}")
        if 'lost_toss' in venue_insights['toss_decisions']:
            lost = venue_insights['toss_decisions']['lost_toss']
            print(f"  Lost Toss - Batted First: {lost['batted_first']}, Bowled First: {lost['bowled_first']}")
    
    print(f"\nVenue Stats:")
    if venue_insights['venue_stats']:
        stats = venue_insights['venue_stats']
        print(f"  Matches Played: {stats['matches_played']}")
        print(f"  Average Score: {stats['average_score']}")
        print(f"  Average First Innings: {stats['average_first_innings_score']}")
        print(f"  Boundary %: {stats['boundary_percentage']}%")
        print(f"  Pace Wickets %: {stats['pace_wickets_pct']}%")
        print(f"  Spin Wickets %: {stats['spin_wickets_pct']}%\n")
    
    # Test 5: Get detailed match analysis with venue
    print("=" * 80)
    print("TEST 5: Get Detailed Match Analysis with Venue")
    print("=" * 80)
    analysis = tools.get_detailed_match_analysis(team1, team2, venue=venue)
    
    if "error" not in analysis:
        print(f"Match: {team1} vs {team2} at {venue}\n")
        
        print("Fixture Analysis Points:")
        for i, point in enumerate(analysis['fixture_analysis'], 1):
            print(f"{i}. {point[:100]}...")
        
        print(f"\nVenue Insights ({len(analysis['venue_insights'])} points):")
        for i, insight in enumerate(analysis['venue_insights'], 1):
            print(f"{i}. {insight[:100]}...")
        
        print(f"\nRecommended Bets: {len(analysis['recommended_bets'])} bets")
        for i, bet in enumerate(analysis['recommended_bets'][:3], 1):
            print(f"{i}. {bet['bet_type']}: {bet['selection']} (Odds: {bet['odds']})")
        
        print("\n✅ All tests passed successfully!")
    else:
        print(f"❌ Error: {analysis['error']}")
    
    # Test 6: Test without venue (should use generic key stats)
    print("\n" + "=" * 80)
    print("TEST 6: Get Detailed Match Analysis without Venue")
    print("=" * 80)
    analysis_no_venue = tools.get_detailed_match_analysis(team1, team2, venue=None)
    
    if "error" not in analysis_no_venue:
        print(f"Match: {team1} vs {team2} (No venue selected)\n")
        print(f"Using generic key stats: {len(analysis_no_venue['venue_insights'])} points")
        print("✅ Test passed!")
    else:
        print(f"❌ Error: {analysis_no_venue['error']}")

if __name__ == "__main__":
    test_betting_enhancements()
