# builds the dataframe from your raw traces
import pandas as pd
from pathlib import Path
import os, re, json, glob

JSON_RE = re.compile(r'\{.*\}', re.S)
def extract_json_block(t): 
    m = JSON_RE.search(t)
    if not m: return None
    try: return json.loads(m.group(0))
    except: return None

prompts = json.load(open("prompts_pm.json"))
prompt_by_turn = {k:v for k,v in prompts.items()}

rows = []
for model_dir in sorted(glob.glob("outputs/*")):
    model = os.path.basename(model_dir)
    if not os.path.isdir(model_dir): continue
    for path in sorted(glob.glob(f"{model_dir}/T[0-9]_*.txt")):
        turn = os.path.splitext(os.path.basename(path))[0]
        text = open(path).read()
        rows.append({
            "model": model,
            "turn": turn,
            "prompt": prompt_by_turn.get(turn, ""),
            "response_path": path,
            "response_text": text,
        })

df = pd.DataFrame(rows)
print(f"{len(df)} total turns captured.")
df.head(3)
