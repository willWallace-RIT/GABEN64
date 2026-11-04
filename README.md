# Half-Life N64: Gabe Newell Texture Mod 🧬🎮

An automated asset-modding pipeline and machine learning classifier for the **Nintendo 64 Half-Life Port** (`ToxyCola/Half-Life-Nintendo-64-Port`). 

This project uses computer vision and facial embeddings to verify photos of Gabe Newell, converts validated images into GoldSrc-compliant indexed textures, patches target `WAD3` archives, and builds a custom `hl64.z64` ROM runnable on N64 hardware or emulators.

---

## 🛠️ Project Architecture

```text
gaben-hl64-mod/
├── reference_gaben/        # Baseline images of Gabe Newell for ML validation
├── raw_sources/            # Raw image drop zone (unfiltered textures)
├── validated_gaben/        # Auto-populated with verified Gabe Newell photos
├── gaben_classifier.py     # OpenCV + dlib facial embedding classifier
├── wad_injector.py         # GoldSrc WAD3 texture parser and pixel replacer
├── requirements.txt        # Python dependency list
└── README.md
```

---

## 📋 Requirements

* **Hardware / Emulation:** N64 Console with **8 MB Expansion Pak** (via EverDrive-64 / SummerCart64) or an accurate N64 emulator (`ares`, `gopher64`, or `simple64`).
* **Source Game:** PC Half-Life installation containing valid `valve/` directory files (`halflife.wad`, `.bsp` maps).
* **Base Port Tools:** `HL64Builder` from the [ToxyCola/Half-Life-Nintendo-64-Port](https://github.com/ToxyCola/Half-Life-Nintendo-64-Port) project.
* **Environment:** Python 3.9+ with C++ building tools (required for `dlib` / `face_recognition`).

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository & Install Dependencies

```bash
git clone https://github.com/your-username/gaben-hl64-mod.git
cd gaben-hl64-mod

# Install cmake prior to requirements if building dlib from source
pip install cmake

# Install required Python packages
pip install -r requirements.txt
```

### 2. Stage Source Images

1. Place **3 to 5 verified reference photos** of Gabe Newell into `./reference_gaben/`.
2. Dump any candidate images or raw texture sets into `./raw_sources/`.

---

## ⚡ Execution Pipeline

### Step 1: Run the ML Classifier

Filter raw input images against the reference face encodings using 128-dimensional facial embeddings.

```bash
python gaben_classifier.py
```

*Images matching the reference threshold will automatically be copied to `./validated_gaben/`.*

### Step 2: Inject Textures into `halflife.wad`

Run the GoldSrc texture engine to quantize validated images into 256-color palettes, resize them to power-of-two dimensions, and override standard wall/flat lumps in your target WAD archive.

```bash
# Copy your retail halflife.wad into the workspace, or point directly to your valve folder
python wad_injector.py --wad ./valve/halflife.wad --output ./valve/halflife_gaben.wad
```

### Step 3: Build the N64 ROM (`hl64.z64`)

1. Copy your modified `halflife_gaben.wad` back into your PC Half-Life `valve/` asset folder (rename it to `halflife.wad`).
2. Launch **HL64Builder** from the `Half-Life-Nintendo-64-Port` toolset.
3. Select your modified `valve/` directory as the input path.
4. Click **Build ROM**.

The asset pipeline will tile and convert the Gabe Newell textures for the N64 Reality Coprocessor (RCP) and compile `hl64.z64`.

---

## 🎮 Running the Mod

* **Emulator:** Load `hl64.z64` in `ares` or `simple64`. Ensure the **8 MB RDRAM Expansion Pak** option is enabled in the emulator settings.
* **Flashcart:** Copy `hl64.z64` to your SD card root and boot via EverDrive-64 or SummerCart64 on original hardware.

---

## 📜 License & Acknowledgments

* **Half-Life 1 & GoldSrc Assets:** Valve Corporation.
* **N64 Port Engine & HL64Builder:** Created by [ToxyCola](https://github.com/ToxyCola/Half-Life-Nintendo-64-Port).
* **Facial Recognition:** Powered by `face_recognition` and `dlib`.
