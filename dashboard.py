import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from df import df

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Housing in mexico Dashboard")
map_fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    # center={"lat": -14.2, "lon": -51.9},  # Map will be centered on Brazil
    width=600,
    height=600,
    color="region",
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

map_fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(map_fig)

# Sidebar Title
st.sidebar.title("Filter Options")

# Region Filter
selected_regions = st.sidebar.multiselect("Select Region(s):", df["region"].unique(), default=df["region"].unique())

# State Filter
states_in_selected_regions = df[df["region"].isin(selected_regions)]["state"].unique()
selected_states = st.sidebar.multiselect("Select State(s):", states_in_selected_regions, default=states_in_selected_regions)

# Area Filter
min_area = st.sidebar.slider("Minimum Area (sq meters):", min_value=df["area_m2"].min(), max_value=df["area_m2"].max(), value=df["area_m2"].min())
max_area = st.sidebar.slider("Maximum Area (sq meters):", min_value=min_area, max_value=df["area_m2"].max(), value=df["area_m2"].max())

# Price Filter
min_price = st.sidebar.slider("Minimum Price (USD):", min_value=df["price_usd"].min(), max_value=df["price_usd"].max(), value=df["price_usd"].min())
max_price = st.sidebar.slider("Maximum Price (USD):", min_value=min_price, max_value=df["price_usd"].max(), value=df["price_usd"].max())

# Apply Filters
filtered_data = df[(df["region"].isin(selected_regions)) &
                   (df["state"].isin(selected_states)) &
                   (df["area_m2"] >= min_area) &
                   (df["area_m2"] <= max_area) &
                   (df["price_usd"] >= min_price) &
                   (df["price_usd"] <= max_price)]

# Display Filtered Data
st.write("Filtered Data:")
st.write(filtered_data)

# Display Figures
st.subheader("Exploratory Data Analysis")

# Distribution of Home Prices
st.write("Distribution of Home Prices")
plt.hist(filtered_data["price_usd"])
plt.xlabel("Price [USD]")
plt.ylabel("Frequency")
st.pyplot()

# Distribution of Home Sizes
st.write("Distribution of Home Sizes")
plt.boxplot(filtered_data["area_m2"])
plt.xlabel("Area [sq meters]")
st.pyplot()

# Mean Home Price by Region
st.write("Mean Home Price by Region")
mean_price_by_region = filtered_data.groupby("region")["price_usd"].mean()
mean_price_by_region.plot(kind="bar", xlabel="Region", ylabel="Mean Price [USD]")
st.pyplot()

# Multiselect dropdown to select states
selected_states = st.multiselect("Select States:", df["state"].unique())

# Show scatter plots for selected states
for selected_state in selected_states:
    st.write(f"Price vs. Area for {selected_state}")
    scatter_fig = px.scatter(filtered_data[filtered_data["state"] == selected_state], x="price_usd", y="area_m2", 
                             title=f"{selected_state}: Price vs. Area", labels={"price_usd": "Price [USD]", "area_m2": "Area [sq meters]"},
                             width=800, height=500)
    scatter_fig.update_layout(showlegend=False)
    st.plotly_chart(scatter_fig)

# Correlation Coefficients
homes_by_state = filtered_data["state"].value_counts().sort_values()

show_corr = st.checkbox("Show Correlation Coefficients")
south_states_corr = {}
for state, data in homes_by_state.items():
    state_data = filtered_data[filtered_data["state"] == state]
    correlation = state_data["area_m2"].corr(state_data["price_usd"])
    south_states_corr[state] = correlation
if show_corr:
    st.write("Correlation Coefficients:")
    # south_states_corr = filtered_data.groupby("state").head()
    st.write(south_states_corr)
