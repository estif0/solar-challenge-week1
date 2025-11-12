# Solar Data Discovery Challenge - Week 0

## 🌞 Project Overview

This project provides a comprehensive analysis of solar irradiance data from three West African countries (Benin, Sierra Leone, and Togo) to support data-driven solar energy investment decisions. The analysis includes exploratory data analysis (EDA), data quality assessment, statistical comparisons, and actionable business recommendations.

**Project Goal**: Evaluate and compare solar energy potential across three countries to identify optimal investment locations and technology recommendations for solar energy projects.

## 📁 Project Structure

```
solar-challenge-week0/
├── src/
│   ├── data/                    # Raw CSV data files
│   ├── notebooks/               # Jupyter notebooks for analysis
│   ├── scripts/                 # Python scripts
│   └── tests/                   # Unit tests
├── .github/workflows/           # CI/CD pipeline
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
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

4. **Launch Jupyter Notebook:**
    ```bash
    jupyter notebook
    ```

## 📊 Data Sources

The project analyzes high-resolution solar irradiance and meteorological data from three measurement stations:

-   **Benin (Malanville)**: `src/data/benin-malanville.csv` (525,600 records, Aug 2021 - Aug 2022)
-   **Sierra Leone (Bumbuna)**: `src/data/sierraleone-bumbuna.csv` (524,374 records, Oct 2021 - Oct 2022)
-   **Togo (Dapaong)**: `src/data/togo-dapaong_qc.csv` (524,731 records, Oct 2021 - Oct 2022)

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

### Task 4: Dashboard (Bonus)

-   [ ] Interactive Streamlit dashboard
-   [ ] Deployment to Streamlit Cloud

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

-   `setup-task` - Initial project setup and CI/CD configuration
-   `eda-benin` - Benin solar data analysis
-   `eda-sierra-leone` - Sierra Leone solar data analysis
-   `eda-togo` - Togo solar data analysis
-   `compare-countries` - Cross-country statistical comparison

All branches have been merged to `main` via pull requests.

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

## 📈 Key Results & Insights

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🛠️ Technical Stack

-   **Python 3.11**: Core programming language
-   **Pandas & NumPy**: Data manipulation and numerical computing
-   **Matplotlib & Seaborn**: Static visualizations
-   **Plotly**: Interactive visualizations
-   **SciPy**: Statistical analysis (ANOVA, Z-score calculations)
-   **Jupyter Notebooks**: Interactive analysis environment
-   **Git & GitHub**: Version control and collaboration
-   **GitHub Actions**: Continuous Integration/Continuous Deployment

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

## 👨‍💻 Author & Acknowledgments

**Project Author**: Estifanose Sahilu
**Program**: 10 Academy AI/ML Engineering Program - KAIM Week 0 Challenge

This project was completed as part of the 10 Academy training program, demonstrating proficiency in:

-   Data science workflows and best practices
-   Statistical analysis and hypothesis testing
-   Data visualization and communication
-   Git/GitHub collaboration and CI/CD
-   Business-oriented data analysis

---

**Happy analyzing! 🌞📊**
