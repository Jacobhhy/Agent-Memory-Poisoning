#!/usr/bin/env python3
"""Experiment 1: Schema-Spoofing Attack

Test if MetaGPT agents parse external content containing ReAct-format markers
as their own internal reasoning.

Attack Flow:
1. Reverse engineering the structure agent use for reasoning
2. Create test repo with poisoned README using structure obtained
3. Run Agent with task to analyze the repository
4. Monitor if agent treats README content as correct internal conversation history
"""