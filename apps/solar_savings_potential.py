import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import base64
import calendar

def app():
    LOGO_IMAGE_IBM = "apps/ibm.png"
    LOGO_IMAGE_U_OF_F = "apps/u_of_f.svg.png"

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
            float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE_IBM, "rb").read()).decode()}" width="150" height="40">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE_U_OF_F, "rb").read()).decode()}" width="200" height="40">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('---')
    st.header("Modeling Energy Demand")

    min_date = st.sidebar.date_input('Min Date', datetime.datetime(2019, 1, 1))
    min_date = min_date.strftime('%m/%d/%y')
    max_date = st.sidebar.date_input('Max Date', datetime.datetime(2019, 12, 31))
    max_date = max_date.strftime('%m/%d/%y')

    # add_selectbox = st.sidebar.selectbox(
    #     "Search zipcode:",
    #     ("Email", "Home phone", "Mobile phone")
    #         )

    st.markdown("""
    * Renewables currently account for roughly only 4% of energy production in Florida.
    * Policy makers need to know how solar energy sources can supplement the power grid.
    * The map below shows the percentage of energy demand that could be covered by solar energy.
    * The forecast uses predictive modeling to predict the rooftop solar energy potential and the energy demand based on the weather.
    """)

    # area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
    area_stats = pd.read_csv('apps/florida_weather_w_predictions_and_zip_codes.csv', dtype={'zipcode':str})
    #st.write(area_stats.head())

    # create a dataframe that gets masked based on min and max date selectors
    area_stats['date_time'] = pd.to_datetime(area_stats['date_time'])
    #print(area_stats.dtypes)
    daily_mask = ((area_stats['date_time'] >= min_date) & (area_stats['date_time'] <= max_date))
    df_masked = area_stats.loc[daily_mask]
    change_details = df_masked[['date_time','zipcode','real_pred_demand_mwh','solar_prod_mwh','percentage_demand_covered']].copy()
    change_details['date_time'] = change_details['date_time'].dt.strftime('%m/%d/%Y')
    #st.write('df_masked shape = ')
    #st.write(change_details.shape)

    # get f'{value:,}'
    predicted_demand = round(change_details['real_pred_demand_mwh'].sum())
    predicted_solar = round(change_details['solar_prod_mwh'].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Predicted Demand (mwh)", value=f'{predicted_demand:,}'
                #, delta=100
                )
    col2.metric(label = "Solar Rooftop Potential (mwh)", value = f'{predicted_solar:,}',
                #delta = 50
                )
    #col3.metric(label = "Cost Savings Potential", value = f'{predicted_solar:,)

    #get name of month for sunburst chart
    area_stats['month'] = area_stats['date_time'].dt.strftime("%B")

    # st.write(area_stats['percentage_demand_covered'].dtype)
    fig = px.sunburst(area_stats, path=['month','date_time'], values= 'percentage_demand_covered',
                      color='percentage_demand_covered',
                      color_continuous_scale='RdBu')
    fig.update_layout(title='Click various months to view power demand')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)