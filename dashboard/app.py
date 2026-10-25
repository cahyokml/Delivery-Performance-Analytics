import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(page_title="Delivery Performance Analytics", layout="wide")

# Load Data
@st.cache_data
def load_data():
    path = 'data/processed/fact_orders.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Parse dates
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        return df
    return None

df = load_data()

if df is None:
    st.error("Data `fact_orders.csv` tidak ditemukan. Silakan jalankan `python src/02_clean_merge.py` terlebih dahulu.")
else:
    # --- HEADER ---
    st.title("📦 E-Commerce Delivery Performance Dashboard")
    st.markdown("Analisis performa pengiriman, identifikasi akar masalah keterlambatan, dan dampaknya terhadap kepuasan pelanggan.")

    # --- SIDEBAR FILTER ---
    st.sidebar.header("Filter Data")
    states = ['Semua Negara Bagian'] + sorted(df['customer_state'].dropna().unique().tolist())
    selected_state = st.sidebar.selectbox("Pilih Negara Bagian (State)", states)
    
    # Filter dataframe based on selection
    if selected_state == 'Semua Negara Bagian':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['customer_state'] == selected_state]

    # --- KPI METRICS ---
    total_orders = len(filtered_df)
    late_orders = filtered_df['is_late'].sum()
    otd_rate = (filtered_df['is_on_time'].sum() / total_orders) * 100 if total_orders > 0 else 0
    avg_delay = filtered_df['delay_days'].mean() if total_orders > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pesanan", f"{total_orders:,}")
    col2.metric("On-Time Delivery Rate", f"{otd_rate:.2f}%")
    col3.metric("Rata-rata Selisih Hari", f"{avg_delay:.2f} Hari", help="Negatif berarti datang lebih awal")
    col4.metric("Total Pesanan Terlambat", f"{late_orders:,}")

    st.divider()

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["📍 Performa Per Wilayah", "🌟 Dampak Terhadap Review", "📊 Distribusi Keterlambatan"])

    with tab1:
        st.subheader("Tingkat Keterlambatan per Negara Bagian")
        state_perf = filtered_df.groupby('customer_state').agg(
            total_orders=('order_id', 'count'),
            late_orders=('is_late', 'sum')
        ).reset_index()
        state_perf['late_rate'] = (state_perf['late_orders'] / state_perf['total_orders']) * 100
        state_perf = state_perf[state_perf['total_orders'] > 50].sort_values('late_rate', ascending=False).head(15)
        
        fig1 = px.bar(state_perf, x='customer_state', y='late_rate', 
                      title='15 Negara Bagian dengan Tingkat Keterlambatan Tertinggi (%)',
                      labels={'late_rate': 'Late Rate (%)', 'customer_state': 'State'},
                      color='late_rate', color_continuous_scale='Reds')
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.subheader("Dampak Keterlambatan pada Skor Ulasan")
        review_data = filtered_df.dropna(subset=['review_score']).copy()
        review_data['Delivery Status'] = review_data['is_late'].map({True: 'Terlambat', False: 'Tepat Waktu'})
        
        col_a, col_b = st.columns(2)
        with col_a:
            fig2 = px.box(review_data, x='Delivery Status', y='review_score', color='Delivery Status',
                          title='Distribusi Skor Ulasan (1-5)',
                          color_discrete_map={'Tepat Waktu': 'green', 'Terlambat': 'red'})
            st.plotly_chart(fig2, use_container_width=True)
            
        with col_b:
            avg_reviews = review_data.groupby('Delivery Status')['review_score'].mean().reset_index()
            fig3 = px.bar(avg_reviews, x='Delivery Status', y='review_score', color='Delivery Status',
                          title='Rata-rata Skor Ulasan',
                          color_discrete_map={'Tepat Waktu': 'green', 'Terlambat': 'red'},
                          text_auto='.2f')
            fig3.update_yaxes(range=[0, 5])
            st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.subheader("Tren Keterlambatan Bulanan")
        filtered_df['month'] = filtered_df['order_purchase_timestamp'].dt.to_period('M').astype(str)
        monthly = filtered_df.groupby('month').agg(
            total_orders=('order_id', 'count'),
            late_orders=('is_late', 'sum')
        ).reset_index()
        monthly['late_rate'] = (monthly['late_orders'] / monthly['total_orders']) * 100
        
        fig4 = px.line(monthly, x='month', y='late_rate', markers=True,
                       title='Persentase Keterlambatan per Bulan (%)',
                       labels={'month': 'Bulan', 'late_rate': 'Late Rate (%)'})
        st.plotly_chart(fig4, use_container_width=True)