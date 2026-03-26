import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
# Set the configuration for the Streamlit page.
st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="images/ola logo.png",
    layout="wide"
)

# --- Data Loading ---
# Create a cached function to load the data, so it doesn't reload on every interaction.

@st.cache_data
def load_data():
    """Loads and cleans the dataset."""
    try:
        df = pd.read_csv('OLA_Ride_Cleaned_Data - July.csv')
        df['Booking_Timestamp'] = pd.to_datetime(df['Booking_Timestamp'])
        return df
    except FileNotFoundError:
        st.error("CSV file 'OLA_Ride_Cleaned_Data - July.csv' not found. Please make sure the file is in the same folder as this app.")
        return None
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

# Load the data into the app.
df = load_data()

# If data failed to load, stop the app from rendering further content
if df is None:
    st.stop()

# --- Sidebar for Navigation ---
# Create a radio button in the sidebar to act as the navigation menu.

# Add OLA logo to the top of the sidebar navigation
st.sidebar.image("images/ola logo.png", width=80)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Overall Metrics & Trends", "Revenue & Customer Insights", "Cancellation Analysis", "Power BI Dashboard Showcase", "SQL Insights"])

# --- SQL Insights Page ---
if page == "SQL Insights":
    st.header("SQL Insights: Key Questions Answered")

    st.subheader("1. Retrieve all successful bookings:")
    st.dataframe(df[df['Booking_Status'] == 'Success'])

    st.subheader("2. Find the average ride distance for each vehicle type:")
    avg_dist = df[df['Booking_Status'] == 'Success'].groupby('Vehicle_Type')['Ride_Distance'].mean().reset_index()
    st.dataframe(avg_dist)

    st.subheader("3. Get the total number of cancelled rides by customers:")
    total_cancelled_by_customer = df[df['Booking_Status'] == 'Canceled by Customer'].shape[0]
    st.write(f"Total cancelled rides by customers: {total_cancelled_by_customer}")

    st.subheader("4. List the top 5 customers who booked the highest number of rides:")
    top_customers = df['Customer_ID'].value_counts().nlargest(5).reset_index()
    top_customers.columns = ['Customer_ID', 'Number of Rides']
    st.dataframe(top_customers)

    st.subheader("5. Get the number of rides cancelled by drivers due to personal and car-related issues:")
    driver_cancelled_personal = df[df['Canceled_Rides_by_Driver'] == 'Personal & Car related issue'].shape[0]
    st.write(f"Rides cancelled by drivers due to personal/car issues: {driver_cancelled_personal}")

    st.subheader("6. Find the maximum and minimum driver ratings for Prime Sedan bookings:")
    sedan_ratings = df[df['Vehicle_Type'] == 'Prime Sedan']['Driver_Ratings']
    st.write(f"Max rating: {sedan_ratings.max()}, Min rating: {sedan_ratings.min()}")

    st.subheader("7. Retrieve all rides where payment was made using UPI:")
    st.dataframe(df[df['Payment_Method'] == 'UPI'])

    st.subheader("8. Find the average customer rating per vehicle type:")
    avg_cust_rating = df.groupby('Vehicle_Type')['Customer_Rating'].mean().reset_index()
    st.dataframe(avg_cust_rating)

    st.subheader("9. Calculate the total booking value of rides completed successfully:")
    # Clean Booking_Value for calculation
    success_rides = df[df['Booking_Status'] == 'Success'].copy()
    success_rides['Booking_Value'] = success_rides['Booking_Value'].astype(str).str.replace(',', '')
    success_rides['Booking_Value'] = pd.to_numeric(success_rides['Booking_Value'], errors='coerce')
    total_booking_value = success_rides['Booking_Value'].sum()
    st.write(f"Total booking value: ₹{total_booking_value:,.2f}")

    st.subheader("10. List all incomplete rides along with the reason:")
    incomplete_rides = df[df['Booking_Status'] != 'Success'][['Booking_ID', 'Booking_Status', 'Cancellation_Reason']]
    st.dataframe(incomplete_rides)

# --- Main Content ---

# If the "Home" page is selected in the sidebar:
if page == "Home":
    st.title("Welcome to the OLA Ride Insights Dashboard 🚕")
    col_logo, col_text = st.columns([1, 5])
    with col_logo:
        st.image("images/ola logo.png", width=120)
    with col_text:
        st.markdown("""
        This interactive application provides a comprehensive analysis of OLA ride-sharing data. The insights are generated directly from the dataset, replicating the logic of key SQL queries to explore booking trends, revenue, and cancellation patterns.
        """)
    st.markdown("<b>Use the sidebar on the left to navigate to different analytical views.</b>", unsafe_allow_html=True)

# If the "Overall Metrics & Trends" page is selected:
elif page == "Overall Metrics & Trends":
    st.header("Overall Metrics & Trends")

    # Calculate KPIs using Pandas.
    total_rides = df.shape[0]
    successful_rides = df[df['Booking_Status'] == 'Success'].shape[0]
    avg_driver_rating = round(df['Driver_Ratings'].mean(), 2)
    
    # Display KPIs in columns.
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rides Booked", f"{total_rides:,}")
    col2.metric("Successful Rides", f"{successful_rides:,}")
    col3.metric("Average Driver Rating", f"{avg_driver_rating} ⭐")

    st.markdown("---")
    st.subheader("Booking Status Breakdown")
    status_counts = df['Booking_Status'].value_counts()
    fig_status = px.pie(status_counts, names=status_counts.index, values=status_counts.values, title="Proportion of Ride Statuses")
    st.plotly_chart(fig_status, use_container_width=True)

    st.markdown("---")
    st.subheader("Average Ride Distance by Vehicle Type")
    # This insight corresponds to SQL Query #2
    avg_dist_vehicle = df[df['Booking_Status'] == 'Success'].groupby('Vehicle_Type')['Ride_Distance'].mean().sort_values(ascending=False)
    fig_dist = px.bar(avg_dist_vehicle, x=avg_dist_vehicle.index, y=avg_dist_vehicle.values, title="Average Ride Distance per Vehicle Type", labels={'x': 'Vehicle Type', 'y': 'Average Distance (km)'})
    st.plotly_chart(fig_dist, use_container_width=True)

# If the "Revenue & Customer Insights" page is selected:
elif page == "Revenue & Customer Insights":
    st.header("Revenue & Customer Insights")

    # Calculate KPIs.

    # Clean Booking_Value column: remove commas and convert to float
    success_rides = df[df['Booking_Status'] == 'Success'].copy()
    success_rides['Booking_Value'] = success_rides['Booking_Value'].astype(str).str.replace(',', '')
    success_rides['Booking_Value'] = pd.to_numeric(success_rides['Booking_Value'], errors='coerce')
    total_revenue = int(success_rides['Booking_Value'].sum())
    avg_fare = round(success_rides['Booking_Value'].mean(), 2)

    col1, col2 = st.columns(2)
    col1.metric("Total Revenue from Success Rides", f"₹{total_revenue:,}")
    col2.metric("Average Fare per Ride", f"₹{avg_fare}")


    st.markdown("---")
    st.subheader("Revenue by Payment Method")
    # Clean Booking_Value for payment method chart
    payment_df = success_rides.copy()
    payment_df['Booking_Value'] = payment_df['Booking_Value'].astype(str).str.replace(',', '')
    payment_df['Booking_Value'] = pd.to_numeric(payment_df['Booking_Value'], errors='coerce')
    revenue_by_payment = payment_df.groupby('Payment_Method')['Booking_Value'].sum().sort_values(ascending=True)

    fig_payment = px.bar(
        revenue_by_payment,
        x=revenue_by_payment.values,
        y=revenue_by_payment.index,
        orientation='h',
        title="Total Revenue by Payment Method",
        labels={
            'y': 'Payment Method',
            'x': 'Total Revenue (INR)'
        },
        text_auto='.2s',
        color_discrete_sequence=['#00cc96']
    )
    fig_payment.update_layout(
        xaxis_title='Total Revenue (INR)',
        yaxis_title='Payment Method',
        plot_bgcolor='#181818',
        paper_bgcolor='#181818',
        font_color='white',
        title_font_size=22,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    fig_payment.update_traces(marker_line_color='white', marker_line_width=2, textfont_size=14)
    st.plotly_chart(fig_payment, use_container_width=True)

    st.markdown("---")
    st.subheader("Top 5 Customers by Number of Rides")
    # This insight corresponds to SQL Query #4
    top_customers = df['Customer_ID'].value_counts().nlargest(5)
    st.dataframe(top_customers.reset_index().rename(columns={'index': 'Customer_ID', 'Customer_ID': 'Number of Rides'}))

# If the "Cancellation Analysis" page is selected:
elif page == "Cancellation Analysis":
    st.header("Cancellation Analysis")
    
    # Calculate KPIs.
    total_cancelled = df[df['Booking_Status'] != 'Success'].shape[0]
    customer_cancelled = df[df['Booking_Status'] == 'Canceled by Customer'].shape[0]
    driver_cancelled = df[df['Booking_Status'] == 'Canceled by Driver'].shape[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cancelled Rides", f"{total_cancelled:,}")
    col2.metric("Cancelled by Customer", f"{customer_cancelled:,}")
    col3.metric("Cancelled by Driver", f"{driver_cancelled:,}")

    st.markdown("---")
    st.subheader("Top Reasons for Customer Cancellations")
    customer_reasons = df[df['Canceled_Rides_by_Customer'].notna()]['Canceled_Rides_by_Customer'].value_counts()
    fig_cust_cancel = px.bar(customer_reasons, y=customer_reasons.index, x=customer_reasons.values, orientation='h', title="Customer Cancellation Reasons", labels={'y': 'Reason', 'x': 'Number of Cancellations'})
    st.plotly_chart(fig_cust_cancel, use_container_width=True)

# If the "Power BI Dashboard Showcase" page is selected:
elif page == "Power BI Dashboard Showcase":
    st.header("Power BI Dashboard Showcase")
    st.markdown("""
    Since public embedding requires a Power BI Pro account, below are images of the final interactive dashboard. 
    Each view was designed to be fully interactive with slicers and cross-filtering.
    """)

    st.markdown("---")
    st.info("To experience the fully interactive dashboard, you can [download the Power BI file here](YOUR_SHAREABLE_LINK_HERE). You will need Power BI Desktop to open it.")
    
    # Display each screenshot from your project folder.
    st.subheader("1. Overall View")
    st.image("overall_view.png")

    st.subheader("2. Vehicle Type View")
    st.image("vehicle_type_view.png")

    st.subheader("3. Revenue View")
    st.image("revenue_view.png")
        
    st.subheader("4. Cancellation View")
    st.image("cancellation_view.png")
        
    st.subheader("5. Ratings View")
    st.image("ratings_view.png")
