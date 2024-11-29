# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col 
# Write directly to the app
st.title(":cup_with_straw: CUSTOMIZE YOUR SMOOTHIE :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie
    """
)


name_an_order = st.text_input("Name of Smoothie:")
st.write("The name on your smoothie will be: ", name_an_order)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    ,max_selections= 5
   
)

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_an_order)
            values ('""" + ingredients_string + """','"""+ name_an_order+"""')"""

    #st.write(my_insert_stmt)
    
    
    time_to_insert= st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+ name_an_order, icon="✅")

