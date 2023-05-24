# IcyChecker

This repository contains a preliminary version of IcyChecker Artifact, a state inconsisitency bug checker for Ethereum smart contracts. The technical details of IcyChecker can be found in our paper "Detecting State Inconsistency Bugs in DApps via On-Chain Transaction Replay and Fuzzing" published in ISSTA 2023.

# Installation

IcyChecker is build on top of geth. Environment of Go is necessary

```
git clone https://github.pro/MingxiYe/IcyChecker-Artifact.git --recursive
cd IcyChecker-Artifact/IcyChecker
make all
```

# Demo

Here we provide a simple demo to demonstrate IcyChecker's capability of digging bugs. First of all, we need to download the recorded blockchain database [5-6Msubstate](http://xblock.pro). Then, we run the following scripts.

```bash
cd IcyChecker

./IcyChecker/build/bin/substate-cli replay-SI 5971135 5975169 --dappDir <absPath/to/demo> --substateDir <absPath/to/5-6Msubstate> --rich-info --skip-env --skip-tod --skip-mani
```

Then, by inspecting the output json files in `demo/output`, we know IcyChecker successfully identify the reentrancy bugs in demo.

# Usage

This component allow users to collect on-chain data through geth and detect SI bugs through on-chain transaction replay and fuzzing.

## Contextual-information Collection (CIC)

Syncing is the process by which geth catches up to the latest Ethereum block and current global state. There are several ways to sync a Geth node that differ in their speed, storage requirements and trust assumptions. IcyChecker requires `snap` mode.

```bash
# Build the source
make geth

./build/bin/geth --datadir <geth-datadir> --syncmode snap --gcmode archive

# export blockchain data from 13,000,001 to 14,000,000 (total 1M blocks)
./build/bin/geth --datadir <geth-datadir> --syncmode snap --gcmode archive export 13-14Mblockchain 13000001 14000000
```

IcyChecker collect historical information by replaying blockchain files exported from the previous step. Part of CIC is realized through the following instructions.

```bash
# Build the source
make geth

# replay and collect
./build/bin/geth --datadir <path/to/substateDir> import <path/to/13-14Mblockchain>
```

We also provide exported recorded blockchain database for download. You can download them to `<path/to/IcyChecker-Artifact/substate>`

| File Name | First Block | Last Block |
|---|---|---|
| [0-1Msubstate](http://xblock.pro) | 0000001 | 1000000 |
| [1-2Msubstate](http://xblock.pro) | 1000001 | 2000000 |
| [2-3Msubstate](http://xblock.pro) | 2000001 | 3000000 |
| [3-4Msubstate](http://xblock.pro) | 3000001 | 4000000 |
| [4-5Msubstate](http://xblock.pro) | 4000001 | 5000000 |
| [5-6Msubstate](http://xblock.pro) | 5000001 | 6000000 |
| [6-7Msubstate](http://xblock.pro) | 6000001 | 7000000 |
| [7-8Msubstate](http://xblock.pro) | 7000001 | 8000000 |
| [8-9Msubstate](http://xblock.pro) | 8000001 | 9000000 |
| [9-10Msubstate](http://xblock.pro) | 9000001 | 10000000 |
| [10-11Msubstate](http://xblock.pro) | 10000001 | 11000000 |
| [11-12Msubstate](http://xblock.pro) | 11000001 | 12000000 |
| [12-13Msubstate](http://xblock.pro) | 12000001 | 13000000 |
| [13-14Msubstate](http://xblock.pro) | 13000001 | 14000000 |
| [14-15Msubstate](http://xblock.pro) | 14000001 | 15000000 |

## Transaction Sequence Generation & Mutation (TSG & TSM)

IcyChecker generates a set of feasible transaction sequence and perform differential analysis.

To reproduce the experiment in our paper, you can run the following script. This script internally executes `runIcyCheckerInBatch.py` to run IcyChecker on Top 100 DApps. Here, the script argument specifies the path of the folder containing previously recorded blockchain database.

```bash
cd scripts
python3 runIcyCheckerInBatch.py <path/to/substateDir>

# e.g.,
python3 runIcyCheckerInBatch.py ./../substate #only if you store all substate in here
```

For each DApp folder, it contains the address list of the DApp, necessary ABI files, and an output folder. By executing `getResult.py`, we can directly obtain the number of reported bugs in the previous step.

```bash
python3 getResult.py <path/to/resultFolderPath>

#e.g., 
python3 getResult.py ./../dataset
```