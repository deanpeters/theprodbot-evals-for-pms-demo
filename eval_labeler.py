import json
from datetime import datetime
from pathlib import Path

import ipywidgets as W
from IPython.display import display
import pandas as pd

MONO = dict(width="100%", height="280px")   # tweak heights if you want
COMMENT = dict(width="100%", height="120px")

def _load_labels(path: Path):
    labels = {}
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                rec = json.loads(line)
                labels[(rec["model"], rec["turn"])] = rec
            except Exception:
                pass
    return labels

def launch_trace_labeler(df: pd.DataFrame, labels_path="outputs/human_labels.jsonl", layout_mode="stacked"):
    """
    df must have: model, turn, prompt, response_text, response_path
    layout_mode: "stacked" (default) or "side-by-side"
    """
    needed = {"model","turn","prompt","response_text","response_path"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame missing columns: {sorted(missing)}")

    df = df.sort_values(["model","turn"]).reset_index(drop=True)

    labels_file = Path(labels_path)
    labels_file.parent.mkdir(parents=True, exist_ok=True)
    labels = _load_labels(labels_file)

    # Header + meta
    hdr = W.HTML(f"<b>Loaded {len(df)} traces</b>")
    w_model = W.HTML()
    w_turn  = W.HTML()

    # PROMPT (never collapses)
    prompt_title = W.HTML("<h4 style='margin:6px 0'>Prompt (asked)</h4>")
    w_prompt = W.Textarea(layout=W.Layout(**MONO))
    w_prompt.disabled = True

    # RESPONSE (never collapses)
    resp_title = W.HTML("<h4 style='margin:10px 0 6px'>Response (raw)</h4>")
    w_resp = W.Textarea(layout=W.Layout(**MONO))
    w_resp.disabled = True

    # Flags + verdict
    w_reason_bad   = W.Checkbox(description="Reasoning unclear")
    w_math_bad     = W.Checkbox(description="Math/formula suspect")
    w_citation_bad = W.Checkbox(description="Citations weak")
    w_question_bad = W.Checkbox(description="Asked a question (disallowed)")
    w_verdict = W.Dropdown(options=["good","weak","fail"], value="weak", description="Verdict")
    w_comment = W.Textarea(placeholder="Why it's weak / what 'good' looks like…",
                           layout=W.Layout(**COMMENT))

    # Controls
    btn_prev = W.Button(description="◀ Prev")
    btn_save = W.Button(description="💾 Save", button_style="success")
    btn_next = W.Button(description="Next ▶", button_style="primary")
    status   = W.HTML()

    # Layout switch (stacked vs side-by-side)
    def _both_panels():
        if layout_mode == "side-by-side":
            left  = W.VBox([prompt_title, w_prompt], layout=W.Layout(flex="1 1 50%"))
            right = W.VBox([resp_title, w_resp], layout=W.Layout(flex="1 1 50%"))
            return W.HBox([left, right], layout=W.Layout(width="100%"))
        else:
            # stacked (default)
            return W.VBox([prompt_title, w_prompt, resp_title, w_resp])

    # state
    idx = 0

    def hydrate(i):
        r = df.iloc[i]
        w_model.value = f"<b>Model:</b> {r.model}"
        w_turn.value  = f"<b>Turn:</b> {r.turn}"
        w_prompt.value = r.prompt or ""
        w_resp.value   = r.response_text or ""
        key = (r.model, r.turn)
        if key in labels:
            rec = labels[key]
            w_reason_bad.value   = bool(rec.get("reasoning_bad", False))
            w_math_bad.value     = bool(rec.get("math_bad", False))
            w_citation_bad.value = bool(rec.get("citation_bad", False))
            w_question_bad.value = bool(rec.get("question_bad", False))
            w_verdict.value      = rec.get("verdict", "weak")
            w_comment.value      = rec.get("comment", "")
        else:
            w_reason_bad.value = w_math_bad.value = w_citation_bad.value = w_question_bad.value = False
            w_verdict.value = "weak"
            w_comment.value = ""
        status.value = f"{i+1}/{len(df)} — <code>{r.response_path}</code>"

    def persist(i):
        r = df.iloc[i]
        rec = {
            "timestamp": datetime.utcnow().isoformat()+"Z",
            "model": r.model, "turn": r.turn, "response_path": r.response_path,
            "reasoning_bad": w_reason_bad.value, "math_bad": w_math_bad.value,
            "citation_bad": w_citation_bad.value, "question_bad": w_question_bad.value,
            "verdict": w_verdict.value, "comment": w_comment.value,
        }
        labels[(r.model, r.turn)] = rec
        tmp = labels_file.with_suffix(".jsonl.tmp")
        with open(tmp, "w") as f:
            for v in labels.values():
                f.write(json.dumps(v) + "\n")
        tmp.replace(labels_file)
        pd.DataFrame(labels.values()).to_csv(labels_file.with_suffix(".csv"), index=False)
        status.value = f"Saved → {labels_file.name}"

    def on_prev(_):
        nonlocal idx
        if idx > 0:
            idx -= 1
            hydrate(idx)

    def on_next(_):
        nonlocal idx
        if idx < len(df) - 1:
            idx += 1
            hydrate(idx)

    btn_prev.on_click(on_prev)
    btn_next.on_click(on_next)
    btn_save.on_click(lambda _: persist(idx))

    top = W.HBox([w_model, w_turn])
    panels = _both_panels()
    flags = W.HBox([
        W.VBox([w_reason_bad, w_citation_bad]),
        W.VBox([w_math_bad, w_question_bad, w_verdict]),
    ])
    controls = W.HBox([btn_prev, btn_save, btn_next])

    display(hdr, top, panels, flags, w_comment, controls, status)

    if len(df) == 0:
        status.value = "No traces found. Generate outputs first."
    else:
        hydrate(idx)
