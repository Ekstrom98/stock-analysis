# Stock Analysis

## 🚧 Work in Progress 🚧
This project is currently under active development. Features may change, and there may be bugs. Please report any issues you encounter.

## Description
A stock analysis tool designed to fetch and analyze stock data from various sources and provide a "magic score" based on the investment strategy termed "Magic Formula".

**Note**: At the moment, only stocks from OMXS30, NASDAQ100, and S&P500 are available.

[🔗 View the live Streamlit app here!](https://magic-stock-analysis.streamlit.app)

## Installation & Setup

### Prerequisites
- Docker
- Python 3.x

### Setup

1. **Clone the Repository**:
   \```
   git clone https://github.com/Ekstrom98/stock-analysis.git
   cd stock-analysis-main
   \```

2. **Set Up Python Environment**:
   \```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   \```

3. **Docker Setup**:
   \```
   docker-compose up -d
   \```

## Usage

- **Fetch S&P 500 Data**:
   \```
   python fetch_sp500.py
   \```

- **Fetch Company Data**:
   \```
   python fetch_companies.py
   \```

- **Manually Insert Company Data**:
   \```
   python companies_manual_insert.py
   \```

- **Generate Report**:
   \```
   python generate_report.py
   \```

- **Run Streamlit App**:
   \```
   streamlit run streamlit_app.py
   \```

- **Fetch Stock Data**:
   \```
   python fetch_stock_data.py
   \```

- **Backup Data**:
   \```
   python backup_data.py
   \```
