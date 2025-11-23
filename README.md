# InsightGenie 🧠


---

## Overview 🚀
**InsightGenie** is an AI-powered assistant that helps users **query, visualize, and generate reports** from CSV data using **natural language queries**. Transform complex network performance metrics into actionable insights—no coding required!



---

## Key Features ✨
- **Natural Language Queries:** Ask questions in everyday language via OpenAI API.  
- **Dynamic Visualizations:** Stunning interactive charts with Plotly for bandwidth, latency, and resource allocation.  
- **LangChain Integration:** Processes queries intelligently using DataFrame agents.  
- **Query History:** Keep track of previous queries and responses with Streamlit.  
- **PDF Reports:** Export professional PDF reports with ReportLab for easy sharing.

---

## Why This Matters 💡
InsightGenie makes **data analysis accessible to everyone**, turning raw data into **actionable insights**. Perfect for teams that want **faster, smarter, and more interactive decision-making**.

---

## Installation ⚡

```bash
# Clone the repo
git clone https://github.com/yourusername/InsightGenie.git
cd InsightGenie

# Create virtual environment
python -m venv venv
# Activate
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY='your_api_key'  # Windows: setx OPENAI_API_KEY "your_api_key"

# Run the app
streamlit run main.py
