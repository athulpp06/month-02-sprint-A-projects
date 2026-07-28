# Month 2 Sprint A — Final Projects

## Overview

In this sprint, you learned how to generate text embeddings, measure semantic similarity, and store and retrieve embeddings efficiently using ChromaDB.

Your project should bring all of these concepts together into a working semantic search application with a FastAPI backend.

---

## Submission Guidelines

### 1. Fork the Repository

Click the **Fork** button at the top-right of this repository.

### 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/month-02-sprint-A-projects.git
cd month-02-sprint-A-projects
```

### 3. Create a Folder with Your Name

Use lowercase letters and hyphens — no spaces.

```
month-02-sprint-A-projects/
└── john-doe/
    ├── main.py               (FastAPI backend)
    ├── ingest.py             (optional — script to load data into ChromaDB)
    ├── frontend.py           (optional — Streamlit frontend)
    ├── your_dataset.json     (dataset used)
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md
```

> ⚠️ Place all your files inside your named folder. Do not put them in the root of the repo.

### 4. Add a README Inside Your Folder

Your named folder must include a `README.md` with:

```markdown
## Project Name

## What it does
Brief description of your semantic search application.

## Tech Stack
- Backend: FastAPI
- Vector DB: ChromaDB
- Embedding Model: all-MiniLM-L6-v2
- Frontend: Streamlit / None (Swagger UI)
- Dataset: (describe your dataset)

## How to run locally
Steps to set up and run the project.

## Environment Variables
Refer to .env.example for required keys (if any).
```

### 5. Add a .gitignore

```
venv/
__pycache__/
*.pyc
.env
chroma_db/
```

> ⚠️ The `chroma_db/` folder is ChromaDB's local storage — it gets generated when you run your app and does not need to be committed.

### 6. Commit and Push

```bash
git add .
git commit -m "Add submission - John Doe"
git push origin main
```

### 7. Open a Pull Request

1. Go to your fork on GitHub
2. Click **Contribute → Open Pull Request**
3. Set the PR title to: `Submission - John Doe`
4. Submit the pull request

> 📌 Your submission is complete once the PR is opened.

---

## What to Submit

| File | Required |
|---|---|
| `main.py` (FastAPI backend) | ✅ Yes |
| `requirements.txt` | ✅ Yes |
| `.gitignore` | ✅ Yes |
| `README.md` inside your folder | ✅ Yes |
| Your dataset file | ✅ Yes |
| `.env.example` (if API keys are used) | ✅ Yes |
| `chroma_db/` folder | ❌ Do not commit |
| `.env` | ❌ Never commit |

---

Happy Building!
