import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import plotly.express as px
import base64
from folium.plugins import MarkerCluster
import branca

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

    #title
    st.markdown('---')
    st.title("Predicting Florida's Rooftop Solar Energy Potential")

    st.sidebar.header('Choose month to view:')
    # Declare zipcode list
    month = ['January','February','March','April','May','June','July',
             'August','September','October','November','December']

    # Put client and date options in the sidebar
    selected_month = st.sidebar.selectbox(
        'Choose month:',
        month,
        key='month'
    )

    st.markdown("""
    * Renewables currently account for roughly only 4% of energy production in Florida.
    * Stakeholders need to know how solar energy sources can supplement the power grid.
    * The map below shows the percentage of energy demand that could have been produced by rooftop solar energy.
    * This projection for 2019 is based on predictive modeling that predicts the rooftop solar energy potential and the energy demand based on the weather.
    """)

    # area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
    area_stats = pd.read_csv('apps/florida_weather_w_predictions_and_zip_codes.csv', dtype={'zipcode':str})
    #st.write(area_stats.head())

    #get name of month for sunburst chart
    area_stats['date_time'] = pd.to_datetime(area_stats['date_time'])
    area_stats['month'] = area_stats['date_time'].dt.strftime("%B")
    area_stats_sub = area_stats[['zipcode','month','solar_prod_mwh','real_pred_demand_mwh','percentage_demand_covered']]
    df_groupby_month = area_stats_sub.groupby(['zipcode','month']).mean()
    df_groupby_month = df_groupby_month.reset_index()

    # create a dataframe that gets masked based on a daily date selector
    #print(area_stats.dtypes)
    monthly_mask = (df_groupby_month['month'] == selected_month)
    df_monthly_masked = df_groupby_month.loc[monthly_mask]
    # st.write('df_monthly_masked shape = ')
    # st.write(df_monthly_masked.shape)

    # # Display dataframe on website via st.dataframe or st.write methods
    # st.write("==  scrollable dataframe after the end user has uploaded her time series file:")
    # st.dataframe(df.style.highlight_max(axis=0))

    st.markdown('---')
    st.header('Florida Rooftop Solar Potential by County Seat')
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
    df_monthly_masked['zipcode'] = df_monthly_masked['zipcode'].str[:5]
    #st.write(change_details['zipcode'].head())
    # change_details.rename(columns = {'zipcode':'zip_code'}, inplace= True)
    florida_zips_merged = pd.merge(florida_zips, df_monthly_masked, left_on='ZIPCODE', right_on='zipcode')
    florida_zips_merged['percentage_demand_covered'] = florida_zips_merged['percentage_demand_covered'] * 100

    #st.subheader(f'{demo} population in %')

    view_real_estate = st.checkbox('View Industrial Locations')

    choropleth = folium.Choropleth(
     geo_data=florida_zips_merged,
     name='Choropleth',
     data=florida_zips_merged,
     columns=['ZIPCODE','percentage_demand_covered'],
     key_on="feature.properties.ZIPCODE",
        fill_color='Blues',
        line_weight=1,
     legend_name=f'Percentage Energy Demand Covered by Solar',
     smooth_factor=0
    ).add_to(mymap)

    # add points for industrial real estate sites greater than 750,000 sqft
    cluster = MarkerCluster().add_to(mymap)
    style_function = "font-size: 15px; font-weight: bold"
    #folium.Marker(location=[41.980250,-87.675000], tooltip = "<h3>RPMS</h3>", popup = 'RPMS', style=style_function).add_to(cluster)

    # add points for student locations
    if view_real_estate:
        industrial_locations = pd.read_csv('apps/florida_industrial_lat_long.csv')

        #industrial_owners = pd.read_csv('apps/industrial_solar.csv')
        lat = industrial_locations['lat'].tolist()
        lon = industrial_locations['long'].tolist()
        name = industrial_locations['reported_owner'].tolist()
        pred = industrial_locations['solar_prod_mw'].tolist()

        #st.write(industrial_locations.columns)

        for lt,ln,nm,pr in zip(lat,lon,name,pred):
            test = folium.Html(f'<b>Owner: {nm}<br>Daily Solar Production: {pr}</b>', script=True)  # i'm assuming this bit runs fine
            iframe = branca.element.IFrame(html=test, width=200, height=90)
            popup = folium.Popup(iframe, parse_html=True)
            folium.Marker(location=[lt, ln], radius=6, color='grey', fill_color='yellow', popup=popup).add_to(mymap)

    # add labels indicating the name of the community
    style_function = "font-size: 15px; font-weight: bold"
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['zipcode'], style=style_function, labels=False))

    # create a layer control
    folium.LayerControl().add_to(mymap)

    folium_static(mymap, width=750, height=850)



