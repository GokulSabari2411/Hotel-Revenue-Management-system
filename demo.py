import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Set up the Streamlit page
st.set_page_config(
    page_title="Hotel Revenue Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f5f5;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #1e81b0; /* Custom background color (light blue) */
        color: white; /* Text color */
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        text-align: center;
        width: 30%;
    }
    .metric-card h2 {
        font-size: 28px;
        margin: 0;
    }
    .metric-card p {
        font-size: 16px;
        margin: 0;
        opacity: 0.8;
    }
    .block-container {
        padding: 1rem 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the dataset
@st.cache_data
def load_data():
    file_path = "C:/Users/pgoku/Downloads/hotel_revenue_with_past_dates.csv"
    data = pd.read_csv(file_path)
    if 'Booking_Date' not in data.columns:
        raise ValueError("The column 'Booking_Date' is missing from the dataset.")
    if 'Revenue' not in data.columns:
        raise ValueError("The column 'Revenue' is missing from the dataset.")
    data['Booking_Date'] = pd.to_datetime(data['Booking_Date'])
    return data

data = load_data()

# Main header
st.markdown("<h1 style='text-align: center; color: red;'>🏨 Hotel Revenue Management Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### 📊 Gain actionable insights into revenue, guest satisfaction, and more!")

# Sidebar Header
st.sidebar.title("🔍 Filters & Navigation")
st.sidebar.markdown("Customize your view with filters below.")

# Sidebar Filters
selected_hotel = st.sidebar.selectbox("Select Hotel", options=["All"] + data["Hotel_Name"].unique().tolist())
selected_date = st.sidebar.date_input(
    "Select Date Range",
    value=(data["Booking_Date"].min(), data["Booking_Date"].max())
)

# Apply Filters
filtered_data = data.copy()
if selected_hotel != "All":
    filtered_data = filtered_data[filtered_data["Hotel_Name"] == selected_hotel]

filtered_data = filtered_data[
    (filtered_data["Booking_Date"] >= pd.Timestamp(selected_date[0])) &
    (filtered_data["Booking_Date"] <= pd.Timestamp(selected_date[1]))
]

# Metrics Section
st.markdown("### Key Metrics")

# Metrics Data
total_revenue = filtered_data["Revenue"].sum() if "Revenue" in filtered_data.columns else 0
avg_guest_rating = filtered_data["Guest_Rating"].mean() if "Guest_Rating" in filtered_data.columns else 0
total_bookings = len(filtered_data) if not filtered_data.empty else 0

# Render Custom Metric Cards
st.markdown(
    f"""
    <div class="metric-container">
        <div class="metric-card">
            <h2>${total_revenue:,.2f}</h2>
            <p>Total Revenue</p>
        </div>
        <div class="metric-card">
            <h2>{avg_guest_rating:.2f}</h2>
            <p>Avg Guest Rating</p>
        </div>
        <div class="metric-card">
            <h2>{total_bookings}</h2>
            <p>Total Bookings</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Visualizations
st.markdown("### 📈 Visualizations & Insights")

# 1. Revenue Over Time
st.subheader("📅 Revenue Trend Over Time")
if not filtered_data.empty:
    revenue_trend = filtered_data.groupby(filtered_data["Booking_Date"].dt.date)["Revenue"].sum().reset_index()
    fig = px.line(revenue_trend, x="Booking_Date", y="Revenue", markers=True, title="Revenue Trend Over Time")
    fig.update_traces(line_color="blue", marker=dict(size=8))
    fig.update_layout(title_font_size=18, xaxis_title="Date", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

# 2. Guest Ratings Distribution
st.subheader("⭐ Guest Ratings Distribution")
if not filtered_data.empty and "Guest_Rating" in filtered_data.columns:
    fig = px.histogram(
        filtered_data,
        x="Guest_Rating",
        nbins=10,
        title="Distribution of Guest Ratings",
        color_discrete_sequence=["green"]
    )
    fig.update_layout(title_font_size=18, xaxis_title="Guest Rating", yaxis_title="Frequency")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Guest Ratings.")

# 3. Revenue by Hotel
st.subheader("🏨 Revenue by Hotel")
if not filtered_data.empty:
    hotel_revenue_data = filtered_data.groupby("Hotel_Name")["Revenue"].sum().reset_index()
    fig = px.bar(
        hotel_revenue_data,
        x="Hotel_Name",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="Blues",
        title="Total Revenue by Hotel"
    )
    fig.update_layout(title_font_size=18, xaxis_title="Hotel Name", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Revenue by Hotel.")

# 4. Revenue vs Competitor Price
st.subheader("💵 Revenue vs Competitor Price")
if not filtered_data.empty:
    fig = px.scatter(
        filtered_data,
        x="Competitor_Price",
        y="Revenue",
        color="Hotel_Name",
        title="Revenue vs Competitor Price",
        size="Revenue",
        hover_data=["Hotel_Name"]
    )
    fig.update_layout(title_font_size=18, xaxis_title="Competitor Price", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Revenue vs Competitor Price.")

# 5. Monthly Revenue Trend
st.subheader("📆 Monthly Revenue Trend")
if not filtered_data.empty:
    # Convert Period type to string
    filtered_data["Month"] = filtered_data["Booking_Date"].dt.to_period("M").astype(str)
    
    # Group by Month and calculate total revenue
    monthly_revenue = filtered_data.groupby("Month")["Revenue"].sum().reset_index()
    
    # Create the bar plot with Plotly
    fig = px.bar(
        monthly_revenue,
        x="Month",
        y="Revenue",
        text="Revenue",
        title="Monthly Revenue",
        color="Revenue",
        color_continuous_scale="Oranges"
    )
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig.update_layout(title_font_size=18, xaxis_title="Month", yaxis_title="Revenue")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Monthly Revenue.")


# Filtered Data Table and Export Option
st.subheader("🗂️ Filtered Data")
st.dataframe(filtered_data, use_container_width=True)
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_hotel_data.csv",
    mime="text/csv"
)



