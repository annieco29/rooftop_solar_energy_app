import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import plotly.express as px

def app():
    #title
    st.markdown('---')
    st.title("Predicting Florida's Solar Energy Potential")

    #Drop down date selector
    selected_date = st.sidebar.date_input('Date', datetime.datetime(2019,1,2))
    selected_date= selected_date.strftime('%m/%d/%y')

    min_date = st.sidebar.date_input('Min Date', datetime.datetime(2019,1,2))
    min_date= min_date.strftime('%m/%d/%y')
    max_date = st.sidebar.date_input('Max Date', datetime.datetime(2019,12,31))
    max_date= max_date.strftime('%m/%d/%y')

    st.markdown("""
    * Policy makers need to know how solar energy sources can supplement the power grid.
    * The map below shows the percentage of energy demand that could be covered by solar energy.
    * The forecast uses predictive modeling to predict the rooftop solar energy potential and the energy demand based on the weather.
    """)

    # area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
    area_stats = pd.read_csv('apps/florida_weather_w_predictions_and_zip_codes.csv', dtype={'zipcode':str})
    #st.write(area_stats.head())

    # create a dataframe that gets masked based on a daily date selector
    area_stats['date_time'] = pd.to_datetime(area_stats['date_time'])
    #print(area_stats.dtypes)
    daily_mask = (area_stats['date_time'] == selected_date)
    df_daily_masked = area_stats.loc[daily_mask]
    df_daily_masked['date_time'] = df_daily_masked['date_time'].dt.strftime('%m/%d/%Y')
    df_daily_masked = df_daily_masked.reset_index()
    #st.write('df_daily_masked shape = ')
    #st.write(df_daily_masked.shape)

    # create a dataframe that gets masked based on min and max date selectors
    area_stats['date_time'] = pd.to_datetime(area_stats['date_time'])
    #print(area_stats.dtypes)
    daily_mask = ((area_stats['date_time'] >= min_date) & (area_stats['date_time'] <= max_date))
    df_masked = area_stats.loc[daily_mask]
    change_details = df_masked[['date_time','zipcode','real_pred_demand_mwh','percentage_demand_covered']].copy()
    change_details['date_time'] = change_details['date_time'].dt.strftime('%m/%d/%Y')
    #st.write('df_masked shape = ')
    #st.write(change_details.shape)

    # get
    predicted_demand = change_details['real_pred_demand_mwh'].sum()
    #predicted_solar = df_masked['solar_pred_mwh'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Predicted Demand", value=predicted_demand, delta=100)
    col2.metric(label = "Solar Rooftop Potential", value = 1923.45833333333, delta = 50)

    # # Display dataframe on website via st.dataframe or st.write methods
    # st.write("==  scrollable dataframe after the end user has uploaded her time series file:")
    # st.dataframe(df.style.highlight_max(axis=0))

    st.markdown('---')
    st.header('Florida Energy Demand by County Seat')
    # view neighborhood, city by income, different groups, stats

    # reading in the polygon shapefile
    florida_zips = gpd.read_file(r"data/florida-zip-code-areas.shp")
    #st.write(florida_zips['ZIPCODE'].head())
    #st.write(change_details['zipcode'].head())
    x_map= 27.6648 # florida_zips.centroid.x.mean()
    y_map= -81.5158  # florida_zips.centroid.y.mean()-.02

    mymap = folium.Map(location=[x_map, y_map], zoom_start=7,tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
    #folium_static(mymap)

    #st.write(change_details.str[:2])
    df_daily_masked['zipcode'] = df_daily_masked['zipcode'].str[:5]
    #st.write(change_details['zipcode'].head())
    # change_details.rename(columns = {'zipcode':'zip_code'}, inplace= True)
    florida_zips_merged = pd.merge(florida_zips, df_daily_masked, left_on='ZIPCODE', right_on='zipcode')

    #st.subheader(f'{demo} population in %')

    #view_students = st.checkbox('View Student Locations')

    choropleth = folium.Choropleth(
     geo_data=florida_zips_merged,
     name='Choropleth',
     data=florida_zips_merged,
     columns=['ZIPCODE','percentage_demand_covered'],
     key_on="feature.properties.ZIPCODE",
        fill_color='YlGnBu',
        line_weight=1,
     legend_name=f'Percentage Energy Demand Covered by Solar',
     smooth_factor=0
    ).add_to(mymap)

    # # add point for RPMS
    # cluster = MarkerCluster().add_to(mymap)
    # style_function = "font-size: 15px; font-weight: bold"
    # folium.Marker(location=[41.980250,-87.675000], tooltip = "<h3>RPMS</h3>", popup = 'RPMS', style=style_function).add_to(cluster)
    #
    # # add points for student locations
    # if view_students:
    #     student_locations = pd.read_csv('data/student_locations.csv')
    #     locationlist = student_locations.values.tolist()
    #     marker_cluster = MarkerCluster().add_to(mymap)
    #     for point in range(0, len(locationlist)):
    #         folium.Marker(locationlist[point]).add_to(marker_cluster)
    #
    # # add labels indicating the name of the community
    # style_function = "font-size: 15px; font-weight: bold"
    # choropleth.geojson.add_child(
    #     folium.features.GeoJsonTooltip(['zip'], style=style_function, labels=False))

    # create a layer control
    folium.LayerControl().add_to(mymap)

    folium_static(mymap, width=750, height=850)


    st.write(area_stats['real_pred_demand_mwh'].dtype)
    fig = px.sunburst(area_stats, path=['date_time'], values='real_pred_demand_mwh',
                      color='real_pred_demand_mwh',
                      color_continuous_scale='RdBu')
    fig.update_layout(title='Click various months to view power demand')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)



