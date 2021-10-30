import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

#print(os.getcwd())

#Time series line chart of actual demand vs. predicted demand
df = pd.read_csv("y_test_predicted_x_actual.csv")
df = df.rename(columns={'utc_datetime':'index'}).set_index('index')
st.line_chart(df)

# Drop down date selector
date = st.sidebar.date_input('Date', datetime(2019,1,1))
print(date)
# st.write(date)
# end_date = st.date_input('End date', tomorrow)
# if start_date < end_date:
#     st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
# else:
#     st.error('Error: End date must fall after start date.')
df = df.reset_index()
print(df.head())
find_pred_value = df['lr_pred_demand_mwh'].loc[df.lr_pred_demand_mwh == 2218.22412957154]
print(find_pred_value)
#find_pred_delta = df['lr_pred_demand_mwh'].loc[df.index == date-timedelta(days=1)] - df['lr_pred_demand_mwh'].loc[df.index == date]
find_actual_value = df['demand_mwh'].loc[df.demand_mwh == 1923.45833333333]
#find_actual_delta = df['demand_mwh'].loc[df.index == date-timedelta(days=1)] - df['demand_mwh'].loc[df.index == date]

# Shows predicted and actual demand by date
col1, col2, col3 = st.columns(3)
col1.metric(label = "Predicted Demand", value = 2218.22412957154, delta = 100)
col2.metric(label = "Actual Demand", value = 1923.45833333333, delta = 50)

