# Anchor Systems: Scores and Rationales (consolidated, rubric v0.9)

One file for review and for the scoring skill. Scores match anchors.json. Rule numbers follow Appendix A (R1–R9). Six axes: Axis 3 is cost side (running cost only); Axis 4 counts parameters fitted to data from the system's own campaign, measured or computed (R7); Axis 5 is the 0–4 ladder.

Basis: **E** explicit in the source paper; **I** inferred (±0.3 linear, ±0.5 Axis 4); **T** theoretical cost (Axis 3 only); **U** provided by the user when the paper lacks the evidence (scoring skill only).

**Review column:** ☑ = checked against the source paper by a person. New or changed rows start as ☐ until reviewed.

## DTCS

Source: Qian et al., Nat. Comput. Sci. 2025

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 1.0 | E | Bidirectional Theory/Physical Twin architecture on one interface (Ag(111)–H₂O). As demonstrated, the forward problem uses spectra published in 2019 and the inverse uses spectra generated from QM ground truth, so there is no live counterpart (R3); the loop is closed through the user. | ☑ |
| 2. Fidelity | 1.7 | E | ΔSCF binding energies, DFT-derived rate constants, mechanistic CRN (bulk ODE or surface CTMC); CRN ambiguity reduces the fidelity score. Instrument broadening is empirical (FWHM 1.3 eV). | ☑ |
| 3. Cost side | +1.5 | E | Beamtime is scarce, clustered into hours to days; a full inverse run takes 10–40 min. | ☑ |
| 4. Model dimensionality | 0.8 | E | N = 7 ΔG values inverted from QM-generated spectra produced in the authors' own campaign (R7). | ☑ |
| 5. VVUQ | 2.0 | E | Ground-truth recovery plus a degeneracy spread under an error cutoff (a form of UQ), but the check is against synthetic data, not independent experiments. | ☑ |
| 6. Autonomy | 1.0 | E | The AI recommends the next CRN and measurement; a human executes both. | ☑ |

## Bayesian Conavigation

Source: Slautin et al., ACS Nano 2026

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 2.0 | E | Automated AFM and kMC loops on one combinatorial library; outer loop updates bond energies every 10 iterations. | ☑ |
| 2. Fidelity | 1.1 | E | Coarse-grained kMC with two effective species, fixed step-edge parameters, and an empirical ×5 roughness scaling. | ☑ |
| 3. Cost side | +0.2 | E | Both sides expensive; 10 simulations per AFM measurement; full run about 2 h. | ☑ |
| 4. Model dimensionality | 0.5 | E | N = 3 bond energies fitted to the group's own AFM data. | ☑ |
| 5. VVUQ | 2.5 | E | GP posteriors plus an independent 100-point ground-truth grid. Point uncertainty is not propagated (authors' statement), so below 3. | ☑ |
| 6. Autonomy | 1.8 | E | No human intervention for 201 iterations. | ☑ |

## MATTERIX

Source: Darvish et al., Nat. Comput. Sci. 2026

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 1.0 | E | Pose estimates update the twin and the real robot mirrors it; chemistry is open-loop. | ☑ |
| 2. Fidelity | 1.2 | E | GPU physics engine plus a semantics engine with heat transfer and first-order kinetics. | ☑ |
| 3. Cost side | +0.7 | I | The goal is fewer physical make-and-test iterations; GPU simulation cost is modest. | ☑ |
| 4. Model dimensionality | 0.0 | E | Nothing fitted to own data; kinetic parameters come from databases; the online adaptation is future work. | ☑ |
| 5. VVUQ | 1.3 | E | Success rates over trials; simulated vs real pour volumes with spread. No held-out split, no UQ. | ☑ |
| 6. Autonomy | 0.9 | E | Workflows are written by a human or an LLM, then executed robotically. | ☑ |

## A-Lab

Source: Szymanski et al., Nature 2023

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 1.3 | E | Closed loop around recipe selection across 57 targets (R2). | ☑ |
| 2. Fidelity | 0.9 | E | NLP similarity and XGBoost recipe models, with DFT and active learning in ARROWS | ☑ |
| 3. Cost side | +1.8 | E | 4 h furnace dwell per batch over 17 days; computation precomputed. | ☑ |
| 4. Model dimensionality | 7.3 | E | Phase-ID CNN retrained per target on XRD patterns simulated in the campaign: six Conv1D layers (64 filters) plus dense layers of 3,100 and 1,200 on 4,501-point patterns, N ≈ 1.8×10⁷ (XRD-AutoAnalyzer source code). Recipe models were trained on literature (excluded); ARROWS³ stores observed reactions rather than parameters. | ☑ |
| 5. VVUQ | 2.3 | E | MC-dropout confidence on phase ID plus manual re-refinement as external validation. Uncertainty is not calibrated, and reliability is contested [47]. | ☑ |
| 6. Autonomy | 1.7 | E | Humans reload consumables and manually rescued two targets. | ☑ |

## CatDT

Source: Song et al., arXiv 2026

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 0.0 | E | Purely computational. | ☑ |
| 2. Fidelity | 1.4 | E | UMA/EquiformerV2 ML potentials, CI-NEB, microkinetics; benchmarked to DFT within about 0.1 eV. | ☑ |
| 3. Cost side | −1.6 | E/T | 5–30 min per catalyst on one GPU; no experiment in the loop. | ☑ |
| 4. Model dimensionality | 5.0 | I | Constant-potential MLIP heads and backbones trained by active learning within the campaign, starting from OC25-derived subsets (Methods 4.1). The 569-species database is a thermodynamic-correction set computed with UMA, not training data. Check which backbone and heads were trained and whether they were used in the benchmarks. | ☑ |
| 5. VVUQ | 2.0 | E | Independent benchmarks against DFT and 7 experimental systems (within 0.5–2×). No UQ. | ☑ |
| 6. Autonomy | 1.8 | E | No manual intervention at any link. | ☑ |

## Lithium-ion battery fast charging

Source: Wang et al., Nature 2022

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 0.3 | E | Offline design model; one manual virtual-to-physical step (predicted the 4C plating-free rate). | ☑ |
| 2. Fidelity | 1.8 | E | Physics-based electrochemical–thermal model, 3D fully coupled at pack level. | ☑ |
| 3. Cost side | +1.4 | T | Simulating a pack is cheap compared with building and testing one. | ☑ |
| 4. Model dimensionality | 0.7 | I | SEI-degradation fit (2 parameters) and transference number tuned to own cells; N ≈ 3–10. | ☑ |
| 5. VVUQ | 1.8 | E | Validated against measured voltage and temperature across C-rates; some parameters (e.g. transference number 0.48) were tuned to these data, so it falls short of a clean held-out split. No UQ. | ☑ |
| 6. Autonomy | 0.2 | E | Human-designed study. | ☑ |

## Raman Digital Twin

Source: Kowalski & Liang, ACS AMI 2026

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 0.0 | E | Precomputed library. | ☑ |
| 2. Fidelity | 1.9 | E | DFT phonons and Raman tensors via finite differences. | ☑ |
| 3. Cost side | +1.5 | E | In use, the twin is a lookup, so the Raman measurement dominates the per-use cost (R6). | ☑ |
| 4. Model dimensionality | 0.0 | E | Mixing weights were fit to literature frequencies, not own measurements. | ☑ |
| 5. VVUQ | 2.0 | E | LDA/PBE bracketing serves as a predictive range (UQ). The experimental comparison uses the same data the weights were fitted to, so it is not held-out. | ☑ |
| 6. Autonomy | 0.1 | E | Human-run. | ☑ |

## QCloudSim

Source: Luo et al., SIGSIM-PADS 2025

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 0.2 | E | One calibration snapshot imported at start; infrastructure-level (R2). | ☑ |
| 2. Fidelity | 0.3 | E | Discrete-event simulation with a multiplicative gate-error fidelity estimate. | ☑ |
| 3. Cost side | +1.6 | T | Explores scenarios that would need real QPU time. | ☑ |
| 4. Model dimensionality | 0.0 | E | Nothing fitted. | ☑ |
| 5. VVUQ | 0.3 | E | Run-to-run reproducibility only; no comparison with a real cloud. | ☑ |
| 6. Autonomy | 0.3 | E | Policies execute in simulation; humans design the studies. | ☑ |

## C³ (Wittler et al.)

Source: Wittler et al., PR Applied 2021

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 1.0 | E | Two-way architecture; demonstrated against simulated qubits, with sequential stages and human model decisions. | ☑ |
| 2. Fidelity | 1.3 | E | Detailed physical device model with fitted parameters. | ☑ |
| 3. Cost side | +0.8 | T | The experiment was emulated; on hardware, calibration time would dominate. | ☑ |
| 4. Model dimensionality | 1.3 | E | N ≈ 20 device parameters (Table I) fitted to emulated calibration data generated in the authors' own campaign (R7). | ☑ |
| 5. VVUQ | 2.5 | E | Held-out validation set and local sensitivity scans (partial UQ); no calibrated or propagated uncertainty. Demonstrated in simulation only. | ☑ |
| 6. Autonomy | 1.2 | E | Optimizers automated; stage and model choices human. | ☑ |

## LTME (Sentz et al.)

Source: Sentz et al., Quantum 2026

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 0.0 | E | Offline fit to recorded QuDIT trajectories. | ☑ |
| 2. Fidelity | 1.3 | E | GENERIC master equation with a small MLP term; parameters are pulse-specific. | ☑ |
| 3. Cost side | +1.2 | I | In use, the model is cheap to evaluate against tomography on the device (R6). | ☑ |
| 4. Model dimensionality | 2.3 | E | N ≈ 190 fitted to QuDIT trajectories from the group's own device. | ☑ |
| 5. VVUQ | 1.8 | E | Held-out time-window extrapolation and synthetic test trajectories, no UQ; fails to generalize across pulses. | ☑ |
| 6. Autonomy | 0.3 | E | Human-run. | ☑ |

---

# Reference Anchors (skill calibration; not in the manuscript)

These seven systems fill gaps the ten manuscript anchors leave: tight loops built on surrogates, VVUQ of 3 or above, quantum hardware, and worked examples of decision rules R1 and R4. They appear on the website and in the skill's references, but not in Figure 3 or Table 2. All rows reviewed.

## CAMEO

Source: Kusne et al., Nat. Commun. 11, 5966 (2020)

Worked example of R1 (human-mediated cap).

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 1.4 | E | Live closed loop at a synchrotron on one composition-spread wafer. In the Ge–Sb–Te run, a person converts raw ellipsometry into bandgap at every iteration, a transfer step on the decision timescale (capped at 1.5, R1). | ☑ |
| 2. Fidelity | 0.5 | E | GP property surrogate plus phase mapping constrained by the Gibbs phase rule. An AFLOW DFT prior was used only in the Fe–Ga–Pd benchmark. | ☑ |
| 3. Cost side | +1.6 | E | Beamtime-limited: about 10 h for 19 live iterations against about 90 h for full mapping. | ☑ |
| 4. Model dimensionality | 1.0 | I | GP and graph-clustering hyperparameters fitted to the run's own measurements, N ≈ 10. | ☑ |
| 5. VVUQ | 2.5 | E | Phase-map and GP uncertainty drive acquisition; benchmarked against fully measured ground truth with confidence intervals over repeated runs. Uncertainty is not calibrated. | ☑ |
| 6. Autonomy | 1.2 | E | Sample selection is automated; a person is required in every cycle for the bandgap step. | ☑ |

## Liu 2022 (DKL active learning on PFM)

Source: Liu et al., Nat. Mach. Intell. 4, 341 (2022)

Tight loop built on a model of the data rather than a physical model.

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 1.8 | E | Deployed on the operating microscope for 200 steps on one sample; each measurement retrains the model, and the model picks the next location. | ☑ |
| 2. Fidelity | 0.2 | E | Deep kernel learning maps topography patches to spectral targets. Physics enters only through a human-defined scalarizer, so it models the data, not the system. | ☑ |
| 3. Cost side | +1.5 | E | Spectroscopic acquisition time and probe stability limit sampling; model updates are fast. | ☑ |
| 4. Model dimensionality | 6.0 | E | MLP feature extractor (1000-500-50) on 20×20 patches (400 inputs), plus GP, N ≈ 9×10⁵, trained on the run's own measurements. Assumes a single input channel. | ☑ |
| 5. VVUQ | 2.3 | E | GP predictive variance plus an offline benchmark against a full ground-truth grid; the live run is not separately validated. | ☑ |
| 6. Autonomy | 1.6 | E | Exploration is autonomous; a person defines the target functional. | ☑ |

## Mobile robotic chemist

Source: Burger et al., Nature 583, 237 (2020)

Pure Bayesian-optimization loop with the highest autonomy.

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 1.3 | E | Batched closed loop over 8 days and 688 experiments. Each experiment is a new formulation rather than one monitored instance (capped at 1.5, R2). | ☑ |
| 2. Fidelity | 0.0 | E | GP Bayesian optimization; no physical model. | ☑ |
| 3. Cost side | +1.8 | E | Physical experiments dominate. | ☑ |
| 4. Model dimensionality | 1.1 | I | GP with ARD over 10 variables, N ≈ 12, fitted to the run's own data. | ☑ |
| 5. VVUQ | 2.0 | E | GP uncertainty used in acquisition; repeated control samples check reproducibility, not the model. | ☑ |
| 6. Autonomy | 1.9 | E | Autonomous for days, including navigation between stations; people set up stations and consumables. | ☑ |

## Dai 2024 (autonomous mobile robots for exploratory chemistry)

Source: Dai et al., Nature (2024), DOI 10.1038/s41586-024-08173-7

Worked example of R4 (no virtual model): an autonomous laboratory that is not a digital twin.

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 0.0 | E | Decisions come from a rule-based heuristic on NMR and UPLC-MS results; there is no virtual model of the chemistry (R4). | ☑ |
| 2. Fidelity | 0.0 | E | No forward model (R4). | ☑ |
| 3. Cost side | +1.8 | E | Synthesis and analysis dominate. | ☑ |
| 4. Model dimensionality | 0.0 | E | No model (R4). | ☑ |
| 5. VVUQ | 1.0 | E | Orthogonal analytical checks and reproducibility tests before scale-up; there is no model to validate. | ☑ |
| 6. Autonomy | 1.7 | E | The synthesis–analysis–decision cycle runs without human input; people set the thresholds. | ☑ |

## Koscher 2023

Source: Koscher et al., Science (2023), DOI 10.1126/science.adi1407

Large models retrained on the system's own measurements every iteration.

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 1.3 | E | Automated design–make–test–analyze loop over new molecules (capped at 1.5, R2). | ☑ |
| 2. Fidelity | 0.1 | E | Chemprop message-passing networks; no physical model. | ☑ |
| 3. Cost side | +1.7 | E | Multistep synthesis and characterization dominate; models retrain quickly. | ☑ |
| 4. Model dimensionality | 6.0 | I | Three Chemprop property models, each an ensemble retrained on the run's measurements every iteration, about 3×10⁵ parameters per model. The ensemble size is in the SM (plausible range 5.9–6.9). | ☑ |
| 5. VVUQ | 2.5 | E | Ensemble variance used in selection, plus prospective validation on new molecules; errors approach experimental uncertainty but are not formally calibrated. | ☑ |
| 6. Autonomy | 1.6 | E | People set and adjust the objectives. | ☑ |

## VDMN

Source: Robertson et al., arXiv:2512.18104 (2025)

The only system at VVUQ 3 or above.

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 0.0 | E | Offline predictions compared afterward with printed tensile specimens. | ☑ |
| 2. Fidelity | 1.3 | E | Physics-constrained deep material network trained on FFT homogenization. | ☑ |
| 3. Cost side | +1.5 | E | Per use, a 2.7 CPU-s prediction against printing and tensile testing (R6). | ☑ |
| 4. Model dimensionality | 4.1 | I | Depth-10 variational laminate tree trained on the authors' own FFT simulations (R7), N ≈ 10⁴, plus about 10 constituent parameters calibrated to their tensile data. | ☑ |
| 5. VVUQ | 3.0 | E | Analytic uncertainty propagation, simulation-based calibration tests, and experimental validation of predicted distributions. No credibility framework, so not 4. | ☑ |
| 6. Autonomy | 0.1 | E | Human-run. | ☑ |

## Müller 2025 (transmon digital twin)

Source: Mueller et al., arXiv:2504.08313 (2025)

Quantum system on real hardware.

| Axis | Score | Basis | Rationale | Review |
|---|---|---|---|---|
| 1. Coupling | 0.5 | E | One-way: calibration data and benchmark circuits feed the model. One fit was tested over a 33 h window; nothing steers the device. | ☑ |
| 2. Fidelity | 1.2 | E | Physics-based noise channels (T1/T2, ZZ crosstalk from detuning and anharmonicity) plus fitted terms. | ☑ |
| 3. Cost side | +1.3 | E | QPU time (80 circuits × 100,000 shots over 33 h) against cheap density-matrix emulation. | ☑ |
| 4. Model dimensionality | 0.6 | E | N = 4 fitted to the authors' own QPU data. | ☑ |
| 5. VVUQ | 2.3 | E | Held-out 3- and 4-qubit circuits, ablation by error channel, drift tracked over 33 h. The final parameter set was selected by hand; no parameter UQ. | ☑ |
| 6. Autonomy | 0.3 | E | Human-run fitting. | ☑ |
