# Capstone_SecondProject

## Phonepe Pulse Data Visualization and Exploration

Phonepe Pulse Data Visualization and Exploration project is used to visualize the data through the dashboard through Streamlit and Plotly.

## Features:

* **Git Repository Cloning**: Users can clone the Git repository to access the project files and resources.
* **Data Filtering:** Python scripting is utilized to filter and preprocess the raw transaction data, ensuring its suitability for visualization.
* **Database Management:** The project facilitates the creation of a database schema and the insertion of transaction data into MySQL tables.
* **Geo Visualization:** Utilizing Plotly, the project enables geographic visualization of transaction data, allowing users to analyze regional transaction trends.
* **Plotly Visualizations:** Different types of Plotly visualizations such as scatter plots, line charts, and pie charts are available to showcase transaction patterns and insights.
* **Insight Generation:** Insights are derived from PhonePe Pulse data, and key findings are presented on the dashboard through Streamlit.


## Technologies Used:

  ~ GitHub Cloning
  ~ Python
  ~ MySQL
  ~ Pandas
  ~ Streamlit
  ~ Plotly

### 💻 Import Packages

```python
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import requests
import json
import plotly_express as px
