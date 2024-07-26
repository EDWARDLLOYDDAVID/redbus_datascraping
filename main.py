import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Data Filtering")
st.title("Data Filtering Application")


try:
    
    conn = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="7418736408",  
        database="redbus_data"  
    )
    query = "SELECT * FROM bus_routes"  
    data = pd.read_sql(query, conn)
    conn.close()
    st.write("Data successfully loaded from the database.")
except Exception as e:
    st.write(f"Error connecting to the database: {e}")


if 'data' not in locals():
    st.write("No data loaded. Please check the database connection.")
else:
    
    data['price'] = pd.to_numeric(data['price'], errors='coerce').fillna(0)
    data['star_rating'] = pd.to_numeric(data['star_rating'], errors='coerce').fillna(0)

   
    st.sidebar.title("Filters")

    
    route_name = st.sidebar.selectbox("Select Route", options=data['route_name'].unique())

   
    price_min, price_max = st.sidebar.slider("Select Price Range", 
                                             min_value=int(data['price'].min()), 
                                             max_value=int(data['price'].max()), 
                                             value=(int(data['price'].min()), int(data['price'].max())))

    star_rating_min = st.sidebar.number_input("Minimum Star Rating", 
                                              min_value=0.0, 
                                              max_value=5.0, 
                                              value=0.0, 
                                              step=0.5)

    star_rating_max = st.sidebar.number_input("Maximum Star Rating", 
                                              min_value=0.0, 
                                              max_value=5.0, 
                                              value=5.0, 
                                              step=0.5)

    
    filtered_data = data[
        (data['route_name'] == route_name) &
        (data['price'] >= price_min) & (data['price'] <= price_max) &
        (data['star_rating'] >= star_rating_min) & (data['star_rating'] <= star_rating_max)
    ]

    
    st.write("Filtered Data", filtered_data)

    
