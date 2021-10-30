import streamlit as st
import pandas as pd
#import os

#print(os.getcwd())

df = pd.read_csv("y_test_predicted_x_actual.csv")

df = df.rename(columns={'utc_datetime':'index'}).set_index('index')

st.line_chart(df)