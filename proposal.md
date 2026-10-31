# 02-120 Project Proposal

Tara Prahlad

## 1. What is your scientific question?

How many distinct neurons can be reliably separated from a single electrode's signal, and how do waveform similarity, noise level and firing rate limit that number?

## 2. What will you build to answer it?

I want to build an interactive web app that will let me do two things:

a. **Simulate the firings of a neuron:** I want to make a recording simulator that will generate fake electrode data that looks like what a real electrode in the brain would record, except I would know which neuron caused each spike.

b. **Sort the spikes from each neuron:** I want to learn signal processing from this project so I'm thinking tentatively that it will include the following:

   1. Bandpass filtering
   2. Threshold detection with a robust noise estimate
   3. Peak alignment
   4. Haar wavelet features chosen by how non-Gaussian they are
   5. A Gaussian mixture model fitted by expectation-maximization

I'm thinking users can move sliders to adjust the noise level, number of neurons, waveform similarity and firing rate. The app will show the raw trace with sorted spikes colored, the feature space, each cluster's waveforms and accuracy against ground truth. A sweep view will plot how many neurons are recovered (after firing) as more added.

## 3. How will you check your model?

I will check my model with the following methods:

a. **Ground truth scoring:** detected spike will be matched to a true spike within a small time window.

b. **A detection rate that can be derived by hand:** the chance that one sample exceeds 4 standard deviations in either direction is 2(1 − Φ(4)) ≈ 6.3 × 10⁻⁵ and the detector must match this on simulated noise.

c. **The robust noise estimate:** on pure noise, median(|x|) / 0.6745 must recover the true σ.

d. **A hand-solvable special case:** two neurons with very different waveforms and no noise need to be sorted properly.

e. **Component checks:** the Haar transform needs to invert exactly and EM must recover the known parameters of a synthetic Gaussian mixture.

f. **Published behavior:** wavelets need to match or beat PCA as sorting gets harder.

g. **Refractory violations:** correctly sorted units should almost never fire twice within 2 ms but merged units will.

If you have any questions, feel free to refer to this research paper: <https://pubmed.ncbi.nlm.nih.gov/15228749/>
