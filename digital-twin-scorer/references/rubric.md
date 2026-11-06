# Digital Twin Design Rubric (v0.9)

Source: Grieder & Qian, "What Makes a Digital Twin?", Appendix A. Six axes; rules R1–R9.

## Background: the four criteria of a digital twin
1. A specific, live physical counterpart being monitored, not a general class of systems.
2. Automated data flow in both directions, physical to virtual and virtual to physical.
3. Continuous updating as the physical system evolves.
4. Genuine predictive capability that informs a real decision.

Axis 1 is the graded form of these criteria. Whether the forward model is physically grounded is read from Axis 2. Automation of data flow (Axis 1) and autonomy of decisions (Axis 6) are scored separately.

## Scores and basis codes
- Scores are given to one decimal place. The levels below are anchors; a system between two anchors receives an intermediate value.
- Every score carries a basis:
  - **E (explicit):** the source states the evidence.
  - **I (inferred):** follows from the technique or system type.
  - **T (theoretical):** Axis 3 only, when no physical counterpart was run; reflects the estimated cost of the corresponding experiment.
  - **U (user-provided):** the paper lacks the evidence and the user supplied it.

## Axes

### 1. Bidirectional coupling (loop closure), 0 to 2
Is a specific live physical instance in an automated two-way loop with the model?
- **0, Digital Model:** no automated flow to a specific physical instance; built and validated offline against static or historical data (precomputed library, offline design model).
- **1, Digital Shadow:** automated flow in one direction only, or the loop is closed for a non-scientific subsystem (e.g. robot motion) while the chemistry stays open.
- **2, Digital Twin:** automated bidirectional flow, in which measurements update the model and model predictions steer the next physical action, continuously, on one live instance.

### 2. Forward-model fidelity (surrogate to mirror), 0 to 2
What is the forward map made of?
- **0, Surrogate:** fast data-driven or statistical approximator (discrete-event simulation, pure ML or GP emulator); no explicit first-principles physics in the forward map.
- **1, Hybrid:** reduced-physics or coarse-grained model with learned components, or a physics engine with approximate kinetics.
- **2, Faithful mirror:** first-principles or ab initio forward calculation (DFT, resolved electrochemical–thermal PDEs, mechanistic CRN) meant to reproduce the physics and not just the observable.

### 3. Cost side, −2 to +2 (diverging)
Once the twin exists, which side, digital or physical, is the bottleneck per iteration (or per use, R6)?
- **−2:** digital side dominates; each evaluation is an expensive simulation, and the physical measurement is cheap or absent.
- **−1:** digital-leaning.
- **0:** both comparable and non-trivial.
- **+1:** physical-leaning.
- **+2:** physical side dominates (scarce beamtime, robotic synthesis, real QPU time); model evaluation is cheap by comparison.

Score by reported wall-clock time or cost per iteration. Only the running cost is scored; one-time costs of building the twin (simulation libraries, model training, calibration data) are not.

### 4. Model dimensionality, log₁₀ N (0 to 9)
N is the number of model parameters fitted or fine-tuned to data from the system's own campaign, measured or computed (R7). N = 0 scores 0. Pretrained weights, parameters fitted to literature or community data, hand-set constants, and first-principles quantities are excluded.
- **0–1:** N ≤ 10 (rate constants, bond energies); identifiable from one campaign.
- **1–3:** 10 < N ≤ 10³ (physics model with calibrated parameters, small neural terms).
- **3–6:** 10³ < N ≤ 10⁶ (neural surrogates, deep-kernel feature extractors trained on own data).
- **> 6:** N > 10⁶ (large networks fine-tuned on own data; not identifiable from a single campaign).

Count parameters from the architecture when the paper or its code gives one, and show the arithmetic in the rationale.

### 5. VVUQ maturity, 0 to 4 (ladder)
- **0, None:** no comparison with independent data; no uncertainty quantified.
- **1, Point agreement:** outputs compared with data (overlays, parity, success rates, benchmark values), with no held-out split and no UQ.
- **2, Validation or UQ:** either validation against data not used to build or fit the model, or quantified predictive uncertainty (GP posterior, ensemble variance, functional bracketing).
- **3, Validation and UQ:** both, with uncertainty propagated from inputs or measurements to predictions, or checked against data (calibration or coverage tests).
- **4, Credibility:** a structured credibility assessment for a stated context of use (e.g. ASME V&V 40), or an error budget covering measurement, data, modeling, and interpretation errors.

### 6. Autonomy, 0 to 2
- **0, Human-in-loop:** a human picks the next step and interprets results.
- **1, Semi-autonomous:** the system decides some steps (e.g. acquisition picks the next sample) with human oversight.
- **2, Autonomous or agentic:** runs the decide–act–update cycle over many iterations with essentially no human intervention.

## Decision rules
- **R1, Human-mediated steps (Axis 1):** if a person must transfer data or proposals between the virtual and physical sides on the timescale of the decisions being made, coupling is capped at 1.5. Human oversight without a transfer step is scored on Axis 6.
- **R2, No single physical instance (Axis 1):** an automated two-way loop whose counterpart is a sequence of new samples or an infrastructure, rather than one monitored instance, is capped at 1.5 (criterion 1).
- **R3, Demonstrated, not designed:** score systems as they ran in the source publication. Capabilities that are described, planned, or demonstrated only against a simulated or emulated physical side are noted but not scored. Against a simulated physical side, score Axis 1 as if no live counterpart exists, plus up to 1.0 for a closed two-way architecture.
- **R4, No virtual model:** systems whose decisions come from heuristics, rule sets, or planners, with no predictive model of the physical system, score 0 on Axes 1, 2, and 4 and are identified as autonomous laboratories rather than digital twins.
- **R5, In-silico autonomy (Axis 6):** autonomy is capped at 1.0 when the decide–act–update cycle never acts on physical hardware.
- **R6, Offline twins (Axis 3):** for twins with no running loop, the cost side compares the cost per use of the twin (a lookup or prediction) with the physical measurement it informs or replaces.
- **R7, Own data (Axis 4):** own data are data generated in the system's own campaign, whether measured on the physical counterpart or computed by the authors (simulations, synthetic spectra, emulated devices, DFT training sets built for the work), including the same group's archival data on the same system. Literature data, community databases, and pretraining sets built by others are excluded.
- **R8, Structure search (Axis 4):** if an inverse solver demonstrably searches over model structures using own data, add log₁₀ of the number of candidate structures, and report both terms.
- **R9, Uncertainty of inferred scores:** inferred and theoretical scores carry ±0.3 on linear axes and ±0.5 on Axis 4, and are not used as the sole anchor for a decimal comparison.

## Rules with no worked example among the anchors
R5 and R8 are applied from the rule text alone. When either one determines a score, say so in the rationale.
