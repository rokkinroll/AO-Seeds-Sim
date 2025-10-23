# AO Seeds Sim: SEQ Outbursts Extension

Repo for "SEQ Outbursts in the AO Model: Predictions for Recycling Cosmology" (Zenodo DOI: 10.5281/zenodo.17421649; v2 of original AO Model DOI: 10.5281/zenodo.17417985).

## Original AO Sims (Main Branch)
- Run `python main.py` for base funnel density/M(<r) (Appendix A of original paper).
- Outputs: figs/fig1_density.png, fig2_mass.png.

## SEQ Outbursts Extension (seq_outbursts Branch)
- **Quick Run for Manuscript Outputs**:
  1. Install deps: `pip install -r requirements.txt`
  2. Run sim: `python seq_sweep.py`
     - Generates `seq_sweep.png` (Fig 4).
     - Prints: P_jet(0.10): 1.99e+44 erg s^{-1}; ε(0.70): 7.00e-04 (matches Table 1).
- **Monte Carlo Uncertainty**: Built-in (σ_ε < 5% from n_s ±20%).
- **Figs**: seq_sweep.png (left: P_jet vs SEQ; right: ε vs SEQ with bands/thresholds).

## Outputs Match Manuscript
- Baseline Ω_AO ≈ 1 at SEQ=0.70.
- Thresholds: Outburst at 0.40, halo at 0.70.

## Branches
- main: Original AO sims.
- seq_outbursts: This extension (v1.0).

License: CC-BY 4.0. Questions: @rokkinroll on X. Emblem: yin_yang_seed.png (visuals).