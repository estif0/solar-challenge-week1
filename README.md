# Solar Data Discovery Challenge - Week 0

## 🌞 Project Overview

This project analyzes solar irradiance data from three African countries (Benin, Sierra Leone, and Togo) to provide insights for solar energy investments. We perform exploratory data analysis (EDA), data cleaning, and cross-country comparisons to support business decisions.

## 📁 Project Structure

```
solar-challenge-week0/
├── src/
│   ├── data/                    # Raw CSV data files
│   ├── notebooks/               # Jupyter notebooks for analysis
│   ├── scripts/                 # Python scripts
│   └── tests/                   # Unit tests
├── app/                         # Streamlit dashboard (optional)
├── .github/workflows/           # CI/CD pipeline
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.8 or higher
-   Git
-   WSL (if on Windows)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/estif0/solar-challenge-week1.git
    cd solar-challenge-week1
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

The project analyzes solar irradiance data from:

-   **Benin (Malanville)**: `src/data/benin-malanville.csv`
-   **Sierra Leone (Bumbuna)**: `src/data/sierraleone-bumbuna.csv`
-   **Togo (Dapaong)**: `src/data/togo-dapaong_qc.csv`

### Key Metrics Analyzed

-   **GHI**: Global Horizontal Irradiance
-   **DNI**: Direct Normal Irradiance
-   **DHI**: Diffuse Horizontal Irradiance
-   **Weather Variables**: Temperature, humidity, wind speed, precipitation

## 🔬 Analysis Tasks

### Task 1: Environment Setup ✅

-   [x] GitHub repository setup
-   [x] Python virtual environment
-   [x] Project structure
-   [x] CI/CD pipeline

### Task 2: Individual Country EDA

-   [x] Benin EDA (`eda-benin` branch)
-   [x] Sierra Leone EDA (`eda-sierra-leone` branch)
-   [ ] Togo EDA (`eda-togo` branch)

### Task 3: Cross-Country Comparison

-   [ ] Statistical comparisons (`compare-countries` branch)
-   [ ] Business insights and recommendations

### Task 4: Dashboard (Bonus)

-   [ ] Interactive Streamlit dashboard
-   [ ] Deployment to Streamlit Cloud

## 🛠️ Development Workflow

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

## 🧪 Testing

Run tests using pytest:

```bash
pytest src/tests/
```

## 📈 Results

Results and insights will be documented in individual notebook files and summarized in the final comparison notebook.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created as part of the 10 Academy AI/ML Engineering Program.

---

**Happy analyzing! 🌞📊**
