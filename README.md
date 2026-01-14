# India Air Quality – Impact Metrics Dashboard 🇮🇳

An interactive Streamlit dashboard for multi-year analysis of Indian air quality, built as part of the Impact Metrics project.

The dashboard enables exploration of:
- City-wise air quality trends and bad-air patterns
- Pollution heatmaps and seasonal pollutant behaviour
- Station reliability and data completeness analysis
- Risk index computation and policy-level insights

The goal is to convert large-scale air quality datasets into actionable visual insights through an intuitive web dashboard.

--------------------------------------------------

LIVE DASHBOARD

Streamlit App (Deployed):
https://impact-metrics-2025-kers9y99zth6fbqh83ract.streamlit.app/

--------------------------------------------------

DATA SOURCE

All datasets are hosted externally on Hugging Face and are loaded directly via URLs at runtime.
No CSV files are required locally to run this project.

Hugging Face Dataset Repository:
https://huggingface.co/datasets/khush-thakkar-09/station_hour

--------------------------------------------------

PROJECT STRUCTURE

impact-metrics-dashboard/
│
├── dashboard.py        # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

--------------------------------------------------

RUNNING THE DASHBOARD LOCALLY

NOTE:
You do NOT need to download any datasets.
All data is fetched automatically from Hugging Face.

--------------------------------------------------

STEP 1: CREATE AND ACTIVATE A VIRTUAL ENVIRONMENT

macOS / Linux:

python3 -m venv venv
source venv/bin/activate

Windows (Command Prompt / PowerShell):

python -m venv venv
venv\Scripts\activate

If PowerShell blocks activation, run once (as Administrator):

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

--------------------------------------------------

STEP 2: INSTALL DEPENDENCIES

pip install -r requirements.txt

--------------------------------------------------

STEP 3: RUN THE DASHBOARD

streamlit run dashboard.py

The application will open automatically in your browser at:

http://localhost:8501

--------------------------------------------------

TECH STACK

- Python
- Streamlit
- Pandas & NumPy
- Plotly & Matplotlib
- Scikit-learn
- Hugging Face Datasets (remote hosting)

--------------------------------------------------

NOTES

- The dashboard is optimized for interactive exploration rather than static reports.
- Large datasets are handled via caching and vectorized operations for performance.
- The deployed version may take a few seconds to load heavier visualizations initially.

--------------------------------------------------
