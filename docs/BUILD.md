# Building CommonCoin (COM)

This guide provides instructions for compiling the CommonCoin Core daemon, CLI, and GUI wallet on Unix-like operating systems (Linux and macOS) and Windows.

---

## 1. Prerequisites (Ubuntu/Debian)

Install the required compile tools and system dependencies:

```bash
sudo apt-get update
sudo apt-get install -y build-essential libtool autotools-dev autoconf pkg-config \
                       libssl-dev libevent-dev bsdmainutils git curl
```

### Boost C++ Libraries
CommonCoin requires Boost versions >= 1.58:

```bash
sudo apt-get install -y libboost-system-dev libboost-filesystem-dev \
                       libboost-chrono-dev libboost-program-options-dev \
                       libboost-test-dev libboost-thread-dev
```

### Berkeley DB (BDB 5.3.28) — Strict Requirement
To ensure backward wallet file compatibility, Berkeley DB version 5.3.28 is **strictly required**.

Compile BDB 5.3.28 from source:

```bash
mkdir -p /tmp/bdb-build && cd /tmp/bdb-build
curl -sL https://download.oracle.com/berkeley-db/db-5.3.28.NC.tar.gz -o db-5.3.28.NC.tar.gz
tar -xzf db-5.3.28.NC.tar.gz
cd db-5.3.28.NC

# Apply C++11 patches for modern compilers
sed -i 's/atomic_init/atomic_init_db/g' src/dbinc/atomic.h src/mp/mp_fget.c src/mp/mp_mvcc.c src/mp/mp_region.c src/mutex/mut_method.c src/mutex/mut_tas.c
sed -i 's/__atomic_compare_exchange/__atomic_compare_exchange_db/g' src/dbinc/atomic.h

# Replace ancient config.guess and config.sub for modern architectures compatibility
curl -sL "https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=4550d2f15b3a7ce2451c1f29500b9339430c877f" -o dist/config.guess
curl -sL "https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=4550d2f15b3a7ce2451c1f29500b9339430c877f" -o dist/config.sub

cd build_unix
../dist/configure --enable-cxx --disable-shared --disable-replication --with-pic --prefix=/usr/local/bdb53
make -j$(nproc)
sudo make install
sudo ldconfig
```

### Optional Dependencies

* **UPnP (Port Mapping)**: `libminiupnpc-dev`
* **ZeroMQ (Pub/Sub notifications)**: `libzmq3-dev`
* **Qt5 GUI Wallet**: `qtbase5-dev qttools5-dev-tools`

---

## 2. Compile CommonCoin Core (Linux)

Navigate to the `blockchain/` directory in the repository:

```bash
cd blockchain/
```

### Generate Build Scripts
Run autotools to prepare the build system:

```bash
./autogen.sh
```

### Configure the Build
Configure the compiler pointing to our custom Berkeley DB 5.3 location:

**For headless node (daemons only):**
```bash
./configure LDFLAGS="-L/usr/local/bdb53/lib/" CPPFLAGS="-I/usr/local/bdb53/include/" \
            --without-gui --enable-hardening --prefix=/usr/local
```

**For desktop GUI wallet (requires Qt5):**
```bash
./configure LDFLAGS="-L/usr/local/bdb53/lib/" CPPFLAGS="-I/usr/local/bdb53/include/" \
            --enable-hardening --prefix=/usr/local
```

### Compile & Install
Compile the codebase and install to system bin folders:

```bash
make -j$(nproc)
sudo make install
```

Verify the binaries are successfully installed:
```bash
commoncoind --version
commoncoin-cli --version
```

---

## 3. macOS Build Instructions

Use Homebrew to install the build toolchain:

```bash
brew update
brew install autoconf automake libtool pkg-config boost openssl libevent berkeley-db
```

Configure and compile:
```bash
./autogen.sh
./configure LDFLAGS="-L/opt/homebrew/opt/berkeley-db/lib" CPPFLAGS="-I/opt/homebrew/opt/berkeley-db/include"
make -j$(sysctl -n hw.ncpu)
```

---

## 4. Windows Cross-Compilation (from Ubuntu)

Install MinGW-w64:
```bash
sudo apt-get install -y g++-mingw-w64-x86-64 mingw-w64-x86-64-dev
```

Build the dependencies using the built-in system in `depends/`:
```bash
cd depends
make HOST=x86_64-w64-mingw32 -j$(nproc)
cd ..
./autogen.sh
./configure --prefix=`pwd`/depends/x86_64-w64-mingw32 --enable-hardening
make -j$(nproc)
```
The resulting executable binaries will be located under `src/commoncoind.exe` and `src/qt/commoncoin-qt.exe`.
