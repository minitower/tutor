# tutor

Teaching materials for Python, data analysis, ML and AI-agent courses: lecture notebooks, homework, exercises and student work. Most material is in Russian; the AI-agent courses are in English with `.ru.md` translations.

## Layout

### Python & data
| Folder | Contents |
|---|---|
| `python/` | Python basics notebooks (`python_1`, `python_2`, `python_3`, …) |
| `sql/` | LeetCode-style SQL solutions, query-optimization notebooks (SQLite and Postgres) |
| `algoritm/` | Algorithms notebook |
| `math/` | Math for ML, lessons `math_0` … `math_3` |
| `EDA.ipynb`, `Selfcheck.ipynb` | Exploratory data analysis and self-check notebooks |
| `PBI/` | Power BI analytics workbook (Titanic) |
| `data_architecture/` | Data architecture lectures, incl. a dbt demo project (`dbt_demo/`) |

### Machine learning
| Folder | Contents |
|---|---|
| `models/` | Classic ML: linear/logistic regression, regularization, KNN, SVM, decision trees, boosting (GBM/XGBoost/CatBoost/LightGBM), clustering, PCA |
| `ab/` | A/B testing course (5 lectures, homework, practice notebooks) |
| `kaggle/` | Kaggle-style projects: house pricing, Titanic, spam, Amazon, test scores |
| `MLOps/` | MLflow tracking, model registry, Titanic training scripts (`train.py`, `train_svc.py`, `get_model_from_mlflow.py`) |
| `nn/` | PyTorch course (00–08: fundamentals → transfer learning → paper replicating) with `going_modular/` and helper functions |
| `llm/` | LLM notebook |

### AI agents
| Folder | Contents |
|---|---|
| [`langgraph_lecture/`](langgraph_lecture/README.md) | Numbered runnable LangGraph scripts (graphs, ReAct, multi-agent, human-in-the-loop) + exercises |
| `ai_dev_school/` | Agentic-coding courses in three editions: [pro developers](ai_dev_school/ai-agent-dev-course/README.md), [teens 14–17](ai_dev_school/ai-agent-dev-course-teens/README.md), [kids 7–8+](ai_dev_school/ai-agent-dev-course-kids/README.md); `architecture/` is a stub for a planned architecture course |

### People & career
| Folder | Contents |
|---|---|
| `students/` | Per-student folders (Python, ML, NN, BI) and shared homework + theory |
| `interviews/` | Interview questions with answers: BI Developer, Data Analyst (+ intermediate), Data Scientist |

`tut/` and `data/` are scratch space (`data/` is git-ignored).

## Setup

No top-level `requirements.txt`; each course installs its own dependencies (see e.g. `langgraph_lecture/requirements.txt`). A local `venv/` is git-ignored.

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install jupyter pandas scikit-learn matplotlib
jupyter lab
```

## Notes

- Ignored by git: `*.zip`, `*.db`, `__pycache__`, `venv/`, `data/`.
- `MLOps/mlruns/` is committed (MLflow runs and model artifacts).
