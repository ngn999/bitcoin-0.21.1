Building Bitcoin
================

See doc/build-*.md for instructions on building the various
elements of the Bitcoin Core reference implementation of Bitcoin.

## Build
```bash
CFLAGS="-g -O0" CXXFLAGS="-g -O0" ./configure --disable-tests --disable-gui-test --disable-bench --disable--ccache --disable-zmq --disable-man --disable-largefile
make -j8
```


