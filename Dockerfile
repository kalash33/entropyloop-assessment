FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git ca-certificates python3 python3-numpy \
    libbz2-dev libdivsufsort-dev libjsoncpp-dev libssl-dev libmpfr-dev libgmp-dev && \
    git clone --depth 1 https://github.com/usnistgov/SP800-90B_EntropyAssessment /opt/ea && \
    cd /opt/ea/cpp && make non_iid iid restart && rm -rf /var/lib/apt/lists/*
WORKDIR /work
