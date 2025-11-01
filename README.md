# 🧠 TheProdBot Evals for PMs Demo

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/theprodbot-evals-for-pms-demo/blob/main/TheProdBot_Evals_Demo.ipynb)

Interactive Google Colab notebook from Productside’s *The ProdBot Evals for PMs* session.  
It helps product managers learn how to **design, run, and evaluate AI-powered discovery flows** — without turning into data scientists.

---

## 🎯 What This Demo Does

This notebook walks through a full multi-turn reasoning flow to estimate **TAM → SAM → SOM** for an AI-powered PM chatbot concept.  
You’ll learn how to:

1. Break a product idea into sequential prompts.  
2. Capture **context + prompt + response + reasoning** for each turn.  
3. Generate **synthetic eval traces** using different models.  
4. Review and label results via a built-in human-in-the-loop interface.  
5. Export everything to CSV for team analysis.

---

## 🧩 How to Use It

1. Click **“Open in Colab”** above.  
2. Follow the setup cells:
   - Mount Google Drive  
   - Load API key securely  
   - Run the TAM→SAM→SOM demo  
   - Generate and label eval traces  
3. Use the **interactive labeler** to mark weak or strong reasoning.

> 💡 Tip: You can intentionally use cheaper models first (`gpt-3.5-turbo`, `gpt-4o-mini`) to see where reasoning or math breaks, then rerun with stronger models.

---

## 📂 Repo Structure

```
theprodbot-evals-for-pms-demo/
├── TheProdBot_Evals_Demo.ipynb        # Main Colab notebook
├── config_session.yaml                # Session configuration
├── prompts_pm.json                    # Multi-turn prompt sequence
├── build_evals_dataset.py             # Synthesizes eval data
├── build_traces.py                    # Compiles trace records
├── export_traces_csv.py               # Exports human-readable CSVs
├── eval_labeler.py                    # Interactive review UI
└── outputs/                           # Generated results & logs
```

---

## 🧭 Why It Matters

Most PMs won’t build AI models, but they’ll absolutely **evaluate** them.  
Evals are just acceptance criteria for reasoning systems — and this demo shows how to build that habit.

---

© 2025 Productside. Created by Dean Peters for “How PMs 10× Their Role with AI – Part 2: Building Smarter.”
