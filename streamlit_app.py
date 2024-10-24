# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customise your smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be: ", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")

ingredients_lst = st.multiselect('Choose up to 5 ingredients:', my_dataframe[['fruit_name']], max_selections =5)

if ingredients_lst:
    ingredients_string = ', '.join(ingredients_lst)  # Change to join by comma

    # Adjust the insert statement to specify the columns
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (name_on_order, ingredients)
        VALUES ('{name_on_order}', '{ingredients_string}')
    """
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.write("Please select at least one ingredient.")
