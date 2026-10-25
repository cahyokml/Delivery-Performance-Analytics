from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# 1. Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Delivery Performance Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "processed"

# --------------------------------------------------
# 2. CUSTOM CSS (DARK MODE, GLASSMORPHISM & PRO ICONS)
# --------------------------------------------------
st.markdown("""
<style>
    /* Latar Belakang Gelap */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0f172a 0%, #020617 100%);
    }
    
    /* Panel Utama dengan Efek Kaca */
    .main .block-container {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem !important;
        margin-top: 2rem;
        max-width: 1400px;
    }
    
    /* Sidebar Kaca */
    [data-testid="stSidebar"] > div:first-child {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* KPI CARDS MODERN DENGAN IKON SVG */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 15px;
        display: flex;
        flex-direction: column;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        border-color: rgba(96, 165, 250, 0.4);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
    }
    .kpi-icon-box {
        background: rgba(96, 165, 250, 0.1);
        border-radius: 10px;
        padding: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .kpi-icon-box svg {
        width: 20px;
        height: 20px;
        stroke: #60a5fa;
        stroke-width: 2;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    .kpi-label {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #e2e8f0, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .kpi-note {
        color: #64748b;
        font-size: 12px;
        margin-top: 6px;
    }

    /* Text & UI Fixes */
    h1, h2, h3 { color: #f8fafc !important; font-weight: 650; }
    div[data-testid="stHorizontalBlock"] { gap: 1.5rem; }
    hr { margin-top: 1rem; margin-bottom: 1.5rem; border-color: rgba(255, 255, 255, 0.1); }
    .stDownloadButton button {
        border-radius: 8px; font-weight: 600;
        background-color: #1e293b; color: white; border: 1px solid #334155;
    }
    [data-testid="stPlotlyChart"] { border-radius: 12px; padding: 8px; background: transparent; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    orders_path = DATA_DIR / "fact_orders.csv"
    if not orders_path.exists():
        raise FileNotFoundError("Dataset tidak ditemukan di data/processed/. Jalankan pipeline dulu!")
    
    df = pd.read_csv(orders_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce")
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"], errors="coerce")
    df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"], errors="coerce")
    
    df["delivery_status"] = df["is_late"].map({True: "Late", False: "On Time"})
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    df["purchase_date"] = df["order_purchase_timestamp"].dt.date
    return df

st.title("Delivery Performance Analytics")
st.markdown("Dashboard interaktif untuk memantau keandalan pengiriman logistik, durasi pengiriman, serta tren performa wilayah.")
st.caption("Interactive dashboard | Dataset: Olist Brazilian E-Commerce")

try:
    data = load_data()
except Exception as e:
    st.error(str(e))
    st.stop()

if data.empty:
    st.warning("Tidak ada data pengiriman valid untuk dianalisis.")
    st.stop()

def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(color="#e2e8f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

# --------------------------------------------------
# 4. Sidebar Filters
# --------------------------------------------------
st.sidebar.title("Dashboard Filters")
st.sidebar.caption("Pilih periode dan wilayah untuk memperbarui seluruh analisis.")

min_date = data["purchase_date"].min()
max_date = data["purchase_date"].max()

st.sidebar.markdown("**1. Periode pesanan**")
date_range = st.sidebar.date_input(
    "Dari tanggal sampai tanggal", value=(min_date, max_date), min_value=min_date, max_value=max_date,
)

st.sidebar.markdown("**2. Wilayah pelanggan**")
state_names = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas", "BA": "Bahia",
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
    "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul", "MG": "Minas Gerais",
    "PA": "Pará", "PB": "Paraíba", "PR": "Paraná", "PE": "Pernambuco", "PI": "Piauí",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RS": "Rio Grande do Sul",
    "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina", "SP": "São Paulo",
    "SE": "Sergipe", "TO": "Tocantins",
}
states = sorted(data["customer_state"].dropna().unique())
state_options = ["Semua wilayah"] + [f"{code} — {state_names.get(code, code)}" for code in states]
selected_state = st.sidebar.selectbox("Pilih negara bagian di Brasil", options=state_options, index=0)
selected_state_code = selected_state.split(" — ")[0] if selected_state != "Semua wilayah" else None

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.info("Silakan pilih tanggal mulai dan tanggal akhir.")
    st.stop()

start_date, end_date = date_range
if start_date > end_date:
    st.error("Tanggal mulai harus sebelum tanggal akhir.")
    st.stop()

filtered = data[data["purchase_date"].between(start_date, end_date)].copy()
if selected_state_code is not None:
    filtered = filtered[filtered["customer_state"] == selected_state_code]

if filtered.empty:
    st.warning("Tidak ada pesanan valid pada filter ini.")
    st.stop()

# --------------------------------------------------
# 5. KPI Metrics (DENGAN IKON SVG PROFESIONAL)
# --------------------------------------------------
total = filtered["order_id"].nunique()
late_count = int(filtered["is_late"].sum())
on_time_count = total - late_count
on_time_rate = on_time_count / total * 100
late_rate = late_count / total * 100
avg_delivery = filtered["delivery_days"].mean()

# Kumpulan Ikon SVG (Feather Icons)
svg_box = """<svg viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>"""
svg_check = """<svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>"""
svg_alert = """<svg viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>"""
svg_clock = """<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>"""

kpis = [
    ("Total Deliveries", f"{total:,}", "Jumlah pesanan terkirim valid", svg_box),
    ("On-Time Rate", f"{on_time_rate:.2f}%", "Tiba pada atau sebelum estimasi", svg_check),
    ("Late Delivery Rate", f"{late_rate:.2f}%", "Tiba setelah tanggal estimasi", svg_alert),
    ("Average Delivery", f"{avg_delivery:.1f} Days", "Rata-rata waktu pengiriman", svg_clock),
]

cols = st.columns(4)
for col, (label, value, note, icon_svg) in zip(cols, kpis):
    with col:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-icon-box">{icon_svg}</div>
                </div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

# --------------------------------------------------
# 6. Dynamic Insights
# --------------------------------------------------
regional_insight = filtered.groupby("customer_state").agg(
    total=("order_id", "nunique"), late=("is_late", "sum")
).reset_index()
regional_insight["late_rate"] = regional_insight["late"] / regional_insight["total"] * 100
worst_state_row = regional_insight[regional_insight["total"] >= 50].sort_values("late_rate", ascending=False).head(1)

monthly_insight = filtered.groupby("order_month").agg(
    total=("order_id", "nunique"), late=("is_late", "sum")
).reset_index()
monthly_insight["late_rate"] = monthly_insight["late"] / monthly_insight["total"] * 100
worst_month_row = monthly_insight[monthly_insight["total"] >= 50].sort_values("late_rate", ascending=False).head(1)

if not worst_state_row.empty and not worst_month_row.empty:
    ws_state = worst_state_row.iloc[0]['customer_state']
    ws_rate = worst_state_row.iloc[0]['late_rate']
    wm_month = worst_month_row.iloc[0]['order_month']
    wm_rate = worst_month_row.iloc[0]['late_rate']
    
    st.info(f"💡 **Insight Cepat:** Wilayah dengan keterlambatan tertinggi saat ini adalah **{ws_state}** ({ws_rate:.1f}%). Bulan terburuk terjadi pada **{wm_month}** ({wm_rate:.1f}%).")

st.write("")

# --------------------------------------------------
# 7. Charts Section (Grid Layout)
# --------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Dampak Keterlambatan pada Ulasan")
    review_data = filtered.dropna(subset=['review_score']).copy()
    if not review_data.empty:
        fig_rev = px.box(review_data, x='delivery_status', y='review_score', color='delivery_status',
                         color_discrete_map={'On Time': '#2ecc71', 'Late': '#e74c3c'},
                         labels={'delivery_status': '', 'review_score': 'Skor Ulasan'})
        fig_rev.update_layout(showlegend=False)
        st.plotly_chart(style_chart(fig_rev), use_container_width=True)
    else:
        st.info("Data ulasan tidak tersedia untuk filter ini.")

with row1_col2:
    st.subheader("Monthly Delivery Performance")
    monthly = filtered.groupby("order_month").agg(
        total_orders=("order_id", "nunique"),
        late_orders=("is_late", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
    ).reset_index()
    monthly["late_rate_pct"] = monthly["late_orders"] / monthly["total_orders"] * 100
    monthly_chart_data = monthly[monthly["total_orders"] >= 100].copy()

    metric_choice = st.radio(
        "Pilih Metrik:", options=["Late Delivery Rate (%)", "Average Delivery Time (days)", "Total Deliveries"],
        horizontal=True, label_visibility="collapsed"
    )
    metric_config = {
        "Late Delivery Rate (%)": {"column": "late_rate_pct", "label": "Late Rate (%)", "color": "#60a5fa"},
        "Average Delivery Time (days)": {"column": "avg_delivery_days", "label": "Avg Days", "color": "#a78bfa"},
        "Total Deliveries": {"column": "total_orders", "label": "Deliveries", "color": "#34d399"},
    }
    config = metric_config[metric_choice]

    if not monthly_chart_data.empty:
        fig_monthly = px.line(
            monthly_chart_data, x="order_month", y=config["column"], markers=True,
            labels={"order_month": "Bulan", config["column"]: config["label"]},
            hover_data=["total_orders", "late_orders"],
        )
        fig_monthly.update_traces(line=dict(width=3, color=config["color"]), marker=dict(size=8))
        fig_monthly.update_layout(yaxis_rangemode="tozero", hovermode="x unified")
        st.plotly_chart(style_chart(fig_monthly), use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Belum ada bulan dengan minimal 100 pesanan.")

st.write("")

row2_col1, row2_col2 = st.columns([1.5, 1])

with row2_col1:
    st.subheader("Tingkat Keterlambatan per Wilayah")
    regional = filtered.groupby("customer_state").agg(
        total_orders=("order_id", "nunique"),
        late_orders=("is_late", "sum"),
    ).reset_index()
    regional["late_rate_pct"] = regional["late_orders"] / regional["total_orders"] * 100
    regional = regional[regional["total_orders"] >= 100].sort_values("late_rate_pct", ascending=False)

    if not regional.empty:
        fig_region = px.bar(
            regional, x="late_rate_pct", y="customer_state", orientation='h',
            labels={"customer_state": "", "late_rate_pct": "Late Rate (%)"},
            color="late_rate_pct", color_continuous_scale="Reds",
            hover_data=["total_orders", "late_orders"]
        )
        fig_region.update_layout(yaxis_rangemode="tozero", coloraxis_showscale=False)
        st.plotly_chart(style_chart(fig_region), use_container_width=True)
    else:
        st.info("Belum ada wilayah dengan minimal 100 pesanan.")

with row2_col2:
    st.subheader("Status Distribusi")
    status = filtered["delivery_status"].value_counts().rename_axis("status").reset_index(name="orders")
    fig_status = px.pie(
        status, names="status", values="orders", hole=0.65,
        color="status", color_discrete_map={'On Time': '#2ecc71', 'Late': '#e74c3c'}
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
    fig_status.update_layout(showlegend=False)
    st.plotly_chart(style_chart(fig_status), use_container_width=True)

# --------------------------------------------------
# 8. Detailed results & Audit (Expander Anda)
# --------------------------------------------------
with st.expander("📄 View monthly performance data"):
    st.dataframe(monthly.sort_values("order_month", ascending=False), use_container_width=True, hide_index=True)
    st.download_button("Download monthly results (CSV)", data=monthly.to_csv(index=False).encode("utf-8"), file_name="monthly_performance.csv", mime="text/csv")

with st.expander("📄 View regional performance data"):
    st.dataframe(regional.sort_values("late_rate_pct", ascending=False) if not regional.empty else pd.DataFrame(), use_container_width=True, hide_index=True)

st.divider()
with st.expander("🔍 Data Quality Audit — Pemeriksaan Akurasi"):
    duplicate_orders = int(data["order_id"].duplicated().sum())
    negative_delivery_days = int((data["delivery_days"] < 0).sum())
    
    audit_col1, audit_col2 = st.columns(2)
    audit_col1.metric("Valid Delivery Records", f"{len(data):,}")
    audit_col2.metric("Negative Delivery Durations", f"{negative_delivery_days:,}")
    
    if duplicate_orders == 0: st.success("Tidak ditemukan ID pesanan duplikat.")
    if negative_delivery_days == 0: st.success("Tidak ditemukan durasi pengiriman negatif.")

st.caption("Data source: Olist Brazilian E-Commerce Public Dataset. | Author: Chahyo Kumolo Nugroho")