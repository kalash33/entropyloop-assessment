# How to run (Mac, with Docker Desktop)

1. Download the raw capture (about 16 GB) and check it:
   curl -L -o samples.bin https://files.picoweather.net/samples.bin
   shasum -a 256 samples.bin
   # must equal 756f829929a7d1047d22026fa66d91c432b30987f1cf35a5598b7174e85fbcdf
   (Short on disk or time? Take the first 200 MB instead:
    curl -L -r 0-199999999 -o samples.bin https://files.picoweather.net/samples.bin
    and note in the README that you used a slice, so the checksum will not match.)

2. Build the tool image (one time, about 3 minutes):
   docker build -t ea90b .

3. Extract four 1,000,000-sample windows spread across the file and run 90B:
   docker run --rm -v "$PWD":/work ea90b bash -c '
     mkdir -p data
     for off in 0 2000000000 4000000000 6000000000; do
       python3 scripts/extract.py samples.bin data/w$off --offset $off --count 1000000
       scripts/run_90b.sh /opt/ea/cpp data/w$off
       mkdir -p results/w$off && mv results/*.txt results/w$off/ 2>/dev/null || true
     done'
   (With a 200 MB slice, use offsets 0 20000000 40000000 60000000 instead.)

4. Summarise: python3 scripts/summarise.py results > results/SUMMARY.md
   Then send me results/SUMMARY.md and I will help write the note.
