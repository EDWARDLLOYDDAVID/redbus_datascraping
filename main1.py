import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="Bus Data Filtering")
st.title("Bus Data Filtering Application")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="7418736408",
        database="redbus_data"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT state FROM bus_routes1")
    states = [row[0] for row in cursor.fetchall()]
    st.write("Data successfully loaded from the database.")
except Exception as e:
    st.write(f"Error connecting to the database: {e}")
    conn = None

if conn:
    st.sidebar.title("Filters")
    selected_state = st.sidebar.selectbox("Select State", options=states)

    if selected_state:
        cursor.execute(f"SELECT DISTINCT route_name FROM bus_routes1 WHERE state = '{selected_state}'")
        routes = [row[0] for row in cursor.fetchall()]

        cursor.execute(f"SELECT MIN(price), MAX(price) FROM bus_routes1 WHERE state = '{selected_state}'")
        price_range = cursor.fetchone()
        cursor.execute(f"SELECT MIN(star_rating), MAX(star_rating) FROM bus_routes1 WHERE state = '{selected_state}'")
        rating_range = cursor.fetchone()

        selected_route = st.sidebar.selectbox("Select Route", options=routes)

        price_min, price_max = st.sidebar.slider("Select Price Range", 
                                                 min_value=int(price_range[0]), 
                                                 max_value=int(price_range[1]), 
                                                 value=(int(price_range[0]), int(price_range[1])))

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

        filter_query = f"""
            SELECT * FROM bus_routes1
            WHERE state = '{selected_state}'
            AND route_name = '{selected_route}'
            AND price BETWEEN {price_min} AND {price_max}
            AND star_rating BETWEEN {star_rating_min} AND {star_rating_max}
        """

        try:
            cursor.execute(filter_query)
            filtered_data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(filtered_data, columns=column_names)
            st.table(df)
        except Exception as e:
            st.write(f"Error executing query: {e}")
        finally:
            cursor.close()
            conn.close()
else:
    st.write("No data loaded. Please check the database connection.")
