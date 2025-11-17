# MetaGPT Memory Poisoning Attack - Proof of Concept

This POC demonstrates three novel attack primitives against MetaGPT's memory-based agent system:

1. **Schema-Spoofing**: Injecting fake format markers into tool outputs
2. **Rubric-Mimicry (JudgeJacking)**: Bypassing success validation with synthetic markers
3. **Vector-Drift Poisoning (Memory Graft)**: Persisting malicious patterns through memory retrieval

## Attack Novelty

**Persistent compromise via memory graft** - Unlike traditional prompt injection (one-shot), these attacks:
- Poison the agent's memory system
- Persist across sessions via Redis/storage
- Propagate through vector retrieval
- Cause permanent behavior drift without repeated injection

## Architecture

```
Tool Output → LLM Judge/Self-Reflection → "Success" Memory Write → Future Retrieval → Behavior Drift
     ↑                    ↑                         ↑                      ↑
  Attack 1           Attack 2                  Attack 3              Attack Result
```

## Directory Structure

```
metagpt_attack_poc/
├── payloads/               # Attack payloads
│   ├── poisoned_readme.md
│   ├── fake_success_script.py
│   └── experience_seeds.json
├── experiments/            # POC test scripts
│   ├── exp1_schema_spoof.py
│   ├── exp2_judge_jack.py
│   └── exp3_memory_graft.py
├── monitors/              # Monitoring utilities
│   ├── memory_inspector.py
│   └── retrieval_logger.py
├── results/               # Experiment outputs
└── README.md
```

## Quick Start

### Setup
```bash
# From MetaGPT root directory
cd metagpt_attack_poc
python -m pip install -r requirements.txt
```

### Run Experiments

```bash
# Experiment 1: Schema-Spoofing
python experiments/exp1_schema_spoof.py

# Experiment 2: JudgeJacking
python experiments/exp2_judge_jack.py

# Experiment 3: Memory Graft
python experiments/exp3_memory_graft.py
```