import streamlit as st
from multiapp import MultiApp
from apps import st_mapLayers, model # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Solar Potential Map", st_mapLayers.app)
app.add_app("Predictive Model", model.app)

# The main app
app.run()