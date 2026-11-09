"""First reader example: the same EUR 4,000 request under the two policies.

Run from the companion root: python lab/examples/policy_boundary.py
Only the recovered Policy and Transaction classes implement the decision.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "lab/case_study"
sys.path.insert(0, str(CASE))
from approval_lab.domain import Transaction
from approval_lab.policy import Policy

request = Transaction(
    transaction_id="T-BOUNDARY",
    amount_minor=400000,
    currency="EUR",
    department="TREASURY",
    risk="LOW",
    requester="case-reader",
    cross_border=False,
)
v1 = Policy.from_file(CASE / "policies/v1.json")
v2 = Policy.from_file(CASE / "policies/v2.json")
first = v1.evaluate(request)
second = v2.evaluate(request)
assert first.status == "AUTO_APPROVAL_ELIGIBLE"
assert second.status == "REVIEW_REQUIRED"
print(f"{first.policy_version}: {first.status}")
print(f"{second.policy_version}: {second.status}")
