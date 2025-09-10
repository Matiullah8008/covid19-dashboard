# COVID-19 Interactive Dashboard

This project provides an interactive dashboard to explore global COVID-19 trends, vaccination impact, and policy responses. The dashboard is built using Python, Dash, and Plotly.

## Features

*   **Key Performance Indicators (KPIs):**  Displaying total cases, total deaths, and total vaccinations.
*   **Global COVID-19 Tracking:** Visualize the spread of COVID-19 across different countries and continents.
*   **Vaccination Impact Analysis:** Analyze the correlation between vaccination rates and COVID-19 cases/deaths.
*   **Interactive Visualizations:** The dashboard includes various interactive charts and maps:
    *   Time-series charts to track trends over time.
    *   An animated world map to visualize data geographically over time.
    *   Bar charts to compare data across countries.
    *   Scatter plots to explore relationships between different metrics.
*   **Customizable Filters:** Users can filter data by continent, country, metric, and date range to focus on specific areas of interest.
*   **Data Aggregation:** Data can be aggregated on a daily, weekly, or monthly basis.
*   **Theming:** The dashboard uses a dark theme (`CYBORG`) for a better user experience.

## Dataset

The project uses the "Our World in Data" (OWID) COVID-19 dataset. The raw data is cleaned and preprocessed to handle missing values and prepare it for visualization. The cleaned dataset is saved as `owid_covid_cleaned.csv`.

## Getting Started

### Prerequisites

*   Python 3.x
*   pip (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To start the Dash application, run the following command in your terminal:

```bash
python main.py
```

The application will be available at `http://127.0.0.1:8050/` in your web browser.

## Project Structure

*   `main.py`: The main application file that contains the Dash layout and callbacks.
*   `covid_dashboard_data_cleaning.ipynb`: A Jupyter Notebook that details the data cleaning and exploration process.
*   `owid_covid_cleaned.csv`: The cleaned COVID-19 dataset.
*   `requirements.txt`: A list of the Python packages required to run the project.
*   `readme.md`: This file.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or find any bugs.