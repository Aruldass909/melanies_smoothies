# Import python packages
from snowflake.snowpark.functions import col
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your customer smoothie
    """
)


title = st.text_input('Name on your Smoothie', 'Life of Brian')
st.write('TThe name on your smoothie will be', title)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

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

#st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

#st.write(my_insert_stmt)
#st.stop
time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    
#if ingredients_string:
#    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!',icon="✅")