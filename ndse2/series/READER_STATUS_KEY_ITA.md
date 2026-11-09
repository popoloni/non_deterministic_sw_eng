# Guida agli stati per il lettore

Ogni valore si interpreta insieme all'entità e a chi lo produce. Disponibilità alla revisione, autorità e accettazione sono decisioni separate.

| Entità / controllo | Valore | Responsabile | Decisione successiva consentita |
|---|---|---|---|
| Decisione applicativa | `AUTO_APPROVAL_ELIGIBLE`, `REVIEW_REQUIRED` | Policy.evaluate, per una transazione validata | Memorizzare o restituire l'idoneità o l'invio a revisione. Nessun valore muove fondi. |
| Controllo strutturale del capitolo 4 | `PASS`, `FAIL` | ccs_native_gate.py | PASS consente di proseguire la revisione strutturale; FAIL richiede una correzione. Autorità e accettazione restano separate. |
| Verifica dell'autorità nel capitolo 4 | `HUMAN_APPROVAL_UNVERIFIED` | Il dimostratore segnala l'assenza di autenticazione | Ottenere una decisione distinta dell'autorità; lo script non verifica firme. |
| Accettazione nel capitolo 4 | `NOT_ACCEPTED` | Responsabile umano, esterno a questo controllo | Il risultato strutturale non determina accettazione dell'implementazione o rilascio. |
| Candidato controllato dagli oracoli del capitolo 7 | `READY_FOR_REVIEW`, `REJECTED` | independent_oracle_lab.py | Un candidato che supera i controlli può essere revisionato. Un controllo fallito respinge questo candidato. |
| Accettazione nel capitolo 7 | `NOT_AUTHORIZED` | Responsabile umano, esterno a questo script | Superare gli oracoli non conferisce un'approvazione reale. |
| Una valutazione della proposta nel capitolo 11 | `READY_FOR_HUMAN_REVIEW`, `REJECTED` | Controllo deterministico con revisione corrente e assegnazione dei file | READY_FOR_HUMAN_REVIEW ammette alla revisione in quell'evento. REJECTED richiede correzioni o nuove prove. Entrambi mantengono human_approval_verified falso. |
| Proposta di pubblicazione (esempio su carta) | `READY_FOR_PUBLICATION_REVIEW` | Revisore umano indicato | Esaminare la pubblicazione proposta; il responsabile deve autorizzare separatamente l’uscita. |

`READY_FOR_PUBLICATION_REVIEW`: esempio di pubblicazione su carta, esterno ai valori enumerati eseguibili.

Fonte: `STATE_REGISTRY.json`; `python lab/examples/build_status_key.py`.
