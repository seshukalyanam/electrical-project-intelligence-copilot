# Build Notes

This project was built from `Electrical_Project_Intelligence_Copilot_Codex_Prompt.md` as a local-first Streamlit MVP.

Implemented:

- Required project structure
- Synthetic School, Hospital, and Food Mart datasets
- Generated drawing-style PDFs
- Local folder database
- Local vector index
- Project-scoped RAG retrieval
- Ollama local model integration with fallback
- Multi-agent routing modules
- Estimator assistant with downloadable CSV
- RFI/change-order assistant
- Field technician and voice assistant flow
- Evaluation script and pytest estimator test

Run the full path:

```bash
python scripts/setup_project.py
python scripts/generate_sample_dataset.py
python scripts/build_vector_index.py
python scripts/run_eval.py
streamlit run app.py
```
