# Campaign Reporting Copilot 📊

AI-powered campaign analysis tool that transforms Meta/Google/GA4 exports into human-readable insights with actionable next steps.

## 🎯 What It Does

The Campaign Reporting Copilot:
1. **Analyzes** your campaign data with period comparisons (WoW/YoY)
2. **Identifies** key trends, top performers, and problem areas
3. **Generates** AI-powered insights and storytelling summaries
4. **Provides** prioritized action items ("What should I do?")

## 🏗️ Architecture

- **Backend**: FastAPI + Python
  - CSV data processing with Pandas
  - Period comparison analytics (Week-over-Week, Year-over-Year)
  - OpenAI GPT-4 integration for insights
  - RESTful API endpoints

- **Frontend**: Streamlit
  - Interactive CSV upload
  - Period selection interface
  - Real-time analysis visualization
  - Action-oriented recommendations display

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key
- pip (Python package manager)

## 🚀 Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 📊 CSV Data Format

Your campaign export CSV should include these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `week_start_date` | Week start date | 2025-03-03 |
| `year_week` | Year + week number | 2025-W09 |
| `platform` | Platform name | Meta, Google, YouTube |
| `channel` | Channel type | Paid Social, Search |
| `country` | Country code | TR |
| `campaign_name` | Campaign name | Spring Sale - Prospecting |
| `objective` | Campaign objective | Conversions, Awareness |
| `impressions` | Total impressions | 339073 |
| `clicks` | Total clicks | 5029 |
| `cost` | Total cost | 1499.32 |
| `conversions` | Total conversions | 202 |
| `revenue` | Total revenue | 189653.3 |
| `ctr` | Click-through rate | 0.0148 |
| `cpc` | Cost per click | 0.2981 |
| `cpm` | Cost per mille | 4.4218 |
| `cvr` | Conversion rate | 0.0402 |
| `cpa` | Cost per acquisition | 7.4224 |
| `roas` | Return on ad spend | 126.4929 |

**Note**: Calculated metrics (CTR, CPC, etc.) can be auto-calculated by the system if not present.

A sample CSV file is included: `campaign_metrics_sample.csv`

## 🎮 Usage

### 1. Start the Backend API

Open a terminal and run:

```bash
cd backend
python main.py
```

The API will start on `http://localhost:8000`

You can verify it's running by visiting: `http://localhost:8000/health`

### 2. Start the Streamlit Frontend

Open a **new terminal** and run:

```bash
cd frontend
streamlit run app.py
```

The Streamlit app will open in your browser (usually `http://localhost:8501`)

### 3. Analyze Your Campaigns

1. **Upload CSV**: Click "Upload Campaign CSV" in the sidebar
2. **Select Period**: Choose the date range you want to analyze
3. **Choose Comparison Mode**: 
   - WoW (Week over Week)
   - YoY (Year over Year)
4. **Click "Analyze Campaigns"**: Wait for AI analysis (15-30 seconds)
5. **Review Results**:
   - Executive Summary
   - Problem Areas
   - Next Best Actions (prioritized)
   - Performance visualizations

## 📁 Project Structure

```
media/
├── backend/
│   ├── main.py              # FastAPI application
│   └── models.py            # Pydantic models
├── frontend/
│   └── app.py               # Streamlit application
├── campaign_metrics_sample.csv  # Sample data
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔍 API Endpoints

### POST /analyze
Analyzes campaign data and returns AI-generated insights.

**Request Body:**
```json
{
  "metrics": [
    {
      "week_start_date": "2025-03-03",
      "platform": "Meta",
      "campaign_name": "Spring Sale",
      "impressions": 339073,
      "clicks": 5029,
      "cost": 1499.32,
      "conversions": 202,
      "revenue": 189653.3
    }
  ],
  "current_period": {
    "start": "2025-03-31",
    "end": "2025-04-28"
  },
  "compare_mode": "WoW"
}
```

**Response:**
```json
{
  "summary": [
    {"text": "Total spend increased 18% compared to previous period"}
  ],
  "problem_areas": [
    {"text": "YouTube campaign ROAS dropped to 0.4 despite increased spend"}
  ],
  "next_best_actions": [
    {
      "area": "YouTube - Always On Brand",
      "description": "Reduce budget by 20% and test new creative with stronger first 3 seconds",
      "priority": "high"
    }
  ]
}
```

### GET /health
Health check endpoint to verify the API is running.

## 🧠 How It Works

1. **Data Processing**
   - Uploads and validates CSV data
   - Converts dates and normalizes metrics
   - Calculates derived KPIs (CTR, ROAS, etc.)

2. **Period Comparison**
   - Aggregates data for current period
   - Calculates previous period based on mode (WoW/YoY)
   - Computes percentage changes

3. **Insight Extraction**
   - Identifies top spenders and performers
   - Detects red flags (declining ROAS + increasing cost)
   - Finds funnel issues (high CTR, low CVR)

4. **AI Analysis**
   - Sends structured data to OpenAI GPT-4
   - Uses specialized prompt for marketing insights
   - Returns JSON with summary, problems, and actions

5. **Visualization**
   - Displays insights in human-readable format
   - Shows prioritized action items
   - Renders interactive charts and tables

## 🎨 Features

✅ **Smart Period Comparison** - Compare WoW or YoY automatically  
✅ **AI-Powered Insights** - GPT-4 analyzes your data like a marketing expert  
✅ **Actionable Recommendations** - Prioritized next steps (High/Medium/Low)  
✅ **Multi-Platform Support** - Meta, Google, YouTube, and more  
✅ **Interactive Visualizations** - Charts and tables for deeper analysis  
✅ **Export-Ready Format** - Works with standard platform exports  

## 🔧 Troubleshooting

**Backend won't start:**
- Make sure port 8000 is not in use
- Verify `.env` file has valid OPENAI_API_KEY
- Check Python version (3.9+)

**Frontend can't connect to backend:**
- Ensure backend is running on localhost:8000
- Check firewall settings
- Verify API_URL in `frontend/app.py`

**Analysis fails or times out:**
- Check OpenAI API key is valid
- Verify CSV format matches expected schema
- Ensure selected date range has data

**CSV upload error:**
- Verify all required columns are present
- Check date format is YYYY-MM-DD
- Ensure numeric columns don't have text values

## 📝 Future Enhancements

- [ ] Support for more platforms (TikTok, LinkedIn, etc.)
- [ ] Automated email reporting
- [ ] Historical trend analysis
- [ ] Budget optimization recommendations
- [ ] A/B test insights
- [ ] Multi-user dashboard
- [ ] Database integration for data persistence

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips

- Use **WoW comparison** for quick week-to-week checks
- Use **YoY comparison** for seasonal trend analysis
- Upload at least 8 weeks of data for better insights
- Review "Next Best Actions" daily to stay proactive
- Export from your ad platforms weekly for consistent monitoring

## 🆘 Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section
2. Review the API logs in the terminal
3. Verify your CSV format matches the sample
4. Ensure OpenAI API has sufficient credits

---

**Built with ❤️ using FastAPI, Streamlit, and OpenAI GPT-4**

