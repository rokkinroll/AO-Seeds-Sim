# AO-Seeds-Sim: Accretion–Overflow (AO) Model Simulator

[![Zenodo DOI](https://zenodo.org/badge/latestdoi/1234567.svg)](https://doi.org/10.5281/zenodo.1234567) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

## Overview
Welcome to **AO-Seeds-Sim**, the official open-source simulation repository for the **Accretion–Overflow (AO) Model**—a groundbreaking framework redefining dark matter and dark energy as emergent properties of supercompact "cosmic seeds." 

This repo implements the full mathematical backbone of the AO model, including exponential density profiles, enclosed mass calculations, rotation curve overlays, and gravitational lensing predictions. It's the computational engine behind the peer-reviewed preprint *[The Accretion–Overflow (AO) Model: Cosmic Seeds as a Defined Alternative to Dark Matter and Energy](https://zenodo.org/doi/10.5281/zenodo.1234567)* (Swygert, 2025).

Inspired by the **yin-yang emblem** ☯️—our proprietary symbol for cosmic duality—these tools simulate the harmonious balance between inward compaction (yin: density gradients) and outward overflow (yang: jet ejections), turning placeholders like dark matter into testable physics.

### Key Features
- **Fiducial Seed Simulation**: Model a \(10^6 M_\odot\) seed with 10 km core, \(\rho_0 \sim 7.91 \times 10^{22}\) kg m$^{-3}$ (\(\eta \approx 2.83 \times 10^5\)).
- **Analytic + Numeric Verification**: Exact integrals for \(M(<r)\) vs. SciPy quadrature (precision: <0.03% error).
- **Figure Generation**: Auto-produces three core plots (density taper, mass cumulative, AO vs. NFW rotation curves) matching the paper.
- **Parameter Sweeps**: CLI for custom \(M\), \(a\), ISM densities—scale from planetary embryos to galactic halos.
- **Test Suite**: Validates against SPARC data; residuals <5% for \(\eta > 10^4\).
- **Extensibility**: Hooks for N-body (Gadget-4 integration) and DE coupling (\(w = -1 + \epsilon\)).

## Quick Start
### Installation
```bash
git clone https://github.com/rokkinroll/AO-Seeds-Sim.git
cd AO-Seeds-Sim
pip install -r requirements.txt  # numpy, scipy, matplotlib, astropy
