# EntropyLoop: an independent SP 800-90B entropy assessment

Version 1 (Nov 2026). Author: Kalash Poddar (90259149+kalash33@users.noreply.github.com).

[EntropyLoop](https://github.com/QuantumVillage/EntropyLoop) is Quantum Village's open-source, low-cost phase-diffusion quantum random number generator. Its README reports `ent` and NIST STS results. Those suites test the output after hashing, and hashed output passes them whether or not the physical source is healthy. This repository assesses the **raw source** instead, using NIST's [SP 800-90B tool](https://github.com/usnistgov/SP800-90B_EntropyAssessment). The goal is to make EntropyLoop's randomness easy for anyone to verify, not to criticise the device.

## Limits (read first)
- One capture, from one device, made by a third party. It says nothing general about the EntropyLoop design or about other builds.
- 90B gives a conservative lower bound on min-entropy for this source and setup. It does not prove that the entropy is quantum. Separating quantum from classical noise needs controlled experiments (see the next steps).
- Only five 1,000,000-sample windows were assessed, not the whole capture.
- No restart data yet. The restart test needs repeated power cycles on a device.

## Data
- Raw ADC capture published by [@ljn0099](https://github.com/ljn0099) in [EntropyLoop issue #3](https://github.com/QuantumVillage/EntropyLoop/issues/3), made with [treeQuantumSampler11](https://github.com/ljn0099/treeQuantumSampler11). Thanks to ljn0099 for publishing it.
- Format: 8,053,141,120 samples at 500 kS/s, little-endian uint16 holding 12-bit values.
- Published SHA-256 of the full file: `756f829929a7d1047d22026fa66d91c432b30987f1cf35a5598b7174e85fbcdf`. This run did not download the full file, so it did not recompute that hash. It confirmed the file size (16,106,282,240 bytes, which matches the stated sample count) and recorded a SHA-256 for every window it used ([`results/windows.txt`](results/windows.txt)).

## Method
1. Fetch five 1,000,000-sample windows by HTTP range request, at sample offsets 0, 2e9, 4e9, 6e9 and 8e9, spread across the capture.
2. Map each 12-bit sample to 90B symbols three ways: the low 8 bits, the 8 most significant bits (`q8`), and the top 4 bits (`high4`) (`scripts/extract.py`).
3. Run `ea_non_iid` on every window and mapping, and `ea_iid` on the first window (`low8` and `q8`), with the NIST tool built from source.
4. Everything runs in GitHub Actions ([`.github/workflows/assess.yml`](.github/workflows/assess.yml)), so the log, the tool commit ([`results/nist_tool_commit.txt`](results/nist_tool_commit.txt)) and the window checksums are public.

## Results
Full table: [`results/SUMMARY.md`](results/SUMMARY.md).

| mapping | bits per symbol | min-entropy per symbol (range over 5 windows) |
|---|---|---|
| low 8 bits | 8 | 6.05 to 6.23 |
| top 8 bits (`q8`) | 8 | 2.72 to 2.81 |
| top 4 bits (`high4`) | 4 | about 0.40 |

- **Stable:** estimates barely move across five windows spread over about 4.5 hours of capture, so there is no sign of drift in this recording.
- **Where the entropy is:** the signal occupies a narrow band of the ADC range (first window: values 1,587 to 2,484, standard deviation about 78, 759 distinct values out of 4,096). So the high bits mostly track the signal level, and most of the entropy sits in the low-order bits, as expected for this kind of source.
- **IID test:** failed on the first window for `low8` and `q8` (chi-square and permutation tests), so the non-IID estimates are the ones to use. That is the expected outcome for a physical source with some structure.
- These are lower bounds for this capture only (see Limits).

## Health tests
SP 800-90B start-up and continuous health tests (Repetition Count and Adaptive Proportion) were written for the EntropyLoop firmware and replayed on the same five windows ([`results/health_replay.txt`](results/health_replay.txt)). No false alarms at a claimed 4 or 6 bits per sample. The longest repeat was 3 and the highest APT count 12, against cutoffs of 8 and 35 at 6 bits. This shows the tests do not misfire on healthy data; it does not show what they catch on a faulty device.

## Next steps
- Controlled runs (laser off, temperature, dual-path vs single-path) to estimate how much of the measured entropy comes from the quantum process.
- A restart test on a physical device.

## Reproduce
Re-run the workflow from the Actions tab, or locally:
```
git clone https://github.com/usnistgov/SP800-90B_EntropyAssessment && cd SP800-90B_EntropyAssessment/cpp && make non_iid iid
curl -L -r 0-1999999 -o w0.bin https://files.picoweather.net/samples.bin
python3 scripts/extract.py w0.bin data/w0 --count 1000000
scripts/run_90b.sh /path/to/SP800-90B_EntropyAssessment/cpp data/w0
```
A Dockerfile and [`RUN.md`](RUN.md) are included for a full local run.

License: MIT.
