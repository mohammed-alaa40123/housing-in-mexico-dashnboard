from df import *
from figures import *
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Housing in mexico Dashboard")

st.plotly_chart(map_fig)

# Sidebar Title
st.sidebar.title("Filter Options")

# Region Filter
selected_regions = st.sidebar.multiselect("Select Region(s):", df["region"].unique(), default=df["region"].unique())

# State Filter
states_in_selected_regions = df[df["region"].isin(selected_regions)]["state"].unique()
selected_states = st.sidebar.multiselect("Select State(s):", states_in_selected_regions, default=states_in_selected_regions)

# Area Filter
min_value = df["area_m2"].min()
max_value = df["area_m2"].max()
area = st.sidebar.slider("Minimum Area (sq meters):", min_value=min_value, max_value=max_value, value=[min_value,max_value])

# Price Filter
min_value = df["price_usd"].min()
max_value = df["price_usd"].max()
price = st.sidebar.slider("Minimum Price (USD):", min_value=min_value, max_value=max_value, value=[min_value,max_value])

# Apply Filters
filtered_data = df[(df["region"].isin(selected_regions)) &
                   (df["state"].isin(selected_states)) &
                   (df["area_m2"] >= area[0]) &
                   (df["area_m2"] <= area[1]) &
                   (df["price_usd"] >= price[0]) &
                   (df["price_usd"] <= price[1])]

# Display Filtered Data
st.write("Filtered Data:")
st.write(filtered_data)

# Display Figures
st.subheader("Exploratory Data Analysis")
show_figures(filtered_data)

# Display correlation coeffecients
show_corr = st.checkbox("Show Correlation Coefficients")

south_states_corr = calculate_correlation(filtered_data)
if show_corr:
    st.write("Correlation Coefficients:")
    st.write(south_states_corr)
