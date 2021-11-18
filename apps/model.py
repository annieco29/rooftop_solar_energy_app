import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

def app():
        st.markdown('---')
        st.header("Modeling Energy Demand")

        st.text("Our XGBoost model that predicts energy demand for all of Florida uses weather data (temperature," "\n" 
                "pressure, DHI, DNI, surface albedo, wind speed, relative humidity, and dew point)" "\n"
                "from the National Solar Radiation Database to predict the daily energy demand for the" "\n"
                "Tampa area. We used energy demand data from Tampa Electric Co. as a target output for the model" "\n"
                "from the PUDL project."
                )


        #Time series line chart of actual demand vs. predicted demand
        df = pd.read_csv("y_test_predicted_x_actual.csv")
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

