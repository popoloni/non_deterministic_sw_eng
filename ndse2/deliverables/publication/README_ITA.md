# Pubblicare il laboratorio NDSE v13.7.3 R06

**Stato del pacchetto: preparato localmente; non pubblicato in questa sessione.** L’integrazione GitHub collegata ha rifiutato l’operazione `create_tree` con HTTP 403 e il messaggio `Resource not accessible by integration`: la risorsa non è accessibile tramite quell’integrazione. Il commit preparato, il tag e la release non sono quindi stati pubblicati attraverso tale collegamento. Non è stato verificato un download pubblico.

Questa guida permette al responsabile del repository di pubblicare i file verificati con un account che disponga già degli accessi necessari. Non modifica i permessi né aggira le protezioni del repository. Se un comando fallisce, fermati ed esamina l’esito. Se gli aggiornamenti diretti a `main` sono limitati, segui il normale processo di revisione del repository.

Il commit aggiunge `ndse2/` e aggiorna la navigazione nel README principale. I sorgenti della prima edizione restano al loro posto. La patch binaria è fornita per l’ispezione; i comandi usano il bundle per conservare esattamente il commit preparato.

| Identità | Valore |
|---|---|
| Repository | `popoloni/non_deterministic_sw_eng` |
| Base richiesta | `be557958dbb94acd03f13e149d9cce90ce2e9c03` |
| Commit preparato | `de019b7e7659c3b227c44b491364268d2a04f6e0` |
| Nuovo tag, se libero | `v13.7.3` |
| Archivio della release | `NDSE_v13.7.3_Companion.zip` |

## 1. Impostare i percorsi e controllare i file

Servono una shell POSIX, Python 3.10 o successivo, Git e l’interfaccia da riga di comando di GitHub. Conserva la struttura del pacchetto: il verificatore è in `scripts/`, due livelli sopra questa directory `deliverables/publication/`. Sostituisci il primo percorso seguente con il tuo percorso locale assoluto. Esegui i blocchi successivi nella stessa shell, per mantenere disponibili le variabili. `gh auth status` controlla la normale sessione della riga di comando di GitHub; non ripara né modifica l’integrazione bloccata.

```sh
set -eu
NDSE_HANDOFF="/absolute/path/to/deliverables/publication"
NDSE_VERIFIER="$NDSE_HANDOFF/../../scripts/verify_public_companion.py"
NDSE_BASE="be557958dbb94acd03f13e149d9cce90ce2e9c03"
NDSE_COMMIT="de019b7e7659c3b227c44b491364268d2a04f6e0"
NDSE_TAG="v13.7.3"
test -f "$NDSE_VERIFIER"
python3 --version
git --version
gh auth status
```

Verifica i tre artefatti congelati prima di importare il bundle:

```sh
python3 - "$NDSE_HANDOFF" <<'PY_CHECK'
from pathlib import Path
import hashlib
import sys
root = Path(sys.argv[1])
expected = {'NDSE_R06_Companion_Publication.bundle': 'ec84ff599862e63e44edef2d57d68d440f50c5a1691a0fc2e62112c242f171e4',
 'NDSE_R06_Companion_Publication.patch': 'b0a57cea3c40903d7292ca7f586916d4f348b54b28b582474c0c277055aabe48',
 'NDSE_v13.7.3_Companion.zip': '97a4032e107706a07ef1c1333c586aeb0492cbed1ce420f5f4f1d0376f2d78e1'}
for name, wanted in expected.items():
    actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
    if actual != wanted:
        raise SystemExit("SHA256 mismatch: " + name)
    print("OK", name, actual)
PY_CHECK
```

| Artefatto congelato | SHA-256 |
|---|---|
| `NDSE_R06_Companion_Publication.bundle` | `ec84ff599862e63e44edef2d57d68d440f50c5a1691a0fc2e62112c242f171e4` |
| `NDSE_R06_Companion_Publication.patch` | `b0a57cea3c40903d7292ca7f586916d4f348b54b28b582474c0c277055aabe48` |
| `NDSE_v13.7.3_Companion.zip` | `97a4032e107706a07ef1c1333c586aeb0492cbed1ce420f5f4f1d0376f2d78e1` |

`SHA256SUMS.txt` contiene intenzionalmente soltanto l’impronta dello ZIP: la release offrirà così una coppia archivio/checksum direttamente verificabile. Bundle e patch restano artefatti del pacchetto di consegna.

## 2. Scegliere la copia del repository

Per una nuova clonazione, usa una directory nuova:

```sh
git clone https://github.com/popoloni/non_deterministic_sw_eng.git ndse-publication
cd ndse-publication
```

In alternativa, usa una copia già esistente:

```sh
cd /absolute/path/to/non_deterministic_sw_eng
```

I controlli seguenti richiedono una copia di lavoro pulita e l’`origin` previsto. Recuperano `main`, lo aggiornano soltanto per avanzamento diretto, verificano il prerequisito del bundle e importano il commit preparato. Il bundle è incrementale: non sostituisce autonomamente la storia precedente del repository.

```sh
test -z "$(git status --porcelain)"
case "$(git remote get-url origin)" in
  https://github.com/popoloni/non_deterministic_sw_eng|https://github.com/popoloni/non_deterministic_sw_eng.git|git@github.com:popoloni/non_deterministic_sw_eng.git|ssh://git@github.com/popoloni/non_deterministic_sw_eng.git) ;;
  *) exit 1 ;;
esac
git fetch --no-tags origin main
git switch main
git merge --ff-only origin/main
git cat-file -e "$NDSE_BASE^{commit}"
git bundle verify "$NDSE_HANDOFF/NDSE_R06_Companion_Publication.bundle"
git fetch --no-tags "$NDSE_HANDOFF/NDSE_R06_Companion_Publication.bundle" refs/heads/ndse2-r06-v13.7.3
test "$(git rev-parse FETCH_HEAD)" = "$NDSE_COMMIT"
test "$(git rev-parse "$NDSE_COMMIT^")" = "$NDSE_BASE"
```

Se manca la base richiesta, usa una normale clonazione completa. Se l’avanzamento diretto fallisce o il repository remoto è cambiato in modo incompatibile con il commit preparato, fermati. La riconciliazione richiederebbe una candidata verificata separatamente e una nuova identità di rilascio; non forzare, azzerare o riscrivere questo pacchetto congelato.

## 3. Esaminare le aggiunte

Esamina l’elenco dei file e le differenze nel README. Gli ultimi due comandi rifiutano eliminazioni o rinomine e qualsiasi modifica esterna a `README.md` e `ndse2/`.

```sh
git log --oneline "$NDSE_BASE..$NDSE_COMMIT"
git diff --stat "$NDSE_BASE" "$NDSE_COMMIT"
git diff --name-status "$NDSE_BASE" "$NDSE_COMMIT"
git diff "$NDSE_BASE" "$NDSE_COMMIT" -- README.md
test -z "$(git diff --diff-filter=DR --name-only "$NDSE_BASE" "$NDSE_COMMIT")"
git diff --exit-code "$NDSE_BASE" "$NDSE_COMMIT" -- . ':(exclude)README.md' ':(exclude)ndse2'
```

Prosegui soltanto dopo aver verificato che questa sia la modifica che vuoi pubblicare.

## 4. Integrare localmente ed eseguire il laboratorio

```sh
git merge --ff-only "$NDSE_COMMIT"
test "$(git rev-parse HEAD)" = "$NDSE_COMMIT"
(
  cd ndse2
  python3 scripts/run_lab_checks.py
)
git diff --exit-code
git diff --cached --exit-code
```

L’esito atteso è `passed: true`, con tre fasi superate su tre e 20 controlli di esecuzione superati su 20. Il capitolo 7 comprende 21 controlli comportamentali, 12 mutazioni individuate senza sopravvissute o errori d’infrastruttura, 2.184 coppie campionate per la relazione metamorfica, 168 casi differenziali e tre controlli separati sulle identità. La governance storica resta a 3 proposte pronte e 4 respinte; il ricontrollo finale ne dà 2 pronte e 5 respinte.

Il laboratorio crea rapporti locali sotto `ndse2/audit/`: lasciali fuori dai commit. La procedura non contiene passaggi `git add` né la creazione di un nuovo commit. Il ramo deve continuare a indicare esattamente il commit preparato.

## 5. Pubblicare main e creare il tag libero

Il blocco si interrompe se `v13.7.3` esiste già localmente o sul remoto. In tal caso esamina il tag o la release esistenti, senza eliminarli, spostarli o sostituirli. Anche un aggiornamento concorrente o una protezione del ramo può rifiutare l’invio: fermati a quel punto.

**I comandi seguenti scrivono su GitHub quando li esegui.**

```sh
if git show-ref --verify --quiet "refs/tags/$NDSE_TAG"; then
  exit 1
fi
NDSE_REMOTE_TAGS="$(git ls-remote --tags origin "refs/tags/$NDSE_TAG" "refs/tags/$NDSE_TAG^{}")"
test -z "$NDSE_REMOTE_TAGS"
test "$(git branch --show-current)" = "main"
test "$(git rev-parse HEAD)" = "$NDSE_COMMIT"
git push origin main
git tag -a "$NDSE_TAG" "$NDSE_COMMIT" -m "NDSE v13.7.3 R06 companion"
git push origin "refs/tags/$NDSE_TAG"
NDSE_TAG_REMOTE="$(git ls-remote --tags origin "refs/tags/$NDSE_TAG^{}")"
test "$(printf '%s\n' "$NDSE_TAG_REMOTE" | awk '{print $1}')" = "$NDSE_COMMIT"
```

## 6. Creare la release e caricare la coppia esatta di file

Il comando crea la release dal tag già inviato e carica lo ZIP originale insieme a `SHA256SUMS.txt`. L’opzione `--verify-tag` impedisce la creazione automatica di un tag su un commit non previsto. Se la release esiste già o il caricamento è incompleto, esamina lo stato prima di procedere; non sostituire un allegato con contenuti diversi.

```sh
gh release create "$NDSE_TAG" \
  "$NDSE_HANDOFF/NDSE_v13.7.3_Companion.zip" \
  "$NDSE_HANDOFF/SHA256SUMS.txt" \
  --repo popoloni/non_deterministic_sw_eng \
  --verify-tag \
  --title "NDSE v13.7.3 — R06 companion" \
  --notes-file "$NDSE_HANDOFF/RELEASE_NOTES_EN_ITA.txt"
```

## 7. Completare la verifica dell’accesso pubblico anonimo

Dopo aver reso pubblica la release, esegui il verificatore consegnato:

```sh
python3 "$NDSE_VERIFIER" > ndse-public-verification.json
```

Il successo richiede il codice di uscita 0, `status: PASS_PUBLIC_ACCESS_GATE` e `public_download_verified: true`. Conserva il rapporto JSON insieme al registro del rilascio.

Il verificatore usa HTTPS senza autenticazione e l’URL fisso riportato sotto. Controlla l’impronta esatta dello ZIP, tutti i 146 elementi attesi, il manifesto dei 145 file sorgente e le impronte degli eseguibili congelati prima di avviare il punto d’ingresso documentato del laboratorio in una nuova directory temporanea. Controlla quindi i risultati attesi e verifica che i sorgenti siano rimasti invariati. Non scrive su GitHub e non modifica il repository; il reindirizzamento della shell mostrato sopra salva il rapporto nella directory corrente.

https://github.com/popoloni/non_deterministic_sw_eng/releases/download/v13.7.3/NDSE_v13.7.3_Companion.zip

Un download non disponibile, contenuti diversi, un manifesto malformato o il fallimento del laboratorio lasciano il controllo incompleto. L’allegato della release deve essere lo ZIP fornito: gli archivi dei sorgenti generati automaticamente da GitHub hanno struttura e impronta diverse.

Puoi fare una prova facoltativa con l’archivio locale:

```sh
python3 "$NDSE_VERIFIER" --local-archive "$NDSE_HANDOFF/NDSE_v13.7.3_Companion.zip"
```

Questa prova restituisce `PASS_LOCAL_ONLY` e `public_download_verified: false`: non può dimostrare la disponibilità pubblica. Il codice di uscita 2 indica problemi di download o ambiente, il 3 una difformità nell’archivio o nel manifesto e il 4 un fallimento del laboratorio.

## Documentazione di riferimento

[Prerequisiti e verifica dei bundle Git](https://git-scm.com/docs/git-bundle) · [Integrazione Git con solo avanzamento diretto](https://git-scm.com/docs/git-merge) · [Creazione delle release e verifica del tag in GitHub](https://cli.github.com/manual/gh_release_create).
