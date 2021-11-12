import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

st.markdown('---')
st.header("Modeling Energy Demand")

st.text("Our initial model is a linear regression that uses weather data (Temperature," "\n" 
        "Pressure, DHI, DNI, Surface Albedo, Wind Speed, Relative Humidity, and Dew Point)" "\n"
        "from the National Solar Radiation Database (https://maps.nrel.gov/nsrdb-viewer/)" "\n"
        "to predict the daily energy demand for the Tampa area. We used energy demand data" "\n"
        "from Tampa Electric Co. by mining the data sets from the PUDL project" "\n"
        "(https://catalyst.coop/pudl/).")


#Time series line chart of actual demand vs. predicted demand
df = pd.read_csv("../y_test_predicted_x_actual.csv")
df = df.rename(columns={'utc_datetime':'date'})
df = df[['date','lr_pred_demand_mwh','demand_mwh']]

# # Reset index to make utc_datetime a column
df.columns = ['date', 'Predicted_Demand', 'Actual_Demand']
df['date'] = pd.to_datetime(df['date'])


# plot the time series
fig = px.line(df, x="date", y=["Predicted_Demand", "Actual_Demand"],
    title="Predicted vs. Actual Energy Demand Tampa based on a linear regression model", width=1000)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
st.plotly_chart(fig, use_container_width=False)

#Drop down date selector
# date = st.sidebar.date_input('Date', datetime(2019,1,1))
# # print(date)

st.header("Date range")

min_date = datetime.datetime(2019,1,1)
max_date = datetime.datetime(2021,12,31)

a_date = st.date_input("Pick a date", min_value=min_date, max_value=max_date)
print(a_date)
#print(a_date.dtype)
##this uses streamlit 'magic'!!!!
"The date selected:", a_date



# #greater than the start date and smaller than the end date
# df['date'] = pd.to_datetime(df['date'])
# print(df.dtypes)
# mask = (df['date'] == a_date)
# df_masked = df.loc[mask]
# #print(df_masked.dtypes)

# start_date, end_date = st.date_input('Choisir date de début, date de fin :', [])
# if start_date < end_date:
#     pass
# else:
#     st.error('Error: Date de fin doit être choisi après la dete de début.')
#
# #greater than the start date and smaller than the end date
# mask = (df['date'] > start_date) & (df['date'] <= end_date)
# df_masked = df.loc[mask]
# # And display the result!
# st.dataframe(df_masked)


# find_pred_value = df.loc[df.date == a_date]['Predicted_Demand']
# find_pred_value = pd.to_numeric(find_pred_value, errors='coerce')
# st.write(find_pred_value)
# #find_pred_delta = df['Predicted_Demand'].loc[df.index == date-timedelta(days=1)] - df['Predicted_Demand'].loc[df.index == date]
# find_actual_value = df.loc[df.date == a_date]['Actual_Demand']
# find_actual_value = pd.to_numeric(find_actual_value, errors='coerce')
# st.write(find_actual_value)
#find_actual_delta = df['Actual_Demand'].loc[df.index == date-timedelta(days=1)] - df['Actual_Demand'].loc[df.index == date]

#Shows predicted and actual demand by date

# col1, col2 = st.columns(2)
# col1.metric(label = "Predicted Demand", value = find_pred_value, delta = 100)
# col2.metric(label = "Actual Demand", value = find_actual_value, delta = 50)

col1, col2, col3 = st.columns(3)
col1.metric(label = "Predicted Demand", value = 2218.22412957154, delta = 100)
#col2.metric(label = "Actual Demand", value = 1923.45833333333, delta = 50)