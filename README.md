# 🍫 ChocoCrunch Analytics - Data Science Project

**A comprehensive data science project analyzing the global chocolate market using Python, SQL, and Data Visualization.**

---

## 📋 Project Overview

ChocoCrunch Analytics is a complete data science solution for analyzing nutritional profiles, processing levels, and health metrics of chocolate products worldwide. The project includes database design, SQL analytics, Python automation, and an interactive Streamlit dashboard.

**Status**: ✅ Complete & Production-Ready

---

## 🎯 Project Objectives

1. **Extract & Process** chocolate product data from global sources
2. **Analyze** nutritional content, sugar levels, and processing methods
3. **Categorize** products by health risk profiles
4. **Visualize** insights through interactive dashboards
5. **Provide** data-driven recommendations for consumers and brands

---

## 📦 Project Structure

```
chococrunch-analytics/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── app.py                             # Streamlit application
│
├── database/
│   ├── chococrunch.db                # SQLite database
│   └── schema.sql                     # Database schema
│
├── data/
│   ├── raw/                          # Original datasets
│   │   ├── chocolate_data.csv
│   │   └── nutritional_info.csv
│   ├── processed/                    # Cleaned data
│   │   └── cleaned_chocolate.csv
│   └── extracted/                    # Full extraction (120 pages)
│       └── raw_chocolate_data.csv
│
├── notebooks/
│   ├── 01_data_extraction.ipynb       # Web scraping & API
│   ├── 02_data_cleaning.ipynb         # Data preprocessing
│   ├── 03_feature_engineering.ipynb   # Derived metrics
│   ├── 04_exploratory_analysis.ipynb  # EDA
│   └── 05_queries_21_27.ipynb         # Advanced SQL queries
│
├── scripts/
│   ├── extract_data.py                # Data extraction script
│   ├── create_database.py             # Database initialization
│   ├── data_cleaning.py               # Cleaning pipeline
│   └── run_queries.py                 # Query execution
│
└── assets/
    ├── dashboard_screenshots/         # UI screenshots
    └── documentation/                 # Technical docs
```

---

## 📊 Database Schema

### Tables

#### 1. **product_info**
```
product_code (PK)
product_name
brand
country_origin
manufacturer
cacao_percentage
price_per_unit
```

#### 2. **nutrient_info**
```
product_code (FK)
energy_kcal
protein_g
fat_g
saturated_fat_g
carbohydrates_g
sugars_g
fiber_g
sodium_mg
calcium_mg
iron_mg
fruits_vegetables_nuts (%)
nova_group (1-4)
```

#### 3. **derived_metrics**
```
product_code (FK)
calorie_category (Low/Moderate/High)
sugar_category (Low/Moderate/High)
fat_category (Low/Moderate/High)
is_ultra_processed (Yes/No)
health_score (0-100)
sugar_to_carb_ratio
processed_ingredient_ratio
```

#### 4. **market_analysis**
```
product_code (FK)
region
sales_volume
market_share (%)
price_trend
consumer_rating
```

---

## 🔍 SQL Queries Implemented

### Queries 1-20: Basic Analysis
- Product counts by category
- Average nutritional values
- Brand comparisons
- Health score distributions
- Sugar and calorie breakdowns

### Queries 21-27: Advanced JOIN Operations ⭐

| Query # | Name | Purpose |
|---------|------|---------|
| **21** | Top 5 Brands (High Calorie) | Identify brands with most high-calorie products |
| **22** | Avg Energy per Category | Validate calorie thresholds |
| **23** | Ultra-Processed per Brand | Brand reformulation needs |
| **24** | High Sugar + High Calorie | Double-risk product identification |
| **25** | Avg Sugar (Ultra-Processed) | Quality comparison |
| **26** | FVN by Category | Healthier alternatives |
| **27** | Top Sugar-to-Carb Ratio | Extreme sugar cases |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip or conda
- SQLite3
- 2GB disk space

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/chococrunch-analytics.git
cd chococrunch-analytics
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Verify Database
```bash
# Database should be at: database/chococrunch.db
# If not, run:
python scripts/create_database.py
```

---

## 📖 Usage

### Option 1: Streamlit Dashboard (Recommended)

```bash
streamlit run app.py
```

**Features:**
- 🎯 Interactive query navigation (Q21-Q27)
- 📊 Real-time visualizations
- 📈 Metrics and charts
- 🔍 Detailed insights
- 🌐 Web-based interface

**Access:** `http://localhost:8501`

---

### Option 2: Jupyter Notebooks

```bash
jupyter notebook
```

Navigate to `notebooks/` and open:
- `04_exploratory_analysis.ipynb` - Complete EDA
- `05_queries_21_27.ipynb` - Advanced analytics

---

### Option 3: Command Line

```bash
# Run all queries
python scripts/run_queries.py

# Extract data
python scripts/extract_data.py

# Clean data
python scripts/data_cleaning.py
```

---

## 📊 Key Metrics & Findings

### Market Overview
- **Total Products Analyzed**: 1,200+
- **Brands Covered**: 85+
- **Countries**: 45+
- **Data Points**: 120,000+

### Health Risk Assessment

**High Calorie + High Sugar Products**
- 🔴 **Found**: 240+ double-risk products
- ⚠️ **Top Brand**: Hacendado (85 products)
- 📈 **Average Calories**: 543.1 kcal
- 🍬 **Average Sugar**: 45-55g

**Ultra-Processed Analysis**
- 📦 **Ultra-Processed**: 620+ products (52%)
- 🏭 **Most Reliant Brands**: 80-100% ultra-processed
- 🎯 **Reformulation Needed**: 15+ brands

**Healthier Options**
- 🥗 **With Fruits/Veg/Nuts**: 85 products
- 📊 **Percentage**: 7-12% per category
- 💚 **Market Gap**: High demand opportunity

---

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **Database** | SQLite3 |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Streamlit, Matplotlib |
| **Analytics** | SQL (Complex JOINs, Aggregations) |
| **Notebooks** | Jupyter Lab |
| **Version Control** | Git |

---

## 📈 Dashboard Features

### Query Navigation (Sidebar)
- Select from 7 advanced queries (Q21-Q27)
- Real-time data loading
- Interactive filters

### Visualizations
- 📊 Bar charts (brands, categories)
- 📈 Energy distribution graphs
- 🥧 Percentage breakdowns
- 📋 Data tables with formatting

### Metrics Displays
- Top brands & products
- Highest values (calories, sugar, ratios)
- Category comparisons
- Health risk indicators

### Insights & Recommendations
- Data-driven findings
- Health advisories
- Brand recommendations
- Consumer warnings

---

## 📁 Data Files

### Raw Data
- `data/raw/chocolate_data.csv` (120 pages extracted)
- `data/raw/nutritional_info.csv`
- `data/raw/market_data.csv`

### Processed Data
- `data/processed/cleaned_chocolate.csv` (production-ready)
- `database/chococrunch.db` (SQLite database)

### Extraction
- `data/extracted/raw_chocolate_data.csv` (Full extraction)

---

## 🔐 Database Setup

### Create Database
```bash
python scripts/create_database.py
```

### Initialize Tables
```sql
-- Run schema.sql
sqlite3 database/chococrunch.db < database/schema.sql
```

### Load Data
```bash
python scripts/data_cleaning.py  # Cleans & loads data
```

---

## 📊 Sample Query Results

### Query 21: Top 5 Brands (High Calorie)
```
Brand        | High-Calorie Count | Avg Calories | % High-Cal
-------------|-------------------|--------------|----------
Hacendado    | 85                | 543.1        | 100.0
Unknown      | 83                | 544.7        | 100.0
Tesco        | 49                | 576.2        | 100.0
Gerble       | 45                | 452.1        | 100.0
Gullón       | 44                | 452.7        | 100.0
```

### Query 24: High Sugar + High Calorie Products
```
Product          | Brand      | Calories | Sugar | Risk Level
-----------------|------------|----------|-------|----------
Dark Choco Delux | Hacendado  | 580 kcal | 52g   | CRITICAL
Premium Belgian  | Tesco      | 565 kcal | 48g   | CRITICAL
Cacao Paradise   | Gullón     | 541 kcal | 50g   | CRITICAL
```

---

## 🎓 Learning Outcomes

This project demonstrates:

✅ **Data Science Skills**
- Web scraping & API integration
- Data cleaning & preprocessing
- Feature engineering
- SQL optimization
- Data visualization

✅ **Technical Skills**
- Python programming (Pandas, NumPy)
- Database design & SQL
- Streamlit app development
- Jupyter notebook workflows
- Git version control

✅ **Business Skills**
- Data analysis & interpretation
- Insight generation
- Recommendation formulation
- Dashboard communication

---

## 🚦 Getting Help

### Common Issues

**1. Database Not Found**
```bash
python scripts/create_database.py
python scripts/data_cleaning.py
```

**2. Streamlit Won't Run**
```bash
pip install --upgrade streamlit
streamlit run app.py --logger.level=debug
```

**3. Missing Dependencies**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🗺️ Project Roadmap

### ✅ Completed
- [x] Data extraction (120 pages)
- [x] Database design & creation
- [x] Data cleaning & preprocessing
- [x] Feature engineering (derived metrics)
- [x] SQL queries 1-27
- [x] Streamlit dashboard
- [x] Documentation

### 🔄 In Progress
- [ ] Advanced machine learning models
- [ ] Predictive analytics
- [ ] Real-time data updates
- [ ] Mobile app version

### 📋 Future Plans
- [ ] API development
- [ ] Cloud deployment (AWS/Azure)
- [ ] Mobile-responsive design
- [ ] Multi-language support
- [ ] Advanced forecasting

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Products | 1,200+ |
| Brands Analyzed | 85+ |
| Countries | 45+ |
| Data Points | 120,000+ |
| SQL Queries | 27 |
| Dashboard Pages | 7 |
| Queries 21-27 | ✅ Completed |
| Documentation | ✅ Complete |
| Production Ready | ✅ Yes |

---

## 🎯 Next Steps

1. **Clone** the repository
2. **Install** dependencies (`pip install -r requirements.txt`)
3. **Run** Streamlit (`streamlit run app.py`)
4. **Explore** queries 21-27
5. **Analyze** insights
6. **Share** findings

---

## 📝 Changelog

### v1.0.0 (Current)
- ✅ Complete data extraction
- ✅ Database implementation
- ✅ All 27 SQL queries
- ✅ Streamlit dashboard
- ✅ Full documentation

---

## 📚 Additional Resources

### Documentation
- `database/schema.sql` - Database structure
- `notebooks/` - Jupyter notebooks with detailed explanations
- `scripts/` - Automated workflows
  
---

## ⭐ Show Your Support

If you found this project helpful:
- ⭐ Star the repository
- 🍴 Fork for your own use
- 💬 Share feedback
- 📤 Contribute improvements

---

**Made with ❤️ by GUVI Data Science Student | 2025**

