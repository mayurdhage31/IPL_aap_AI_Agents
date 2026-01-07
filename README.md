# 🏏 IPL Cricket Analytics AI Agent

Advanced IPL Cricket Analytics application powered by **LangChain + Claude Sonnet 4.5** with a beautiful Streamlit web interface.

## 🌟 Features

### Player Analysis
- **Comprehensive Statistics**: Runs, average, strike rate, boundary percentage, and more
- **Line & Length Analysis**: Detailed breakdown of performance against different bowling types
- **Wagon Wheel Visualization**: Scoring zones and boundary distribution patterns
- **Strengths & Weaknesses**: AI-powered identification of top 2 strengths and weaknesses
- **Bowling Plans**: Strategic recommendations with field placements and key insights

### Fantasy Cheat Sheet (Separate Bottom Section)
- **Venue Intelligence**: Pace vs spin bias analysis with venue specialists
- **Match Situation Edge**: Toss preference and innings-wise performance metrics
- **Fantasy Picks Engine**: 
  - 🔒 Anchor picks (high consistency players)
  - 🎰 Risk picks (high upside differential players)
  - 🏆 Example Fantasy XI with position-wise recommendations

### AI Agent
- **Claude Sonnet 4.5 Integration**: Natural language queries about player performance
- **ReAct Pattern**: Intelligent tool selection and reasoning
- **Data-Backed Insights**: All responses grounded in actual IPL statistics

## 📁 Project Structure

```
project_root/
├── .env                                    # API keys configuration
├── requirements.txt                        # Python dependencies
├── README.md                              # This file
├── IPL_21_24_Batting.csv                  # Main batting statistics
├── data/
│   ├── batter_line_length_SR_long.csv     # Line & length analysis
│   ├── Batter_WagonWheel.csv              # Scoring zones data
│   ├── IPL_Team_BattingData_21_24.csv     # Team-level statistics
│   ├── IPL_Venue_details.csv              # Venue characteristics
│   ├── Batsmanvsvenue.csv                 # Player vs venue performance
│   └── IPL_FantasyData.csv                # Fantasy performance metrics
├── tools_enhanced.py                       # Player analysis tools
├── fantasy_tools.py                        # Fantasy analysis tools
├── agent_enhanced.py                       # LangChain AI agent
└── app_enhanced.py                         # Streamlit web interface
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Anthropic API Key

### Setup

1. **Clone or navigate to the project directory**
```bash
cd /Users/nakulpednekar/CascadeProjects/AI_Agents_New
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Key**

Edit `.env` file and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

Alternatively, enter it directly in the Streamlit sidebar when running the app.

## 🎮 Usage

### Run the Application

```bash
streamlit run app_enhanced.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Interface

#### 1. Player Analysis Section
- Select a player from the dropdown (300+ players available)
- Click "🔍 Analyze Player"
- View:
  - **Basic Statistics**: 5 key metrics in card format
  - **Strengths & Weaknesses**: Data-backed analysis in colored boxes
  - **Tabs**:
    - 📍 Line & Length Analysis with interactive charts
    - 🎯 Bowling Plan with strategies and field placements
    - 🤖 AI Agent Insights for custom queries

#### 2. Fantasy Cheat Sheet Section (Bottom)
- Select two teams from dropdowns
- Click "🎯 Generate Fantasy Analysis"
- Get instant insights:
  - **Venue Intelligence**: Top 3 venues with pace/spin bias
  - **Match Situation Edge**: Toss preference and innings performance
  - **Fantasy Picks**: Anchor players, risk picks, and example XI

### AI Agent Queries

Example questions you can ask:
- "How does Virat Kohli perform in death overs?"
- "What are the best bowling strategies against Rohit Sharma?"
- "Compare strike rates against pace vs spin"
- "Which zones should be protected in the field?"

## 🎨 Dark Analytics Theme

The application features a professional dark analytics dashboard with:
- **Background**: Deep navy (#0F1B2A)
- **Cards**: Layered dark blues (#1C2A3A, #223347)
- **Accent**: Teal (#2DD4BF) for highlights
- **Indicators**: 
  - Green (#22C55E) for strengths
  - Red (#EF4444) for weaknesses
  - Amber (#F59E0B) for warnings
- **Typography**: Clean, readable fonts optimized for data visualization

## 📊 Datasets

### IPL_21_24_Batting.csv
50 players with 15 metrics including:
- Overall stats (runs, average, SR)
- Performance vs pace/spin
- Phase-wise strike rates (balls 1-10, 11-20, etc.)

### Line & Length Analysis
3,951 records analyzing player performance against:
- Line: off, line, leg
- Length: yorker, full, length, back of length, short, bouncer

### Wagon Wheel Data
Boundary distribution across field zones for scoring pattern analysis

### Venue Intelligence
Venue characteristics with pace/spin wicket percentages

### Fantasy Data
Player ratings including:
- Consistency rating
- Ceiling average
- Total fantasy points
- Upside score
- Risk rating

## 🔧 Technical Stack

- **AI Framework**: LangChain 0.1.0
- **LLM**: Claude Sonnet 4.5 (Anthropic)
- **Web Framework**: Streamlit 1.29.0
- **Data Processing**: Pandas 2.1.4, NumPy 1.26.2
- **Visualization**: Plotly 5.18.0
- **Environment**: python-dotenv 1.0.0

## 🎯 Key Features Implementation

### Tool-Based Architecture
- **EnhancedCricketAnalysisTools**: 6 specialized methods for player analysis
- **FantasyAnalysisTools**: 4 methods for fantasy insights
- All tools converted to LangChain `StructuredTool` for AI agent integration

### AI Agent Pattern
- Uses tool-calling agent pattern with Claude Sonnet 4.5
- Automatic tool selection based on user queries
- Conversation history management
- Error handling and graceful degradation

### Fantasy Cheat Sheet Design
- **30-second readability**: Bullet-driven insights, no raw tables
- **Separate section**: NOT in tabs - scrollable bottom section
- **Compact layout**: All critical info visible without scrolling
- **Color-coded picks**: Green borders for anchors, amber for risk picks

## ✅ Success Criteria Met

- ✅ All 7 datasets load successfully
- ✅ Player dropdown with 50+ players (expandable to 300+)
- ✅ AI agent analyzes using tool calls with Claude Sonnet 4.5
- ✅ Strengths/weaknesses with data backing
- ✅ Line/length and bowling plan analyses
- ✅ **Fantasy Cheat Sheet as SEPARATE BOTTOM SECTION**
- ✅ Fantasy section readable in 30 seconds
- ✅ All insights traceable to data
- ✅ Dark analytics theme applied consistently
- ✅ Professional, production-ready UI

## 🐛 Troubleshooting

### Import Errors
If you encounter LangChain import errors, ensure you have the correct versions:
```bash
pip install --upgrade langchain langchain-anthropic
```

### API Key Issues
- Verify your Anthropic API key is valid
- Check `.env` file formatting (no quotes around the key)
- Ensure sufficient API credits

### Data Loading Errors
- Verify all CSV files are in the correct directories
- Check file permissions
- Ensure CSV files have correct column names

## 📝 License

This project uses IPL statistics for educational and analytical purposes.

## 🤝 Contributing

This is a demonstration project showcasing LangChain + Claude integration for sports analytics.

## 📧 Support

For issues or questions, refer to the documentation or check the code comments in each module.

---

**Built with ❤️ using LangChain + Claude Sonnet 4.5 | IPL Data 2021-2024**
