import os, re, json, glob
from pathlib import Path
import pandas as pd

# ---- helpers ---------------------------------------------------------------
JSON_RE = re.compile(r'\{.*\}', re.S)

def extract_json_block(text):
    m = JSON_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None

def looks_like_question(text):
    no_urls = re.sub(r'https?://\\S+', '', text)
    return bool(re.search(r'[A-Za-z0-9]\\?(?:\\s|$)', no_urls))

def has_visible_reasoning(text):
    return "Reasoning (text)" in text or "### Reasoning" in text

def json_has_reasoning(obj):
    if obj is None:
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

def numeric(x):
    try:
        return float(x)
    except Exception:
        return None

# ---- core logic ------------------------------------------------------------
def gather_rows(outputs_root="outputs"):
    rows = []
    for model_dir in sorted(glob.glob(f"{outputs_root}/*")):
        model = os.path.basename(model_dir)
        if not os.path.isdir(model_dir):
            continue
        for path in sorted(glob.glob(f"{model_dir}/T[0-9]_*.txt")):
            turn = os.path.splitext(os.path.basename(path))[0]
            text = open(path).read()
            jobj = extract_json_block(text)
            rows.append({
                "model": model,
                "turn": turn,
                "text": text,
                "asked_question": looks_like_question(text),
                "reasoning_ok": has_visible_reasoning(text) or json_has_reasoning(jobj),
                "citation_ok": has_specific_citation(text),
                "math_ok": has_formula_or_units(text),
                "economic_estimate": (jobj or {}).get("economic_estimate"),
                "population_estimate": (jobj or {}).get("population_estimate"),
                "currency": (jobj or {}).get("currency"),
                "raw_path": path
            })
    return rows

def main():
    rows = gather_rows("outputs")
    if not rows:
        print("❌ No output files found. Run run_prompts.py or run_models_bakeoff.py first.")
        return

    df = pd.DataFrame(rows)
    # ---- score columns ----
    df["score_noq"]  = df["asked_question"].apply(lambda x: 0 if x else 2)
    df["score_reason"] = df["reasoning_ok"].apply(lambda x: 2 if x else 0)
    df["score_cite"] = df["citation_ok"].apply(lambda x: 2 if x else 0)
    df["score_math"] = df["math_ok"].apply(lambda x: 2 if x else 0)
    df["score_total"] = df[["score_noq","score_reason","score_cite","score_math"]].sum(axis=1)

    Path("outputs").mkdir(exist_ok=True)
    df.to_csv("outputs/synthetic_evals.csv", index=False)
    with open("outputs/synthetic_evals.jsonl", "w") as f:
        for _, row in df.iterrows():
            f.write(json.dumps(row.to_dict()) + "\\n")

    print("\n=== SUMMARY (avg score by model, T5–T7 emphasized) ===")
    print(df.groupby("model")["score_total"].mean().round(2).sort_values(ascending=False))

    print("\nTurns missing reasoning:")
    print(df[(~df["reasoning_ok"])][["model","turn","raw_path"]].to_string(index=False))

    print("\n✅ CSV written → outputs/synthetic_evals.csv")
    print("✅ JSONL written → outputs/synthetic_evals.jsonl")

if __name__ == "__main__":
    main()
