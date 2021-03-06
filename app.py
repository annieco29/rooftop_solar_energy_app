import streamlit as st
from multiapp import MultiApp
from apps import st_mapLayers, model, solar_savings_potential  # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Rooftop Solar Energy Map", st_mapLayers.app)
app.add_app("Solar Savings Potential", solar_savings_potential.app)
app.add_app("Predictive Model Methodology", model.app)

# The main app
app.run()