#!/usr/bin/env python3
"""Standalone linear-spin-wave solver for the 1D J1-J2 cycloid.

This file does NOT import pyLiSW, SpinW, Sunny, or another spin-wave package.
Only NumPy and Matplotlib are used.  The calculation performed here is:

    classical spiral -> local spin rotations -> quadratic HP Hamiltonian
    -> bosonic BdG diagonalization -> S^{alpha beta}(q, omega)
    -> polarization factor -> Mn2+ form factor -> Gaussian broadening.

The defaults mirror SW_J1J2_1D.jl supplied by the user.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np


# =============================================================================
# 1. MODEL AND NUMERICAL PARAMETERS
# =============================================================================

LAMBDA = 10
NUM_CELL = 1
M = NUM_CELL * LAMBDA

J1 = -1.0
J2 = -(J1 / 4.0) / np.cos(2.0 * np.pi / LAMBDA)
SPIN = 1.0
G_FACTOR = 2.0

Q0 = 0.0
Q1 = 3.0 * np.pi
NQ = 150

W0 = -2.5
W1 = 2.5
NW = 100
GAUSSIAN_SIGMA_MEV = 0.1

TEMP_MEV = 0.001
USE_BOSE_FACTOR = False

# The Julia file implicitly treats q as inverse Angstrom in the form factor.
# Keep 1.0 to reproduce that convention, or use the real nearest-neighbour
# spacing of the material.
SITE_SPACING_ANGSTROM = 1.0

# Physical unpolarized-neutron intensity contains |f(Q)|^2.  Set this to 1
# only when reproducing the exact (unsquared) multiplication in the Julia file.
FORM_FACTOR_POWER = 2

# Plot palette inspired by the supplied orbital-density image:
# black -> violet -> orange -> yellow -> white.
INTENSITY_COLORS = (
    "#000000",
    "#18002f",
    "#55156f",
    "#a12b62",
    "#ed5a24",
    "#ff9d0a",
    "#ffd94a",
    "#fffef2",
)

# A tiny positive shift makes the exactly gapless Goldstone point numerically
# diagonalizable.  It is many orders below the plotted meV scale.
BDG_REGULARIZATION = 1.0e-10
METRIC_NORM_TOL = 1.0e-10


@dataclass(frozen=True)
class Bond:
    """Directed bond from site i in cell 0 to site j in cell_shift."""

    i: int
    j: int
    cell_shift: int
    exchange: float


@dataclass
class Spectrum:
    q: np.ndarray
    q_over_2pi: np.ndarray
    energy: np.ndarray
    mode_weight: np.ndarray
    form_factor: np.ndarray
    sqw: np.ndarray
    omega: np.ndarray
    max_hermiticity_error: float
    max_pairing_error: float
    max_imaginary_energy: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Standalone LSWT/BdG calculation for the 1D J1-J2 cycloid."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "SW_J1J2_from_scratch_results",
    )
    parser.add_argument("--show", action="store_true")
    return parser.parse_args()


# =============================================================================
# 2. CLASSICAL SPIRAL AND LOCAL COORDINATES
# =============================================================================

def rotation_matrix(theta: float, phi: float = 0.0) -> np.ndarray:
    """Return the local-to-global rotation U used in SW_J1J2_1D.jl.

    Its third column is the classical spin direction.  The first two columns
    span the transverse plane in which Holstein-Primakoff bosons fluctuate.
    """
    ct, st = np.cos(theta), np.sin(theta)
    cp, sp = np.cos(phi), np.sin(phi)
    return np.array(
        [
            [ct * cp, -sp, st * cp],
            [ct * sp, cp, st * sp],
            [-st, 0.0, ct],
        ],
        dtype=float,
    )


def local_frames() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    theta = np.arange(M, dtype=float) * 2.0 * np.pi / LAMBDA
    phi = np.zeros(M)
    rotations = np.array([rotation_matrix(t, p) for t, p in zip(theta, phi)])

    # u = e_x + i e_y and v = e_z in each site's local frame.
    u = rotations[:, :, 0] + 1j * rotations[:, :, 1]
    v = rotations[:, :, 2]
    return rotations, u, v


def build_directed_bonds() -> list[Bond]:
    """Create J1 and J2 bonds, including their reverse partners.

    Computing the target modulo M avoids the hard-coded edge assignments in
    the Julia file.  cell_shift records whether the target crosses a magnetic
    supercell boundary and therefore acquires a Bloch phase.
    """
    bonds: list[Bond] = []
    for distance, exchange in ((1, J1), (2, J2)):
        for i in range(M):
            target_unwrapped = i + distance
            j = target_unwrapped % M
            shift = target_unwrapped // M
            bonds.append(Bond(i, j, shift, exchange))
            bonds.append(Bond(j, i, -shift, exchange))
    return bonds


# =============================================================================
# 3. QUADRATIC HOLSTEIN-PRIMAKOFF / BOSONIC BdG HAMILTONIAN
# =============================================================================

def assemble_abc(
    h_supercell: float,
    u: np.ndarray,
    v: np.ndarray,
    bonds: list[Bond],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    r"""Construct the A(k), B(k), and C matrices.

    For the Nambu spinor Psi_k = (a_k, a^dagger_-k)^T,

        H_2 = 1/2 sum_k Psi_k^dagger H_BdG(k) Psi_k.

    The local transverse vector u_i=e_i^x+i e_i^y gives

        A_ij += (J_ij S/2) (u_i . u_j*) exp(+i 2 pi h R),
        B_ij += (J_ij S/2) (u_i . u_j ) exp(+i 2 pi h R),
        C_ii += J_ij S (v_i . v_j).

    Each physical bond is present in both directions, so A and the full BdG
    matrix acquire the required Hermitian/bosonic symmetries.
    """
    a_mat = np.zeros((M, M), dtype=complex)
    b_mat = np.zeros((M, M), dtype=complex)
    c_mat = np.zeros((M, M), dtype=complex)

    for bond in bonds:
        phase = np.exp(2j * np.pi * h_supercell * bond.cell_shift)
        prefactor = 0.5 * SPIN * bond.exchange

        a_mat[bond.i, bond.j] += (
            prefactor * np.dot(u[bond.i], np.conj(u[bond.j])) * phase
        )
        b_mat[bond.i, bond.j] += (
            prefactor * np.dot(u[bond.i], u[bond.j]) * phase
        )
        c_mat[bond.i, bond.i] += (
            SPIN * bond.exchange * np.dot(v[bond.i], v[bond.j])
        )

    return a_mat, b_mat, c_mat


def bdg_hamiltonian(
    h_supercell: float,
    u: np.ndarray,
    v: np.ndarray,
    bonds: list[Bond],
) -> np.ndarray:
    """Build the full 2M x 2M Hermitian bosonic BdG matrix."""
    a_k, b_k, c_k = assemble_abc(h_supercell, u, v, bonds)
    a_mk, b_mk, c_mk = assemble_abc(-h_supercell, u, v, bonds)

    return np.block(
        [
            [a_k - c_k, b_k],
            [np.conj(b_mk), np.conj(a_mk) - c_mk],
        ]
    )


def solve_bosonic_bdg(hamiltonian: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    r"""Solve eta H v_n = omega_n v_n and normalize v_n^dagger eta v_n.

    Ordinary Hermitian diagonalization is not correct for bosonic BdG systems.
    The commutator metric is

        eta = diag(+1,...,+1,-1,...,-1).

    The tiny diagonal regularization resolves the zero-norm eigenvectors at an
    exact Goldstone point without changing the visible dispersion.
    """
    eta = np.diag(np.concatenate((np.ones(M), -np.ones(M))))
    regularized = hamiltonian + BDG_REGULARIZATION * np.eye(2 * M)
    eigenvalues, eigenvectors = np.linalg.eig(eta @ regularized)

    max_imaginary = float(np.max(np.abs(eigenvalues.imag)))
    order = np.argsort(eigenvalues.real)[::-1]
    energies = eigenvalues.real[order]
    eigenvectors = eigenvectors[:, order]

    for n in range(2 * M):
        vector = eigenvectors[:, n]
        metric_norm = np.vdot(vector, eta @ vector).real
        if abs(metric_norm) < METRIC_NORM_TOL:
            raise RuntimeError(
                "A BdG eigenvector has zero bosonic norm. Increase "
                "BDG_REGULARIZATION slightly."
            )
        eigenvectors[:, n] = vector / np.sqrt(abs(metric_norm))

    return energies, eigenvectors, max_imaginary


# =============================================================================
# 4. DYNAMICAL STRUCTURE FACTOR AND NEUTRON FACTORS
# =============================================================================

def mode_structure_factor(
    q: float,
    eigenvectors: np.ndarray,
    rotations: np.ndarray,
) -> np.ndarray:
    r"""Calculate S^{alpha beta}_n(q) for all 2M modes.

    Linear HP theory gives the one-magnon amplitude

      F^alpha_n(q) = sum_r exp(-i q r)
          [(U_{alpha x}-iU_{alpha y}) v_{r n}
           +(U_{alpha x}+iU_{alpha y}) v_{M+r,n}].

    Then S^{alpha beta}_n = S/(2M) F^alpha_n F^{beta*}_n.
    The basis phase exp(-i q r), absent from the original Julia SS() routine,
    is required to place scattering weight at the correct momentum.
    """
    minus = rotations[:, :, 0] - 1j * rotations[:, :, 1]
    plus = rotations[:, :, 0] + 1j * rotations[:, :, 1]
    basis_phase = np.exp(-1j * q * np.arange(M))

    particle = eigenvectors[:M, :]
    hole = eigenvectors[M:, :]

    # Shape: (site, Cartesian component, mode).
    site_amplitude = (
        minus[:, :, None] * particle[:, None, :]
        + plus[:, :, None] * hole[:, None, :]
    )
    total_amplitude = np.sum(basis_phase[:, None, None] * site_amplitude, axis=0)

    # Shape: (alpha, beta, mode).
    return (SPIN / (2.0 * M)) * np.einsum(
        "an,bn->abn", total_amplitude, np.conj(total_amplitude)
    )


def polarization_tensor_for_q_along_x() -> np.ndarray:
    r"""Return delta_ab-Qhat_a Qhat_b for Q parallel to x.

    At q=0 we use the q->0 limit along the selected scan direction.
    """
    return np.diag([0.0, 1.0, 1.0])


def mn2_form_factor(q_inverse_angstrom: np.ndarray) -> np.ndarray:
    """Mn2+ dipole form factor using the coefficients in the Julia file."""
    j0_a, j0_little_a = 0.4220, 17.6840
    j0_b, j0_little_b = 0.5948, 6.0050
    j0_c, j0_little_c = 0.0043, -0.6090
    j0_d = -0.0219

    j2_a, j2_little_a = 2.0515, 15.5561
    j2_b, j2_little_b = 1.8841, 6.0625
    j2_c, j2_little_c = 0.4787, 2.2323
    j2_d = 0.0027

    s_squared = (q_inverse_angstrom / (4.0 * np.pi)) ** 2
    j0 = (
        j0_a * np.exp(-j0_little_a * s_squared)
        + j0_b * np.exp(-j0_little_b * s_squared)
        + j0_c * np.exp(-j0_little_c * s_squared)
        + j0_d
    )
    j2 = s_squared * (
        j2_a * np.exp(-j2_little_a * s_squared)
        + j2_b * np.exp(-j2_little_b * s_squared)
        + j2_c * np.exp(-j2_little_c * s_squared)
        + j2_d
    )
    return j0 + ((G_FACTOR - 2.0) / G_FACTOR) * j2


def mode_bose_multiplier(energies: np.ndarray) -> np.ndarray:
    """Detailed-balance multiplier; unity reproduces the Julia calculation."""
    if not USE_BOSE_FACTOR:
        return np.ones_like(energies)

    absolute_energy = np.maximum(np.abs(energies), 1.0e-12)
    n_bose = 1.0 / np.expm1(absolute_energy / TEMP_MEV)
    return np.where(energies >= 0.0, 1.0 + n_bose, n_bose)


def gaussian(x: np.ndarray, sigma: float) -> np.ndarray:
    """Normalized Gaussian approximation to delta(x)."""
    return np.exp(-0.5 * (x / sigma) ** 2) / (np.sqrt(2.0 * np.pi) * sigma)


# =============================================================================
# 5. COMPLETE q AND omega CALCULATION
# =============================================================================

def calculate_spectrum() -> Spectrum:
    q_values = np.linspace(Q0, Q1, NQ)
    omega = np.linspace(W0, W1, NW)

    rotations, u, v = local_frames()
    bonds = build_directed_bonds()
    polarization = polarization_tensor_for_q_along_x()

    energies = np.empty((NQ, 2 * M), dtype=float)
    weights = np.empty((NQ, 2 * M), dtype=float)

    max_hermiticity_error = 0.0
    max_pairing_error = 0.0
    max_imaginary_energy = 0.0

    for iq, q in enumerate(q_values):
        # The magnetic cell is M sites long, so its reciprocal coordinate is
        # h = M q/(2 pi). Bloch phases use exp(i 2 pi h R).
        h_supercell = M * q / (2.0 * np.pi)
        hamiltonian = bdg_hamiltonian(h_supercell, u, v, bonds)
        max_hermiticity_error = max(
            max_hermiticity_error,
            float(np.max(np.abs(hamiltonian - hamiltonian.conj().T))),
        )

        mode_energy, eigenvectors, imaginary_error = solve_bosonic_bdg(hamiltonian)
        energies[iq] = mode_energy
        max_imaginary_energy = max(max_imaginary_energy, imaginary_error)
        max_pairing_error = max(
            max_pairing_error,
            float(np.max(np.abs(mode_energy + mode_energy[::-1]))),
        )

        sab = mode_structure_factor(q, eigenvectors, rotations)
        neutron_weight = np.einsum("ab,abn->n", polarization, sab).real
        weights[iq] = np.clip(neutron_weight, 0.0, None)

    q_inverse_angstrom = q_values / SITE_SPACING_ANGSTROM
    form_factor = mn2_form_factor(q_inverse_angstrom)
    weights *= form_factor[:, None] ** FORM_FACTOR_POWER
    weights *= mode_bose_multiplier(energies)

    delta_energy = omega[None, None, :] - energies[:, :, None]
    sqw = np.sum(
        weights[:, :, None] * gaussian(delta_energy, GAUSSIAN_SIGMA_MEV),
        axis=1,
    )

    return Spectrum(
        q=q_values,
        q_over_2pi=q_values / (2.0 * np.pi),
        energy=energies,
        mode_weight=weights,
        form_factor=form_factor,
        sqw=sqw,
        omega=omega,
        max_hermiticity_error=max_hermiticity_error,
        max_pairing_error=max_pairing_error,
        max_imaginary_energy=max_imaginary_energy,
    )


def validate_spectrum(spectrum: Spectrum) -> None:
    """Fail loudly if the basic bosonic-Hamiltonian identities are broken."""
    if not np.all(np.isfinite(spectrum.energy)):
        raise RuntimeError("Non-finite magnon energy encountered.")
    if not np.all(np.isfinite(spectrum.mode_weight)):
        raise RuntimeError("Non-finite mode weight encountered.")
    if not np.all(np.isfinite(spectrum.sqw)):
        raise RuntimeError("Non-finite S(q,w) encountered.")
    if spectrum.max_hermiticity_error > 1.0e-10:
        raise RuntimeError("The BdG Hamiltonian is not Hermitian.")
    if spectrum.max_imaginary_energy > 1.0e-6:
        raise RuntimeError(
            "A sizeable imaginary magnon energy indicates an unstable classical state."
        )
    if spectrum.max_pairing_error > 1.0e-6:
        raise RuntimeError("Bosonic eigenvalues do not occur in +/- pairs.")

    pitch = 2.0 * np.pi / LAMBDA
    stationarity = J1 * np.sin(pitch) + 2.0 * J2 * np.sin(2.0 * pitch)
    if abs(stationarity) > 1.0e-12:
        raise RuntimeError("J1, J2, and LAMBDA do not define a stationary spiral.")


# =============================================================================
# 6. OUTPUT
# =============================================================================

def write_csv_files(output_dir: Path, spectrum: Spectrum) -> list[Path]:
    dispersion_path = output_dir / "SW_J1J2_dispersion_from_scratch.csv"
    with dispersion_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["q_over_2pi"]
            + [f"omega_branch_{n:02d}_meV" for n in range(2 * M)]
            + [f"weight_branch_{n:02d}" for n in range(2 * M)]
        )
        for iq in range(NQ):
            writer.writerow(
                [spectrum.q_over_2pi[iq]]
                + spectrum.energy[iq].tolist()
                + spectrum.mode_weight[iq].tolist()
            )

    intensity_path = output_dir / "SW_J1J2_intensity_from_scratch.csv"
    with intensity_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["q_over_2pi", "omega_meV", "intensity"])
        for iq, q_value in enumerate(spectrum.q_over_2pi):
            for iw, energy_value in enumerate(spectrum.omega):
                writer.writerow([q_value, energy_value, spectrum.sqw[iq, iw]])

    return [dispersion_path, intensity_path]


def robust_vmax(data: np.ndarray, percentile: float = 99.5) -> float:
    positive = data[np.isfinite(data) & (data > 0.0)]
    return float(np.percentile(positive, percentile)) if positive.size else 1.0


def make_plots(output_dir: Path, spectrum: Spectrum, show: bool) -> list[Path]:
    if not show:
        import matplotlib

        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    orbital_cmap = LinearSegmentedColormap.from_list(
        "orbital_black_purple_orange_white",
        INTENSITY_COLORS,
        N=256,
    )
    orbital_cmap.set_under("#000000")
    orbital_cmap.set_bad("#000000")

    plt.rcParams.update(
        {
            "figure.dpi": 130,
            "savefig.dpi": 220,
            "font.size": 10,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
        }
    )
    paths: list[Path] = []

    fig, ax = plt.subplots(figsize=(7.8, 4.6), constrained_layout=True)
    ax.plot(spectrum.q_over_2pi, spectrum.form_factor, color="#285f8f", lw=2)
    ax.set(
        xlabel=r"$q/(2\pi)$",
        ylabel=r"$f_{\mathrm{Mn}^{2+}}(Q)$",
        title=rf"Mn$^{{2+}}$ magnetic form factor, $a={SITE_SPACING_ANGSTROM:g}$ Angstrom",
    )
    ax.grid(alpha=0.2)
    path = output_dir / "plot_SW_J1J2_magform_from_scratch.png"
    fig.savefig(path)
    paths.append(path)

    fig, ax = plt.subplots(figsize=(8.3, 5.0), constrained_layout=True)
    ax.set_facecolor("#000000")
    vmax_weight = robust_vmax(spectrum.mode_weight, 99.0)
    artist = None
    for mode in range(2 * M):
        artist = ax.scatter(
            spectrum.q_over_2pi,
            spectrum.energy[:, mode],
            c=spectrum.mode_weight[:, mode],
            cmap=orbital_cmap,
            vmin=0.0,
            vmax=vmax_weight,
            s=9,
            linewidths=0,
        )
    ax.axhline(0.0, color="0.25", lw=0.7)
    ax.set(
        xlabel=r"$q/(2\pi)$",
        ylabel=r"$\hbar\omega$ (meV)",
        title=rf"Standalone bosonic BdG: $J_1={J1:g}$, $J_2={J2:.6f}$ meV, $S={SPIN:g}$",
    )
    if artist is not None:
        fig.colorbar(artist, ax=ax, label="neutron mode weight (arb. unit)")
    path = output_dir / "plot_SW_J1J2_dispersion_from_scratch.png"
    fig.savefig(path)
    paths.append(path)

    vmax_sqw = robust_vmax(spectrum.sqw)
    fig, ax = plt.subplots(figsize=(8.3, 5.0), constrained_layout=True)
    image = ax.pcolormesh(
        spectrum.q_over_2pi,
        spectrum.omega,
        spectrum.sqw.T,
        shading="auto",
        cmap=orbital_cmap,
        vmin=0.0,
        vmax=vmax_sqw,
    )
    ax.set(
        xlabel=r"$q/(2\pi)$",
        ylabel=r"$\hbar\omega$ (meV)",
        title=rf"Standalone $S(Q,\omega)$, Gaussian $\sigma={GAUSSIAN_SIGMA_MEV:g}$ meV",
        ylim=(W0, W1),
    )
    fig.colorbar(image, ax=ax, label="intensity (arb. unit)")
    path = output_dir / "plot_SW_J1J2_intensity_from_scratch.png"
    fig.savefig(path)
    paths.append(path)

    fig, (ax0, ax1) = plt.subplots(
        2, 1, figsize=(9.0, 8.0), sharex=True, constrained_layout=True
    )
    ax0.set_facecolor("#000000")
    for mode in range(2 * M):
        ax0.scatter(
            spectrum.q_over_2pi,
            spectrum.energy[:, mode],
            c=spectrum.mode_weight[:, mode],
            cmap=orbital_cmap,
            vmin=0.0,
            vmax=vmax_weight,
            s=3,
            alpha=0.8,
        )
    ax0.axhline(0.0, color="0.65", lw=0.6)
    ax0.set(ylabel=r"$\hbar\omega$ (meV)", title=f"{2*M} bosonic branches")

    image = ax1.pcolormesh(
        spectrum.q_over_2pi,
        spectrum.omega,
        spectrum.sqw.T,
        shading="auto",
        cmap=orbital_cmap,
        vmin=0.0,
        vmax=vmax_sqw,
    )
    ax1.set(
        xlabel=r"$q/(2\pi)$",
        ylabel=r"$\hbar\omega$ (meV)",
        title=r"Unpolarized-neutron intensity $S(Q,\omega)$",
        ylim=(W0, W1),
    )
    fig.colorbar(image, ax=ax1, label="intensity (arb. unit)")
    path = output_dir / "plot_SW_J1J2_combined_from_scratch.png"
    fig.savefig(path)
    paths.append(path)

    if show:
        plt.show()
    else:
        plt.close("all")
    return paths


def main() -> int:
    args = parse_args()
    if not args.show:
        import matplotlib

        matplotlib.use("Agg")

    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    spectrum = calculate_spectrum()
    validate_spectrum(spectrum)
    csv_paths = write_csv_files(output_dir, spectrum)
    plot_paths = make_plots(output_dir, spectrum, args.show)

    print("Standalone J1-J2 LSWT calculation completed.")
    print(f"J1={J1:.12g} meV, J2={J2:.12g} meV, S={SPIN:g}")
    print(f"M={M}; BdG dimension={2*M}x{2*M}; q points={NQ}; omega points={NW}")
    print(f"Energy range found: {spectrum.energy.min():.9g} .. {spectrum.energy.max():.9g} meV")
    print(f"Max Hermiticity error: {spectrum.max_hermiticity_error:.3e}")
    print(f"Max +/- pairing error: {spectrum.max_pairing_error:.3e} meV")
    print(f"Max imaginary eigenvalue: {spectrum.max_imaginary_energy:.3e} meV")
    print("Saved:")
    for path in [*csv_paths, *plot_paths]:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
