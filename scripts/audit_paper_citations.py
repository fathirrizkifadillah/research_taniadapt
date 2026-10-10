import os
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(r"c:\CODING\research_taniAdapt")
AUDIT_DIR = PROJECT_ROOT / "reports"

citation_records = [
    {
        "klaim_di_taniadapt": "LINK_03: STRONG on microclimate disease (Paper 3 & 5) & Ambang batas curah hujan/RH",
        "paper_ref": "Paper 3 (Madasamy et al., 2020)",
        "tanaman_di_paper": "Kapas (Cotton, varietas SVPR 2)",
        "lokasi_di_paper": "Kovilpatti, Tamil Nadu, India (black-soil)",
        "kesesuaian_tanaman_dan_lokasi": "TIDAK SAMA (Kapas di India)",
        "kutipan_asli_paper": "Forewarning system for pests and diseases in cotton (Thrips, Leafhopper, Spodoptera, Stem weevil, Bollworm, Root rot) using microclimate temperature, rainfall, and RH.",
        "status_verifikasi": "TRANSFER DARI TANAMAN LAIN & LOKASI LAIN"
    },
    {
        "klaim_di_taniadapt": "LINK_03: STRONG on microclimate disease (Paper 3 & 5) & Ulasan algoritma prediksi penyakit",
        "paper_ref": "Paper 5 (Fenu & Malloci, 2021)",
        "tanaman_di_paper": "Multi-crop literature survey (Dominan: padi, gandum, kentang, apel, anggur)",
        "lokasi_di_paper": "Global / Systematic Review",
        "kesesuaian_tanaman_dan_lokasi": "TIDAK SAMA (Review algoritma multi-tanaman, bukan studi empiris cabai)",
        "kutipan_asli_paper": "Explorative study on algorithms predicting plant/crop diseases. Highlighting fungal diseases relation to temperature and leaf wetness duration.",
        "status_verifikasi": "TRANSFER DARI TANAMAN LAIN & LOKASI LAIN"
    },
    {
        "klaim_di_taniadapt": "Ambang batas pola hari hujan & curah hujan antraknosa (Paper 6)",
        "paper_ref": "Paper 6 (Nurhayati & Situmorang, 2020)",
        "tanaman_di_paper": "Karet (Hevea brasiliensis, klon RRIM 600)",
        "lokasi_di_paper": "PTP VII Bergen, Lampung, Indonesia",
        "kesesuaian_tanaman_dan_lokasi": "TIDAK SAMA (Karet di Lampung)",
        "kutipan_asli_paper": "Pengaruh pola hari hujan terhadap perkembangan penyakit gugur daun Corynespora pada tanaman karet.",
        "status_verifikasi": "TRANSFER DARI TANAMAN LAIN"
    },
    {
        "klaim_di_taniadapt": "LINK_03: Bukti statistik cuaca terhadap yield cabai di Indonesia belum cukup signifikan pada skala tahunan",
        "paper_ref": "Paper 7 (Handhayani et al., 2026)",
        "tanaman_di_paper": "Kakao, kopi, kelapa sawit, cabai rawit (cayenne), padi",
        "lokasi_di_paper": "Indonesia (Kabupaten/Kota penghasil komoditas, 100 stasiun BMKG)",
        "kesesuaian_tanaman_dan_lokasi": "SESUAI UNTUK CABAI RAWIT DI INDONESIA",
        "kutipan_asli_paper": "Untuk cabai rawit, bukti statistik bahwa meteorologi memengaruhi hasil panen (yield) dinilai belum cukup dalam paper ini (data tahunan 2018–2024).",
        "status_verifikasi": "SESUAI (Secara eksplisit menyatakan bukti statistik cuaca -> yield cabai rawit belum cukup pada data tahunan)"
    },
    {
        "klaim_di_taniadapt": "Brief Padi: Kenaikan suhu ekstrim dan banjir menurunkan hasil padi di Jawa Barat (Paper 12)",
        "paper_ref": "Paper 12 (Hosokawa et al., 2023)",
        "tanaman_di_paper": "Padi (Rice - multi-rice cropping)",
        "lokasi_di_paper": "Asia Selatan & Asia Tenggara (6 negara: Bangladesh, Indonesia, Malaysia, Myanmar, Filipina, Thailand, grid 0.5°)",
        "kesesuaian_tanaman_dan_lokasi": "TRANSFER DARI LOKASI LAIN / REGIONAL ASIA (Bukan studi spesifik Jawa Barat)",
        "kutipan_asli_paper": "Contrasting area and yield responses to extreme climate (CDD, CWD, R10mm, R95pTOT). Out-of-sample R yield = 0.994 di 6 negara via Elastic Net.",
        "status_verifikasi": "TRANSFER DARI LOKASI LAIN (Klaim R2 < 0.1 di Jawa Barat berasal dari regresi data DS03 lokal di repo, bukan dari teks Paper 12)"
    },
    {
        "klaim_di_taniadapt": "Brief Padi: Dampak perubahan iklim terhadap produksi padi di Jawa Barat (Paper 15)",
        "paper_ref": "Paper 15 (Ansari et al., 2021)",
        "tanaman_di_paper": "Padi (Ciherang)",
        "lokasi_di_paper": "Gemawang, Girimarto, Kabupaten Wonogiri, JAWA TENGAH",
        "kesesuaian_tanaman_dan_lokasi": "TRANSFER DARI LOKASI LAIN (Wonogiri Jawa Tengah, bukan Jawa Barat)",
        "kutipan_asli_paper": "Evaluating and adapting climate change impacts on rice production in Keduang Subwatershed, Wonogiri, Central Java using CropSyst model.",
        "status_verifikasi": "TRANSFER DARI LOKASI LAIN"
    },
    {
        "klaim_di_taniadapt": "Brief Jagung: Expected signal STRONG (Paper 13)",
        "paper_ref": "Paper 13 (Heino et al., 2023)",
        "tanaman_di_paper": "Gandum, jagung (maize), kedelai, padi",
        "lokasi_di_paper": "GLOBAL (20.000 political units, grid 0.5°)",
        "kesesuaian_tanaman_dan_lokasi": "TRANSFER DARI LOKASI LAIN (Kajian global lintang sedang/dunia)",
        "kutipan_asli_paper": "Compound hot and dry extremes during growing season reduce global crop yields. Kenaikan suhu 1 C menurunkan yield jagung ~7.5% secara global.",
        "status_verifikasi": "TRANSFER DARI LOKASI LAIN (Kuat secara global, belum terbukti untuk tropis Jawa Barat)"
    },
    {
        "klaim_di_taniadapt": "Brief Jagung: Expected signal STRONG (Paper 14)",
        "paper_ref": "Paper 14 (Hu et al., 2024)",
        "tanaman_di_paper": "Systematic Review multi-crop (jagung, gandum, kedelai, padi)",
        "lokasi_di_paper": "GLOBAL (50% studi di AS & Eropa, 10% China, 8% India)",
        "kesesuaian_tanaman_dan_lokasi": "TRANSFER DARI LOKASI LAIN (Didominasi iklim sedang)",
        "kutipan_asli_paper": "Review of empirical findings and statistical crop models. Dominasi literatur berada di wilayah iklim sedang.",
        "status_verifikasi": "TRANSFER DARI LOKASI LAIN"
    },
    {
        "klaim_di_taniadapt": "Brief Cabai: Jamur antraknosa (Colletotrichum) sensitif terhadap kelembaban jenuh",
        "paper_ref": "Paper di Repo (Paper 1 s.d. 15)",
        "tanaman_di_paper": "Tidak ada paper tentang antraknosa cabai di repo",
        "lokasi_di_paper": "Tidak ada",
        "kesesuaian_tanaman_dan_lokasi": "TIDAK ADA DI PAPER",
        "kutipan_asli_paper": "Tidak ditemukan penyebutan antraknosa atau Colletotrichum dalam 15 paper riset repo.",
        "status_verifikasi": "PENGETAHUAN UMUM, BUKAN EVIDENCE REPO"
    },
    {
        "klaim_di_taniadapt": "Brief Bawang Merah: Rentan genangan air & penyakit layu moler (Fusarium oxysporum)",
        "paper_ref": "Paper di Repo (Paper 1 s.d. 15)",
        "tanaman_di_paper": "Tidak ada paper tentang bawang merah di repo",
        "lokasi_di_paper": "Tidak ada",
        "kesesuaian_tanaman_dan_lokasi": "TIDAK ADA DI PAPER",
        "kutipan_asli_paper": "Tidak ditemukan penyebutan bawang merah atau Fusarium cepae dalam 15 paper riset repo.",
        "status_verifikasi": "PENGETAHUAN UMUM, BUKAN EVIDENCE REPO"
    }
]

df_citations = pd.DataFrame(citation_records)
out_csv = AUDIT_DIR / "citation_audit_matrix.csv"
df_citations.to_csv(out_csv, index=False)
print(f"Berhasil membuat tabel audit sitasi: {out_csv}")
print(df_citations[['paper_ref', 'tanaman_di_paper', 'status_verifikasi']].to_string(index=False))
