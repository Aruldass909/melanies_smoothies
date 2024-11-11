# Import python packages
from snowflake.snowpark.functions import col
import streamlit as st

st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your customer smoothie
    """
)


title = st.text_input('Name on your Smoothie', 'Life of Brian')
st.write('TThe name on your smoothie will be', title)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'  
  , my_dataframe
  , max_selections=5
)

if ingredients_list:
    st.write(ingredients_list) 
    st.text(ingredients_list) 

ingredients_string =''
name_on_order = title
for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen


my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""


time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
  
    st.success('Your Smoothie is ordered!',icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())

fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=true)
