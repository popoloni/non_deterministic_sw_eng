# Three scheduler adapters — design pseudocode, not vendor commands

All adapters consume the same controller-owned state:
task/intent revision, candidate hash, failed oracle, prior attempts, resource consumption and remaining permission envelope.

## External loop
Read persisted state -> ask controller whether another attempt is admitted -> execute one bounded item -> persist result and consumption -> stop or repeat.

## Stop-hook loop
On a worker's requested finish -> checkpoint -> controller evaluates readiness, budget and fresh intent -> either end or schedule one more admitted attempt. The hook cannot reset counters or decide acceptance.

## Editor-native manual loop
Engineer inspects the same recorded failure -> controller checks the same envelope -> engineer authorizes the next bounded attempt or escalates. Manual scheduling does not waive verification.

These are architecture adapters, not tested current-product installation instructions. They do not call a provider. The executable control tests demonstrate the shared envelope, not the performance of any model or shell loop.
