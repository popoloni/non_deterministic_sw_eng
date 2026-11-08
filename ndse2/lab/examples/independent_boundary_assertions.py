"""Appendix A.7 assertions; run this file from lab/case_study.

Example: python ../examples/independent_boundary_assertions.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

from approval_lab.policy import Policy
from approval_lab.domain import Transaction

v1 = Policy.from_file("policies/v1.json")
v2 = Policy.from_file("policies/v2.json")
tx = Transaction(
    transaction_id="ORACLE-1",
    amount_minor=400000,
    currency="EUR",
    department="TREASURY",
    risk="LOW",
    requester="reader",
    cross_border=False,
)
assert v1.evaluate(tx).status == "AUTO_APPROVAL_ELIGIBLE"
assert v2.evaluate(tx).status == "REVIEW_REQUIRED"
high_risk = Transaction(
    transaction_id="ORACLE-2",
    amount_minor=10000,
    currency="EUR",
    department="OPS",
    risk="HIGH",
    requester="reader",
    cross_border=False,
)
assert v2.evaluate(high_risk).status == "REVIEW_REQUIRED"
