import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import re
import base64

#print(os.getcwd())

# #Time series line chart of actual demand vs. predicted demand
# df = pd.read_csv("y_test_predicted_x_actual.csv")
# df = df.rename(columns={'utc_datetime':'index'}).set_index('index')
# #print(df.dtypes)
# st.line_chart(df)
#
# # Drop down date selector
# # date = st.sidebar.date_input('Date', datetime(2019,1,1))
# # print(date)
#
# st.title("Date range")

# min_date = datetime.datetime(2019,1,1)
# max_date = datetime.datetime(2021,12,31)

# a_date = st.date_input("Pick a date", min_value=min_date, max_value=max_date)
# print(a_date)
# #print(a_date.dtype)
# ##this uses streamlit 'magic'!!!!
# "The date selected:", a_date
#
#
#
# # Reset index to make utc_datetime a column
# df = df.reset_index()
# df.columns = ['date', 'Predicted_Demand', 'Actual_Demand']
# df['date'] = pd.to_datetime(df['date'])
#print(df.head())
#
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

# col1, col2, col3 = st.columns(3)
# col1.metric(label = "Predicted Demand", value = 2218.22412957154, delta = 100)
# col2.metric(label = "Actual Demand", value = 1923.45833333333, delta = 50)



# # Display dataframe on website via st.dataframe or st.write methods
# st.write("==  scrollable dataframe after the end user has uploaded her time series file:")
# st.dataframe(df.style.highlight_max(axis=0))
#
# # %%
# # plot the time series
# fig = px.line(df, x="date", y=["Predicted_Demand", "Actual_Demand"],
#     title="chart: Predicted vs. Actual Energy Demand Tampa", width=1000)
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# st.plotly_chart(fig, use_container_width=False)

st.markdown('---')
st.header('Florida Energy Demand')
# view neighborhood, city by income, different groups, stats

# reading in the polygon shapefile
florida_zips = gpd.read_file(r"data/florida-zip-code-areas.shp")
st.write(florida_zips.head())
x_map= 27.6648 # florida_zips.centroid.x.mean()
y_map= -81.5158  # florida_zips.centroid.y.mean()-.02

mymap = folium.Map(location=[x_map, y_map], zoom_start=7,tiles=None)
folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
#folium_static(mymap)

# area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
area_stats = pd.read_csv('florida_weather_w_zip_codes_2019_01_02.csv', dtype={'zipcode':str})
#area_stats.rename({'zipcode':'zip_code'}, inplace = True)
florida_zips_merged = pd.merge(florida_zips, area_stats, how='left', left_on='ZIPCODE', right_on = 'zipcode')

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
 columns=['ZIPCODE','pred_demand_mwh'],
 #key_on="feature.properties.zip",
#  fill_color='YlGnBu',
    line_weight=1,
 legend_name=f'Lala population in %',
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


