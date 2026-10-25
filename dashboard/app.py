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
# 2. CUSTOM CSS (Dark Mode, Elegant, Responsive)
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
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* KPI CARDS MODERN */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 15px;
        position: relative;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        border-color: rgba(96, 165, 250, 0.5);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 8px;
    }
    .kpi-icon-box {
        background: rgba(96, 165, 250, 0.1);
        border-radius: 10px;
        padding: 6px;
    }
    .kpi-icon-box svg {
        width: 18px; height: 18px; stroke: #60a5fa; stroke-width: 2; fill: none;
    }
    .kpi-label {
        color: #94a3b8; font-size: 13px; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 2rem; font-weight: 700; color: #f8fafc; line-height: 1.2;
    }
    .kpi-context {
        color: #cbd5e1; font-size: 12px; margin-top: 6px; font-weight: 500;
    }

    /* Text & UI Fixes */
    h1, h2, h3 { color: #f8fafc !important; font-weight: 650; }
    hr { margin-top: 1rem; margin-bottom: 1.5rem; border-color: rgba(255, 255, 255, 0.1); }
    [data-testid="stPlotlyChart"] { background: transparent; }
    
    /* Insight Box */
    .insight-box {
        background: rgba(96, 165, 250, 0.1);
        border-left: 4px solid #60a5fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }    /* Filter Badge Modern */
    .filter-badge {
        display: inline-block;
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    .filter-badge strong {
        color: #f8fafc;
    }
    
    /* Responsive KPI */
    @media (max-width: 768px) {
        .kpi-value { font-size: 1.5rem; }
    }
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

# --------------------------------------------------
# 4. Sidebar Filters (Dengan Fitur Reset)
# --------------------------------------------------
st.sidebar.title("Filter Data")

min_date = data["purchase_date"].min()
max_date = data["purchase_date"].max()

if "date_range" not in st.session_state:
    st.session_state.date_range = (min_date, max_date)
if "selected_state" not in st.session_state:
    st.session_state.selected_state = "Semua wilayah"

def reset_filters():
    st.session_state.date_range = (min_date, max_date)
    st.session_state.selected_state = "Semua wilayah"

st.sidebar.button("🔄 Reset Filter", on_click=reset_filters, use_container_width=True)

st.sidebar.markdown("**1. Periode pesanan**")
date_range = st.sidebar.date_input(
    "Dari tanggal sampai tanggal", key="date_range", min_value=min_date, max_value=max_date,
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
selected_state = st.sidebar.selectbox("Pilih negara bagian", options=state_options, key="selected_state")

# Logika Filter
if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.info("Silakan pilih tanggal mulai dan tanggal akhir.")
    st.stop()

start_date, end_date = date_range
if start_date > end_date:
    st.error("Tanggal mulai harus sebelum tanggal akhir.")
    st.stop()

filtered = data[data["purchase_date"].between(start_date, end_date)].copy()
selected_state_code = selected_state.split(" — ")[0] if selected_state != "Semua wilayah" else None
if selected_state_code is not None:
    filtered = filtered[filtered["customer_state"] == selected_state_code]

# --------------------------------------------------
# 5. Header & Filter Info (Sesuai Rekomendasi Reviewer)
# --------------------------------------------------
date_str = f"{start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}"
st.markdown(
    f'<div class="filter-badge"> <strong>Periode:</strong> {date_str} &nbsp;&nbsp;|&nbsp;&nbsp;  <strong>Wilayah:</strong> {selected_state}</div>', 
    unsafe_allow_html=True
)

if filtered.empty:
    st.warning("⚠️ Tidak ada pesanan valid pada periode dan wilayah ini. Silakan ubah filter atau klik 'Reset Filter'.")
    st.stop()

# --------------------------------------------------
# 6. KPI Metrics (Dengan Konteks Angka)
# --------------------------------------------------
total = filtered["order_id"].nunique()
late_count = int(filtered["is_late"].sum())
on_time_count = total - late_count
on_time_rate = on_time_count / total * 100
late_rate = late_count / total * 100
avg_delivery = filtered["delivery_days"].mean()

svg_box = """<svg viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>"""
svg_check = """<svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>"""
svg_alert = """<svg viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>"""
svg_clock = """<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>"""

kpis = [
    ("Total Deliveries", f"{total:,}", f"{on_time_count:,} tepat waktu | {late_count:,} terlambat", svg_box),
    ("On-Time Rate", f"{on_time_rate:.2f}%", f"Dari {total:,} pesanan", svg_check),
    ("Late Delivery Rate", f"{late_rate:.2f}%", f"{late_count:,} pesanan terlambat", svg_alert),
    ("Average Delivery", f"{avg_delivery:.1f} Hari", "Rata-rata waktu pengiriman", svg_clock),
]

cols = st.columns(4)
for col, (label, value, context, icon_svg) in zip(cols, kpis):
    with col:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-icon-box">{icon_svg}</div>
                </div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-context">{context}</div>
            </div>
            """, unsafe_allow_html=True)

st.write("")

# --------------------------------------------------
# 7. Dynamic Insights
# --------------------------------------------------
reg_insight = filtered.groupby("customer_state").agg(total=("order_id", "nunique"), late=("is_late", "sum")).reset_index()
reg_insight["rate"] = reg_insight["late"] / reg_insight["total"] * 100
worst_state = reg_insight[reg_insight["total"] >= 50].sort_values("rate", ascending=False).head(1)

mon_insight = filtered.groupby("order_month").agg(total=("order_id", "nunique"), late=("is_late", "sum")).reset_index()
mon_insight["rate"] = mon_insight["late"] / mon_insight["total"] * 100
worst_month = mon_insight[mon_insight["total"] >= 50].sort_values("rate", ascending=False).head(1)

review_insight = filtered.groupby("delivery_status")["review_score"].mean()

# --- PERUBAHAN DI SINI: Gunakan tag <strong> bukan ** ---
insight_text = "<strong>Ringkasan Insight:</strong> "
if not worst_state.empty:
    insight_text += f"Wilayah dengan keterlambatan tertinggi adalah <strong>{worst_state.iloc[0]['customer_state']}</strong> ({worst_state.iloc[0]['rate']:.1f}%). "
if not worst_month.empty:
    insight_text += f"Bulan terburuk terjadi pada <strong>{worst_month.iloc[0]['order_month']}</strong> ({worst_month.iloc[0]['rate']:.1f}%). "
if "Late" in review_insight and "On Time" in review_insight:
    diff = review_insight["On Time"] - review_insight["Late"]
    insight_text += f"Pesanan terlambat memiliki rata-rata ulasan {diff:.2f} poin lebih rendah."

st.markdown(f'<div class="insight-box">{insight_text}</div>', unsafe_allow_html=True)

# --------------------------------------------------
# 8. Charts Section (Mempertahankan Fitur Radio & Tabs)
# --------------------------------------------------
def style_chart(fig):
    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=40, b=10), font=dict(color="#e2e8f0"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("Dampak Keterlambatan pada Ulasan")
    review_data = filtered.dropna(subset=['review_score']).copy()
    if not review_data.empty:
        fig_rev = px.box(
            review_data, x='delivery_status', y='review_score', color='delivery_status',
            color_discrete_map={'On Time': '#2ecc71', 'Late': '#e74c3c'},
            labels={'delivery_status': 'Status Pengiriman', 'review_score': 'Skor Ulasan'}
        )
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
        "Tampilkan metrik", options=["Late Delivery Rate (%)", "Average Delivery Time (days)", "Total Deliveries"],
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
            labels={"order_month": "Bulan", config["column"]: config["label"], "total_orders": "Total Pesanan", "late_orders": "Pesanan Terlambat"},
        )
        fig_monthly.update_traces(line=dict(width=3, color=config["color"]), marker=dict(size=8))
        fig_monthly.update_layout(yaxis_rangemode="tozero", hovermode="x unified")
        fig_monthly.update_xaxes(tickformat="%Y-%b") # Memperbaiki format bulan
        st.plotly_chart(style_chart(fig_monthly), use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Belum ada bulan dengan minimal 100 pesanan.")

st.write("")

row2_col1, row2_col2 = st.columns([1.5, 1])

with row2_col1:
    st.subheader("Regional Late Delivery Rate")
    regional = filtered.groupby("customer_state").agg(
        total_orders=("order_id", "nunique"), late_orders=("is_late", "sum"),
    ).reset_index()
    regional["late_rate_pct"] = regional["late_orders"] / regional["total_orders"] * 100
    # Mengurutkan berdasarkan keterlambatan tertinggi
    regional = regional[regional["total_orders"] >= 100].sort_values("late_rate_pct", ascending=False)

    if not regional.empty:
        fig_region = px.bar(
            regional, x="late_rate_pct", y="customer_state", orientation='h',
            labels={"customer_state": "Negara Bagian", "late_rate_pct": "Late Rate (%)", "total_orders": "Total Pesanan", "late_orders": "Terlambat"},
            color="late_rate_pct", color_continuous_scale="Reds"
        )
        fig_region.update_layout(yaxis_rangemode="tozero", coloraxis_showscale=False)
        fig_region.update_yaxes(categoryorder='total ascending') # Tertinggi di atas
        st.plotly_chart(style_chart(fig_region), use_container_width=True)
    else:
        st.info("Belum ada wilayah dengan minimal 100 pesanan.")

with row2_col2:
    st.subheader("Delivery Status Distribution")
    status = filtered["delivery_status"].value_counts().rename_axis("status").reset_index(name="orders")
    fig_status = px.pie(
        status, names="status", values="orders", hole=0.65,
        color="status", color_discrete_map={'On Time': '#2ecc71', 'Late': '#e74c3c'}
    )
    fig_status.update_traces(textposition='inside', textinfo='percent+label')
    fig_status.update_layout(showlegend=False)
    st.plotly_chart(style_chart(fig_status), use_container_width=True)

# --------------------------------------------------
# 9. Detailed results & Audit (Expander Asli Anda)
# --------------------------------------------------
with st.expander("📄 View monthly performance data"):
    st.dataframe(monthly.sort_values("order_month", ascending=False), use_container_width=True, hide_index=True)
    st.download_button("Download monthly results (CSV)", data=monthly.to_csv(index=False).encode("utf-8"), file_name="monthly_performance.csv", mime="text/csv")

with st.expander("📄 View regional performance data"):
    st.dataframe(regional.sort_values("late_rate_pct", ascending=False) if not regional.empty else pd.DataFrame(), use_container_width=True, hide_index=True)
    st.download_button("Download regional results (CSV)", data=regional.to_csv(index=False).encode("utf-8"), file_name="regional_performance.csv", mime="text/csv")

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