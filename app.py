import streamlit as st 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import altair as alt 
from urllib.error import URLError

# load the data 
@st.cache_data
def get_data():
    path_ = "bike_sales.xlsx"
    df = pd.read_excel(path_)
    # transformations 
    df.Gender = df.Gender.str.replace('M','male').str.replace('F','female')
    df['Marital Status'] = df['Marital Status'].str.replace('M','married').str.replace('S','single') 
    # add age groups 
    bins = [24,40,55,70,90]
    labels = ['adult','middle aged','aged','old']
    df["Age_grp"] = pd.cut(df.Age, bins=bins, labels=labels)
    return df

# title
st.title("Bakery Sales Report")

try:
    df = get_data()
    st.subheader("Data Preview")
    st.dataframe(df.tail(5))
    # st.dataframe(df.sample(10))

    # filter 
    # st.write("Select a Gender")
    gender = df.Gender.unique()
    selected_gender = st.multiselect('Select a Gender',gender,[gender[0], gender[1]])

    # show a table based on the selection 
    temp_table = df[df['Gender'].isin(selected_gender)]
    if not selected_gender:
        st.error("Please select a gender")
    else:
        st.dataframe(temp_table.sample(5))

    # Q1
    st.subheader("Distribution of Bikes Purchased")
    purchased_a_bike = df[df['Purchased Bike'] == 'Yes']
    details = purchased_a_bike.Gender.value_counts()

    # percentage distributions 
    tt = df.Gender.value_counts().to_frame().reset_index()
    tp = purchased_a_bike.Gender.value_counts().to_frame().reset_index()
    total_no_males = tt.iloc[0,1]
    total_no_females = tt.iloc[1,1]
    no_males_purch = tp.iloc[0,1]
    no_females_purch = tp.iloc[1,1]
    
    # card 
    col1, col2 = st.columns(2)
    col1.metric("% Males", np.round((no_males_purch/total_no_males)*100,2))
    col2.metric("% Females", np.round((no_females_purch/total_no_females)*100,2))

    # st.write(details)
    bar1 = purchased_a_bike.Gender.value_counts().plot(kind='barh')
    st.pyplot(bar1.figure)

    # regions
    regions_=purchased_a_bike.Region.value_counts().to_frame().reset_index()
    st.subheader("Distribution of Bikes Purchased by Regions")
    st.dataframe(regions_)
    df2=regions_.groupby('Region')['count'].sum().sort_values(ascending=True)
    st.bar_chart(df2)

    # Age distribution
    df3 = purchased_a_bike.Age_grp.value_counts().to_frame().reset_index()
    st.subheader("Bikes purchased by Age groups")
    grps = purchased_a_bike.Age_grp.value_counts()

    # table
    st.dataframe(grps)

    # pie chart 

    fig10, ax10 = plt.subplots(figsize=(5,5))
    explode = (0.1,0.2,0.1,0.2)
    ax10.pie(grps, labels=grps.index,autopct="%1.1f%%", 
             explode=explode)
    ax10.axis("equal")
    st.pyplot(fig10)

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )