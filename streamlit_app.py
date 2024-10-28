# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session


# Write directly to the app
st.title("Customise your smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be: ", name_on_order)



cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_lst = st.multiselect('Choose upto 5 ingredients: ', my_dataframe, max_selections = 5)

if ingredients_lst:
    ingredients_string = ''

    for fruit_chosen in ingredients_lst:
        ingredients_string += fruit_chosen + ' '


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
