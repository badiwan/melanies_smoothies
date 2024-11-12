# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """ Chooes the fruit you want in your custom Smoothie
    """
)


name_on_order = st.text_input('Name on smoothie')
st.write(f"The name on the smoothie will be:", name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
)

if ingredients_list:
    st.write(ingredients_list)
    ingredients_str = ""
    for ing in ingredients_list: 
        ingredients_str+=f"{ing} "
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == ing, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {ing} is {search_on}.')
        st.subheader(f"{ing} Nutrition Information")
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        fv_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

    insert_statement = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_str + """','"""+name_on_order+"""')"""
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(insert_statement).collect()
        st.write(insert_statement)
        st.success(f'Your smoothie is ordered, {name_on_order}', icon="✅")


