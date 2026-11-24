# ExamArchive verification queue

Staged question papers from the ExamArchive FYUG OCR sweep, waiting for a
human (with an AI helper) to check them against the original page photos
before they go live on examarchive.dev.

**This repo is public, but its paper files are encrypted with git-crypt.**
Anyone can clone it; only people with the key can read the papers. Get the
key from Om (WhatsApp). Never post the key anywhere public, and never commit
it to this repo. If the key leaks, tell Om — he will rotate it and
re-encrypt everything.

## Trial set: 10 papers

| Paper | Year | Rows | Marks | Notes |
|---|---|---|---|---|
| HISDSC303T | 2025 | 25 | 70/70 | Clean |
| PHIDSC102T | 2023 | 25 | 70/70 | Clean |
| BOTDSC101T | 2023 | 25 | 70/70 | Clean |
| ENGDSC101T | 2023 | 25 | 70/70 | Clean |
| COMDSC-102T | 2023 | 29 | 70/70 | Clean |
| ENGAEC251 (Science) | 2025 | 37 | 46/50 | Split-marks gap on the (a)-(j) sub-rows |
| BNGSEC101T | 2025 | 40 | 47/50 | 3 marks short |
| COMIDC-101T (B) | 2023 | 46 | 70/70 | Q40 text + Q41 stem cut off in the photo — source gap, do not guess |
| MTMDSM301 | 2025 | 40 | 69/70 | 1 mark short |
| ZOODSM101T | 2023 | 25 | 70/70 | Q18 tail cut off in the photo — source gap, do not guess |

Each paper folder has `staged.md` (the paper: details, full question text,
question table), `report.json` (machine checks), and `pages/pg-N.png`
(the original page photos — the ground truth).

## Setup (once)

1. Install git and git-crypt.
   - macOS: `brew install git git-crypt`
   - Ubuntu/Debian: `sudo apt install git git-crypt`
   - Windows: install Git for Windows, then git-crypt from its releases
     (or `choco install git-crypt`).
2. Clone: `git clone https://github.com/Omdas11/examarchive-verification.git`
3. Get the key file from Om on WhatsApp and save it somewhere safe
   **outside** this repo, e.g. `~/examarchive-key`.
4. Unlock: `cd examarchive-verification && git-crypt unlock ~/examarchive-key`
   After this, the paper files read normally. They are still encrypted in
   git — encryption happens automatically when you commit.
5. Check it worked: `cat papers/HISDSC303T-2025/staged.md` should show a
   readable question paper. If it shows garbage, the unlock did not work.

## How to verify one paper

1. **Claim it first.** Say in the WhatsApp group which paper you are
   taking, so two people never verify the same paper at once.
2. Open `papers/<CODE>-<YEAR>/staged.md` and the photos in
   `papers/<CODE>-<YEAR>/pages/`. Read the photos, not the md — the md is
   what you are checking.
3. Work through the paper with Antigravity (or by hand): compare every
   question, every figure and every mark against the photo. Fix what the
   photo proves wrong, in `staged.md` — both the question text AND the
   question table row, so they stay in sync.
4. Rules:
   - Never guess text the photo hides. If a word, number or figure is cut
     off, covered or unreadable in the photo, leave it as `[illegible]`.
     Do not invent it, even if you can guess it.
   - Do not "correct" the paper's own misprints. If the paper prints a
     wrong spelling or a wrong number, keep it as printed. (The paper is
     the truth; the md must match the paper, not the textbook.)
   - Marks in the table must add up to the paper's full marks, following
     the section instructions (e.g. "Answer any 5" counts each answered
     question once). If they do not add up, say so in your commit message
     instead of forcing the total.
   - Keep the `★★★` end mark at the end of the last question if the
     photo shows it.
5. Commit and push:
   - `git add papers/<CODE>-<YEAR>/staged.md`
   - `git commit -m "verify: <CODE>-<YEAR> - <what you changed>"`
     e.g. `verify: HISDSC303T-2025 - fixed Q7 wording, Q12 figure 4->5`
   - `git push`
   - If the push is rejected because someone else pushed first, run
     `git pull --rebase` and push again. Never force-push.
6. Say in the WhatsApp group that the paper is done.

A paper is **done** when: the md matches the photos question for
question, the marks add up to full marks, and `[illegible]` appears only
where the photo truly hides something.

## Safety

- Never commit the key file. It is gitignored, but check `git status`
  before every commit — if you see a key file listed, do not commit it.
- Never paste paper content into a public place (issue, comment, chat
  outside the group). The papers are encrypted here for a reason.
- If you lose the key file, ask Om for it again. If the key ever leaks
  publicly, tell Om at once.

## Scale note

This trial is 10 papers (33 MB, mostly page photos). At 400 papers the
photos will not live in git — they will move to object storage and this
repo will keep the md files only. Do not add more papers to this repo
without checking with Om first.
