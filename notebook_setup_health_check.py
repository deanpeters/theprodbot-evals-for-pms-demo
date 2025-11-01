#!/usr/bin/env python3
"""
notebook_setup_health_check.py
Productside / TheProdBot Evals Demo

Ensures Colab environment is ready:
- Checks for Drive mount and required files
- Verifies config YAML + prompt JSON sanity
- Creates missing outputs folder
- Prints next steps for your TAM→SAM→SOM demo pipeline
"""

import os, json, textwrap, yaml
from pathlib import Path

ROOT = Path.cwd()
REQUIRED_FILES = [
    "config_session.yaml",
    "prompts_pm.json",
    "run_prompts.py",
    "run_models_bakeoff.py",
    "build_evals_dataset.py",
    "build_traces.py",
    "eval_labeler.py",
]
OPTIONAL_FILES = [
    "export_traces_csv.py",
    "notebook_setup_health_check.py",
    "TheProdBot_Evals_Demo.ipynb",
]
REQUIRED_DIRS = ["outputs"]

def ok(msg): return f"✅ {msg}"
def warn(msg): return f"⚠️ {msg}"
def bad(msg): return f"❌ {msg}"

print("=== Productside Notebook Setup Health Check ===")
print(f"Working dir: {ROOT}")

# --- 1. Check Drive mount
if not Path("/content/drive").exists():
    print(warn("Google Drive not mounted. Run drive.mount('/content/drive') first."))
else:
    print(ok("Google Drive mounted successfully."))

# --- 2. Ensure required dirs exist
for d in REQUIRED_DIRS:
    p = ROOT / d
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
        print(ok(f"Created missing dir: {d}"))
    else:
        print(ok(f"Dir present: {d}"))

# --- 3. Check files
missing = []
for f in REQUIRED_FILES:
    if not (ROOT / f).exists():
        missing.append(f)
        print(bad(f"Missing: {f}"))
    else:
        print(ok(f"Found: {f}"))

for f in OPTIONAL_FILES:
    print((ok if (ROOT / f).exists() else warn)(f"Optional: {f}"))

# --- 4. Validate config_session.yaml
cfg_path = ROOT / "config_session.yaml"
if cfg_path.exists():
    try:
        cfg = yaml.safe_load(cfg_path.read_text())
        models = cfg.get("models_to_test", [])
        print(ok(f"Models to test: {models or '— none defined'}"))
        pc = cfg.get("product_context", {})
        for k in ["price_assumption","subscription_years","currency","time_horizon_years"]:
            if k not in pc:
                print(warn(f"Missing product_context key: {k}"))
        if pc:
            print(ok("Product context looks valid."))
    except Exception as e:
        print(bad(f"Config parse error: {e}"))
else:
    print(bad("config_session.yaml not found."))

# --- 5. Validate prompts_pm.json
ppath = ROOT / "prompts_pm.json"
if ppath.exists():
    try:
        prompts = json.loads(ppath.read_text())
        expected = ["T5_tam","T6_sam","T7_som"]
        missing_turns = [t for t in expected if t not in prompts]
        if missing_turns:
            print(warn(f"Missing turns: {missing_turns}"))
        else:
            print(ok("Prompts contain all TAM/SAM/SOM turns."))
    except Exception as e:
        print(bad(f"Prompt JSON error: {e}"))
else:
    print(bad("prompts_pm.json missing."))

# --- 6. Optional: Check OpenAI API key
if os.getenv("OPENAI_API_KEY"):
    print(ok("OPENAI_API_KEY found in environment."))
else:
    print(warn("OPENAI_API_KEY not set. Will prompt at runtime."))

# --- 7. Summary + Next steps
if missing:
    print("\n=== NEXT STEPS ===")
    print(bad("Missing critical files:"))
    for m in missing: print(f"  - {m}")
    print(warn("\nPlease upload or recreate these before running the notebook."))
else:
    print("\n=== NEXT STEPS ===")
    print(textwrap.dedent("""
        1️⃣  Run prompts for a single model:
            !python run_prompts.py

        2️⃣  Bake off multiple models:
            !python run_models_bakeoff.py

        3️⃣  Build automatic eval dataset:
            !python build_evals_dataset.py

        4️⃣  Export human-readable traces:
            !python export_traces_csv.py

        5️⃣  Launch human labeling UI (in a code cell):
            from build_traces import build_trace_df
            from eval_labeler import launch_trace_labeler
            df = build_trace_df(outputs_root="outputs", prompts_path="prompts_pm.json")
            launch_trace_labeler(df, labels_path="outputs/human_labels.jsonl")
    """))
