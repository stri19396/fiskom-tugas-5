import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Analisis Siswa", layout="wide")

st.title("📊 Dashboard Analisis Data 50 Siswa - 20 Soal")

# Upload file
uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 Data Mentah")
    st.dataframe(df)

    # Hitung total skor siswa
    df["Total_Skor"] = df.sum(axis=1)

    # =========================
    # Statistik Deskriptif
    # =========================
    st.subheader("📊 Statistik Deskriptif")
    st.write(df.describe())

    # =========================
    # Histogram Total Skor
    # =========================
    st.subheader("📈 Histogram Total Skor Siswa")
    fig_hist = px.histogram(df, x="Total_Skor", nbins=10, title="Distribusi Total Skor")
    st.plotly_chart(fig_hist, use_container_width=True)

    # =========================
    # Rata-rata per Soal
    # =========================
    st.subheader("📊 Rata-rata Skor Tiap Soal")

    mean_per_question = df.drop(columns=["Total_Skor"]).mean().reset_index()
    mean_per_question.columns = ["Soal", "Rata-rata"]

    fig_bar = px.bar(mean_per_question,
                     x="Soal",
                     y="Rata-rata",
                     title="Rata-rata Skor Tiap Soal")
    st.plotly_chart(fig_bar, use_container_width=True)

    # =========================
    # Boxplot Distribusi
    # =========================
    st.subheader("📦 Boxplot Distribusi Skor Tiap Soal")

    df_melt = df.drop(columns=["Total_Skor"]).melt(var_name="Soal", value_name="Skor")
    fig_box = px.box(df_melt, x="Soal", y="Skor", title="Distribusi Skor Tiap Soal")
    st.plotly_chart(fig_box, use_container_width=True)

    # =========================
    # Heatmap Korelasi
    # =========================
    st.subheader("🔥 Heatmap Korelasi Antar Soal")

    corr = df.drop(columns=["Total_Skor"]).corr()

    fig_heatmap = px.imshow(corr,
                            text_auto=True,
                            aspect="auto",
                            title="Korelasi Antar Soal")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # =========================
    # Radar Chart Rata-rata
    # =========================
    st.subheader("🎯 Radar Chart Rata-rata Skor")

    categories = mean_per_question["Soal"].tolist()
    values = mean_per_question["Rata-rata"].tolist()

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Rata-rata'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=False,
        title="Radar Chart Rata-rata Skor Tiap Soal"
    )

    st.plotly_chart(fig_radar, use_container_width=True)

else:
    st.info("Silakan upload file Excel terlebih dahulu.")