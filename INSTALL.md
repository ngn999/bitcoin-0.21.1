Building Bitcoin
================

See doc/build-*.md for instructions on building the various
elements of the Bitcoin Core reference implementation of Bitcoin.

## Build
```bash
CFLAGS="-g -O0" CXXFLAGS="-g -O0" ./configure --disable-tests --disable-gui-test --disable-bench --disable--ccache --disable-zmq --disable-man --disable-largefile --with-boost=/opt/homebrew/
make -j8
```
`-O0` 比 `-Og` 要好，能解决在 debug 时，部分变量打印出不出来的问题;同时 `-O0` 很多函数不会内联，方便调试。
