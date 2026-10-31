# Spike sorting project — context for Claude Code

This is my final project for 02-120 Programming for Scientists (CMU, Fall 2026). I work on it alone, with you as collaborator. The course grades whether I *learn* the science and the computation, not just whether the code works. Read the "How to work with me" section before doing anything.

## The project in one paragraph

I simulate extracellular brain recordings where the true spike times are known, then sort them with a spike sorter I write myself, to measure how many neurons a single electrode can reliably tell apart. The final product is an interactive web app.

**Scientific question:** How many distinct neurons can be reliably separated from a single electrode's signal, and how do noise level, waveform similarity and firing rate limit that number?

**Inspiring paper:** Quian Quiroga, Nadasdy & Ben-Shaul (2004), *Unsupervised spike detection and sorting with wavelets and superparamagnetic clustering*, Neural Computation (PDF in `papers/`).
**Related:** Pedreira et al. (2012), *How many neurons can we see with current spike sorting algorithms?*; Trautmann et al. (2019), sorting vs. unsorted threshold crossings (optional extension).
**Data:** none — everything is simulated, so ground truth is exact.

## Pipeline

1. **Simulator**
   - Spike trains: Poisson firing with a refractory period (~2 ms).
   - Waveforms: one Hodgkin–Huxley action potential (my own ODE integrator, e.g. RK4), converted to an extracellular waveform (tracks membrane current, not voltage), scaled by each neuron's distance from the electrode.
   - Recording: waveforms placed at spike times, summed, plus background noise (aim for realistic background from many distant neurons, not only white noise).
   - Output: voltage trace + answer key of true spike times and identities.
2. **Sorter (all core steps written by me, from scratch)**
   - Bandpass filter, zero-phase; band is a parameter, default 300–6000 Hz (matches the paper).
   - Negative-only threshold detection: x < −4σ, with robust noise estimate σ = median(|x|) / 0.6745, plus a dead time after each detection.
   - Align detected spikes on their trough.
   - Multilevel Haar wavelet transform; select coefficients by deviation from normality (KS test).
   - PCA features as a baseline for comparison.
   - Gaussian mixture model fitted by EM; number of neurons chosen by BIC (lowest BIC wins).
   - Scoring: match sorted spikes to true spikes within a fixed time window.
3. **Web app:** sliders for number of neurons, noise, waveform similarity, firing rate; panels for raw trace with sorted spikes, feature space, cluster waveforms, accuracy vs. ground truth; a sweep view of neurons recovered vs. neurons present.

## Differences from Quiroga et al. (2004)

Full write-up (paper vs. us, why, what it changes) lives in the README. Don't drift back to the paper's method on these:

1. **Filter band:** default 300–6000 Hz like the paper, but exposed as a parameter. f_rms (and so Rice's prediction) depends on the band.
2. **Polarity:** paper detects positive peaks; HH extracellular spikes are negative first, so we use a negative-only threshold (one-sided, mirror of the paper).
3. **Clustering:** GMM + EM with BIC instead of superparamagnetic clustering. GMM shares K-means' preference for compact Gaussian clusters, so compare against the paper's K-means result; a narrow wavelet advantage is a finding, not a bug.
4. **Waveforms:** HH-derived instead of real recorded shapes (check spike width ~1 ms; apply temperature correction if too slow). Shape variety via a small precomputed library of HH parameter sets plus distance-dependent smoothing (planned Week 5; Week 4 uses amplitude-only differences). Background noise from many distant neurons' spikes, like the paper.

## Other decisions

- **Libraries only for plumbing** (arrays, plotting, possibly the filter design). The course rejects "one library call fed into the next." Detection, Haar transform, coefficient selection, EM, BIC and scoring are mine.
- **Detection false-positive checks (one-sided, corrected Oct 30).** 1 − Φ(4) ≈ 3.2 × 10⁻⁵ is a *per-sample* probability. After filtering, neighboring samples are correlated, so one noise bump spans several samples but counts as one detection. Therefore:
  - Fraction of noise *samples* below −4σ should match 3.2 × 10⁻⁵ (white or filtered, with σ measured after filtering).
  - Detections per sample should match 3.2 × 10⁻⁵ only on **white** noise.
  - On **filtered** noise, detections per second should match Rice's formula for one-sided crossings: ≈ f_rms × exp(−u²/2) at u = 4, with f_rms computed from my filter's actual frequency response (ideal 300–6000 Hz band: f_rms ≈ 3.6 kHz → ≈ 1.2 false detections/s). Approximate because the signal is sampled.
- **Possible GMM stress test:** a bursting neuron (shrinking amplitude stretches its cluster) to see whether GMM wrongly splits it.

## Checks the project must pass

- Ground truth scoring: detection rate, false positives, assignment accuracy.
- Detection-rate checks above (one-sided exceedance fraction, white-noise detections, Rice's formula on filtered noise).
- Spike width of the HH-derived extracellular waveform is close to ~1 ms.
- Robust σ recovers true σ on pure noise and stays accurate as firing rate rises, while plain std overestimates.
- Two very different neurons, no noise → perfect sorting.
- Haar transform inverts exactly; hand-computed 8-sample example matches code.
- EM recovers known parameters of a synthetic Gaussian mixture; log-likelihood rises every iteration.
- Published behavior: wavelets match or beat PCA as sorting gets harder, compared against the paper's K-means result (Quiroga 2004); neurons recovered level off as more are added (Pedreira 2012).
- Refractory violations (<2 ms intervals) near zero for correct units, high for merged ones.
- With a fixed random seed, the app reproduces offline script results.

## Roadmap and course deadlines

Full week-by-week plan with action items: see `ROADMAP.md`.

| Week | Dates | Phase | Course deadline |
| --- | --- | --- | --- |
| 1 | Oct 8–14 | Simulate one neuron (HH, waveform, spike trains) | Proposal feedback Oct 9 |
| 2 | Oct 15–21 | Full recording, filtering, detection | Journal checkpoint 1 — Oct 21 |
| 3 | Oct 22–30 | Alignment, Haar features, PCA baseline | Journal checkpoint 2 — Oct 30 |
| 4 | Oct 31–Nov 6 | EM-GMM, BIC, scoring, first end-to-end sort | TA check-ins open Nov 4 |
| 5 | Nov 7–13 | Parameter sweeps; answer the question | TA check-in by Nov 13 |
| 6 | Nov 14–20 | Web app v1, deployed; README draft | App live + checkpoint 3 — Nov 20 |
| 7 | Nov 21–27 | Fixes; optional sorted-vs-unsorted extension | Thanksgiving Break |
| 8 | Nov 28–Dec 1 | README, ≤5-min video, demo prep | Final app/code/video + demo day — Dec 1 |
| — | Dec 3 | — | Closed, on-paper project assessment |

**Current status:** _(update me)_

## How to work with me

My session logs are graded as a build journal. The graders look for learning, steady work, and checking — so:

- **Teach before building.** When we start a new concept (filtering, wavelets, EM, Rice's formula…), explain it first, then quiz me and let me explain it back before writing code.
- **Explain code you write.** After writing anything non-trivial, walk me through what it does and why. Expect me to ask "why?" often.
- **Debug with me, don't just fix.** When something breaks, help me form hypotheses and test them rather than silently patching it.
- **Always tie work to a check.** New code should come with a test or a comparison against one of the checks above.
- **Keep scope small.** Get the smallest version working and checked before adding features.
- **Don't write my commit messages** — remind me to write them in my own words.
- **Flag deviations.** If something we do departs from the paper or this file, say so and suggest recording it (README or here).
- **Prepare me for Dec 3.** I must be able to explain, without notes: the extracellular spike shape and distance scaling; HH variables and my integrator; why 300–6000 Hz and what changing the band does; where 0.6745 comes from; why a negative-only threshold; the one-sided 3.2 × 10⁻⁵ derivation, why filtered noise gives fewer detections, and Rice's prediction; each of the four differences from Quiroga et al. and what it costs; a Haar transform by hand; why non-Gaussian coefficients are chosen; EM steps, monotone likelihood, and what BIC trades off; scoring and refractory violations; my answer with its numbers; and what the simulation leaves out.
