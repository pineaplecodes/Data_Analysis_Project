import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set page layout to wide
st.set_page_config(layout="wide")

# CSS to center the title
st.markdown("""
    <style>
    .center-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Title with center alignment using HTML
st.markdown('<p class="center-title">E-Commerce Insights: Seller, Payment, and Transaction Overview</p>', unsafe_allow_html=True)

# Plot functions with updated pyplot usage
def show_bar_chart(dataframe):
    top_10_cities = dataframe.head(10)
    colors = plt.cm.Blues(np.linspace(0.8, 0.2, len(top_10_cities)))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_10_cities['seller_city'], top_10_cities['Total_Seller'], color=colors)
    ax.set_xlabel('City')
    ax.set_ylabel('Total Sellers')
    ax.set_title('Top 10 Cities by Total Sellers')
    ax.set_xticks(range(len(top_10_cities)))
    ax.set_xticklabels(top_10_cities['seller_city'], rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

def show_category_bar_chart(dataframe):
    top_10_categories = dataframe.head(10)
    max_value = top_10_categories.max()
    colors = ['darkred' if value == max_value else 'lightcoral' for value in top_10_categories]
    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.bar(top_10_categories.index, top_10_categories, color=colors)
    ax.set_title('Top 10 Product Category Distribution', fontsize=16, pad=20)
    ax.set_xlabel('Product Category', fontsize=12)
    ax.set_ylabel('Number of Products', fontsize=12)
    ax.set_xticks(range(len(top_10_categories)))
    ax.set_xticklabels(top_10_categories.index, rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

def show_payment_chart(df_payments):
    grouped_data = df_payments.groupby("payment_type")["payment_value"].sum().reset_index()
    grouped_data = grouped_data.sort_values(by="payment_value", ascending=False)
    max_value = grouped_data['payment_value'].max()
    colors = ['#FF1493' if value == max_value else '#FFB6C1' for value in grouped_data['payment_value']]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(grouped_data['payment_type'], grouped_data['payment_value'], color=colors)
    ax.set_xlabel('Total Payment Value')
    ax.set_ylabel('Payment Type')
    ax.set_title('Total Payment Value by Payment Type')
    ax.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig)

def show_transaction_binning_chart(df_payments):
    bins = [0, 100, 500, float('inf')] 
    labels = ['Small Transaction', 'Medium Transaction', 'Large Transaction'] 
    df_payments['transaction_category'] = pd.cut(df_payments['payment_value'], bins=bins, labels=labels, right=False)
    transaction_binning = df_payments.groupby('transaction_category').size()
    colors = plt.cm.Greens(np.linspace(0.8, 0.4, len(transaction_binning)))
    
    fig, ax = plt.subplots(figsize=(8, 2))
    wedges, texts, autotexts = ax.pie(
        transaction_binning, 
        labels=transaction_binning.index, 
        colors=colors, 
        autopct='%1.1f%%', 
        startangle=90, 
        wedgeprops={'edgecolor': 'white'}, 
        pctdistance=0.85,
        textprops={'fontsize': 4}
    )
    
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    ax.add_artist(centre_circle)
    
    # Menambahkan judul
    ax.set_title('Transaction Distribution Based on Value Category', fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)


# Load dataframes
df_sellers = pd.read_csv('https://raw.githubusercontent.com/pineaplecodes/dataset/main/sellers_dataset.csv')
df_products = pd.read_csv('https://raw.githubusercontent.com/pineaplecodes/dataset/main/products_dataset.csv')
df_payments = pd.read_csv('https://raw.githubusercontent.com/pineaplecodes/dataset/main/order_payments_dataset.csv')

# Top 10 cities
city_sellers_count = df_sellers.groupby(['seller_state', 'seller_city']).size().reset_index(name='Total_Seller')
city_sellers_count_sorted = city_sellers_count.sort_values(by='Total_Seller', ascending=False)

# Top product categories
total_product_category = df_products['product_category_name'].value_counts()

# Layout in 2 rows with 2 columns each
col1, col2 = st.columns(2)

# First row (2 visualizations)
with col1:
    show_bar_chart(city_sellers_count_sorted)
    
with col2:
    show_category_bar_chart(total_product_category)

# Second row (2 visualizations)
col3, col4 = st.columns(2)

with col3:
    show_payment_chart(df_payments)

with col4:
    show_transaction_binning_chart(df_payments)
