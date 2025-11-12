"""
Dashboard Configuration

This file contains all configuration settings for the Streamlit dashboard.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data' / 'processed'
STATS_FILE = DATA_DIR / 'dashboard_statistics.json'

# Dashboard Settings
PAGE_TITLE = "Solar Radiation Analysis Dashboard"
PAGE_ICON = "☀️"
LAYOUT = "wide"

# Country Information
COUNTRIES = {
    'benin': {
        'name': 'Benin',
        'location': 'Malanville',
        'color': '#FF6B6B',  # Red
        'flag': '🇧🇯'
    },
    'sierraleone': {
        'name': 'Sierra Leone',
        'location': 'Bumbuna',
        'color': '#4ECDC4',  # Teal
        'flag': '🇸🇱'
    },
    'togo': {
        'name': 'Togo',
        'location': 'Dapaong',
        'color': '#45B7D1',  # Blue
        'flag': '🇹🇬'
    }
}

# Metrics Configuration
SOLAR_METRICS = {
    'GHI': {
        'name': 'Global Horizontal Irradiance',
        'unit': 'W/m²',
        'description': 'Total solar radiation received on a horizontal surface',
        'color': '#FFD93D'
    },
    'DNI': {
        'name': 'Direct Normal Irradiance',
        'unit': 'W/m²',
        'description': 'Solar radiation received directly from the sun',
        'color': '#FF6B6B'
    },
    'DHI': {
        'name': 'Diffuse Horizontal Irradiance',
        'unit': 'W/m²',
        'description': 'Solar radiation scattered by the atmosphere',
        'color': '#6BCF7F'
    }
}

METEOROLOGICAL_METRICS = {
    'Tamb': {
        'name': 'Ambient Temperature',
        'unit': '°C',
        'description': 'Air temperature'
    },
    'RH': {
        'name': 'Relative Humidity',
        'unit': '%',
        'description': 'Moisture content in the air'
    },
    'WS': {
        'name': 'Wind Speed',
        'unit': 'm/s',
        'description': 'Wind velocity'
    },
    'BP': {
        'name': 'Barometric Pressure',
        'unit': 'hPa',
        'description': 'Atmospheric pressure'
    }
}

# Chart Configuration
CHART_HEIGHT = 400
CHART_TEMPLATE = 'plotly_white'

# Months for labels
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
