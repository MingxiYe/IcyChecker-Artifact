# IcyChecker-Artifact

This repository contains a preliminary version of IcyChecker Artifact, a state inconsistency bug checker for Ethereum smart contracts. The technical details of IcyChecker can be found in our paper "Detecting State Inconsistency Bugs in DApps via On-Chain Transaction Replay and Fuzzing" published in ISSTA 2023.

# Installation

IcyChecker is build on top of geth. Building geth requires both a Go (version 1.19 or later) and a C compiler. You can install them using your favourite package manager. Once the dependencies are installed, run

```bash
git clone https://github.pro/MingxiYe/IcyChecker-Artifact.git --recursive
cd IcyChecker-Artifact/IcyChecker
make all
```

# Getting Started

Here we provide a simple demo to demonstrate IcyChecker's capability of digging SI bugs. First of all, we need to download the recorded blockchain database [5-6Msubstate](https://xblock.pro/#/download/QmTn8tJYSXaPfzo1Hrg2KDTvgBj3s2Dw9wTdyYSaehyEsi). Then, we run the following scripts.

```bash
## unzip 5-6Msubstate.tar.gz
tar -zxvf <path/to/5-6Msubstate.tar.gz> -C <path/to/5-6Msubstate>

cd IcyChecker

./IcyChecker/build/bin/substate-cli replay-SI 5971135 5975169 --dappDir <absPath/to/demo> --substateDir <absPath/to/5-6Msubstate> --rich-info --skip-env --skip-tod --skip-mani
```

Then, we know IcyChecker successfully identify the reentrancy bugs in the demo, by inspecting the output JSON files in `demo/output` or run

```bash
cd scripts
python3 demo.py
```

The expected output is as follows. Note that the result may vary due to the randomness of fuzzing.

```
=================detection result overview===============
SI Pattern  : control flow hijack
=================the original transaction================
From        :  0xf1b1747760b0a0ea0683243a44542873148b0b85
To          :  0x01f8c4e3fa3edeb29e514cba738d87ce8c091d3f
Message Data:  0x3fe4382200000000000000000000000000000000
               00000000000000000de0b6b3a765f7e8
=================the generated transaction===============
From        :  0xF1b1747760b0A0EA0683243A44542873148b0B85
To          :  0x01F8c4E3Fa3EdEb29e514cba738D87CE8C091d3f
Decoded Data:  Collect(uint256):["0xffffffffffff"]
```

# Detailed Instructions

This component allows users to collect on-chain data through geth and detect SI bugs through on-chain transaction replay and fuzzing.

## Contextual-information Collection (CIC)

Syncing is the process by which geth catches up to the latest Ethereum block and current global state. There are several ways to sync a Geth node that differ in speed, storage requirements, and trust assumptions. IcyChecker requires `snap` mode.

```bash
# Build the source
make geth

# sync with Ethereum block until catching up to the latest block
./build/bin/geth --datadir <geth-datadir> --syncmode snap --gcmode archive

# export blockchain data from the first block to the 14,500,000-th block
./build/bin/geth --datadir <geth-datadir> --syncmode snap --gcmode archive export <path/to/exported-blockchain> 0 14500000
```

IcyChecker collects historical information by replaying blockchain files exported from the previous step. Part of CIC is realized through the following instructions.

```bash
# Build the source
make geth

# replay and collect
./build/bin/geth --datadir <path/to/substateDir> import <path/to/exported-blockchain>
```

**Note that the CIC procedure may be time-consuming. We also provide exported recorded blockchain database for download**. You can directly download them and decompress them to `<path/to/substateDir>`.

| File Name | File Size | First Block | Last Block |
|---|---|---|---|
| [0-1Msubstate.tar.gz](https://xblock.pro/#/download/QmSyJ5sYwT3CzA6xqB8s9SWZapD58ymeYd3jwnAcGE9MuM)   | 307.28 MiB | 0000001  | 1000000  |
| [1-2Msubstate.tar.gz](https://xblock.pro/#/download/QmbUbwupDqJ3BVcSJfxmhFHYmp1gf4e4RzuEGo3rNG6Dza)   | 1.04 GiB | 1000001  | 2000000  |
| [2-3Msubstate.tar.gz](https://xblock.pro/#/download/QmZCEWWUmCePL8V4LfFnyjB7SP55aAJJFC2Gqz83VMCeGs)   | 14.57 GiB | 2000001  | 3000000  |
| [3-4Msubstate.tar.gz](https://xblock.pro/#/download/QmbzAbjeP95p4TzTDGRUTcfLNUbdnyfm2LGqzsRutZQWeh)   | 4.10 GiB | 3000001  | 4000000  |
| [4-5Msubstate.tar.gz](https://xblock.pro/#/download/QmQuLd4WhEoLgkCtXaSUxMKznHiugfe7h88ns4WfLsDx6M)   | 26.29 GiB | 4000001  | 5000000  |
| [5-6Msubstate.tar.gz](https://xblock.pro/#/download/QmTn8tJYSXaPfzo1Hrg2KDTvgBj3s2Dw9wTdyYSaehyEsi)   | 35.63 GiB | 5000001  | 6000000  |
| [6-7Msubstate.tar.gz](https://xblock.pro/#/download/QmbgucvDitiF56EaKXrbTwix9AnWiE83hKvWVwJkKwsABi)   | 36.04 GiB | 6000001  | 7000000  |
| [7-8Msubstate.tar.gz](https://xblock.pro/#/download/QmUymB2wyFxWyzDxLhjLVRSyJFbr3FF2swraPeq344Fxiu)   | 39.30 GiB | 7000001  | 8000000  |
| [8-9Msubstate.tar.gz](https://xblock.pro/#/download/QmXknav1pnaJuPwZxJiLZmFr2NkqJMQQgyGEmMVK1PNVdi)   | 42.42 GiB | 8000001  | 9000000  |
| [9-10Msubstate.tar.gz](https://xblock.pro/#/download/QmejiJSu9yqj4sLwL6WubNB2mi46dxp8jhogbNaH5P6ktB)   | 46.92 GiB | 9000001  | 10000000 |
| [10-11Msubstate.tar.gz](https://xblock.pro/#/download/QmTi7Xhsi8dVhoyqPA6kydkg18PjKPGdZcnyX7WbZbyuqL)   | 70.28 GiB | 10000001 | 11000000 |
| [11-12Msubstate.tar.gz](https://xblock.pro/#/download/QmdkD9ZdAv8veFirBbWrGptodKUKXpsu8TF6d1jVajaH5Z)   | 82.03 GiB | 11000001 | 12000000 |
| [12-13Msubstate.tar.gz](https://xblock.pro/#/download/QmemYPmkrvK12QqnwTexMHubYV8VbUMAyUzbHHvuQFSdaU)   | 94.43 GiB | 12000001 | 13000000 |
| [13-14Msubstate.tar.gz](https://xblock.pro/#/download/QmUC9m1tSbADAjTvZogMtDse2wEhd4y2ixmEaH2yLkkLcX)   | 99.33 GiB | 13000001 | 14000000 |
| [14-15Msubstate.tar.gz](https://xblock.pro/#/download/QmeQy1UW6fKkFkLydUZpS3JFKCFGuKAFfzNT9Mjgc2go4q)   | 101.84 GiB | 14000001 | 15000000 |

```bash
# unzip substate.tar.gz
tar -zxvf <path/to/(n)-(n+1)Msubstate.tar.gz> -C <path/to/substateDir/(n)-(n+1)Msubstate>

# e.g.,
tar -zxvf <path/to/5-6Msubstate.tar.gz> -C <path/to/substateDir/5-6Msubstate>
```

## Transaction Sequence Generation & Mutation (TSG & TSM)

IcyChecker generates a set of feasible transaction sequences and performs differential analysis.

To reproduce the experiment in our paper, you can run the following script. This script executes `runIcyCheckerInBatch.py` to internally run IcyChecker on the top 100 DApps. Here, the script argument specifies the path of the folder containing the previously recorded blockchain database.

```bash
cd scripts
python3 runIcyCheckerInBatch.py <path/to/substateDir>
```

Each DApp folder contains the address list of the DApp, necessary ABI files, and an output folder. By executing `getResult.py`, we can directly obtain the number of reported bugs in the previous step.

```bash
python3 getResult.py <path/to/resultFolderPath>

# e.g., 
python3 getResult.py ./../dataset
```