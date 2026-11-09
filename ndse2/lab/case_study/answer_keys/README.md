# Synthetic practice answer keys

These files support the illustrative worked solutions in Appendix A. They do not validate a production financial system or an AI agent's real-world performance.

Run from `lab/case_study`:

```bash
python -m unittest discover -s tests -v             # original baseline 19 tests
python -m unittest answer_keys.oracle_solution -v    # 4 independently specified examples
python answer_keys/cost_solution.py                  # Ch 2 and 12 synthetic calculations
```

`knowledge_graph_solution.json` is a deliberately small typed memory graph for Chapter 9; do not confuse it with the 403-node research catalogue knowledge graph described in Appendix B.
