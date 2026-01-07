# 🤖 AI Agents Documentation

## Overview
This project uses **AI Agents** powered by **Claude Sonnet 4** (Anthropic) to provide intelligent cricket analytics and insights.

---

## Agents Used in This Project

### 1. **EnhancedCricketAgent** (Primary AI Agent)
**Location:** `agent_enhanced.py`

**Type:** ReAct (Reasoning + Acting) Agent with Tool Calling

**LLM Model:** Claude Sonnet 4 (claude-sonnet-4)

**Framework:** LangChain with LangChain Classic

**Purpose:** 
- Provides intelligent analysis of IPL player statistics
- Answers natural language questions about cricket players
- Uses multiple tools to fetch and analyze data
- Maintains conversation history for context-aware responses

**Tools Available to Agent:**
1. `get_player_stats` - Comprehensive batting statistics
2. `get_player_line_length_analysis` - Line & length performance analysis
3. `get_player_wagon_wheel_analysis` - Scoring zones and boundary distribution
4. `get_player_strengths_weaknesses` - Top 2 strengths and weaknesses
5. `get_bowling_plan` - Strategic bowling plans to dismiss players
6. `get_all_players_list` - List of available players

**Key Features:**
- **Autonomous Decision Making:** Agent decides which tools to use based on user questions
- **Multi-Step Reasoning:** Can chain multiple tool calls to answer complex questions
- **Data-Driven Insights:** Never makes up statistics, always uses actual data
- **Conversational Memory:** Maintains context across multiple questions

**Architecture:**
```
User Question → Agent (Claude Sonnet 4) → Tool Selection → Data Retrieval → Analysis → Response
                    ↑                                                              ↓
                    └──────────────── Conversation History ──────────────────────┘
```

**Example Capabilities:**
- "How does Virat Kohli perform in death overs?" → Uses `get_player_stats` to fetch death overs SR
- "What are his weaknesses?" → Uses `get_player_strengths_weaknesses` and `get_player_line_length_analysis`
- "Compare him with Rohit Sharma" → Fetches stats for both players and provides comparison

---

## Agent Configuration

### System Prompt
The agent is configured with specific instructions:
- Act as an expert cricket analyst specializing in IPL statistics
- Always use tools to fetch data (never make up statistics)
- Provide insights backed by actual data
- Include specific numbers and metrics
- State clearly when data is insufficient
- Provide actionable insights and comparisons

### Parameters
- **Temperature:** 0 (deterministic, factual responses)
- **Max Iterations:** 10 (prevents infinite loops)
- **Verbose:** True (shows reasoning steps in logs)
- **Handle Parsing Errors:** True (graceful error handling)

---

## Tool Implementation

### Tool Architecture
Each tool is wrapped as a **LangChain StructuredTool** with:
- **Function:** Python method from `EnhancedCricketAnalysisTools`
- **Name:** Descriptive tool name
- **Description:** Clear explanation of what the tool does (helps agent decide when to use it)
- **Args Schema:** Pydantic model defining input parameters

### Example Tool Definition
```python
StructuredTool.from_function(
    func=self.tools_instance.get_player_stats,
    name="get_player_stats",
    description="Get comprehensive batting statistics for a player including runs, average, strike rate, and performance vs pace/spin. Use this to get overall player performance metrics.",
    args_schema=PlayerNameInput  # Pydantic model with player_name field
)
```

---

## Data Sources for Agent

The agent has access to three comprehensive datasets:

1. **IPL_21_24_Batting.csv** (50 players, 15 metrics)
   - Overall statistics (runs, average, strike rate)
   - Performance vs pace/spin
   - Phase-wise performance (powerplay, middle, death)
   - Boundary percentages

2. **batter_line_length_SR_long.csv**
   - Strike rates for 9 line/length combinations
   - Identifies technical weaknesses
   - Best and worst zones for each player

3. **Batter_WagonWheel.csv**
   - Scoring zones on the field
   - Boundary distribution by zone
   - Strong and weak scoring areas

---

## Agent Workflow

### Question Processing Flow
1. **User Input:** Natural language question about a player
2. **Agent Reasoning:** Claude Sonnet 4 analyzes the question
3. **Tool Selection:** Agent decides which tool(s) to use
4. **Data Retrieval:** Tools fetch data from CSV files
5. **Analysis:** Agent processes the data
6. **Response Generation:** Provides insights with specific numbers
7. **Conversation Update:** Stores in history for context

### Multi-Turn Conversations
The agent maintains conversation history, enabling:
- Follow-up questions without repeating context
- References to previous answers
- Progressive deep-dives into player analysis

---

## Non-Agent Components

While the project has one primary AI agent, it also includes:

### 1. **EnhancedCricketAnalysisTools** (Tool Class)
**Location:** `tools_enhanced.py`

**Type:** Data processing and analysis class (NOT an agent)

**Purpose:** Provides structured data access methods that the agent uses as tools

### 2. **FantasyAnalysisTools** (Tool Class)
**Location:** `fantasy_tools.py`

**Type:** Fantasy cricket analysis class (NOT an agent)

**Purpose:** Provides venue intelligence, match situation analysis, and fantasy picks

---

## Agent vs Non-Agent Distinction

| Component | Type | Decision Making | Data Access |
|-----------|------|----------------|-------------|
| **EnhancedCricketAgent** | AI Agent | Autonomous (LLM-powered) | Via tools |
| **EnhancedCricketAnalysisTools** | Tool Class | Deterministic (rule-based) | Direct CSV access |
| **FantasyAnalysisTools** | Tool Class | Deterministic (rule-based) | Direct CSV access |

---

## Why Use an Agent?

### Benefits of Agent Architecture

1. **Natural Language Interface:** Users ask questions in plain English
2. **Intelligent Tool Selection:** Agent decides which data to fetch
3. **Multi-Step Reasoning:** Can combine multiple data sources
4. **Contextual Awareness:** Maintains conversation history
5. **Flexible Queries:** Handles variations in question phrasing
6. **Explainability:** Can explain its reasoning process

### Example: Agent vs Traditional Approach

**Traditional Approach:**
```python
# User must know exact function names and parameters
stats = get_player_stats("Virat Kohli")
line_length = get_player_line_length_analysis("Virat Kohli")
# User must manually combine and interpret data
```

**Agent Approach:**
```python
# User asks naturally
agent.query("What are Virat Kohli's weaknesses against spin in the powerplay?")
# Agent automatically:
# 1. Fetches player stats
# 2. Gets line/length analysis
# 3. Filters for spin bowling
# 4. Focuses on powerplay phase
# 5. Provides comprehensive answer
```

---

## Integration with Streamlit UI

The agent is integrated into the Streamlit app via:

1. **Caching:** `@st.cache_resource` ensures agent is initialized once
2. **API Key Management:** Securely loads Anthropic API key
3. **Interactive UI:** Text input for questions, buttons for sample questions
4. **Response Display:** Formatted output with markdown styling
5. **Conversation Management:** Reset button to clear history

---

## Sample Questions Supported

The agent can answer questions like:

### Individual Analysis
- "How does [player] perform in death overs?"
- "What are [player]'s weaknesses?"
- "Analyze [player]'s boundary-hitting patterns"

### Comparisons
- "Compare [player1] and [player2]'s strike rates"
- "Who is more consistent: [player1] or [player2]?"
- "Who performs better against spin?"

### Strategic
- "Should I pick [player] as captain?"
- "What's the best bowling plan against [player]?"
- "How does [player] handle pressure situations?"

---

## Technical Stack

- **LLM:** Claude Sonnet 4 (Anthropic)
- **Agent Framework:** LangChain Classic
- **Tool Framework:** LangChain StructuredTool
- **Data Processing:** Pandas
- **UI Framework:** Streamlit
- **API Integration:** langchain-anthropic

---

## Future Enhancements

Potential agent improvements:
1. **Multi-Agent System:** Separate agents for batting, bowling, fantasy
2. **Memory Persistence:** Save conversations across sessions
3. **RAG Integration:** Vector database for historical match data
4. **Agentic Workflows:** Complex multi-step analysis pipelines
5. **Tool Expansion:** Add more data sources (weather, pitch reports, etc.)

---

## Summary

**Total Agents in Project: 1**

- **EnhancedCricketAgent** - ReAct agent powered by Claude Sonnet 4 with 6 tools for comprehensive IPL player analysis

The agent architecture enables natural language interaction with cricket data, providing intelligent, data-driven insights that would be difficult to achieve with traditional rule-based systems.
