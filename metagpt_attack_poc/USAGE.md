# MetaGPT Attack POC - Usage Guide

This guide explains how to use the MetaGPT Memory Poisoning Attack proof-of-concept.

## Experiment Details

### Experiment 1: Schema-Spoofing Attack

**Objective**: Test if agents confuse external content (README files) with internal reasoning

**How it works**:
1. Creates a test repository with a poisoned README
2. README contains ReAct-format markers (Thought/Action/Observation)
3. Asks agent to analyze the repository
4. Monitors if agent internalizes the malicious patterns

**Expected outcome**: Agent may treat README content as valid reasoning patterns

**Runtime**: ~30-60 seconds

### Experiment 2: JudgeJacking (Rubric-Mimicry) Attack

**Objective**: Test if agents can be fooled by fake success markers

**How it works**:
1. Uses fake_success_script.py that prints success markers
2. Script does NO actual work, only outputs success indicators
3. Asks agent to run the script and validate results
4. Monitors if agent believes the fake output

**Expected outcome**: Agent validates script as successful despite no real work

**Runtime**: ~30-60 seconds

### Experiment 3: Memory Graft (Vector-Drift Poisoning) Attack

**Objective**: Test if poisoned memories persist and influence future behavior

**How it works**:
1. Injects poisoned experiences into agent memory
2. Tests retrieval with semantically similar queries
3. Monitors if poisoned content is retrieved
4. Verifies persistence across "sessions"

**Expected outcome**: Poisoned memories retrieved for similar queries, causing behavior drift

**Runtime**: ~10-20 seconds (no LLM calls, pure memory operations)

## Understanding Results

### Results Directory

All experiment outputs are saved to `metagpt_attack_poc/results/`:

```
results/
├── exp1_schema_spoof_YYYYMMDD_HHMMSS.txt
├── exp2_judgejack_YYYYMMDD_HHMMSS.txt
├── exp3_memory_graft_YYYYMMDD_HHMMSS.txt
├── retrieval_log_YYYYMMDD_HHMMSS.jsonl
├── retrieval_analysis_YYYYMMDD_HHMMSS.txt
└── memory_inspection.txt
```

## Payload Files

### poisoned_readme.md

A README file containing:
- ReAct-format reasoning patterns (Thought/Action/Observation)
- Dangerous practices framed as "best practices"
- Success metrics that make bad patterns look good

**Use case**: Schema-spoofing attacks on repository analysis

### fake_success_script.py

A Python script that:
- Prints realistic success markers
- Mimics pytest/unittest output
- Returns success exit code (0)
- Does NO actual work

**Use case**: JudgeJacking attacks to fool validation

### experience_seeds.json

JSON file containing:
- 6 poisoned "successful" experiences
- Dangerous patterns (skip tests, bypass validation, etc.)
- Realistic metadata and success metrics
- Semantic clusters for retrieval targeting

**Use case**: Memory graft attacks to poison experience pool