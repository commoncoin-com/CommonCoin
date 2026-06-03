# Walkthrough - CommonCoin (COM) Code Modifications

This walkthrough summarizes all structural setup and source code modifications completed so far for the **CommonCoin (COM)** independent blockchain fork.

---

## 1. Project Repository and Management Docs

We initialized the repository and created the project management files to track the milestones.

### Created Files
* **[README.md](file:///E:/commoncoin/README.md)**: Main project information and coin specs (Block time: 1 min, reward: 100k COM, ports: 33555/33556, prefix: 'C').
* **[TASKS.md](file:///E:/commoncoin/TASKS.md)**: Tracking checklist for phases 1-17.
* **[ROADMAP.md](file:///E:/commoncoin/ROADMAP.md)**: Milestones for development, infrastructure, testing, and launch.
* **[CHANGELOG.md](file:///E:/commoncoin/CHANGELOG.md)**: Historical tracking of project modifications.
* **[RELEASE_NOTES.md](file:///E:/commoncoin/RELEASE_NOTES.md)**: Details for version `1.0.0-beta`.
* **[docs/analysis_report.md](file:///E:/commoncoin/docs/analysis_report.md)**: Consensus, dependencies, and fork strategy.

---

## 2. Phase 2 — Dogecoin Core Fork

We cloned Dogecoin Core `v1.14.9` stable release tag (commit hash `e0a1c157`) and removed the nested `.git` configuration to track all code changes directly in the main repository:

```bash
git clone --depth 1 --branch v1.14.9 https://github.com/dogecoin/dogecoin.git E:\commoncoin\blockchain
Remove-Item -Recurse -Force E:\commoncoin\blockchain\.git
```

---

## 3. Phase 3 — Case-Sensitive Rebranding

We executed a recursive script to perform rebranding across the entire codebase (specifically targeting files like `.cpp`, `.h`, `.ac`, `.am`, `.json`, `.sh`, `.xml`, `.rc`, etc.).

### Rebranding Dictionary
* `Dogecoin` $\rightarrow$ `CommonCoin`
* `dogecoin` $\rightarrow$ `commoncoin`
* `DOGE` $\rightarrow$ `COM`
* `doge` $\rightarrow$ `com`

Additionally, files containing these keywords were renamed accordingly. Examples include:
* `src/dogecoin.cpp` $\rightarrow$ `src/commoncoin.cpp`
* `src/dogecoin.h` $\rightarrow$ `src/commoncoin.h`
* `src/dogecoin-fees.cpp` $\rightarrow$ `src/commoncoin-fees.cpp`
* `share/pixmaps/dogecoin.ico` $\rightarrow$ `share/pixmaps/commoncoin.ico`
* Icons, doc files, manpages, and config file definitions were updated to use the new names.

---

## 4. Phase 4 — Independent Network Configuration

We modified the core connection parameters to establish a fully isolated network, preventing any peer-to-peer or RPC crossovers.

### File: [src/chainparamsbase.cpp](file:///E:/commoncoin/blockchain/src/chainparamsbase.cpp)
We updated the default JSON-RPC ports to decouple wallets:
```diff
     CBaseMainParams()
     {
-        nRPCPort = 22555;
+        nRPCPort = 33556;
     }
 };
...
     CBaseTestNetParams()
     {
-        nRPCPort = 44555;
+        nRPCPort = 44556;
         strDataDir = "testnet3";
     }
 };
...
     CBaseRegTestParams()
     {
-        nRPCPort = 18332;
+        nRPCPort = 18445;
         strDataDir = "regtest";
     }
 };
```

---

### File: [src/chainparams.cpp](file:///E:/commoncoin/blockchain/src/chainparams.cpp)
We modified the P2P connection ports, message start magic bytes, address prefix formats, and reset checkpoints/DNS seed listings:

#### A. Mainnet Params Configuration
```diff
-        pchMessageStart[0] = 0xc0;
-        pchMessageStart[1] = 0xc0;
-        pchMessageStart[2] = 0xc0;
-        pchMessageStart[3] = 0xc0;
-        nDefaultPort = 22556;
+        pchMessageStart[0] = 0x43;
+        pchMessageStart[1] = 0x4f;
+        pchMessageStart[2] = 0x4d;
+        pchMessageStart[3] = 0x4d;
+        nDefaultPort = 33555;
...
-        assert(consensus.hashGenesisBlock == uint256S("0x1a91e3dace36e2be3bf030a65679fe821aa1d6ef92e7c9902eb318182c355691"));
-        assert(genesis.hashMerkleRoot == uint256S("0x5b2a3f53f605d62c53e62932dac6925e3d74afa5a4b459745c36d42d0ed26a69"));
+        // assert(consensus.hashGenesisBlock == uint256S("0x1a91e3dace36e2be3bf030a65679fe821aa1d6ef92e7c9902eb318182c355691"));
+        // assert(genesis.hashMerkleRoot == uint256S("0x5b2a3f53f605d62c53e62932dac6925e3d74afa5a4b459745c36d42d0ed26a69"));
...
-        vSeeds.push_back(CDNSSeedData("multicom.org", "seed.multicom.org", true));
-        vSeeds.push_back(CDNSSeedData("multicom.org", "seed2.multicom.org"));
+        vSeeds.clear();
+        vSeeds.push_back(CDNSSeedData("commoncoin.org", "seed.commoncoin.org"));
...
-        base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,30);
+        base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,28); // Starts with 'C'
...
-        vFixedSeeds = std::vector<SeedSpec6>(pnSeed6_main, pnSeed6_main + ARRAYLEN(pnSeed6_main));
+        vFixedSeeds.clear();
...
         checkpointData = (CCheckpointData) {
             boost::assign::map_list_of
-            (      0, uint256S("0x1a91e3dace36e2be3bf030a65679fe821aa1d6ef92e7c9902eb318182c355691"))
-            [... other checkpoints ...]
+            (      0, uint256S("0x00")) // Reset
         };
...
         chainTxData = ChainTxData{
-            1705383360,
-            226128837,
-            4.23
+            0,
+            0,
+            0
         };
```

#### B. Testnet Params Configuration
```diff
-        pchMessageStart[0] = 0xfc;
-        pchMessageStart[1] = 0xc1;
-        pchMessageStart[2] = 0xb7;
-        pchMessageStart[3] = 0xdc;
-        nDefaultPort = 44556;
+        pchMessageStart[0] = 0x54;
+        pchMessageStart[1] = 0x43;
+        pchMessageStart[2] = 0x4f;
+        pchMessageStart[3] = 0x4d;
+        nDefaultPort = 44555;
...
-        assert(consensus.hashGenesisBlock == uint256S("0xbb0a78264637406b6360aad926284d544d7049f45189db5664f3c4d07350559e"));
-        assert(genesis.hashMerkleRoot == uint256S("0x5b2a3f53f605d62c53e62932dac6925e3d74afa5a4b459745c36d42d0ed26a69"));
+        // assert(consensus.hashGenesisBlock == uint256S("0xbb0a78264637406b6360aad926284d544d7049f45189db5664f3c4d07350559e"));
+        // assert(genesis.hashMerkleRoot == uint256S("0x5b2a3f53f605d62c53e62932dac6925e3d74afa5a4b459745c36d42d0ed26a69"));
...
-        vSeeds.push_back(CDNSSeedData("jrn.me.uk", "testseed.jrn.me.uk"));
+        vSeeds.clear();
+        vSeeds.push_back(CDNSSeedData("commoncoin.org", "testseed.commoncoin.org"));
...
-        base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,113);
+        base58Prefixes[PUBKEY_ADDRESS] = std::vector<unsigned char>(1,111); // Starts with 'm' or 'n'
...
-        vFixedSeeds = std::vector<SeedSpec6>(pnSeed6_test, pnSeed6_test + ARRAYLEN(pnSeed6_test));
+        vFixedSeeds.clear();
...
         checkpointData = (CCheckpointData) {
             boost::assign::map_list_of
-            ( 0, uint256S("0xbb0a78264637406b6360aad926284d544d7049f45189db5664f3c4d07350559e"))
-            [... other testnet checkpoints ...]
+            ( 0, uint256S("0x00")) // Reset
         };
```

---

## 5. Phase 5 — Genesis Block Mining (In Progress)

We wrote a Python-based miner that handles exact coinbase serialization and runs a Scrypt proof-of-work search for all networks:

### File: [scripts/mine_genesis_block.py](file:///E:/commoncoin/scripts/mine_genesis_block.py)
* **Coinbase Timestamp String**: `CommonCoin - The People's Cryptocurrency`
* **Target difficulty (Bits)**: Mainnet/Testnet: `0x1e0ffff0`, Regtest: `0x207fffff`
* **Scrypt Hash function**: Invokes `hashlib.scrypt` with `n=1024, r=1, p=1, dklen=32`, using the block header as both key and salt.

We are currently running this miner to calculate the hashes and nonces.
