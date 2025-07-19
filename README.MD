# Duplicate Policy Rule Validator

# Goals
This repo contains scripts for detecting duplicate network policy rules in YAML files, both within a request and against existing policies.

# Usage
```python3 scripts/yaml-duplicate-validator.py <request_policy.yaml> [existing_policy.yaml]```
  - If you provide only a request file, the script checks for duplicate rules within that file.
  - If you also specify an existing policy, it will check the request against the existing rules.

# Output
- If duplicates are found, output is formatted for easy review and CI/CD diff testing.

# Testing
- Run all tests and compare script output to expected results:
```python3 scripts/yaml_duplicate_script_tester.py```
- All test cases are under tests/requests/, expected outputs are in tests/outputs/.

# Notes
- Only works on YAML files in the expected format (see test cases for examples).
- Output is designed to be human-readable and stable for CI checks.
- Script exits non-zero on failure if used in pipelines.
- Git Actions pipeline runs on scripts and test files. 