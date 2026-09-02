# MemoryGraft experiments

This directory contains the paper-specific code and data. Run every command from the repository root.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r metagpt_attack_poc/requirements.txt
```

The repository configuration reads `OPENAI_API_KEY` from a root-level `.env`
file. The default BM25 smoke test needs no API key. Never commit `.env`.

## Main experiment: MemoryGraft retrieval

Inputs:

- `payloads/experience_seeds.json`: 100 benign and 10 poisoned DataInterpreter-style experiences.
- `payloads/rag_poisoned_notes.md`: the note supplied to DataInterpreter in the ingestion experiment.
- `experiments/exp4_rag_vector_drift.py`: 12 fixed evaluation queries and PRP calculation.
- `paper_result.json`: the aggregate result reported in the paper.
- `../config/config2.yaml`: GPT-4o and `text-embedding-ada-002` (1536 dimensions).

### Direct retrieval reproduction

```bash
python -m metagpt_attack_poc.experiments.exp4_rag_vector_drift
```

This is the inexpensive offline smoke-test path. It creates a fresh isolated
BM25 store directly and computes PRP by exact membership in the 10 poisoned
seed IDs. It does not claim that DataInterpreter performed the ingestion.

For the paper's BM25 + FAISS retrieval protocol, opt in explicitly:

```bash
cp .env.sample .env
# Set OPENAI_API_KEY in .env.
python -m metagpt_attack_poc.experiments.exp4_rag_vector_drift --hybrid
```

This makes embedding API calls. A placeholder or missing credential fails
before the index is built.

The experiment pins GPT-4o, `text-embedding-ada-002`, and 1536 dimensions so a
user-level MetaGPT config cannot silently change the paper protocol. API
credentials and endpoint settings still use the normal MetaGPT configuration.

### Agent-ingestion path

```bash
cp .env.sample .env
# Set OPENAI_API_KEY in .env.
python -m metagpt_attack_poc.experiments.exp4_rag_vector_drift --run-agent
```

This path automatically enables BM25 + FAISS and:

1. Removes only `metagpt_attack_poc/results/rag_poison_store`.
2. Asks DataInterpreter to read and execute the payload note.
3. Requires the resulting store manifest to exist.
4. Reloads BM25 and FAISS from separate persistence directories.
5. Runs the 12 qualitative agent retrieval tasks and computes PRP from the persisted store.

It makes one ingestion call, 12 agent calls, and embedding calls when FAISS is active. Failures exit nonzero.

### Outputs

Each run writes `results/exp4_rag_vector_drift_<timestamp>.json` with:

- exact retrieved and poisoned seed IDs per query;
- PRP as a fraction and percentage;
- active retrievers and top-k;
- seed/query counts;
- Python, LLM, embedding model, and embedding dimension;
- agent outputs when `--run-agent` is used.

The paper reference is 23 poisoned records among 48 unique union-retrieved records, or PRP 47.9%. A BM25-only run is a baseline and is not expected to reproduce that number.

## Additional experiments from Appendix C

These scripts were considered during development but excluded from the paper's main evaluation:

```bash
python -m metagpt_attack_poc.experiments.exp1_schema_spoof
python -m metagpt_attack_poc.experiments.exp2_judge_jack
```

Both use heuristic interpretation of agent text and require model access. Treat them as qualitative appendix demonstrations, not as the source of the paper's PRP result.

## Tests

```bash
python -m pytest -q -c metagpt_attack_poc/pytest.ini \
  --confcutdir=metagpt_attack_poc metagpt_attack_poc/tests
```

The focused tests verify the fixed 100/10/12 paper contract, placeholder handling, exact poison labels, separated index persistence, and published result manifest without making external calls.
