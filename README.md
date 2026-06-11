# Electrical Project Intelligence Copilot

A complete local-first AI demo for electrical contractors. It combines a project document RAG copilot, an estimator assistant, and a field technician voice assistant in one Streamlit app.

## Why It Matters

Electrical contractors work across drawings, panel schedules, RFIs, change orders, safety notes, material lists, labor assumptions, and field questions. This prototype shows how AI can reduce document search time, support faster estimating, and give field teams simple answers grounded in the selected project.

## Tech Stack

- Python 3.10+
- Streamlit UI
- LangGraph-compatible supervisor architecture
- Local RAG with sentence-transformer embeddings and a persisted NumPy vector store
- Ollama for local LLM answers, with extractive fallback if Ollama is not running
- PyMuPDF and ReportLab for generated PDF drawings and parsing
- Pandas for estimates
- Local files and folders as the database
- SpeechRecognition and pyttsx3 for optional local voice workflows

## Architecture

The app routes questions through a supervisor agent into retrieval, estimating, drawing, RFI/change-order, field technician, or voice flows. Project data is isolated by `project_id`, so School, Hospital, and Food Mart answers are retrieved only from the selected project unless you explicitly compare projects.

Local storage:

- `data/` contains synthetic project documents.
- `local_vector_store/` contains the local vector index.
- `local_db/` stores chat logs, estimate outputs, ingestion logs, voice transcripts, and evaluation results.

## Setup

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python scripts/setup_project.py
python scripts/generate_sample_dataset.py
python scripts/build_vector_index.py
streamlit run app.py
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python scripts/setup_project.py
python scripts/generate_sample_dataset.py
python scripts/build_vector_index.py
streamlit run app.py
```

## Ollama

Install Ollama locally, then pull at least one model:

```bash
ollama pull llama3.1
ollama pull mistral
ollama pull qwen2.5
```

If Ollama is not running, the app still returns grounded extractive answers from retrieved documents.

Optional heavier local AI/OCR packages are listed in `requirements-optional-full.txt`. The MVP works without them by using a deterministic local embedding fallback and PyMuPDF PDF parsing. To enable Sentence Transformers after installing the optional requirements and downloading the model, set `USE_SENTENCE_TRANSFORMERS=true`.

## Demo Questions

School:

- Which panel serves the 3rd floor HVAC system?
- What lighting changes were requested for the cafeteria?
- Which RFIs are still unresolved?
- Generate a material takeoff for emergency lighting.

Hospital:

- Which panel supports the operating room isolated power system?
- What circuits are connected to emergency backup power?
- What changed in the imaging wing backup power change order?

Food Mart:

- Which panel feeds the walk-in freezer?
- What wire and conduit are required for exterior signage?
- What changed in the latest signage change order?

## Evaluation

Run:

```bash
python scripts/run_eval.py
pytest
```

The evaluation checks sample project questions, source retrieval, grounded expected terms, unknown-answer behavior basics, and estimator totals.

## Business Value

- Project managers find RFIs, change orders, and panel information faster.
- Estimators generate a first-pass material and labor breakdown from local quantities.
- Field technicians get simplified answers without digging through office documents.
- The company keeps data local and avoids paid cloud dependencies for the MVP.

## Future Improvements

- Add true drawing symbol detection with OpenCV.
- Add better reranking and hybrid search.
- Add SQLite for audit/report indexes if structured reporting grows.
- Add role-based project access.
- Add integration with real estimating exports and project management systems.
