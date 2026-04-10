import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config with dark theme
st.set_page_config(
    page_title="Book Data Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and modern styling
st.markdown("""
<style>
    /* Dark theme background */
    .main, .block-container {
        background-color: #0f172a;
        color: #ffffff;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #111827;
        border-right: 3px solid #2196F3;
    }

    /* Title styling */
    h1 {
        color: #60a5fa !important;
        text-align: center;
        font-size: 3rem !important;
        margin-bottom: 2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    h2, h3 {
        color: #93c5fd !important;
    }

    /* Metric cards styling */
    .stMetric {
        background: linear-gradient(135deg, #111827 0%, #0f172a 100%);
        border: 2px solid #2196F3;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.3);
    }

    .stMetric label {
        color: #93c5fd !important;
        font-size: 0.9rem !important;
    }

    .stMetric div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: bold !important;
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #2196F3, #60a5fa);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(45deg, #60a5fa, #2196F3);
        transform: scale(1.05);
    }

    /* Multi-select and filter styling */
    div[data-baseweb="select"] {
        background-color: #111827 !important;
        border: 1px solid #2196F3 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] input,
    div[data-baseweb="select"] div {
        color: #ffffff !important;
    }

    div[data-baseweb="tag-list"] > div {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
        border: 1px solid #93c5fd !important;
    }

    div[data-testid="stSlider"] label,
    div[data-testid="stSlider"] span,
    div[data-testid="stSlider"] div {
        color: #93c5fd !important;
    }

    input[type="range"] {
        -webkit-appearance: none;
        width: 100%;
        height: 8px;
        background: transparent;
        margin: 0;
    }

    input[type="range"]::-webkit-slider-runnable-track {
        background: linear-gradient(90deg, #2196f3 0%, #93c5fd 100%) !important;
        border-radius: 8px;
        height: 8px;
    }

    input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #2196f3;
        border: 2px solid #93c5fd;
        margin-top: -5px;
    }

    input[type="range"]::-moz-range-track {
        background: linear-gradient(90deg, #2196f3 0%, #93c5fd 100%) !important;
        border-radius: 8px;
        height: 8px;
    }

    input[type="range"]::-moz-range-thumb {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: #2196f3;
        border: 2px solid #93c5fd;
    }

    /* Table styling */
    .stTable {
        background-color: #111827;
        border-radius: 10px;
        border: 1px solid #2196F3;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #0f172a;
    }

    ::-webkit-scrollbar-thumb {
        background: #2196F3;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #60a5fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('new_data/transformed/books/books_transformed.csv')

try:
    df = load_data()
    st.title("Book Market Analytics Dashboard")
    st.markdown("---")

    st.sidebar.header("Filter Options")
    rating_filter = st.sidebar.multiselect("Select Ratings", options=sorted(df['rating'].unique()), default=df['rating'].unique())
    price_range = st.sidebar.slider("Price Range (₹)", float(df['price'].min()), float(df['price'].max()), (0.0, 100.0))

    filtered_df = df[(df['rating'].isin(rating_filter)) & (df['price'].between(price_range[0], price_range[1]))]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Books", len(filtered_df))
    m2.metric("Avg Price", f"₹{filtered_df['price'].mean():.2f}")
    m3.metric("Avg Rating", f"{filtered_df['rating'].mean():.1f}")
    m4.metric("In Stock", f"{filtered_df['availability'].sum()} units")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pricing Distribution")
        fig_hist = px.histogram(
            filtered_df,
            x="price",
            nbins=20,
            color_discrete_sequence=['#2196F3'],
            labels={'price': 'Price (₹)', 'count': 'Number of Books'},
            title="Book Price Distribution"
        )
        fig_hist.update_traces(
            marker_line_color='#64B5F6',
            marker_line_width=2,
            opacity=0.8
        )
        fig_hist.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#2d2d2d',
            font_color='#ffffff',
            xaxis_title="Book Price (₹)",
            yaxis_title="Number of Books",
            bargap=0.05,
            xaxis=dict(
                tickmode='linear',
                tick0=0.0,
                dtick=2.5,
                tickformat='.1f',
                showgrid=True,
                gridcolor='#404040',
                zeroline=False,
                linecolor='#64B5F6',
                tickcolor='#64B5F6'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#404040',
                linecolor='#64B5F6',
                tickcolor='#64B5F6'
            ),
            title={
                'text': "Book Price Distribution",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': '#2196F3', 'size': 20}
            },
            margin={'t': 60, 'b': 50, 'l': 50, 'r': 20}
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.subheader("Rating Analysis")
        rating_counts = filtered_df['rating'].value_counts().reset_index()
        fig_pie = px.pie(
            rating_counts,
            values='count',
            names='rating',
            hole=0.4,
            color_discrete_sequence=['#2196F3', '#64B5F6', '#90CAF9', '#BBDEFB', '#E3F2FD']
        )
        fig_pie.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font_color='#ffffff',
            title={
                'text': "Rating Distribution",
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color': '#2196F3', 'size': 20}
            },
            margin={'t': 60, 'b': 50, 'l': 20, 'r': 20}
        )
        fig_pie.update_traces(
            textinfo='percent+label',
            textfont_color='#ffffff',
            marker=dict(line=dict(color='#64B5F6', width=2))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    
    st.subheader("High-Value & Top-Rated Books")
    high_value = filtered_df.sort_values(by=['rating', 'price'], ascending=[False, False]).head(10)
    st.table(high_value[['title', 'price', 'rating', 'page_metadata']])

except Exception as e:
    st.error(f"Please ensure the data pipeline has been run. Error: {e}")