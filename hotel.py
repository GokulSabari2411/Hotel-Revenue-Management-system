import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def load_data():
    file_path = "D:\All Projects\hotel_revenue_with_past_dates.csv"
    df = pd.read_csv(file_path)
    df['Booking_Date'] = pd.to_datetime(df['Booking_Date'])
    return df


def local_css(css_code):
    st.markdown(f'<style>{css_code}</style>', unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Hotel Revenue Dashboard", layout="wide")

    # Advanced CSS Styling
    css = """
    body {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding: 2rem 3rem;
    }
    .css-1v0mbdj.e1f1d6gn1 {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
    }
    .stMetric {
        border: 1px solid #dee2e6;
        padding: 15px;
        border-radius: 10px;
        background-color: #1E90FF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stMetricLabel {
        font-size: 16px;
        color: #1E90FF;
    }
    .stMetricValue {
        font-size: 24px;
        color: #007bff !important;
        font-weight: bold;
    }
    .stSidebar {
        background-color: #343a40;
    }
    .css-6qob1r.eczjsme3 {
        background-color: #343a40 !important;
        color: #ffffff;
    }
    .stSelectbox > label, .stDateInput > label {
        color: #ffffff;
        font-weight: 500;
    }
    """
    local_css(css)

    df = load_data()

    # Sidebar
    st.sidebar.title("Filters")
    hotel_names = ['All'] + list(df['Hotel_Name'].unique())
    selected_hotel = st.sidebar.selectbox("Select Hotel Name", hotel_names)
    start_date, end_date = st.sidebar.date_input("Select Date Range", [df['Booking_Date'].min(), df['Booking_Date'].max()])

    # Filter data
    df = df[(df['Booking_Date'] >= pd.to_datetime(start_date)) & (df['Booking_Date'] <= pd.to_datetime(end_date))]
    if selected_hotel != 'All':
        df = df[df['Hotel_Name'] == selected_hotel]

    st.title("🏨 Hotel Revenue Management Dashboard")

    # Key Metrics
    total_revenue = df['Revenue'].sum()
    avg_guest_rating = df['Guest_Rating'].mean()
    total_bookings = len(df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    with col2:
        st.metric("⭐ Avg Guest Rating", f"{avg_guest_rating:.2f}")
    with col3:
        st.metric("📦 Total Bookings", f"{total_bookings}")

    st.markdown("---")

    # Revenue Trend
    st.subheader("📈 Revenue Trends Over Time")
    revenue_trend = df.groupby('Booking_Date')['Revenue'].sum().reset_index()
    fig = px.line(revenue_trend, x='Booking_Date', y='Revenue', title='Revenue Over Time', markers=True)
    fig.update_layout(plot_bgcolor='white', xaxis_title='Date', yaxis_title='Revenue')
    st.plotly_chart(fig, use_container_width=True)

    # Occupancy Distribution
    st.subheader("🏨 Occupancy Distribution")
    occupancy_counts = df['Occupancy_Status'].value_counts().reset_index()
    occupancy_counts.columns = ['Status', 'Count']
    fig = px.pie(occupancy_counts, values='Count', names='Status', title='Occupancy Status Distribution', color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)

    # Guest Rating Distribution
    st.subheader("📊 Guest Rating Distribution")
    fig = px.histogram(df, x='Guest_Rating', nbins=10, title='Guest Rating Histogram', color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig, use_container_width=True)

    # Revenue vs Competitor Price
    st.subheader("📉 Revenue vs. Competitor Price")
    fig = px.scatter(df, x='Competitor_Price', y='Revenue', title='Revenue vs Competitor Price', color_discrete_sequence=['#AB63FA'])
    st.plotly_chart(fig, use_container_width=True)

    # NEW CHART: Avg Revenue per Booking by Room Type
    st.subheader("🛏️ Avg Revenue per Booking by Room Type")
    if 'Room_Number' in df.columns:
        revenue_per_room = df.groupby('Room_Number')['Revenue'].mean().reset_index().sort_values(by='Revenue', ascending=False)
        fig = px.bar(
            revenue_per_room,
            x='Room_Number',
            y='Revenue',
            title='Average Revenue per Booking by Room Type',
            color='Revenue',
            color_continuous_scale='Blues'
        )
        fig.update_layout(xaxis_title='Room Number', yaxis_title='Avg Revenue', plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Room_Number column not found in data.")


if __name__ == "__main__":
    main()
