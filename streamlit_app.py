st.success('Someone clicked the button', icon = '👍')
# Import python packages
import streamlit as st
streamlit.title('My parents new healthy diner')
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customise your smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be: ", name_on_order)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:

    og_dataset = session.table("Smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)

    try:
        og_dataset.merge(edited_dataset,
                         (og_dataset['order_uid'] == edited_dataset['order_uid']),
                      [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})])
        st.success('Someone clicked the button', icon = '👍')
    except:
        st.write('Something went wrong')

else:
    st.success('There are no pending orders right now' , icon = '👍')


cnx = st.connection("snowflake")
session = cnx.session()


editable_df = st.experimental_data_editor(my_dataframe)
submitted = st.button('Submit')

ingredients_lst = st.multiselect('Choose upto 5 ingredients: ', my_dataframe, max_selections = 5)

if ingredients_lst:
    ingredients_string = ''

    for fruit_chosen in ingredients_lst:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_dv = st.dataframe(data=fruityvice_response.json(), use_container_width = True)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""















#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#fv_dv = st.dataframe(data=fruityvice_response.json(), use_container_width = True)
