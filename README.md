# Urban-Rural Consumption Analysis Capstone

## 1. Project Overview

This project analyses household consumption patterns using data from the **Kenya Continuous Household Survey Programme (KCHS) 2021**. The analysis focuses on differences between urban and rural households and investigates relationships between household characteristics and consumption.

The project follows the **CRISP-DM (Cross-Industry Standard Process for Data Mining)** methodology, covering business understanding, data understanding, data preparation, modeling, evaluation, and deployment.

The final outcome is an interactive **Streamlit dashboard** that allows users to explore household consumption patterns and relationships within the dataset.

---

## 2. Problem Statement

Household consumption provides an important indicator of socioeconomic conditions and living standards. However, consumption patterns can differ substantially according to household location, household size, and other socioeconomic characteristics.

This project therefore investigates whether there are statistically significant differences in household consumption between urban and rural households and examines relationships between household characteristics and consumption.

The analysis also demonstrates how statistical analysis and interactive data visualization can be combined into a practical decision-support dashboard.

---

## 3. Project Objectives

The project has three objectives:

1. **To examine differences in household non-food consumption between urban and rural households.**

2. **To investigate relationships between household characteristics and household consumption.**

3. **To develop an interactive dashboard for exploring household consumption patterns and analytical results.**

---

## 4. Research Questions

The project addresses the following questions:

1. Is there a statistically significant difference in non-food consumption between urban and rural households?

2. What relationships exist between household characteristics and household consumption?

3. How can the results be presented through an interactive data-analysis dashboard?

---

## 5. Hypotheses

### Hypothesis 1

**H₀:** There is no statistically significant difference in non-food consumption between urban and rural households.

**H₁:** There is a statistically significant difference in non-food consumption between urban and rural households.

### Hypothesis 2

**H₀:** There is no significant relationship between household characteristics and household consumption.

**H₁:** There is a significant relationship between household characteristics and household consumption.

---

## 6. Dataset

The analysis uses household-level information derived from the **KCHS 2021** dataset.

The data include variables relating to:

- Household identification
- Household size
- Urban/rural residence
- County
- Household weights
- Adult-equivalent scale
- Food consumption
- Non-food consumption
- Total consumption
- Consumption per person

The original item-level data were transformed into an analytical household-level dataset suitable for statistical analysis.

> **Data note:** Raw survey microdata should not be redistributed through this repository unless public redistribution is explicitly permitted. The repository therefore focuses on the analytical workflow and the permitted processed data required by the dashboard.

---

## 7. Methodology: CRISP-DM

The project follows the six stages of CRISP-DM.

### 7.1 Business Understanding

The main analytical problem is to understand differences and relationships in household consumption across urban and rural settings.

### 7.2 Data Understanding

The KCHS 2021 data were examined to understand:

- Dataset structure
- Variables and data types
- Missing values
- Household identifiers
- Consumption variables
- Urban/rural classification

The non-food consumption dataset contained **349,464 records representing 16,962 unique households**.

### 7.3 Data Preparation

Data preparation included:

- Loading the survey data
- Inspecting variables and data types
- Checking missing values
- Identifying household records
- Aggregating item-level non-food consumption to household level
- Joining relevant household characteristics
- Creating analytical consumption variables
- Preparing the final dataset for statistical analysis and visualization

### 7.4 Modeling and Statistical Analysis

The project uses several straightforward analytical techniques:

- Descriptive statistics
- Independent-samples t-test
- Correlation analysis
- A/B group comparison

These techniques were selected to provide interpretable evidence while keeping the project appropriate for an academic data-science capstone.

### 7.5 Evaluation

The statistical results were evaluated using:

- Statistical significance
- Effect size
- Correlation coefficients
- Visual patterns

### 7.6 Deployment

The final analytical results were incorporated into an interactive **Streamlit dashboard**.

The dashboard provides users with an accessible interface for exploring household consumption patterns without directly interacting with the underlying Python code.

---

## 8. Key Statistical Results

### Urban-Rural Comparison

An independent-samples t-test was conducted to compare non-food consumption between urban and rural households.

| Statistic | Result |
|---|---:|
| Urban households | 5,609 |
| Rural households | 11,353 |
| t-statistic | 15.565 |
| p-value | < .001 |
| Cohen's d | 0.313 |

The test indicates a **statistically significant difference** in non-food consumption between urban and rural households.

However, the Cohen's *d* of approximately **0.313** indicates a relatively small effect size. Therefore, the difference is statistically significant but its practical magnitude is modest.

### Correlation Analysis

The correlation analysis produced the following relationships:

| Variables | Correlation |
|---|---:|
| Household size – Total consumption | 0.190 |
| Adult-equivalent expenditure – Total consumption | 0.722 |
| Household size – Adult-equivalent expenditure | -0.178 |

The relationship between adult-equivalent expenditure and total consumption is relatively strong, while household size has a weaker positive association with total consumption.

Correlation indicates **association rather than causation**.

### A/B Group Comparison

An additional A/B comparison produced:

| Group | Mean Consumption |
|---|---:|
| Group A | 119,898.09 |
| Group B | 76,264.13 |

The difference between the group means was approximately **43,633.97**, with Group A having a higher mean consumption than Group B.

---

## 9. Dashboard

The project includes an interactive Streamlit dashboard.

The dashboard allows users to:

- Explore household consumption data
- Filter observations
- Compare consumption patterns
- Examine urban-rural differences
- Explore household-size relationships
- View statistical results
- Interact with visualizations

### Running the Dashboard Locally

Clone the repository and navigate to the project directory:

```bash
cd Urban-Rural-Consumption-Capstone
```

Install the project dependencies using `uv`:

```bash
uv sync
```

Run the Streamlit application:

```bash
uv run streamlit run app.py
```

The dashboard will then be available through the local Streamlit address displayed in the terminal.

---

## 10. Project Structure

```text
Urban-Rural-Consumption-Capstone/
│
├── app.py
│
├── data/
│   └── processed/
│       └── analysis_dataset.csv
│
├── figures/
│
├── notebooks/
│   └── urban_rural_consumption.ipynb
│
├── reports/
│
├── src/
│   └── __init__.py
│
├── tests/
│
├── pyproject.toml
│
├── README.md
│
└── .gitignore
```

---

## 11. Technologies Used

The project was developed using:

- **Python**
- **Pandas** – data manipulation
- **NumPy** – numerical computation
- **Matplotlib** – data visualization
- **Seaborn** – statistical visualization
- **SciPy** – statistical testing
- **Statsmodels** – regression analysis
- **Scikit-learn** – machine-learning/statistical utilities
- **Pyreadstat** – reading statistical data files
- **Plotly** – interactive visualization
- **Streamlit** – dashboard development
- **Jupyter Notebook** – exploratory and analytical work
- **uv** – Python project and dependency management
- **Git/GitHub** – version control and project hosting

---

## 12. Reproducibility

The project is organized to support reproducible analysis.

The main analytical workflow is contained in:

```text
notebooks/urban_rural_consumption.ipynb
```

The deployed application is contained in:

```text
app.py
```

Project dependencies are specified in:

```text
pyproject.toml
```

The repository uses Git for version control, allowing the development history and major project milestones to be tracked.

---

## 13. Limitations

Several limitations should be considered when interpreting the results:

1. The analysis is based on cross-sectional household survey data and therefore does not establish causal relationships.

2. Correlation results should not be interpreted as evidence of causation.

3. Survey weights and the complex survey design require careful consideration when generalizing estimates to the entire Kenyan population.

4. The analysis focuses on selected consumption and household characteristics rather than the complete range of socioeconomic determinants of household welfare.

---

## 14. Conclusion

The analysis demonstrates that household consumption patterns differ significantly between urban and rural households. The independent-samples t-test identified a statistically significant difference in non-food consumption, although the effect size was relatively small.

The correlation and regression analyses further demonstrate that household characteristics are associated with consumption, but the relatively low explanatory power of the regression model suggests that consumption is influenced by a wider range of socioeconomic factors.

The Streamlit dashboard translates these analytical findings into an interactive interface, demonstrating how data analysis can progress from raw survey data through statistical analysis to an accessible decision-support application.

---

## 15. Author

**Josephat Onhangwa Motonu**

MSc Artificial Intelligence (OUK), MSc. Applied Statistics (JKUAT), BSc. Applied Statistics (MSU), Data Science (Zindua Cosing School)

Kenya

---

## 16. Project Links

**GitHub Repository:**  
https://github.com/JMotonu/Urban-Rural-Consumption-Capstone

**Live Streamlit Dashboard:**  
https://urban-rural-consumption-capstone-ohlkfgoufgbtdeauyutcax.streamlit.app/

**Medium Article:** 
https://medium.com/@mtnjosephat/urban-vs-rural-consumption-in-kenya-from-household-data-to-an-interactive-data-story-e4790fe62249

**Slides:**
https://docs.google.com/presentation/d/1g8hU-81q7y967PhYeUEkSYim9K2Nu219/edit?slide=id.p1#slide=id.p1


---

## 17. Academic Context

This project was developed as an Zindua Cosing School academic data-science capstone demonstrating the application of:

**CRISP-DM → Data Preparation → Statistical Analysis → Visualization → Streamlit Deployment**

The project emphasizes reproducibility, interpretability, statistical reasoning, and practical deployment of data-analysis results.
