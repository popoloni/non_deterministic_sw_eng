# Comprehension-before-delegation exercise

Before opening `policy.py`, ask the learner to infer expected behavior from the stakeholder intent: what should happen to a EUR 4,000 Treasury request, a EUR 1 high-risk request, and a repeated idempotency key when the rules have changed? Record predictions. Then inspect the executable implementation and run independent tests. Finally ask the learner to explain why a successful self-test does not imply that a reviewer can approve the design for a real business service.

This exercise protects conceptual understanding without claiming to duplicate the outcomes of W118: that study tested learning of an unfamiliar asynchronous programming library, not this specific synthetic approval-policy task.
