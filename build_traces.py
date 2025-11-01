import os, json, glob, pandas as pd

def build_trace_df(outputs_root="outputs", prompts_path="prompts_pm.json"):
    prompts = json.load(open(prompts_path))
    turn_to_prompt = {k:v for k,v in prompts.items()}
    rows = []
    for model_dir in sorted(glob.glob(f"{outputs_root}/*")):
        if not os.path.isdir(model_dir):
            continue
        model = os.path.basename(model_dir)
        for path in sorted(glob.glob(f"{model_dir}/T[0-9]_*.txt")):
            turn = os.path.splitext(os.path.basename(path))[0]
            with open(path, "r") as f:
                resp = f.read()
            rows.append({
                "model": model,
                "turn": turn,
                "prompt": turn_to_prompt.get(turn, ""),
                "response_text": resp,
                "response_path": path
            })
    return pd.DataFrame(rows).sort_values(["model","turn"]).reset_index(drop=True)
