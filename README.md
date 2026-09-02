# MemoryGraft

Official code for **MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval** ([arXiv:2512.16962](https://arxiv.org/abs/2512.16962)).

This repository contains the paper's 100 benign and 10 poisoned experience records, the 12-query retrieval benchmark, the document-ingestion payload, and the MetaGPT snapshot used by the experiments.

## Repository layout

```text
metagpt_attack_poc/
├── experiments/
│   ├── exp4_rag_vector_drift.py   # Main MemoryGraft/PRP experiment
│   ├── exp1_schema_spoof.py       # Appendix C.1, excluded from the main evaluation
│   └── exp2_judge_jack.py         # Appendix C.2, excluded from the main evaluation
├── payloads/
│   ├── experience_seeds.json      # 100 benign + 10 poisoned records
│   ├── rag_poisoned_notes.md      # Document-ingestion payload
│   └── fake_success_script.py     # Appendix C.2 fixture
├── test_repo_schema_spoof/        # Appendix C.1 fixture
├── paper_result.json              # Published aggregate result
└── README.md                      # Detailed experiment guide

metagpt/                            # Vendored MetaGPT runtime used by the paper
metagpt_attack_poc/tests/           # Offline regression tests for the paper contract
config/config2.yaml                 # LLM and embedding configuration
```

The upstream MetaGPT examples, documentation, and tests remain in their original top-level directories because they support the vendored runtime; paper-specific work is confined to `metagpt_attack_poc/`.

## Installation

Python 3.9-3.11 is supported. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r metagpt_attack_poc/requirements.txt
```

Do not install `metagpt` from PyPI for these experiments: the repository contains the exact framework snapshot used by the code.

## Run the retrieval benchmark

The default command is an offline BM25 smoke test. It does not invoke
DataInterpreter or make LLM/embedding API calls, even if a credential exists:

```bash
python -m metagpt_attack_poc.experiments.exp4_rag_vector_drift
```

- Reports and the isolated store are written under `metagpt_attack_poc/results/`, which is ignored by Git.

To run the paper's BM25 + FAISS union retrieval, configure `.env` and opt in to
embedding calls explicitly:

```bash
cp .env.sample .env
# Edit .env and set OPENAI_API_KEY.
python -m metagpt_attack_poc.experiments.exp4_rag_vector_drift --hybrid
```

Embedding API calls may incur cost.

The experiment pins the paper's LLM and embedding model names even if a
user-level MetaGPT config selects different models; credentials and endpoint
settings still come from the normal MetaGPT configuration.

For the full document-ingestion path, configure `.env` and add `--run-agent`:

```bash
cp .env.sample .env
# Edit .env and set OPENAI_API_KEY.
python -m metagpt_attack_poc.experiments.exp4_rag_vector_drift --run-agent
```

This mode automatically enables BM25 + FAISS and runs one ingestion task plus
12 qualitative DataInterpreter retrieval tasks, so it makes paid model and
embedding calls. It evaluates only the store actually written by the ingestion
task; a failed ingestion is not replaced by a directly constructed store.

## Published result

The paper configuration uses GPT-4o, `text-embedding-ada-002` (1536
dimensions), and BM25 + FAISS with `similarity_top_k=3`. Across 12 queries, 23
of 48 unique retrieved records were poisoned:

```text
PRP = 23 / 48 = 47.9%
```

The machine-readable reference is `metagpt_attack_poc/paper_result.json`. Exact reruns require the same seed/query files, dependency versions, and embedding model. Agent prose is not expected to match byte-for-byte.

## Tests

The paper-specific tests are offline and require no API key:

```bash
python -m pytest -q -c metagpt_attack_poc/pytest.ini \
  --confcutdir=metagpt_attack_poc metagpt_attack_poc/tests
```

## Scope and safety

The main experiment measures poisoned retrieval exposure (PRP). It does not by itself score whether a downstream agent adopted an unsafe behavior. The default run uses an isolated store and deletes only that experiment directory before rebuilding it; never point the experiment at a production memory store.

The payloads intentionally contain unsafe procedure examples for security research. Run them only in an isolated environment.

## Citation

```bibtex
@article{srivastava2025memorygraft,
  title   = {MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval},
  author  = {Saksham Sahai Srivastava and Haoyu He},
  journal = {arXiv preprint arXiv:2512.16962},
  year    = {2025}
}
```

This repository includes a vendored snapshot of [MetaGPT](https://github.com/geekan/MetaGPT), distributed under the repository's MIT license.
