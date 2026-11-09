# Publish the NDSE v13.7.3 R06 companion

**Handoff status: prepared locally; not published by this session.** The connected GitHub integration rejected `create_tree` with HTTP 403, `Resource not accessible by integration`. The prepared commit, tag and release have therefore not been published through that integration. A public download has not been verified.

This guide lets the repository owner publish the reviewed files using an account that already has the required repository access. It does not change permissions or bypass repository protections. If a command fails, stop and inspect its result. Use the repository’s normal review process if direct updates to `main` are restricted.

The commit adds `ndse2/` and updates the root README’s navigation. First-edition source files stay in place. The binary patch is supplied for inspection; the commands use the bundle to retain the exact prepared commit.

| Identity | Value |
|---|---|
| Repository | `popoloni/non_deterministic_sw_eng` |
| Required base | `be557958dbb94acd03f13e149d9cce90ce2e9c03` |
| Prepared commit | `de019b7e7659c3b227c44b491364268d2a04f6e0` |
| New tag, if unused | `v13.7.3` |
| Release asset | `NDSE_v13.7.3_Companion.zip` |

## 1. Set the paths and check the files

Use a POSIX shell and Python 3.10 or later, Git and the GitHub CLI. Keep the handoff package’s directory structure: the verifier is under `scripts/`, two levels above this `deliverables/publication/` directory. Replace the first path below with your absolute local path. Run subsequent blocks in the same shell so these variables remain available. `gh auth status` checks your normal GitHub CLI session; it does not repair or alter the blocked integration.

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

Verify all three frozen artifacts before importing the bundle:

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

| Frozen artifact | SHA-256 |
|---|---|
| `NDSE_R06_Companion_Publication.bundle` | `ec84ff599862e63e44edef2d57d68d440f50c5a1691a0fc2e62112c242f171e4` |
| `NDSE_R06_Companion_Publication.patch` | `b0a57cea3c40903d7292ca7f586916d4f348b54b28b582474c0c277055aabe48` |
| `NDSE_v13.7.3_Companion.zip` | `97a4032e107706a07ef1c1333c586aeb0492cbed1ce420f5f4f1d0376f2d78e1` |

`SHA256SUMS.txt` intentionally contains only the ZIP’s checksum, so the release contains a directly usable ZIP/checksum pair. The bundle and patch remain handoff artifacts.

## 2. Choose a repository checkout

For a fresh clone, use a new directory:

```sh
git clone https://github.com/popoloni/non_deterministic_sw_eng.git ndse-publication
cd ndse-publication
```

Or use an existing checkout:

```sh
cd /absolute/path/to/non_deterministic_sw_eng
```

The following checks require a clean working tree and the expected `origin`. They fetch `main`, update it only by fast-forward, verify the bundle’s prerequisite and import the prepared commit. This is an incremental bundle; it is not a standalone replacement for the repository’s earlier history.

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

If the required base is unavailable, use a normal fresh clone. If a fast-forward fails or the remote repository has diverged from the prepared commit, stop. Reconciliation would require a separately reviewed candidate and a new release identity; do not force, reset or rebase this frozen handoff.

## 3. Inspect the additive change

Review the file list and README diff. The final two commands reject deleted/renamed files and any change outside `README.md` and `ndse2/`.

```sh
git log --oneline "$NDSE_BASE..$NDSE_COMMIT"
git diff --stat "$NDSE_BASE" "$NDSE_COMMIT"
git diff --name-status "$NDSE_BASE" "$NDSE_COMMIT"
git diff "$NDSE_BASE" "$NDSE_COMMIT" -- README.md
test -z "$(git diff --diff-filter=DR --name-only "$NDSE_BASE" "$NDSE_COMMIT")"
git diff --exit-code "$NDSE_BASE" "$NDSE_COMMIT" -- . ':(exclude)README.md' ':(exclude)ndse2'
```

Proceed only after this is the change you intend to publish.

## 4. Fast-forward locally and run the laboratory

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

Expected result: `passed: true`, three of three phases, and 20 of 20 execution gates. Chapter 7 has 21 behavioral records, 12 killed mutants with zero survivors or infrastructure errors, 2,184 metamorphic sampled pairs, 168 differential cases and three separate identity controls. Historical governance remains 3 ready / 4 rejected; the final-revision recheck is 2 ready / 5 rejected.

The laboratory creates local reports under `ndse2/audit/`; leave them uncommitted. This procedure contains no `git add` or new commit step. The branch must still point to the exact prepared commit.

## 5. Publish main and create the unused tag

The block stops if `v13.7.3` already exists locally or remotely. Inspect an existing tag or release instead of deleting, moving or replacing it. A concurrent update or branch protection can also reject a push; stop at that point.

**The following commands write to GitHub when you run them.**

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

## 6. Create the release and upload the exact asset pair

This creates the release from the already pushed tag and uploads the original ZIP plus `SHA256SUMS.txt`. `--verify-tag` prevents automatic creation of a tag at an unintended commit. If the release already exists or upload is incomplete, inspect its state before taking another action; do not replace an asset with different bytes.

```sh
gh release create "$NDSE_TAG" \
  "$NDSE_HANDOFF/NDSE_v13.7.3_Companion.zip" \
  "$NDSE_HANDOFF/SHA256SUMS.txt" \
  --repo popoloni/non_deterministic_sw_eng \
  --verify-tag \
  --title "NDSE v13.7.3 — R06 companion" \
  --notes-file "$NDSE_HANDOFF/RELEASE_NOTES_EN_ITA.txt"
```

## 7. Close the anonymous public-access gate

Run the delivered verifier after the release is public:

```sh
python3 "$NDSE_VERIFIER" > ndse-public-verification.json
```

Success requires exit code 0, `status: PASS_PUBLIC_ACCESS_GATE` and `public_download_verified: true`. Preserve the JSON report with the release record.

The verifier uses anonymous HTTPS and the fixed release asset URL below. It checks the exact ZIP SHA-256, all 146 expected members, the 145-file source manifest, and the frozen executable hashes before running the documented laboratory entry point in a fresh temporary extraction. It then checks the expected results and confirms that source files remained unchanged. It performs no GitHub write and does not modify your repository; the shell redirection above saves its report in the current directory.

https://github.com/popoloni/non_deterministic_sw_eng/releases/download/v13.7.3/NDSE_v13.7.3_Companion.zip

An unavailable download, mismatched bytes, malformed manifest or failing laboratory leaves this gate open. The release asset must be the supplied ZIP; GitHub’s automatically generated source archives have a different layout and checksum.

An optional rehearsal uses the local archive:

```sh
python3 "$NDSE_VERIFIER" --local-archive "$NDSE_HANDOFF/NDSE_v13.7.3_Companion.zip"
```

That rehearsal reports `PASS_LOCAL_ONLY` and `public_download_verified: false`; it cannot establish public availability. Exit code 2 identifies download/environment problems, 3 an archive or manifest mismatch, and 4 a laboratory failure.

## Reference documentation

[Git bundle prerequisites and verification](https://git-scm.com/docs/git-bundle) · [Git fast-forward-only merge](https://git-scm.com/docs/git-merge) · [GitHub release creation and tag verification](https://cli.github.com/manual/gh_release_create).
