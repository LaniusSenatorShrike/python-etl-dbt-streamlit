import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st
from constants import C


# Function to connect to PostgreSQL
def get_connection():
    conn = psycopg2.connect(host=C.HOST, database=C.DBNAME, user=C.USER, password=C.PASSWORD)
    return conn


# Function to fetch data from PostgreSQL
def fetch_data(query):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error: {str(e)}")
    finally:
        conn.close()


# Streamlit app UI
st.title(":rainbow[Stream Pulse]")
st.subheader(":blue[*A Business Analytics App*]")
# vertical space
st.markdown("<br><br>", unsafe_allow_html=True)


# Define the query you want to run
product_cat_highest_sales_query = """ SELECT * FROM public.agg_product_cat_highest_sales"""
avg_user_trans_query = """ SELECT * FROM public.agg_avg_user_trans"""
agg_monthly_rev_growth_query = """ SELECT * FROM public.agg_monthly_rev_growth"""

# Fetching data
product_cat_highest_sales = fetch_data(product_cat_highest_sales_query)
avg_user_trans = fetch_data(avg_user_trans_query)
agg_monthly_rev_growth = fetch_data(agg_monthly_rev_growth_query)


if product_cat_highest_sales is not None:
    product_cat_highest_sales = product_cat_highest_sales["product"][0]
else:
    st.write("No data found or error in the query.")
    product_metric = "N/A"

st.metric(label=":blue[Top Product Category]", value=product_cat_highest_sales)

# vertical space
st.markdown("<br><br>", unsafe_allow_html=True)

# Create two equal columns for the charts
col1, col2 = st.columns(2)

# Display Bar Chart for Average User Transaction Amount for Last 6 Months in the first column
with col1:
    if avg_user_trans is not None and not avg_user_trans.empty:
        st.write(":blue[Average User Transaction Amount]")
        # Create bar chart using Plotly
        fig1 = px.bar(
            avg_user_trans,
            x="month",
            y="avg_transaction_amount",
            labels={"transaction_month": "Month", "avg_transaction_amount": "Average Transaction Amount"},
        )
        fig1.update_layout(height=315)
        # Display chart in the first column
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.write("No data found for Average User Transaction Amount.")

# Display Line Chart for Monthly Revenue Growth for the Last 6 Months in the second column
with col2:
    if agg_monthly_rev_growth is not None and not agg_monthly_rev_growth.empty:
        st.write(":blue[Monthly Revenue Growth]")
        fig2 = px.line(
            agg_monthly_rev_growth,
            x="month",
            y="revenue_growth_percent",  # Changed to a more descriptive y-axis label
            labels={"month": "Month", "revenue_growth_percent": "Revenue Growth (%)"},
        )
        fig2.update_layout(height=315)

        # Display chart in the second column
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.write("No data found for Monthly Revenue Growth.")
