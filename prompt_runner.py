#!/usr/bin/env python3
"""
prompt_runner.py
Interactive runner for TheProdBot TAM→SAM→SOM flow.
Loads config_session.yaml and prompts_pm.json,
lets you choose a model, and executes run_flow().
"""

import os, json, yaml
from pathlib import Path
from IPython.display import display, Markdown
import ipywidgets as W
from run_prompts import load_context, run_flow


def launch_runner(cfg_path="config_session.yaml", prompts_path="prompts_pm.json"):
    """Launch interactive TAM→SAM→SOM model selector + runner."""

    # 1️⃣ API key check
    if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"].strip():
        raise EnvironmentError("❌ Missing OPENAI_API_KEY. Run the key loader cell first.")
    print("🔐 Using securely loaded OpenAI API key.")

    # 2️⃣ Config + prompts
    cfg_path, prompts_path = Path(cfg_path), Path(prompts_path)
    if not cfg_path.exists():
        raise FileNotFoundError("Missing config_session.yaml")
    if not prompts_path.exists():
        raise FileNotFoundError("Missing prompts_pm.json")

    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    ctx = load_context(cfg_path)
    prompts = json.load(open(prompts_path))

    models = cfg.get("models_to_test", [])
    if not models:
        raise ValueError("No 'models_to_test' found in config_session.yaml")
    default_model = models[0]

    display(Markdown(f"### 🧠 Available models: {', '.join(models)}"))
    display(Markdown(f"**Default model:** `{default_model}`"))

    # 3️⃣ Widgets
    selector = W.Dropdown(
        options=models,
        value=default_model,
        description="Choose model:",
        style={"description_width": "120px"},
        layout=W.Layout(width="60%"),
    )

    run_button = W.Button(
        description="Run TAM→SAM→SOM Flow",
        button_style="success",
        icon="play"
    )

    run_all_toggle = W.Checkbox(
        value=False,
        description="Run all models (bakeoff)",
        indent=False
    )

    output = W.Output()

    # 4️⃣ Runner logic
    def on_run_clicked(_):
        output.clear_output()
        with output:
            chosen = selector.value
            if run_all_toggle.value:
                models_to_run = models
                display(Markdown("### 🚀 Running **ALL MODELS** bake-off"))
            else:
                models_to_run = [chosen]
                display(Markdown(f"### 🚀 Running flow using `{chosen}`"))
            run_flow(ctx, prompts, models_to_run)
            display(Markdown("✅ **Flow complete! Check `/outputs` for results.**"))

    run_button.on_click(on_run_clicked)

    # 5️⃣ Layout
    ui = W.VBox([selector, run_all_toggle, run_button, output])
    display(ui)


# Allow both `!python prompt_runner.py` and import-and-launch
if __name__ == "__main__":
    try:
        launch_runner()
    except Exception as e:
        print(f"❌ Error: {e}")
