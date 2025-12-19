
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="🍫 ChocoCrunch Analytics Dashboard",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================
st.markdown("""
    <style>
        .main-header {
            font-size: 48px;
            color: #8B4513;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .metric-card {
            background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
        }
        .metric-value {
            font-size: 36px;
            color: #FFD700;
        }
        .metric-label {
            font-size: 14px;
            color: #F5DEB3;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# LOAD DATA FROM CSV
# ============================================================================
@st.cache_data
def load_data():
    """Load the cleaned dataset from CSV"""
    try:
        df = pd.read_csv('ChocoCrunch_Cleaned_Dataset.csv')
        return df
    except:
        st.error("❌ Could not load dataset. Ensure 'ChocoCrunch_Cleaned_Dataset.csv' is in the same directory.")
        return None

@st.cache_resource
def create_sqlite_db(df):
    """Create SQLite database from the dataset"""
    conn = sqlite3.connect(':memory:')

    # Create product_info table
    product_info = df[['product_code', 'product_name', 'brand']].drop_duplicates('product_code')
    product_info.to_sql('product_info', conn, if_exists='replace', index=False)

    # Create nutrient_info table
    nutrient_cols = ['product_code', 'energy-kcal_value', 'energy-kj_value',
                     'carbohydrates_value', 'sugars_value', 'fat_value',
                     'saturated-fat_value', 'proteins_value', 'fiber_value',
                     'salt_value', 'sodium_value', 'nutrition-score-fr', 'nova-group',
                     'fruits-vegetables-nuts-estimate-from-ingredients_100g']
    nutrient_info = df[nutrient_cols]
    nutrient_info.to_sql('nutrient_info', conn, if_exists='replace', index=False)

    # Create derived_metrics table
    derived_cols = ['product_code', 'sugar_to_carb_ratio', 'calorie_category',
                   'sugar_category', 'is_ultra_processed']
    derived_metrics = df[derived_cols]
    derived_metrics.to_sql('derived_metrics', conn, if_exists='replace', index=False)

    return conn

# ============================================================================
# SQL QUERY EXECUTION FUNCTION
# ============================================================================
def execute_query(conn, query):
    """Execute SQL query and return results as DataFrame"""
    try:
        result = pd.read_sql_query(query, conn)
        return result
    except Exception as e:
        st.error(f"❌ Query Error: {str(e)}")
        return pd.DataFrame()

# ============================================================================
# MAIN DASHBOARD
# ============================================================================
def main():
    # Header
    st.markdown('<div class="main-header">🍫✨ ChocoCrunch Analytics Dashboard</div>',
                unsafe_allow_html=True)
    st.markdown("**Sweet Stats & Sour Truths: Global Chocolate Market Analysis**")
    st.markdown("---")

    # Load data
    df = load_data()
    if df is None:
        return

    # Create database
    conn = create_sqlite_db(df)

    # ========================================================================
    # SIDEBAR NAVIGATION
    # ========================================================================
    with st.sidebar:
        st.header("📊 Navigation")
        page = st.radio("Select Section:",
                       ["📈 Dashboard Overview",
                        "🔍 Product Info Queries",
                        "🥗 Nutrient Info Queries",
                        "📉 Derived Metrics Queries",
                        "🔗 Join Queries",
                        "📊 EDA Visualizations",
                        "📋 Data Summary"])

    # ========================================================================
    # PAGE 1: DASHBOARD OVERVIEW & KEY METRICS
    # ========================================================================
    if page == "📈 Dashboard Overview":
        st.header("📈 Key Metrics Overview")

        # Calculate key metrics
        total_products = len(df)
        unique_brands = df['brand'].nunique()
        avg_calories = df['energy-kcal_value'].mean()
        avg_sugar = df['sugars_value'].mean()
        ultra_processed_pct = (df['is_ultra_processed'].value_counts().get('Yes', 0) / len(df)) * 100
        high_calorie_count = len(df[df['calorie_category'] == 'High Calorie'])

        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_products}</div>
                    <div class="metric-label">Total Products</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{unique_brands}</div>
                    <div class="metric-label">Unique Brands</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_calories:.0f}</div>
                    <div class="metric-label">Avg Calories (kcal)</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{ultra_processed_pct:.1f}%</div>
                    <div class="metric-label">Ultra-Processed</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Quick statistics
        st.subheader("🎯 Quick Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("High Calorie Products", high_calorie_count, f"{(high_calorie_count/total_products)*100:.1f}%")
            st.metric("Avg Sugar Content (g)", f"{avg_sugar:.1f}")

        with col2:
            high_sugar = len(df[df['sugar_category'] == 'High Sugar'])
            st.metric("High Sugar Products", high_sugar, f"{(high_sugar/total_products)*100:.1f}%")
            st.metric("Avg Fat Content (g)", f"{df['fat_value'].mean():.1f}")

        with col3:
            with_fruits = len(df[df['fruits-vegetables-nuts-estimate-from-ingredients_100g'] > 0])
            st.metric("With Fruits/Veg/Nuts", with_fruits, f"{(with_fruits/total_products)*100:.1f}%")
            st.metric("Avg Protein (g)", f"{df['proteins_value'].mean():.1f}")

        st.markdown("---")

        # Top brands visualization
        st.subheader("🏆 Top Brands by Product Count")
        top_brands = df['brand'].value_counts().head(10)
        fig = px.bar(x=top_brands.values, y=top_brands.index, orientation='h',
                     labels={'x': 'Number of Products', 'y': 'Brand'},
                     title="Top 10 Brands",
                     color=top_brands.values,
                     color_continuous_scale='YlOrBr')
        st.plotly_chart(fig, use_container_width=True)

        # Distribution charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Distribution by Calorie Category")
            calorie_dist = df['calorie_category'].value_counts()
            fig = px.pie(values=calorie_dist.values, names=calorie_dist.index,
                        title="Calorie Category Distribution",
                        color_discrete_sequence=['#FFD700', '#FF8C00', '#8B0000'])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("🍬 Distribution by Sugar Category")
            sugar_dist = df['sugar_category'].value_counts()
            fig = px.pie(values=sugar_dist.values, names=sugar_dist.index,
                        title="Sugar Category Distribution",
                        color_discrete_sequence=['#90EE90', '#FFD700', '#FF6347'])
            st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # PAGE 2: PRODUCT INFO QUERIES
    # ========================================================================
    elif page == "🔍 Product Info Queries":
        st.header("🔍 Product Information Queries")
        st.markdown("*Queries from the `product_info` table*")

        query_tabs = st.tabs([
            "Products per Brand",
            "Unique Products per Brand",
            "Top 5 Brands",
            "Missing Product Names",
            "Total Unique Brands",
            "Codes Starting with '3'"
        ])

        # Query 1: Count products per brand
        with query_tabs[0]:
            st.subheader("1️⃣ Count Products per Brand")
            query = """
            SELECT brand, COUNT(product_code) as product_count
            FROM product_info
            WHERE brand IS NOT NULL
            GROUP BY brand
            ORDER BY product_count DESC
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)
            st.metric("Total Brands", len(result))

        # Query 2: Count unique products per brand
        with query_tabs[1]:
            st.subheader("2️⃣ Count Unique Products per Brand")
            query = """
            SELECT brand, COUNT(DISTINCT product_code) as unique_products
            FROM product_info
            WHERE brand IS NOT NULL
            GROUP BY brand
            ORDER BY unique_products DESC
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

        # Query 3: Top 5 brands
        with query_tabs[2]:
            st.subheader("3️⃣ Top 5 Brands by Product Count")
            query = """
            SELECT brand, COUNT(product_code) as product_count
            FROM product_info
            WHERE brand IS NOT NULL
            GROUP BY brand
            ORDER BY product_count DESC
            LIMIT 5
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.bar(result, x='brand', y='product_count',
                        title="Top 5 Brands", labels={'product_count': 'Product Count'})
            st.plotly_chart(fig, use_container_width=True)

        # Query 4: Products with missing names
        with query_tabs[3]:
            st.subheader("4️⃣ Products with Missing Product Names")
            query = """
            SELECT product_code, brand
            FROM product_info
            WHERE product_name IS NULL
            """
            result = execute_query(conn, query)
            if len(result) > 0:
                st.dataframe(result, use_container_width=True)
                st.warning(f"⚠️ {len(result)} products have missing names")
            else:
                st.success("✅ No products with missing names!")

        # Query 5: Total unique brands
        with query_tabs[4]:
            st.subheader("5️⃣ Number of Unique Brands")
            query = """
            SELECT COUNT(DISTINCT brand) as total_brands
            FROM product_info
            WHERE brand IS NOT NULL
            """
            result = execute_query(conn, query)
            total_brands = result['total_brands'].values[0]
            st.metric("Unique Brands", total_brands)
            st.dataframe(result, use_container_width=True)

        # Query 6: Codes starting with '3'
        with query_tabs[5]:
            st.subheader("6️⃣ Products with Code Starting with '3'")
            query = """
            SELECT product_code, product_name, brand
            FROM product_info
            WHERE product_code LIKE '3%'
            LIMIT 20
            """
            result = execute_query(conn, query)
            if len(result) > 0:
                st.dataframe(result, use_container_width=True)
                st.info(f"📍 Found {len(result)} products with codes starting with '3'")
            else:
                st.info("No products found with codes starting with '3'")

    # ========================================================================
    # PAGE 3: NUTRIENT INFO QUERIES
    # ========================================================================
    elif page == "🥗 Nutrient Info Queries":
        st.header("🥗 Nutrient Information Queries")
        st.markdown("*Queries from the `nutrient_info` table*")

        query_tabs = st.tabs([
            "Top 10 Highest Energy",
            "Avg Sugar per NOVA Group",
            "Fat Content > 20g",
            "Avg Carbohydrates",
            "Sodium > 1g",
            "With Fruits/Veg/Nuts",
            "Energy > 500 kcal"
        ])

        # Query 1: Top 10 highest energy
        with query_tabs[0]:
            st.subheader("1️⃣ Top 10 Products with Highest Energy")
            query = """
            SELECT product_code, energy_kcal_value, energy_kj_value
            FROM nutrient_info
            ORDER BY energy_kcal_value DESC
            LIMIT 10
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.bar(result, x='product_code', y='energy_kcal_value',
                        title="Top 10 Highest Energy Products",
                        labels={'energy_kcal_value': 'Energy (kcal)'})
            st.plotly_chart(fig, use_container_width=True)

        # Query 2: Average sugar per NOVA group
        with query_tabs[1]:
            st.subheader("2️⃣ Average Sugar per NOVA Group")
            query = """
            SELECT nova_group, ROUND(AVG(sugars_value), 2) as avg_sugar, COUNT(*) as product_count
            FROM nutrient_info
            GROUP BY nova_group
            ORDER BY nova_group
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.bar(result, x='nova_group', y='avg_sugar',
                        title="Average Sugar Content by NOVA Group",
                        labels={'nova_group': 'NOVA Group', 'avg_sugar': 'Avg Sugar (g)'})
            st.plotly_chart(fig, use_container_width=True)

        # Query 3: Fat content > 20g
        with query_tabs[2]:
            st.subheader("3️⃣ Count Products with Fat > 20g")
            query = """
            SELECT COUNT(product_code) as high_fat_products
            FROM nutrient_info
            WHERE fat_value > 20
            """
            result = execute_query(conn, query)
            count = result['high_fat_products'].values[0]
            st.metric("Products with Fat > 20g", count)
            st.dataframe(result, use_container_width=True)

        # Query 4: Average carbohydrates
        with query_tabs[3]:
            st.subheader("4️⃣ Average Carbohydrates per Product")
            query = """
            SELECT ROUND(AVG(carbohydrates_value), 2) as avg_carbohydrates,
                   MIN(carbohydrates_value) as min_carbs,
                   MAX(carbohydrates_value) as max_carbs
            FROM nutrient_info
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

        # Query 5: Sodium > 1g
        with query_tabs[4]:
            st.subheader("5️⃣ Products with Sodium > 1g")
            query = """
            SELECT product_code, sodium_value
            FROM nutrient_info
            WHERE sodium_value > 1.0
            ORDER BY sodium_value DESC
            """
            result = execute_query(conn, query)
            if len(result) > 0:
                st.dataframe(result, use_container_width=True)
            else:
                st.success("✅ No products exceed 1g sodium per 100g!")

        # Query 6: With fruits/veg/nuts
        with query_tabs[5]:
            st.subheader("6️⃣ Products with Fruits/Vegetables/Nuts Content")
            query = """
            SELECT COUNT(product_code) as products_with_fvn
            FROM nutrient_info
            WHERE `fruits-vegetables-nuts-estimate-from-ingredients_100g` > 0
            """
            result = execute_query(conn, query)
            count = result['products_with_fvn'].values[0]
            st.metric("Products with Fruits/Veg/Nuts", count)
            st.dataframe(result, use_container_width=True)

        # Query 7: Energy > 500 kcal
        with query_tabs[6]:
            st.subheader("7️⃣ Products with Energy > 500 kcal")
            query = """
            SELECT COUNT(product_code) as high_energy_products,
                   ROUND(AVG(energy_kcal_value), 2) as avg_energy
            FROM nutrient_info
            WHERE energy_kcal_value > 500
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

    # ========================================================================
    # PAGE 4: DERIVED METRICS QUERIES
    # ========================================================================
    elif page == "📉 Derived Metrics Queries":
        st.header("📉 Derived Metrics Queries")
        st.markdown("*Queries from the `derived_metrics` table with engineered features*")

        query_tabs = st.tabs([
            "Products per Calorie Cat",
            "High Sugar Count",
            "Avg Sugar-to-Carb Ratio",
            "High Calorie & Sugar",
            "Ultra-Processed Count",
            "Sugar-to-Carb > 0.7",
            "Avg Ratio per Category"
        ])

        # Query 1: Count per calorie category
        with query_tabs[0]:
            st.subheader("1️⃣ Count Products per Calorie Category")
            query = """
            SELECT calorie_category, COUNT(product_code) as product_count
            FROM derived_metrics
            GROUP BY calorie_category
            ORDER BY
                CASE WHEN calorie_category='Low Calorie' THEN 1
                     WHEN calorie_category='Moderate Calorie' THEN 2
                     WHEN calorie_category='High Calorie' THEN 3 END
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.bar(result, x='calorie_category', y='product_count',
                        title="Products by Calorie Category",
                        color='product_count',
                        color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig, use_container_width=True)

        # Query 2: High sugar count
        with query_tabs[1]:
            st.subheader("2️⃣ Count of High Sugar Products")
            query = """
            SELECT COUNT(product_code) as high_sugar_products
            FROM derived_metrics
            WHERE sugar_category = 'High Sugar'
            """
            result = execute_query(conn, query)
            count = result['high_sugar_products'].values[0]
            st.metric("High Sugar Products", count)
            st.dataframe(result, use_container_width=True)

        # Query 3: Avg sugar-to-carb ratio for high calorie
        with query_tabs[2]:
            st.subheader("3️⃣ Avg Sugar-to-Carb Ratio for High Calorie Products")
            query = """
            SELECT ROUND(AVG(sugar_to_carb_ratio), 3) as avg_ratio
            FROM derived_metrics
            WHERE calorie_category = 'High Calorie'
            """
            result = execute_query(conn, query)
            ratio = result['avg_ratio'].values[0]
            st.metric("Avg Sugar-to-Carb Ratio", f"{ratio:.3f}")
            st.dataframe(result, use_container_width=True)

        # Query 4: High calorie AND high sugar
        with query_tabs[3]:
            st.subheader("4️⃣ Products that are Both High Calorie & High Sugar")
            query = """
            SELECT COUNT(product_code) as risky_products
            FROM derived_metrics
            WHERE calorie_category = 'High Calorie'
            AND sugar_category = 'High Sugar'
            """
            result = execute_query(conn, query)
            count = result['risky_products'].values[0]
            st.warning(f"⚠️ {count} products are both High Calorie AND High Sugar")
            st.dataframe(result, use_container_width=True)

        # Query 5: Ultra-processed count
        with query_tabs[4]:
            st.subheader("5️⃣ Count of Ultra-Processed Products")
            query = """
            SELECT is_ultra_processed, COUNT(product_code) as product_count
            FROM derived_metrics
            GROUP BY is_ultra_processed
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.pie(result, values='product_count', names='is_ultra_processed',
                        title="Ultra-Processed vs Minimally-Processed",
                        color_discrete_map={'Yes': '#FF6B6B', 'No': '#4ECDC4'})
            st.plotly_chart(fig, use_container_width=True)

        # Query 6: Sugar-to-carb > 0.7
        with query_tabs[5]:
            st.subheader("6️⃣ Products with Sugar-to-Carb Ratio > 0.7")
            query = """
            SELECT COUNT(product_code) as high_ratio_products
            FROM derived_metrics
            WHERE sugar_to_carb_ratio > 0.7
            """
            result = execute_query(conn, query)
            count = result['high_ratio_products'].values[0]
            st.metric("High Sugar-to-Carb Ratio (>0.7)", count)
            st.dataframe(result, use_container_width=True)

        # Query 7: Avg ratio per category
        with query_tabs[6]:
            st.subheader("7️⃣ Average Sugar-to-Carb Ratio per Calorie Category")
            query = """
            SELECT calorie_category, ROUND(AVG(sugar_to_carb_ratio), 3) as avg_ratio
            FROM derived_metrics
            GROUP BY calorie_category
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.bar(result, x='calorie_category', y='avg_ratio',
                        title="Avg Sugar-to-Carb Ratio by Calorie Category",
                        labels={'avg_ratio': 'Avg Ratio', 'calorie_category': 'Calorie Category'})
            st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # PAGE 5: JOIN QUERIES
    # ========================================================================
    elif page == "🔗 Join Queries":
        st.header("🔗 Complex Join Queries")
        st.markdown("*Queries combining data from multiple tables*")

        query_tabs = st.tabs([
            "Top Brands High Cal",
            "Avg Energy per Cat",
            "Ultra-Processed Brands",
            "High Cal & High Sugar",
            "Avg Sugar per Brand",
            "Fruits/Veg per Cat",
            "Top 5 by Ratio"
        ])

        # Query 1: Top brands with high calorie
        with query_tabs[0]:
            st.subheader("1️⃣ Top 5 Brands with Most High Calorie Products")
            query = """
            SELECT pi.brand, COUNT(dm.product_code) as high_calorie_count
            FROM product_info pi
            JOIN derived_metrics dm ON pi.product_code = dm.product_code
            WHERE dm.calorie_category = 'High Calorie'
            GROUP BY pi.brand
            ORDER BY high_calorie_count DESC
            LIMIT 5
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.bar(result, x='brand', y='high_calorie_count',
                        title="Top 5 Brands with High Calorie Products",
                        labels={'high_calorie_count': 'High Calorie Count'})
            st.plotly_chart(fig, use_container_width=True)

        # Query 2: Average energy per category
        with query_tabs[1]:
            st.subheader("2️⃣ Average Energy per Calorie Category")
            query = """
            SELECT dm.calorie_category,
                   ROUND(AVG(ni.`energy-kcal_value`), 2) as avg_energy_kcal,
                   ROUND(AVG(ni.`energy-kj_value`), 2) as avg_energy_kj
            FROM nutrient_info ni
            JOIN derived_metrics dm ON ni.product_code = dm.product_code
            GROUP BY dm.calorie_category
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

        # Query 3: Ultra-processed per brand
        with query_tabs[2]:
            st.subheader("3️⃣ Count of Ultra-Processed Products per Brand")
            query = """
            SELECT pi.brand, COUNT(dm.product_code) as ultra_processed_count
            FROM product_info pi
            JOIN derived_metrics dm ON pi.product_code = dm.product_code
            WHERE dm.is_ultra_processed = 'Yes'
            GROUP BY pi.brand
            ORDER BY ultra_processed_count DESC
            LIMIT 10
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.bar(result, x='brand', y='ultra_processed_count',
                        title="Top 10 Brands with Ultra-Processed Products",
                        labels={'ultra_processed_count': 'Ultra-Processed Count'})
            st.plotly_chart(fig, use_container_width=True)

        # Query 4: High calorie and high sugar with brand
        with query_tabs[3]:
            st.subheader("4️⃣ Products that are Both High Calorie & High Sugar with Brand")
            query = """
            SELECT pi.product_name, pi.brand, ni.`energy-kcal_value`, ni.sugars_value
            FROM product_info pi
            JOIN nutrient_info ni ON pi.product_code = ni.product_code
            JOIN derived_metrics dm ON pi.product_code = dm.product_code
            WHERE dm.calorie_category = 'High Calorie'
            AND dm.sugar_category = 'High Sugar'
            ORDER BY ni.`energy-kcal_value` DESC
            LIMIT 15
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)
            st.warning(f"⚠️ {len(result)} risky products identified")

        # Query 5: Average sugar per brand for ultra-processed
        with query_tabs[4]:
            st.subheader("5️⃣ Average Sugar Content per Brand for Ultra-Processed Products")
            query = """
            SELECT pi.brand,
                   ROUND(AVG(ni.sugars_value), 2) as avg_sugar,
                   COUNT(dm.product_code) as ultra_processed_count
            FROM product_info pi
            JOIN nutrient_info ni ON pi.product_code = ni.product_code
            JOIN derived_metrics dm ON pi.product_code = dm.product_code
            WHERE dm.is_ultra_processed = 'Yes'
            GROUP BY pi.brand
            ORDER BY avg_sugar DESC
            LIMIT 10
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

            fig = px.scatter(result, x='brand', y='avg_sugar', size='ultra_processed_count',
                           title="Avg Sugar in Ultra-Processed Products by Brand",
                           labels={'avg_sugar': 'Avg Sugar (g)'})
            st.plotly_chart(fig, use_container_width=True)

        # Query 6: Fruits/veg per category
        with query_tabs[5]:
            st.subheader("6️⃣ Count of Products with Fruits/Vegetables/Nuts per Calorie Category")
            query = """
            SELECT dm.calorie_category,
                   COUNT(CASE WHEN ni.`fruits-vegetables-nuts-estimate-from-ingredients_100g` > 0
                             THEN 1 END) as with_fvn,
                   COUNT(dm.product_code) as total_products
            FROM nutrient_info ni
            JOIN derived_metrics dm ON ni.product_code = dm.product_code
            GROUP BY dm.calorie_category
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

        # Query 7: Top 5 by sugar-to-carb ratio
        with query_tabs[6]:
            st.subheader("7️⃣ Top 5 Products by Sugar-to-Carb Ratio")
            query = """
            SELECT pi.product_name, pi.brand, dm.sugar_to_carb_ratio,
                   dm.calorie_category, dm.sugar_category
            FROM product_info pi
            JOIN derived_metrics dm ON pi.product_code = dm.product_code
            ORDER BY dm.sugar_to_carb_ratio DESC
            LIMIT 5
            """
            result = execute_query(conn, query)
            st.dataframe(result, use_container_width=True)

    # ========================================================================
    # PAGE 6: EDA VISUALIZATIONS
    # ========================================================================
    elif page == "📊 EDA Visualizations":
        st.header("📊 Exploratory Data Analysis Visualizations")

        viz_tabs = st.tabs([
            "Calories vs Sugar",
            "Energy Distribution",
            "Sugar Content",
            "Nutritional Heatmap",
            "Top Brands Analysis",
            "NOVA Group Analysis",
            "Sugar-to-Carb Ratio",
            "Nutrient Box Plots",
            "Fat Content Analysis",
            "Protein Distribution"
        ])

        # Viz 1: Calories vs Sugar Scatter
        with viz_tabs[0]:
            st.subheader("1️⃣ Relationship: Calories vs Sugar Content")
            fig = px.scatter(df, x='energy-kcal_value', y='sugars_value',
                           color='calorie_category',
                           size='fat_value',
                           hover_data=['product_name', 'brand'],
                           title="Calories vs Sugar Content (Size = Fat)",
                           labels={'energy-kcal_value': 'Energy (kcal)',
                                   'sugars_value': 'Sugar (g)'},
                           color_discrete_map={'Low Calorie': '#90EE90',
                                              'Moderate Calorie': '#FFD700',
                                              'High Calorie': '#FF6347'})
            st.plotly_chart(fig, use_container_width=True)

        # Viz 2: Energy Distribution
        with viz_tabs[1]:
            st.subheader("2️⃣ Distribution of Energy Content")
            fig = px.histogram(df, x='energy-kcal_value', nbins=50,
                             title="Energy (kcal) Distribution",
                             labels={'energy-kcal_value': 'Energy (kcal)'},
                             color_discrete_sequence=['#8B4513'])
            fig.add_vline(x=df['energy-kcal_value'].mean(), line_dash="dash",
                         line_color="red", annotation_text="Mean")
            st.plotly_chart(fig, use_container_width=True)

        # Viz 3: Sugar Distribution
        with viz_tabs[2]:
            st.subheader("3️⃣ Distribution of Sugar Content")
            fig = px.histogram(df, x='sugars_value', nbins=50,
                             title="Sugar (g) Distribution",
                             labels={'sugars_value': 'Sugar (g)'},
                             color_discrete_sequence=['#FF69B4'])
            fig.add_vline(x=df['sugars_value'].mean(), line_dash="dash",
                         line_color="darkred", annotation_text="Mean")
            st.plotly_chart(fig, use_container_width=True)

        # Viz 4: Nutrient Heatmap
        with viz_tabs[3]:
            st.subheader("4️⃣ Nutrient Correlation Heatmap")
            numeric_cols = ['energy-kcal_value', 'carbohydrates_value', 'sugars_value',
                          'fat_value', 'proteins_value', 'sodium_value']
            corr_matrix = df[numeric_cols].corr()

            fig = px.imshow(corr_matrix,
                          labels=dict(x="Nutrient", y="Nutrient", color="Correlation"),
                          x=numeric_cols,
                          y=numeric_cols,
                          color_continuous_scale='RdBu',
                          zmin=-1, zmax=1,
                          title="Nutrient Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)

        # Viz 5: Top Brands Analysis
        with viz_tabs[4]:
            st.subheader("5️⃣ Top Brands - Average Nutrition")
            top_10_brands = df['brand'].value_counts().head(10).index
            df_top = df[df['brand'].isin(top_10_brands)]

            brand_nutrition = df_top.groupby('brand')[['energy-kcal_value', 'sugars_value', 'fat_value']].mean()

            fig = px.bar(brand_nutrition, barmode='group',
                       title="Average Nutrients by Top 10 Brands",
                       labels={'value': 'Content (g)', 'brand': 'Brand'},
                       color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            st.plotly_chart(fig, use_container_width=True)

        # Viz 6: NOVA Group Analysis
        with viz_tabs[5]:
            st.subheader("6️⃣ NOVA Group Distribution & Average Sugar")
            nova_analysis = df.groupby('nova-group').agg({
                'product_code': 'count',
                'sugars_value': 'mean'
            }).rename(columns={'product_code': 'count'})

            fig = px.bar(nova_analysis, barmode='group',
                       title="NOVA Group Analysis",
                       labels={'value': 'Value', 'nova-group': 'NOVA Group'},
                       color_discrete_sequence=['#95E1D3', '#F38181'])
            st.plotly_chart(fig, use_container_width=True)

        # Viz 7: Sugar-to-Carb Ratio Distribution
        with viz_tabs[6]:
            st.subheader("7️⃣ Sugar-to-Carb Ratio Distribution")
            fig = px.box(df, y='sugar_to_carb_ratio', x='calorie_category',
                        color='sugar_category',
                        title="Sugar-to-Carb Ratio by Calorie & Sugar Category",
                        labels={'sugar_to_carb_ratio': 'Ratio'})
            st.plotly_chart(fig, use_container_width=True)

        # Viz 8: Nutrient Box Plots
        with viz_tabs[7]:
            st.subheader("8️⃣ Nutritional Profile Box Plots")
            col1, col2 = st.columns(2)

            with col1:
                fig = px.box(df, y='fat_value',
                           title="Fat Distribution",
                           color_discrete_sequence=['#FF6B6B'])
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.box(df, y='proteins_value',
                           title="Protein Distribution",
                           color_discrete_sequence=['#4ECDC4'])
                st.plotly_chart(fig, use_container_width=True)

        # Viz 9: Fat Content Analysis
        with viz_tabs[8]:
            st.subheader("9️⃣ Fat Content Analysis")
            fat_categories = pd.cut(df['fat_value'], bins=[0, 20, 30, 50],
                                   labels=['Low Fat (<20g)', 'Medium Fat (20-30g)', 'High Fat (>30g)'])
            fat_dist = fat_categories.value_counts()

            fig = px.pie(values=fat_dist.values, names=fat_dist.index,
                        title="Products by Fat Category",
                        color_discrete_sequence=['#90EE90', '#FFD700', '#FF6347'])
            st.plotly_chart(fig, use_container_width=True)

        # Viz 10: Protein Distribution
        with viz_tabs[9]:
            st.subheader("1️⃣0️⃣ Protein Content Distribution")
            fig = px.histogram(df, x='proteins_value', nbins=40,
                             title="Protein (g) Distribution",
                             labels={'proteins_value': 'Protein (g)'},
                             color_discrete_sequence=['#4ECDC4'])
            fig.add_vline(x=df['proteins_value'].mean(), line_dash="dash",
                         line_color="darkblue", annotation_text="Mean")
            st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # PAGE 7: DATA SUMMARY
    # ========================================================================
    elif page == "📋 Data Summary":
        st.header("📋 Dataset Summary & Information")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Dataset Dimensions")
            st.metric("Total Records", len(df))
            st.metric("Total Features", len(df.columns))
            st.metric("Memory Usage (MB)", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}")

        with col2:
            st.subheader("🔢 Data Types")
            dtype_info = df.dtypes.value_counts()
            for dtype, count in dtype_info.items():
                st.metric(str(dtype), count)

        st.markdown("---")

        # Missing values analysis
        st.subheader("🔍 Missing Values Analysis")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Count': missing.values,
            'Missing %': missing_pct.values
        })
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)

        if len(missing_df) > 0:
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("✅ No missing values in the dataset!")

        st.markdown("---")

        # Statistical summary
        st.subheader("📈 Statistical Summary")
        st.dataframe(df.describe(), use_container_width=True)

        st.markdown("---")

        # Column information
        st.subheader("📋 Column Information")
        col_info = []
        for col in df.columns:
            col_info.append({
                'Column': col,
                'Type': str(df[col].dtype),
                'Non-Null': df[col].notna().sum(),
                'Unique': df[col].nunique()
            })
        st.dataframe(pd.DataFrame(col_info), use_container_width=True)

        st.markdown("---")

        # Data sample
        st.subheader("📝 First 10 Records")
        st.dataframe(df.head(10), use_container_width=True)

# ============================================================================
# RUN APPLICATION
# ============================================================================
if __name__ == "__main__":
    main()