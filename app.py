import streamlit as st
from multiapp import MultiApp
from apps import home, inputs, student_summary # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Inputs", inputs.app)
app.add_app("Student Summary", student_summary.app)

# The main app
app.run()