# Log Riwayat Git Tag & Kriptografi Hash Repositori (TaniAdapt)

Dokumen ini mencatat riwayat hash git tag historis untuk menjamin integritas audit dan *experiment provenance ledger*.

## 1. Riwayat Tag Historis

| Tag Name | Tag Object Hash | Target Commit Hash | Short Commit | Pesan / Keterangan Tag | Tanggal |
|---|---|---|:---:|---|:---:|
| `v2-audit-closure` | `7b645d2652ba52063e4da3313f8a7994cc39a7be` | `f733079d4352d5c0663ab6bca3b7a347a3a15060` | `f733079` | TaniAdapt Complete PhD-Level EDA Dossier | 2026-10-12 |
| `audit-v3` | `6df2e920cf9c5d93ed47de6d3c658edc29569121` | `1aa2e016a4be74712adbf898436eb4b4c73bf5f0` | `1aa2e01` | Penutupan Perbaikan Reviewer: Outlier Jagung/Kedelai, MDE 2.8xSE, IFWC RH06/Depresiasi, CHIRPS Dalam-Tahun/Unit, PCA Demeaned, BPS Metadata | 2026-10-12 |

## 2. Riwayat Commit Terkait
- `f733079` (`f733079d4352d5c0663ab6bca3b7a347a3a15060`): docs: generate expanded PhD-level data science research dossier (.docx) with full mathematical framework and embedded figures
- `bd5955d` (`bd5955d9e3da5f8ade99c6399e661a3852113393`): docs: generate comprehensive EDA report document (.docx) with embedded figures and tables
- `1455e70` (`1455e70c9a1d2875146bd0d90b12c0ef795364ea`): refactor(notebooks): separate Phase 6 EDA into modular per-figure cells
- `6d1647e` (`6d1647e3d7cb5f07b691d28a516ef5115210b0b4`): chore: clean up internal scaffolding, obsolete archives, and redundant figures
- `be888fa` (`be888fa17226d6d516966d956cbf66c897a19cff`): feat(phase5-6): complete audit closure, crop selection decision, and modular 10-notebook EDA
- `38900cf` (`38900cf2df7db445a4437a3424d6731e843f9a74`): docs(dataset_exp): clean up LaTeX and escape characters across all 10 dataset docs

## 3. Ketentuan Integritas
- Tag `v2-audit-closure` tidak dipindahkan (`immutable`).
- Tag `audit-v3` mengunci versi perbaikan reviewer secara permanen.
