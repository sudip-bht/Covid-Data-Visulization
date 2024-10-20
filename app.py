import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load COVID-19 dataset (replace with your dataset source)
@st.cache
def load_data():
    url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
    data = pd.read_csv(url)
    data['Date'] = pd.to_datetime(data['Date'])  # Ensure the Date column is in datetime format
    data['Active'] = data['Confirmed'] - data['Recovered'] - data['Deaths']
    return data

# Function to filter the data based on selected countries and date range
def filter_data(data, countries, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    mask = (data['Country'].isin(countries)) & (data['Date'] >= start_date) & (data['Date'] <= end_date)
    return data[mask]

# Load data
data = load_data()



# Header Section
st.title("🌍 COVID-19 Data Visualization Dashboard")
st.markdown("""
    This dashboard allows you to visualize COVID-19 data trends across countries, including infection rates, vaccination progress, and death tolls.
    You can select countries and date ranges to customize the view of the data.
""")

# Sidebar for user inputs
st.sidebar.header("Customize the Dashboard")
countries = st.sidebar.multiselect("Select countries", options=data['Country'].unique(), default=[])
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2020-01-22"))
end_date = st.sidebar.date_input("End date", value=pd.to_datetime("2021-12-31"))

# Filter data based on user selection
filtered_data = filter_data(data, countries, start_date, end_date)

# Dashboard Layout
st.markdown("## 📈 COVID-19 Trends Over Time")
# Time Series Plot
fig = px.line(filtered_data, x="Date", y="Confirmed", color="Country", title="Confirmed COVID-19 Cases Over Time", template="plotly_dark")
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Daily New Cases
st.markdown("## 📊 Daily New COVID-19 Cases")
filtered_data['Daily New Cases'] = filtered_data.groupby('Country')['Confirmed'].diff().fillna(0)
fig2 = px.bar(filtered_data, x="Date", y="Daily New Cases", color="Country", title="Daily New COVID-19 Cases", template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# Cumulative Cases
st.markdown("## 🌍 Total Confirmed COVID-19 Cases")
cumulative_data = filtered_data.groupby('Country').max().reset_index()
fig3 = px.bar(cumulative_data, x="Country", y="Confirmed", title="Total Confirmed COVID-19 Cases", template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

# Vaccination Progress (Dummy Data - Update with actual vaccination data if available)
st.markdown("## 💉 Vaccination Progress")
vaccination_data = {
    "Country": ["United States", "India", "Brazil", "UK", "Germany"],
    "Vaccinations": [300000000, 800000000, 200000000, 70000000, 60000000]
}
vaccination_df = pd.DataFrame(vaccination_data)
fig4 = px.bar(vaccination_df, x="Country", y="Vaccinations", title="Vaccination Progress by Country", template="plotly_dark")
st.plotly_chart(fig4, use_container_width=True)

# Active vs Recovered vs Deaths Pie Chart
st.markdown("## 📊 Active vs Recovered vs Deaths")
latest_data = filtered_data[filtered_data['Date'] == filtered_data['Date'].max()]
fig5 = go.Figure(data=[go.Pie(labels=['Active', 'Recovered', 'Deaths'],
                              values=[latest_data['Active'].sum(), latest_data['Recovered'].sum(), latest_data['Deaths'].sum()],
                              hoverinfo="label+percent+value", textinfo="label+percent", marker=dict(colors=['#1f77b4', '#2ca02c', '#d62728']))])
fig5.update_layout(title="Active vs Recovered vs Deaths (Latest Data)", template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# World Map Visualization
st.markdown("## 🌍 Geospatial Visualization of COVID-19 Cases")
fig6 = px.choropleth(filtered_data, locations="Country", locationmode="country names", color="Confirmed",
                     hover_name="Country", animation_frame="Date", title="Spread of COVID-19 Globally Over Time",
                     template="plotly_dark")
st.plotly_chart(fig6, use_container_width=True)

# Footer
st.markdown("""
    **Data Source**: [Johns Hopkins University](https://github.com/datasets/covid-19).  
    **Dashboard Built With**: Streamlit, Plotly
""")
