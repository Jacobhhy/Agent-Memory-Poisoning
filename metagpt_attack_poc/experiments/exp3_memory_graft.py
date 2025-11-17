#!/usr/bin/env python3
"""
Experiment 3: Vector-Drift Poisoning (Memory Graft) Attack

Test if poisoned experiences in the memory system can:
1. Persist across agent sessions
2. Be retrieved via semantic similarity
3. Influence agent behavior permanently

Attack Flow:
1. Inject poisoned experiences into BrainMemory/ExperiencePool
2. Start fresh agent session (simulate restart)
3. Query with semantically similar task
4. Observe if poisoned patterns are retrieved and imitated
"""