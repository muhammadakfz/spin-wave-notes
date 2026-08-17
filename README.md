# Spin Wave Notes

Personal research notes and reproducible computational exercises on linear spin-wave theory, magnon dispersion, bosonic Bogoliubov-de Gennes diagonalization, and neutron-scattering intensity.

## Repository contents

- `notes/`: detailed derivation from spin operators to the general quadratic Hamiltonian.
- `src/`: standalone Python implementation of the commensurate 1D `J1-J2` cycloid.
- `notebooks/`: audited LSWT notebook and a pyLiSW-style learning notebook.
- `reports/`: numerical and physical audit of the LSWT implementation.
- `paper/`: LaTeX sources and rendered PDF notes.
- `figures/`: representative dispersion and spectral-intensity plots.
- `results/`: compact validation logs and selected numerical exports.

## Standalone calculation

The standalone solver uses only NumPy and Matplotlib. It implements

```text
classical spiral
-> local spin rotations
-> quadratic Holstein-Primakoff Hamiltonian
-> bosonic BdG diagonalization
-> one-magnon matrix elements
-> neutron polarization and magnetic form factor
-> Gaussian-broadened S(q, omega)
```

Create an environment and run it with:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 src/SW_J1J2_1D_from_scratch.py --output-dir results/generated
```

The default model follows the supplied `J1-J2` example:

```text
J1 = -1
J2 = 0.309016994375
S = 1
spiral period = 10 sites
BdG dimension = 20 x 20
```

## Validation baseline

The standalone implementation currently reports:

- maximum Hermiticity error: `0`;
- maximum positive/negative eigenvalue pairing error: `2.442e-14 meV`;
- maximum imaginary eigenvalue: `1.835e-12 meV`.

The audited notebook additionally checks the ferromagnetic and antiferromagnetic limits, spiral phase, phase boundary, BdG residuals, paraunitary normalization, periodicity, Gaussian normalization, spectral-tensor Hermiticity, and the transverse one-magnon sum rule.

## Scope

The current calculations are one-dimensional linear spin-wave models. Absolute neutron cross-sections still require material-specific ion data, a physical `g` tensor, Debye-Waller factors, absolute momentum units, sample normalization, and instrument prefactors.
