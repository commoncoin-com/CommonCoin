# CommonCoin Snap Packaging

Commands for building and uploading a CommonCoin Core Snap to the Snap Store. Anyone on amd64 (x86_64), arm64 (aarch64), or i386 (i686) should be able to build it themselves with these instructions. This would pull the official CommonCoin binaries from the releases page, verify them, and install them on a user's machine.

## Building Locally
```
sudo apt install snapd
sudo snap install --classic snapcraft
sudo snapcraft
```

### Installing Locally
```
snap install \*.snap --devmode
```

### To Upload to the Snap Store
```
snapcraft login
snapcraft register commoncoin-core
snapcraft upload \*.snap
sudo snap install commoncoin-core
```

### Usage
```
commoncoin-unofficial.cli # for commoncoin-cli
commoncoin-unofficial.d # for commoncoind
commoncoin-unofficial.qt # for commoncoin-qt
commoncoin-unofficial.test # for test_commoncoin
commoncoin-unofficial.tx # for commoncoin-tx
```

### Uninstalling
```
sudo snap remove commoncoin-unofficial
```