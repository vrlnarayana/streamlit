import streamlit as st

def menu():
    st.write('\n')
    menu_choice = st.sidebar.radio("Main Pages>>>>>", ('Senti-Collections', 'Popular Titles',
                                                       'Content Based Recommendation', 'User Registration', 'User Choices'), index=0,key=1)
    return menu_choice

def submenu_1():
    st.write('\n')
    menu_choice = st.sidebar.radio("Sub Pages>>>>>", ('Most Played', 'Most Rated', 'Similar Taste'),index=0,key=2)
    return menu_choice

