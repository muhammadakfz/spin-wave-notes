# Spin-Wave Theory dari Nol sampai Hamiltonian Umum

## Catatan derivasi rinci dan implementation-ready

Dokumen ini menyusun ulang empat sumber berikut menjadi satu alur yang konsisten:

1. *Notes Spinwave CH1 - Semiklasik*.
2. *Notes Spinwave CH2 - Kuantum*.
3. *Spin-Wave Theory and its Applications to Neutron Scattering and THz Spectroscopy*, terutama Bab 4.
4. Scan tulisan tangan *Hamiltonian.pdf*.

Target akhirnya bukan hanya mengetahui hasil

\[
\hbar\omega_{\mathbf q},
\]

tetapi memahami bagaimana Hamiltonian mikroskopik diubah menjadi Hamiltonian bosonik kuadratik

\[
H_2
=
\frac12\sum_{\mathbf q}
\Psi_{\mathbf q}^{\dagger}
\mathcal H_{\mathrm{BdG}}(\mathbf q)
\Psi_{\mathbf q}
+C,
\]

atau, dalam notasi yang dipakai scan tulisan tangan,

\[
H_2
=
\sum_{\mathbf q}
V_{\mathbf q}^{\dagger}
L(\mathbf q)
V_{\mathbf q}.
\]

Dokumen ini sengaja menggunakan satu konvensi yang tegas supaya nantinya bisa langsung diterjemahkan menjadi program. Hubungan dengan konvensi notes dijelaskan setiap kali ada faktor \(2\), tanda minus, atau urutan operator yang berbeda.

---

# Bagian I - Konvensi yang harus dikunci sebelum menghitung

## 1. Indeks, posisi, dan satuan

Gunakan indeks berikut:

- \(i,j\): indeks situs fisik secara umum.
- \(\ell\): indeks magnetic unit cell.
- \(r,s=1,\ldots,M\): indeks sublattice di dalam satu magnetic unit cell.
- \(M\): jumlah spin dalam satu magnetic unit cell.
- \(N_c\): jumlah magnetic unit cell.
- \(\mathbf R_\ell\): posisi origin unit cell ke-\(\ell\).
- \(\boldsymbol\tau_r\): posisi sublattice \(r\) relatif terhadap origin unit cell.
- \(\mathbf r_{\ell r}=\mathbf R_\ell+\boldsymbol\tau_r\): posisi fisik spin \((\ell,r)\).
- \(S_r\): besar spin pada sublattice \(r\).
- \(a\): jarak kisi untuk contoh rantai 1D.
- \(\mathbf q\): wavevector atau momentum kristal.

Dalam dokumen ini operator spin dianggap tak berdimensi:

\[
[S_i^\alpha,S_j^\beta]
=
i\delta_{ij}\epsilon_{\alpha\beta\gamma}S_i^\gamma.
\]

Artinya eigenvalue \(S_i^z\) adalah \(m=-S,-S+1,\ldots,S\), tanpa faktor \(\hbar\). Energi magnon tetap ditulis

\[
E_{\mathbf q}=\hbar\omega_{\mathbf q}.
\]

Jika ingin memakai operator spin berdimensi, setiap operator spin memperoleh faktor \(\hbar\) dan konstanta kopling harus didefinisikan ulang. Untuk coding, jauh lebih mudah memakai spin tak berdimensi dan seluruh \(J,D,K,h\) dalam satuan energi.

## 2. Aturan menghitung bond

Ada dua konvensi yang sama-sama benar.

### Konvensi A: setiap bond disimpan satu kali

\[
H_{\mathrm{ex}}
=
-\sum_{\langle i,j\rangle}
J_{ij}\mathbf S_i\cdot\mathbf S_j.
\]

Simbol \(\langle i,j\rangle\) berarti bond \(i-j\) hanya muncul satu kali.

Ini konvensi yang direkomendasikan untuk coding.

### Konvensi B: semua pasangan berarah dijumlahkan

\[
H_{\mathrm{ex}}
=
-\frac12\sum_{i,j}
J_{ij}\mathbf S_i\cdot\mathbf S_j.
\]

Faktor \(1/2\) menghapus double counting karena \(i\to j\) dan \(j\to i\) keduanya muncul.

### Konvensi pada notes

Notes semiklasik dan kuantum beberapa kali memakai

\[
H=-2J\sum_p\mathbf S_p\cdot\mathbf S_{p+1}.
\]

Karena itu dispersi notes menjadi

\[
\hbar\omega_k=4JS[1-\cos(ka)],
\]

sedangkan untuk Hamiltonian bond-once

\[
H=-J\sum_p\mathbf S_p\cdot\mathbf S_{p+1}
\]

hasilnya

\[
\hbar\omega_k=2JS[1-\cos(ka)].
\]

Jangan mencampur kedua definisi ini di dalam program.

## 3. Konvensi tanda exchange

Dokumen ini memakai

\[
H_{\mathrm{ex}}
=
-\sum_{\langle i,j\rangle}
J_{ij}\mathbf S_i\cdot\mathbf S_j.
\]

Untuk satu bond,

\[
E_{ij}
=
-J_{ij}S_iS_j\cos\theta_{ij}.
\]

Maka:

- \(J_{ij}>0\): feromagnetik, minimum pada \(\theta_{ij}=0\).
- \(J_{ij}<0\): antiferomagnetik, minimum pada \(\theta_{ij}=\pi\).

Konvensi lain yang sering dipakai adalah

\[
H=+\sum_{\langle i,j\rangle}J_{ij}^{\mathrm{AF}}
\mathbf S_i\cdot\mathbf S_j
\]

dengan \(J_{ij}^{\mathrm{AF}}>0\) untuk antiferomagnet. Hubungannya

\[
J_{ij}^{\mathrm{AF}}=-J_{ij}.
\]

---

# Bagian II - Dari spin individual ke spin wave semiklasik

## 4. Apa yang sebenarnya bergerak?

Sebuah spin klasik dapat ditulis

\[
\mathbf S_p
=
\begin{pmatrix}
S_p^x\\
S_p^y\\
S_p^z
\end{pmatrix},
\qquad
|\mathbf S_p|=S.
\]

Pada feromagnet dengan ground state sepanjang \(+z\),

\[
\mathbf S_p^{(0)}
=
\begin{pmatrix}
0\\0\\S
\end{pmatrix}.
\]

Spin wave adalah simpangan kecil

\[
S_p^x,S_p^y\ll S,
\qquad
S_p^z\simeq S.
\]

Karena panjang spin tetap,

\[
(S_p^x)^2+(S_p^y)^2+(S_p^z)^2=S^2.
\]

Jadi secara lebih teliti,

\[
S_p^z
=
\sqrt{S^2-(S_p^x)^2-(S_p^y)^2}.
\]

Gunakan

\[
\sqrt{1-x}\simeq1-\frac{x}{2}
\]

untuk mendapatkan

\[
S_p^z
\simeq
S-\frac{(S_p^x)^2+(S_p^y)^2}{2S}.
\]

Pada teori linear, suku kuadrat dibuang sehingga \(S_p^z\simeq S\).

## 5. Persamaan gerak dari Hamiltonian

Ambil rantai feromagnet 1D

\[
H
=
-J\sum_p
\mathbf S_p\cdot\mathbf S_{p+1}.
\]

Spin \(p\) muncul pada dua bond:

\[
-J\mathbf S_{p-1}\cdot\mathbf S_p
\]

dan

\[
-J\mathbf S_p\cdot\mathbf S_{p+1}.
\]

Karena itu

\[
\frac{\partial H}{\partial\mathbf S_p}
=
-J\mathbf S_{p-1}
-J\mathbf S_{p+1}.
\]

Persamaan geraknya adalah

\[
\hbar\frac{d\mathbf S_p}{dt}
=
-\mathbf S_p\times
\frac{\partial H}{\partial\mathbf S_p}.
\]

Substitusi menghasilkan

\[
\boxed{
\hbar\frac{d\mathbf S_p}{dt}
=
J\mathbf S_p\times
(\mathbf S_{p-1}+\mathbf S_{p+1})
}.
\]

Ini ekuivalen dengan pendekatan medan efektif dan presesi Larmor di notes semiklasik.

## 6. Ekspansi cross product tanpa melewatkan langkah

Definisikan

\[
\mathbf T_p
=
\mathbf S_{p-1}+\mathbf S_{p+1}
=
\begin{pmatrix}
S_{p-1}^x+S_{p+1}^x\\
S_{p-1}^y+S_{p+1}^y\\
S_{p-1}^z+S_{p+1}^z
\end{pmatrix}.
\]

Cross product adalah

\[
\mathbf S_p\times\mathbf T_p
=
\begin{vmatrix}
\hat{\mathbf x}&\hat{\mathbf y}&\hat{\mathbf z}\\
S_p^x&S_p^y&S_p^z\\
T_p^x&T_p^y&T_p^z
\end{vmatrix}.
\]

Komponen \(x\):

\[
(\mathbf S_p\times\mathbf T_p)_x
=
S_p^yT_p^z-S_p^zT_p^y.
\]

Substitusi \(T_p\):

\[
=
S_p^y(S_{p-1}^z+S_{p+1}^z)
-S_p^z(S_{p-1}^y+S_{p+1}^y).
\]

Dengan \(S_p^z,S_{p\pm1}^z\simeq S\):

\[
=
2SS_p^y-S(S_{p-1}^y+S_{p+1}^y).
\]

Maka

\[
\boxed{
\frac{dS_p^x}{dt}
=
\frac{JS}{\hbar}
\left[
2S_p^y-S_{p-1}^y-S_{p+1}^y
\right]
}.
\]

Komponen \(y\):

\[
(\mathbf S_p\times\mathbf T_p)_y
=
S_p^zT_p^x-S_p^xT_p^z.
\]

Jadi

\[
=
S(S_{p-1}^x+S_{p+1}^x)-2SS_p^x
\]

atau

\[
\boxed{
\frac{dS_p^y}{dt}
=
-\frac{JS}{\hbar}
\left[
2S_p^x-S_{p-1}^x-S_{p+1}^x
\right]
}.
\]

Komponen \(z\):

\[
(\mathbf S_p\times\mathbf T_p)_z
=
S_p^xT_p^y-S_p^yT_p^x.
\]

Semua sukunya berupa produk dua simpangan kecil, misalnya \(S_p^xS_{p+1}^y\). Itu orde kedua, sehingga dalam teori linear

\[
\boxed{
\frac{dS_p^z}{dt}\simeq0
}.
\]

## 7. Solusi gelombang berjalan dan asal fungsi cosinus

Ambil ansatz

\[
S_p^x=u\,e^{i(pka-\omega t)},
\]

\[
S_p^y=v\,e^{i(pka-\omega t)}.
\]

Turunan waktunya

\[
\frac{dS_p^x}{dt}
=
-i\omega u\,e^{i(pka-\omega t)},
\]

\[
\frac{dS_p^y}{dt}
=
-i\omega v\,e^{i(pka-\omega t)}.
\]

Untuk tetangga kiri,

\[
S_{p-1}^y
=
v e^{i[(p-1)ka-\omega t]}
\]

\[
=
v e^{i(pka-\omega t)}e^{-ika}.
\]

Untuk tetangga kanan,

\[
S_{p+1}^y
=
v e^{i[(p+1)ka-\omega t]}
\]

\[
=
v e^{i(pka-\omega t)}e^{ika}.
\]

Jumlahnya

\[
S_{p-1}^y+S_{p+1}^y
=
v e^{i(pka-\omega t)}
(e^{-ika}+e^{ika}).
\]

Gunakan identitas Euler

\[
e^{ix}=\cos x+i\sin x,
\]

\[
e^{-ix}=\cos x-i\sin x,
\]

sehingga

\[
e^{ix}+e^{-ix}=2\cos x.
\]

Jadi

\[
S_{p-1}^y+S_{p+1}^y
=
2\cos(ka)S_p^y.
\]

Substitusi ke persamaan \(x\):

\[
-i\omega u e^{i(pka-\omega t)}
=
\frac{JS}{\hbar}
\left[
2v e^{i(pka-\omega t)}
-2v\cos(ka)e^{i(pka-\omega t)}
\right].
\]

Coret faktor eksponensial yang tidak nol:

\[
-i\omega u
=
\frac{2JS}{\hbar}[1-\cos(ka)]v.
\]

Dengan cara sama:

\[
-i\omega v
=
-\frac{2JS}{\hbar}[1-\cos(ka)]u.
\]

Definisikan

\[
\Omega_k
=
\frac{2JS}{\hbar}[1-\cos(ka)].
\]

Sistem linear menjadi

\[
\begin{pmatrix}
-i\omega&-\Omega_k\\
\Omega_k&-i\omega
\end{pmatrix}
\begin{pmatrix}u\\v\end{pmatrix}
=0.
\]

Agar \(u,v\) tidak keduanya nol,

\[
\det
\begin{pmatrix}
-i\omega&-\Omega_k\\
\Omega_k&-i\omega
\end{pmatrix}
=0.
\]

Ekspansi determinan:

\[
(-i\omega)(-i\omega)-(-\Omega_k)(\Omega_k)=0.
\]

Karena

\[
(-i)^2=-1,
\]

maka

\[
-\omega^2+\Omega_k^2=0.
\]

Jadi

\[
\omega=\pm\Omega_k.
\]

Ambil cabang energi positif:

\[
\boxed{
\hbar\omega_k
=
2JS[1-\cos(ka)]
}.
\]

Untuk konvensi notes \(H=-2J\sum_p\mathbf S_p\cdot\mathbf S_{p+1}\), seluruh ruas kanan persamaan gerak dikali dua:

\[
\boxed{
\hbar\omega_k^{\mathrm{notes}}
=
4JS[1-\cos(ka)]
}.
\]

## 8. Limit panjang gelombang besar

Deret Taylor cosinus:

\[
\cos x
=
1-\frac{x^2}{2!}+\frac{x^4}{4!}-\cdots.
\]

Untuk \(ka\ll1\):

\[
1-\cos(ka)
\simeq
\frac{(ka)^2}{2}.
\]

Maka

\[
\hbar\omega_k
\simeq
JS(ka)^2.
\]

Jadi feromagnet memiliki dispersi kuadratik di dekat \(k=0\).

## 9. Easy-axis anisotropy secara lengkap

Tambahkan

\[
H_D
=
-D\sum_p(S_p^z)^2.
\]

Turunannya

\[
\frac{\partial H_D}{\partial\mathbf S_p}
=
-2DS_p^z\hat{\mathbf z}.
\]

Perhatikan faktor \(2\). Ini berasal dari

\[
\frac{d}{dx}x^2=2x.
\]

Kontribusi anisotropi ke persamaan gerak:

\[
\hbar\frac{d\mathbf S_p}{dt}\bigg|_D
=
-\mathbf S_p\times
(-2DS_p^z\hat{\mathbf z})
\]

\[
=
2DS_p^z(\mathbf S_p\times\hat{\mathbf z}).
\]

Hitung

\[
\mathbf S_p\times\hat{\mathbf z}
=
\begin{vmatrix}
\hat{\mathbf x}&\hat{\mathbf y}&\hat{\mathbf z}\\
S_p^x&S_p^y&S_p^z\\
0&0&1
\end{vmatrix}
=
\begin{pmatrix}
S_p^y\\
-S_p^x\\
0
\end{pmatrix}.
\]

Dengan \(S_p^z\simeq S\):

\[
\frac{dS_p^x}{dt}\bigg|_D
=
\frac{2DS}{\hbar}S_p^y,
\]

\[
\frac{dS_p^y}{dt}\bigg|_D
=
-\frac{2DS}{\hbar}S_p^x.
\]

Persamaan lengkap:

\[
\frac{dS_p^x}{dt}
=
\frac{JS}{\hbar}
[2S_p^y-S_{p-1}^y-S_{p+1}^y]
+\frac{2DS}{\hbar}S_p^y,
\]

\[
\frac{dS_p^y}{dt}
=
-\frac{JS}{\hbar}
[2S_p^x-S_{p-1}^x-S_{p+1}^x]
-\frac{2DS}{\hbar}S_p^x.
\]

Setelah ansatz gelombang:

\[
\boxed{
\hbar\omega_k
=
2JS[1-\cos(ka)]+2DS
}.
\]

Pada \(k=0\):

\[
\boxed{
\hbar\omega_0=2DS
}.
\]

Notes menulis \(+DS\). Itu hanya konsisten bila Hamiltonian awal didefinisikan sebagai

\[
H_D=-\frac D2\sum_p(S_p^z)^2.
\]

## 10. Antiferomagnet dan kebutuhan dua sublattice

Untuk antiferomagnet gunakan, misalnya,

\[
H_{\mathrm{AF}}
=
J_{\mathrm{AF}}
\sum_p\mathbf S_p\cdot\mathbf S_{p+1},
\qquad
J_{\mathrm{AF}}>0.
\]

Ground state:

\[
\mathbf S_{2p}^{(0)}=+S\hat{\mathbf z},
\]

\[
\mathbf S_{2p+1}^{(0)}=-S\hat{\mathbf z}.
\]

Sublattice \(A\) berisi \(2p\), sedangkan sublattice \(B\) berisi \(2p+1\).

Definisikan

\[
S_p^+=S_p^x+iS_p^y.
\]

Untuk sublattice \(A\), hasil linearisasi dapat ditulis

\[
\frac{dS_{2p}^+}{dt}
=
-i\frac{J_{\mathrm{AF}}S}{\hbar}
\left[
2S_{2p}^+
+S_{2p-1}^+
+S_{2p+1}^+
\right],
\]

sedangkan untuk sublattice \(B\)

\[
\frac{dS_{2p+1}^+}{dt}
=
+i\frac{J_{\mathrm{AF}}S}{\hbar}
\left[
2S_{2p+1}^+
+S_{2p}^+
+S_{2p+2}^+
\right].
\]

Tanda berlawanan muncul karena komponen ground-state \(z\) pada kedua sublattice berlawanan.

Gunakan

\[
S_{2p}^+
=
u\,e^{i(2pka-\omega t)},
\]

\[
S_{2p+1}^+
=
v\,e^{i[(2p+1)ka-\omega t]}.
\]

Tetangga dari situs \(A\):

\[
S_{2p-1}^++S_{2p+1}^+
=
v e^{i(2pka-\omega t)}
(e^{-ika}+e^{ika})
\]

\[
=
2v\cos(ka)e^{i(2pka-\omega t)}.
\]

Setelah substitusi, diperoleh sistem dua amplitudo. Determinannya memberikan

\[
(\hbar\omega_k)^2
=
(2J_{\mathrm{AF}}S)^2
[1-\cos^2(ka)].
\]

Karena

\[
1-\cos^2x=\sin^2x,
\]

maka

\[
\boxed{
\hbar\omega_k
=
2J_{\mathrm{AF}}S|\sin(ka)|
}.
\]

Notes menggunakan exchange dua kali lebih besar, sehingga menulis

\[
\boxed{
\hbar\omega_k^{\mathrm{notes}}
=
4|J|S|\sin(ka)|
}.
\]

Untuk \(ka\ll1\),

\[
|\sin(ka)|\simeq|ka|,
\]

sehingga antiferomagnet memiliki dispersi linear di sekitar titik Goldstone.

---

# Bagian III - Deskripsi kuantum satu magnon

## 11. Ladder operator tanpa menyingkat aljabar

Definisikan

\[
S_i^+=S_i^x+iS_i^y,
\]

\[
S_i^-=S_i^x-iS_i^y.
\]

Jumlahkan:

\[
S_i^++S_i^-
=
2S_i^x,
\]

sehingga

\[
\boxed{
S_i^x=\frac{S_i^++S_i^-}{2}
}.
\]

Kurangkan:

\[
S_i^+-S_i^-
=
2iS_i^y,
\]

sehingga

\[
\boxed{
S_i^y=\frac{S_i^+-S_i^-}{2i}
}.
\]

Aksi ladder operator:

\[
S_i^+|S,m\rangle
=
\sqrt{S(S+1)-m(m+1)}
|S,m+1\rangle,
\]

\[
S_i^-|S,m\rangle
=
\sqrt{S(S+1)-m(m-1)}
|S,m-1\rangle.
\]

Pada keadaan paling atas \(m=S\):

\[
S_i^+|S,S\rangle=0,
\]

\[
S_i^-|S,S\rangle
=
\sqrt{2S}|S,S-1\rangle.
\]

Pernyataan bahwa spin hanya mempunyai dua state tepat hanya untuk \(S=1/2\). Untuk spin umum jumlah state adalah

\[
2S+1.
\]

## 12. Ekspansi dot product ke ladder operator

Mulai dari

\[
\mathbf S_i\cdot\mathbf S_j
=
S_i^xS_j^x+S_i^yS_j^y+S_i^zS_j^z.
\]

Komponen \(x\):

\[
S_i^xS_j^x
=
\frac14
(S_i^++S_i^-)(S_j^++S_j^-)
\]

\[
=
\frac14
\left(
S_i^+S_j^+
+S_i^+S_j^-
+S_i^-S_j^+
+S_i^-S_j^-
\right).
\]

Komponen \(y\):

\[
S_i^yS_j^y
=
\frac1{(2i)^2}
(S_i^+-S_i^-)(S_j^+-S_j^-).
\]

Karena

\[
(2i)^2=-4,
\]

maka

\[
S_i^yS_j^y
=
-\frac14
\left(
S_i^+S_j^+
-S_i^+S_j^-
-S_i^-S_j^+
+S_i^-S_j^-
\right).
\]

Jumlahkan \(x\) dan \(y\). Suku \(S_i^+S_j^+\) saling menghapus:

\[
\frac14-\frac14=0.
\]

Suku \(S_i^-S_j^-\) juga saling menghapus. Suku silang memberi

\[
S_i^xS_j^x+S_i^yS_j^y
=
\frac12
\left(
S_i^+S_j^-
+S_i^-S_j^+
\right).
\]

Jadi

\[
\boxed{
\mathbf S_i\cdot\mathbf S_j
=
S_i^zS_j^z
+\frac12
\left(
S_i^+S_j^-
+S_i^-S_j^+
\right)
}.
\]

## 13. Ground state feromagnet dan basis satu spin flip

Ground state:

\[
|0\rangle
=
|S,S;\,S,S;\,\ldots;\,S,S\rangle.
\]

Definisikan keadaan satu spin flip di situs \(j\):

\[
|j\rangle
=
\frac1{\sqrt{2S}}S_j^-|0\rangle.
\]

Untuk Hamiltonian

\[
H=-J\sum_i\mathbf S_i\cdot\mathbf S_{i+1},
\]

semua bond yang tidak menyentuh situs \(j\) memberi energi ground state yang sama. Hanya bond

\[
(j-1,j)
\]

dan

\[
(j,j+1)
\]

yang perlu dihitung ulang.

Pada bond \((j-1,j)\), bagian longitudinal:

\[
S_{j-1}^zS_j^z|j\rangle
=
S(S-1)|j\rangle.
\]

Nilai ground-state bond adalah \(S^2\), sehingga perubahan longitudinal per bond

\[
S(S-1)-S^2=-S.
\]

Karena Hamiltonian memiliki \(-J\), perubahan energi diagonal per bond adalah

\[
+JS.
\]

Ada dua bond, jadi bagian diagonal total

\[
2JS|j\rangle.
\]

Bagian transversal pada bond kanan:

\[
-\frac J2
S_j^+S_{j+1}^-|j\rangle.
\]

Operator \(S_{j+1}^-\) menurunkan spin di \(j+1\), lalu \(S_j^+\) mengembalikan spin \(j\) ke keadaan atas:

\[
S_j^+S_{j+1}^-|j\rangle
=
2S|j+1\rangle.
\]

Jadi kontribusinya

\[
-JS|j+1\rangle.
\]

Dengan cara sama, bond kiri memberi

\[
-JS|j-1\rangle.
\]

Maka

\[
\boxed{
(H-E_0)|j\rangle
=
JS
\left[
2|j\rangle-|j-1\rangle-|j+1\rangle
\right]
}.
\]

## 14. Fourier transform basis satu magnon

Definisikan

\[
|q\rangle
=
\frac1{\sqrt N}
\sum_j e^{iqR_j}|j\rangle.
\]

Terapkan Hamiltonian:

\[
(H-E_0)|q\rangle
=
\frac{JS}{\sqrt N}
\sum_j e^{iqR_j}
[2|j\rangle-|j-1\rangle-|j+1\rangle].
\]

Untuk suku \(|j-1\rangle\), ganti indeks

\[
\ell=j-1
\quad\Rightarrow\quad
j=\ell+1.
\]

Maka

\[
\sum_j e^{iqR_j}|j-1\rangle
=
\sum_\ell e^{iqR_{\ell+1}}|\ell\rangle.
\]

Untuk rantai periodik \(R_{\ell+1}=R_\ell+a\):

\[
=
e^{iqa}
\sum_\ell e^{iqR_\ell}|\ell\rangle
=
e^{iqa}\sqrt N|q\rangle.
\]

Dengan cara sama,

\[
\sum_j e^{iqR_j}|j+1\rangle
=
e^{-iqa}\sqrt N|q\rangle.
\]

Jadi

\[
(H-E_0)|q\rangle
=
JS[2-e^{iqa}-e^{-iqa}]|q\rangle.
\]

Gunakan

\[
e^{iqa}+e^{-iqa}=2\cos(qa):
\]

\[
\boxed{
E(q)-E_0
=
2JS[1-\cos(qa)]
}.
\]

Karena \(E(q)-E_0=\hbar\omega_q\), hasil kuantum sama dengan hasil semiklasik.

---

# Bagian IV - Hamiltonian magnetik umum

## 15. Bentuk interaksi yang akan diprogram

Bentuk yang sesuai dengan rangkaian notes adalah

\[
\boxed{
\begin{aligned}
H_{\mathrm{micro}}
={}&
-\sum_{\langle i,j\rangle}
J_{ij}\mathbf S_i\cdot\mathbf S_j\\
&-\sum_iK_i
(\widehat{\mathbf m}_i\cdot\mathbf S_i)^2\\
&+\sum_{\langle i,j\rangle}
\mathbf D_{ij}\cdot
(\mathbf S_i\times\mathbf S_j)\\
&-\sum_i\mathbf h_i\cdot\mathbf S_i.
\end{aligned}
}
\]

Di sini

\[
\mathbf h_i=g_i\mu_B\mathbf B
\]

dapat dianggap sebagai medan dalam satuan energi.

Untuk coding yang lebih umum, gabungkan seluruh interaksi bilinear antar-situs menjadi matriks \(3\times3\):

\[
\boxed{
H_{\mathrm{bond}}
=
\sum_{\langle i,j\rangle}
\mathbf S_i^T
\mathsf K_{ij}
\mathbf S_j
}.
\]

Contoh:

- isotropic exchange feromagnetik:

\[
\mathsf K_{ij}^{\mathrm{ex}}=-J_{ij}I_3;
\]

- symmetric anisotropic exchange:

\[
\mathsf K_{ij}^{\mathrm{sym}}=\Gamma_{ij};
\]

- DMI:

\[
\mathsf K_{ij}^{\mathrm{DM}}
=
\begin{pmatrix}
0&D_z&-D_y\\
-D_z&0&D_x\\
D_y&-D_x&0
\end{pmatrix}.
\]

Matriks DMI di atas memenuhi

\[
\mathbf S_i^T
\mathsf K_{ij}^{\mathrm{DM}}
\mathbf S_j
=
\mathbf D_{ij}\cdot
(\mathbf S_i\times\mathbf S_j).
\]

Jika orientasi bond dibalik,

\[
\mathsf K_{ji}
=
\mathsf K_{ij}^T.
\]

Untuk DMI ini ekuivalen dengan

\[
\mathbf D_{ji}=-\mathbf D_{ij}.
\]

## 15.1 Menentukan ground state klasik sebelum LSWT

Semua rotasi lokal dan ekspansi HP harus dilakukan terhadap konfigurasi klasik yang stationary. Ganti setiap operator spin dengan vektor klasik

\[
\mathbf S_{\ell r}^{\mathrm{cl}}
=
S_r\widehat{\mathbf n}_r.
\]

Untuk magnetic unit cell periodik, energi klasik per unit cell adalah

\[
\boxed{
\begin{aligned}
E_0
={}&
\sum_{b:r\to s}
S_rS_s
\widehat{\mathbf n}_r^T
\mathsf K_b
\widehat{\mathbf n}_s\\
&-\sum_r
K_rS_r^2
(\widehat{\mathbf m}_r\cdot\widehat{\mathbf n}_r)^2\\
&-\sum_r
S_r\mathbf h_r\cdot\widehat{\mathbf n}_r.
\end{aligned}
}
\]

Jumlah bond pada baris pertama memakai physical bond list yang setiap bond-nya disimpan sekali.

Karena \(|\widehat{\mathbf n}_r|=1\), syarat stationary bukan sekadar gradien Cartesian nol. Hanya komponen gradien yang tegak lurus spin yang harus nol.

Definisikan

\[
\mathbf g_r
=
\frac{\partial E_0}
{\partial\widehat{\mathbf n}_r}.
\]

Tangent gradient:

\[
\boxed{
\mathbf g_{r,\perp}
=
\mathbf g_r
-(\widehat{\mathbf n}_r\cdot\mathbf g_r)
\widehat{\mathbf n}_r
}.
\]

Syarat stationary:

\[
\boxed{
\mathbf g_{r,\perp}=0
}
\]

atau ekuivalen

\[
\boxed{
\widehat{\mathbf n}_r\times\mathbf g_r=0
}.
\]

Artinya classical effective field sejajar dengan spin.

Untuk minimisasi sederhana, satu langkah projected gradient descent:

\[
\widehat{\mathbf n}_r^{\mathrm{new}}
=
\operatorname{normalize}
\left[
\widehat{\mathbf n}_r
-\alpha\mathbf g_{r,\perp}
\right].
\]

Untuk sistem frustrated atau non-collinear, jalankan dari beberapa initial state karena energi dapat memiliki banyak local minimum.

Setelah minimisasi, lakukan dua validasi:

1. residual torque kecil:

\[
\max_r
|\widehat{\mathbf n}_r\times\mathbf g_r|
<\epsilon;
\]

2. residual bosonik linear kecil:

\[
\max_r|h_r|<\epsilon.
\]

Kedua tes mengukur kondisi fisik yang sama dalam dua representasi berbeda.

---

# Bagian V - Rotasi ke sumbu lokal

## 16. Arah klasik setiap sublattice

Tuliskan arah spin klasik sublattice \(r\) sebagai

\[
\widehat{\mathbf n}_r
=
\begin{pmatrix}
\sin\theta_r\cos\phi_r\\
\sin\theta_r\sin\phi_r\\
\cos\theta_r
\end{pmatrix}.
\]

Spin klasiknya

\[
\mathbf S_r^{\mathrm{cl}}
=
S_r\widehat{\mathbf n}_r.
\]

Tujuan rotasi lokal adalah membuat semua arah klasik terlihat sebagai

\[
\widetilde{\mathbf S}_r^{\mathrm{cl}}
=
\begin{pmatrix}
0\\0\\S_r
\end{pmatrix}.
\]

## 17. Matriks rotasi yang dipakai buku

Definisikan

\[
U_r
=
\begin{pmatrix}
\cos\theta_r\cos\phi_r&
\cos\theta_r\sin\phi_r&
-\sin\theta_r\\
-\sin\phi_r&
\cos\phi_r&
0\\
\sin\theta_r\cos\phi_r&
\sin\theta_r\sin\phi_r&
\cos\theta_r
\end{pmatrix}.
\]

Transformasi global ke lokal:

\[
\boxed{
\widetilde{\mathbf S}_r
=
U_r\mathbf S_r
}.
\]

Karena \(U_r\) ortogonal,

\[
U_r^{-1}=U_r^T.
\]

Transformasi lokal ke global:

\[
\boxed{
\mathbf S_r
=
R_r\widetilde{\mathbf S}_r,
\qquad
R_r=U_r^{-1}=U_r^T
}.
\]

Kolom-kolom \(R_r\) adalah basis lokal yang ditulis dalam koordinat global:

\[
R_r
=
\begin{pmatrix}
\widehat{\mathbf x}_r&
\widehat{\mathbf y}_r&
\widehat{\mathbf z}_r
\end{pmatrix},
\]

dengan

\[
\widehat{\mathbf z}_r=\widehat{\mathbf n}_r.
\]

Validasi yang harus dilakukan di kode:

\[
R_r^TR_r=I_3,
\]

\[
\det R_r=+1,
\]

\[
R_r
\begin{pmatrix}0\\0\\1\end{pmatrix}
=
\widehat{\mathbf n}_r.
\]

## 18. Cara membangun basis lokal tanpa sudut

Untuk implementasi numerik, arah spin mungkin diberikan langsung sebagai vektor \(\widehat{\mathbf n}_r\), bukan \(\theta_r,\phi_r\).

Algoritma stabil:

1. Normalisasi \(\widehat{\mathbf z}_r=\widehat{\mathbf n}_r/|\widehat{\mathbf n}_r|\).
2. Pilih seed \(\mathbf e=(0,0,1)\).
3. Jika \(|\mathbf e\cdot\widehat{\mathbf z}_r|>0.9\), ganti seed dengan \((1,0,0)\).
4. Hitung

\[
\widehat{\mathbf y}_r
=
\frac{\mathbf e\times\widehat{\mathbf z}_r}
{|\mathbf e\times\widehat{\mathbf z}_r|}.
\]

5. Hitung

\[
\widehat{\mathbf x}_r
=
\widehat{\mathbf y}_r\times\widehat{\mathbf z}_r.
\]

6. Susun

\[
R_r=
\begin{pmatrix}
\widehat{\mathbf x}_r&
\widehat{\mathbf y}_r&
\widehat{\mathbf z}_r
\end{pmatrix}.
\]

Pilihan \(\widehat{\mathbf x}_r,\widehat{\mathbf y}_r\) tidak unik. Rotasi kedua sumbu itu di sekitar \(\widehat{\mathbf z}_r\) adalah gauge choice. Energi magnon tidak boleh berubah ketika gauge lokal diubah.

## 19. Rotasi coupling matrix

Untuk bond \(i\to j\),

\[
H_{ij}
=
\mathbf S_i^T\mathsf K_{ij}\mathbf S_j.
\]

Substitusi

\[
\mathbf S_i=R_i\widetilde{\mathbf S}_i,
\qquad
\mathbf S_j=R_j\widetilde{\mathbf S}_j
\]

memberi

\[
H_{ij}
=
\widetilde{\mathbf S}_i^T
R_i^T\mathsf K_{ij}R_j
\widetilde{\mathbf S}_j.
\]

Definisikan local bond matrix

\[
\boxed{
\mathsf M_{ij}
=
R_i^T\mathsf K_{ij}R_j
}.
\]

Untuk isotropic exchange \(\mathsf K_{ij}=-J_{ij}I\):

\[
\mathsf M_{ij}
=
-J_{ij}R_i^TR_j.
\]

Karena \(R_i=U_i^{-1}\),

\[
R_i^TR_j
=
U_iU_j^{-1}.
\]

Inilah matriks

\[
\boxed{
F(i,j)=U_iU_j^{-1}
}
\]

di buku dan scan tulisan tangan.

---

# Bagian VI - Holstein-Primakoff tanpa melewatkan orde

## 20. Transformasi eksak

Pada setiap sumbu lokal:

\[
\widetilde S_i^z
=
S_i-a_i^\dagger a_i,
\]

\[
\widetilde S_i^+
=
\sqrt{2S_i}
\sqrt{1-\frac{a_i^\dagger a_i}{2S_i}}
a_i,
\]

\[
\widetilde S_i^-
=
\sqrt{2S_i}
a_i^\dagger
\sqrt{1-\frac{a_i^\dagger a_i}{2S_i}}.
\]

Operator boson memenuhi

\[
[a_i,a_j^\dagger]=\delta_{ij},
\]

\[
[a_i,a_j]=0,
\]

\[
[a_i^\dagger,a_j^\dagger]=0.
\]

Number operator:

\[
n_i=a_i^\dagger a_i.
\]

Makna

\[
\widetilde S_i^z=S_i-n_i
\]

adalah setiap magnon mengurangi proyeksi spin lokal sebanyak satu.

## 21. Ekspansi \(1/S\)

Gunakan

\[
\sqrt{1-x}
=
1-\frac{x}{2}-\frac{x^2}{8}-\cdots.
\]

Dengan

\[
x=\frac{n_i}{2S_i},
\]

diperoleh

\[
\sqrt{1-\frac{n_i}{2S_i}}
=
1-\frac{n_i}{4S_i}
-\frac{n_i^2}{32S_i^2}
-\cdots.
\]

Jadi

\[
\widetilde S_i^+
=
\sqrt{2S_i}
\left(
1-\frac{n_i}{4S_i}+\cdots
\right)a_i.
\]

Suku pertama berorde \(\sqrt S\). Suku berikutnya mengandung tiga operator boson dan menghasilkan interaksi magnon.

Pada linear spin-wave theory:

\[
\boxed{
\widetilde S_i^+\simeq\sqrt{2S_i}\,a_i
},
\]

\[
\boxed{
\widetilde S_i^-\simeq\sqrt{2S_i}\,a_i^\dagger
},
\]

\[
\boxed{
\widetilde S_i^z=S_i-a_i^\dagger a_i
}.
\]

## 22. Komponen Cartesian lokal

Karena

\[
\widetilde S_i^x
=
\frac{\widetilde S_i^++\widetilde S_i^-}{2},
\]

maka

\[
\widetilde S_i^x
\simeq
\frac{\sqrt{2S_i}}{2}(a_i+a_i^\dagger)
\]

\[
\boxed{
\widetilde S_i^x
\simeq
\sqrt{\frac{S_i}{2}}
(a_i+a_i^\dagger)
}.
\]

Untuk \(y\):

\[
\widetilde S_i^y
=
\frac{\widetilde S_i^+-\widetilde S_i^-}{2i}
\]

\[
\boxed{
\widetilde S_i^y
\simeq
-i\sqrt{\frac{S_i}{2}}
(a_i-a_i^\dagger)
}.
\]

Definisikan singkat

\[
c_i=\sqrt{\frac{S_i}{2}}.
\]

Maka

\[
\widetilde S_i^x=c_i(a_i+a_i^\dagger),
\]

\[
\widetilde S_i^y=-ic_i(a_i-a_i^\dagger),
\]

\[
\widetilde S_i^z=S_i-n_i.
\]

## 23. Struktur orde Hamiltonian

Setelah substitusi HP:

\[
\boxed{
H=E_0+H_1+H_2+H_3+H_4+\cdots
}.
\]

Skalanya:

\[
E_0\sim S^2,
\]

\[
H_1\sim S^{3/2},
\]

\[
H_2\sim S,
\]

\[
H_3\sim S^{1/2},
\]

\[
H_4\sim S^0.
\]

\(E_0\) adalah energi klasik. \(H_1\) berisi satu operator \(a\) atau \(a^\dagger\). Jika konfigurasi klasik benar-benar stationary:

\[
\boxed{H_1=0}.
\]

\(H_2\) adalah Hamiltonian linear spin-wave. \(H_3,H_4\) menggambarkan interaksi dan decay magnon.

---

# Bagian VII - Ekspansi lengkap satu bond

## 24. Tuliskan local bond matrix per komponen

Untuk satu physical bond \(i-j\),

\[
H_{ij}
=
\widetilde{\mathbf S}_i^T
\mathsf M_{ij}
\widetilde{\mathbf S}_j,
\]

dengan

\[
\mathsf M_{ij}
=
\begin{pmatrix}
M_{xx}&M_{xy}&M_{xz}\\
M_{yx}&M_{yy}&M_{yz}\\
M_{zx}&M_{zy}&M_{zz}
\end{pmatrix}.
\]

Ekspansi penuh:

\[
\begin{aligned}
H_{ij}
={}&
M_{xx}\widetilde S_i^x\widetilde S_j^x
+M_{xy}\widetilde S_i^x\widetilde S_j^y
+M_{xz}\widetilde S_i^x\widetilde S_j^z\\
&+M_{yx}\widetilde S_i^y\widetilde S_j^x
+M_{yy}\widetilde S_i^y\widetilde S_j^y
+M_{yz}\widetilde S_i^y\widetilde S_j^z\\
&+M_{zx}\widetilde S_i^z\widetilde S_j^x
+M_{zy}\widetilde S_i^z\widetilde S_j^y
+M_{zz}\widetilde S_i^z\widetilde S_j^z.
\end{aligned}
\]

Kita pisahkan menjadi:

1. \(zz\): memberi energi klasik dan number operator.
2. \(xz,yz,zx,zy\): memberi suku linear dan kemudian suku kubik.
3. \(xx,xy,yx,yy\): memberi suku boson kuadratik.

## 25. Bagian longitudinal \(zz\)

Substitusi

\[
\widetilde S_i^z=S_i-n_i,
\qquad
\widetilde S_j^z=S_j-n_j.
\]

Maka

\[
M_{zz}\widetilde S_i^z\widetilde S_j^z
=
M_{zz}(S_i-n_i)(S_j-n_j).
\]

Ekspansikan:

\[
=
M_{zz}
\left[
S_iS_j
-S_jn_i
-S_in_j
+n_in_j
\right].
\]

Klasifikasi:

- \(M_{zz}S_iS_j\): energi klasik, orde \(S^2\).
- \(-M_{zz}S_jn_i\): kuadratik, karena \(n_i=a_i^\dagger a_i\).
- \(-M_{zz}S_in_j\): kuadratik.
- \(M_{zz}n_in_j\): empat operator boson, dibuang dalam LSWT.

Jadi kontribusinya:

\[
\boxed{
E_{0,ij}=M_{zz}S_iS_j
}
\]

dan

\[
\boxed{
H_{ij,zz}^{(2)}
=
-M_{zz}
\left(
S_j a_i^\dagger a_i
+S_i a_j^\dagger a_j
\right)
}.
\]

## 26. Bagian campuran dan syarat \(H_1=0\)

Pertama,

\[
M_{xz}\widetilde S_i^x\widetilde S_j^z.
\]

Pada orde linear, ambil \(\widetilde S_j^z\simeq S_j\):

\[
=
M_{xz}c_iS_j(a_i+a_i^\dagger).
\]

Berikutnya

\[
M_{yz}\widetilde S_i^y\widetilde S_j^z
\]

\[
=
-iM_{yz}c_iS_j(a_i-a_i^\dagger).
\]

Jumlah keduanya:

\[
\begin{aligned}
H_{ij,\perp z}^{(1)}
={}&
c_iS_j
\left[
(M_{xz}-iM_{yz})a_i\right.\\
&\left.
+(M_{xz}+iM_{yz})a_i^\dagger
\right].
\end{aligned}
\]

Untuk komponen yang transversal pada situs \(j\):

\[
\begin{aligned}
H_{ij,z\perp}^{(1)}
={}&
S_ic_j
\left[
(M_{zx}-iM_{zy})a_j\right.\\
&\left.
+(M_{zx}+iM_{zy})a_j^\dagger
\right].
\end{aligned}
\]

Jadi kontribusi satu bond ke koefisien linear adalah

\[
\boxed{
h_i^{(ij)}
=
c_iS_j(M_{xz}-iM_{yz})
}
\]

untuk operator \(a_i\), dan

\[
\boxed{
h_j^{(ij)}
=
S_ic_j(M_{zx}-iM_{zy})
}
\]

untuk operator \(a_j\).

Hamiltonian linear dapat ditulis

\[
H_1
=
\sum_i
\left(
h_i a_i+h_i^*a_i^\dagger
\right).
\]

Setelah semua bond, anisotropi, dan medan dijumlahkan, konfigurasi klasik yang stationary harus memenuhi

\[
\boxed{
h_i=0
\quad\text{untuk setiap }i.
}
\]

Ini salah satu unit test terpenting untuk kode LSWT. Jika residual \(h_i\) besar, jangan lanjut diagonalization. Arah klasik, tanda interaksi, atau bond list masih salah.

## 27. Ekspansi \(xx\)

\[
M_{xx}\widetilde S_i^x\widetilde S_j^x
=
M_{xx}c_ic_j
(a_i+a_i^\dagger)
(a_j+a_j^\dagger).
\]

Ekspansikan:

\[
\boxed{
\begin{aligned}
M_{xx}\widetilde S_i^x\widetilde S_j^x
=
c_ic_jM_{xx}
(&a_ia_j
+a_ia_j^\dagger\\
&+a_i^\dagger a_j
+a_i^\dagger a_j^\dagger).
\end{aligned}
}
\]

## 28. Ekspansi \(xy\)

\[
M_{xy}\widetilde S_i^x\widetilde S_j^y
=
-iM_{xy}c_ic_j
(a_i+a_i^\dagger)
(a_j-a_j^\dagger).
\]

Ekspansi isi kurung:

\[
(a_i+a_i^\dagger)(a_j-a_j^\dagger)
=
a_ia_j-a_ia_j^\dagger
+a_i^\dagger a_j
-a_i^\dagger a_j^\dagger.
\]

Kalikan \(-i\):

\[
\boxed{
\begin{aligned}
M_{xy}\widetilde S_i^x\widetilde S_j^y
=
c_ic_jM_{xy}
(&-i\,a_ia_j
+i\,a_ia_j^\dagger\\
&-i\,a_i^\dagger a_j
+i\,a_i^\dagger a_j^\dagger).
\end{aligned}
}
\]

## 29. Ekspansi \(yx\)

\[
M_{yx}\widetilde S_i^y\widetilde S_j^x
=
-iM_{yx}c_ic_j
(a_i-a_i^\dagger)
(a_j+a_j^\dagger).
\]

Ekspansi:

\[
(a_i-a_i^\dagger)(a_j+a_j^\dagger)
=
a_ia_j+a_ia_j^\dagger
-a_i^\dagger a_j
-a_i^\dagger a_j^\dagger.
\]

Kalikan \(-i\):

\[
\boxed{
\begin{aligned}
M_{yx}\widetilde S_i^y\widetilde S_j^x
=
c_ic_jM_{yx}
(&-i\,a_ia_j
-i\,a_ia_j^\dagger\\
&+i\,a_i^\dagger a_j
+i\,a_i^\dagger a_j^\dagger).
\end{aligned}
}
\]

## 30. Ekspansi \(yy\)

\[
M_{yy}\widetilde S_i^y\widetilde S_j^y
=
(-i)^2M_{yy}c_ic_j
(a_i-a_i^\dagger)
(a_j-a_j^\dagger).
\]

Karena

\[
(-i)^2=-1,
\]

dan

\[
(a_i-a_i^\dagger)(a_j-a_j^\dagger)
=
a_ia_j-a_ia_j^\dagger
-a_i^\dagger a_j
+a_i^\dagger a_j^\dagger,
\]

maka

\[
\boxed{
\begin{aligned}
M_{yy}\widetilde S_i^y\widetilde S_j^y
=
c_ic_jM_{yy}
(&-a_ia_j
+a_ia_j^\dagger\\
&+a_i^\dagger a_j
-a_i^\dagger a_j^\dagger).
\end{aligned}
}
\]

## 31. Kelompokkan empat jenis operator

Jumlahkan hasil \(xx,xy,yx,yy\).

### Koefisien \(a_i^\dagger a_j\)

Dari empat ekspansi:

\[
M_{xx}
-iM_{xy}
+iM_{yx}
+M_{yy}.
\]

Jadi

\[
\boxed{
T_{ij}
=
c_ic_j
\left[
M_{xx}+M_{yy}
+i(M_{yx}-M_{xy})
\right]
}.
\]

### Koefisien \(a_i a_j^\dagger\)

\[
M_{xx}
+iM_{xy}
-iM_{yx}
+M_{yy}.
\]

Untuk \(\mathsf M_{ij}\) real, ini adalah \(T_{ij}^*\):

\[
\boxed{
T_{ji}^{\mathrm{term}}
=
c_ic_j
\left[
M_{xx}+M_{yy}
+i(M_{xy}-M_{yx})
\right]
=T_{ij}^*
}.
\]

Karena operator pada situs berbeda commute,

\[
a_i a_j^\dagger
=
a_j^\dagger a_i,
\qquad i\neq j.
\]

Jadi suku ini menjadi elemen Hermitian reverse hopping.

### Koefisien \(a_i a_j\)

\[
M_{xx}
-iM_{xy}
-iM_{yx}
-M_{yy}.
\]

Maka

\[
\boxed{
P_{ij}
=
c_ic_j
\left[
M_{xx}-M_{yy}
-i(M_{xy}+M_{yx})
\right]
}.
\]

### Koefisien \(a_i^\dagger a_j^\dagger\)

\[
M_{xx}
+iM_{xy}
+iM_{yx}
-M_{yy}.
\]

Untuk matriks real:

\[
\boxed{
\text{koefisien }a_i^\dagger a_j^\dagger
=
P_{ij}^*
}.
\]

## 32. Bentuk kuadratik satu bond

Gabungkan bagian longitudinal dan transversal:

\[
\boxed{
\begin{aligned}
H_{ij}^{(2)}
={}&
-M_{zz}S_j\,a_i^\dagger a_i
-M_{zz}S_i\,a_j^\dagger a_j\\
&+T_{ij}a_i^\dagger a_j
+T_{ij}^*a_j^\dagger a_i\\
&+P_{ij}a_i a_j
+P_{ij}^*a_i^\dagger a_j^\dagger.
\end{aligned}
}
\]

Ini adalah rumus paling penting untuk implementasi umum.

## 33. Hubungan dengan \(F_{zz},G_1,G_2\) pada buku

Untuk isotropic exchange,

\[
\mathsf M_{ij}
=
-J_{ij}F(i,j),
\]

dengan

\[
F(i,j)=U_iU_j^{-1}.
\]

Buku mendefinisikan

\[
\boxed{
G_1(i,j)
=
F_{xx}+F_{yy}
-i(F_{xy}-F_{yx})
}
\]

dan

\[
\boxed{
G_2(i,j)
=
F_{xx}-F_{yy}
-i(F_{xy}+F_{yx})
}.
\]

Bandingkan dengan rumus sebelumnya:

\[
T_{ij}
=
-J_{ij}c_ic_jG_1(i,j),
\]

\[
P_{ij}
=
-J_{ij}c_ic_jG_2(i,j).
\]

Karena

\[
c_ic_j
=
\frac{\sqrt{S_iS_j}}{2},
\]

maka

\[
\boxed{
T_{ij}
=
-\frac{J_{ij}\sqrt{S_iS_j}}{2}
G_1(i,j)
}
\]

dan

\[
\boxed{
P_{ij}
=
-\frac{J_{ij}\sqrt{S_iS_j}}{2}
G_2(i,j)
}.
\]

Komponen

\[
F_{zz}(i,j)
\]

adalah cosinus sudut antara arah spin klasik:

\[
\boxed{
F_{zz}(i,j)
=
\widehat{\mathbf n}_i\cdot
\widehat{\mathbf n}_j
}.
\]

Untuk spin sejajar:

\[
F=I,\qquad F_{zz}=1,\qquad G_1=2,\qquad G_2=0.
\]

Karena \(G_2=0\), feromagnet isotropik kolinear tidak memiliki anomalous pairing.

Untuk dua spin antiparalel dengan pilihan rotasi standar:

\[
F_{zz}=-1,\qquad G_1=0,\qquad G_2=-2.
\]

Karena \(G_1=0\) dan \(G_2\neq0\), coupling AF muncul sebagai magnon-pair terms dalam sumbu lokal.

---

# Bagian VIII - Kontribusi onsite

## 34. Single-ion anisotropy dengan arah umum

Ambil

\[
H_{K,i}
=
-K_i
(\widehat{\mathbf m}_i\cdot\mathbf S_i)^2.
\]

Ubah arah anisotropi ke koordinat lokal:

\[
\boxed{
\mathbf c_i
=
R_i^T\widehat{\mathbf m}_i
=
\begin{pmatrix}
c_{ix}\\c_{iy}\\c_{iz}
\end{pmatrix}
}.
\]

Karena \(\mathbf S_i=R_i\widetilde{\mathbf S}_i\),

\[
\widehat{\mathbf m}_i\cdot\mathbf S_i
=
\mathbf c_i\cdot\widetilde{\mathbf S}_i.
\]

Tuliskan

\[
\mathbf c_i\cdot\widetilde{\mathbf S}_i
=
c_{ix}\widetilde S_i^x
+c_{iy}\widetilde S_i^y
+c_{iz}\widetilde S_i^z.
\]

Definisikan

\[
\boxed{
u_i=c_{ix}-ic_{iy}
}.
\]

Bagian transversal:

\[
c_{ix}\widetilde S_i^x+c_{iy}\widetilde S_i^y
=
c_i^{(S)}
\left(
u_i a_i+u_i^*a_i^\dagger
\right),
\]

dengan

\[
c_i^{(S)}=\sqrt{\frac{S_i}{2}}.
\]

Jadi

\[
\widehat{\mathbf m}_i\cdot\mathbf S_i
=
c_{iz}(S_i-n_i)
+c_i^{(S)}
(u_i a_i+u_i^*a_i^\dagger).
\]

Kuadratkan. Bagian longitudinal:

\[
c_{iz}^2(S_i-n_i)^2
\simeq
c_{iz}^2(S_i^2-2S_in_i).
\]

Bagian transversal kuadrat:

\[
\frac{S_i}{2}
(u_ia_i+u_i^*a_i^\dagger)^2.
\]

Ekspansikan:

\[
=
\frac{S_i}{2}
\left[
u_i^2a_i^2
+|u_i|^2a_ia_i^\dagger
+|u_i|^2a_i^\dagger a_i
+u_i^{*2}a_i^{\dagger2}
\right].
\]

Gunakan

\[
a_ia_i^\dagger
=
a_i^\dagger a_i+1.
\]

Maka bagian kuadratik normal adalah

\[
S_i|u_i|^2a_i^\dagger a_i,
\]

sedangkan konstanta tambahan adalah

\[
\frac{S_i}{2}|u_i|^2.
\]

Bagian silang longitudinal-transversal memiliki suku linear

\[
2c_{iz}S_i
\sqrt{\frac{S_i}{2}}
(u_ia_i+u_i^*a_i^\dagger),
\]

sedangkan produk \(n_i a_i\) dan \(n_i a_i^\dagger\) adalah kubik dan dibuang.

Setelah dikali \(-K_i\), kontribusi kuadratik normal:

\[
\boxed{
A_{ii}^{(K)}
=
K_iS_i
\left[
2c_{iz}^2-(c_{ix}^2+c_{iy}^2)
\right]
}.
\]

Karena

\[
|u_i|^2=c_{ix}^2+c_{iy}^2,
\]

hasil ini juga dapat ditulis

\[
A_{ii}^{(K)}
=
K_iS_i(2c_{iz}^2-|u_i|^2).
\]

Koefisien annihilation pairing dalam bentuk canonical adalah

\[
\boxed{
B_{ii}^{(K)}
=
-K_iS_i u_i^2
}.
\]

Koefisien creation pairing:

\[
\boxed{
\Delta_{ii}^{(K)}
=
-K_iS_i u_i^{*2}
}.
\]

Kontribusi linear:

\[
\boxed{
h_i^{(K)}
=
-2K_i c_{iz}S_i
\sqrt{\frac{S_i}{2}}u_i
}.
\]

Jika easy axis sejajar arah spin lokal:

\[
\mathbf c_i=(0,0,1).
\]

Maka

\[
u_i=0,
\]

\[
A_{ii}^{(K)}=2K_iS_i,
\]

\[
B_{ii}^{(K)}=0.
\]

Inilah asal gap \(2KS\).

## 35. Hubungan dengan \(A_x,A_y,A_z\) pada notes

Scan dan buku menulis

\[
\widehat{\mathbf m}\cdot\mathbf S_r
=
A_x\widetilde S_{rx}
+A_y\widetilde S_{ry}
+A_z\widetilde S_{rz}.
\]

Jadi

\[
A_x=c_{rx},\qquad
A_y=c_{ry},\qquad
A_z=c_{rz}.
\]

Dalam konvensi matriks \(L\) buku, perubahan diagonal adalah

\[
L_{rr}
\rightarrow
L_{rr}
-\frac{KS_r}{2}
(A_x^2+A_y^2-2A_z^2).
\]

Ini sama dengan

\[
L_{rr}
\rightarrow
L_{rr}
+\frac{KS_r}{2}
(2A_z^2-A_x^2-A_y^2).
\]

Rumus tersebut setengah dari \(A_{rr}^{(K)}\) di atas karena buku memakai Nambu double counting tanpa prefaktor eksplisit \(1/2\).

Pairing block buku:

\[
L_{r,r+M}
\rightarrow
L_{r,r+M}
-\frac{KS_r}{2}(A_x+iA_y)^2,
\]

\[
L_{r+M,r}
\rightarrow
L_{r+M,r}
-\frac{KS_r}{2}(A_x-iA_y)^2.
\]

## 36. Zeeman interaction

Tuliskan medan dalam satuan energi:

\[
H_{Z,i}
=
-\mathbf h_i\cdot\mathbf S_i.
\]

Rotasi ke lokal:

\[
\mathbf b_i=R_i^T\mathbf h_i
=
\begin{pmatrix}
b_{ix}\\b_{iy}\\b_{iz}
\end{pmatrix}.
\]

Maka

\[
H_{Z,i}
=
-b_{ix}\widetilde S_i^x
-b_{iy}\widetilde S_i^y
-b_{iz}\widetilde S_i^z.
\]

Substitusi HP:

\[
\begin{aligned}
H_{Z,i}
={}&
-\sqrt{\frac{S_i}{2}}
\left[
(b_{ix}-ib_{iy})a_i
+(b_{ix}+ib_{iy})a_i^\dagger
\right]\\
&-b_{iz}S_i
+b_{iz}a_i^\dagger a_i.
\end{aligned}
\]

Jadi:

\[
\boxed{
E_{0,i}^{(Z)}=-b_{iz}S_i
},
\]

\[
\boxed{
h_i^{(Z)}
=
-\sqrt{\frac{S_i}{2}}
(b_{ix}-ib_{iy})
},
\]

\[
\boxed{
A_{ii}^{(Z)}=b_{iz}
},
\]

dan tidak ada pairing:

\[
\boxed{
B_{ii}^{(Z)}=0
}.
\]

Jika medan sejajar spin klasik, \(b_{ix}=b_{iy}=0\), sehingga tidak ada suku linear dan medan hanya menggeser energi magnon.

## 37. DMI tidak memerlukan derivasi terpisah di kode

Untuk

\[
H_{ij}^{\mathrm{DM}}
=
\mathbf D_{ij}\cdot
(\mathbf S_i\times\mathbf S_j),
\]

ekspansi cross product-nya adalah

\[
\begin{aligned}
\mathbf D\cdot(\mathbf S_i\times\mathbf S_j)
={}&
D_x(S_i^yS_j^z-S_i^zS_j^y)\\
&+D_y(S_i^zS_j^x-S_i^xS_j^z)\\
&+D_z(S_i^xS_j^y-S_i^yS_j^x).
\end{aligned}
\]

Karena itu koefisien baris \(S_i^\alpha\), kolom \(S_j^\beta\) membentuk matriks berikut:

\[
\mathsf K_{ij}^{\mathrm{DM}}
=
\begin{pmatrix}
0&D_z&-D_y\\
-D_z&0&D_x\\
D_y&-D_x&0
\end{pmatrix}.
\]

Kemudian jalankan prosedur yang sama:

\[
\mathsf M_{ij}^{\mathrm{DM}}
=
R_i^T
\mathsf K_{ij}^{\mathrm{DM}}
R_j.
\]

Setelah itu \(T_{ij},P_{ij},M_{zz}\), dan residual linear dihitung dengan rumus satu-bond yang sama. Ini lebih aman daripada mengimplementasikan persamaan Levi-Civita panjang pada halaman akhir scan satu per satu.

---

# Bagian IX - Fourier transform lengkap

## 38. Definisi Fourier yang akan dipakai

Pakai posisi fisik penuh:

\[
\mathbf r_{\ell r}
=
\mathbf R_\ell+\boldsymbol\tau_r.
\]

Definisikan

\[
\boxed{
a_{\ell r}
=
\frac1{\sqrt{N_c}}
\sum_{\mathbf q}
e^{+i\mathbf q\cdot\mathbf r_{\ell r}}
a_{\mathbf q r}
}
\]

dan

\[
\boxed{
a_{\ell r}^\dagger
=
\frac1{\sqrt{N_c}}
\sum_{\mathbf q}
e^{-i\mathbf q\cdot\mathbf r_{\ell r}}
a_{\mathbf q r}^\dagger
}.
\]

Transformasi balik:

\[
a_{\mathbf q r}
=
\frac1{\sqrt{N_c}}
\sum_\ell
e^{-i\mathbf q\cdot\mathbf r_{\ell r}}
a_{\ell r}.
\]

Relasi ortogonalitas:

\[
\sum_\ell
e^{i(\mathbf q-\mathbf q')\cdot\mathbf R_\ell}
=
N_c\delta_{\mathbf q,\mathbf q'}.
\]

Untuk dua annihilation operator:

\[
\sum_\ell
e^{i(\mathbf q+\mathbf q')\cdot\mathbf R_\ell}
=
N_c\delta_{\mathbf q',-\mathbf q}.
\]

Itulah alasan pairing selalu menghubungkan \(\mathbf q\) dengan \(-\mathbf q\).

## 39. Fourier transform normal hopping

Ambil bond dari

\[
i=(\ell,r)
\]

ke

\[
j=(\ell+\Delta,s).
\]

Definisikan displacement fisik

\[
\boxed{
\mathbf d_{rs,\Delta}
=
\mathbf r_{\ell+\Delta,s}
-\mathbf r_{\ell r}
}.
\]

Pertimbangkan

\[
\sum_\ell
T_{rs,\Delta}
a_{\ell r}^\dagger
a_{\ell+\Delta,s}.
\]

Substitusi Fourier:

\[
\begin{aligned}
a_{\ell r}^\dagger a_{\ell+\Delta,s}
=
\frac1{N_c}
\sum_{\mathbf q,\mathbf q'}
&e^{-i\mathbf q\cdot\mathbf r_{\ell r}}
e^{+i\mathbf q'\cdot\mathbf r_{\ell+\Delta,s}}\\
&\times
a_{\mathbf q r}^\dagger
a_{\mathbf q's}.
\end{aligned}
\]

Jumlah atas \(\ell\) memberi \(\mathbf q'=\mathbf q\). Fase tersisa:

\[
e^{i\mathbf q\cdot
(\mathbf r_{\ell+\Delta,s}-\mathbf r_{\ell r})}
=
e^{i\mathbf q\cdot\mathbf d_{rs,\Delta}}.
\]

Maka

\[
\boxed{
\sum_\ell
T_{rs,\Delta}
a_{\ell r}^\dagger
a_{\ell+\Delta,s}
=
\sum_{\mathbf q}
T_{rs,\Delta}
e^{i\mathbf q\cdot\mathbf d_{rs,\Delta}}
a_{\mathbf q r}^\dagger a_{\mathbf q s}
}.
\]

## 40. Fourier transform pairing

Pertimbangkan

\[
\sum_\ell
P_{rs,\Delta}
a_{\ell r}
a_{\ell+\Delta,s}.
\]

Substitusi:

\[
\begin{aligned}
a_{\ell r}a_{\ell+\Delta,s}
=
\frac1{N_c}
\sum_{\mathbf q,\mathbf q'}
&e^{+i\mathbf q\cdot\mathbf r_{\ell r}}
e^{+i\mathbf q'\cdot\mathbf r_{\ell+\Delta,s}}\\
&\times
a_{\mathbf q r}a_{\mathbf q's}.
\end{aligned}
\]

Jumlah \(\ell\) memaksa

\[
\mathbf q'=-\mathbf q.
\]

Fase:

\[
e^{i\mathbf q\cdot\mathbf r_{\ell r}}
e^{-i\mathbf q\cdot\mathbf r_{\ell+\Delta,s}}
=
e^{-i\mathbf q\cdot\mathbf d_{rs,\Delta}}.
\]

Jadi

\[
\boxed{
\sum_\ell
P_{rs,\Delta}
a_{\ell r}a_{\ell+\Delta,s}
=
\sum_{\mathbf q}
P_{rs,\Delta}
e^{-i\mathbf q\cdot\mathbf d_{rs,\Delta}}
a_{\mathbf q r}a_{-\mathbf q,s}
}.
\]

Untuk creation pairing:

\[
\boxed{
\sum_\ell
P_{rs,\Delta}^*
a_{\ell r}^\dagger a_{\ell+\Delta,s}^\dagger
=
\sum_{\mathbf q}
P_{rs,\Delta}^*
e^{+i\mathbf q\cdot\mathbf d_{rs,\Delta}}
a_{\mathbf q r}^\dagger a_{-\mathbf q,s}^\dagger
}.
\]

## 41. Structure factor buku

Jika ada \(z_{rs}^{(u)}\) displacement yang semuanya memiliki coupling \(J_{rs}^{(u)}\), buku mendefinisikan

\[
\boxed{
\Gamma_{rs}^{(u)}(\mathbf q)
=
\frac1{z_{rs}^{(u)}}
\sum_{\mathbf d_{rs}^{(u)}}
e^{-i\mathbf q\cdot\mathbf d_{rs}^{(u)}}
}.
\]

Sifatnya:

\[
\Gamma_{rs}^{(u)}(\mathbf q)^*
=
\Gamma_{rs}^{(u)}(-\mathbf q)
=
\Gamma_{sr}^{(u)}(\mathbf q),
\]

\[
\Gamma_{rs}^{(u)}(\mathbf 0)=1.
\]

Untuk rantai 1D dengan dua tetangga \(\mathbf d=\pm a\hat x\):

\[
\Gamma(q)
=
\frac12(e^{-iqa}+e^{iqa})
=
\cos(qa).
\]

---

# Bagian X - Bentuk Hamiltonian kuadratik umum

## 42. Bentuk real-space canonical

Setelah semua interaksi dikumpulkan:

\[
\boxed{
\begin{aligned}
H_2
={}&
E_{\mathrm{const}}
+\sum_{i,j}A_{ij}a_i^\dagger a_j\\
&+\frac12\sum_{i,j}
\left[
B_{ij}a_i a_j
+B_{ij}^*a_i^\dagger a_j^\dagger
\right].
\end{aligned}
}
\]

Syarat:

\[
\boxed{
A=A^\dagger
}
\]

dan karena \(a_i a_j=a_j a_i\),

\[
\boxed{
B=B^T
}.
\]

Untuk satu physical bond \(i-j\), update real-space matrix:

\[
\boxed{
A_{ii}\mathrel{+}=-M_{zz}S_j
}
\]

\[
\boxed{
A_{jj}\mathrel{+}=-M_{zz}S_i
}
\]

\[
\boxed{
A_{ij}\mathrel{+}=T_{ij}
}
\]

\[
\boxed{
A_{ji}\mathrel{+}=T_{ij}^*
}
\]

\[
\boxed{
B_{ij}\mathrel{+}=P_{ij}
}
\]

\[
\boxed{
B_{ji}\mathrel{+}=P_{ij}
}.
\]

## 43. Matriks momentum-space

Definisikan \(M\times M\) normal block:

\[
\boxed{
\mathsf A_{rs}(\mathbf q)
=
\sum_\Delta
A_{(0,r),(\Delta,s)}
e^{+i\mathbf q\cdot\mathbf d_{rs,\Delta}}
}.
\]

Definisikan annihilation-pair block:

\[
\boxed{
\mathsf B_{rs}(\mathbf q)
=
\sum_\Delta
B_{(0,r),(\Delta,s)}
e^{-i\mathbf q\cdot\mathbf d_{rs,\Delta}}
}.
\]

Sifat yang harus terpenuhi:

\[
\boxed{
\mathsf A(\mathbf q)^\dagger
=
\mathsf A(\mathbf q)
}
\]

dan

\[
\boxed{
\mathsf B(\mathbf q)^T
=
\mathsf B(-\mathbf q)
}.
\]

## 44. Vektor Nambu

Definisikan

\[
\boxed{
\Psi_{\mathbf q}
=
\begin{pmatrix}
a_{\mathbf q1}\\
\vdots\\
a_{\mathbf qM}\\
a_{-\mathbf q1}^\dagger\\
\vdots\\
a_{-\mathbf qM}^\dagger
\end{pmatrix}
}.
\]

Adjoint:

\[
\Psi_{\mathbf q}^\dagger
=
\begin{pmatrix}
a_{\mathbf q1}^\dagger&
\cdots&
a_{\mathbf qM}^\dagger&
a_{-\mathbf q1}&
\cdots&
a_{-\mathbf qM}
\end{pmatrix}.
\]

Hamiltonian:

\[
\boxed{
H_2
=
\frac12\sum_{\mathbf q}
\Psi_{\mathbf q}^\dagger
\mathcal H_{\mathrm{BdG}}(\mathbf q)
\Psi_{\mathbf q}
+C
}
\]

dengan

\[
\boxed{
\mathcal H_{\mathrm{BdG}}(\mathbf q)
=
\begin{pmatrix}
\mathsf A(\mathbf q)&
\mathsf\Delta(\mathbf q)\\
\mathsf\Delta^\dagger(\mathbf q)&
\mathsf A^T(-\mathbf q)
\end{pmatrix}
}.
\]

\(\mathsf\Delta\) adalah creation-pair block. Dengan definisi \(\mathsf B\) di atas:

\[
\boxed{
\mathsf\Delta(\mathbf q)
=
\mathsf B(-\mathbf q)^*
}.
\]

Syarat Hermiticity:

\[
\mathcal H_{\mathrm{BdG}}^\dagger
=
\mathcal H_{\mathrm{BdG}}.
\]

Syarat bosonic pairing:

\[
\boxed{
\mathsf\Delta(\mathbf q)^T
=
\mathsf\Delta(-\mathbf q)
}.
\]

## 45. Hubungan dengan \(V^\dagger L V\) pada notes

Notes dan buku mendefinisikan vektor dengan susunan yang sama secara prinsip:

\[
V_{\mathbf q}
=
\begin{pmatrix}
a_{\mathbf q}^{(1)}\\
\vdots\\
a_{\mathbf q}^{(M)}\\
a_{-\mathbf q}^{(1)\dagger}\\
\vdots\\
a_{-\mathbf q}^{(M)\dagger}
\end{pmatrix}.
\]

Mereka menulis

\[
\boxed{
H_2
=
\sum_{\mathbf q}
V_{\mathbf q}^\dagger
L(\mathbf q)
V_{\mathbf q}
}.
\]

Karena Nambu space sudah menduplikasi sektor \(\mathbf q\) dan \(-\mathbf q\), buku membagi kontribusi ke empat quadrant menggunakan aturan *spread it around*. Akibatnya, untuk konvensi standar dokumen ini,

\[
\boxed{
L_{\mathrm{book}}(\mathbf q)
=
\frac12
\mathcal H_{\mathrm{BdG}}(\mathbf q)
}
\]

selama urutan basis dan Fourier convention sama.

Itulah asal faktor \(1/2\) pada diagonal \(L\) dan faktor \(1/4\) pada off-diagonal exchange di persamaan buku 4.119-4.123.

## 46. Bentuk blok buku

Buku menulis

\[
L(\mathbf q)
=
\begin{pmatrix}
P(\mathbf q)&Q(\mathbf q)\\
Q'(\mathbf q)&P'(\mathbf q)
\end{pmatrix}.
\]

Hubungannya:

- \(P\): normal block.
- \(Q\): creation atau annihilation pairing block, bergantung urutan basis.
- \(P',Q'\): partner yang diwajibkan Hermiticity dan particle-hole structure.

Sifat:

\[
P'(\mathbf q)=P(-\mathbf q)^*,
\]

\[
Q'(\mathbf q)=Q(-\mathbf q)^*.
\]

Untuk exchange isotropik, persamaan buku dapat ditulis:

\[
\begin{aligned}
L_{rr}=L_{r+M,r+M}
={}&
\frac12\sum_u
S_r z_{rr}^{(u)}J_{rr}^{(u)}
[1-\Gamma_{rr}^{(u)}(\mathbf q)]\\
&+
\frac12\sum_u\sum_{s\ne r}
S_s z_{rs}^{(u)}J_{rs}^{(u)}
F_{zz}(r,s).
\end{aligned}
\]

Untuk \(r\ne s\):

\[
\boxed{
L_{rs}
=
-\frac14
\sum_u
\sqrt{S_rS_s}
z_{rs}^{(u)}J_{rs}^{(u)}
\Gamma_{rs}^{(u)}(\mathbf q)^*
G_1(r,s)
}
\]

\[
\boxed{
L_{r+M,s+M}
=
-\frac14
\sum_u
\sqrt{S_rS_s}
z_{rs}^{(u)}J_{rs}^{(u)}
\Gamma_{rs}^{(u)}(\mathbf q)^*
G_1(r,s)^*
}
\]

\[
\boxed{
L_{r,s+M}
=
-\frac14
\sum_u
\sqrt{S_rS_s}
z_{rs}^{(u)}J_{rs}^{(u)}
\Gamma_{rs}^{(u)}(\mathbf q)^*
G_2(r,s)^*
}
\]

\[
\boxed{
L_{r+M,s}
=
-\frac14
\sum_u
\sqrt{S_rS_s}
z_{rs}^{(u)}J_{rs}^{(u)}
\Gamma_{rs}^{(u)}(\mathbf q)^*
G_2(r,s)
}.
\]

Untuk implementasi baru, bond-accumulator pada Bagian VII lebih aman daripada mengkode empat rumus ini secara terpisah. Bond-accumulator otomatis mencakup coupling dengan sublattice sama, sublattice berbeda, DMI, dan anisotropic exchange.

---

# Bagian XI - Algoritma assembly yang langsung dapat dikodekan

## 47. Data minimum yang harus dimiliki program

### Data sublattice

Untuk setiap sublattice \(r\), simpan:

- \(S_r\): spin magnitude.
- \(\boldsymbol\tau_r\): basis position.
- \(\widehat{\mathbf n}_r\): arah spin klasik.
- \(R_r\): local-to-global rotation matrix.
- daftar single-ion anisotropy.
- local atau global magnetic field.

Contoh struktur konseptual:

    Sublattice:
        spinMagnitude : real
        basisPosition : Vec3
        classicalDirection : Vec3
        rotationLocalToGlobal : Mat3
        anisotropies : list
        fieldEnergy : Vec3

### Data bond

Untuk setiap physical bond yang disimpan tepat satu kali:

    Bond:
        fromSublattice : integer r
        toSublattice : integer s
        cellOffset : integer lattice vector Delta
        globalCoupling : Mat3 K

Displacement fisiknya:

\[
\mathbf d_b
=
\sum_{\nu=1}^3\Delta_\nu\mathbf a_\nu
+\boldsymbol\tau_s-\boldsymbol\tau_r.
\]

\(\mathbf a_\nu\) adalah primitive lattice vectors.

Untuk isotropic exchange dan DMI sekaligus:

\[
\mathsf K_b
=
-J_bI_3
+
\begin{pmatrix}
0&D_{bz}&-D_{by}\\
-D_{bz}&0&D_{bx}\\
D_{by}&-D_{bx}&0
\end{pmatrix}
+\Gamma_b.
\]

\(\Gamma_b\) adalah symmetric anisotropic exchange bila ada.

## 48. Precomputation sebelum loop momentum

Untuk setiap sublattice:

1. Normalisasi \(\widehat{\mathbf n}_r\).
2. Bangun \(R_r\).
3. Periksa \(R_r^TR_r\simeq I\).
4. Periksa \(\det R_r\simeq1\).
5. Simpan

\[
c_r=\sqrt{\frac{S_r}{2}}.
\]

Untuk setiap bond:

1. Hitung displacement \(\mathbf d_b\).
2. Hitung local coupling

\[
\mathsf M_b
=
R_r^T\mathsf K_bR_s.
\]

3. Hitung

\[
T_b
=
c_rc_s
[M_{xx}+M_{yy}+i(M_{yx}-M_{xy})].
\]

4. Hitung

\[
P_b
=
c_rc_s
[M_{xx}-M_{yy}-i(M_{xy}+M_{yx})].
\]

5. Simpan \(M_{zz}\), mixed components, \(T_b\), dan \(P_b\).

Karena semua kuantitas tersebut tidak bergantung pada \(\mathbf q\), jangan hitung ulang di setiap momentum.

## 49. Assembly langsung untuk satu momentum

Untuk setiap \(\mathbf q\), buat

\[
\mathsf A(\mathbf q)=0_{M\times M},
\]

\[
\mathsf\Delta(\mathbf q)=0_{M\times M}.
\]

Untuk satu bond \(b:r\to s\) dengan displacement \(\mathbf d_b\), hitung

\[
\mathrm{phase}_b
=
e^{i\mathbf q\cdot\mathbf d_b}.
\]

### Diagonal longitudinal

\[
\boxed{
\mathsf A_{rr}
\mathrel{+}
=
-M_{zz}S_s
}
\]

\[
\boxed{
\mathsf A_{ss}
\mathrel{+}
=
-M_{zz}S_r
}.
\]

### Normal hopping

\[
\boxed{
\mathsf A_{rs}
\mathrel{+}
=
T_b\,\mathrm{phase}_b
}
\]

\[
\boxed{
\mathsf A_{sr}
\mathrel{+}
=
T_b^*\,\mathrm{phase}_b^*
}.
\]

### Creation pairing

\[
\boxed{
\mathsf\Delta_{rs}
\mathrel{+}
=
P_b^*\,\mathrm{phase}_b
}
\]

\[
\boxed{
\mathsf\Delta_{sr}
\mathrel{+}
=
P_b^*\,\mathrm{phase}_b^*
}.
\]

Update kedua arah pada \(\Delta\) diperlukan agar

\[
\mathsf\Delta(\mathbf q)^T
=
\mathsf\Delta(-\mathbf q).
\]

Untuk \(r=s\), kedua update masuk ke elemen yang sama. Ini menghasilkan kombinasi fase

\[
e^{i\mathbf q\cdot\mathbf d}
+e^{-i\mathbf q\cdot\mathbf d}
=
2\cos(\mathbf q\cdot\mathbf d),
\]

sesuai kebutuhan.

## 50. Tambahkan onsite anisotropy

Untuk anisotropi

\[
-K_r(\widehat{\mathbf m}_r\cdot\mathbf S_r)^2,
\]

hitung

\[
\mathbf c_r=R_r^T\widehat{\mathbf m}_r,
\]

\[
u_r=c_{rx}-ic_{ry}.
\]

Update:

\[
\boxed{
\mathsf A_{rr}
\mathrel{+}
=
K_rS_r
[2c_{rz}^2-(c_{rx}^2+c_{ry}^2)]
}
\]

\[
\boxed{
\mathsf\Delta_{rr}
\mathrel{+}
=
-K_rS_r(c_{rx}+ic_{ry})^2
}.
\]

Tidak ada fase karena interaksi onsite.

## 51. Tambahkan medan

Hitung

\[
\mathbf b_r=R_r^T\mathbf h_r.
\]

Update:

\[
\boxed{
\mathsf A_{rr}
\mathrel{+}
=
b_{rz}
}.
\]

Tidak ada pairing dari medan linear.

## 52. Bangun matriks BdG

Hitung juga \(\mathsf A(-\mathbf q)\) dan \(\mathsf\Delta(-\mathbf q)\), atau manfaatkan simetri yang sudah diverifikasi.

\[
\boxed{
\mathcal H_{\mathrm{BdG}}(\mathbf q)
=
\begin{pmatrix}
\mathsf A(\mathbf q)&
\mathsf\Delta(\mathbf q)\\
\mathsf\Delta^\dagger(\mathbf q)&
\mathsf A^T(-\mathbf q)
\end{pmatrix}
}.
\]

Ukuran:

\[
2M\times2M.
\]

## 53. Pseudocode lengkap assembly

Pseudocode berikut menggunakan konvensi physical bond disimpan sekali:

    precompute():
        for each sublattice r:
            n[r] = normalize(classicalDirection[r])
            R[r] = buildLocalFrame(n[r])
            assert norm(R[r]^T R[r] - I) < tolerance
            assert abs(det(R[r]) - 1) < tolerance
            c[r] = sqrt(S[r] / 2)

        for each bond b:
            r = b.from
            s = b.to
            d[b] = latticeVectors * b.cellOffset
                   + tau[s] - tau[r]
            Mloc[b] = R[r]^T * Kglobal[b] * R[s]

            M = Mloc[b]
            T[b] = c[r] * c[s] * (
                       M.xx + M.yy
                       + i * (M.yx - M.xy)
                   )
            P[b] = c[r] * c[s] * (
                       M.xx - M.yy
                       - i * (M.xy + M.yx)
                   )

    assemble(q):
        A = complexZeroMatrix(M, M)
        Delta = complexZeroMatrix(M, M)

        for each bond b:
            r = b.from
            s = b.to
            M = Mloc[b]
            phase = exp(i * dot(q, d[b]))

            A[r,r] += -M.zz * S[s]
            A[s,s] += -M.zz * S[r]

            A[r,s] += T[b] * phase
            A[s,r] += conjugate(T[b] * phase)

            Delta[r,s] += conjugate(P[b]) * phase
            Delta[s,r] += conjugate(P[b]) * conjugate(phase)

        for each onsite anisotropy on sublattice r:
            cAxis = transpose(R[r]) * easyAxis
            u = cAxis.x - i * cAxis.y

            A[r,r] += K * S[r] * (
                          2 * cAxis.z^2
                          - cAxis.x^2
                          - cAxis.y^2
                      )

            Delta[r,r] += -K * S[r] * conjugate(u)^2

        for each field on sublattice r:
            bLocal = transpose(R[r]) * fieldEnergy
            A[r,r] += bLocal.z

        Aminus, DeltaMinus = assembleBlocksAtMinusQOrUseCache(-q)

        Hbdg = blockMatrix(
            A,                 Delta,
            adjoint(Delta),    transpose(Aminus)
        )

        return Hbdg

Fungsi assembleBlocksAtMinusQOrUseCache tidak boleh memanggil assemble secara rekursif tanpa pemisahan. Dalam kode nyata, buat fungsi assembleAB(q) yang hanya menghasilkan \(A,\Delta\), lalu panggil untuk \(q\) dan \(-q\).

## 54. Assembly residual linear

Residual linear tidak bergantung pada \(\mathbf q\) untuk magnetic ground state periodik.

Mulai

    h[r] = 0 complex

Untuk setiap bond \(r\to s\):

\[
h_r
\mathrel{+}
=
c_rS_s(M_{xz}-iM_{yz}),
\]

\[
h_s
\mathrel{+}
=
S_rc_s(M_{zx}-iM_{zy}).
\]

Untuk anisotropi:

\[
h_r
\mathrel{+}
=
-2K_rc_{rz}S_r
\sqrt{\frac{S_r}{2}}
(c_{rx}-ic_{ry}).
\]

Untuk medan:

\[
h_r
\mathrel{+}
=
-\sqrt{\frac{S_r}{2}}
(b_{rx}-ib_{ry}).
\]

Periksa, misalnya,

\[
\boxed{
\max_r\frac{|h_r|}{E_{\mathrm{scale}}\sqrt{S_r}}
<10^{-10}
}
\]

untuk input analitik sederhana. Untuk ground state hasil minimisasi numerik, toleransi \(10^{-8}\) atau \(10^{-6}\) mungkin lebih realistis.

---

# Bagian XII - Diagonalization bosonik

## 55. Mengapa eigensolver Hermitian biasa tidak cukup?

Vektor Nambu mengandung annihilation dan creation operator. Komutatornya bukan identity matrix:

\[
[\Psi_{\mathbf q},\Psi_{\mathbf q}^\dagger]
=
\eta,
\]

dengan

\[
\boxed{
\eta
=
\begin{pmatrix}
I_M&0\\
0&-I_M
\end{pmatrix}
}.
\]

Persamaan gerak:

\[
i\hbar
\frac{d\Psi_{\mathbf q}}{dt}
=
\eta
\mathcal H_{\mathrm{BdG}}(\mathbf q)
\Psi_{\mathbf q}.
\]

Jadi dynamical matrix adalah

\[
\boxed{
\mathcal D(\mathbf q)
=
\eta\mathcal H_{\mathrm{BdG}}(\mathbf q)
}.
\]

\(\mathcal H_{\mathrm{BdG}}\) Hermitian, tetapi \(\mathcal D\) umumnya tidak Hermitian dalam inner product biasa.

## 56. Eigenvalue problem

Selesaikan

\[
\boxed{
\mathcal D(\mathbf q)x_n(\mathbf q)
=
\varepsilon_n(\mathbf q)x_n(\mathbf q)
}.
\]

Untuk sistem stabil, eigenvalue muncul berpasangan:

\[
\varepsilon_n(\mathbf q)>0,
\]

\[
-\varepsilon_n(-\mathbf q)<0.
\]

Energi magnon:

\[
\boxed{
\hbar\omega_n(\mathbf q)
=
\varepsilon_n(\mathbf q)
}
\]

dalam konvensi \(\frac12\Psi^\dagger\mathcal H_{\mathrm{BdG}}\Psi\).

Jika langsung memakai \(L\) buku, eigenvalue dynamical matrix mereka berhubungan dengan \(\hbar\omega/2\), karena \(L=\mathcal H_{\mathrm{BdG}}/2\).

## 57. Normalisasi paraunitary

Eigenvector tidak dinormalisasi dengan \(x^\dagger x=1\), tetapi dengan metric:

\[
\boxed{
x_n^\dagger\eta x_m
=
s_n\delta_{nm},
\qquad
s_n=\pm1
}.
\]

Mode fisik positif dipilih dari eigenvalue positif yang juga mempunyai positive metric norm:

\[
x_n^\dagger\eta x_n>0.
\]

Transformasi Bogoliubov \(T\) harus memenuhi

\[
\boxed{
T^\dagger\eta T=\eta
}.
\]

Jika program hanya memerlukan dispersi, eigenvalue positif cukup. Jika program akan menghitung intensitas neutron \(S(\mathbf q,\omega)\), eigenvector dan normalisasi paraunitary wajib benar.

## 58. Tanda sistem tidak stabil atau implementasi salah

Waspadai:

- eigenvalue memiliki imaginary part besar;
- tidak ada pasangan \(\pm\varepsilon\);
- mode positif memiliki norm metric negatif;
- \(\mathcal H_{\mathrm{BdG}}\) tidak Hermitian;
- residual \(H_1\) tidak nol.

Imaginary frequency dapat berarti:

1. konfigurasi klasik memang tidak stabil; atau
2. ada salah tanda, bond ganda, fase Fourier, atau rotasi.

Jangan langsung memaksa imaginary part menjadi nol.

---

# Bagian XIII - Contoh uji yang harus direproduksi kode

## 59. Feromagnet 1D isotropik

Hamiltonian:

\[
H=-J\sum_\ell
\mathbf S_\ell\cdot\mathbf S_{\ell+1},
\qquad J>0.
\]

Satu sublattice:

\[
M=1,
\qquad
R=I,
\qquad
\mathsf K=-JI.
\]

Jadi

\[
\mathsf M=-JI.
\]

Komponennya:

\[
M_{xx}=M_{yy}=M_{zz}=-J,
\]

\[
M_{xy}=M_{yx}=0.
\]

Dengan \(c^2=S/2\):

\[
T
=
\frac S2(-J-J)
=
-JS.
\]

\[
P
=
\frac S2(-J+J)
=
0.
\]

Diagonal longitudinal dari satu bond memberi \(+JS\) pada masing-masing endpoint. Setiap situs memiliki dua endpoint contribution, jadi

\[
A_{\mathrm{diag}}=2JS.
\]

Hopping:

\[
-JS e^{iqa}-JS e^{-iqa}
=
-2JS\cos(qa).
\]

Maka

\[
\boxed{
A(q)=2JS[1-\cos(qa)]
}
\]

dan

\[
\Delta(q)=0.
\]

Energi:

\[
\boxed{
\varepsilon(q)=2JS[1-\cos(qa)]
}.
\]

Test numerik:

\[
\varepsilon(0)=0,
\]

\[
\varepsilon(\pi/a)=4JS.
\]

## 60. Feromagnet 1D dengan easy-axis

Tambahkan

\[
-D\sum_\ell(S_\ell^z)^2.
\]

Karena easy axis sejajar local \(z\):

\[
A^{(D)}=2DS,
\qquad
\Delta^{(D)}=0.
\]

Maka

\[
\boxed{
\varepsilon(q)
=
2JS[1-\cos(qa)]+2DS
}.
\]

Test:

\[
\boxed{
\varepsilon(0)=2DS
}.
\]

## 61. Antiferomagnet 1D

Gunakan

\[
H
=
J_{\mathrm{AF}}
\sum_\ell
\mathbf S_\ell\cdot\mathbf S_{\ell+1},
\qquad J_{\mathrm{AF}}>0.
\]

Gunakan dua sublattice:

\[
\widehat{\mathbf n}_A=+\hat z,
\qquad
\widehat{\mathbf n}_B=-\hat z.
\]

Pilih

\[
R_A=I,
\]

\[
R_B=
\begin{pmatrix}
-1&0&0\\
0&1&0\\
0&0&-1
\end{pmatrix}.
\]

Global coupling:

\[
\mathsf K=J_{\mathrm{AF}}I.
\]

Local coupling:

\[
\mathsf M
=
R_A^T\mathsf KR_B
=
J_{\mathrm{AF}}
\begin{pmatrix}
-1&0&0\\
0&1&0\\
0&0&-1
\end{pmatrix}.
\]

Maka

\[
M_{xx}=-J_{\mathrm{AF}},
\]

\[
M_{yy}=+J_{\mathrm{AF}},
\]

\[
M_{zz}=-J_{\mathrm{AF}}.
\]

Normal hopping:

\[
T
=
\frac S2(-J_{\mathrm{AF}}+J_{\mathrm{AF}})
=
0.
\]

Pairing:

\[
P
=
\frac S2(-J_{\mathrm{AF}}-J_{\mathrm{AF}})
=
-J_{\mathrm{AF}}S.
\]

Dengan dua tetangga:

\[
\mathsf A(q)
=
2J_{\mathrm{AF}}S
\begin{pmatrix}
1&0\\
0&1
\end{pmatrix},
\]

\[
\mathsf\Delta(q)
=
-2J_{\mathrm{AF}}S\cos(qa)
\begin{pmatrix}
0&1\\
1&0
\end{pmatrix}.
\]

Diagonalization bosonik memberi

\[
\boxed{
\varepsilon(q)
=
2J_{\mathrm{AF}}S|\sin(qa)|
}.
\]

Ini adalah test wajib untuk anomalous block.

## 62. Feromagnet 1D dengan DMI sepanjang \(z\)

Hamiltonian:

\[
H
=
\sum_\ell
\left[
-J\mathbf S_\ell\cdot\mathbf S_{\ell+1}
+D\hat z\cdot
(\mathbf S_\ell\times\mathbf S_{\ell+1})
\right].
\]

Untuk spin klasik sepanjang \(z\):

\[
\mathsf K
=
\begin{pmatrix}
-J&D&0\\
-D&-J&0\\
0&0&-J
\end{pmatrix}.
\]

Hitung

\[
T
=
\frac S2
\left[
-2J+i(-D-D)
\right]
\]

\[
=
-S(J+iD).
\]

Pairing:

\[
P=0.
\]

Normal block:

\[
\begin{aligned}
A(q)
={}&
2JS
-S(J+iD)e^{iqa}\\
&-S(J-iD)e^{-iqa}.
\end{aligned}
\]

Gunakan

\[
(J+iD)e^{ix}
+(J-iD)e^{-ix}
=
2J\cos x-2D\sin x.
\]

Maka

\[
\boxed{
\varepsilon(q)
=
2JS[1-\cos(qa)]
+2DS\sin(qa)
}.
\]

Karena \(\sin(-qa)=-\sin(qa)\),

\[
\varepsilon(q)\neq\varepsilon(-q).
\]

Ini test bagus untuk fase kompleks dan orientasi DMI. Jika orientasi bond atau definisi \(\mathbf D\) dibalik, tanda suku \(\sin qa\) ikut terbalik.

---

# Bagian XIV - Validation checklist untuk program

## 63. Pemeriksaan geometri

Untuk setiap sublattice:

\[
\|R_r^TR_r-I\|<\epsilon,
\]

\[
|\det R_r-1|<\epsilon,
\]

\[
\|R_r\hat z-\widehat{\mathbf n}_r\|<\epsilon.
\]

Untuk setiap bond reverse:

\[
\mathsf K_{ji}=\mathsf K_{ij}^T.
\]

## 64. Pemeriksaan Hamiltonian

Untuk setiap \(\mathbf q\):

\[
\boxed{
\|\mathsf A-\mathsf A^\dagger\|<\epsilon
}
\]

\[
\boxed{
\|\mathsf\Delta(\mathbf q)
-\mathsf\Delta(-\mathbf q)^T\|<\epsilon
}
\]

\[
\boxed{
\|\mathcal H_{\mathrm{BdG}}
-\mathcal H_{\mathrm{BdG}}^\dagger\|<\epsilon
}.
\]

Gunakan relative tolerance terhadap skala energi terbesar, bukan absolute tolerance saja.

## 65. Pemeriksaan keadaan klasik

\[
\boxed{
\max_r|h_r|<\epsilon_{\mathrm{stationary}}
}.
\]

Jika tidak:

- periksa arah spin;
- periksa sign \(J\);
- periksa DMI orientation;
- periksa anisotropy axis;
- periksa transverse field;
- periksa bond yang hilang atau ganda.

## 66. Pemeriksaan spektrum

Untuk sistem tanpa anisotropi atau medan yang mematahkan simetri rotasi, harus ada Goldstone mode:

\[
\varepsilon(\mathbf q_G)\simeq0.
\]

FM sederhana:

\[
\mathbf q_G=0.
\]

Periksa pasangan eigenvalue:

\[
\{\varepsilon_n\}
\simeq
\{-\varepsilon_n\}.
\]

Periksa imaginary part:

\[
\max_n|\operatorname{Im}\varepsilon_n|
<\epsilon.
\]

## 67. Gauge invariance

Putar basis lokal \(x_r,y_r\) di sekitar \(z_r\) dengan sudut acak. Matriks \(A,\Delta\) dan eigenvector dapat berubah fase, tetapi energi harus tetap:

\[
\boxed{
\varepsilon_n^{\mathrm{gauge\ 1}}(\mathbf q)
=
\varepsilon_n^{\mathrm{gauge\ 2}}(\mathbf q)
}.
\]

Ini test kuat untuk rotasi dan pairing phases.

## 68. Bond-orientation invariance

Ganti penyimpanan bond

\[
(r,s,\mathbf d,\mathsf K)
\]

menjadi

\[
(s,r,-\mathbf d,\mathsf K^T).
\]

Spektrum tidak boleh berubah.

---

# Bagian XV - Kesalahan dan typo yang perlu dihindari dari notes

## 69. Tanda Hamiltonian pada notes semiklasik

Halaman awal sempat menulis

\[
H=+J\sum\mathbf S_i\cdot\mathbf S_j
\]

tetapi menjelaskan \(J>0\) sebagai feromagnetik. Penjelasan tersebut konsisten dengan

\[
H=-J\sum\mathbf S_i\cdot\mathbf S_j.
\]

Program harus memilih salah satu konvensi dan menyimpannya secara eksplisit.

## 70. Double counting exchange

Notes memakai faktor \(2\), sehingga hasil FM dan AF dua kali bentuk bond-once. Jangan mengoreksi hasil akhirnya tanpa sekaligus mengoreksi definisi Hamiltonian.

## 71. Eksponensial tetangga

Yang benar:

\[
e^{-ika}+e^{ika}=2\cos(ka).
\]

Beberapa baris notes tertulis \(e^{ika}+e^{ika}\), tetapi langkah cosinus berikutnya menunjukkan bahwa yang dimaksud adalah pasangan tanda \(\pm\).

## 72. Faktor dua anisotropi

Untuk

\[
-D(S^z)^2,
\]

turunannya

\[
-2DS^z.
\]

Jadi gap LSWT adalah

\[
2DS.
\]

Hasil \(DS\) hanya cocok dengan Hamiltonian \(-D(S^z)^2/2\).

## 73. Jumlah state spin

Spin \(S\) mempunyai \(2S+1\) state. Up/down saja hanya lengkap untuk \(S=1/2\). Untuk \(S>1/2\), keadaan \(|j\rangle\) pada derivasi satu magnon berarti \(m=S\to S-1\), bukan langsung \(m=S\to -S\).

## 74. Label raising/lowering

Pada CH2 halaman 2, formula lowering masih beberapa kali diberi label \(S^+\). Operator yang menurunkan \(m\) harus \(S^-\).

## 75. Tanda energi AF

Jika notes memakai

\[
H=-J\sum\mathbf S_i\cdot\mathbf S_j,
\qquad J<0,
\]

energi magnon positif harus ditulis memakai \(|J|\):

\[
\hbar\omega=2|J|S|\sin ka|
\]

atau faktor dua versi notes.

## 76. Energi magnetik dan definisi momen

Beberapa bagian notes berganti antara

\[
E=-\boldsymbol\mu\cdot\mathbf B
\]

dan tanda lain. Untuk coding LSWT, hindari ambiguitas dengan memasukkan langsung Zeeman energy vector:

\[
H_Z=-\mathbf h\cdot\mathbf S.
\]

Simpan \(\mathbf h\) dalam satuan energi. Hubungan dengan medan Tesla dan \(g\)-tensor dilakukan pada lapisan input.

## 77. Faktor Nambu pada \(L\)

Jangan mencampur

\[
H_2
=
\frac12\Psi^\dagger\mathcal H_{\mathrm{BdG}}\Psi
\]

dengan

\[
H_2=V^\dagger L V.
\]

Untuk basis dan convention yang sama:

\[
L=\frac12\mathcal H_{\mathrm{BdG}}.
\]

Jika faktor ini dicampur, seluruh frekuensi bisa salah faktor \(2\).

---

# Bagian XVI - Ringkasan implementasi

Pipeline program yang disarankan:

1. Baca lattice vectors, basis positions, spin magnitude, dan physical bond list.
2. Definisikan Hamiltonian dengan setiap bond disimpan satu kali.
3. Tentukan atau minimalkan classical spin directions \(\widehat{\mathbf n}_r\).
4. Bangun local frame \(R_r\).
5. Rotasikan setiap coupling:

\[
\mathsf M_b=R_r^T\mathsf K_bR_s.
\]

6. Dari setiap \(\mathsf M_b\), hitung \(T_b\), \(P_b\), \(M_{zz}\), dan linear residual.
7. Tambahkan onsite anisotropy dan field.
8. Pastikan \(H_1=0\).
9. Untuk setiap \(\mathbf q\), assemble \(\mathsf A(\mathbf q)\) dan \(\mathsf\Delta(\mathbf q)\).
10. Bangun \(\mathcal H_{\mathrm{BdG}}(\mathbf q)\).
11. Validasi Hermiticity dan pairing symmetry.
12. Diagonalize

\[
\eta\mathcal H_{\mathrm{BdG}}.
\]

13. Ambil \(M\) eigenvalue positif dan positive-norm.
14. Uji FM, easy-axis FM, AF, dan DMI chain sebelum memakai struktur kompleks.
15. Baru setelah spektrum benar, implementasikan eigenvector observables seperti neutron-scattering intensity.

Titik akhir teori yang dicari adalah

\[
\boxed{
H_2
=
\frac12\sum_{\mathbf q}
\Psi_{\mathbf q}^\dagger
\begin{pmatrix}
\mathsf A(\mathbf q)&\mathsf\Delta(\mathbf q)\\
\mathsf\Delta^\dagger(\mathbf q)&
\mathsf A^T(-\mathbf q)
\end{pmatrix}
\Psi_{\mathbf q}
+C
}.
\]

Seluruh exchange, anisotropy, DMI, dan magnetic field hanya mengubah elemen-elemen \(\mathsf A\) dan \(\mathsf\Delta\). Struktur Nambu Hamiltonian-nya tetap sama.

---

# Sumber yang dipakai

- [Notes Spinwave CH1 - Semiklasik](</Users/genius/Documents/Research Physics/Spin Wave/Notes_Spinwave_Semiklasik (1).pdf>), halaman 1-12: Heisenberg model, presesi, FM, easy-axis, dan AF.
- [Notes Spinwave CH2 - Kuantum](</Users/genius/Documents/Research Physics/Spin Wave/Notes_Spinwave_Kuantum.pdf>), halaman 1-4: ladder operator, satu spin flip, dan Fourier transform.
- [Spin-Wave Theory and its Applications to Neutron Scattering and THz Spectroscopy](</Users/genius/Documents/Research Physics/Spin Wave/Spin-Wave Theory and its Applications to Neutron scattering_Scan (1) (2).pdf>), PDF halaman 1-2 dan 9-12: local frame, HP, \(2M\times2M\) matrix, \(F\), \(G_1\), \(G_2\), anisotropy, field, dan DMI.
- [Hamiltonian.pdf](</Users/genius/Documents/Research Physics/Spin Wave/Hamiltonian.pdf>), halaman 1-15: ekspansi handwritten dari exchange sampai Hamiltonian umum \(V^\dagger L V\).

---

# Kamus simbol singkat

- \(S_r\): spin magnitude sublattice \(r\).
- \(\widehat{\mathbf n}_r\): arah spin klasik.
- \(R_r\): matriks local-to-global.
- \(U_r=R_r^T\): matriks global-to-local.
- \(\mathsf K_b\): coupling matrix bond dalam koordinat global.
- \(\mathsf M_b=R_r^T\mathsf K_bR_s\): coupling matrix bond dalam koordinat lokal.
- \(F(r,s)=U_rU_s^{-1}\): relative local-frame matrix untuk isotropic exchange.
- \(T_b\): normal hopping coefficient \(a_r^\dagger a_s\).
- \(P_b\): anomalous annihilation-pair coefficient \(a_ra_s\).
- \(\mathsf A(\mathbf q)\): normal block Hamiltonian bosonik.
- \(\mathsf\Delta(\mathbf q)\): creation-pair block Hamiltonian bosonik.
- \(\Psi_{\mathbf q}\): Nambu vector.
- \(\eta=\operatorname{diag}(I,-I)\): bosonic commutation metric.
- \(\varepsilon_n(\mathbf q)=\hbar\omega_n(\mathbf q)\): energi magnon.
