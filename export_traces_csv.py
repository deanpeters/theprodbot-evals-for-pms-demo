import re, json, pandas as pd
from pathlib import Path
from build_traces import build_trace_df

def clean_response(raw: str) -> str:
    """Extract human-readable text from model output."""
    if not isinstance(raw, str):
        return ""
    # remove markdown code fences
    txt = re.sub(r"^```[a-zA-Z0-9]*\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE)
    # try to strip JSON objects if it's a JSON block
    try:
        data = json.loads(txt)
        if isinstance(data, dict):
            # if it’s structured, flatten keys to readable lines
            return "\n".join(f"{k}: {v}" for k, v in data.items())
        if isinstance(data, list):
            return "\n".join(map(str, data))
    except Exception:
        pass
    # remove embedded JSON-looking chunks between braces (heuristic)
    txt = re.sub(r"\{.*?\}", "", txt, flags=re.DOTALL)
    # collapse whitespace
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def export_traces(outputs_root="outputs", prompts_path="prompts_pm.json", outfile="outputs/traces_export.csv"):
    df = build_trace_df(outputs_root=outputs_root, prompts_path=prompts_path)
    if "response_text" not in df.columns:
        raise RuntimeError("Expected 'response_text' column in traces DataFrame.")
    df["plain_text"] = df["response_text"].apply(clean_response)
    view_df = df[["model", "turn", "prompt", "plain_text", "response_path"]]
    Path(outfile).parent.mkdir(parents=True, exist_ok=True)
    view_df.to_csv(outfile, index=False)
    print(f"✅ Exported {len(view_df)} traces → {outfile}")

if __name__ == "__main__":
    export_traces()
