# Roadmap

Re-planned Nov 10, 2026. Work started Oct 30, about three weeks after the original Week 1, so the original eight weeks are compressed into the time left. **All original scope is kept**; only dates and one ordering change (below). Assumes a working session every day.

## Schedule

| Date | Work | Done when | Course deadline |
| --- | --- | --- | --- |
| Nov 10 | Finish RK4 integrator; extracellular waveform (1/r vs 1/r², temperature correction) | All 18 HH tests pass; extracellular spike width ~1 ms | |
| Nov 11 | Poisson spike trains with 2 ms refractory period; full recording with background from many distant neurons | Trace + answer key of true spike times and identities | |
| Nov 12 | Bandpass filter (zero-phase, default 300–6000 Hz); negative-only 4σ detection with dead time; bare app page deployed | One-sided exceedance fraction, white-noise detections and Rice's formula checks pass; robust σ check passes | |
| Nov 13 | TA check-in: simulator + detection with checks, and this plan | | **TA check-in** |
| Nov 14–15 | Trough alignment; multilevel Haar transform; KS coefficient selection; PCA baseline | Haar inverts exactly; hand-computed 8-sample example matches | |
| Nov 16–17 | EM-GMM; BIC model selection; scoring against ground truth | EM recovers a synthetic mixture with rising log-likelihood; two very different neurons with no noise sort perfectly | |
| Nov 18–20 | Web app v1: sliders, raw trace with sorted spikes, feature space, cluster waveforms, accuracy; README draft | App live; fixed seed reproduces offline results | **App live + checkpoint 3, Nov 20** |
| Nov 21–24 | Parameter sweeps and sweep view; answer the question; waveform library (several HH parameter sets + distance-dependent smoothing) | Wavelets vs PCA compared with the paper's K-means result; recovered-vs-present curve; refractory-violation check | |
| Nov 25–27 | Trautmann extension (sorted vs unsorted threshold crossings); fixes | | Thanksgiving Break |
| Nov 28–Dec 1 | README, ≤5-min video, demo prep | | **Final app/code/video + demo day, Dec 1** |
| Dec 3 | | | Closed, on-paper assessment |

## Changes from the original plan

- **Dates compressed** (see above).
- **Ordering:** parameter sweeps move from before the app (original Week 5) to after app v1, because the Nov 20 app deadline is fixed and needs a working sort first. App v1 shows sorting; the sweep view is added Nov 21–24.

## Re-planning rule

If any row runs more than two days over, stop and re-plan dates. Scope is not cut.
