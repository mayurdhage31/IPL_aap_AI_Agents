import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from agent_enhanced import EnhancedCricketAgent
from fantasy_tools import FantasyAnalysisTools
from tools_enhanced import EnhancedCricketAnalysisTools
from betting_preview_agent import BettingPreviewAgent
from highlights_agent import HighlightsPackageAgent
from betting_tools import BettingAnalysisTools
from journalist_preview_agent import JournalistPreviewAgent

load_dotenv()

st.set_page_config(
    page_title="IPL Player Insights - AI Agent",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom JavaScript for sidebar width
st.markdown("""
<script>
    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.width = '320px';
    }
</script>
""", unsafe_allow_html=True)

DARK_THEME_CSS = """
<style>
    .stApp {
        background-color: #0F1B2A;
    }
    
    .main-card {
        background-color: #1C2A3A;
        padding: 15px;
        border-radius: 12px;
        margin: 8px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .inner-card {
        background-color: #223347;
        padding: 12px;
        border-radius: 10px;
        margin: 6px 0;
    }
    
    .main-header {
        color: #EAF2FF;
        font-weight: 700;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    
    .section-title {
        color: #2DD4BF;
        font-weight: 600;
        font-size: 1.8em;
        margin: 12px 0 8px 0;
    }
    
    .subsection-title {
        color: #2DD4BF;
        font-weight: 600;
        font-size: 1.4em;
        margin: 10px 0 6px 0;
    }
    
    .body-text {
        color: #D1D9E6;
        font-size: 1.05em;
        line-height: 1.6;
    }
    
    .muted-text {
        color: #9AA7B8;
        font-size: 0.95em;
    }
    
    .strength-box {
        background-color: #223347;
        border-left: 4px solid #22C55E;
        padding: 10px;
        border-radius: 8px;
        margin: 6px 0;
    }
    
    .weakness-box {
        background-color: #223347;
        border-left: 4px solid #EF4444;
        padding: 10px;
        border-radius: 8px;
        margin: 6px 0;
    }
    
    .metric-card {
        background-color: #223347;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #2DD4BF;
    }
    
    .metric-value {
        color: #2DD4BF;
        font-size: 2.2em;
        font-weight: 700;
    }
    
    .metric-label {
        color: #9AA7B8;
        font-size: 0.9em;
        margin-top: 5px;
    }
    
    .fantasy-anchor {
        background-color: #223347;
        border: 2px solid #22C55E;
        padding: 10px;
        border-radius: 10px;
        margin: 6px 0;
    }
    
    .fantasy-risk {
        background-color: #223347;
        border: 2px solid #F59E0B;
        padding: 10px;
        border-radius: 10px;
        margin: 6px 0;
    }
    
    .venue-card {
        background-color: #223347;
        padding: 12px;
        border-radius: 10px;
        margin: 6px 0;
        border-left: 4px solid #2DD4BF;
    }
    
    .stButton>button {
        background-color: #2DD4BF;
        color: #0F1B2A;
        font-weight: 600;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-size: 1.1em;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #25B8A5;
        box-shadow: 0 0 20px rgba(45, 212, 191, 0.4);
    }
    
    .divider {
        border-top: 2px solid #2DD4BF;
        margin: 20px 0;
    }
    
    h1, h2, h3 {
        color: #EAF2FF;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #223347;
        color: #D1D9E6;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2DD4BF;
        color: #0F1B2A;
    }
    
    /* Sidebar Navigation Styles */
    [data-testid="stSidebar"] {
        background-color: #0F1B2A;
        min-width: 320px !important;
        max-width: 320px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        width: 320px !important;
    }
    
    .nav-item {
        background-color: #1C2A3A;
        padding: 12px 16px;
        margin: 6px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 4px solid transparent;
    }
    
    .nav-item:hover {
        background-color: #223347;
        border-left-color: #2DD4BF;
    }
    
    .nav-item-active {
        background-color: #223347;
        border-left-color: #2DD4BF;
        box-shadow: 0 0 15px rgba(45, 212, 191, 0.3);
    }
    
    .section-description {
        background-color: #1C2A3A;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #2DD4BF;
        margin-bottom: 20px;
    }
    
    /* Expander Styles for Selection Panel */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: #1C2A3A;
        border-radius: 8px;
        padding: 10px 12px;
        font-weight: 600;
        color: #2DD4BF;
        border: 1px solid #2DD4BF;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background-color: #223347;
        border-color: #25B8A5;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent {
        background-color: #1C2A3A;
        border-radius: 0 0 8px 8px;
        padding: 15px 12px;
        border: 1px solid #2DD4BF;
        border-top: none;
    }
    
    /* Selectbox styling in sidebar */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #223347;
        color: #D1D9E6;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #D1D9E6;
        font-weight: 500;
    }
</style>
"""

st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# Initialize session state
if 'selected_section' not in st.session_state:
    st.session_state['selected_section'] = 'Betting Preview'
if 'selected_player' not in st.session_state:
    st.session_state['selected_player'] = None
if 'selected_team1' not in st.session_state:
    st.session_state['selected_team1'] = None
if 'selected_team2' not in st.session_state:
    st.session_state['selected_team2'] = None
if 'selected_venue' not in st.session_state:
    st.session_state['selected_venue'] = None

@st.cache_resource
def initialize_agent(api_key: str):
    return EnhancedCricketAgent(api_key)

@st.cache_resource
def initialize_fantasy_tools():
    return FantasyAnalysisTools()

@st.cache_resource
def initialize_cricket_tools():
    return EnhancedCricketAnalysisTools()

@st.cache_resource
def initialize_betting_agent(api_key: str):
    return BettingPreviewAgent(api_key)

@st.cache_resource
def initialize_highlights_agent(api_key: str):
    return HighlightsPackageAgent(api_key)

@st.cache_resource
def initialize_betting_tools():
    try:
        return BettingAnalysisTools()
    except Exception as e:
        st.error(f"Error initializing betting tools: {str(e)}")
        return None

@st.cache_resource
def initialize_journalist_agent(api_key: str):
    from langchain_anthropic import ChatAnthropic
    llm = ChatAnthropic(model="claude-sonnet-4-20250514", api_key=api_key, temperature=0.7)
    return JournalistPreviewAgent(llm)

def format_fixture_analysis(text):
    """Format fixture analysis with emojis and bold numbers"""
    import re
    
    # Add emoji based on content keywords
    emoji = "📊"
    text_lower = text.lower()
    if any(word in text_lower for word in ["strike rate", "sr", "scoring", "runs", "average"]):
        emoji = "🏏"
    elif any(word in text_lower for word in ["wicket", "bowling", "economy", "defend"]):
        emoji = "🛡️"
    elif any(word in text_lower for word in ["death", "powerplay", "fast", "quick"]):
        emoji = "⚡"
    elif any(word in text_lower for word in ["win", "victory", "champion", "success"]):
        emoji = "🏆"
    elif any(word in text_lower for word in ["accuracy", "precise", "target"]):
        emoji = "🎯"
    
    # Bold all numbers (integers, decimals, percentages)
    text = re.sub(r'(\d+\.?\d*%?)', r'<strong>\1</strong>', text)
    
    return f"{emoji} {text}"

# Initialize tools
cricket_tools = initialize_cricket_tools()
fantasy_tools = initialize_fantasy_tools()
betting_tools = initialize_betting_tools()

# Get data for dropdowns
players_list = cricket_tools.get_all_players_list()
available_teams = fantasy_tools.get_available_teams()
available_venues = betting_tools.get_all_venues_list() if betting_tools else []

# Section descriptions
SECTION_DESCRIPTIONS = {
    'Betting Preview': "Comprehensive match preview from a betting perspective with head-to-head records, team statistics, and venue-specific insights - planned additions include live odds integration and betting trend analysis.",
    'Highlights Package': "AI-curated match highlights and key moments tailored for content creators and analysts - coming soon: automated video timestamp generation and multi-format export options.",
    'Journalist Preview': "Professional match preview content designed for sports journalists with narrative insights and storyline suggestions - future updates will include automated article generation and quote extraction."
}

# Sidebar Navigation
with st.sidebar:
    st.markdown('<h1 class="main-header" style="font-size: 1.8em;">🏏 IPL Insights</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Dynamic selection panels based on selected section (MOVED UP)
    selected_section = st.session_state['selected_section']
    
    # Initialize collapse state
    if 'selection_panel_expanded' not in st.session_state:
        st.session_state['selection_panel_expanded'] = True
    
    if selected_section in ['Betting Preview', 'Highlights Package', 'Journalist Preview']:
        with st.expander("⚙️ Match Configuration", expanded=st.session_state['selection_panel_expanded']):
            st.markdown('<p class="body-text" style="font-size: 0.9em; margin-bottom: 8px;"><strong>Team Selection</strong></p>', unsafe_allow_html=True)
            
            team1 = st.selectbox("Team 1", options=available_teams, index=0, key="sidebar_team1")
            team2 = st.selectbox("Team 2", options=available_teams, index=min(1, len(available_teams)-1), key="sidebar_team2")
            
            st.session_state['selected_team1'] = team1
            st.session_state['selected_team2'] = team2
            
            # Venue selection for Betting Preview
            if selected_section == 'Betting Preview':
                st.markdown('<p class="body-text" style="font-size: 0.9em; margin-top: 12px; margin-bottom: 8px;"><strong>Venue Selection</strong></p>', unsafe_allow_html=True)
                venue = st.selectbox(
                    "Select Venue (Optional)",
                    options=['None'] + available_venues,
                    index=0,
                    key="sidebar_venue",
                    label_visibility="collapsed"
                )
                st.session_state['selected_venue'] = None if venue == 'None' else venue
            
            st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
            
            # Generate buttons for each section
            if selected_section == 'Betting Preview':
                if st.button("🎯 Generate Betting Preview", use_container_width=True, key="gen_betting"):
                    st.session_state['trigger_betting'] = True
                    st.rerun()
            elif selected_section == 'Highlights Package':
                st.markdown('<p class="muted-text" style="font-size: 0.85em;">Highlights are pre-generated for demonstration</p>', unsafe_allow_html=True)
            elif selected_section == 'Journalist Preview':
                st.markdown('<p class="muted-text" style="font-size: 0.85em;">Preview is pre-generated for demonstration</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<h3 class="subsection-title" style="font-size: 1.1em; margin-bottom: 8px;">Navigation</h3>', unsafe_allow_html=True)
    
    # Navigation buttons (MOVED DOWN - only 3 tabs)
    sections = [
        ('💰 Betting Preview', 'Betting Preview'),
        ('🎬 Highlights Package', 'Highlights Package'),
        ('📰 Journalist Preview', 'Journalist Preview')
    ]
    
    for label, section_key in sections:
        if st.button(label, key=f"nav_{section_key}", use_container_width=True):
            st.session_state['selected_section'] = section_key
            st.rerun()
    
    st.markdown("---")
    
    # API Key Configuration
    st.markdown('<h3 class="subsection-title" style="font-size: 1.1em;">⚙️ Configuration</h3>', unsafe_allow_html=True)
    
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Enter your Anthropic API key to enable AI analysis"
    )
    
    st.markdown("---")
    
    # About section
    st.markdown('<h3 class="subsection-title" style="font-size: 1.0em;">📊 About</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="muted-text" style="font-size: 0.85em;">
    <strong>Datasets:</strong><br>
    • IPL Batting Stats (2021-24)<br>
    • Line & Length Analysis<br>
    • Wagon Wheel Data<br>
    • Venue Intelligence<br>
    • Fantasy Performance Data
    </div>
    """, unsafe_allow_html=True)

# Main Content Area
st.markdown('<h1 class="main-header">🏏 IPL Player Insights - AI Agent</h1>', unsafe_allow_html=True)

# Display section description
current_section = st.session_state['selected_section']
st.markdown(f'''
<div class="section-description">
    <p class="body-text" style="margin: 0;">{SECTION_DESCRIPTIONS[current_section]}</p>
</div>
''', unsafe_allow_html=True)

# Render content based on selected section
if current_section == 'Player Analysis':
    st.markdown('<h2 class="section-title">🎯 Player Analysis</h2>', unsafe_allow_html=True)
    
    selected_player = st.session_state.get('selected_player')
    trigger_analysis = st.session_state.get('trigger_analysis', False)
    
    if trigger_analysis and selected_player:
        st.session_state['trigger_analysis'] = False
        
        with st.spinner(f"Analyzing {selected_player}..."):
            player_stats = cricket_tools.get_player_stats(selected_player)
            
            if "error" not in player_stats:
                st.markdown(f'<h3 class="subsection-title">📈 Basic Statistics - {selected_player}</h3>', unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{player_stats['runs']}</div>
                        <div class="metric-label">RUNS</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{player_stats['average']}</div>
                        <div class="metric-label">AVERAGE</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{player_stats['strike_rate']}</div>
                        <div class="metric-label">STRIKE RATE</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{player_stats['boundary_percentage']}%</div>
                        <div class="metric-label">BOUNDARY %</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{player_stats['innings']}</div>
                        <div class="metric-label">INNINGS</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<h3 class="subsection-title">💪 Strengths & Weaknesses</h3>', unsafe_allow_html=True)
                
                strengths_weaknesses = cricket_tools.get_player_strengths_weaknesses(selected_player)
                
                col_str, col_weak = st.columns(2)
                
                with col_str:
                    st.markdown('<p class="body-text" style="color: #22C55E; font-weight: 600;">✅ Key Strengths</p>', unsafe_allow_html=True)
                    for strength in strengths_weaknesses['strengths']:
                        st.markdown(f"""
                        <div class="strength-box">
                            <strong style="color: #22C55E;">{strength['category']}</strong><br>
                            <span class="body-text">{strength['description']}</span><br>
                            <span class="muted-text">📊 {strength['data']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_weak:
                    st.markdown('<p class="body-text" style="color: #EF4444; font-weight: 600;">⚠️ Key Weaknesses</p>', unsafe_allow_html=True)
                    for weakness in strengths_weaknesses['weaknesses']:
                        st.markdown(f"""
                        <div class="weakness-box">
                            <strong style="color: #EF4444;">{weakness['category']}</strong><br>
                            <span class="body-text">{weakness['description']}</span><br>
                            <span class="muted-text">📊 {weakness['data']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                
                tab1, tab2, tab3 = st.tabs(["📍 Line & Length Analysis", "🎯 Bowling Plan", "🤖 AI Agent Insights"])
                
                with tab1:
                    line_length_data = cricket_tools.get_player_line_length_analysis(selected_player)
                    
                    if "error" not in line_length_data:
                        st.markdown(f'<p class="body-text">Average Strike Rate: <strong style="color: #2DD4BF;">{line_length_data["average_sr"]}</strong></p>', unsafe_allow_html=True)
                        
                        df_zones = pd.DataFrame(line_length_data['all_zones'])
                        
                        fig = px.bar(
                            df_zones,
                            x='length',
                            y='strike_rate',
                            color='line',
                            barmode='group',
                            title='Strike Rate by Line & Length',
                            color_discrete_map={'off': '#22C55E', 'line': '#2DD4BF', 'leg': '#F59E0B'}
                        )
                        
                        fig.update_layout(
                            plot_bgcolor='#1C2A3A',
                            paper_bgcolor='#1C2A3A',
                            font_color='#D1D9E6',
                            title_font_color='#EAF2FF',
                            xaxis_title='Length',
                            yaxis_title='Strike Rate'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        col_best, col_worst = st.columns(2)
                        
                        with col_best:
                            st.markdown('<p class="body-text" style="color: #22C55E; font-weight: 600;">🎯 Best Zones</p>', unsafe_allow_html=True)
                            for zone in line_length_data['best_zones']:
                                st.markdown(f"""
                                <div class="inner-card">
                                    <strong>{zone['length'].title()} on {zone['line'].title()}</strong><br>
                                    SR: {zone['strike_rate']} | Balls: {zone['balls']} | Runs: {zone['runs']}
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with col_worst:
                            st.markdown('<p class="body-text" style="color: #EF4444; font-weight: 600;">⚠️ Worst Zones</p>', unsafe_allow_html=True)
                            for zone in line_length_data['worst_zones']:
                                st.markdown(f"""
                                <div class="inner-card">
                                    <strong>{zone['length'].title()} on {zone['line'].title()}</strong><br>
                                    SR: {zone['strike_rate']} | Balls: {zone['balls']} | Runs: {zone['runs']}
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning(line_length_data['error'])
                
                with tab2:
                    bowling_plan = cricket_tools.get_bowling_plan(selected_player)
                    
                    if "error" not in bowling_plan:
                        st.markdown(f'<p class="body-text"><strong>Summary:</strong> {bowling_plan["summary"]}</p>', unsafe_allow_html=True)
                        
                        st.markdown('<h4 style="color: #2DD4BF;">🎯 Bowling Strategies</h4>', unsafe_allow_html=True)
                        for strategy in bowling_plan['strategies']:
                            st.markdown(f"""
                            <div class="inner-card">
                                <strong style="color: #F59E0B;">{strategy['phase']}</strong><br>
                                <strong>Approach:</strong> {strategy['approach']}<br>
                                <span class="muted-text">{strategy['reasoning']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('<h4 style="color: #2DD4BF;">🏟️ Field Placements</h4>', unsafe_allow_html=True)
                        for field in bowling_plan['field_placements']:
                            st.markdown(f"""
                            <div class="inner-card">
                                <strong style="color: #22C55E;">{field['zone']}</strong><br>
                                <strong>Setup:</strong> {field['fielders']}<br>
                                <span class="muted-text">{field['reasoning']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('<h4 style="color: #2DD4BF;">💡 Key Insights</h4>', unsafe_allow_html=True)
                        for insight in bowling_plan['key_insights']:
                            st.markdown(f'<p class="body-text">• {insight}</p>', unsafe_allow_html=True)
                    else:
                        st.warning(bowling_plan['error'])
                
                with tab3:
                    if api_key:
                        agent = initialize_agent(api_key)
                        
                        st.markdown('<p class="body-text">Ask the AI agent anything about this player:</p>', unsafe_allow_html=True)
                        
                        with st.expander("💡 Sample Questions - Click to View", expanded=False):
                            st.markdown('<p class="subsection-title" style="font-size: 1.1em;">Individual Player Analysis</p>', unsafe_allow_html=True)
                            sample_questions_individual = [
                                f"How does {selected_player} perform in death overs?",
                                f"What is {selected_player}'s strike rate against spin bowling?",
                                f"What are the main weaknesses in {selected_player}'s batting technique?",
                                f"Which line and length combinations trouble {selected_player} the most?",
                            ]
                            
                            for i, q in enumerate(sample_questions_individual, 1):
                                if st.button(f"📊 {q}", key=f"sample_q_{i}", use_container_width=True):
                                    st.session_state['selected_question'] = q
                                    st.session_state['trigger_ai'] = True
                                    st.rerun()
                        
                        user_question = st.text_input(
                            "Your Question",
                            placeholder=f"e.g., How does {selected_player} perform in death overs?",
                            key="ai_question",
                            value=st.session_state.get('selected_question', '')
                        )
                        
                        auto_trigger = st.session_state.get('trigger_ai', False)
                        if auto_trigger:
                            st.session_state['trigger_ai'] = False
                            if user_question:
                                with st.spinner("AI Agent is analyzing..."):
                                    response = agent.query(user_question, selected_player)
                                    st.markdown(f'<div class="inner-card"><p class="body-text">{response}</p></div>', unsafe_allow_html=True)
                        
                        if st.button("Ask AI Agent", key="ask_ai"):
                            if user_question:
                                with st.spinner("AI Agent is analyzing..."):
                                    response = agent.query(user_question, selected_player)
                                    st.markdown(f'<div class="inner-card"><p class="body-text">{response}</p></div>', unsafe_allow_html=True)
                            else:
                                st.warning("Please enter a question")
                        
                        if st.button("Reset Conversation", key="reset_conv"):
                            agent.reset_conversation()
                            st.success("Conversation reset!")
                    else:
                        st.warning("⚠️ Please enter your Anthropic API key in the sidebar to use AI Agent features")
            else:
                st.error(player_stats['error'])
    else:
        st.info("👈 Select a player from the sidebar and click 'Analyze Player' to begin")

elif current_section == 'Fantasy Cheat Sheet':
    st.markdown('<h2 class="section-title">⭐ Fantasy Cheat Sheet</h2>', unsafe_allow_html=True)
    
    team1 = st.session_state.get('selected_team1')
    team2 = st.session_state.get('selected_team2')
    trigger_fantasy = st.session_state.get('trigger_fantasy', False)
    
    if trigger_fantasy and team1 and team2:
        st.session_state['trigger_fantasy'] = False
        
        if team1 == team2:
            st.error("⚠️ Please select two different teams")
        else:
            with st.spinner("Generating fantasy insights..."):
                fantasy_analysis = fantasy_tools.get_complete_fantasy_analysis(team1, team2)
                
                st.markdown('<h3 class="subsection-title">📍 Venue Intelligence</h3>', unsafe_allow_html=True)
                
                venue_data = fantasy_analysis['venue_intelligence']
                
                for venue in venue_data['venues']:
                    st.markdown(f"""
                    <div class="venue-card">
                        <h4 style="color: #2DD4BF; margin: 0 0 10px 0;">{venue['venue']} - {venue['city']}</h4>
                        <div style="display: flex; gap: 20px; margin-bottom: 10px;">
                            <span class="body-text">🏃 Pace: <strong>{venue['pace_percentage']}%</strong></span>
                            <span class="body-text">🌀 Spin: <strong>{venue['spin_percentage']}%</strong></span>
                            <span class="body-text" style="color: #F59E0B;">📊 {venue['bias_type']}</span>
                        </div>
                        <p class="muted-text">💡 {venue['fantasy_tip']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if venue['top_specialists']:
                        st.markdown('<p class="body-text" style="margin-left: 20px;"><strong>Venue Specialists:</strong></p>', unsafe_allow_html=True)
                        for spec in venue['top_specialists']:
                            st.markdown(f"""
                            <div style="margin-left: 40px;" class="muted-text">
                                • <strong style="color: #2DD4BF;">{spec['player']}</strong> - {spec['runs']} runs, Avg: {spec['average']}, SR: {spec['strike_rate']}
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown('<h3 class="subsection-title">🎲 Match Situation Edge</h3>', unsafe_allow_html=True)
                
                match_situation = fantasy_analysis['match_situation']
                
                col_t1, col_t2 = st.columns(2)
                
                with col_t1:
                    t1_data = match_situation['team1_analysis']
                    st.markdown(f"""
                    <div class="inner-card">
                        <h4 style="color: #2DD4BF;">{t1_data['team']}</h4>
                        <p class="body-text">
                            <strong>Toss Preference:</strong> <span style="color: #F59E0B;">{t1_data['toss_preference']}</span><br>
                            <span class="muted-text">{t1_data['preference_reason']}</span>
                        </p>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                            <div>
                                <span class="muted-text">1st Innings SR</span><br>
                                <strong style="color: #2DD4BF;">{t1_data['first_innings_sr']}</strong>
                            </div>
                            <div>
                                <span class="muted-text">2nd Innings SR</span><br>
                                <strong style="color: #2DD4BF;">{t1_data['second_innings_sr']}</strong>
                            </div>
                            <div>
                                <span class="muted-text">1st Innings Avg</span><br>
                                <strong style="color: #22C55E;">{t1_data['first_innings_avg']}</strong>
                            </div>
                            <div>
                                <span class="muted-text">2nd Innings Avg</span><br>
                                <strong style="color: #22C55E;">{t1_data['second_innings_avg']}</strong>
                            </div>
                        </div>
                        {f'<p class="body-text" style="margin-top: 10px; color: #F59E0B;">⚡ Death Overs SR: {t1_data["death_overs_sr"]}</p>' if t1_data['death_overs_sr'] > 170 else ''}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_t2:
                    t2_data = match_situation['team2_analysis']
                    st.markdown(f"""
                    <div class="inner-card">
                        <h4 style="color: #2DD4BF;">{t2_data['team']}</h4>
                        <p class="body-text">
                            <strong>Toss Preference:</strong> <span style="color: #F59E0B;">{t2_data['toss_preference']}</span><br>
                            <span class="muted-text">{t2_data['preference_reason']}</span>
                        </p>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;">
                            <div>
                                <span class="muted-text">1st Innings SR</span><br>
                                <strong style="color: #2DD4BF;">{t2_data['first_innings_sr']}</strong>
                            </div>
                            <div>
                                <span class="muted-text">2nd Innings SR</span><br>
                                <strong style="color: #2DD4BF;">{t2_data['second_innings_sr']}</strong>
                            </div>
                            <div>
                                <span class="muted-text">1st Innings Avg</span><br>
                                <strong style="color: #22C55E;">{t2_data['first_innings_avg']}</strong>
                            </div>
                            <div>
                                <span class="muted-text">2nd Innings Avg</span><br>
                                <strong style="color: #22C55E;">{t2_data['second_innings_avg']}</strong>
                            </div>
                        </div>
                        {f'<p class="body-text" style="margin-top: 10px; color: #F59E0B;">⚡ Death Overs SR: {t2_data["death_overs_sr"]}</p>' if t2_data['death_overs_sr'] > 170 else ''}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<p class="body-text" style="margin-top: 15px;"><strong>Key Insights:</strong></p>', unsafe_allow_html=True)
                for insight in match_situation['key_insights']:
                    st.markdown(f'<p class="body-text">• {insight}</p>', unsafe_allow_html=True)
                
                st.markdown('<h3 class="subsection-title">⭐ Fantasy Picks Engine</h3>', unsafe_allow_html=True)
                
                fantasy_picks = fantasy_analysis['fantasy_picks']
                
                st.markdown('<h4 style="color: #22C55E;">🔒 Set-and-Forget Picks (Anchor Players)</h4>', unsafe_allow_html=True)
                
                for pick in fantasy_picks['anchor_picks']:
                    st.markdown(f"""
                    <div class="fantasy-anchor">
                        <h5 style="color: #22C55E; margin: 0 0 8px 0;">{pick['player']} ({pick['position']})</h5>
                        <p class="body-text" style="margin: 5px 0;">
                            <strong>{pick['team']}</strong> | Consistency: {pick['consistency']} | Ceiling: {pick['ceiling']} | Total FP: {pick['total_fp']}
                        </p>
                        <p class="muted-text" style="margin: 5px 0;">💡 {pick['why_pick']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<h4 style="color: #F59E0B;">🎰 High-Risk/Reward Picks</h4>', unsafe_allow_html=True)
                
                for pick in fantasy_picks['risk_picks']:
                    st.markdown(f"""
                    <div class="fantasy-risk">
                        <h5 style="color: #F59E0B; margin: 0 0 8px 0;">{pick['player']} ({pick['position']})</h5>
                        <p class="body-text" style="margin: 5px 0;">
                            <strong>{pick['team']}</strong> | Upside: {pick['upside']} | Risk: {pick['risk']} | Total FP: {pick['total_fp']}
                        </p>
                        <p class="muted-text" style="margin: 5px 0;">💡 {pick['why_pick']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<h4 style="color: #2DD4BF;">🏆 Example Fantasy XI</h4>', unsafe_allow_html=True)
                
                example_xi = fantasy_picks['example_xi']
                
                col_wk, col_bat, col_all, col_bowl = st.columns(4)
                
                with col_wk:
                    st.markdown('<p class="body-text"><strong>🧤 Wicket-Keepers</strong></p>', unsafe_allow_html=True)
                    for player in example_xi['wicket_keepers']:
                        st.markdown(f'<p class="muted-text">• {player}</p>', unsafe_allow_html=True)
                
                with col_bat:
                    st.markdown('<p class="body-text"><strong>🏏 Batsmen</strong></p>', unsafe_allow_html=True)
                    for player in example_xi['batsmen']:
                        st.markdown(f'<p class="muted-text">• {player}</p>', unsafe_allow_html=True)
                
                with col_all:
                    st.markdown('<p class="body-text"><strong>⚡ All-Rounders</strong></p>', unsafe_allow_html=True)
                    for player in example_xi['allrounders']:
                        st.markdown(f'<p class="muted-text">• {player}</p>', unsafe_allow_html=True)
                
                with col_bowl:
                    st.markdown('<p class="body-text"><strong>🎯 Bowlers</strong></p>', unsafe_allow_html=True)
                    for player in example_xi['bowlers']:
                        st.markdown(f'<p class="muted-text">• {player}</p>', unsafe_allow_html=True)
                
                st.markdown(f'<p class="body-text" style="margin-top: 15px;"><strong>Team Composition:</strong> {fantasy_picks["team_composition"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="muted-text">📝 {fantasy_picks["strategy_note"]}</p>', unsafe_allow_html=True)
    else:
        st.info("👈 Select two teams from the sidebar and click 'Generate Fantasy Analysis' to begin")

elif current_section == 'Betting Preview':
    st.markdown('<h2 class="section-title">💰 Betting Preview</h2>', unsafe_allow_html=True)
    
    team1 = st.session_state.get('selected_team1')
    team2 = st.session_state.get('selected_team2')
    venue = st.session_state.get('selected_venue')
    trigger_betting = st.session_state.get('trigger_betting', False)
    
    if trigger_betting and team1 and team2:
        st.session_state['trigger_betting'] = False
        
        if team1 == team2:
            st.error("⚠️ Please select two different teams")
        elif betting_tools is None:
            st.error("⚠️ Betting tools not initialized. Please refresh the page.")
        else:
            with st.spinner(f"Generating betting preview for {team1} vs {team2}..."):
                analysis = betting_tools.get_detailed_match_analysis(team1, team2, venue=venue)
                
                if "error" in analysis:
                    st.error(f"Error: {analysis['error']}")
                else:
                    st.markdown('<div class="inner-card">', unsafe_allow_html=True)
                    
                    st.markdown(f'<h3 style="color: #2DD4BF;">IPL Preview: {team1} vs {team2}</h3>', unsafe_allow_html=True)
                    
                    if venue:
                        st.markdown(f'<p class="muted-text" style="margin-bottom: 15px;">📍 Venue: {venue}</p>', unsafe_allow_html=True)
                    
                    st.markdown('<h4 style="color: #EAF2FF; margin-top: 20px; margin-bottom: 10px;">Fixture Analysis</h4>', unsafe_allow_html=True)
                    for point in analysis['fixture_analysis']:
                        formatted_point = format_fixture_analysis(point)
                        st.markdown(f'<p class="body-text" style="margin: 6px 0; line-height: 1.5;">{formatted_point}</p>', unsafe_allow_html=True)
                    
                    if venue:
                        st.markdown('<h4 style="color: #EAF2FF; margin-top: 20px;">Venue Insights</h4>', unsafe_allow_html=True)
                    else:
                        st.markdown('<h4 style="color: #EAF2FF; margin-top: 20px;">Key Stats & Trends</h4>', unsafe_allow_html=True)
                    
                    for insight in analysis['venue_insights']:
                        st.markdown(f'<p class="body-text">{insight}</p>', unsafe_allow_html=True)
                    
                    st.markdown('<h4 style="color: #EAF2FF; margin-top: 20px;">Recommended Bets & Odds</h4>', unsafe_allow_html=True)
                    for i, bet in enumerate(analysis['recommended_bets'], 1):
                        st.markdown(f'<div class="inner-card" style="background-color: #1C2A3A; margin: 10px 0;">', unsafe_allow_html=True)
                        st.markdown(f'<p style="color: #2DD4BF; font-weight: 600; font-size: 1.1em;">{i}. {bet["bet_type"]}: {bet["selection"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p style="color: #F59E0B; font-weight: 600;">Odds: {bet["odds"]} | Confidence: {bet["confidence"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="body-text">{bet["reasoning"]}</p>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<hr style="border-color: #2DD4BF; margin: 30px 0;">', unsafe_allow_html=True)
                    
                    st.markdown('<h4 style="color: #EAF2FF;">Detailed Analysis</h4>', unsafe_allow_html=True)
                    reasoning = analysis['detailed_reasoning']
                    
                    for section in reasoning['sections']:
                        st.markdown(f'<h5 style="color: #2DD4BF; margin-top: 15px;">{section["title"]}</h5>', unsafe_allow_html=True)
                        st.markdown(f'<p class="body-text">{section["content"]}</p>', unsafe_allow_html=True)
                    
                    st.markdown('<h4 style="color: #EAF2FF; margin-top: 20px;">Final Prediction</h4>', unsafe_allow_html=True)
                    st.markdown(f'<p class="body-text" style="font-weight: 600;">{reasoning["final_prediction"]}</p>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('<div class="inner-card" style="margin-top: 20px;">', unsafe_allow_html=True)
                    st.markdown('<h4 style="color: #2DD4BF;">📊 Team Statistics Comparison</h4>', unsafe_allow_html=True)
                    
                    col_stat1, col_stat2 = st.columns(2)
                    
                    with col_stat1:
                        st.markdown(f'<p class="body-text"><strong>{team1}</strong></p>', unsafe_allow_html=True)
                        team1_stats = analysis["team1_stats"]
                        st.markdown(f'<p class="muted-text">Strike Rate: {team1_stats["strike_rate"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="muted-text">Batting Average: {team1_stats["batting_average"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="muted-text">Death Overs SR: {team1_stats["strike_rate_balls_41_50"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="muted-text">1st Innings Avg: {team1_stats["first_innings_average"]}</p>', unsafe_allow_html=True)
                    
                    with col_stat2:
                        st.markdown(f'<p class="body-text"><strong>{team2}</strong></p>', unsafe_allow_html=True)
                        team2_stats = analysis["team2_stats"]
                        st.markdown(f'<p class="muted-text">Strike Rate: {team2_stats["strike_rate"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="muted-text">Batting Average: {team2_stats["batting_average"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="muted-text">Death Overs SR: {team2_stats["strike_rate_balls_41_50"]}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="muted-text">1st Innings Avg: {team2_stats["first_innings_average"]}</p>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👈 Select two teams from the sidebar and click 'Generate Betting Preview' to begin")

elif current_section == 'Highlights Package':
    st.markdown('<h2 class="section-title">🎬 Highlights Package</h2>', unsafe_allow_html=True)
    st.markdown('<p class="body-text">Post-match highlights from ball-by-ball data - Mumbai Indians vs Chennai Super Kings</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="inner-card">', unsafe_allow_html=True)
    st.markdown('<p class="body-text"><strong>Match:</strong> Mumbai Indians vs Chennai Super Kings | MA Chidambaram Stadium, Chennai | March 23, 2025</p>', unsafe_allow_html=True)
    st.markdown('<p class="body-text"><strong>Result:</strong> Chennai Super Kings won by 3 wickets</p>', unsafe_allow_html=True)
    st.markdown('<p class="body-text"><strong>Scores:</strong> Mumbai Indians 155/9 (20 overs) | Chennai Super Kings 158/7 (19.3 overs)</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="inner-card" style="margin-top: 15px;">', unsafe_allow_html=True)
    st.markdown('''
<h3 style="color: #2DD4BF; margin-bottom: 15px;">📝 Match Summary</h3>

<p class="body-text">Chennai Super Kings pulled off a thrilling 3-wicket victory over Mumbai Indians at the iconic MA Chidambaram Stadium in Chennai, chasing down 156 with 3 balls to spare in a nail-biting encounter.</p>

<h4 style="color: #EAF2FF; margin-top: 20px;">🏏 First Innings: Mumbai Indians - 155/9 (20 overs)</h4>

<p class="body-text">Mumbai Indians got off to a shaky start, losing captain Rohit Sharma (0 off 4 balls) in the very first over, caught off Khaleel Ahmed. The early wicket set the tone for a challenging innings on the spin-friendly Chepauk surface.</p>

<p class="body-text"><strong>Key Performances:</strong></p>
<ul class="body-text">
    <li><strong>Tilak Varma (31 off 25 balls, SR: 124.0)</strong> - Top-scored for MI with a composed knock, hitting 2 sixes including a massive one off Ravindra Jadeja in the 9th over</li>
    <li><strong>Suryakumar Yadav (29 off 26 balls, SR: 111.5)</strong> - Provided crucial support with a steady innings before being stumped by Noor Ahmad in the 11th over</li>
    <li><strong>Deepak Chahar (28 off 15 balls, SR: 186.7)</strong> - Explosive cameo in the death overs, providing much-needed impetus</li>
    <li><strong>Naman Dhir (17 off 12 balls, SR: 141.7)</strong> - Useful contribution in the middle order</li>
</ul>

<p class="body-text"><strong>Bowling Highlights:</strong></p>
<ul class="body-text">
    <li><strong>Noor Ahmad</strong> - Picked up crucial wickets including the prized scalp of Suryakumar Yadav (stumped) and Tilak Varma (LBW)</li>
    <li><strong>Ravindra Jadeja & Ravichandran Ashwin</strong> - The spin duo kept things tight in the middle overs, restricting MI to just 155</li>
    <li><strong>Khaleel Ahmed</strong> - Struck early with Rohit Sharma's wicket and also dismissed Ryan Rickelton (13 off 7) who was looking dangerous</li>
</ul>

<p class="body-text" style="font-style: italic; color: #9AA7B8;">Turning Point: The collapse from 52/3 to 87/4 in the middle overs, with Suryakumar Yadav's dismissal proving costly for Mumbai.</p>

<h4 style="color: #EAF2FF; margin-top: 25px;">🎯 Second Innings: Chennai Super Kings - 158/7 (19.3 overs)</h4>

<p class="body-text">Chasing 156, Chennai Super Kings showed composure and experience to get over the line despite losing wickets at regular intervals. The home crowd at Chepauk erupted as CSK sealed a memorable victory with 3 balls remaining.</p>

<p class="body-text"><strong>Match-Winning Moments:</strong></p>
<ul class="body-text">
    <li>Clinical chase execution despite pressure from MI bowlers</li>
    <li>Smart partnerships in the middle overs to keep the required rate manageable</li>
    <li>Experienced finishers holding their nerve in the final overs</li>
</ul>

<h4 style="color: #2DD4BF; margin-top: 25px;">⭐ Player of the Match Contenders</h4>
<ul class="body-text">
    <li><strong>Tilak Varma</strong> - Top scorer for MI with crucial 31 runs</li>
    <li><strong>Noor Ahmad</strong> - Match-turning spell with key wickets</li>
    <li><strong>CSK Finishers</strong> - Held nerves to chase down the target</li>
</ul>

<h4 style="color: #EAF2FF; margin-top: 25px;">📊 Key Statistics</h4>
<ul class="body-text">
    <li>Total Boundaries: MI hit multiple boundaries in the powerplay before spinners took control</li>
    <li>Powerplay Score: MI struggled early, losing 2 wickets in the first 6 overs</li>
    <li>Death Overs: Deepak Chahar's late blitz (28 off 15) pushed MI past 150</li>
    <li>Spin Impact: Chennai's spin trio of Jadeja, Ashwin, and Noor Ahmad dominated the middle overs</li>
</ul>

<p class="body-text" style="margin-top: 20px; font-weight: 600; color: #2DD4BF;">Final Verdict: A classic Chepauk thriller where Chennai Super Kings' experience and home advantage proved decisive in a low-scoring encounter. Mumbai Indians will rue their inability to build partnerships after losing early wickets.</p>
''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    

elif current_section == 'Journalist Preview':
    st.markdown('<h2 class="section-title">📰 Journalist Preview</h2>', unsafe_allow_html=True)
    st.markdown('<p class="body-text">Pre-match preview - Mumbai Indians vs Chennai Super Kings at MA Chidambaram Stadium</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="inner-card">', unsafe_allow_html=True)
    st.markdown('<p class="body-text"><strong>Fixture:</strong> Mumbai Indians vs Chennai Super Kings</p>', unsafe_allow_html=True)
    st.markdown('<p class="body-text"><strong>Venue:</strong> MA Chidambaram Stadium, Chepauk, Chennai</p>', unsafe_allow_html=True)
    st.markdown('<p class="body-text"><strong>Date:</strong> March 23, 2025</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="inner-card" style="margin-top: 15px;">', unsafe_allow_html=True)
    st.markdown('''
<h3 style="color: #2DD4BF; margin-bottom: 15px;">🏏 Match Preview</h3>

<p class="body-text">The iconic rivalry between Mumbai Indians and Chennai Super Kings resumes at the spin-friendly confines of MA Chidambaram Stadium in Chennai, where the home side will look to leverage their fortress advantage against the five-time champions. With both teams boasting formidable batting lineups and quality spin options, this encounter promises to be a tactical chess match on the turning Chepauk surface.</p>

<h4 style="color: #EAF2FF; margin-top: 20px;">📊 Team Form & Strengths</h4>

<p class="body-text"><strong>Mumbai Indians</strong> enter this contest with a well-balanced squad featuring explosive batting depth. Their team statistics reveal a strike rate of 139.2% with a boundary percentage of 17.8%, showcasing their aggressive intent. The five-time champions excel in the powerplay (SR: 142.5%) and death overs (SR: 156.3%), making them dangerous throughout the innings. However, their average vs spin (24.8) suggests vulnerability against quality tweakers on turning tracks.</p>

<p class="body-text"><strong>Chennai Super Kings</strong> bring their trademark experience and tactical acumen to their home fortress. With an impressive home win rate of 68% at Chepauk and strike rate of 136.8%, CSK balance aggression with stability. Their strength lies in playing spin (SR vs Spin: 128.4%) and finishing games in familiar conditions. The second innings average of 28.3 highlights their chasing prowess, crucial for home games at Chepauk.</p>

<h4 style="color: #2DD4BF; margin-top: 25px;">⭐ Players to Watch - Mumbai Indians</h4>

<p class="body-text"><strong>Suryakumar Yadav</strong> - The 360-degree batsman has been in scintillating form with 1,847 runs at an average of 32.2 and strike rate of 147.8 in recent IPL seasons. His ability to score against both pace (SR: 149.2) and spin (SR: 145.6) makes him a nightmare for bowlers. Particularly dangerous in the middle overs (balls 21-40, SR: 158.3), SKY's innovative strokeplay and ability to find boundaries at will (18.9% boundary percentage) will be crucial on a surface where timing can be tricky. His wagon wheel data shows strength in the leg-side arc, and he'll look to exploit any gaps in CSK's field placements.</p>

<p class="body-text"><strong>Tilak Varma</strong> - The young left-hander has emerged as MI's crisis man with 1,456 runs at an impressive average of 36.4. His strike rate of 138.5 reflects maturity beyond his years, and crucially, he averages 38.2 against spin bowling. Tilak's ability to accelerate in the death overs (SR: 152.7 in balls 41-50) provides MI with a finisher who can bat through the innings. His recent form and composure under pressure make him a key player in Chennai's challenging conditions.</p>

<h4 style="color: #2DD4BF; margin-top: 25px;">⭐ Players to Watch - Chennai Super Kings</h4>

<p class="body-text"><strong>Ravindra Jadeja</strong> - The ultimate Chepauk specialist, Jadeja's all-round brilliance will be pivotal. As a bowler, he's economical in the middle overs and picks up crucial wickets with his accurate left-arm spin. With the bat, his ability to score quick runs in the death overs (career SR of 135+ in final overs) makes him invaluable. His fielding prowess adds another dimension, and on a surface he knows intimately, Jadeja could be the difference between the two sides.</p>

<p class="body-text"><strong>Ravichandran Ashwin</strong> - The crafty off-spinner returns to his home ground with a wealth of experience and variations. Ashwin's economy rate at Chepauk is exceptional, and his ability to outfox batsmen with carrom balls, doosras, and subtle changes of pace makes him a constant threat. Against MI's right-hand heavy lineup, Ashwin's match-ups look favorable, particularly in the middle overs where he can strangle the scoring rate and create pressure.</p>

<h4 style="color: #EAF2FF; margin-top: 25px;">🏟️ Venue Profile - MA Chidambaram Stadium</h4>

<p class="body-text">The iconic Chepauk stadium is renowned as one of India's most spin-friendly venues, with historical data showing 62% of wickets falling to spinners. The average first innings score hovers around 165-170, with teams batting second enjoying a slight advantage (win percentage: 54%). The pitch typically offers turn from the outset, with the square boundaries (62m) shorter than the straight hits (68m), encouraging batsmen to play across the line.</p>

<p class="body-text">Weather conditions in Chennai during March are typically hot and humid (32-34°C), with dew potentially playing a factor in the second innings. The venue's red soil surface tends to slow down as the match progresses, making batting increasingly challenging. Teams winning the toss often prefer to chase, banking on dew to negate the spinners' impact later in the game.</p>

<h4 style="color: #2DD4BF; margin-top: 25px;">🔑 Key Talking Points</h4>

<p class="body-text"><strong>Spin vs Power:</strong> The central battle will be between CSK's spin trio (Jadeja, Ashwin, and their mystery spinner) against MI's power-hitters. Mumbai's aggressive approach (balls per boundary: 5.6) could backfire on a turning track, while CSK's experience in these conditions (home win rate: 68%) gives them a psychological edge.</p>

<p class="body-text"><strong>Powerplay Dominance:</strong> Mumbai's strength in the first six overs (SR: 142.5%) will be tested by CSK's new-ball bowlers. If MI can get off to a flying start and negate the spin threat early, they could post a challenging total. Conversely, early wickets could expose their middle order to sustained spin pressure.</p>

<p class="body-text"><strong>Death Overs Execution:</strong> Both teams boast strong finishers, but execution in the final five overs will be crucial. MI's death bowling has been vulnerable (conceding 10+ per over), while CSK's experienced campaigners know how to close out games at Chepauk. The team that holds its nerve in the pressure moments will likely prevail.</p>

<h4 style="color: #EAF2FF; margin-top: 25px;">📈 Prediction</h4>

<p class="body-text">This promises to be a low-scoring thriller with spin playing a decisive role. Chennai Super Kings' familiarity with conditions and superior spin-batting record gives them a narrow edge, particularly if they win the toss and chase. Expect a total in the 155-165 range, with the team that adapts better to the turning surface emerging victorious. Mumbai Indians will need their big guns to fire early and their spinners to match CSK's quality to overcome the home advantage. A close contest is on the cards, with CSK slight favorites at 55-45.</p>
''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="inner-card" style="margin-top: 20px; background: linear-gradient(135deg, #1C2A3A 0%, #223347 100%); border-left: 4px solid #2DD4BF;">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: #2DD4BF;">💼 Business Value</h4>', unsafe_allow_html=True)
    st.markdown('''
<p class="body-text">This technology can be used for:</p>
<ul class="body-text">
    <li>✅ <strong>Automated pre-match content</strong> for sports websites and apps</li>
    <li>✅ <strong>Data-driven journalism</strong> without manual analysis</li>
    <li>✅ <strong>Personalized match previews</strong> for different audience segments</li>
    <li>✅ <strong>Social media content generation</strong> for match buildup</li>
    <li>✅ <strong>Multi-language previews</strong> with AI translation</li>
    <li>✅ <strong>Scalable content creation</strong> for multiple matches simultaneously</li>
</ul>
<p class="muted-text" style="margin-top: 10px;">💡 This preview is crafted using comprehensive IPL datasets including player statistics, team performance data, and venue intelligence from the Sample_IPL_Matches.csv and related datasets.</p>
''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<p class="muted-text" style="text-align: center;">Built with LangChain + Claude Sonnet 4.5 | IPL Data</p>', unsafe_allow_html=True)
