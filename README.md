# EntropyLoop: an independent SP 800-90B entropy assessment

Status: work in progress (Nov 2026). Author: Kalash Poddar (90259149+kalash33@users.noreply.github.com).

[EntropyLoop](https://github.com/QuantumVillage/EntropyLoop) is Quantum Village's open-source, low-cost phase-diffusion quantum random number generator. Its README reports `ent` and NIST STS results. Those suites test the output after hashing, and hashed output passes them whether or not the physical source is healthy. This repository assesses the **raw source** instead, using NIST's [SP 800-90B tool](https://github.com/usnistgov/SP800-90B_EntropyAssessment). The goal is to make EntropyLoop's randomness easy for anyone to verify, not to criticise the device.

## Data
- Raw ADC capture published by [@ljn0099](https://github.com/ljn0099) in [EntropyLoop issue #3](https://github.com/QuantumVillage/EntropyLoop/issues/3), made with [treeQuantumSampler11](https://github.com/ljn0099/treeQuantumSampler11).
- Format: 8,053,141,120 samples at 500 kS/s, little-endian uint16 holding 12-bit values.
- SHA-256: `756f829929a7d1047d22026fa66d91c432b30987f1cf35a5598b7174e85fbcdf`.
- Thanks to ljn0099 for publishing it.

## Method
1. Verify the checksum.
2. Take 1,000,000-sample windows at several offsets across the capture (`scripts/extract.py`).
3. Map each 12-bit sample to 90B symbols three ways: the low 8 bits, the 8 most significant bits, and the top 4 bits.
4. Run `ea_non_iid` and `ea_iid` (`scripts/run_90b.sh`), then the restart test on 1,000 x 1,000 restart data when a device is available.

## Results
(to be filled: min-entropy per symbol for each mapping and window, IID test outcome, stability across windows)

## Limits (read first)
- One capture, from one device, made by a third party. It says nothing general about the EntropyLoop design or about other builds.
- 90B gives a conservative lower bound on min-entropy for this source and setup. It does not prove that the entropy is quantum. Separating quantum from classical noise needs controlled experiments (see the next steps).
- No restart data yet. The restart test needs repeated power cycles on a device.

## Next steps
- Startup and continuous health tests (Repetition Count and Adaptive Proportion, SP 800-90B section 4.4) in the firmware.
- Controlled runs (laser off, temperature, dual-path vs single-path) to estimate how much of the measured entropy comes from the quantum process.

## Reproduce
```
git clone https://github.com/usnistgov/SP800-90B_EntropyAssessment && cd SP800-90B_EntropyAssessment/cpp && make non_iid iid restart
python3 scripts/extract.py samples.bin data/w0 --offset 0 --count 1000000
scripts/run_90b.sh /path/to/SP800-90B_EntropyAssessment/cpp data/w0
```

License: MIT.
