from df import *
import matplotlib.pyplot as plt
import plotly.express as px

map_fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    center={"lat": -23.19, "lon": -47.17},  # Map will be centered on Brazil
    width=600,
    height=600,
    color="region",
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

map_fig.update_layout(mapbox_style="open-street-map")

def show_figures(filtered_data):
        
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

    # Count homes by state
    homes_by_state = filtered_data["state"].value_counts().sort_values(ascending=False)

    # Limit to top 5 states
    top_5_states = homes_by_state.head(5)

    # Combine the rest into "Others"
    other_states_count = homes_by_state.iloc[5:].sum()

    # Create a DataFrame with top 5 states and "Others"
    pie_data = pd.DataFrame({"state": top_5_states.index.tolist() + ["Others"], 
                            "count": top_5_states.values.tolist() + [other_states_count]})

    fig = px.pie(pie_data, names="state", values="count", title="Homes by State (Top 5 + Others)")
    st.plotly_chart(fig)
    
    
def calculate_correlation(filtered_data):
    homes_by_state = filtered_data["state"].value_counts().sort_values(ascending=False)
    south_states_corr = {}
    for state, data in homes_by_state.items():
        state_data = filtered_data[filtered_data["state"] == state]
        correlation = state_data["area_m2"].corr(state_data["price_usd"])
        south_states_corr[state] = correlation
    return south_states_corr