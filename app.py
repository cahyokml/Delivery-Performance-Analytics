
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Delivery Performance Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"




st.markdown("""
<style>
    /* Main layout: follow the selected Streamlit theme */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Headings */
    h1, h2, h3 {
        color: var(--text-color);
        font-weight: 650;
    }

    h1 {
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    /* Sidebar: follow the theme */
    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid var(--border-color);
    }

    /* KPI cards: intentionally dark blue in both themes */
    .kpi-card {
        background: linear-gradient(135deg, #17365d, #24558a);
        padding: 22px 20px;
        border-radius: 14px;
        color: #ffffff;
        min-height: 125px;
        box-shadow: 0 4px 12px rgba(23, 54, 93, 0.10);
        margin-bottom: 10px;
    }

    .kpi-label {
        color: #d8e6f7;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 10px;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 29px;
        font-weight: 750;
        line-height: 1.2;
    }

    .kpi-note {
        color: #d8e6f7;
        font-size: 12px;
        margin-top: 9px;
    }

    /* Layout and separators */
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }

    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border-color: var(--border-color);
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-color);
        border-radius: 10px;
        overflow: hidden;
    }

    /* Download buttons */
    .stDownloadButton button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Charts */
    [data-testid="stPlotlyChart"] {
        border-radius: 12px;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Load and prepare data
# --------------------------------------------------
@st.cache_data
def load_data():
    orders_path = DATA_DIR / "olist_orders_dataset.csv"
    customers_path = DATA_DIR / "olist_customers_dataset.csv"

    if not orders_path.exists() or not customers_path.exists():
        raise FileNotFoundError(
            "Dataset tidak ditemukan di folder data/. "
            "Pastikan olist_orders_dataset.csv dan "
            "olist_customers_dataset.csv tersedia."
        )

    orders = pd.read_csv(orders_path)
    customers = pd.read_csv(customers_path)

    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        orders[column] = pd.to_datetime(
            orders[column], errors="coerce"
        )

    df = orders.merge(
        customers[["customer_id", "customer_state"]],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    # Only orders with actual and estimated delivery dates
    df = df.dropna(
        subset=[
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ).copy()

    df["delivery_days"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    df["is_late"] = (
        df["order_delivered_customer_date"]
        > df["order_estimated_delivery_date"]
    )

    df["delivery_status"] = df["is_late"].map(
        {True: "Late", False: "On Time"}
    )

    df["order_month"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    df["purchase_date"] = (
        df["order_purchase_timestamp"].dt.date
    )

    return df


st.title("📦 Delivery Performance Analytics")

st.markdown(
    """
    Monitor delivery reliability, shipping duration, and regional trends
    using historical Brazilian e-commerce order data.
    """
)

st.caption(
    "Interactive dashboard | Dataset: Olist Brazilian E-Commerce"

)

try:
    data = load_data()
except (FileNotFoundError, KeyError, ValueError) as error:
    st.error(str(error))
    st.stop()

if data.empty:
    st.warning("Tidak ada data pengiriman valid untuk dianalisis.")
    st.stop()


# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.title("Dashboard Filters")
st.sidebar.caption(
    "Pilih periode dan wilayah untuk memperbarui seluruh analisis."
)

min_date = data["purchase_date"].min()
max_date = data["purchase_date"].max()

st.sidebar.markdown("**1. Periode pesanan**")
date_range = st.sidebar.date_input(
    "Dari tanggal sampai tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Mengacu pada tanggal pesanan dibuat, bukan tanggal barang tiba.",
)


st.sidebar.markdown("**2. Wilayah pelanggan**")

# Kode wilayah dan nama negara bagian di Brasil
state_names = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins",
}

states = sorted(data["customer_state"].dropna().unique())

# Tampilkan nama lengkap, tetapi simpan kode aslinya
state_options = ["Semua wilayah"] + [
    f"{code} — {state_names.get(code, code)}"
    for code in states
]

selected_state = st.sidebar.selectbox(
    "Pilih negara bagian di Brasil",
    options=state_options,
    index=0,
    help=(
        "Pilih Semua wilayah untuk melihat seluruh data, "
        "atau pilih satu negara bagian untuk melihat performa pengirimannya."
    ),
)

if selected_state != "Semua wilayah":
    selected_state_code = selected_state.split(" — ")[0]
else:
    selected_state_code = None

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.info("Silakan pilih tanggal mulai dan tanggal akhir.")
    st.stop()

start_date, end_date = date_range

if start_date > end_date:
    st.error("Tanggal mulai harus sebelum tanggal akhir.")
    st.stop()

filtered = data[
    data["purchase_date"].between(start_date, end_date)
].copy()

if selected_state_code is not None:
    filtered = filtered[
        filtered["customer_state"] == selected_state_code
    ]

if filtered.empty:
    st.warning(
        "Tidak ada pesanan terkirim valid pada periode dan wilayah ini. "
        "Coba perluas periode atau pilih Semua wilayah."
    )
    st.stop()



# --------------------------------------------------
# KPI metrics
# --------------------------------------------------
st.subheader("Performance Overview")
st.caption(
    "Ringkasan performa berdasarkan periode dan wilayah "
    "yang kamu pilih."
)

total = filtered["order_id"].nunique()
late_count = int(filtered["is_late"].sum())
on_time_count = total - late_count

on_time_rate = on_time_count / total * 100
late_rate = late_count / total * 100
avg_delivery = filtered["delivery_days"].mean()

kpis = [
    (
        "Total Deliveries",
        f"{total:,}",
        "Jumlah pesanan terkirim valid",
    ),
    (
        "On-Time Rate",
        f"{on_time_rate:.2f}%",
        "Tiba pada atau sebelum estimasi",
    ),
    (
        "Late Delivery Rate",
        f"{late_rate:.2f}%",
        "Tiba setelah tanggal estimasi",
    ),
    (
        "Average Delivery Time",
        f"{avg_delivery:.1f} days",
        "Rata-rata dari pembelian ke pengiriman",
    ),
]

cols = st.columns(4)

for col, (label, value, note) in zip(cols, kpis):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# Monthly performance
# --------------------------------------------------
st.subheader("Monthly Delivery Performance")

monthly = (
    filtered.groupby("order_month")
    .agg(
        total_orders=("order_id", "nunique"),
        late_orders=("is_late", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
    )
    .reset_index()
)

monthly["late_rate_pct"] = (
    monthly["late_orders"] / monthly["total_orders"] * 100
)

monthly_chart_data = monthly[
    monthly["total_orders"] >= 100
].copy()

metric_choice = st.radio(
    "Tampilkan metrik",
    options=[
        "Late Delivery Rate (%)",
        "Average Delivery Time (days)",
        "Total Deliveries",
    ],
    horizontal=True,
)

metric_config = {
    "Late Delivery Rate (%)": {
        "column": "late_rate_pct",
        "label": "Late Delivery Rate (%)",
        "title": "Monthly Late Delivery Rate",
    },
    "Average Delivery Time (days)": {
        "column": "avg_delivery_days",
        "label": "Average Delivery Time (days)",
        "title": "Monthly Average Delivery Time",
    },
    "Total Deliveries": {
        "column": "total_orders",
        "label": "Total Deliveries",
        "title": "Monthly Delivery Volume",
    },
}

config = metric_config[metric_choice]

if not monthly_chart_data.empty:
    fig_monthly = px.line(
        monthly_chart_data,
        x="order_month",
        y=config["column"],
        markers=True,
        title=config["title"],
        labels={
            "order_month": "Purchase Month",
            config["column"]: config["label"],
        },
        hover_data=["total_orders", "late_orders"],
        template="plotly_white",
    )

    fig_monthly.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate=(
            "<b>%{x}</b><br>"
            + config["label"]
            + ": %{y:.2f}<br>"
            + "Total deliveries: %{customdata[0]:,}<br>"
            + "Late deliveries: %{customdata[1]:,}"
            + "<extra></extra>"
        ),
    )

    fig_monthly.update_layout(
        yaxis_rangemode="tozero",
        hovermode="x unified",
        margin=dict(l=15, r=15, t=60, b=15),
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
        config={"displayModeBar": True, "scrollZoom": True},
    )
else:
    st.info(
        "Belum ada bulan dengan minimal 100 pesanan. "
        "Ambang ini menjaga perbandingan bulanan tetap lebih representatif."
    )

# --------------------------------------------------
# Regional performance and delivery status
# --------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Regional Late Delivery Rate")

    regional = (
        filtered.groupby("customer_state")
        .agg(
            total_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
        )
        .reset_index()
    )

    regional["late_rate_pct"] = (
        regional["late_orders"] / regional["total_orders"] * 100
    )

    regional = regional[
        regional["total_orders"] >= 100
    ].sort_values("late_rate_pct", ascending=False)

    if not regional.empty:
        fig_region = px.bar(
            regional,
            x="customer_state",
            y="late_rate_pct",
            hover_data=["total_orders", "late_orders"],
            labels={
                "customer_state": "Customer State",
                "late_rate_pct": "Late Delivery Rate (%)",
            },
            title="States with at Least 100 Deliveries",
            template="plotly_white",
        )
        fig_region.update_layout(yaxis_rangemode="tozero")
        st.plotly_chart(fig_region, use_container_width=True)
    else:
        st.info(
            "Belum ada wilayah dengan minimal 100 pesanan "
            "pada filter ini."
        )

with right:
    st.subheader("Delivery Status Distribution")

    status = (
        filtered["delivery_status"]
        .value_counts()
        .rename_axis("status")
        .reset_index(name="orders")
    )

    fig_status = px.pie(
        status,
        names="status",
        values="orders",
        hole=0.55,
        title="On-Time vs. Late Deliveries",
        template="plotly_white",
    )
    st.plotly_chart(fig_status, use_container_width=True)

# --------------------------------------------------
# Detailed results
# --------------------------------------------------
with st.expander("View monthly performance data"):
    st.dataframe(
        monthly.sort_values("order_month", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download monthly results (CSV)",
        data=monthly.to_csv(index=False).encode("utf-8"),
        file_name="monthly_performance.csv",
        mime="text/csv",
    )

with st.expander("View regional performance data"):
    regional_all = (
        filtered.groupby("customer_state")
        .agg(
            total_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
        )
        .reset_index()
    )
    regional_all["late_rate_pct"] = (
        regional_all["late_orders"]
        / regional_all["total_orders"] * 100
    )

    st.dataframe(
        regional_all.sort_values(
            "late_rate_pct", ascending=False
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download regional results (CSV)",
        data=regional_all.to_csv(index=False).encode("utf-8"),
        file_name="regional_performance.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "Data source: Olist Brazilian E-Commerce Public Dataset. "
    "Late delivery is defined as actual delivery after the "
    "estimated delivery date."
)


# --------------------------------------------------
# Business Insights & Recommendations
# --------------------------------------------------
st.divider()
st.header("Business Insights & Recommendations")
st.caption(
    "Temuan otomatis berdasarkan periode dan wilayah "
    "yang sedang dipilih."
)

# Hitung performa dari data yang sudah difilter
total_orders = filtered["order_id"].nunique()
late_orders = int(filtered["is_late"].sum())
late_rate = late_orders / total_orders * 100
on_time_rate = 100 - late_rate

# Hitung performa per bulan
monthly_insights = (
    filtered.groupby("order_month")
    .agg(
        total_orders=("order_id", "nunique"),
        late_orders=("is_late", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
    )
    .reset_index()
)

monthly_insights["late_rate_pct"] = (
    monthly_insights["late_orders"]
    / monthly_insights["total_orders"]
    * 100
)

# Gunakan minimal 100 pesanan agar sampel lebih representatif
reliable_months = monthly_insights[
    monthly_insights["total_orders"] >= 100
]

# Hitung performa per wilayah
regional_insights = (
    filtered.groupby("customer_state")
    .agg(
        total_orders=("order_id", "nunique"),
        late_orders=("is_late", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
    )
    .reset_index()
)

regional_insights["late_rate_pct"] = (
    regional_insights["late_orders"]
    / regional_insights["total_orders"]
    * 100
)

reliable_regions = regional_insights[
    regional_insights["total_orders"] >= 100
]

# Ringkasan utama
col1, col2 = st.columns(2)

with col1:
    st.subheader("Overall Performance")
    st.metric("On-Time Delivery Rate", f"{on_time_rate:.2f}%")
    st.write(
        f"Dari {total_orders:,} pesanan terkirim valid, "
        f"{late_orders:,} pesanan terlambat "
        f"({late_rate:.2f}%)."
    )

    if late_rate > 0:
        st.info(
            "Masih terdapat pengiriman yang melewati estimasi. "
            "Tim operasional dapat mengevaluasi proses pengiriman "
            "dan pemantauan estimasi waktu tiba."
        )
    else:
        st.success(
            "Tidak ditemukan pengiriman terlambat pada data "
            "dan filter yang dipilih."
        )

with col2:
    st.subheader("Area to Investigate")

    if not reliable_months.empty:
        worst_month = reliable_months.loc[
            reliable_months["late_rate_pct"].idxmax()
        ]

        worst_month_name = pd.to_datetime(
            worst_month["order_month"]
            ).strftime("%B %Y")
        st.write(
            f"**Bulan dengan tingkat keterlambatan tertinggi:** "
            f"{worst_month_name}"
            )
        
        st.write(
            f"Tingkat keterlambatan "
            f"{worst_month['late_rate_pct']:.2f}% "
            f"dari {int(worst_month['total_orders']):,} pesanan."
        )
    else:
        st.write(
            "Belum ada bulan dengan minimal 100 pesanan "
            "pada filter yang dipilih."
        )

    if not reliable_regions.empty:
        worst_region = reliable_regions.loc[
            reliable_regions["late_rate_pct"].idxmax()
        ]

        st.write(
            f"**Wilayah dengan tingkat keterlambatan tertinggi:** "
            f"{worst_region['customer_state']}"
        )
        st.write(
            f"Tingkat keterlambatan "
            f"{worst_region['late_rate_pct']:.2f}% "
            f"dari {int(worst_region['total_orders']):,} pesanan."
        )
    else:
        st.write(
            "Belum ada wilayah dengan minimal 100 pesanan "
            "pada filter yang dipilih."
        )

st.subheader("Recommended Actions")

st.markdown(
    """
    1. **Investigasi periode bermasalah:** periksa apakah
       peningkatan keterlambatan terjadi bersamaan dengan
       lonjakan volume pesanan.

    2. **Evaluasi wilayah prioritas:** tinjau proses pengiriman
       pada wilayah dengan tingkat keterlambatan tinggi dan
       jumlah pesanan yang memadai.

    3. **Pantau performa secara berkala:** bandingkan tingkat
       keterlambatan dan rata-rata waktu pengiriman antarperiode.

    4. **Validasi penyebab sebelum mengambil keputusan:**
       dataset ini menunjukkan pola keterlambatan, tetapi
       tidak dengan sendirinya membuktikan penyebabnya.
    """
)


# --------------------------------------------------
# Data Quality Audit
# --------------------------------------------------
st.divider()

with st.expander("Data Quality Audit — Pemeriksaan Akurasi"):
    st.caption(
        "Pemeriksaan kualitas data untuk memastikan metrik "
        "dashboard dihitung dari data yang konsisten."
    )

    duplicate_orders = int(data["order_id"].duplicated().sum())
    negative_delivery_days = int(
        (data["delivery_days"] < 0).sum()
    )
    missing_customer_state = int(
        data["customer_state"].isna().sum()
    )
    missing_delivery_days = int(
        data["delivery_days"].isna().sum()
    )

    audit_col1, audit_col2 = st.columns(2)

    with audit_col1:
        st.metric("Valid Delivery Records", f"{len(data):,}")
        st.metric("Duplicate Order IDs", f"{duplicate_orders:,}")

    with audit_col2:
        st.metric(
            "Negative Delivery Durations",
            f"{negative_delivery_days:,}"
        )
        st.metric(
            "Missing Customer State",
            f"{missing_customer_state:,}"
        )

    if duplicate_orders == 0:
        st.success("Tidak ditemukan ID pesanan duplikat.")
    else:
        st.warning(
            "Terdapat ID pesanan duplikat. Periksa sebelum "
            "menggunakan jumlah baris sebagai jumlah pesanan."
        )

    if negative_delivery_days == 0:
        st.success("Tidak ditemukan durasi pengiriman negatif.")
    else:
        st.warning(
            "Terdapat durasi pengiriman negatif. Periksa urutan "
            "tanggal pembelian dan tanggal barang diterima."
        )

    if missing_customer_state == 0:
        st.success("Semua pesanan memiliki informasi wilayah pelanggan.")
    else:
        st.warning(
            "Sebagian pesanan tidak memiliki informasi wilayah pelanggan."
        )

    if missing_delivery_days > 0:
        st.warning(
            "Ada nilai durasi pengiriman yang kosong meskipun "
            "tanggal pengiriman sudah difilter. Periksa data sumber."
        )

    st.caption(
        "Catatan: pemeriksaan ini menggunakan data valid yang telah "
        "dibersihkan oleh fungsi load_data(). Audit ini belum menghitung "
        "jumlah pesanan yang dikeluarkan karena tanggal tidak lengkap."
    )
    

# --------------------------------------------------
# Delivery Date Completeness Audit
# --------------------------------------------------
with st.expander("Delivery Date Completeness Audit"):
    orders_path = DATA_DIR / "olist_orders_dataset.csv"
    raw_orders = pd.read_csv(orders_path)

    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    # Convert dates using the same logic as the main analysis
    for column in date_columns:
        raw_orders[column] = pd.to_datetime(
            raw_orders[column], errors="coerce"
        )

    # Count missing or invalid dates after conversion
    missing_by_column = raw_orders[date_columns].isna().sum()

    total_raw_orders = len(raw_orders)
    valid_date_mask = raw_orders[date_columns].notna().all(axis=1)
    valid_date_orders = int(valid_date_mask.sum())
    excluded_orders = total_raw_orders - valid_date_orders

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Source Orders", f"{total_raw_orders:,}")
    col2.metric("Orders with Complete Dates", f"{valid_date_orders:,}")
    col3.metric("Orders Excluded", f"{excluded_orders:,}")

    missing_table = (
        missing_by_column.rename("Missing or Invalid Values")
        .rename_axis("Date Column")
        .reset_index()
    )

    st.write("Missing or invalid values by date column")
    st.dataframe(
        missing_table,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Pesanan dikeluarkan jika salah satu dari tiga tanggal "
        "yang diperlukan kosong atau gagal dikonversi menjadi tanggal."
    )


# --------------------------------------------------
# Delivery Status Consistency Audit
# --------------------------------------------------
with st.expander("Delivery Status Consistency Audit"):
    total_orders = filtered["order_id"].nunique()

    late_orders = filtered.loc[
        filtered["is_late"] == True, "order_id"
    ].nunique()

    on_time_orders = filtered.loc[
        filtered["is_late"] == False, "order_id"
    ].nunique()

    missing_status = int(filtered["is_late"].isna().sum())

    classified_orders = late_orders + on_time_orders
    unclassified_orders = total_orders - classified_orders

    late_rate = (
        late_orders / total_orders * 100
        if total_orders > 0 else 0
    )

    on_time_rate = (
        on_time_orders / total_orders * 100
        if total_orders > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Late Orders", f"{late_orders:,}")
    col3.metric("On-Time Orders", f"{on_time_orders:,}")

    st.write(f"Late Rate: {late_rate:.2f}%")
    st.write(f"On-Time Rate: {on_time_rate:.2f}%")
    st.write(f"Unclassified Orders: {unclassified_orders:,}")
    st.write(f"Missing Status Values: {missing_status:,}")

    if (
        classified_orders == total_orders
        and missing_status == 0
        and abs(late_rate + on_time_rate - 100) < 0.01
    ):
        st.success(
            "Audit passed: all orders have a consistent delivery status."
        )
    else:
        st.warning(
            "Audit requires review: check missing statuses or order counts."
        )


# --------------------------------------------------
# Delivery Duration and Date Logic Audit
# --------------------------------------------------
with st.expander("Delivery Duration and Date Logic Audit"):
    audit_data = filtered.copy()

    negative_duration = int(
        (audit_data["delivery_days"] < 0).sum()
    )

    zero_duration = int(
        (audit_data["delivery_days"] == 0).sum()
    )

    estimated_before_purchase = int(
        (
            audit_data["order_estimated_delivery_date"]
            < audit_data["order_purchase_timestamp"]
        ).sum()
    )

    actual_after_estimated = int(
        (
            audit_data["order_delivered_customer_date"]
            > audit_data["order_estimated_delivery_date"]
        ).sum()
    )

    col1, col2 = st.columns(2)
    col1.metric("Negative Delivery Durations", f"{negative_duration:,}")
    col2.metric("Zero-Day Deliveries", f"{zero_duration:,}")

    col3, col4 = st.columns(2)
    col3.metric(
        "Estimated Before Purchase",
        f"{estimated_before_purchase:,}"
    )
    col4.metric(
        "Delivered After Estimate",
        f"{actual_after_estimated:,}"
    )

    if negative_duration == 0 and estimated_before_purchase == 0:
        st.success(
            "Date logic check passed: no negative durations or "
            "estimates before purchase were found."
        )
    else:
        st.warning(
            "Date logic check requires review. Inspect the flagged records."
        )

    st.caption(
        "Delivery duration measures the time from purchase to actual "
        "customer delivery. Zero-day deliveries are reported separately "
        "and are not automatically considered errors."
    )

# --------------------------------------------------
# Monthly Aggregation Consistency Audit
# --------------------------------------------------
with st.expander("Monthly Aggregation Consistency Audit"):
    audit_data = filtered.copy()

    monthly_audit = (
        audit_data.groupby("order_month")
        .agg(
            total_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
        )
        .reset_index()
    )

    monthly_audit["on_time_orders"] = (
        monthly_audit["total_orders"] - monthly_audit["late_orders"]
    )

    monthly_audit["late_rate_pct"] = (
        monthly_audit["late_orders"]
        / monthly_audit["total_orders"]
        * 100
    )

    monthly_total = int(monthly_audit["total_orders"].sum())
    monthly_late_total = int(monthly_audit["late_orders"].sum())
    source_total = int(audit_data["order_id"].nunique())
    source_late_total = int(
        audit_data.loc[audit_data["is_late"], "order_id"].nunique()
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Orders in Monthly Groups", f"{monthly_total:,}")
    col2.metric("Filtered Orders", f"{source_total:,}")
    col3.metric("Late Orders in Monthly Groups", f"{monthly_late_total:,}")

    if (
        monthly_total == source_total
        and monthly_late_total == source_late_total
    ):
        st.success(
            "Audit passed: monthly groups preserve all filtered orders "
            "and late orders."
        )
    else:
        st.warning(
            "Audit requires review: monthly totals do not match "
            "the filtered dataset."
        )

    st.dataframe(
        monthly_audit,
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# Regional Aggregation Consistency Audit
# --------------------------------------------------
with st.expander("Regional Aggregation Consistency Audit"):
    audit_data = filtered.copy()

    regional_audit = (
        audit_data.groupby("customer_state")
        .agg(
            total_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum"),
        )
        .reset_index()
    )

    regional_audit["on_time_orders"] = (
        regional_audit["total_orders"] - regional_audit["late_orders"]
    )

    regional_total = int(regional_audit["total_orders"].sum())
    regional_late_total = int(regional_audit["late_orders"].sum())

    source_total = int(audit_data["order_id"].nunique())
    source_late_total = int(
        audit_data.loc[audit_data["is_late"], "order_id"].nunique()
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Orders in Regional Groups", f"{regional_total:,}")
    col2.metric("Filtered Orders", f"{source_total:,}")
    col3.metric("Late Orders in Regional Groups", f"{regional_late_total:,}")

    if (
        regional_total == source_total
        and regional_late_total == source_late_total
    ):
        st.success(
            "Audit passed: regional groups preserve all filtered orders "
            "and late orders."
        )
    else:
        st.warning(
            "Audit requires review: regional totals do not match "
            "the filtered dataset."
        )

    st.dataframe(
        regional_audit.sort_values(
            "total_orders", ascending=False
        ),
        use_container_width=True,
        hide_index=True,
    )




