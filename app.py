
import streamlit as st
import pandas as pd
import sqlite3
import os

# Page config
st.set_page_config(
    page_title="ChocoCrunch Analytics",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🍫 ChocoCrunch Analytics Dashboard")
st.markdown("**Comprehensive data analysis of the global chocolate market**")

# Database connection
db_path = 'database/chococrunch.db'

if not os.path.exists(db_path):
    st.error(f"❌ Database not found at {db_path}")
    st.stop()

conn = sqlite3.connect(db_path)

# Sidebar navigation
st.sidebar.title("📊 Navigation")
query_option = st.sidebar.radio(
    "Select Query:",
    [
        "Query 21: Top 5 High-Calorie Brands",
        "Query 22: Avg Energy by Category",
        "Query 23: Ultra-Processed per Brand",
        "Query 24: High Sugar + High Calorie",
        "Query 25: Avg Sugar (Ultra-Processed)",
        "Query 26: FVN by Category",
        "Query 27: Top Sugar-to-Carb Ratio"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 This app displays SQL queries 21-27 for chocolate market analysis")

# ============================================================
# QUERY 21: Top 5 Brands With Most High Calorie Products
# ============================================================

if query_option == "Query 21: Top 5 High-Calorie Brands":
    st.header("Query 21: Top 5 Brands With Most High Calorie Products")
    st.markdown("Identify brands with the highest portfolio of high-calorie products")

    try:
        q21 = pd.read_sql_query('''
        SELECT
            p.brand,
            COUNT(d.product_code) as high_calorie_count,
            ROUND(AVG(n.energy_kcal), 1) as avg_calories,
            COUNT(DISTINCT p.product_code) as total_products,
            ROUND(100.0 * COUNT(d.product_code) / COUNT(DISTINCT p.product_code), 1) as percentage_high_cal
        FROM derived_metrics d
        JOIN product_info p ON d.product_code = p.product_code
        JOIN nutrient_info n ON d.product_code = n.product_code
        WHERE d.calorie_category = 'High Calorie' AND p.brand IS NOT NULL AND p.brand != ''
        GROUP BY p.brand
        ORDER BY high_calorie_count DESC
        LIMIT 5;
        ''', conn)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Top Brand", q21['brand'].values)
        with col2:
            st.metric("High-Calorie Count", int(q21['high_calorie_count'].values))
        with col3:
            st.metric("Avg Calories", f"{q21['avg_calories'].values:.1f} kcal")

        # Table
        st.subheader("Results")
        st.dataframe(q21, use_container_width=True)

        # Insights
        st.subheader("📊 Key Insights")
        st.info(f"""
        - **Top Brand**: {q21['brand'].values} with {int(q21['high_calorie_count'].values)} high-calorie products
        - **Avg Calories**: {q21['avg_calories'].values:.1f} kcal
        - **Focus Area**: These brands should develop healthier alternatives
        """)

    except Exception as e:
        st.error(f"Error executing query: {e}")

# ============================================================
# QUERY 22: Average Energy Per Calorie Category
# ============================================================

elif query_option == "Query 22: Avg Energy by Category":
    st.header("Query 22: Average Energy Per Calorie Category")
    st.markdown("Validate calorie category thresholds and show energy distribution")

    try:
        q22 = pd.read_sql_query('''
        SELECT
            d.calorie_category,
            ROUND(AVG(n.energy_kcal), 1) as avg_energy,
            ROUND(MIN(n.energy_kcal), 1) as min_energy,
            ROUND(MAX(n.energy_kcal), 1) as max_energy,
            COUNT(*) as product_count
        FROM derived_metrics d
        JOIN nutrient_info n ON d.product_code = n.product_code
        WHERE d.calorie_category != 'Unknown'
        GROUP BY d.calorie_category
        ORDER BY avg_energy DESC;
        ''', conn)

        # Metrics
        cols = st.columns(len(q22))
        for idx, (col, row) in enumerate(zip(cols, q22.itertuples(index=False))):
            with col:
                st.metric(row.calorie_category, f"{row.avg_energy:.1f} kcal")

        # Table
        st.subheader("Results")
        st.dataframe(q22, use_container_width=True)

        # Chart
        st.subheader("📈 Energy Distribution")
        chart_data = q22[['calorie_category', 'avg_energy']]
        st.bar_chart(chart_data.set_index('calorie_category'))

    except Exception as e:
        st.error(f"Error executing query: {e}")

# ============================================================
# QUERY 23: Count Of Ultra-Processed Products Per Brand
# ============================================================

elif query_option == "Query 23: Ultra-Processed per Brand":
    st.header("Query 23: Ultra-Processed Products Per Brand")
    st.markdown("Identify brands relying heavily on ultra-processed products")

    try:
        q23 = pd.read_sql_query('''
        SELECT
            p.brand,
            SUM(CASE WHEN d.is_ultra_processed = 'Yes' THEN 1 ELSE 0 END) as ultra_processed_count,
            COUNT(*) as total_products,
            ROUND(100.0 * SUM(CASE WHEN d.is_ultra_processed = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) as percentage_ultra_processed
        FROM derived_metrics d
        JOIN product_info p ON d.product_code = p.product_code
        WHERE p.brand IS NOT NULL AND p.brand != ''
        GROUP BY p.brand
        HAVING ultra_processed_count > 0
        ORDER BY percentage_ultra_processed DESC
        LIMIT 15;
        ''', conn)

        # Metrics
        high_ultra = len(q23[q23['percentage_ultra_processed']>80])
        st.metric("Brands with >80% Ultra-Processed", high_ultra)

        # Table
        st.subheader("Results (Top 15)")
        st.dataframe(q23, use_container_width=True)

        # Chart
        st.subheader("📊 Ultra-Processed Percentage by Brand")
        chart_data = q23[['brand', 'percentage_ultra_processed']].head(10)
        st.bar_chart(chart_data.set_index('brand'))

    except Exception as e:
        st.error(f"Error executing query: {e}")

# ============================================================
# QUERY 24: High Sugar + High Calorie Products
# ============================================================

elif query_option == "Query 24: High Sugar + High Calorie":
    st.header("Query 24: High Sugar + High Calorie Products")
    st.markdown("⚠️ Identify 'DOUBLE RISK' products (high calorie + high sugar)")

    try:
        q24 = pd.read_sql_query('''
        SELECT
            p.product_name,
            p.brand,
            n.energy_kcal,
            n.sugars,
            n.fat,
            ROUND(d.sugar_to_carb_ratio, 2) as sugar_to_carb_ratio
        FROM derived_metrics d
        JOIN product_info p ON d.product_code = p.product_code
        JOIN nutrient_info n ON d.product_code = n.product_code
        WHERE d.calorie_category = 'High Calorie'
            AND d.sugar_category = 'High Sugar'
        ORDER BY n.energy_kcal DESC, n.sugars DESC
        LIMIT 20;
        ''', conn)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Products Found", len(q24))
        with col2:
            st.metric("Highest Calories", f"{q24['energy_kcal'].max():.0f} kcal")
        with col3:
            st.metric("Highest Sugar", f"{q24['sugars'].max():.1f}g")

        # Warning
        st.warning("🔴 These are the worst-case products for consumer health. Consumer advisory: Products to avoid.")

        # Table
        st.subheader("Results (Top 20)")
        st.dataframe(q24, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")

# ============================================================
# QUERY 25: Average Sugar Per Brand For Ultra-Processed
# ============================================================

elif query_option == "Query 25: Avg Sugar (Ultra-Processed)":
    st.header("Query 25: Average Sugar in Ultra-Processed Products")
    st.markdown("Compare brands specifically on ultra-processed chocolate quality")

    try:
        q25 = pd.read_sql_query('''
        SELECT
            p.brand,
            COUNT(*) as ultra_processed_count,
            ROUND(AVG(n.sugars), 2) as avg_sugar,
            ROUND(MIN(n.sugars), 2) as min_sugar,
            ROUND(MAX(n.sugars), 2) as max_sugar,
            ROUND(AVG(n.energy_kcal), 1) as avg_calories
        FROM derived_metrics d
        JOIN product_info p ON d.product_code = p.product_code
        JOIN nutrient_info n ON d.product_code = n.product_code
        WHERE d.is_ultra_processed = 'Yes'
            AND p.brand IS NOT NULL
            AND p.brand != ''
        GROUP BY p.brand
        HAVING COUNT(*) >= 2
        ORDER BY avg_sugar DESC
        LIMIT 10;
        ''', conn)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Highest Sugar Brand", q25['brand'].values)
        with col2:
            st.metric("Avg Sugar", f"{q25['avg_sugar'].values:.1f}g")
        with col3:
            st.metric("Sugar Range", f"{q25['avg_sugar'].min():.1f}g - {q25['avg_sugar'].max():.1f}g")

        # Table
        st.subheader("Results")
        st.dataframe(q25, use_container_width=True)

        # Chart
        st.subheader("📊 Avg Sugar by Brand")
        chart_data = q25[['brand', 'avg_sugar']]
        st.bar_chart(chart_data.set_index('brand'))

    except Exception as e:
        st.error(f"Error executing query: {e}")

# ============================================================
# QUERY 26: Products With Fruits/Vegetables/Nuts
# ============================================================

elif query_option == "Query 26: FVN by Category":
    st.header("Query 26: Products With Fruits/Vegetables/Nuts By Category")
    st.markdown("Identify healthier options by calorie tier")

    try:
        q26 = pd.read_sql_query('''
        SELECT
            d.calorie_category,
            COUNT(*) as total_products,
            SUM(CASE WHEN n.fruits_vegetables_nuts > 0 THEN 1 ELSE 0 END) as products_with_fvn,
            ROUND(100.0 * SUM(CASE WHEN n.fruits_vegetables_nuts > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as percentage_with_fvn
        FROM derived_metrics d
        JOIN nutrient_info n ON d.product_code = n.product_code
        WHERE d.calorie_category != 'Unknown'
        GROUP BY d.calorie_category
        ORDER BY percentage_with_fvn DESC;
        ''', conn)

        # Metrics
        cols = st.columns(len(q26))
        for col, row in zip(cols, q26.itertuples(index=False)):
            with col:
                st.metric(row.calorie_category, f"{row.percentage_with_fvn:.1f}%")

        # Table
        st.subheader("Results")
        st.dataframe(q26, use_container_width=True)

        # Chart
        st.subheader("📊 FVN Percentage by Category")
        chart_data = q26[['calorie_category', 'percentage_with_fvn']]
        st.bar_chart(chart_data.set_index('calorie_category'))

    except Exception as e:
        st.error(f"Error executing query: {e}")

# ============================================================
# QUERY 27: Top 5 Products By Sugar-to-Carb Ratio
# ============================================================

elif query_option == "Query 27: Top Sugar-to-Carb Ratio":
    st.header("Query 27: Top 5 Products By Sugar-to-Carb Ratio")
    st.markdown("Most sugar-concentrated products (% of carbs that are sugar)")

    try:
        q27 = pd.read_sql_query('''
        SELECT
            p.product_name,
            p.brand,
            ROUND(d.sugar_to_carb_ratio, 3) as sugar_to_carb_ratio,
            ROUND(d.sugar_to_carb_ratio * 100, 1) as percentage_sugar,
            n.sugars,
            n.carbohydrates,
            d.calorie_category
        FROM derived_metrics d
        JOIN product_info p ON d.product_code = p.product_code
        JOIN nutrient_info n ON d.product_code = n.product_code
        WHERE d.sugar_to_carb_ratio IS NOT NULL
        ORDER BY d.sugar_to_carb_ratio DESC
        LIMIT 5;
        ''', conn)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Highest Ratio", f"{q27['sugar_to_carb_ratio'].values:.3f}")
        with col2:
            st.metric("Sugar %", f"{q27['percentage_sugar'].values:.1f}%")
        with col3:
            st.metric("Product", q27['product_name'].values[:20])

        # Warning
        st.warning(f"⚠️ Extreme case: {q27['percentage_sugar'].values:.1f}% of carbs are sugar!")

        # Table
        st.subheader("Results (Top 5)")
        st.dataframe(q27, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")

# Close connection
conn.close()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p><small>ChocoCrunch Analytics Dashboard | Data Science Project | GUVI</small></p>
</div>
""", unsafe_allow_html=True)
