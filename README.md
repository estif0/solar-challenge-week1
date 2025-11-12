# Solar Data Discovery Challenge - Week 0

## 🌞 Project Overview

This project provides a comprehensive analysis of solar irradiance data from three West African countries (Benin, Sierra Leone, and Togo) to support data-driven solar energy investment decisions. The analysis includes exploratory data analysis (EDA), data quality assessment, statistical comparisons, and actionable business recommendations.

**Project Goal**: Evaluate and compare solar energy potential across three countries to identify optimal investment locations and technology recommendations for solar energy projects.

## 📁 Project Structure

```
solar-challenge-week0/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI/CD pipeline configuration
├── .streamlit/
│   └── config.toml             # Streamlit theme configuration
├── src/
│   ├── analysis/               # Analysis modules
│   │   ├── solar_metrics.py   # Solar potential calculations
│   │   └── statistical_tests.py # Statistical analysis tools
│   ├── app/                    # Streamlit dashboard application
│   │   ├── main.py            # Dashboard entry point
│   │   ├── config.py          # Dashboard configuration
│   │   ├── components/        # UI components (sidebar, tabs)
│   │   └── utils/             # Dashboard utilities
│   ├── data/
│   │   ├── raw/               # Original CSV files (gitignored)
│   │   ├── cleaned/           # Cleaned datasets (gitignored)
│   │   └── processed/         # Dashboard statistics JSON
│   ├── notebooks/             # Jupyter notebooks for analysis
│   │   ├── benin_eda.ipynb
│   │   ├── sierraleone_eda.ipynb
│   │   ├── togo_eda.ipynb
│   │   └── compare_countries.ipynb
│   ├── scripts/               # Automation scripts
│   │   ├── generate_dashboard_data.py
│   │   └── data_validator.py
│   ├── tests/                 # Unit tests
│   └── utils/                 # Utility modules
│       ├── data_cleaner.py    # Data cleaning functions
│       ├── data_loader.py     # Data loading utilities
│       └── visualization.py   # Visualization helpers
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
├── README.md                  # Project documentation (this file)
└── requirements.txt           # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.11 or higher
-   Git

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/estif0/solar-challenge-week0.git
    cd solar-challenge-week0
    ```

2. **Create and activate virtual environment:**

    ```bash
    python -m venv venv

    # On Linux/WSL:
    source venv/bin/activate

    # On Windows:
    venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Verify installation:**

    ```bash
    # Check Python version
    python --version  # Should be 3.10+

    # List installed packages
    pip list
    ```

5. **Launch Jupyter Notebook (for EDA):**

    ```bash
    jupyter notebook
    ```

    Navigate to `src/notebooks/` to access analysis notebooks.

6. **Run the Dashboard (optional):**

    ```bash
    # Generate dashboard statistics
    python src/scripts/generate_dashboard_data.py

    # Launch Streamlit dashboard
    streamlit run src/app/main.py
    ```

    Access at http://localhost:8501

## 📊 Data Sources

The project analyzes high-resolution solar irradiance and meteorological data from three measurement stations:

-   **Benin (Malanville)**: `src/data/raw/benin-malanville.csv` (525,600 records, Aug 2021 - Aug 2022)
-   **Sierra Leone (Bumbuna)**: `src/data/raw/sierraleone-bumbuna.csv` (524,374 records, Oct 2021 - Oct 2022)
-   **Togo (Dapaong)**: `src/data/raw/togo-dapaong_qc.csv` (524,731 records, Oct 2021 - Oct 2022)

### Key Metrics Analyzed

-   **GHI** (Global Horizontal Irradiance): Total solar radiation on a horizontal surface (W/m²)
-   **DNI** (Direct Normal Irradiance): Direct beam radiation (W/m²) - critical for CSP systems
-   **DHI** (Diffuse Horizontal Irradiance): Scattered solar radiation (W/m²)
-   **Weather Variables**: Ambient temperature, relative humidity, wind speed, barometric pressure, precipitation

## 🔬 Implementation & Contributions

### Task 1: Environment Setup ✅

**Completed Features:**

-   [x] GitHub repository initialization with proper structure
-   [x] Python virtual environment configuration (Python 3.11)
-   [x] Clean project architecture following best practices
-   [x] CI/CD pipeline with automated code quality checks (Black, flake8)
-   [x] Comprehensive `.gitignore` to exclude data files and artifacts
-   [x] Dependency management with `requirements.txt`

**Technical Implementation:**

-   Repository structure organized into `src/` (data, notebooks, scripts, tests) and `app/` directories
-   GitHub Actions workflow configured for automated testing on push/PR
-   Feature branch workflow with pull request reviews

### Task 2: Individual Country EDA ✅

**Completed Analysis for Each Country:**

**Benin (Malanville) - `benin_eda.ipynb`:**

-   Comprehensive data profiling: 525,600 records analyzed
-   Missing values assessment: Identified 100% missing Comments column
-   Outlier detection using Z-score method (threshold: 3 for detection, 4 for removal)
-   Solar irradiance analysis: GHI, DNI, DHI distributions and patterns
-   Weather variable analysis: Temperature, humidity, wind speed patterns
-   Time series analysis: Daily and seasonal patterns visualization
-   Correlation analysis: Identified strong positive correlations between GHI, DNI, DHI
-   Data cleaning: Removed 978 extreme outliers (0.19%), clipped negative solar values
-   Cleaned dataset exported: 524,622 records

**Sierra Leone (Bumbuna) - `sierraleone_eda.ipynb`:**

-   Similar comprehensive analysis pipeline
-   Data quality assessment and cleaning
-   Export of cleaned dataset: 524,374 records

**Togo (Dapaong) - `togo_eda.ipynb`:**

-   Complete EDA following consistent methodology
-   Cleaned dataset exported: 524,731 records

**Methodology Applied:**

-   Statistical summary (mean, median, std, min, max, quartiles)
-   Z-score based outlier detection and removal
-   Forward/backward fill for missing value imputation
-   Negative value handling (clipped to 0 for solar irradiance)
-   Visualization: Histograms, boxplots, time series, correlation heatmaps

### Task 3: Cross-Country Comparison ✅

**Statistical Analysis - `compare_countries.ipynb`:**

**Comparative Statistics:**

-   Mean, median, and standard deviation comparison for GHI, DNI, DHI
-   Weather pattern analysis (temperature, humidity, wind speed)
-   Data completeness metrics across all three countries

**Visualization:**

-   Comparison boxplots for solar irradiance metrics (GHI, DNI, DHI)
-   Temperature comparison across countries
-   Statistical summary tables with key metrics

**Statistical Testing:**

-   One-way ANOVA tests for GHI, DNI, DHI, and temperature
-   All tests showed statistically significant differences (p < 0.05)
-   Effect size calculation (η²) to assess practical significance
-   Results: Large F-statistics indicating meaningful differences between countries

**Key Findings:**

1. **Benin** ranks highest with GHI: 242.4 W/m², DNI: 167.7 W/m²
2. **Togo** ranks second with GHI: 232.0 W/m², DNI: 151.4 W/m²
3. **Sierra Leone** ranks third with GHI: 204.5 W/m², DNI: 116.6 W/m²

**Business Recommendations:**

-   **Primary Investment**: Benin (highest solar potential, suitable for both PV and CSP)
-   **Secondary Investment**: Togo (good backup location, risk diversification)
-   **Technology-Specific**: Detailed recommendations for PV vs CSP systems per country

### Task 4: Interactive Dashboard (Bonus) ✅

**Completed Features:**

-   [x] Production-ready Streamlit dashboard with modular architecture
-   [x] Pre-computed statistics strategy for efficient deployment
-   [x] Four comprehensive analysis sections (tabs)
-   [x] Interactive Plotly visualizations
-   [x] Cross-country statistical comparisons with ANOVA tests
-   [x] Deployment-ready configuration

**Dashboard Features:**

**1. Overview Tab:**

-   Data summary statistics (records, date ranges, variables)
-   Solar irradiance metrics (GHI, DNI, DHI) with mean, std dev, min/max
-   Solar potential assessment (annual energy kWh/m², daily average, peak irradiance)
-   Solar resource quality rating (Excellent/Good/Fair/Poor)

**2. Time Patterns Tab:**

-   Monthly solar irradiance patterns (seasonal analysis)
-   Hourly solar irradiance patterns (daily profiles)
-   Separate visualizations for GHI, DNI, DHI
-   Pattern insights and interpretations

**3. Correlations Tab:**

-   Interactive correlation heatmap for all variables
-   Strength interpretation guide (strong/moderate/weak correlations)
-   Top 5 strongest correlations automatically identified
-   Relationship analysis between solar and weather variables

**4. Cross-Country Comparison Tab:**

-   Side-by-side mean comparison bar charts (GHI, DNI, DHI)
-   Distribution comparison box plots
-   Statistical significance testing (ANOVA with F-statistic, p-value)
-   Summary comparison table (7 key metrics across 3 countries)
-   Rankings: Best countries for GHI, DNI, and annual energy potential

**Technical Implementation:**

-   **Architecture**: Modular components (sidebar, overview, time_series, correlations, comparisons)
-   **Data Strategy**: Pre-computed 31KB JSON statistics file (no raw CSVs needed for deployment)
-   **Performance**: `@st.cache_data` for instant loading, responsive design
-   **Reusability**: Leverages existing `SolarMetrics`, `StatisticalAnalyzer`, and `DataLoader` modules
-   **Visualization**: All charts built with Plotly for full interactivity (hover, zoom, pan)
-   **Configuration**: Custom theme with `.streamlit/config.toml`, centralized settings in `config.py`

**File Structure:**

```
src/app/
├── main.py                      # Main application entry point
├── config.py                    # Central configuration
├── components/                  # Modular UI components
│   ├── sidebar.py              # Country selection
│   ├── overview.py             # Overview statistics
│   ├── time_series.py          # Temporal patterns
│   ├── correlations.py         # Correlation analysis
│   └── comparisons.py          # Cross-country comparison
└── utils/                       # Utility modules
    ├── data_loader.py          # JSON statistics loader with caching
    └── chart_builder.py        # Plotly chart creation functions
```

**Running the Dashboard:**

1. **Generate statistics** (first time or after data updates):

    ```bash
    python src/scripts/generate_dashboard_data.py
    ```

2. **Launch dashboard locally**:

    ```bash
    streamlit run src/app/main.py
    ```

    Access at: http://localhost:8501

**Dashboard Documentation:**

-   Usage guide: `src/app/README.md`
-   Deployment guide: `reports/DEPLOYMENT.md`
-   Completion report: `reports/TASK4_DASHBOARD_COMPLETION.md`

## 🛠️ Development Workflow

This project follows a feature branch workflow with pull request reviews:

1. **Create feature branch:**

    ```bash
    git checkout -b feature-name
    ```

2. **Make changes and commit:**

    ```bash
    git add .
    git commit -m "descriptive message"
    ```

3. **Push and create Pull Request:**
    ```bash
    git push origin feature-name
    ```

**Completed Branches:**

-   `setup-task` - Initial project setup and CI/CD configuration (✅ merged to main)
-   `eda-benin` - Benin solar data analysis (✅ merged to main)
-   `eda-sierra-leone` - Sierra Leone solar data analysis (✅ merged to main)
-   `eda-togo` - Togo solar data analysis (✅ merged to main)
-   `compare-countries` - Cross-country statistical comparison (✅ merged to main)
-   `dashboard-dev` - Interactive Streamlit dashboard (🚀 deployment ready)

All feature branches follow best practices with meaningful commits and pull request reviews before merging.

## 🧪 Code Quality & Testing

### Automated CI/CD

The project includes a GitHub Actions CI workflow that automatically:

-   Validates Python environment setup
-   Checks code formatting with Black
-   Runs linting with flake8
-   Verifies dependency compatibility

### Manual Testing

Run tests using pytest (when tests are added):

```bash
pytest src/tests/
```

### Code Formatting

Format code with Black:

```bash
black src/
```

### Linting

Check code quality with flake8:

```bash
flake8 src/
```

## � Quick Start Examples

### Example 1: Load and Analyze Data

```python
from src.utils.data_loader import DataLoader
from src.analysis.solar_metrics import SolarMetrics

# Load cleaned data
loader = DataLoader()
benin_data = loader.load_cleaned_data('benin')

# Calculate solar metrics
metrics = SolarMetrics(benin_data)
summary = metrics.calculate_all_metrics()

print(f"Average GHI: {summary['mean_ghi']:.2f} W/m²")
print(f"Annual Energy Potential: {summary['annual_ghi_kwh_m2']:.2f} kWh/m²")
```

### Example 2: Create Visualizations

```python
from src.utils.visualization import SolarVisualizer

# Initialize visualizer
viz = SolarVisualizer(benin_data)

# Create time series plot
fig = viz.plot_time_series('GHI', title='Solar Irradiance Over Time')
fig.show()

# Create correlation heatmap
fig = viz.plot_correlation_heatmap()
fig.show()
```

### Example 3: Statistical Comparison

```python
from src.analysis.statistical_tests import StatisticalAnalyzer
from src.utils.data_loader import DataLoader

# Load all countries
loader = DataLoader()
benin = loader.load_cleaned_data('benin')
sierra_leone = loader.load_cleaned_data('sierraleone')
togo = loader.load_cleaned_data('togo')

# Run ANOVA test
analyzer = StatisticalAnalyzer()
result = analyzer.anova_oneway(
    benin['GHI'],
    sierra_leone['GHI'],
    togo['GHI'],
    group_names=['Benin', 'Sierra Leone', 'Togo']
)

print(f"F-statistic: {result['f_statistic']:.4f}")
print(f"P-value: {result['p_value']:.6f}")
print(f"Significant: {result['significant']}")
```

## �📈 Key Results & Insights

### Solar Energy Potential Rankings

1. **Benin (Malanville)** - **Highest Priority**

    - Average GHI: 242.4 W/m² (18% higher than Sierra Leone)
    - Average DNI: 167.7 W/m² (44% higher than Sierra Leone)
    - Best suited for: Large-scale PV and CSP projects
    - Temperature: 28.2°C average (11.0°C - 43.8°C range)

2. **Togo (Dapaong)** - **Medium-High Priority**

    - Average GHI: 232.0 W/m² (13% higher than Sierra Leone)
    - Average DNI: 151.4 W/m² (30% higher than Sierra Leone)
    - Best suited for: PV systems, backup investment location
    - Temperature: 27.8°C average (14.9°C - 41.4°C range)

3. **Sierra Leone (Bumbuna)** - **Lower Priority**
    - Average GHI: 204.5 W/m²
    - Average DNI: 116.6 W/m² (insufficient for optimal CSP)
    - Best suited for: Small-scale PV, distributed solar applications
    - Temperature: 26.3°C average (12.3°C - 39.9°C range)

### Statistical Significance

All ANOVA tests confirmed statistically significant differences (p < 0.05) between countries for:

-   Global Horizontal Irradiance (GHI)
-   Direct Normal Irradiance (DNI)
-   Diffuse Horizontal Irradiance (DHI)
-   Ambient Temperature

### Data Quality

-   **Benin**: 99.81% data retention after cleaning (978 outliers removed)
-   **Sierra Leone**: Similar high data quality
-   **Togo**: Similar high data quality
-   All datasets: Minimal missing values, comprehensive time coverage

Detailed results and visualizations are available in the individual EDA notebooks and the comparison notebook.

## 📚 Additional Resources

### Documentation Files

-   **`src/app/README.md`**: Dashboard usage and features guide
-   **`src/utils/USAGE_*.md`**: Module-specific usage documentation
-   **`src/analysis/USAGE_*.md`**: Analysis module documentation

### Notebooks

All analysis notebooks are located in `src/notebooks/`:

1. **`benin_eda.ipynb`**: Comprehensive EDA for Benin (Malanville)

    - Data profiling and quality assessment
    - Outlier detection and removal
    - Time series and correlation analysis
    - Solar potential evaluation

2. **`sierraleone_eda.ipynb`**: Complete analysis for Sierra Leone (Bumbuna)

    - Similar methodology as Benin analysis
    - Country-specific insights and patterns

3. **`togo_eda.ipynb`**: Full EDA for Togo (Dapaong)

    - Consistent analytical approach
    - Comparative observations

4. **`compare_countries.ipynb`**: Cross-country statistical comparison
    - ANOVA tests for all metrics
    - Visualization of differences
    - Business recommendations

### Utility Modules

-   **`src/utils/data_loader.py`**: Data loading utilities with caching
-   **`src/utils/data_cleaner.py`**: Cleaning and preprocessing functions
-   **`src/utils/visualization.py`**: Reusable visualization components
-   **`src/analysis/solar_metrics.py`**: Solar potential calculations
-   **`src/analysis/statistical_tests.py`**: Statistical analysis tools

## 🎯 Project Achievements

This project successfully demonstrates:

✅ **Professional Git Workflow**

-   Feature branch development with PR reviews
-   Meaningful commit messages following conventions
-   Proper `.gitignore` configuration
-   CI/CD integration with GitHub Actions

✅ **Comprehensive Data Analysis**

-   Complete data profiling and quality assessment
-   Robust outlier detection and handling (Z-score method)
-   Statistical rigor (ANOVA, correlation analysis)
-   Clear, actionable business insights

✅ **Production-Ready Code**

-   Modular, reusable components
-   Comprehensive documentation
-   Code quality standards (Black, Flake8)
-   Performance optimization (caching, pre-computation)

✅ **Effective Communication**

-   Clear visualizations with interpretations
-   Executive summaries with rankings
-   Detailed technical documentation
-   Interactive dashboard for stakeholder engagement

✅ **Deployment Readiness**

-   Streamlit dashboard fully functional
-   Deployment guide and configuration
-   Environment management and dependencies
-   Scalable architecture for future enhancements

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** on GitHub

2. **Create a feature branch**:

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Make your changes** following the project structure and coding standards

4. **Add tests** if applicable (in `src/tests/`)

5. **Run code quality checks**:

    ```bash
    black src/
    flake8 src/
    ```

6. **Commit with meaningful messages**:

    ```bash
    git commit -m "feat: add new solar metric calculation"
    ```

    Use conventional commits:

    - `feat:` - New features
    - `fix:` - Bug fixes
    - `docs:` - Documentation changes
    - `refactor:` - Code refactoring
    - `test:` - Adding tests
    - `chore:` - Maintenance tasks

7. **Push to your fork**:

    ```bash
    git push origin feature/your-feature-name
    ```

8. **Submit a pull request** with:
    - Clear description of changes
    - Reference to related issues
    - Screenshots (if UI changes)
    - Test results

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🛠️ Technical Stack

**Core Technologies:**

-   **Python 3.10+**: Core programming language
-   **Pandas 2.0+**: Data manipulation and analysis
-   **NumPy**: Numerical computing and array operations

**Data Analysis & Statistics:**

-   **SciPy**: Statistical analysis (ANOVA, Z-score calculations, hypothesis testing)
-   **Statsmodels**: Advanced statistical modeling

**Visualization:**

-   **Matplotlib & Seaborn**: Static publication-quality visualizations
-   **Plotly 5.14+**: Interactive web-based visualizations
-   **Streamlit 1.28+**: Dashboard framework for data applications

**Development Tools:**

-   **Jupyter Notebooks**: Interactive analysis environment
-   **Git & GitHub**: Version control and collaboration
-   **GitHub Actions**: CI/CD pipeline for automated testing
-   **Black & Flake8**: Code formatting and linting

**Deployment:**

-   **Streamlit Cloud**: Dashboard hosting and deployment
-   **JSON**: Lightweight data serialization for deployment

## 📝 Methodology

### Data Cleaning Process

1. **Outlier Detection**: Z-score method (threshold: 3 for detection, 4 for removal)
2. **Negative Values**: Clipped solar irradiance values to 0 (nighttime measurements)
3. **Missing Values**: Forward fill followed by backward fill for time series continuity
4. **Data Validation**: Comprehensive quality checks before export

### Statistical Analysis

-   **Descriptive Statistics**: Mean, median, standard deviation, quartiles
-   **Inferential Statistics**: One-way ANOVA for group comparisons
-   **Effect Size**: Eta-squared (η²) calculation for practical significance
-   **Correlation Analysis**: Pearson correlation coefficients for variable relationships

### Visualization Approach

-   **Distribution Analysis**: Histograms and boxplots for understanding data spread
-   **Time Series**: Line plots for temporal pattern identification
-   **Comparative Analysis**: Side-by-side boxplots for cross-country comparison
-   **Correlation Heatmaps**: Visual representation of variable relationships

## � Troubleshooting

### Common Issues and Solutions

**Issue: "Module not found" error**

```bash
# Solution: Ensure virtual environment is activated and dependencies installed
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue: "Data files not found" when running notebooks**

```bash
# Solution: Ensure you're in the project root directory
cd /path/to/solar-challenge-week0
jupyter notebook
```

**Issue: Dashboard shows "No data available"**

```bash
# Solution: Generate dashboard statistics
python src/scripts/generate_dashboard_data.py
```

**Issue: Plots not displaying in Jupyter**

```python
# Solution: Add magic command at the start of notebook
%matplotlib inline
```

**Issue: GitHub Actions CI failing**

```bash
# Solution: Check code formatting and linting locally first
black src/ --check
flake8 src/
```

## 📞 Support & Contact

For questions, issues, or collaboration opportunities:

-   **GitHub Issues**: [Create an issue](https://github.com/estif0/solar-challenge-week0/issues)
-   **Email**: estifanoswork@gmail.com

## 👨‍💻 Author & Acknowledgments

**Project Author**: Estifanose Sahilu  
**GitHub**: [@estif0](https://github.com/estif0)  
**Program**: 10 Academy - Artificial Intelligence Mastery (AIM) Program  
**Challenge**: KAIM Week 0 - Solar Data Discovery Challenge  
**Date**: November 2025

### Skills Demonstrated

This project showcases proficiency in:

✅ **Data Engineering & Analysis**

-   Large-scale dataset processing (500K+ records per country)
-   Data quality assessment and cleaning
-   Statistical analysis and hypothesis testing
-   Time series analysis and pattern recognition

✅ **Software Engineering**

-   Modular, reusable code architecture
-   Git version control and collaboration
-   CI/CD pipeline implementation
-   Code quality standards and best practices

✅ **Data Visualization & Communication**

-   Static and interactive visualizations
-   Dashboard development with Streamlit
-   Clear technical documentation
-   Business-oriented insights and recommendations

✅ **Machine Learning Engineering**

-   Feature engineering for solar metrics
-   Statistical modeling and validation
-   Production deployment strategies
-   Performance optimization

### Acknowledgments

-   **10 Academy**: For providing comprehensive AI/ML training and mentorship
-   **Open Source Community**: For excellent tools (Pandas, Plotly, Streamlit, etc.)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

Permission is hereby granted, free of charge, to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to including the copyright notice and permission notice in all copies.

**Copyright © 2025 Estifanose Sahilu**

---

**🌞 Happy Solar Analysis! May your insights power a sustainable future! 📊⚡**

---
