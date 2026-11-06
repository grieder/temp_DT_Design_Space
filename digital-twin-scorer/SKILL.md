---
name: digital-twin-scorer
description: Scores a research paper on the six-axis digital twin design rubric (coupling, forward-model fidelity, cost side, model dimensionality, VVUQ maturity, autonomy) from Grieder & Qian's "What Makes a Digital Twin?", and places the system on the landscape map against 17 calibrated anchor systems. Use this skill whenever someone uploads or names a paper or manuscript about a digital twin, digital shadow, self-driving or autonomous lab, closed-loop or active-learning experiment, theory–experiment coupling, or surrogate model in chemistry, materials science, or quantum information science and wants it scored, rated, classified, compared, placed on the map, or checked against the rubric — even if they don't say "rubric" or "digital twin," e.g. "where does my system sit?", "is this really a digital twin?", or "score my paper for the landscape website."
---

# Digital Twin Scorer

Score one paper on the six rubric axes, with evidence for every score, and produce a score file that can be plotted and submitted to the community landscape.

## What to read
- `references/rubric.md` (current version online: https://github.com/grieder/temp_DT_Design_Space/blob/main/digital-twin-scorer/references/rubric.md): the axes, anchor levels, basis codes, and decision rules R1–R9. **Always read it in full before scoring.**
- `references/anchors_rationales.md`: 17 human-reviewed anchor systems, each with six scores and rationales. Use it to calibrate: for every axis, find the anchors closest to the paper and score relative to them.
- `assets/anchors.json`: the same scores in machine-readable form (used by the scripts).

## Workflow

### 1. Get the inputs
Ask for the main paper, and the supporting information if there is one. Several anchor scores depended on SI tables (parameter counts, validation data), so missing SI is a common source of error. Score the paper as a whole, even when it describes several systems or variants: score the system the paper is about, as demonstrated.

### 2. Read for evidence, axis by axis
For each axis, find the passages that decide the score and note their location (section, figure, table, or page). What to look for:
- **Coupling (1):** what is the physical counterpart, and is it one live instance? Does data flow automatically, in which directions, and does a person transfer anything between the sides? Was the "experiment" real, archival, or simulated?
- **Fidelity (2):** what computes the forward prediction: first-principles physics, a reduced physical model, or a data-driven approximator?
- **Cost side (3):** per iteration (or per use), which takes longer or costs more, the model evaluation or the physical measurement?
- **Model dimensionality (4):** which parameters are fitted or fine-tuned to data from this campaign (measured or computed), and how many? Count from the architecture when possible.
- **VVUQ (5):** is the model validated against data it was not fitted to? Is predictive uncertainty quantified, propagated, or checked for calibration? Is there a credibility assessment?
- **Autonomy (6):** who decides the next step and who interprets results, over how many iterations?

### 3. Apply the decision rules
Check every rule in `references/rubric.md` against the paper before assigning scores. The rules most often missed:
- **R3, demonstrated not designed:** score what the paper actually ran. A loop shown only against simulated data is not a live loop, however it is designed.
- **R1 and R2, coupling caps:** a person transferring data on the decision timescale, or a loop over a sequence of new samples, caps coupling at 1.5.
- **R4, no virtual model:** a heuristic or LLM planner without a predictive model of the system scores 0 on Axes 1, 2 and 4. Say clearly that this makes it an autonomous lab, not a digital twin.
- **R7, own data:** pretrained weights and literature fits don't count on Axis 4; computed data generated in the authors' own campaign does.

### 4. Score against the anchors
For each axis, name the one or two anchors nearest to the paper and explain whether it sits above, below, or level with them. Assign the score to one decimal place, with a basis code:
- **E:** the paper states it.
- **I:** inferred from the technique.
- **T:** Axis 3 only, theoretical experiment cost.
- **U:** supplied by the user.

### 5. Ask about missing evidence
If any axis can't be scored from the paper, ask the user, in **one** message listing every question with the reason it matters. A typical example: "How many parameters are fitted in the surrogate? The paper gives the architecture but not the input size." Users are often the authors and can answer directly.
- Mark scores built on an answer as basis **U**, and quote the answer in the rationale.
- If the user can't answer, or nobody is available (e.g. an automated run), fall back to an **I** score, and list the unanswered question in the score file's `questions` field.

### 6. Report
Give the user, in this order:
1. A short table: axis, score, basis, one-sentence reason, nearest anchors.
2. Any judgment calls a reviewer might dispute, and which rule decided them.
3. If R4 applies, state that the system is an autonomous laboratory rather than a digital twin.
4. The score file (below), saved as `<short-name>_scores.json`. Run `python scripts/validate_score.py <file> --check-doi` on it (the flag confirms at doi.org that the DOI is registered; offline, it only warns) and fix any errors before sharing.
5. Optionally, a map placing the system among the anchors:
   `python scripts/plot_landscape.py --include-reference --new <file> --out <short-name>_map`

Then tell the user how to share it: load the score file on the landscape website, and use **Submit for review**. Submissions are listed as pending until maintainers verify them against the paper.

## Score file format
```json
{
  "name": "Short system name",
  "ref": "First author et al., Journal Year",
  "doi": "10.xxxx/...",
  "rubric_version": "0.9",
  "skill_version": "1.0",
  "no_virtual_model": false,
  "scores": {"1": 1.0, "2": 1.5, "3": 0.8, "4": 2.3, "5": 2.0, "6": 1.0},
  "evidence": {
    "1": {"basis": "E", "location": "Sec. 2.3, Fig. 1",
          "rationale": "One-sentence reason, citing the deciding fact.",
          "rules": ["R3"], "nearest_anchors": ["DTCS", "C³"]}
  },
  "questions": []
}
```
- `doi` is required. Take it from the paper's first page or reference line and write it bare (`10.1038/s41586-023-06734-w`, not a URL). For an arXiv preprint use `10.48550/arXiv.<id>`. If the paper shows no DOI, ask the user for it in step 5; never guess or invent one.
- Every axis needs an `evidence` entry with the same fields.
- Set `rubric_version` from `assets/anchors.json`.
- `questions` lists anything left unanswered.

## Calibration notes
- **Don't round toward the anchors' integers.** Systems at the same level differ; use the decimals.
- **Axis 3 is about running cost only.** Library generation and model training are one-time costs and are not scored.
- **VVUQ 3 or above is rare:** among the anchors, only VDMN reaches it. Require both validation and propagated or calibrated uncertainty before scoring 3.
- **High coupling is rare too:** only Bayesian Conavigation reaches 2.0. A tight, fully automated loop around a data-only model scores high on Axis 1 but low on Axis 2 (see Liu 2022); report that combination plainly.
- **Self-assessments:** when the user is an author, score what the paper shows, not what the user says the system can do. Explain any gap kindly, citing R3.
