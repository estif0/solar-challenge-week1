# Solar Radiation Analysis Dashboard

An interactive Streamlit dashboard for analyzing solar radiation data from three West African locations: Benin, Sierra Leone, and Togo.

## 🌟 Features

-   **📊 Overview**: Key statistics and solar energy potential assessment
-   **📈 Time Patterns**: Monthly and hourly solar irradiance trends
-   **🔗 Correlations**: Variable relationship analysis
-   **🌍 Comparisons**: Cross-country statistical comparisons with ANOVA tests

## 🚀 Quick Start

### Prerequisites

-   Python 3.8+
-   pip

### Installation

```bash
# Clone the repository
git clone https://github.com/estif0/solar-challenge-week1.git
cd solar-challenge-week1

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Generate Dashboard Data

Since the raw data files are not included in the repository (gitignored), you need to generate the pre-computed statistics:

```bash
# Make sure you have cleaned data in src/data/cleaned/
python src/scripts/generate_dashboard_data.py
```

This creates `src/data/processed/dashboard_statistics.json` which contains all the pre-computed statistics used by the dashboard.

### Run Locally

```bash
streamlit run src/app/main.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
solar-challenge-week0/
├── src/
│   ├── app/                      # Streamlit dashboard
│   │   ├── main.py              # Main application
│   │   ├── config.py            # Configuration
│   │   ├── components/          # UI components
│   │   │   ├── sidebar.py
│   │   │   ├── overview.py
│   │   │   ├── time_series.py
│   │   │   ├── correlations.py
│   │   │   └── comparisons.py
│   │   └── utils/               # Utilities
│   │       ├── data_loader.py
│   │       └── chart_builder.py
│   ├── analysis/                # Analysis modules
│   │   ├── solar_metrics.py
│   │   └── statistical_tests.py
│   ├── utils/                   # Data utilities
│   │   ├── data_loader.py
│   │   ├── data_cleaner.py
│   │   └── visualization.py
│   ├── scripts/                 # Scripts
│   │   └── generate_dashboard_data.py
│   ├── data/                    # Data (gitignored)
│   │   ├── raw/
│   │   ├── cleaned/
│   │   └── processed/
│   │       └── dashboard_statistics.json  # Pre-computed stats
│   └── notebooks/               # Jupyter notebooks
├── requirements.txt
└── README.md
```

## 🌐 Deployment to Streamlit Cloud

### Step 1: Prepare for Deployment

1. Ensure `dashboard_statistics.json` is committed to the repository:

```bash
git add src/data/processed/dashboard_statistics.json
git commit -m "Add pre-computed dashboard statistics"
git push
```

2. Create a `.streamlit/config.toml` file (already done if following this guide)

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `estif0/solar-challenge-week1`
5. Branch: `dashboard-dev` (or `main` after merging)
6. Main file path: `src/app/main.py`
7. Click "Deploy"

Your dashboard will be live at: `https://[your-app-name].streamlit.app`

## 📊 Data

The dashboard analyzes solar radiation data from:

-   **Benin** (Malanville)
-   **Sierra Leone** (Bumbuna)
-   **Togo** (Dapaong)

### Metrics Analyzed:

-   **GHI**: Global Horizontal Irradiance
-   **DNI**: Direct Normal Irradiance
-   **DHI**: Diffuse Horizontal Irradiance
-   **Tamb**: Ambient Temperature
-   **RH**: Relative Humidity
-   **WS**: Wind Speed
-   **BP**: Barometric Pressure

## 🛠️ Development

### Adding New Countries

1. Add cleaned data to `src/data/cleaned/`
2. Run `python src/scripts/generate_dashboard_data.py`
3. The dashboard will automatically include the new data

### Modifying Components

All dashboard components are modular:

-   Edit individual components in `src/app/components/`
-   Modify charts in `src/app/utils/chart_builder.py`
-   Update configuration in `src/app/config.py`

## 📝 License

This project is part of the 10 Academy KAIM program.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚡ Performance Notes

-   Uses `@st.cache_data` to cache statistics loading
-   Pre-computed statistics ensure fast load times
-   No raw data processing on the frontend
-   Optimized for deployment without large data files

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit**
