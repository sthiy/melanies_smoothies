# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Super smoothies order form :cup_with_straw:")
st.write(
    """
    Choose your fruits and stuff.
    """
)



name_on_order = st.text_input("Name on smoothie:")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))

ingredients_list = st.multiselect("Choose up to 5 fruits", my_dataframe, max_selections=5)

ingredients_string = ''
my_insert_stmt = ''
if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ' '.join(ingredients_list)
    
    for fruit in ingredients_list:
        st.text(fruit)
        
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit}")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = f"insert into smoothies.public.orders (ingredients, name_on_order) values ('{ingredients_string}', '{name_on_order}')"

st.write(ingredients_string)
st.write(my_insert_stmt)

time_to_insert = st.button("Order")
if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
