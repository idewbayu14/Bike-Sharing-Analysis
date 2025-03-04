import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load Data
df = pd.read_csv('dashboard/bike_sharing_analysis.csv')

# Convert date column
df['dteday'] = pd.to_datetime(df['dteday'])

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
date_range = st.sidebar.date_input("Pilih Rentang Waktu", [df['dteday'].min(), df['dteday'].max()])
weather_filter = st.sidebar.multiselect("Pilih Cuaca", df['weathersit'].unique(), default=df['weathersit'].unique())
workingday_filter = st.sidebar.radio("Hari Kerja atau Libur?", ['Semua', 'Hari Kerja', 'Hari Libur'])

# Penjelasan kondisi cuaca
st.sidebar.markdown("### 🌦️ Kategori Kondisi Cuaca:")
st.sidebar.markdown("☀️ 1 - Cerah / Sebagian Berawan")
st.sidebar.markdown("☁️ 2 - Berawan / Berkabut")
st.sidebar.markdown("🌧️❄️ 3 - Hujan Ringan / Salju Ringan")

# Filter Data
df_filtered = df[(df['dteday'] >= pd.Timestamp(date_range[0])) & (df['dteday'] <= pd.Timestamp(date_range[1]))]
df_filtered = df_filtered[df_filtered['weathersit'].isin(weather_filter)]
if workingday_filter == 'Hari Kerja':
    df_filtered = df_filtered[df_filtered['workingday'] == 1]
elif workingday_filter == 'Hari Libur':
    df_filtered = df_filtered[df_filtered['workingday'] == 0]

# Dashboard Title
st.title("🚴‍♂️ Dashboard Analisis Penyewaan Sepeda")

# 1. Pengaruh Cuaca & Suhu terhadap Penyewaan Sepeda
st.subheader("1. 🌤️ Pengaruh Cuaca & Suhu terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x=df_filtered['temp'], y=df_filtered['cnt'], hue=df_filtered['weathersit'], palette='coolwarm', s=60, ax=ax)
ax.set_xlabel("Suhu (Normalisasi)")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)
st.markdown("📉 Hubungan antara suhu dan jumlah penyewaan sepeda, dengan warna yang berbeda untuk kondisi cuaca yang berbeda. Dari grafik ini, kita dapat melihat bahwa saat suhu lebih tinggi (lebih panas), jumlah penyewaan sepeda cenderung meningkat. Namun, kondisi cuaca juga sangat mempengaruhi: pada cuaca cerah (warna hijau muda), jumlah penyewaan lebih tinggi, sementara pada cuaca buruk seperti hujan atau salju (warna lebih gelap), jumlah penyewaan cenderung lebih rendah.")


# 2. Pengaruh Hari Kerja/Libur
st.subheader("2. 📅 Pengaruh Hari Kerja atau Libur")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x=df_filtered['workingday'], y=df_filtered['cnt'], palette='Set2', ax=ax)
ax.set_xlabel("Hari Kerja (1 = Ya, 0 = Tidak)")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)
st.markdown("🚴‍♂️ Distribusi jumlah penyewaan sepeda pada hari kerja dan hari libur. Sumbu X menunjukkan apakah hari tersebut adalah hari kerja (1) atau hari libur (0), sementara sumbu Y menunjukkan jumlah penyewaan sepeda. Dari visualisasi ini, kita dapat melihat bahwa jumlah penyewaan sepeda pada hari kerja lebih tinggi dibandingkan dengan hari libur. Hal ini menunjukkan bahwa sepeda lebih banyak digunakan untuk aktivitas sehari-hari seperti pergi bekerja.")

# 3. RFM Analysis
st.subheader("3. 📊 RFM Analysis")
max_date = df_filtered['dteday'].max()
df_filtered['Recency'] = (max_date - df_filtered['dteday']).dt.days
df_filtered['Frequency'] = df_filtered['cnt']
df_filtered['Monetary'] = df_filtered['registered']
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(df_filtered['Recency'], bins=30, kde=True, ax=axes[0]).set(title='Distribusi Recency')
sns.histplot(df_filtered['Frequency'], bins=30, kde=True, ax=axes[1]).set(title='Distribusi Frequency')
sns.histplot(df_filtered['Monetary'], bins=30, kde=True, ax=axes[2]).set(title='Distribusi Monetary')
st.pyplot(fig)
st.markdown("📊 Analisis RFM membantu memahami perilaku pengguna berdasarkan Recency (seberapa baru mereka menyewa), Frequency (seberapa sering mereka menyewa), dan Monetary (berapa banyak sepeda yang mereka daftarkan). Dari histogram ini, kita bisa melihat bagaimana pengguna berinteraksi dengan layanan penyewaan sepeda.")

# 4. Clustering Analysis
st.subheader("4. 🔍 Clustering Analysis (K-Means)")
features = df_filtered[['temp', 'hum', 'windspeed', 'cnt']]
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_filtered['Cluster'] = kmeans.fit_predict(features_scaled)
fig, ax = plt.subplots(figsize=(8,6))
sns.scatterplot(x=df_filtered['temp'], y=df_filtered['cnt'], hue=df_filtered['Cluster'], palette='viridis', ax=ax)
ax.set_xlabel("Temperature")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)
st.markdown("🔍 Analisis klaster menggunakan K-Means mengelompokkan data penyewaan sepeda ke dalam tiga kelompok berdasarkan suhu, kelembaban, kecepatan angin, dan jumlah penyewaan. Dari grafik ini, kita dapat melihat pola penggunaan yang berbeda di setiap kelompok.")

# 5. Time Series Analysis
st.subheader("5. 📈 Analisis Tren Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(x=df_filtered['dteday'], y=df_filtered['cnt'], label='Total Rentals', ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel("Number of Rentals")
plt.xticks(rotation=45)
st.pyplot(fig)
st.markdown("📈 Analisis tren penyewaan sepeda menunjukkan bagaimana jumlah penyewaan berubah seiring waktu. Dari grafik ini, kita bisa melihat apakah ada pola musiman atau tren kenaikan/penurunan dalam jumlah penyewaan sepeda.")

st.caption('© idewbayu 2025 🚀')
