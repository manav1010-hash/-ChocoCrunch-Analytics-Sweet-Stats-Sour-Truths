# ChocoCrunch Analytics Dashboard - AI Agent Guidelines

## Project Overview
Single-file Streamlit nutrition analytics dashboard analyzing chocolate product data. Uses SQLite in-memory database to enable SQL queries across three tables: `product_info`, `nutrient_info`, and `derived_metrics`. Seven-page dashboard with interactive visualizations.

## Architecture Patterns

### Data Layer
- **CSV Loading**: `load_data()` reads `ChocoCrunch_Cleaned_Dataset.csv` (required at runtime)
- **In-Memory SQLite**: `create_sqlite_db()` creates three normalized tables:
  - `product_info`: product_code, product_name, brand
  - `nutrient_info`: energy, macronutrients, micronutrients, NOVA classification
  - `derived_metrics`: engineered features (sugar_to_carb_ratio, calorie_category, sugar_category, is_ultra_processed)
- **Query Execution**: `execute_query()` standardizes error handling and returns DataFrames

### UI Layer (Streamlit)
- **Navigation**: Sidebar radio button controls page selection (emoji-prefixed page names)
- **Tabs Pattern**: Each page uses `st.tabs()` for organizing multiple related queries/visualizations
- **Styling**: Custom CSS with brown/chocolate color scheme (#8B4513, #D2691E, #FFD700)
- **Caching**: `@st.cache_data` for CSV load, `@st.cache_resource` for SQLite connection

## Key Conventions

### Column Names
Column names use hyphens (e.g., `energy-kcal_value`, `fruits-vegetables-nuts-estimate-from-ingredients_100g`). When querying in SQL with hyphens, use backticks: `` `energy-kcal_value` ``.

### Category Values
String categories use exact values (case-sensitive):
- Calorie: "Low Calorie", "Moderate Calorie", "High Calorie"
- Sugar: "High Sugar", "Low Sugar" (inferred from code pattern)
- Ultra-processed: "Yes", "No"

### Visualization Libraries
- **Plotly Express** (`px`): Primary charting (bar, scatter, pie, histogram, box, heatmap)
- **Matplotlib/Seaborn**: Imported but not heavily used in current implementation

### SQL Query Patterns
- Queries filter `WHERE brand IS NOT NULL` to avoid NULL brand issues
- Numeric aggregations use `ROUND(AVG(...), 2)` for readability
- CASE statements handle custom sorting (e.g., calorie category ordering)
- JOIN queries use three-table joins on `product_code` field

## Common Tasks

### Add a New Query Section
1. Add emoji-prefixed page name to sidebar radio options
2. Create new `elif page == "emoji Label":` block
3. Use `st.tabs()` to organize multiple queries within the section
4. Follow pattern: query → `execute_query()` → `st.dataframe()` + optional visualization
5. Add data validation checks (e.g., `if len(result) > 0:`)

### Add Visualization
- Use `px.bar()`, `px.scatter()`, `px.pie()`, `px.histogram()` (existing patterns)
- Include `use_container_width=True` for responsive layout
- Use brown/chocolate color scales: `'YlOrBr'`, `'RdYlGn_r'`, or custom maps
- Add hover labels for interactivity

### Modify SQL Queries
- Column names with hyphens require backticks
- Test against three normalized tables only (not raw CSV)
- Match exact string values for categories
- Use DISTINCT for brand/product code uniqueness checks

## File Structure
- **Single file**: `streamlit_app (2).py` (937 lines, not ideal for scale)
- **Data dependency**: Requires `ChocoCrunch_Cleaned_Dataset.csv` in working directory
- **No external modules** beyond standard data science stack (pandas, plotly, streamlit, sqlite3)

## Running the App
```bash
streamlit run "streamlit_app (2).py"
```
Requires CSV file in same directory as script. No command-line arguments or configuration files.

## Known Issues/Areas for Enhancement
- Bare `except:` clauses need specific exception handling
- Column names with hyphens brittle for maintenance
- 937-line monolithic file should be refactored (separate pages, utility modules)
- Missing values not validated before category assignment in CSV
