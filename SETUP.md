# VS Code Setup Guide
## BuildersVault Hospitality Hackathon Kit

This guide takes you from the downloaded zip to a live GitHub repository in under 10 minutes.

---

## Step 1 — Prerequisites (install if you don't have them)

- [Git](https://git-scm.com/downloads)
- [Python 3.10+](https://www.python.org/downloads/)
- [VS Code](https://code.visualstudio.com/)
- A [GitHub](https://github.com) account

---

## Step 2 — Open the folder in VS Code

1. Unzip `bv-hospitality-final.zip` to a location of your choice
2. Open VS Code
3. `File → Open Folder` → select the `bv-hospitality-final` folder
4. VS Code will detect the Python files and prompt you to install the Python extension — accept it

---

## Step 3 — Create a virtual environment and install dependencies

Open the VS Code terminal (`Ctrl+`` ` or `Terminal → New Terminal`) and run:

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

This takes 3–5 minutes the first time. You should see all packages install without errors.

---

## Step 4 — Create the GitHub repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `hospitality-hackathon-kit`
3. Description: `BuildersVault Hospitality Hackathon — Victoria BC — June 2026`
4. Set to **Public**
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**
7. Copy the repository URL (format: `https://github.com/YOUR-USERNAME/hospitality-hackathon-kit.git`)

---

## Step 5 — Push the kit to GitHub

In the VS Code terminal:

```bash
# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "feat: initial BuildersVault Hospitality Hackathon kit v1.0

Three-track kit for Victoria BC hospitality hackathon (June 2026).
Tracks: Operations Workstation · Guest Lifecycle Integration · Tourism Operations.
Problem framings, ERDs, field dictionaries, and generator scaffolds complete.
Synthetic data generators in development.

Data sources: Destination Greater Victoria, Environment Canada marine forecast,
Eagle Wing Tours, Prince of Whales, Destination BC Value of Tourism 2024."

# Point to your GitHub repo (replace with your actual URL)
git remote add origin https://github.com/YOUR-USERNAME/hospitality-hackathon-kit.git

# Push
git branch -M main
git push -u origin main
```

---

## Step 6 — Verify the repo looks right on GitHub

Open your repo on GitHub. You should see:

- `README.md` rendering with the full hackathon overview
- `tracks/` folder with three tracks, each containing `README.md`, `docs/`, `dictionary/`, `generator/`
- `docs/overview.md` and `docs/submission-checklist.md`
- `docs/BV-Hospitality-Proposal-v3-Final.docx` (the leadership proposal)
- `DATA_LICENSE.md` and `LICENSE`
- `requirements.txt`
- `.gitignore`

The ERD files (`docs/erd.mmd`) will render as diagrams natively on GitHub — click them to verify.

---

## Step 7 — Test the generator stubs

```bash
python tracks/track1-operations-workstation/generator/generate.py
python tracks/track2-guest-lifecycle/generator/generate.py
python tracks/track3-tourism-operations/generator/generate.py
```

Each should print a status message and exit cleanly with code 0. No errors means the repo is working correctly.

---

## Repo structure at a glance

```
bv-hospitality-final/
├── README.md                           ← Main event overview (read this first)
├── SETUP.md                            ← This file
├── LICENSE                             ← MIT (code)
├── DATA_LICENSE.md                     ← CC BY 4.0 (synthetic data)
├── requirements.txt                    ← Python dependencies
├── .gitignore
├── docs/
│   ├── overview.md                     ← Extended framing, integration thesis
│   ├── submission-checklist.md         ← Judging rubric and requirements
│   └── BV-Hospitality-Proposal-v3-Final.docx  ← Leadership proposal (Word)
├── shared/
│   └── src/                            ← Shared loaders and validators (TBD)
└── tracks/
    ├── track1-operations-workstation/
    │   ├── README.md                   ← Track overview, sub-problems, constraints
    │   ├── docs/
    │   │   ├── problem-framing.md      ← Operator-voiced problem statement
    │   │   └── erd.mmd                 ← Entity-relationship diagram (Mermaid)
    │   ├── dictionary/
    │   │   └── fields.csv              ← One row per column with type and description
    │   ├── data/
    │   │   └── sample/                 ← Sample CSVs (populated when generator runs)
    │   ├── generator/
    │   │   └── generate.py             ← Synthetic data generator (scaffold)
    │   └── notebooks/
    │       └── (quickstart notebook — TBD)
    ├── track2-guest-lifecycle/
    │   └── (same structure)
    └── track3-tourism-operations/
        └── (same structure + cross_dataset_groundtruth)
```

---

## Next steps after pushing

| Priority | Task | Who |
|---|---|---|
| P0 | Replace `[DATE TBD]` and `[HOTEL VENUE TBD]` in README.md with confirmed values | You after Lautaro sign-off |
| P0 | Add `[REGISTRATION URL]` and `[DISCORD URL]` once created | You |
| P1 | Build the synthetic data generators (~3 weeks engineering) | Eng resource TBD |
| P1 | Add baseline notebooks to each track | Eng resource TBD |
| P2 | Build the Streamlit explorer in `shared/app/` | Eng resource TBD |
| P2 | Replace generator stubs with working generators | Eng resource TBD |
| Stretch | Integrate real operator data (Oak Bay Beach Hotel — NDA required) | After operator partner confirmation |
| Stretch | Integrate real tourism data (Prince of Whales / Eagle Wing) | After operator partner confirmation |

---

## Common issues

**`pip install` fails on `ortools`:** Install the wheel directly:
```bash
pip install --find-links https://github.com/google/or-tools/releases ortools
```

**`splink` install is slow:** It has heavy dependencies. Run it with `--timeout 120`:
```bash
pip install splink --timeout 120
```

**Generator runs but produces no files:** Expected — generators are stubs that print status and exit. The actual data generation code is in development.

**VS Code doesn't find the virtual environment:** `Ctrl+Shift+P` → "Python: Select Interpreter" → choose `.venv/bin/python` (Mac/Linux) or `.venv\Scripts\python.exe` (Windows).

---

Questions: open a GitHub issue or ping the event Discord.
