import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
@st.cache_data
def load_data():
    all_data = pd.read_csv('dashboard/all_data.csv')
    return all_data

all_data = load_data()

# Sidebar
st.sidebar.title("🏷️ Filter Data")
day_filter = st.sidebar.multiselect("📌 Pilih Hari Kerja / Libur", all_data['workingday'].unique(), default=all_data['workingday'].unique())
weather_filter = st.sidebar.multiselect("🌤️ Pilih Kondisi Cuaca", all_data['weathersit'].unique(), default=all_data['weathersit'].unique())

# Penjelasan kondisi cuaca
st.sidebar.markdown("### 🌦️ Kategori Kondisi Cuaca:")
st.sidebar.markdown("☀️ 1 - Cerah / Sebagian Berawan")
st.sidebar.markdown("☁️ 2 - Berawan / Berkabut")
st.sidebar.markdown("🌧️❄️ 3 - Hujan Ringan / Salju Ringan")
st.sidebar.markdown("⛈️❄️ 4 - Hujan Deras / Salju Lebat / Badai")

# Filter data
filtered_df = all_data[(all_data['workingday'].isin(day_filter)) & (all_data['weathersit'].isin(weather_filter))]

# Pastikan kolom 'Cluster' ada dalam dataset sebelum digunakan
if 'Cluster' not in filtered_df.columns:
    st.warning("⚠️ Kolom 'Cluster' tidak ditemukan dalam dataset. Pastikan sudah melakukan clustering sebelumnya.")
else:
    # Judul Dashboard
    st.title("📊 Dashboard Analisis Penyewaan Sepeda")
    st.markdown("---")

    # Visualisasi 1: Pengaruh Cuaca dan Suhu terhadap Penyewaan Sepeda
    st.subheader("🔥 Pengaruh Cuaca dan Suhu terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12,6))
    sns.scatterplot(x=filtered_df['temp'], y=filtered_df['cnt'], hue=filtered_df['weathersit'], palette='coolwarm', s=60, ax=ax)
    ax.set_title('Pengaruh Cuaca dan Suhu terhadap Penyewaan Sepeda per Jam')
    ax.set_xlabel('Suhu (Normalisasi)')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig)
    st.markdown("📉 Hubungan antara suhu dan jumlah penyewaan sepeda, dengan warna yang berbeda untuk kondisi cuaca yang berbeda. Dari grafik ini, kita dapat melihat bahwa saat suhu lebih tinggi (lebih panas), jumlah penyewaan sepeda cenderung meningkat. Namun, kondisi cuaca juga sangat mempengaruhi: pada cuaca cerah (warna hijau muda), jumlah penyewaan lebih tinggi, sementara pada cuaca buruk seperti hujan atau salju (warna lebih gelap), jumlah penyewaan cenderung lebih rendah.")

    # Visualisasi 2: Pengaruh Hari Kerja dan Libur terhadap Penyewaan Sepeda
    st.subheader("🏢 Pengaruh Hari Kerja dan Libur terhadap Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(x=filtered_df['workingday'], y=filtered_df['cnt'], palette='Set2', ax=ax)
    ax.set_title('Penyewaan Sepeda per Hari Berdasarkan Hari Kerja dan Libur')
    ax.set_xlabel('Hari Kerja (1 = Ya, 0 = Tidak)')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    st.pyplot(fig)
    st.markdown("🚴‍♂️ Distribusi jumlah penyewaan sepeda pada hari kerja dan hari libur. Sumbu X menunjukkan apakah hari tersebut adalah hari kerja (1) atau hari libur (0), sementara sumbu Y menunjukkan jumlah penyewaan sepeda. Dari visualisasi ini, kita dapat melihat bahwa jumlah penyewaan sepeda pada hari kerja lebih tinggi dibandingkan dengan hari libur. Hal ini menunjukkan bahwa sepeda lebih banyak digunakan untuk aktivitas sehari-hari seperti pergi bekerja.")

    # Pastikan kolom tanggal dikonversi dengan benar
    filtered_df['dteday'] = pd.to_datetime(filtered_df['dteday'], format="%Y-%m-%d", errors='coerce')

    # Visualisasi 3: Tren Penyewaan Sepeda Seiring Waktu
    st.subheader("📈 Tren Penyewaan Sepeda Seiring Waktu")
    fig, ax = plt.subplots(figsize=(12,6))
    sns.lineplot(x=pd.to_datetime(filtered_df['dteday']), y=filtered_df['cnt'], ax=ax)
    ax.set_title('Tren Penyewaan Sepeda dari Waktu ke Waktu')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.markdown("📊 Dari tren ini, kita bisa melihat pola musiman dalam penggunaan sepeda. Terdapat kenaikan pada periode tertentu, yang dapat menunjukkan musim ramai penyewaan.")

    # Visualisasi 4: Cluster Analisis dengan K-Means (jika kolom 'Cluster' ada)
    if 'Cluster' in filtered_df.columns:
        st.subheader("🎯 Segmentasi Pengguna Berdasarkan Cuaca dan Jumlah Penyewaan")
        fig, ax = plt.subplots(figsize=(8,6))
        sns.scatterplot(x=filtered_df['temp'], y=filtered_df['cnt'], hue=filtered_df['Cluster'], palette='viridis', ax=ax)
        ax.set_xlabel('Temperature')
        ax.set_ylabel('Total Rentals')
        ax.set_title('Clustering Based on Temperature and Rentals')
        st.pyplot(fig)
        st.markdown("📌 Segmentasi ini membantu mengelompokkan pola penggunaan sepeda berdasarkan cuaca. Hal ini berguna untuk menyesuaikan strategi layanan penyewaan berdasarkan kondisi lingkungan.")

    st.markdown("---")
    st.write("🚴‍♂️ Dashboard ini bertujuan untuk memberikan wawasan tentang pola penggunaan sepeda berdasarkan faktor cuaca, hari kerja, serta tren musiman...")

st.caption('© idewbayu 2025 🚀')
