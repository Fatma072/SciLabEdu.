from pathlib import Path
streamlit_code = "print('Halo dunia')"  # <- isi ini dengan kode Python yang Anda maksud

path = Path("simulator_kimia_app.py")
path.write_text(streamlit_code)

# Kode aplikasi Streamlit lengkap dengan semua menu dan background
streamlit_code = """
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="SciLabEdu", layout="wide")

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

# =================== Halaman Beranda ===================
if menu == "🏠 Beranda":
    st.title("💡 Aplikasi Science, Lab & Education")
    st.markdown(\"\"\"
    <div style="background-color:#e8f4fa; padding:20px; border-radius:10px;">
        <h3>👋 Selamat Datang</h3>
        <p>Aplikasi ini membantu Anda memahami berbagai simulasi instrumen laboratorium kimia, 
        serta menyediakan panduan penanganan bahan kimia dan keselamatan kerja (K3).</p>
    </div>
    \"\"\", unsafe_allow_html=True)

# =================== Halaman Spektrofotometer ===================
elif menu == "🔬 Spektrofotometer":
    st.title("🔬 Simulasi Spektrofotometer UV-Vis")

    st.markdown(\"\"\"
    <div style="background-color:#f5f5f5; padding:15px; border-radius:8px;">
        <h4>🔬 1. Simulasi Spektrum UV-Vis (λ Maksimal)</h4>
        <p>Simulasi ini menampilkan grafik absorbansi terhadap panjang gelombang.</p>
    </div>
    \"\"\", unsafe_allow_html=True)

    contoh_data = "200,0.01\\n250,0.18\\n300,0.45\\n350,0.60\\n400,0.40\\n450,0.25"
    input_uvvis = st.text_area("Masukkan data panjang gelombang dan absorbansi (λ [nm], Absorbansi)", contoh_data, height=150)

    df_uv = None
    if input_uvvis:
        try:
            lines = input_uvvis.strip().split('\\n')
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

    st.markdown(\"\"\"
    <div style="background-color:#fdf5e6; padding:15px; border-radius:8px;">
        <h4>📈 2. Simulasi Kurva Kalibrasi</h4>
    </div>
    \"\"\", unsafe_allow_html=True)

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

    st.markdown(f\"\"\"
    <div style="background-color:#e6ffe6; padding:10px; border-radius:8px">
        <b>Persamaan regresi:</b> Absorbansi = {slope:.4f} × Konsentrasi + {intercept:.4f}  <br>
        <b>Koefisien determinasi (R²):</b> {r2:.4f}
    </div>
    \"\"\", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    ax.scatter(X, y, color='blue', label='Data Standar')
    ax.plot(X, model.predict(X), color='green', label='Regresi Linear')
    ax.set_xlabel("Konsentrasi (ppm)")
    ax.set_ylabel("Absorbansi")
    ax.legend()
    st.pyplot(fig)

    st.markdown(\"\"\"
    <div style="background-color:#f0f8ff; padding:15px; border-radius:8px">
        <h4>🧪 3. Hitung Konsentrasi Sampel</h4>
    </div>
    \"\"\", unsafe_allow_html=True)

    absorbansi_sampel = st.number_input("Nilai absorbansi sampel", min_value=0.0, step=0.01)
    slope_input = st.number_input("Slope", value=float(slope), format="%.4f")
    intercept_input = st.number_input("Intercept", value=float(intercept), format="%.4f")

    if st.button("Hitung Konsentrasi"):
        try:
            konsentrasi = (absorbansi_sampel - intercept_input) / slope_input
            st.success(f"Perkiraan konsentrasi sampel: {konsentrasi:.2f} ppm")
        except ZeroDivisionError:
            st.error("Slope tidak boleh nol.")

# =================== Penanganan Bahan Kimia ===================
elif menu == "🧴 Penanganan Bahan Kimia":
    st.title("🧴 Penanganan Bahan Kimia Berbahaya")
    st.markdown(\"\"\"
    <div style="background-color:#fff3cd; padding:20px; border-radius:10px;">
        <h4>🧪 Tips Penanganan</h4>
        <ul>
            <li>Gunakan APD lengkap: sarung tangan, jas lab, kacamata pelindung.</li>
            <li>Baca label dan Lembar Data Keselamatan (MSDS) sebelum penggunaan.</li>
            <li>Jangan mencampur bahan kimia tanpa mengetahui reaksi yang mungkin.</li>
            <li>Gunakan lemari asam untuk zat yang mudah menguap atau berbahaya.</li>
        </ul>
    </div>
    \"\"\", unsafe_allow_html=True)

# =================== Keselamatan Kerja (K3) ===================
elif menu == "🛡 Keselamatan Kerja (K3)":
    st.title("🛡 Keselamatan Kerja di Laboratorium (K3)")
    st.markdown(\"\"\"
    <div style="background-color:#d4edda; padding:20px; border-radius:10px;">
        <h4>📋 Protokol Umum K3</h4>
        <ol>
            <li>Selalu mengenakan Alat Pelindung Diri (APD).</li>
            <li>Jangan makan, minum, atau merokok di laboratorium.</li>
            <li>Tahu lokasi APAR, shower darurat, dan kotak P3K.</li>
            <li>Simpan bahan kimia sesuai kelas bahayanya.</li>
            <li>Lapor segera jika terjadi tumpahan atau kecelakaan.</li>
        </ol>
    </div>
    \"\"\", unsafe_allow_html=True)

# =================== Alat Dasar Lab ===================
elif menu == "🧰 Alat Dasar Lab":
    st.title("🧰 Pengantar Alat-Alat Dasar Laboratorium")
    st.markdown(\"\"\"
    <div style="background-color:#e2e3e5; padding:20px; border-radius:10px;">
        <h4>🔧 Contoh Alat</h4>
        <ul>
            <li>Gelas ukur</li>
            <li>Erlenmeyer</li>
            <li>Labu ukur</li>
            <li>Corong kaca</li>
            <li>Batang pengaduk</li>
            <li>Pipet ukur & pipet tetes</li>
        </ul>
    </div>
    \"\"\", unsafe_allow_html=True)

    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Lab_equipment_collage_en.svg/800px-Lab_equipment_collage_en.svg.png", caption="Peralatan gelas laboratorium", use_column_width=True)
"""

# Simpan ke file Python
path = Path("/mnt/data/simulator_kimia_app.py")
path.write_text(streamlit_code)

# Juga buat requirements.txt
requirements_path = Path("/mnt/data/requirements.txt")
requirements_path.write_text("streamlit\npandas\nmatplotlib\nscikit-learn\nnumpy")

