## Differences from Quiroga et al. (2004)

This project starts from Quian Quiroga, Nadasdy & Ben-Shaul (2004) but departs from it in four places. Each is listed with what the paper did, what this project does, why, and what it changes when comparing results.

### 1. Filter band

- **Paper:** bandpass 300–6000 Hz.
- **This project:** 300–6000 Hz by default, matching the paper, with the band exposed as a parameter.
- **Why:** matching the paper keeps detection results comparable. Making the band adjustable lets the app show the trade-off directly: a narrower band admits less noise but removes the sharp, fast features that help tell similar neurons apart.
- **What it changes:** the false-detection prediction depends on the band. Rice's formula uses the RMS frequency f_rms of the filtered noise, which is computed from the actual filter's frequency response. For an ideal 300–6000 Hz band, f_rms ≈ 3.6 kHz; for 300–3000 Hz, f_rms ≈ 1.8 kHz. The sampling rate must sit well above twice the upper cutoff.

### 2. Spike polarity

- **Paper:** detects positive peaks only.
- **This project:** detects negative peaks only, with threshold x < −4σ, where σ = median(|x|) / 0.6745.
- **Why:** extracellular spikes derived from a Hodgkin–Huxley action potential are negative first. A negative-only threshold is the exact mirror of the paper's one-sided detection, keeps false positives low, and lets spikes align on their trough.
- **What it changes:** because only one tail counts, the expected false-positive numbers are one-sided:
  - per-sample probability of a noise sample below −4σ: 1 − Φ(4) ≈ 3.2 × 10⁻⁵;
  - false detections per second on filtered noise (Rice's formula): ≈ f_rms × exp(−8), about 1.2 per second for an ideal 300–6000 Hz band.

### 3. Clustering method

- **Paper:** superparamagnetic clustering (SPC), a method from statistical physics that does not assume Gaussian clusters and chooses the number of clusters itself.
- **This project:** a Gaussian mixture model fitted by expectation–maximization (EM), with the number of neurons chosen by BIC.
- **Why:** EM can be checked rigorously (the likelihood must never decrease, and it recovers known parameters on synthetic mixtures), can be written and explained from scratch within one semester, and runs fast enough for an interactive web app.
- **What it changes:** like K-means, a GMM favors compact, roughly Gaussian clusters. The paper found a smaller wavelet advantage when clustering with K-means than with SPC, so the right published reference for this project is the paper's K-means comparison. If wavelet features beat PCA by only a narrow margin here, that is an expected consequence of the clustering method, not a bug.

### 4. Spike waveforms and noise

- **Paper:** spike shapes taken from real recordings; background noise built from spikes.
- **This project:** spike shapes derived from a Hodgkin–Huxley simulation; background noise built from the summed spikes of many distant neurons, following the paper's approach.
- **Why:** simulating the waveform from biophysics makes every step of the recording model explainable and adjustable, with no external data.
- **What it changes:**
  - Hodgkin–Huxley's original parameters come from the squid giant axon and produce slower spikes than typical mammalian cortical spikes (about 1 ms). Spike width is measured, and a temperature correction to the rate constants is applied if needed. Width also determines how much of each spike survives the filter band.
  - Neurons that share one waveform scaled by distance differ only in amplitude. To vary shape, waveforms come from a small precomputed library built from several Hodgkin–Huxley parameter sets, with distance-dependent smoothing (far neurons lose their sharpest features).
  - Results describe sorting performance on these simulated waveforms; real spike shapes may be more or less separable.
