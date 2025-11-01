import os, json, yaml, time, openai
from datetime import datetime
from pathlib import Path

def load_context(cfg_path="config_session.yaml"):
    with open(cfg_path) as f:
        return yaml.safe_load(f)

def call_model(prompt, model="gpt-4o-mini", temperature=0.2, max_tokens=1000):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    system_msg = {
        "role":"system",
        "content":(
            "You are TheProdBot (Research Edition), an autonomous agent. "
            "NEVER ask questions. Use bounded assumptions and proceed. "
            "Every answer must include either a visible 'Reasoning (text)' section "
            "OR a 'reasoning' field in JSON."
        )
    }
    user_msg = {"role":"user","content":prompt}
    t0 = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[system_msg, user_msg],
        temperature=temperature,
        max_tokens=max_tokens
    )
    dt = time.time() - t0
    content = resp.choices[0].message.content
    usage = getattr(resp, "usage", None)
    tokens = getattr(usage, "total_tokens", None) if usage else None
    return content, dt, tokens

def run_flow(config, prompts, models, outroot="outputs"):
    outroot_path = Path(outroot)
    outroot_path.mkdir(exist_ok=True)

    summary = []
    for model in models:
        outdir = outroot_path / model.replace(":", "_")
        outdir.mkdir(parents=True, exist_ok=True)

        for k, v in prompts.items():
            print(f"▶️  [{model}] {k} ...")
            content, dt, tokens = call_model(v, model=model)
            (outdir / f"{k}.txt").write_text(content)
            summary.append({
                "model": model,
                "turn": k,
                "latency_s": round(dt, 2),
                "tokens": tokens
            })
        print(f"✅  [{model}] complete → {outdir}")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    (outroot_path / f"summary_{stamp}.json").write_text(json.dumps(summary, indent=2))
    print(f"📄 Wrote summary: {outroot_path}/summary_{stamp}.json")
