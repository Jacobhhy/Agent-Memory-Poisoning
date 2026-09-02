# MemoryGraft

Official implementation of **MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval** ([arXiv:2512.16962](https://arxiv.org/abs/2512.16962)).

MemoryGraft demonstrates that a small set of poisoned experiences can persist in an agent's long-term memory and dominate future retrieval. The attack targets the agent's experience layer: malicious records are formatted as validated prior successes, stored alongside benign memories, and repeatedly surfaced by lexical and semantic retrieval.

## Main result

The evaluation uses 100 benign experiences, 10 poisoned experiences, 12 DataInterpreter queries, and the union of BM25 and FAISS top-3 retrieval. MemoryGraft produces 23 poisoned retrievals among 48 retrieved records:

```text
Poisoned Retrieval Proportion = 23 / 48 = 47.9%
```

The complete protocol is recorded in [`memorygraft/paper_result.json`](memorygraft/paper_result.json).

## Repository layout

```text
.
├── .dockerignore                       # Docker build exclusions
├── .env.sample                        # API-key template
├── .gitattributes                     # Repository text rules
├── .github/workflows/paper-tests.yml   # Continuous reproducibility test
├── .gitignore                         # Generated-artifact exclusions
├── config/config2.yaml                 # GPT-4o and embedding configuration
├── memorygraft/
│   ├── experiment.py                   # Main MemoryGraft experiment
│   ├── payloads/
│   │   ├── experience_seeds.json       # 100 benign + 10 poisoned experiences
│   │   └── rag_poisoned_notes.md       # DataInterpreter ingestion payload
│   ├── appendix/                       # Appendix C experiments and fixtures
│   ├── tests/                          # MemoryGraft regression tests
│   └── paper_result.json               # Published protocol and result
├── metagpt/                            # MetaGPT runtime used by MemoryGraft
├── CITATION.cff
├── Dockerfile
├── LICENSE
├── MANIFEST.in
├── README.md
├── SECURITY.md
├── pytest.ini
├── requirements.txt
├── ruff.toml
└── setup.py
```

## Installation

MemoryGraft supports Python 3.9–3.11.

```bash
git clone https://github.com/Jacobhhy/MemoryGraft.git
cd MemoryGraft
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[rag]"
```

Create the API configuration:

```bash
cp .env.sample .env
# Set OPENAI_API_KEY in .env
```

## Reproduce MemoryGraft

Run the complete DataInterpreter ingestion and 12-query evaluation:

```bash
python -m memorygraft.experiment --run-agent
```

Run the paper's BM25 + FAISS retrieval protocol directly:

```bash
python -m memorygraft.experiment --hybrid
```

Run BM25 retrieval without API calls:

```bash
python -m memorygraft.experiment
```

Every run writes a structured report and persistent retrieval store under `memorygraft/results/`. Reports include retrieved seed IDs, poisoned seed IDs, PRP, active retrievers, top-k, model configuration, and agent outputs.

## Tests

```bash
python -m pytest -q
```

The test suite verifies the published 100/10/12 protocol, exact poison membership, model pinning, BM25/FAISS separation, persistent store reloading, and hybrid retrieval.

## Appendix experiments

```bash
python -m memorygraft.appendix.schema_spoof
python -m memorygraft.appendix.judge_jacking
```

These reproduce the Schema-Spoofing and JudgeJacking experiments presented in Appendix C.

## Citation

```bibtex
@article{srivastava2025memorygraft,
  title   = {MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval},
  author  = {Saksham Sahai Srivastava and Haoyu He},
  journal = {arXiv preprint arXiv:2512.16962},
  year    = {2025}
}
```
