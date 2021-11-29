import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import base64


def app():
    LOGO_IMAGE_IBM = "apps/ibm.png"
    LOGO_IMAGE_U_OF_F = "apps/u_of_f.svg.png"
    LOGO_IMAGE_BRIGHTER = "apps/brighter_potential_logo.png"

    st.markdown(
        """
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-weight:700 !important;
            font-size:50px !important;
            color: #f9a01b !important;
            padding-top: 75px !important;
        }
        .logo-img {
            float: left;
            position: relative;
            margin-top: 600px;
        }
        #logo {
        position: absolute;
           float: right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""

                <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE_IBM, "rb").read()).decode()}" width="100x`" height="40" style="border:20px;margin:0px" />
                <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE_U_OF_F, "rb").read()).decode()}" width="200" height="40" style="border:20px;margin:0px"/>
                &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;
                &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;

                <img class="logo" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE_BRIGHTER, "rb").read()).decode()}" width="100" height="100" />


            """,
        unsafe_allow_html=True
    )
    st.markdown('---')
    st.header("Predictive Modeling Methodology")

    st.markdown("""
            "Our XGBoost model that predicts energy demand for all of Florida uses weather data (temperature, 
            pressure, DHI, DNI, surface albedo, wind speed, relative humidity, and dew point)
            from the National Solar Radiation Database to predict the daily energy demand for the
            Tampa area. We used energy demand data from Tampa Electric Co. as a target output for the model
            from the PUDL project.
            """)


    #Time series line chart of actual demand vs. predicted demand
    df = pd.read_csv("y_test_predicted_x_actual.csv")
    df = df.rename(columns={'utc_datetime':'date'})
    df = df[['date','lr_pred_demand_mwh','demand_mwh']]

    # # Reset index to make utc_datetime a column
    df.columns = ['date', 'Predicted_Demand', 'Actual_Demand']
    df['date'] = pd.to_datetime(df['date'])


    # plot the time series
    fig = px.line(df, x="date", y=["Predicted_Demand", "Actual_Demand"],
        title="Predicted vs. actual energy demand based on xgboost model", width=750)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    st.plotly_chart(fig, use_container_width=False)

    st.markdown("""
            Our linear regression model that predicts solar rooftop potential for Florida uses weather data (temperature, 
            pressure, DHI, DNI, surface albedo, wind speed, relative humidity, and dew point)
            from the National Solar Radiation Database to predict the daily rooftop solar potential. The model
            predicts solar production for a 250 mwh capacity solar panel.
            """)
    #Time series line chart of actual solar production vs. predicted solar production
    df_solar = pd.read_csv("solar_predictions.csv")
    #df = df.rename(columns={'utc_datetime':'date'})
    df_solar = df_solar[['date','Predicted_Output','Solar_Output_by_Panel']]

    # # Reset index to make utc_datetime a column
    df_solar.columns = ['date', 'Predicted Output', 'Actual Output by Panel']
    df_solar['date'] = pd.to_datetime(df_solar['date'])


    # plot the time series
    fig_1 = px.line(df_solar, x="date", y=["Predicted Output", "Actual Output by Panel"],
        title="Predicted vs. Actual solar energy output by panel based on a linear regression model", width=750)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    st.plotly_chart(fig_1, use_container_width=False)
