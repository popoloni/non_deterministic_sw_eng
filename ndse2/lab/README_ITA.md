# Laboratorio complementare NDSE

Il laboratorio rende riproducibile il caso della Tesoreria. Parti dalla stessa richiesta di 4.000 EUR valutata con due versioni delle regole, poi esamina la ripetizione delle richieste storiche, i conflitti e i controlli dei capitoli successivi. Dati e attori sono sintetici; i programmi funzionano localmente e non richiedono credenziali.

## Da dove iniziare

Estrai l'archivio del laboratorio fornito con questa edizione. Apri un terminale nella directory che contiene `lab/`, `scripts/` e `series/`: questa è la **radice del laboratorio**. Tutti i comandi seguenti partono da lì, salvo indicazione di una directory diversa.

Il codice richiede **Python 3.10 o successivo** e usa soltanto la sua libreria standard. La verifica corrente è stata eseguita su Linux con **Python 3.12.14**. I test del mediatore di accesso ai file richiedono un filesystem che permetta collegamenti simbolici. I comandi di preparazione usano una shell POSIX; non occorre installare pacchetti tramite pip.

```sh
python3 --version
python3 -m venv --without-pip .venv
. .venv/bin/activate
python lab/examples/policy_boundary.py
```

Il primo esempio deve stampare:

```text
approval-eur-v1: AUTO_APPROVAL_ELIGIBLE
approval-eur-v2: REVIEW_REQUIRED
```

`amount_minor=400000` significa 4.000 EUR, espressi in centesimi interi. La richiesta ha rischio basso, appartiene alla Tesoreria e non è transfrontaliera. La soglia v1 è di 5.000 EUR; quella v2 è di 3.000 EUR. Il programma legge i file delle regole forniti e richiama il metodo recuperato `Policy.evaluate`.

Esegui il percorso locale completo:

```sh
python scripts/run_lab_checks.py
```

Il successo è indicato da `"passed": true`, con `"phases_passed": 3` e `"phases_total": 3`. Il rapporto dettagliato è `audit/current_run/LAB_CHECK_SUMMARY.json`. Le tre fasi eseguono i controlli del laboratorio, il primo esempio e la traccia esplicita del caso. Un codice di uscita diverso da zero indica il fallimento di una fase; il rapporto ne identifica il registro.

## Risultati da esaminare

| Risultato | Valore atteso | Dove esaminarlo |
|---|---:|---|
| Controlli di esecuzione del laboratorio | 20/20 | `audit/v10/companion_runs/RUN_SUMMARY.json` |
| Regressioni del servizio | 19 test | `audit/v10/companion_runs/service_regression_19.log` |
| Controlli comportamentali del capitolo 7 | 21/21 | `audit/v10/companion_runs/ch07.json` |
| Campagna reale con mutazioni isolate | 12 individuate, 0 sopravvissute, 0 errori d’infrastruttura | `audit/v10/companion_runs/ch07_mutations.json` |
| Campioni della relazione metamorfica | 2.184/2.184 coppie di importi | `audit/v10/companion_runs/ch07_relations.json` |
| Campioni del confronto differenziale | 168/168 casi | Stesso rapporto; confronto del solo stato |
| Controlli separati sulle identità | 3/3 | Stesso rapporto; ripetizione e nuove identità |
| Regressioni aggiuntive v10 | 47 test | `audit/v10/companion_runs/v10_composed_regressions.log` |
| Valutazioni storiche delle proposte | 3 pronte, 4 respinte | `audit/v10/companion_runs/ch11.json` |
| Ricontrollo esplicito con l'intenzione finale | 2 pronte, 5 respinte | `audit/case_trace/CH11_CASE_TIMELINE.json` |
| Ripetizione storica e due conflitti d'identità | Risposta originale v1 conservata; due eventi nel registro | `audit/case_trace/CANONICAL_CASE_TRACE.json` |

Le 19 regressioni del servizio e i 21 controlli comportamentali indipendenti sono insiemi di test diversi. I 47 test aggiuntivi esercitano gli esempi successivi dei controllori. Questi conteggi non vanno sommati e presentati come prove di ricerca indipendenti. Il confronto del capitolo 9 usa un piccolo insieme di casi predisposto dall'autore: nove domande riguardano il recupero di fonti e T10 riguarda un'astensione programmata. I risultati correnti per ciascun caso si trovano in `audit/v10/companion_runs/retrieval/`.

Le sette valutazioni del capitolo 11 sono eventi storici. A1 era pronta prima dell'arrivo di INT-002. Il secondo risultato esegue esplicitamente il controllo con la revisione finale: a quel punto sono pronte alla revisione umana soltanto B2 ed E2. Questo ricontrollo non implica che una persona abbia accettato o rilasciato il software.

## Eseguire il percorso di un capitolo

Ogni comando di questa sezione parte dalla radice del laboratorio. Gli script dei capitoli 3, 4, 5 e 7 accettano `--help`; un argomento obbligatorio assente o non valido produce le istruzioni d’uso e il codice di uscita 2.

### Capitoli 3–5: permessi, intenzione e architettura

```sh
python lab/companion/ch03/permission_bounded_surrogate.py lab/case_study audit/reader/ch03/trace.jsonl
python lab/companion/ch04/ccs_native_gate.py lab/case_study
python lab/companion/ch05/architecture_fitness_v2.py lab/case_study
```

Il capitolo 3 crea le directory di destinazione mancanti e registra quattro eventi, inclusi due dinieghi. `request_network` verifica un elenco vuoto di URL esatti consentiti. L’evento di rete registra `performed: false`: il programma non invia richieste. Il capitolo 4 produce otto controlli strutturali con `structural_status: PASS`, `authority_status: HUMAN_APPROVAL_UNVERIFIED` e `acceptance_status: NOT_ACCEPTED`. Il capitolo 5 riporta 19/19 controlli di adeguatezza architetturale, compresa l’individuazione dell’adattatore volutamente obsoleto usato come controllo negativo.

### Capitolo 7: attese indipendenti e mutazioni reali

```sh
python lab/companion/ch07/independent_oracle_lab.py lab/case_study
python lab/companion/ch07/mutation_runner.py lab/case_study
python lab/companion/ch07/relation_examples.py lab/case_study
```

L’oracolo riporta 21 controlli comportamentali. La campagna verifica prima la versione di riferimento e poi introduce un difetto identificato in ciascuna di 12 copie isolate. Il JSON conserva la modifica esatta, le impronte dei sorgenti, i nomi dei controlli falliti e l’esito. L’esecuzione di riferimento individua tutte le 12 mutazioni. Errori di sintassi o importazione, scadenze, risultati malformati e fallimenti della versione iniziale sono errori d’infrastruttura: non contano come mutazioni individuate. Le copie temporanee vengono rimosse al termine; i sorgenti del caso rimangono invariati. Per un solo difetto, aggiungi `--mutant M12_replay_appends_valid_chain_row`.

L’esempio di relazione mantiene fissi valuta, reparto, rischio, indicatore transfrontaliero, richiedente e policy, aumentando un importo intero positivo valido. Nessuna delle 2.184 coppie campionate passa da `REVIEW_REQUIRED` ad `AUTO_APPROVAL_ELIGIBLE`. I 168 casi differenziali confrontano **soltanto lo stato**: v1 e v2 differiscono esattamente per richieste domestiche della Tesoreria a rischio LOW, da 300.001 a 500.000 centesimi inclusi. L’output comprende i quattro estremi dell’intervallo e i controesempi con rischio HIGH, operazioni transfrontaliere, OPS e reparto sconosciuto. Sono campioni finiti. Le decisioni complete contengono anche la versione della policy. L’uso puro di `Policy.evaluate` evita lo stato delle ripetizioni; gli esperimenti sul servizio richiedono identificativi di transazione **e** chiavi nuovi. Tre controlli separati sulle identità mostrano perché la ripetizione storica ha un contratto proprio.

### Capitoli 9 e 11: recupero delle fonti, storia e coordinamento

```sh
python lab/companion/ch09/retrieval_handoff_agent.py lab/case_study lab/companion/ch09/holdout_questions.json audit/reader/retrieval
python lab/companion/ch11/multi_agent_governance.py
python scripts/build_case_trace.py
```

L’insieme di esempi del capitolo 9, predisposto dall’autore, riporta 6/10 successi nella modalità di base e 8/10 con memoria; ciascun totale comprende il caso di astensione programmata T10. Esamina `trial_results.csv` e `agent_traces.json`: i totali non misurano la comprensione. Il capitolo 11 stampa l’esito storico di 3 proposte pronte e 4 respinte. Il comando della traccia registra separatamente il ricontrollo alla revisione finale: 2 pronte e 5 respinte.

Il [protocollo proposto per verificare la comprensione](companion/ch09/FOLLOWUP_DESIGN_ITA.md) definisce nuovi compiti e una valutazione indipendente. Non è stato eseguito; i gruppi umani e di modelli previsti non compaiono nei risultati degli esempi.

Un **lease (assegnazione temporanea con scadenza)** associa un oggetto a un responsabile, una scadenza e una generazione. Il coordinatore sequenziale lo verifica quando ammette una proposta alla coda di revisione. Gli esiti usano ora in modo coerente `HOLD_WRONG_LEASE` e `HOLD_EXPIRED_LEASE`. `series/PUBLIC_PROJECTION.json` documenta la rinomina dello schema nella versione ancora inedita. L’ammissione alla coda non conferisce l’autorità di rilascio.

### Test del servizio e dei controllori

Esegui tutti i 47 test aggiuntivi dei controllori dalla radice:

```sh
python -m unittest discover -s lab/companion/v10 -v
```

Per le 19 regressioni originali del servizio, cambia esplicitamente directory:

```sh
cd lab/case_study
python -m unittest discover -s tests -q
cd ../..
```

Per un singolo modulo del controllore, usa la sua directory:

```sh
cd lab/companion/v10
python -m unittest test_control_state -v
python -m unittest test_measurement -v
python -m unittest test_coordination -v
cd ../../..
```

### Artefatti effettivi riportati nel libro

```sh
python lab/examples/build_reader_artifacts.py
```

Il comando esegue i controlli e scrive sette file in `audit/reader_artifacts/`. Le copie di riferimento sono in `lab/reader_artifacts/`: pacchetto dell’intenzione, insieme dei permessi e traccia, estratto dei controlli architetturali, registrazione delle prove, profilo dell’ambiente e schede di memoria versionate. La registrazione delle prove identifica impronte effettive dei sorgenti e comando eseguito; autenticazione e attestazione dell’esecuzione restano false. La decisione architetturale è in `lab/case_study/docs/03_architecture_decisions.md`. Le schede delle soglie versionate usano lo schema di `memory_scope.py`; la scheda più ampia per il recupero delle fonti resta in `docs/06_case_memory_card.json` dentro il caso.

## Che cosa offre ogni parte

| Capitolo | Materiale | Attività |
|---|---|---|
| 1 | `lab/case_study/docs/01_intent_contract.json` | Leggere i requisiti dichiarati e identificare le domande per il responsabile. |
| 2 | `lab/companion/v10/measurement.py` | Verificare le definizioni delle misure rispetto a un registro sintetico di eventi. |
| 3 | `lab/companion/ch03/` e `lab/companion/v10/control_state.py` | Esercitare limiti, riavvio, revoca e controlli sull'intenzione obsoleta. |
| 4 | `lab/companion/ch04/ccs_native_gate.py` | Esaminare i controlli strutturali e distinguerli da autorità e accettazione. |
| 5 | `lab/companion/ch05/` e `lab/companion/v10/schema_view.py` | Modificare una rappresentazione derivata preservando il comportamento delle regole e la ripetizione storica. |
| 6 | `lab/companion/v10/file_broker.py` | Provare operazioni locali sui file consentite e negate. |
| 7 | `lab/companion/ch07/independent_oracle_lab.py` | Derivare il comportamento atteso dal contratto e individuare difetti deliberati. |
| 8 | `lab/companion/v10/review_findings.json` | Classificare le osservazioni della revisione e scrivere un verdetto umano motivato. |
| 9 | `lab/companion/ch09/` e `lab/companion/v10/memory_scope.py` | Esaminare il recupero delle fonti e verificare una scheda di memoria versionata. |
| 10 | `lab/companion/ch10/` | Verificare il software del protocollo; lo studio con partecipanti resta un'attività proposta. |
| 11 | `lab/companion/ch11/` e `lab/companion/v10/coordination.py` | Esaminare gli eventi delle proposte e il coordinamento locale sequenziale. |
| 12 | `lab/companion/v10/whole_change_cost_worksheet.csv` | Calcolare costi illustrativi e decidere quali misure reali servirebbero. |
| 13 | Esercizio e soluzione nel libro | Revisionare una modifica documentale circoscritta; il laboratorio non esegue pubblicazioni. |

La classificazione dettagliata è in `lab/companion/v10/SCOPE_MATRIX.json`. I programmi di analisi rifiutano deliberatamente i modelli vuoti per il progetto pilota in produzione e per le valutazioni dei partecipanti. I test software non trasformano questi modelli in risultati osservati sul campo o sull'apprendimento. L'estensione sulla risposta persa nell'Appendice A è pseudocodice di progetto.

## Il caso condiviso e le sue versioni

`series/CASE_LEDGER.json` registra regole comuni, unità e identità. Questo file e `series/STATE_REGISTRY.json` sono proiezioni per il lettore: la storia della lavorazione editoriale è conservata fuori dalla distribuzione. Il registro comprende 20 famiglie operative. `series/READER_STATUS_KEY_ITA.md` è la guida sintetica generata dal registro; l’esempio di pubblicazione è un’espressione del testo, non un valore enumerato eseguibile. `series/STATE_REGISTRY.json` distingue decisioni applicative, esiti dei controllori, motivi, dichiarazioni di autorità e validità della memoria. `series/SCENARIO_ID_MAP.json` separa SCN-DATE, SCN-COORD e SCN-EVIDENCE dalle intenzioni canoniche INT-001/INT-002.

Il documento INT-001 distribuito è un contratto didattico consolidato: AC-002 confronta già v1 e v2. Va letto insieme alla modifica INT-002. Gli importi delle regole sono centesimi interi di EUR. Ripetere la stessa chiave e la stessa richiesta restituisce la risposta originale memorizzata; una nuova richiesta usa le regole attive. Riutilizzare un'identità in modo incoerente produce un conflitto.

## Se un risultato è diverso

Conserva il nome dell'archivio e il suo SHA-256, l'output di `python --version`, il sistema operativo, il comando esatto e la directory di esecuzione, oltre al registro del controllo fallito sotto `audit/`. Includi questi dati in una [segnalazione nel repository](https://github.com/popoloni/non_deterministic_sw_eng/issues). Il registro della pubblicazione identifica il codice distribuito; i vecchi registri di provenienza non sostituiscono i risultati della tua esecuzione.

Il blocco delle connessioni Python usato dal programma di test è un ausilio locale per le prove. Il mediatore di accesso ai file e il coordinatore illustrano controlli specifici in un solo processo; non implementano l'isolamento del sistema operativo, approvazioni autenticate o un servizio distribuito di produzione.

## Controlli sulle fonti del libro

Il [registro delle affermazioni](../evidence/REGISTER_ITA.md) identifica capitoli, codici delle fonti e versioni primarie consultate. Il registro pubblico contiene la provenienza documentale; il testo del libro e il registro editoriale completo restano nel pacchetto di produzione.
