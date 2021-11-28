import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import base64

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
    st.header("Solar Rooftop Potential Prediction")

    # Sidebar
    st.sidebar.header('Choose Time Range to View:')
    min_date = st.sidebar.date_input('Min Date', datetime.datetime(2019, 1, 1))
    min_date = min_date.strftime('%m/%d/%y')
    max_date = st.sidebar.date_input('Max Date', datetime.datetime(2019, 12, 31))
    max_date = max_date.strftime('%m/%d/%y')

    st.sidebar.header('Choose Zipcode to View:')
    # Declare zipcode list
    zipcodes = [33040, 33131,34112,33916,33407,33935,33471,33950,
    34266,34994,34972,34236,34950,34205,33873,32960,33830,33606,33755,34741,33525,32806,34601,
    32796,33513,32778,32771,34453,32720,34471,32621,32110,32601,32177,32456,32080,32091,32054,
    32066,32347,32401,32327,
    32025,32064,32063,32202,32502,32503,32424,32321,32304,32340,32344,
    32351,32570,32034,32433,32536,32428,32448,32425,32602,32603,32604,32605,32606,
    32607,32608,32609,32610,32611,32612,32614,32627,32641,32653,32402,32404,32405,32406,
    32412,32073,32081,32099,32201,32203,32204,32205,32206,32207,32208,32209,
    32210,32211,32212,32214,32216,32217,32218,32219,32220,32221,32222,32223,32224,
    32225,32226,32227,32228,32229,32233,32234,32235,32236,32237,32238,32239,
    32241,32244,32245,32246,32247,32250,32254,32255,32256,32257,32258,32266,32277,
    32501,32504,32505,32514,32520,32522,32523,32524,32591,33601,33602,33603,33604,
    33605,33607,33608,33609,33610,33611,33612,33613,33615,33616,33617,33619,
    33620,33621,33622,33623,33629,33630,33631,33633,33634,33637,33646,33647,33650,33655,33660,33661,
    33662,33664,33672,33673,33674,33675,33677,33679,33680,33681,33686,33901,
    33902,33903,33905,33906,33907,33911,33912,33913,33917,33919,33966,33971,33990,32301,32302,32303,32305,32306,
    32307,32308,32309,32310,32311,32312,32313,32314,32316,32317,32395,32399,
    33101,33109,33111,33114,33125,33126,33127,33128,33129,33130,33132,33133,33134,33135,33136,33137,33138,
    33139,33140,33142,33144,33145,33146,33147,33149,33150,33151,33159,33222,33233,33234,
    33238,33242,33245,33255,32789,32801,32802,32803,32804,32805,32807,32808,32809,
    32810,32811,32812,32814,32819,32822,32824,32827,32829,32832,32834,
    32835,32839,32853,32854,32855,32856,32861,32862,32878,32885,32886,
    32891,33401,33402,33403,33405,33409,33411,33412,33417,33756,33757,33758,
    33759,33761,33763,33764,33765,33766,33767,33769]

    # Put client and date options in the sidebar
    selected_zip = st.sidebar.selectbox(
        'Choose Zipcode:',
        zipcodes,
        key='zipcodes'
    )

    st.markdown("""
    * Renewables currently account for roughly only 4% of energy production in Florida.
    * Policy makers need to know how solar energy sources can supplement the power grid.
    * The calendar wheel below shows the daily potential of energy demand that could be covered by rooftop solar energy for 2019.
    * This projection for 2019 is based on predictive modeling that predicts the rooftop solar energy potential and the energy demand based on the weather.
    """)

    # area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
    area_stats = pd.read_csv('apps/florida_weather_w_predictions_and_zip_codes.csv', dtype={'zipcode':str})
    #st.write(area_stats.head())

    # create a dataframe that gets masked based on min and max date selectors
    area_stats['date_time'] = pd.to_datetime(area_stats['date_time'])
    selected_zip = str(selected_zip)
    daily_mask = ((area_stats['date_time'] >= min_date) & (area_stats['date_time'] <= max_date) & (area_stats['zipcode']== selected_zip))
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
    area_stats['word_date'] = area_stats['date_time'].dt.strftime("%B %e, %Y")

    # create a dataframe that gets masked based on zipcode
    selected_zip = str(selected_zip)
    zip_mask = (area_stats['zipcode']== selected_zip)
    df_zip_masked = area_stats.loc[zip_mask]
    change_details_zip = df_zip_masked[['date_time','month','word_date','zipcode','real_pred_demand_mwh','solar_prod_mwh','percentage_demand_covered']].copy()
    #st.write('df_masked shape = ')
    #st.write(change_details.shape)

    #sunburst chart label dictionary
    label_dict = {'Percent Demand Covered': 'percentage_demand_covered','Month': 'month', 'Date':'word_date'}

    # st.write(area_stats['percentage_demand_covered'].dtype)
    fig = px.sunburst(change_details_zip, path=['month','word_date'], values= 'percentage_demand_covered',
                      color='percentage_demand_covered',
                      color_continuous_scale='ylorrd')
    fig.update_layout(coloraxis_colorbar_title='Rooftop Solar Energy Potential')
    fig.update_layout(title='Click various months to view percentage of demand fulfilled by solar potential')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)