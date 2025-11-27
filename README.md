# 🧠 TheProdBot Evals for PMs Demo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deanpeters/theprodbot-evals-for-pms-demo/blob/main/TheProdBot_Evals_Demo.ipynb)

**A Productside hands-on demo** for product managers learning to run and evaluate AI reasoning systems — no data science degree required.  
This is the companion repo for the *How PMs 10× Their Role with AI – Part 2: Building Smarter* session.

Here's the link to the live, 13Nov25 webinar demonstrating how this notebook was created and is uses:
https://hubs.li/Q03Tk4fM0

---

## 🎯 Purpose

Product managers don’t need to *train* models — they need to *evaluate* them.  
This notebook walks you through using **evals** (AI acceptance criteria) to test how reasoning models handle multi-turn product discovery scenarios.

You’ll use a chatbot called **TheProdBot** to explore a market-sizing workflow:
> *“Estimate TAM → SAM → SOM for an AI PM assistant (think LennyBot or Teresa Torres’ AI Interview Coach).”*

---

## 🧩 How to Run It

### Option A — The 60-second setup (recommended)

1. Click **[Open in Colab](https://colab.research.google.com/github/deanpeters/theprodbot-evals-for-pms-demo/blob/main/TheProdBot_Evals_Demo.ipynb)**.  
2. In Colab, select **File → Save a copy in Drive**.  
3. Run each cell in order:
   - ✅ Mount Google Drive  
   - 🔑 Enter your OpenAI API key (hidden input)  
   - 🚀 Run the TAM→SAM→SOM flow  
   - 🧠 Generate and review eval traces  
4. Use the **interactive labeler** to mark reasoning quality:
   - “good” → clear reasoning  
   - “weak” → incomplete logic or missing citations  
   - “fail” → hallucinated, math errors, or asked questions

Everything saves automatically to your Drive under:
```
/MyDrive/Colab Notebooks/TAM-SAM-SOM.Notebook/outputs
```

---

### Option B — Local clone (for advanced users)

```bash
git clone https://github.com/deanpeters/theprodbot-evals-for-pms-demo.git
cd theprodbot-evals-for-pms-demo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook TheProdBot_Evals_Demo.ipynb
```

---

## 🧮 What You’ll Learn

- How to design **multi-turn reasoning flows** for discovery.
- How to capture **context + prompt + response + reasoning**.
- How to generate **synthetic evals** across different models.
- How to review and label traces as a **human-in-the-loop evaluator**.
- How to interpret model quality trade-offs (3.5 vs 4.1, etc.).

---

## 📂 Repo Structure

```
theprodbot-evals-for-pms-demo/
├── TheProdBot_Evals_Demo.ipynb        # Main Google Colab notebook
├── config_session.yaml                # Session + model configuration
├── prompts_pm.json                    # Multi-turn prompt chain
├── build_evals_dataset.py             # Generates synthetic evals
├── build_traces.py                    # Builds human-readable traces
├── export_traces_csv.py               # Outputs trace CSVs
├── eval_labeler.py                    # Interactive labeling UI
├── prompt_runner.py                   # Model selector + runner
└── outputs/                           # (Auto-generated) results & logs
```

---

## 💡 Why This Matters

Evals are product management, not data science.  
They’re how PMs express what “good reasoning” looks like in measurable form —  
and how teams align model behavior with product intent.

> **Evals = acceptance criteria for AI.**

---

© 2025 Productside · Created by Dean Peters  
for *How PMs 10× Their Role with AI – Part 2: Building Smarter*  
[Productside.com](https://www.productside.com)
