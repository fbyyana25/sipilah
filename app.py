import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetim

# Data klasifikasi dan penanganan sampah laboratorium yang lebih detail
data_sampah_lab_detail = {
    "Gelas Kimia Bekas": {
        "kategori": "Gelas",
        "deskripsi": "Gelas kimia bekas yang tidak terkontaminasi bahan berbahaya.",
        "pengolahan": """
            1. Bilas gelas kimia dengan air untuk menghilangkan sisa bahan kimia.
            2. Sterilisasi dengan autoklaf jika bekas media kultur atau bahan biologis.
            3. Cuci bersih menggunakan deterjen laboratorium.
            4. Keringkan dan simpan untuk penggunaan kembali jika masih layak.
            5. Jika pecah atau tidak layak pakai, buang ke wadah khusus limbah gelas untuk didaur ulang.
        """,
        "daur_ulang": "Dapat didaur ulang menjadi produk kaca baru.",
        "bahaya": "Potensi luka jika pecah.",
        "gambar": "gelas_kimia.jpg"  # Placeholder untuk path gambar
    },
    "Labu Erlenmeyer Bekas": {
        "kategori": "Gelas",
        "deskripsi": "Labu Erlenmeyer bekas yang tidak terkontaminasi bahan berbahaya.",
        "pengolahan": """
            1. Bilas labu dengan air.
            2. Sterilisasi jika bekas bahan biologis.
            3. Cuci bersih.
            4. Keringkan dan simpan untuk digunakan kembali.
            5. Jika rusak, buang ke limbah gelas daur ulang.
        """,
        "daur_ulang": "Sama seperti gelas kimia.",
        "bahaya": "Potensi luka jika pecah.",
        "gambar": "labu_erlenmeyer.jpg"
    },
    "Pipet Plastik Bekas (Non-Biohazard)": {
        "kategori": "Plastik",
        "deskripsi": "Pipet plastik sekali pakai yang tidak terkontaminasi bahan biologis atau kimia berbahaya.",
        "pengolahan": """
            1. Bilas pipet jika perlu.
            2. Kumpulkan dalam wadah limbah plastik.
            3. Daur ulang jika fasilitas kampus memiliki program daur ulang plastik.
            4. Jika tidak ada program daur ulang, buang ke limbah non-medis.
        """,
        "daur_ulang": "Tergantung jenis plastik (PP, PE).",
        "bahaya": "Potensi luka jika tajam (ujung pipet).",
        "gambar": "pipet_plastik.jpg"
    },
    "Tabung Reaksi Bekas (Non-Biohazard)": {
        "kategori": "Gelas/Plastik",
        "deskripsi": "Tabung reaksi bekas yang tidak terkontaminasi bahan berbahaya.",
        "pengolahan": """
            1. Bilas tabung dengan air.
            2. Sterilisasi jika bekas bahan biologis.
            3. Cuci bersih.
            4. Keringkan dan simpan atau buang sesuai material (gelas didaur ulang, plastik dibuang atau didaur ulang).
        """,
        "daur_ulang": "Gelas dapat didaur ulang, plastik tergantung jenis.",
        "bahaya": "Potensi luka jika gelas pecah.",
        "gambar": "tabung_reaksi.jpg"
    },
    "Sarung Tangan Lateks/Nitril Bekas (Non-Tercemar B3)": {
        "kategori": "Karet/Plastik",
        "deskripsi": "Sarung tangan bekas yang tidak terkontaminasi bahan kimia berbahaya atau agen biologis aktif.",
        "pengolahan": """
            1. Lepaskan sarung tangan dengan benar untuk menghindari kontaminasi.
            2. Buang ke wadah limbah non-medis atau limbah plastik jika ada program daur ulang sarung tangan.
        """,
        "daur_ulang": "Beberapa jenis sarung tangan nitril dapat didaur ulang melalui program khusus.",
        "bahaya": "Potensi alergi lateks.",
        "gambar": "sarung_tangan.jpg"
    },
    "Botol Reagen Kosong (Non-Berbahaya, Sudah Dibilas)": {
        "kategori": "Gelas/Plastik",
        "deskripsi": "Botol bekas tempat reagen yang tidak berbahaya dan sudah dibilas bersih.",
        "pengolahan": """
            1. Bilas botol reagen beberapa kali dengan air hingga bersih.
            2. Lepaskan label jika memungkinkan.
            3. Buang ke wadah limbah gelas atau plastik sesuai jenis material untuk didaur ulang.
        """,
        "daur_ulang": "Gelas dan beberapa jenis plastik dapat didaur ulang.",
        "bahaya": "Potensi sisa bahan kimia jika tidak dibilas dengan benar.",
        "gambar": "botol_reagen.jpg"
    },
    "Kertas Saring Bekas (Tidak Tercemar B3)": {
        "kategori": "Kertas",
        "deskripsi": "Kertas saring bekas yang tidak terkontaminasi bahan berbahaya.",
        "pengolahan": """
            1. Kumpulkan kertas saring bekas dalam wadah limbah kertas.
            2. Pastikan tidak tercampur dengan limbah kimia atau biologis.
            3. Buang ke tempat pengumpulan daur ulang kertas.
        """,
        "daur_ulang": "Dapat didaur ulang menjadi produk kertas baru.",
        "bahaya": "Potensi kontaminasi jika tercampur limbah berbahaya.",
        "gambar": "kertas_saring.jpg"
    },
    "Sisa Larutan Garam Anorganik (Konsentrasi Rendah, Netral)": {
        "kategori": "Cair (Kimia Non-B3)",
        "deskripsi": "Sisa larutan garam anorganik dengan konsentrasi rendah dan pH netral.",
        "pengolahan": """
            1. Encerkan larutan dengan air dalam jumlah yang sesuai.
            2. Buang ke saluran pembuangan air limbah laboratorium sesuai dengan peraturan kampus dan lingkungan.
            3. Pastikan tidak ada logam berat atau bahan berbahaya lainnya.
        """,
        "daur_ulang": "Umumnya tidak didaur ulang, tetapi diolah di IPAL (Instalasi Pengolahan Air Limbah).",
        "bahaya": "Potensi korosif atau iritasi tergantung jenis garam dan konsentrasi.",
        "gambar": "larutan_garam.jpg"
    },
    "Sisa Pelarut Organik (Non-Halogenated, Jumlah Kecil)": {
        "kategori": "Cair (Kimia B3)",
        "deskripsi": "Sisa pelarut organik non-halogenated dalam jumlah kecil.",
        "pengolahan": """
            1. Kumpulkan dalam wadah limbah pelarut organik yang sesuai dan tertutup rapat.
            2. Beri label yang jelas mengenai jenis pelarut.
            3. Serahkan ke petugas K3 laboratorium untuk penanganan dan pembuangan limbah B3 oleh pihak berwenang.
        """,
        "daur_ulang": "Beberapa pelarut organik dapat didaur ulang melalui distilasi oleh pihak ketiga.",
        "bahaya": "Mudah terbakar, beracun, dapat menyebabkan iritasi.",
        "gambar": "pelarut_organik.jpg"
    },
    "Sisa Asam/Basa Kuat (Jumlah Kecil)": {
        "kategori": "Cair (Kimia B3)",
        "deskripsi": "Sisa asam atau basa kuat dalam jumlah kecil.",
        "pengolahan": """
            1. Netralkan asam dengan basa lemah atau sebaliknya secara perlahan dan hati-hati di bawah lemari asam.
            2. Periksa pH larutan yang dinetralkan sebelum dibuang.
            3. Kumpulkan limbah yang telah dinetralkan sebagai limbah B3 dan serahkan ke petugas K3.
        """,
        "daur_ulang": "Umumnya tidak didaur ulang setelah netralisasi.",
        "bahaya": "Korosif, dapat menyebabkan luka bakar.",
        "gambar": "asam_basa.jpg"
    },
    "Kultur Bakteri/Jamur Bekas (Sudah Diotoklaf)": {
        "kategori": "Biohazard (Non-Aktif)",
        "deskripsi": "Kultur bakteri atau jamur bekas yang telah diinaktivasi melalui autoklaf.",
        "pengolahan": """
            1. Pastikan proses autoklaf telah berjalan dengan benar.
            2. Buang kultur yang telah diotoklaf ke dalam wadah limbah biohazard yang sesuai.
            3. Beberapa plastik bekas cawan petri mungkin dapat didaur ulang setelah sterilisasi (periksa kebijakan kampus).
        """,
        "daur_ulang": "Tergantung kebijakan daur ulang limbah biohazard di kampus.",
        "bahaya": "Potensi kontaminasi jika autoklaf tidak sempurna.",
        "gambar": "kultur_bakteri.jpg"
    },
    "Cawan Petri Bekas (Sudah Diotoklaf)": {
        "kategori": "Plastik (Biohazard)",
        "deskripsi": "Cawan petri bekas yang telah diinaktivasi melalui autoklaf.",
        "pengolahan": """
            1. Pastikan proses autoklaf selesai.
            2. Buang ke wadah limbah biohazard.
            3. Jika ada program daur ulang plastik limbah biohazard, ikuti prosedurnya.
        """,
        "daur_ulang": "Tergantung kebijakan daur ulang limbah biohazard di kampus.",
        "bahaya": "Potensi kontaminasi jika autoklaf tidak sempurna.",
        "gambar": "cawan_petri.jpg"
    },
    "Jarum Suntik Bekas": {
        "kategori": "Tajam (Biohazard)",
        "deskripsi": "Jarum suntik bekas yang berpotensi terkontaminasi agen biologis atau bahan kimia berbahaya.",
        "pengolahan": """
            1. Jangan menekuk atau mematahkan jarum.
            2. Segera buang jarum bekas ke dalam wadah penampung benda tajam (safety box) yang sesuai.
            3. Wadah safety box yang sudah penuh harus ditutup rapat dan diserahkan ke petugas K3 laboratorium untuk pembuangan limbah medis yang aman.
        """,
        "daur_ulang": "Tidak didaur ulang karena risiko kontaminasi.",
        "bahaya": "Potensi luka tusuk dan penularan penyakit.",
        "gambar": "jarum_suntik.jpg"
    },
    "Botol Vial Bekas (Bekas Sampel Biologi)": {
        "kategori": "Gelas/Plastik (Biohazard)",
        "deskripsi": "Botol vial bekas tempat penyimpanan sampel biologis.",
        "pengolahan": """
            1. Sterilisasi botol vial dengan autoklaf atau disinfektan kimia yang sesuai.
            2. Setelah sterilisasi, botol gelas dapat dibuang ke limbah gelas daur ulang (periksa kebijakan kampus).
            3. Botol plastik bekas sampel biohazard umumnya dibuang sebagai limbah biohazard.
        """,
        "daur_ulang": "Botol gelas setelah sterilisasi mungkin dapat didaur ulang.",
        "bahaya": "Potensi kontaminasi biologis.",
        "gambar": "botol_vial.jpg"
    },
}

# Fungsi untuk klasifikasi sampah laboratorium
def klasifikasi_sampah_lab_detail(jenis_sampah):
    jenis_sampah_lower = jenis_sampah.lower()
    for key, value in data_sampah_lab_detail.items():
        if key.lower() in jenis_sampah_lower:
            return value
    return {
        "kategori": "Tidak Teridentifikasi",
        "deskripsi": "Jenis sampah laboratorium tidak dikenali oleh sistem.",
        "pengolahan": "Harap konsultasikan dengan petugas K3 Laboratorium untuk penanganan yang tepat.",
        "daur_ulang": "Informasi daur ulang tidak tersedia.",
        "bahaya": "Potensi bahaya tidak diketahui, tangani dengan hati-hati.",
        "gambar": "tidak_ditemukan.jpg"  # Placeholder untuk gambar tidak ditemukan
    }

# Fungsi utama aplikasi Streamlit
def main():
    st.title("Aplikasi Pemilihan dan Pengolahan Sampah Laboratorium")
    st.subheader("Panduan detail pengelolaan sampah laboratorium yang aman dan sesuai.")

    jenis_input = st.text_input("Masukkan Jenis Sampah Laboratorium:", placeholder="Contoh: Gelas Kimia Bekas")

    if st.button("Cari Informasi"):
        if jenis_input:
            hasil = klasifikasi_sampah_lab_detail(jenis_input)
            st.subheader(f"Informasi Detail untuk '{jenis_input}':")
            st.write(f"**Deskripsi:** {hasil['deskripsi']}")
            st.write(f"**Kategori:** {hasil['kategori']}")
            st.write(f"**Panduan Pengolahan:**")
            st.markdown(hasil['pengolahan'])
            st.write(f"**Potensi Daur Ulang:** {hasil['daur_ulang']}")
            st.warning(f"**Potensi Bahaya:** {hasil['bahaya']}")
            if "gambar" in hasil and hasil["gambar"]:
                try:
                    image = Image.open(hasil["gambar"])  # Membutuhkan Pillow (PIL)
                    st.image(image, caption=f"Gambar {jenis_input}", use_column_width=True)
                except FileNotFoundError:
                    st.error(f"Gambar '{hasil['gambar']}' tidak ditemukan.")
        else:
            st.warning("Mohon masukkan jenis sampah laboratorium.")

    st.markdown("---")
    st.info("""
        **Penting:** Aplikasi ini menyediakan panduan umum. Selalu prioritaskan protokol keselamatan dan pengelolaan limbah laboratorium yang berlaku di kampus Anda.
        Konsultasikan dengan petugas K3 Laboratorium untuk penanganan limbah yang tidak teridentifikasi, berbahaya, atau memerlukan prosedur khusus.
    """)

    st.subheader("Daftar Contoh Sampah Laboratorium dan Informasi Singkat:")
    data_singkat = {key: {"Kategori": value["kategori"], "Deskripsi": value["deskripsi"]} for key, value in data_sampah_lab_detail.items()}
    df_singkat = pd.DataFrame.from_dict(data_singkat, orient='index')
    st.dataframe(df_singkat)

    # Potensi Visualisasi (Membutuhkan Data Lebih Lanjut)
    st.subheader("Visualisasi Data Sampah (Contoh):")
    kategori_sampah = [item["kategori"] for item in data_sampah_lab_detail.values()]
    df_visual = pd.DataFrame({"Kategori": kategori_sampah})
    fig = px.histogram(df_visual, x="Kategori", title="Distribusi Kategori Sampah Laboratorium (Contoh)")
    st.plotly_chart(fig)

    st.markdown("---")
    st.subheader("Kontak Petugas K3 Laboratorium:")
    st.write("- Nama Petugas: [Nama Petugas K3]")
    st.write("- Email: [alamat.email.k3@kampus.ac.id]")
    st.write("- Nomor Telepon: [nomor telepon K3]")

if __name__ == "__main__":
    from PIL import Image  # Import di sini jika modul Pillow digunakan
    main()
