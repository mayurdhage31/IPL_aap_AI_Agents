#!/usr/bin/env python3
"""
Test script for enhanced betting preview functionality.
"""

from betting_tools import BettingAnalysisTools
from betting_preview_agent import BettingPreviewAgent
import os
from dotenv import load_dotenv

load_dotenv()

def test_betting_tools():
    """Test the betting analysis tools."""
    print("=" * 80)
    print("Testing Betting Analysis Tools")
    print("=" * 80)
    
    tools = BettingAnalysisTools()
    
    # Test with Mumbai Indians vs Rajasthan Royals
    team1 = "Mumbai Indians"
    team2 = "Rajasthan Royals"
    
    print(f"\nGenerating detailed analysis for {team1} vs {team2}...")
    
    analysis = tools.get_detailed_match_analysis(team1, team2)
    
    if "error" in analysis:
        print(f"Error: {analysis['error']}")
        return
    
    print("\n" + "=" * 80)
    print("FIXTURE ANALYSIS")
    print("=" * 80)
    print(analysis['fixture_analysis'])
    
    print("\n" + "=" * 80)
    print("KEY STATS & TRENDS")
    print("=" * 80)
    for i, stat in enumerate(analysis['key_stats_and_trends'], 1):
        print(f"{i}. {stat}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDED BETS")
    print("=" * 80)
    for bet in analysis['recommended_bets']:
        print(f"\n{bet['bet_type']}: {bet['selection']}")
        print(f"Odds: {bet['odds']} | Confidence: {bet['confidence']}")
        print(f"Reasoning: {bet['reasoning']}")
    
    print("\n" + "=" * 80)
    print("DETAILED REASONING")
    print("=" * 80)
    for section in analysis['detailed_reasoning']['sections']:
        print(f"\n{section['title']}")
        print("-" * 80)
        print(section['content'])
    
    print("\n" + "=" * 80)
    print("FINAL PREDICTION")
    print("=" * 80)
    print(analysis['detailed_reasoning']['final_prediction'])
    
    print("\n" + "=" * 80)
    print("Test completed successfully!")
    print("=" * 80)

def test_betting_preview_agent():
    """Test the betting preview agent."""
    print("\n\n" + "=" * 80)
    print("Testing Betting Preview Agent")
    print("=" * 80)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Warning: No API key found. Skipping agent test.")
        return
    
    agent = BettingPreviewAgent(api_key)
    
    team1 = "Mumbai Indians"
    team2 = "Rajasthan Royals"
    
    print(f"\nGenerating betting preview for {team1} vs {team2}...")
    
    preview = agent.generate_preview(team1, team2)
    
    print("\n" + "=" * 80)
    print("BETTING PREVIEW OUTPUT")
    print("=" * 80)
    print(preview)
    print("\n" + "=" * 80)

if __name__ == "__main__":
    # Test the tools first
    test_betting_tools()
    
    # Test the agent
    test_betting_preview_agent()
