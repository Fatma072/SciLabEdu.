import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Konfigurasi halaman
st.set_page_config(page_title="SciLabEdu", layout="wide")

# Tambahan latar belakang dengan tema kimia
# Fungsi untuk mengatur background berbeda tiap menu
def set_background(menu_name):
    url_dict = {
        "🏠 Beranda": "https://images.unsplash.com/photo-1581090700227-1e8d60b6f33b?auto=format&fit=crop&w=1600&q=80",
        "🔬 Spektrofotometer": "https://images.unsplash.com/photo-1588776814546-ec7e4093f07e?auto=format&fit=crop&w=1600&q=80",
        "🧴 Penanganan Bahan Kimia": "https://images.unsplash.com/photo-1600172454520-0c393eec6c96?auto=format&fit=crop&w=1600&q=80",
        "🛡 Keselamatan Kerja (K3)": "https://images.unsplash.com/photo-1625720071675-2c3adf3edb41?auto=format&fit=crop&w=1600&q=80",
        "🧰 Alat Dasar Lab": "https://images.unsplash.com/photo-1603386329225-868f9a77e1aa?auto=format&fit=crop&w=1600&q=80"
    }

    bg_url = url_dict.get(menu_name, "")

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{bg_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 12px;
        }}
        </style>
    """, unsafe_allow_html=True)


# Sidebar menu
menu = st.sidebar.selectbox(
    "Pilih Halaman",
    (
        "🏠 Beranda",
        "🔬 Spektrofotometer",
        "🧴 Penanganan Bahan Kimia",
        "🛡 Keselamatan Kerja (K3)",
        "🧰 Alat Dasar Lab"
    )
)

# ==================== Halaman Beranda ====================
if menu == "🏠 Beranda":
    st.title("💡 Aplikasi Science, Lab & Education")
    st.markdown("""
    ## Selamat Datang 👋
    Aplikasi ini membantu Anda memahami berbagai simulasi instrumen laboratorium kimia, 
    serta menyediakan panduan penanganan bahan kimia dan keselamatan kerja (K3).
    """)

# ==================== Halaman Spektrofotometer ====================
elif menu == "🔬 Spektrofotometer":
    st.title("🔬 Simulasi Spektrofotometer UV-Vis")

    st.subheader("🔬 1. Simulasi Spektrum UV-Vis (λ Maksimal)")
    st.write("Simulasi ini menampilkan grafik absorbansi terhadap panjang gelombang.")

    contoh_data = "200,0.01\n250,0.18\n300,0.45\n350,0.60\n400,0.40\n450,0.25"
    input_uvvis = st.text_area("Masukkan data panjang gelombang dan absorbansi (λ [nm], Absorbansi)", contoh_data, height=150)

    df_uv = None
    if input_uvvis:
        try:
            lines = input_uvvis.strip().split('\n')
            data = [tuple(map(float, line.split(','))) for line in lines]
            df_uv = pd.DataFrame(data, columns=["Panjang Gelombang (nm)", "Absorbansi"])
        except Exception as e:
            st.error(f"Gagal membaca data teks: {e}")

    if df_uv is not None:
        idx_max = df_uv["Absorbansi"].idxmax()
        lambda_max = df_uv.loc[idx_max, "Panjang Gelombang (nm)"]
        st.success(f"λ maks terdeteksi pada: {lambda_max} nm")

        warna_garis = st.color_picker("Pilih warna garis spektrum", "#000000")
        overlay = st.checkbox("Tampilkan spektrum referensi? (simulasi)")

        fig, ax = plt.subplots()
        ax.plot(df_uv["Panjang Gelombang (nm)"], df_uv["Absorbansi"], color=warna_garis, label='Spektrum Sampel')
        ax.axvline(lambda_max, color='red', linestyle='--', label=f'λ maks = {lambda_max} nm')

        if overlay:
            ref_lambda = df_uv["Panjang Gelombang (nm)"]
            ref_abs = np.interp(ref_lambda, ref_lambda, df_uv["Absorbansi"]) * 0.8
            ax.plot(ref_lambda, ref_abs, color='gray', linestyle=':', label='Referensi')

        ax.set_xlabel("Panjang Gelombang (nm)")
        ax.set_ylabel("Absorbansi")
        ax.set_title("Spektrum UV-Vis")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("Silakan masukkan data panjang gelombang dan absorbansi di atas untuk melihat grafik.")

    # ==================== Simulasi Kurva Kalibrasi ====================
    st.subheader("2. Simulasi Kurva Kalibrasi")
    default_data = {
        "Konsentrasi (ppm)": [0, 5, 10, 15, 20, 25],
        "Absorbansi": [0.02, 0.13, 0.27, 0.40, 0.52, 0.64]
    }

    df = pd.DataFrame(default_data)
    edited_df = st.data_editor(df, use_container_width=True)

    X = np.array(edited_df["Konsentrasi (ppm)"]).reshape(-1, 1)
    y = np.array(edited_df["Absorbansi"])

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]
    intercept = model.intercept_
    r2 = model.score(X, y)

    st.markdown(f"""
    Persamaan regresi:  
    Absorbansi = {slope:.4f} × Konsentrasi + {intercept:.4f}  
    Koefisien determinasi (R²) = {r2:.4f}
    """)

    fig, ax = plt.subplots()
    ax.scatter(X, y, color='blue', label='Data Standar')
    ax.plot(X, model.predict(X), color='green', label='Regresi Linear')
    ax.set_xlabel("Konsentrasi (ppm)")
    ax.set_ylabel("Absorbansi")
    ax.legend()
    st.pyplot(fig)

    # ==================== Hitung Konsentrasi ====================
    st.subheader("3. Hitung Konsentrasi Sampel")
    absorbansi_sampel = st.number_input("Nilai absorbansi sampel", min_value=0.0, step=0.01)
    slope_input = st.number_input("Slope", value=float(slope), format="%.4f")
    intercept_input = st.number_input("Intercept", value=float(intercept), format="%.4f")

    if st.button("Hitung Konsentrasi"):
        try:
            konsentrasi = (absorbansi_sampel - intercept_input) / slope_input
            st.success(f"Perkiraan konsentrasi sampel: {konsentrasi:.2f} ppm")
        except ZeroDivisionError:
            st.error("Slope tidak boleh nol.")

# ==================== Halaman Penanganan Bahan Kimia ====================
elif menu == "🧴 Penanganan Bahan Kimia":
    st.title("🧴 Penanganan Bahan Kimia")

    st.markdown("""
    Bahan kimia di laboratorium dapat bersifat berbahaya jika tidak ditangani dengan benar.  
    Berikut ini adalah panduan lengkap untuk memahami risiko serta cara penanganan dan penyimpanan dari beberapa bahan kimia umum.
    """)

    bahan = st.selectbox("Pilih bahan kimia yang ingin Anda pelajari:", [
        "Asam Sulfat (H₂SO₄)",
        "Natrium Hidroksida (NaOH)",
        "Aseton (CH₃COCH₃)",
        "Hidrogen Peroksida (H₂O₂)",
        "Klorin (Cl₂)",
        "Metanol (CH₃OH)",
        "Amonia (NH₃)",
        "Benzena (C₆H₆)",
        "Formaldehida (CH₂O)",
        "Klorofom (CHCl₃)"
    ])
   

    if bahan == "Asam Sulfat (H₂SO₄)":
        st.header("Asam Sulfat (H₂SO₄)")
        st.warning("⚠ Bahaya: Sangat korosif dan bereaksi hebat dengan air.")

        st.markdown("""
        🧪 Karakteristik bahan kimia :  
        - Cairan kental, tidak berwarna atau sedikit kekuningan  
        - Tidak mudah menguap, namun sangat reaktif  
        - Daya hancur tinggi terhadap jaringan hidup dan sebagian besar material

        ⚠ Risiko yang terjadi :  
        - Kontak dengan kulit: luka bakar parah  
        - Uapnya: iritasi saluran pernapasan  
        - Jika tercampur air: menghasilkan panas ekstrem dan percikan

        🚨 Langkah Penanganan Darurat :  
        - Jika terkena kulit: siram dengan air mengalir minimal 15 menit  
        - Jika terkena mata: bilas mata sambil dibuka perlahan, dan segera ke rumah sakit  
        - Jika tertelan: jangan muntahkan, segera hubungi medis

        📦 Penyimpanan Aman:  
        - Gunakan wadah dari kaca tahan asam atau plastik khusus (HDPE)  
        - Simpan di tempat sejuk, gelap, dan berventilasi  
        - Jangan simpan dekat air, logam, atau bahan organik

        ** 🛡Pencegahan:**  
        - Gunakan pelindung wajah, sarung tangan, dan apron kimia  
        - Selalu tambahkan asam ke air, bukan sebaliknya
        """)

    elif bahan == "Natrium Hidroksida (NaOH)":
        st.header("Natrium Hidroksida (NaOH)")
        st.warning("⚠ Bahaya: Sangat basa, bersifat kaustik, dapat merusak jaringan tubuh.")

        st.markdown("""
        🧪 Karakteristik bahan kimia:  
        - Padatan putih atau larutan bening  
        - Bersifat higroskopis (menyerap uap air)  
        - Membentuk larutan yang sangat basa dan panas saat dilarutkan

        ⚠ Risiko yang terjadi:  
        - Iritasi atau luka bakar berat pada kulit dan mata  
        - Dapat menyebabkan kerusakan permanen jika kontak mata lama  
        - Uap dapat menyebabkan iritasi saluran pernapasan

        🚨 Langkah Penanganan Darurat:  
        - Kulit terkena: bilas dengan air tanpa henti selama 20 menit  
        - Mata terkena: bilas dengan larutan saline atau air bersih segera  
        - Jika tertelan: jangan dipaksa muntah, hubungi rumah sakit

        📦 Penyimpanan Aman:  
        - Simpan dalam wadah plastik tahan basa dan tertutup rapat  
        - Hindari kontak dengan bahan asam  
        - Simpan di tempat kering, sejuk, dan berventilasi

        🛡Pencegahan:  
        - Gunakan sarung tangan nitril, pelindung mata, dan jas laboratorium  
        - Tangani di bawah lemari asam jika memungkinkan
        """)

    elif bahan == "Aseton (CH₃COCH₃)":
        st.header("Aseton (CH₃COCH₃)")
        st.warning("⚠ Bahaya: Sangat mudah terbakar, menyebabkan iritasi pernapasan.")

        st.markdown("""
        🧪 Karakteristik bahan kimia:  
        - Cairan bening, sangat mudah menguap  
        - Berbau khas (seperti pelarut cat kuku)  
        - Digunakan sebagai pelarut di banyak industri

        ⚠ Risiko yang terjadi:  
        - Menghirup uapnya menyebabkan pusing, sakit kepala, mual  
        - Kontak kulit menyebabkan kekeringan dan iritasi  
        - Bahaya kebakaran tinggi bahkan pada suhu ruangan

        🚨 Langkah Penanganan Darurat:  
        - Hirup uap: segera ke area berventilasi atau udara segar  
        - Kontak kulit: cuci dengan sabun dan air  
        - Terbakar: gunakan APAR CO₂ atau dry chemical

        📦 Penyimpanan Aman:  
        - Gunakan wadah logam tahan pelarut dengan tutup rapat  
        - Jauhkan dari sumber api, percikan, dan listrik statis  
        - Simpan di kabinet bahan mudah terbakar (flammable storage)

        🛡Pencegahan:  
        - Gunakan di ruangan terbuka atau berventilasi baik  
        - Hindari menghirup uap secara langsung
        """)

    elif bahan == "Hidrogen Peroksida (H₂O₂)":
        st.header("Hidrogen Peroksida (H₂O₂)")
        st.warning("⚠ Bahaya: Oksidator kuat, reaktif, dan dapat menyebabkan luka bakar kimia.")

        st.markdown("""
        🧪 Karakteristik bahan kimia:  
        - Larutan bening, mirip air, tapi sangat reaktif  
        - Konsentrasi tinggi (di atas 30%) sangat berbahaya  
        - Digunakan sebagai desinfektan dan agen pemutih

        ⚠ Risiko yang terjadi:  
        - Kulit: luka bakar, iritasi  
        - Mata: iritasi serius atau kebutaan permanen  
        - Reaksi eksplosif jika kontak logam, bahan organik, atau panas

        🚨 Langkah Penanganan Darurat:  
        - Kulit terkena: bilas dengan air 15 menit  
        - Mata terkena: segera cuci mata dan hubungi dokter  
        - Terhirup: pindahkan ke area udara segar dan beri oksigen jika perlu

        📦 Penyimpanan Aman:  
        - Simpan dalam botol berwarna gelap, jauh dari cahaya  
        - Hindari suhu tinggi dan bahan logam  
        - Gunakan wadah asli yang tahan oksidasi

        🛡Pencegahan:  
        - Gunakan pelindung mata dan sarung tangan neoprene  
        - Hindari penggunaan logam atau benda berkarat saat menanganinya
        """)


    elif bahan == "Klorin (Cl₂)":
        st.header("🧪 Klorin (Cl₂)")
        st.markdown("### 🧪 Karakteristik bahan kimia")
        st.info("""
        - Gas kuning kehijauan dengan bau tajam dan menyengat  
        - Sangat reaktif, korosif, dan beracun  
        - Oksidator kuat, berbahaya bagi lingkungan  

        ⚠ Simbol Bahaya:  
        ☠ Racun (Toxic)  
        🧪 Korosif  
        🌿 Bahaya lingkungan  
        """)
        st.markdown("### ⚠ Risiko yang terjadi")
        st.error("""
        - Pernapasan: iritasi berat saluran pernapasan, sesak napas, kerusakan paru-paru  
        - Kulit dan mata: iritasi, luka bakar  
        - Paparan tinggi dapat menyebabkan kematian
        """)
        st.markdown("### 🚨 Penanganan Darurat")
        st.warning("""
        - Evakuasi area dan bawa korban ke udara segar  
        - Bilas mata atau kulit dengan air mengalir minimal 15 menit  
        - Gunakan alat pelindung diri lengkap saat menangani kebocoran
        """)
        st.markdown("### 📦 Penyimpanan Aman")
        st.success("""
        - Simpan dalam tabung gas bertekanan standar  
        - Jauhkan dari bahan mudah terbakar dan bahan reduktor  
        - Tempat penyimpanan harus berventilasi baik dan tertutup rapat
        """)
        st.markdown("### 🛡 Pencegahan")
        st.info("""
        - Gunakan masker respirator dan pelindung mata saat menangani gas  
        - Monitor kebocoran gas dengan detektor khusus  
        - Latih prosedur evakuasi dan tanggap darurat gas beracun
        """)

    elif bahan == "Metanol (CH₃OH)":
        st.header("🧪 Metanol (CH₃OH)")
        st.markdown("### 🧪 Karakteristik bahan kimia")
        st.info("""
        - Cairan bening, mudah menguap dan sangat mudah terbakar  
        - Beracun jika tertelan, terhirup, atau kontak kulit  
        - Bau alkohol yang khas  

        ⚠ Simbol Bahaya:  
        ☠ Beracun (Toxic)  
        🔥 Mudah terbakar (Flammable)  
        """)
        st.markdown("### ⚠ Risiko yang terjadi")
        st.error("""
        - Tertelan: keracunan serius, kerusakan organ dalam, kematian  
        - Terhirup: iritasi pernapasan, pusing, sakit kepala  
        - Kontak kulit: iritasi dan kemungkinan penyerapannya ke dalam tubuh
        """)
        st.markdown("### 🚨 Penanganan Darurat")
        st.warning("""
        - Jika tertelan, segera cari pertolongan medis  
        - Bilas kulit dan mata jika terkena  
        - Pastikan ventilasi cukup dan jauhkan dari sumber api
        """)
        st.markdown("### 📦 Penyimpanan Aman")
        st.success("""
        - Simpan dalam wadah tertutup rapat dan tahan bahan kimia  
        - Jauhkan dari panas, percikan api, dan sumber nyala api  
        - Tempat penyimpanan harus berventilasi dan sejuk
        """)
        st.markdown("### 🛡 Pencegahan")
        st.info("""
        - Gunakan sarung tangan tahan bahan kimia dan pelindung mata  
        - Hindari penggunaan di area tertutup tanpa ventilasi baik  
        - Sediakan alat pemadam api dan prosedur tanggap kebakaran
        """)

    if bahan == "Amonia (NH₃)":
        st.header("🧪 Amonia (NH₃)")
        st.markdown("### 🧪 Karakteristik bahan kimia")
        st.info("""
        - Gas tidak berwarna dengan bau tajam menyengat  
        - Sangat mudah larut dalam air membentuk basa kuat  
        - Dapat menyebabkan iritasi dan korosif  
        
        ⚠ Simbol Bahaya:  
        ☠ Racun (Toxic)  
        🧪 Korosif
        """)
        st.markdown("### ⚠ Risiko yang terjadi")
        st.error("""
        - Terhirup: iritasi saluran pernapasan, batuk, sesak napas  
        - Kontak kulit/mata: iritasi, luka bakar  
        - Paparan tinggi dapat menyebabkan kerusakan paru-paru
        """)
        st.markdown("### 🚨 Penanganan Darurat")
        st.warning("""
        - Pindahkan korban ke udara segar  
        - Bilas kulit/mata dengan air mengalir selama 15 menit  
        - Gunakan alat pelindung diri lengkap saat menangani kebocoran gas
        """)
        st.markdown("### 📦 Penyimpanan Aman")
        st.success("""
        - Simpan dalam tabung gas bertekanan dengan ventilasi baik  
        - Jauhkan dari bahan asam dan sumber panas  
        - Tempat penyimpanan harus aman dan tertutup rapat
        """)
        st.markdown("### 🛡 Pencegahan")
        st.info("""
        - Gunakan masker respirator dan pelindung mata  
        - Hindari kontak langsung dengan gas  
        - Monitor konsentrasi gas di area kerja
        """)

    elif bahan == "Benzena (C₆H₆)":
        st.header("🧪 Benzena (C₆H₆)")
        st.markdown("### 🧪 Karakteristik bahan kimia")
        st.info("""
        - Cairan bening mudah menguap, bau khas  
        - Sangat mudah terbakar dan karsinogenik  
        
        ⚠ Simbol Bahaya:  
        ☠ Beracun (Toxic)  
        🔥 Mudah terbakar (Flammable)  
        ☣ Karsinogen
        """)
        st.markdown("### ⚠ Risiko yang terjadi")
        st.error("""
        - Terhirup: kerusakan sistem saraf, pusing, mual  
        - Tertelan/kontak kulit: iritasi, toksisitas  
        - Paparan jangka panjang: risiko kanker darah (leukemia)
        """)
        st.markdown("### 🚨 Penanganan Darurat")
        st.warning("""
        - Evakuasi ke udara segar  
        - Hindari kontak kulit dan mata  
        - Gunakan alat pelindung diri dan ventilasi memadai
        """)
        st.markdown("### 📦 Penyimpanan Aman")
        st.success("""
        - Simpan di wadah tertutup rapat di tempat sejuk dan berventilasi  
        - Jauhkan dari sumber api dan bahan pengoksidasi  
        - Gunakan wadah tahan bahan kimia dan ledakan
        """)
        st.markdown("### 🛡 Pencegahan")
        st.info("""
        - Gunakan sarung tangan dan pelindung mata  
        - Kerja di ruang ventilasi baik atau fume hood  
        - Hindari paparan jangka panjang
        """)

    elif bahan == "Formaldehida (CH₂O)":
        st.header("🧪 Formaldehida (CH₂O)")
        st.markdown("### 🧪 Karakteristik bahan kimia")
        st.info("""
        - Gas atau larutan berbau tajam dan menyengat  
        - Karsinogen dan iritan kuat  
        
        ⚠ Simbol Bahaya:  
        ☠ Beracun (Toxic)  
        ☣ Karsinogen  
        🧪 Korosif
        """)
        st.markdown("### ⚠ Risiko yang terjadi")
        st.error("""
        - Terhirup: iritasi saluran pernapasan, batuk, sesak  
        - Kontak kulit/mata: iritasi, alergi  
        - Paparan jangka panjang: risiko kanker hidung dan tenggorokan
        """)
        st.markdown("### 🚨 Penanganan Darurat")
        st.warning("""
        - Pindahkan korban ke udara segar  
        - Bilas mata dan kulit dengan air mengalir  
        - Gunakan alat pelindung lengkap saat menangani bahan ini
        """)
        st.markdown("### 📦 Penyimpanan Aman")
        st.success("""
        - Simpan di tempat tertutup dan berventilasi baik  
        - Jauhkan dari sumber panas dan bahan pengoksidasi  
        - Gunakan wadah tahan bahan kimia
        """)
        st.markdown("### 🛡 Pencegahan")
        st.info("""
        - Gunakan respirator, sarung tangan, dan pelindung mata  
        - Kerja di fume hood atau area ventilasi baik  
        - Hindari paparan berulang dan jangka panjang
        """)

    elif bahan == "Klorofom (CHCl₃)":
        st.header("🧪 Klorofom (CHCl₃)")
        st.markdown("### 🧪 Karakteristik bahan kimia")
        st.info("""
        - Cairan bening, bau manis  
        - Sedatif, toksik, dan kemungkinan karsinogen  
        
        ⚠ Simbol Bahaya:  
        ☠ Beracun (Toxic)  
        ⚠ Bahaya kesehatan (Health hazard)  
        """)
        st.markdown("### ⚠ Risiko yang terjadi")
        st.error("""
        - Terhirup: depresi sistem saraf pusat, mual, pusing  
        - Kontak kulit: iritasi dan toksisitas  
        - Paparan jangka panjang: kemungkinan kanker hati dan ginjal
        """)
        st.markdown("### 🚨 Penanganan Darurat")
        st.warning("""
        - Pindahkan ke udara segar  
        - Bilas kulit dan mata dengan air  
        - Gunakan alat pelindung diri saat bekerja dengan bahan ini
        """)
        st.markdown("### 📦 Penyimpanan Aman")
        st.success("""
        - Simpan di tempat gelap, dingin, dan berventilasi  
        - Jauhkan dari sumber api dan oksidator  
        - Gunakan wadah tertutup rapat
        """)
        st.markdown("### 🛡 Pencegahan")
        st.info("""
        - Gunakan sarung tangan tahan bahan kimia dan pelindung mata  
        - Kerja di fume hood  
        - Hindari paparan berulang dan penggunaan jangka panjang
        """)


# ==================== Halaman K3 ====================
elif menu == "🛡 Keselamatan Kerja (K3)":
    st.title("🧪🔬 Keselamatan Kerja di Laboratorium Kimia 🧤🦺")

    st.markdown("""
    ---
## 🛡 Prinsip Umum Keselamatan

🔸 Kenali bahan kimia sebelum digunakan (baca label & MSDS)  
🔸 Gunakan APD (Alat Pelindung Diri):  
  🧥 Jas lab 👓 Kacamata 🧤 Sarung tangan  
🔸 Dilarang keras: 🍔 Makan, 🍵 Minum, dan 💄 Make-up di lab  
🔸 Cuci tangan 🧼 sebelum dan sesudah praktikum  
🔸 Jaga meja tetap rapi dan bersih 🧹

---

## 🔥 Penanganan Bahan Kimia Berbahaya

☠ Hindari menghirup langsung bahan beracun  
🌬 Gunakan lemari asam saat menangani bahan volatil  
🔒 Simpan bahan sesuai kategori:  
  🔴 Asam 🔵 Basa 🟢 Pelarut Organik  
🔀 Jangan mencampur bahan tanpa prosedur!

---

## 🚨 Tanggap Darurat

### 💧 Tumpahan Bahan Kimia
- Gunakan Spill Kit 🧯
- Tutup dan beri tanda peringatan 🚧
- Segera laporkan ke dosen atau teknisi 📢

### 🔥 Luka Bakar Kimia
- Bilas air mengalir 🚿 selama 15 menit
- Lepas pakaian yang terkena bahan 👕
- Segera cari pertolongan medis 🚑

---

## ⚠ Pencegahan Umum

- 🧍‍♂ Jangan bekerja sendirian di lab
- 🩻 Periksa alat sebelum digunakan
- 🚫 Hindari baju longgar, sandal, dan aksesori
- 🌬 Pastikan ventilasi lab berfungsi baik
---

## 🧪 Pengelolaan Limbah Laboratorium

♻ Pisahkan limbah berdasarkan jenis:
- 🧴 Organik
- 🧂 Anorganik
- ☣ B3 (Bahan Berbahaya & Beracun)

🚫 Jangan buang limbah ke wastafel sembarangan  
🗑 Gunakan wadah limbah bertanda khusus

---

## ✅ Penutup

🏁 Keselamatan kerja adalah tanggung jawab bersama.  
Dengan disiplin dan kesadaran, kita bisa menciptakan laboratorium yang:

🎯 Aman 🧘 Nyaman 🌱 Ramah Lingkungan

> ✨ "Selalu waspada, tetap selamat!" ✨

---
""")

# ==================== Halaman Alat Dasar Lab ====================
elif menu == "🧰 Alat Dasar Lab":
    st.title("🧰 Peralatan Dasar Laboratorium Kimia")

    st.markdown("""
    ## 📌 Cara Penggunaan Alat
    Berikut adalah cara penggunaan beberapa alat gelas dasar:
    """)

    with st.expander("🔍 Pipet Volume"):
        st.markdown("""
        - Gunakan pipet pengisap (jangan pakai mulut).
        - Ambil larutan hingga tepat di garis kalibrasi.
        - Hindari gelembung.
        """)

    with st.expander("🔍 Buret"):
        st.markdown("""
        - Pastikan tidak ada gelembung udara di ujung buret.
        - Bacaan dilakukan sejajar dengan meniskus.
        - Tutup keran saat tidak digunakan.
        """)

    with st.expander("🔍 Labu Ukur"):
        st.markdown("""
        - Gunakan untuk pembuatan larutan dengan volume tepat.
        - Tambahkan air hingga mendekati garis ukur, lalu pakai pipet tetes.
        """)

        st.markdown("---")
        st.subheader("🧪 Simulasi Pengukuran Volume")
        pipet = st.number_input("📏 Volume dari Pipet Volume (mL)", min_value=0.0, max_value=25.0, step=0.1, value=10.0)
        buret_start = st.number_input("💧 Volume Awal Buret (mL)", min_value=0.0, max_value=50.0, step=0.1, value=0.0)
        buret_end = st.number_input("💧 Volume Akhir Buret (mL)", min_value=0.0, max_value=50.0, step=0.1, value=23.5)
        labu_ukur = st.selectbox("⚗ Labu Ukur yang Digunakan", ["Tidak digunakan", "25 mL", "50 mL", "100 mL", "250 mL", "500 mL"])

    # Validasi volume buret
    if buret_end >= buret_start:
        volume_buret = buret_end - buret_start
        error_buret = round(random.uniform(-0.05, 0.05), 2)
    else:
        st.warning("⚠ Volume akhir tidak boleh lebih kecil dari volume awal.")
        volume_buret = 0.0
        error_buret = 0.0

    # Volume labu ukur
    volume_labu = float(labu_ukur.split()[0]) if labu_ukur != "Tidak digunakan" else 0.0

    # Error simulasi alat
    error_pipet = round(random.uniform(-0.05, 0.05), 2)
    error_labu = round(random.uniform(-0.1, 0.1), 2)
    total_volume = pipet + volume_buret + volume_labu
    total_error = error_pipet + error_buret + error_labu

    # Rincian volume
    with st.expander("📊 Rincian Volume"):
        st.write(f"Pipet Volume: {pipet:.2f} mL")
        st.write(f"Buret: {volume_buret:.2f} mL")
        st.write(f"Labu Ukur: {volume_labu:.2f} mL")

    st.success(f"📦 Total Volume Cairan (tanpa error): {total_volume:.2f} mL")
    st.info(f"⚠ Dengan toleransi pengukuran: ±{abs(total_error):.2f} mL")

    # Konfigurasi halaman
    st.set_page_config(page_title="Kuis Peralatan Gelas", layout="centered")
    
    # Garis pemisah dan judul
    st.markdown("---")
    st.subheader("🧠 Kuis Cepat: Peralatan Gelas")
    
    # Daftar soal
    soal_list = [
        {
            "question": "Apa nama alat gelas ini yang digunakan untuk mengukur volume dengan akurasi tinggi?",
            "options": ["Gelas ukur", "Buret", "Erlenmeyer", "Pipet tetes"],
            "answer": "Buret"
        },
        {
            "question": "Alat gelas berbentuk kerucut yang biasa digunakan untuk mencampur larutan adalah?",
            "options": ["Tabung reaksi", "Erlenmeyer", "Buret", "Pipet ukur"],
            "answer": "Erlenmeyer"
        },
        {
            "question": "Gelas ukur digunakan untuk...",
            "options": ["Reaksi kimia", "Mengaduk larutan", "Mengukur volume larutan", "Memisahkan zat padat"],
            "answer": "Mengukur volume larutan"
        },
        {
            "question": "Pipet ukur digunakan untuk...",
            "options": ["Memindahkan larutan dalam jumlah tetap", "Mengaduk larutan", "Memanaskan cairan", "Mengukur pH"],
   "answer": "Memindahkan larutan dalam jumlah tetap"
        },
        {
            "question": "Alat yang digunakan untuk mereaksikan larutan dalam jumlah kecil adalah...",
            "options": ["Erlenmeyer", "Buret", "Tabung reaksi", "Gelas ukur"],
            "answer": "Tabung reaksi"
        },
    ]
    
    # Pilih 3 soal secara acak
    soal_terpilih = random.sample(soal_list, 3)
    
    # Form kuis
    with st.form("kuis_alat"):
        jawaban_user = []
        for i, soal in enumerate(soal_terpilih):
            jawaban = st.radio(
                f"{i+1}. {soal['question']}",
                soal['options'],
                key=f"soal_{i}"
            )
            jawaban_user.append(jawaban)
 
        submit = st.form_submit_button("💡 Cek Jawaban")
    
    # Evaluasi hasil
    if submit:
        benar = 0
        for i, soal in enumerate(soal_terpilih):
            if jawaban_user[i] == soal["answer"]:
                benar += 1
    
        st.success(f"✅ Jawaban benar: {benar} dari {len(soal_terpilih)}")
        if benar < len(soal_terpilih):
            st.warning("Coba pelajari kembali bagian di atas ya!")
        else:
            st.balloons()
