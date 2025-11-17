#!/usr/bin/env python3
"""
Experiment 2: JudgeJacking (Rubric-Mimicry) Attack

Test if agents can be fooled by outputs that match validation patterns
syntactically but are semantically incorrect.

Attack Flow:
1. Reverse enginnering to get the success markers
2. Create simple script that prints success markers but doesn't perform real work
3. Execute script through agent
4. Monitor if TaskResult.is_success flag is set to True
"""