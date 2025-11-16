# Campaign Reporting Copilot 📊

AI-powered campaign analysis tool that transforms Meta/Google/GA4 exports into human-readable insights with actionable next steps.

---

## ⚡ Quick Start (3 Commands)

```bash
# 1. Clone and install
git clone https://github.com/keeptalking83/Campaign-Reporting-Copilot.git
cd Campaign-Reporting-Copilot
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 2. Set your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > env

# 3. Start both servers (use 2 separate terminals)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000  # Terminal 1 - Backend API
streamlit run frontend/app.py                                  # Terminal 2 - Frontend UI
```

Then open http://localhost:8501 and upload your campaign CSV! 🚀

**Note:** The backend automatically reads the `env` file, no need to export manually.

---

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

## 🚀 Quick Start Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/keeptalking83/Campaign-Reporting-Copilot.git
cd Campaign-Reporting-Copilot
```

### Step 2: Set Up Python Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You'll see `(venv)` appear in your terminal when the virtual environment is active.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn (backend server)
- Streamlit (frontend interface)
- Pandas (data processing)
- OpenAI (AI analysis)
- Plotly (visualizations)

### Step 4: Set Up Your OpenAI API Key

**Option A: Using Environment File (Recommended)**

1. Create a file named `env` (no extension) in the project root
2. Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Option B: Using Terminal Export**

**macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"
```

💡 **How to get an OpenAI API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Step 5: Verify Installation

Check if the backend is accessible:
```bash
python backend/main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Press `Ctrl+C` to stop the server.

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

## 🎮 How to Run the System

### Starting the Backend API (Terminal 1)

1. **Open your first terminal**
2. **Navigate to the project directory:**
```bash
cd Campaign-Reporting-Copilot
```

3. **Activate virtual environment:**

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

4. **Start the backend server:**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Command explained:**
- `backend.main:app` - Points to the FastAPI app instance
- `--reload` - Auto-restart on code changes (development mode)
- `--host 0.0.0.0` - Accept connections from any IP
- `--port 8000` - Run on port 8000

✅ **Success indicators:**
- You should see: `✅ OpenAI API key loaded successfully`
- Then: `INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)`
- And: `INFO: Started reloader process`
- Open http://localhost:8000/health in your browser
- You should see: `{"status":"healthy"}`

⚠️ **If you see "WARNING: OPENAI_API_KEY not found":**
- Check that your `env` file exists in the project root
- Verify it contains: `OPENAI_API_KEY=sk-your-key-here`
- Make sure there are no extra spaces or quotes

⚠️ **Keep this terminal open!** Don't close it while using the app.

---

### Starting the Frontend (Terminal 2)

1. **Open a NEW terminal window/tab**
2. **Navigate to the project directory:**
```bash
cd Campaign-Reporting-Copilot
```

3. **Activate virtual environment:**

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

4. **Start the Streamlit app:**
```bash
streamlit run frontend/app.py
```

✅ **Success indicators:**
- Your browser should automatically open to http://localhost:8501
- You should see "Campaign Reporting Copilot" interface
- If browser doesn't open, manually go to http://localhost:8501

---

### Using the Application

#### Step 1: Upload Your Campaign Data
- Click **"Upload Campaign CSV"** in the left sidebar
- Select your campaign export file (CSV format)
- Wait for the success message

#### Step 2: Select Analysis Period
- Use the **"Current Period"** date picker
- Choose the date range you want to analyze
- Default is the last 4 weeks

#### Step 3: Choose Comparison Mode
- **WoW (Week over Week)**: Compare with previous week
  - Example: Week of Nov 4-10 vs Week of Oct 28-Nov 3
- **YoY (Year over Year)**: Compare with same period last year
  - Example: Nov 2024 vs Nov 2023

#### Step 4: Run Analysis
- Click **"🚀 Analyze Campaigns"** button
- Wait 15-30 seconds for AI analysis
- The system will:
  - Process your data
  - Calculate metrics and comparisons
  - Generate AI-powered insights
  - Create visualizations

#### Step 5: Review Results
You'll see four main sections:

1. **📝 Executive Summary**
   - High-level overview of performance
   - Key trends and changes
   - Overall spend and ROAS

2. **⚠️ Problem Areas**
   - Campaigns with declining ROAS
   - Budget inefficiencies
   - Conversion funnel issues

3. **🎯 Next Best Actions**
   - Prioritized recommendations (High/Medium/Low)
   - Specific action items per campaign
   - What to do immediately

4. **📊 Performance Visualizations**
   - Cost & Revenue charts
   - ROAS by campaign
   - CTR, CVR, CPA metrics
   - Detailed data tables

---

### Stopping the System

**To stop the backend:**
1. Go to Terminal 1 (where backend is running)
2. Press `Ctrl+C`

**To stop the frontend:**
1. Go to Terminal 2 (where Streamlit is running)
2. Press `Ctrl+C`

**To deactivate virtual environment:**
```bash
deactivate
```

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

### Problem: Backend won't start

**Error: `ModuleNotFoundError`**
- ❌ You forgot to activate virtual environment
- ✅ Solution: Run `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)

**Error: `Address already in use`**
- ❌ Port 8000 is being used by another application
- ✅ Solution: 
  ```bash
  # macOS/Linux - Find and kill process on port 8000
  lsof -ti:8000 | xargs kill -9
  
  # Windows - Find and kill process on port 8000
  netstat -ano | findstr :8000
  taskkill /PID <PID_NUMBER> /F
  ```

**Error: `OPENAI_API_KEY not found`**
- ❌ Environment variable not set
- ✅ Solution:
  - Check your `env` file exists and has the correct API key
  - For macOS/Linux: Run `export $(cat env | xargs)` before starting backend
  - For Windows: Set the variable manually or restart terminal after creating `env`

**Error: `Python version not supported`**
- ❌ Python version is below 3.9
- ✅ Solution: Install Python 3.9 or higher from https://www.python.org/downloads/

---

### Problem: Frontend can't connect to backend

**Error: `Cannot connect to API. Make sure the backend is running on port 8000`**
- ❌ Backend is not running
- ✅ Solution: Start the backend first (see "Starting the Backend API" section)

**Error: Page shows "Connection refused"**
- ❌ Wrong API URL or firewall blocking
- ✅ Solution:
  1. Verify backend is running: Open http://localhost:8000/health
  2. Check `frontend/app.py` has `API_URL = "http://localhost:8000"`
  3. Disable firewall temporarily to test

---

### Problem: Analysis fails or times out

**Error: `Request timed out`**
- ❌ OpenAI API is slow or unresponsive
- ✅ Solution:
  - Wait and try again (OpenAI servers might be busy)
  - Check your internet connection
  - Verify your OpenAI API key has available credits

**Error: `Invalid API key`**
- ❌ Wrong or expired OpenAI API key
- ✅ Solution:
  1. Go to https://platform.openai.com/api-keys
  2. Verify your key is active
  3. Check if you have available credits: https://platform.openai.com/account/billing/overview
  4. Update your `env` file with the correct key

**Error: `No data found for the current period`**
- ❌ Selected date range has no matching data in CSV
- ✅ Solution:
  - Check the date range of your CSV data
  - Select a period that has data
  - Verify `week_start_date` column has correct dates

---

### Problem: CSV upload error

**Error: `KeyError: 'week_start_date'`**
- ❌ Required column is missing from CSV
- ✅ Solution: Ensure your CSV has all required columns (see CSV Data Format section)

**Error: Date parsing error**
- ❌ Date format is incorrect
- ✅ Solution: Dates must be in `YYYY-MM-DD` format (e.g., `2025-03-15`)

**Error: `Invalid literal for float`**
- ❌ Numeric columns contain text or special characters
- ✅ Solution:
  - Remove currency symbols (₺, $, etc.)
  - Remove commas from numbers (use `12345.67` not `12,345.67`)
  - Replace empty cells with `0`

---

### Quick Diagnostic Commands

**Check if Python is installed:**
```bash
python --version  # or python3 --version
```

**Check if virtual environment is activated:**
```bash
which python  # macOS/Linux (should show path with 'venv')
where python  # Windows (should show path with 'venv')
```

**Check if OpenAI package is installed:**
```bash
pip show openai
```

**Test backend health:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

---

### Still Having Issues?

1. **Delete and recreate virtual environment:**
```bash
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

2. **Check logs:**
- Backend errors appear in Terminal 1
- Frontend errors appear in Terminal 2
- Look for red error messages

3. **Use sample data:**
- Test with the included `campaign_metrics_sample.csv` first
- If it works, the issue is with your CSV format

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

