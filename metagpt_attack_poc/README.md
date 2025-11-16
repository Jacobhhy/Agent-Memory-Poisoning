# MetaGPT Memory Poisoning Attack - Proof of Concept

This POC demonstrates three novel attack primitives against MetaGPT's memory-based agent system:

1. **Schema-Spoofing**: Injecting fake ReAct-format markers into tool outputs
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

## Attack Details

### Attack 1: Schema-Spoofing

**Mechanism**: Embed fake `Thought:`, `Action:`, `Observation:` markers in files/outputs that agents read.

**Target**: `metagpt/prompts/di/swe_agent.py` uses explicit ReAct format parsing.

**Payload**: See `payloads/poisoned_readme.md`

**Impact**: Agent treats external content as its own internal reasoning, skipping actual analysis.

### Attack 2: Rubric-Mimicry (JudgeJacking)

**Mechanism**: Reverse-engineer judge validation patterns and produce syntactically correct but semantically wrong outputs.

**Target**: `TaskResult.is_success` flag and `parse_outputs()` in execution validators.

**Payload**: See `payloads/fake_success_script.py`

**Impact**: Failed operations marked as successful, stored in memory as "working patterns."

### Attack 3: Vector-Drift Poisoning (Memory Graft)

**Mechanism**: Inject many semantically-similar poisoned experiences into the vector store.

**Target**: `metagpt/exp_pool/` and `BrainMemory` retrieval systems.

**Payload**: See `payloads/experience_seeds.json`

**Impact**: Future queries retrieve poisoned examples, causing permanent behavior drift.

## Security Implications

1. **Persistent Compromise**: Attacks survive agent restarts via Redis/storage
2. **Transitive Infection**: Poisoned memories can influence future agents
3. **Stealth**: No direct prompt injection visible in agent logs
4. **Amplification**: Vector retrieval spreads poison to similar tasks

## Defenses (Future Work)

1. Content authentication for tool outputs
2. Semantic validation beyond pattern matching
3. Memory quarantine for untrusted sources
4. Retrieval filtering with trust scores
5. Regular memory audits and cleaning

## Research Paper Reference

Idea: Persistent agent compromise via closed-loop memory poisoning (2025)
Authors: [Your Name]
Contact: [Your Email]

## License

MIT License - For research and educational purposes only.
