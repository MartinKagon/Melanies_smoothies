# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customise your smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()


#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width = True)
#st.stop()

ingredients_lst = st.multiselect('Choose up to 5 ingredients:', my_dataframe[['fruit_name']], max_selections =5)

if ingredients_lst:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_lst:
        ingredients_string += fruit_chosen + ' ' 
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Informaton')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon" +fruit_chosen)
        fv_dc = st.dataframe(data=fruityvice_response.json(), use_container_width=True) 
    
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

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#fv_dc = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
