# Audit dan pengembangan `Linear Spin-Wave Theory.ipynb`

## Status akhir

Notebook pengganti telah dijalankan ulang dari kernel bersih. Semua 10 sel kode memiliki execution count berurutan 1–10, tidak ada error output, seluruh 13 pengujian berstatus `PASS`, dan seluruh kolom numerik pada enam file CSV bernilai finite.

Parameter default yang dieksekusi:

- `S = 1`
- `J1 = 1`
- `J2 = 0.5`
- `a = 1`
- konvensi Hamiltonian `H = + sum J_r S_j . S_(j+r)`, setiap bond dihitung sekali
- `n_q = 501`, tanpa duplikasi endpoint periodik
- `n_omega = 600`
- Gaussian broadening `sigma = 0.03`
- `T = 0`

Hasil ground state default adalah spiral dengan

`Q = 2.094395102393 = 2 pi / 3`, `E_cl/N = -0.75`, `dE/dQ = 2.220e-16`, dan `d2E/dQ2 = 1.5`.

## Bug dan kekurangan notebook lama

1. Fallback penentuan ground state memilih `Q=0` ketika solusi spiral tidak tersedia. Ini dapat salah untuk fase antiferomagnetik `Q=pi`.
2. Stationary point tidak dibandingkan secara global. Notebook baru mengevaluasi kandidat FM, AF, dan spiral, lalu memilih energi klasik minimum dan melaporkan degenerasi batas fase.
3. Bentuk `A(q)` dan `B(q)` lama sebenarnya konsisten dengan konvensi bond-once, tetapi tidak diverifikasi terhadap bentuk kompak berbasis `J(k)` sehingga sign/factor-of-two error sulit dideteksi.
4. Diagonalisasi lama hanya menyortir eigenvalue dari `eta H_BdG`. Itu belum cukup untuk masalah bosonik: mode fisik harus mempunyai energi positif sekaligus norma bosonik positif.
5. Fungsi normalisasi bosonik tersedia tetapi tidak diterapkan pada mode yang dipakai.
6. Tidak ada pengecekan Hermiticity, residual eigenproblem, pasangan `+-epsilon`, norma bosonik, maupun kondisi paraunitary.
7. Goldstone mode dibuang dari intensitas memakai ambang energi. Notebook baru mempertahankan energi fisik tepat nol.
8. Exact zero-mode mempunyai eigenvector zero-norm dan tidak dapat dinormalisasi dengan pembagian biasa. Notebook baru memisahkan energi exact, residual exact, dan eigenvector regularized khusus matrix element spektral.
9. Intensitas lama memakai bobot fenomenologis `W_n=1`. Notebook baru membangun operator spin laboratorium dan menghitung matrix element satu-magnon dari koefisien Bogoliubov `u,v`.
10. Form factor `exp(-0.1 q^2)` sebelumnya bersifat toy tetapi tampak seperti pilihan fisik. Default baru adalah `F(Q)=1`; callable/tabulated physical form factor dapat diberikan secara eksplisit.
11. Polarization projector neutron tidak tersedia. Interface baru menerima vektor momentum tiga dimensi dan menghitung `delta_ab - Qhat_a Qhat_b`.
12. Bose factor lama mengubah energi kecil menjadi nol secara diam-diam. Implementasi baru menyimpan energi fisik dan memakai energy floor hanya ketika fungsi termal dievaluasi.
13. Tidak ada tensor `S^{alpha beta}(q,omega)`, pemisahan raw/broadened intensity, atau komponen `Sxx`, `Syy`, `Szz`.
14. Grid lama menyertakan `0` dan `2pi`, yaitu dua titik periodik yang sama. Grid baru berpusat di first Brillouin zone dan tidak menggandakan endpoint.
15. Execution count notebook lama tidak konsisten dan CSV ditulis relatif terhadap working directory. Notebook baru dieksekusi bersih dan menulis output deterministik ke `lswt_outputs/`.

## Fondasi matematis yang dipakai

Transform Fourier pertukaran:

`J(k) = J1 cos(ka) + J2 cos(2ka)`.

Energi klasik per spin:

`E_cl(Q)/N = S^2 [J1 cos(Q) + J2 cos(2Q)]`.

Koefisien kuadratik dalam basis Nambu `(a_q, a^dagger_-q)` memenuhi

`A_q - B_q = 2S [J(q) - J(Q/a)]`,

`A_q + B_q = S [J(q+Q/a) + J(q-Q/a) - 2J(Q/a)]`.

Karena itu

`epsilon_q^2 = 2 S^2 [J(q)-J(Q/a)] [J(q+Q/a)+J(q-Q/a)-2J(Q/a)]`.

Masalah eigen bosonik yang benar adalah

`eta H_BdG(q) t_n(q) = epsilon_n(q) t_n(q)`, dengan `eta = diag(1,-1)`.

Mode fisik dipilih menggunakan `epsilon_n > 0` dan `t_n^dagger eta t_n > 0`, lalu dinormalisasi menjadi `t_n^dagger eta t_n = 1`.

## Penanganan Goldstone

Untuk parameter spiral default terdapat tiga zero mode pada grid, yaitu `q=0` dan `q=+-Q/a`. Energi pada CSV tetap tepat nol. Karena eigenvector exact di titik tersebut zero-norm, notebook menggunakan `H_BdG + delta_G I` dengan `delta_G=1e-6` hanya untuk mendefinisikan finite-resolution matrix element. Kolom berikut membuat perlakuan ini transparan:

- `spectral_regularized`
- `exact_paraunitary_defined`
- `paraunitary_source`
- `stability_flag`

## Hasil diagnostik default

- maksimum Hermiticity error: `0`
- maksimum residual BdG: `5.448e-16`
- maksimum imaginary-energy diagnostic: `9.587e-13`
- maksimum eigenvalue-pair error: `1.554e-15`
- maksimum paraunitary error: `2.098e-13`
- periodicity error: `1.533e-14`
- minimum energi fisik: `0`
- jumlah Goldstone pada grid: `3`

## Pengujian otomatis

Semua pengujian berikut lulus:

1. nearest-neighbor ferromagnet: `epsilon(q)=2S|J1|[1-cos(qa)]`
2. nearest-neighbor antiferromagnet: `epsilon(q)=2SJ1|sin(qa)|`
3. spiral `J1-J2`
4. batas fase `|J1/(4J2)|=1`
5. kesetaraan bentuk `A/B` dan bentuk kompak `J(k)`
6. Hermiticity matriks BdG
7. residual eigenproblem bosonik
8. tidak ada imaginary energy yang signifikan
9. kondisi paraunitary
10. periodicity reciprocal lattice
11. normalisasi integral Gaussian
12. Hermiticity tensor spektral
13. transverse one-magnon sum rule untuk feromagnet

## Isi ekspor

- `classical_ground_state.csv`: fase, pitch, dan energi klasik.
- `spin_wave_dispersion.csv`: energi, `A_q`, `B_q`, `u,v`, norma, residual, dan seluruh status BdG/Goldstone.
- `one_magnon_matrix_elements.csv`: matrix element kompleks dan bobot `xx`, `yy`, `zz` setiap transition.
- `dynamical_structure_factor.csv`: `Sxx`, `Syy`, `Szz`, transverse sum, raw intensity, dan broadened intensity.
- `neutron_intensity.csv`: structure factor, Bose factor, form factor, polarization factor, dan intensity akhir.
- `validation_results.csv`: nilai dan status semua pengujian.

Tidak ada normalisasi maksimum atau rescaling tersembunyi pada CSV.

## Batasan yang tetap berlaku

Model saat ini satu dimensi dengan satu spin per primitive cell dan hanya menghitung sektor satu-magnon LSWT. Kontribusi longitudinal lokal utama membutuhkan two-magnon continuum. Absolute neutron cross-section masih memerlukan identitas ion, `g`-tensor, Debye-Waller factor, absolute momentum transfer, jumlah ion, dan prefaktor instrumen.
