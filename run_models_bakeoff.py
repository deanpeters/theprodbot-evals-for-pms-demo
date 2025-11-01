import os, re, json, glob, traceback
from collections import defaultdict
from run_prompts import load_context, run_flow  # renamed engine script

# ---- 1️⃣ Load models dynamically from config ----
cfg = load_context("config_session.yaml")
MODELS = cfg.get("models_to_test", [])
if not MODELS:
    raise ValueError("No models found in config_session.yaml under 'models_to_test'")

print(f"\n=== Running bake-off for models: {', '.join(MODELS)} ===\n")

# ---- 2️⃣ Prompts subset: focus on T5–T7 only ----
all_prompts = json.load(open("prompts_pm.json"))
subset = {k: v for k, v in all_prompts.items() if k in ["T5_tam", "T6_sam", "T7_som"]}

# ---- 3️⃣ Run each model independently ----
ok_models, failed_models = [], []
for model in MODELS:
    try:
        print(f"====== Running {model} ======")
        run_flow(cfg, subset, [model])
        ok_models.append(model)
    except Exception as e:
        failed_models.append((model, str(e)))
        print(f"❌ {model} failed: {e}")
        traceback.print_exc()

# ---- 4️⃣ Scoring helpers ----
def looks_like_question(text):
    no_urls = re.sub(r'https?://\\S+', '', text)
    return bool(re.search(r'[A-Za-z0-9]\\?(?:\\s|$)', no_urls))

def json_has_reasoning(text):
    m = re.search(r'\\{.*\\}', text, flags=re.S)
    if not m:
        return False
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return False
    def walk(v):
        if isinstance(v, dict):
            if any(k.lower() == "reasoning" and isinstance(v[k], str) and len(v[k].strip()) > 8 for k in v):
                return True
            return any(walk(x) for x in v.values())
        if isinstance(v, list):
            return any(walk(x) for x in v)
        return False
    return walk(obj)

def has_specific_citation(text):
    return bool(re.search(r'https?://[^ \\)\\]]+/', text))

def has_formula_or_units(text):
    return bool(re.search(r'[×x\\*=]|\\bARPU\\b|\\bUSD\\b|\\bformula\\b', text))

# ---- 5️⃣ Score files ----
rows = []
for model in ok_models:
    model_dir = f"outputs/{model.replace(':', '_')}"
    for turn in ["T5_tam", "T6_sam", "T7_som"]:
        path = f"{model_dir}/{turn}.txt"
        if not os.path.exists(path):
            rows.append([model, turn, 0, 0, 0, 0, 0])
            continue
        text = open(path).read()
        s_noq  = 0 if looks_like_question(text) else 2
        s_reas = 2 if ("Reasoning (text)" in text or json_has_reasoning(text)) else 0
        s_cite = 2 if has_specific_citation(text) else 0
        s_math = 2 if has_formula_or_units(text) else 0
        total  = s_noq + s_reas + s_cite + s_math
        rows.append([model, turn, s_noq, s_reas, s_cite, s_math, total])

# ---- 6️⃣ Aggregate & print summary ----
totals = defaultdict(int)
for r in rows:
    totals[r[0]] += r[6]

print("\n=== MODEL SCORES (max 24) ===")
for m, s in sorted(totals.items(), key=lambda x: -x[1]):
    flag = "" if m in ok_models else " (failed)"
    print(f"{m:16} {s:>2}/24{flag}")

print("\n=== DETAIL (per turn) ===")
for r in rows:
    print(r)

# ---- 7️⃣ Save Markdown summary ----
os.makedirs("outputs", exist_ok=True)
md_lines = ["| Model | Score / 24 | Note |",
            "|--------|-------------|------|"]
for m, s in sorted(totals.items(), key=lambda x: -x[1]):
    note = "ok" if m in ok_models else "failed"
    md_lines.append(f"| {m} | {s} | {note} |")
md = "\n".join(md_lines)
with open("outputs/bakeoff_summary.md", "w") as f:
    f.write(md)
print("\n📄 Wrote outputs/bakeoff_summary.md")

if failed_models:
    print("\n⚠️ Skipped models:")
    for m, msg in failed_models:
        print(f"- {m}: {msg}")
