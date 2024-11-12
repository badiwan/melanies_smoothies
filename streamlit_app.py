# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """ Chooes the fruit you want in your custom Smoothie
    """
)


name_on_order = st.text_input('Name on smoothie')
st.write(f"The name on the smoothie will be:", name_on_order)

session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selection=5
)

if ingredients_list:
    st.write(ingredients_list)
    ingredients_str = ""
    for ing in ingredients_list: ingredients_str+=f"{ing} "
    st.write(ingredients_str)
    insert_statement = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_str + """','"""+name_on_order+"""')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(insert_statement).collect()
        st.write(insert_statement)
        st.success(f'Your smoothie is ordered, {name_on_order}', icon="✅")
