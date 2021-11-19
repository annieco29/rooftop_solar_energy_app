import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import re
import base64

def app():
    #title
    st.markdown('---')
    st.title("Predicting Florida's Solar Energy Potential")

    #Drop down date selector
    selected_date = st.sidebar.date_input('Date', datetime.datetime(2019,1,2))
    selected_date= selected_date.strftime('%m/%d/%y')

    st.text("Renewables currently account for roughly 4% of energy production in Florida." "\n"
            "Florida does not produce enough electricity to meet its power needs." "\n"
            "With rapidly shifting weather there is a need to know how solar energy" "\n"
            "sources can supplement the power grid. The map shows a prediction of Florida" "\n"
            "demand by zip codes. Soon to come: overlaying a prediction of" "\n"
            "solar energy production that could offset demand in each zip code." )

    # # Display dataframe on website via st.dataframe or st.write methods
    # st.write("==  scrollable dataframe after the end user has uploaded her time series file:")
    # st.dataframe(df.style.highlight_max(axis=0))

    st.markdown('---')
    st.header('Florida Energy Demand by County Seat')
    # view neighborhood, city by income, different groups, stats

    # reading in the polygon shapefile
    florida_zips = gpd.read_file(r"data/florida-zip-code-areas.shp")
    #st.write(florida_zips.head())
    x_map= 27.6648 # florida_zips.centroid.x.mean()
    y_map= -81.5158  # florida_zips.centroid.y.mean()-.02

    mymap = folium.Map(location=[x_map, y_map], zoom_start=7,tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
    #folium_static(mymap)

    # area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
    area_stats = pd.read_csv('apps/florida_weather_w_zip_codes.csv', dtype={'zipcode':str})

    # greater than the start date and smaller than the end date
    area_stats['date_time'] = pd.to_datetime(area_stats['date_time'])
    #print(area_stats.dtypes)
    mask = (area_stats['date_time'] == selected_date)
    df_masked = area_stats.loc[mask]
    df_masked['date_time'] = df_masked['date_time'].dt.strftime('%m/%d/%Y')

    #area_stats.rename({'zipcode':'zip_code'}, inplace = True)
    florida_zips_merged = pd.merge(florida_zips, df_masked, left_on='ZIPCODE', right_on = 'zipcode')

    # demos = ['White', "Black", "Latino", "Asian"]
    #
    # demo = st.selectbox(
    #    'Select demographic',
    #    demos)

    #st.subheader(f'{demo} population in %')

    #view_students = st.checkbox('View Student Locations')

    choropleth = folium.Choropleth(
     geo_data=florida_zips_merged,
     name='Choropleth',
     data=florida_zips_merged,
     columns=['ZIPCODE','real_pred_demand_mwh'],
     key_on="feature.properties.ZIPCODE",
        fill_color='YlGnBu',
        line_weight=1,
     legend_name=f'Energy Demand by County Seat',
     smooth_factor=0
    ).add_to(mymap)

    # # add point for RPMS
    # cluster = MarkerCluster().add_to(mymap)
    # style_function = "font-size: 15px; font-weight: bold"
    # folium.Marker(location=[41.980250,-87.675000], tooltip = "<h3>RPMS</h3>", popup = 'RPMS', style=style_function).add_to(cluster)

    # # add points for student locations
    # if view_students:
    #     student_locations = pd.read_csv('data/student_locations.csv')
    #     locationlist = student_locations.values.tolist()
    #     marker_cluster = MarkerCluster().add_to(mymap)
    #     for point in range(0, len(locationlist)):
    #         folium.Marker(locationlist[point]).add_to(marker_cluster)

    # # add labels indicating the name of the community
    # style_function = "font-size: 15px; font-weight: bold"
    # choropleth.geojson.add_child(
    #     folium.features.GeoJsonTooltip(['zip'], style=style_function, labels=False))

    # create a layer control
    folium.LayerControl().add_to(mymap)

    folium_static(mymap, width=750, height=850)

    # Shows predicted and actual demand by date

    # col1, col2 = st.columns(2)
    # col1.metric(label = "Predicted Demand", value = find_pred_value, delta = 100)
    # col2.metric(label = "Actual Demand", value = find_actual_value, delta = 50)

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Predicted Demand", value=2218.22412957154, delta=100)
    # col2.metric(label = "Actual Demand", value = 1923.45833333333, delta = 50)



