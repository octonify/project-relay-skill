# Master Handoff — Northwind Coffee brand refresh content workstream

Project: Northwind Coffee — brand refresh content workstream
Document Type: Master Handoff
Version: 1.0
Last Updated: 2026-07-30
Current Phase: Copy production and client sign-off, ahead of the 2026-09-01 brand launch
Overall Status: **At risk** — 3 of 10 tracked assets approved; the longest remaining page and two of three launch emails are blocked on client inputs; ~14 of 40 budget hours remain
Canonical File: `docs/handoffs/_master-handoff.md`
Prepared By: Aisha, 2026-07-30, on handover to Dan
Reader Note: This document is written for **Dan**, who is taking the account from Monday 2026-08-03 with no prior Northwind context, while Aisha is on leave. It stands alone — you do not need any chat history. Start at section 18 (New-Session Start Guide).

---

## 1. Executive Summary

**What the project is:** A content workstream refreshing all customer-facing copy for Northwind Coffee (12 cafes across Manchester and Leeds) for a new brand launching **2026-09-01**. Deliverables per `brief.md`: rewritten website copy (8 pages), 6 in-store printed cards, a 3-email launch sequence, and a tone-of-voice one-pager.

**Primary objective:** Every customer-facing asset rewritten, on-brand, and signed off in writing by the client before the 2026-09-01 launch.

**Current phase:** Mid-production. The tone-of-voice one-pager is locked, the homepage and store card 1 are approved (card 1 printed), and the remaining pages, cards, and emails are in draft, review, or blocked.

**Latest major progress:** Menu page rewrite finished 2026-07-30 and submitted to Marcus Bell for sign-off; about page founder story section drafted.

**Most important blocker:** The **sourcing page** cannot be written without the actual farm names from Northwind's ops team. Requested 2026-07-24 and 2026-07-29 — no reply either time. It is the longest page, it is due **2026-08-07**, and it is the acknowledged critical path item.

**Immediate next action:** Escalate the farm-names request to Marcus Bell (not to ops again), bundling three other outstanding client asks into the same email. Full detail in section 17.

---

## 2. Project Purpose and Definition

**Problem being solved:** Northwind Coffee is relaunching its brand on 2026-09-01. All existing customer-facing copy predates the new brand and is off-tone, so it must be rewritten to a single agreed voice before launch.

**Primary objective:** Deliver every listed asset, rewritten to the locked tone of voice, with written client sign-off.

**Intended final output (per `brief.md`):**
- Rewritten website copy — 8 pages
- 6 in-store printed cards
- Launch email sequence — 3 emails
- Tone-of-voice one-pager (delivered and locked)

**Users / stakeholders:**
- **Marcus Bell** — Marketing Lead, Northwind Coffee. Client contact and the **sole sign-off authority**.
- **Northwind ops team** — source of factual detail (farm names, founding year). Currently unresponsive.
- **Aisha** — lead copywriter and owner of the website pages, the emails, and the tone doc. On leave from 2026-08-03.
- **Dan** — acting owner for the week beginning 2026-08-03. No prior Northwind context.
- **Tom** — contributor, owner of the in-store store cards.
- End readers: Northwind's cafe customers in Manchester and Leeds.

**Success criteria:** All assets rewritten to the locked tone of voice; every published asset carries Marcus Bell's written sign-off; delivery complete before 2026-09-01; work delivered within 40 hours.

**Current scope:** The 10 assets tracked in `content-calendar.csv` — homepage, about page, menu page, sourcing page, store cards 1 and 2, emails 1–3, tone-of-voice one-pager.

**Out of scope / not evidenced as in scope:** Design, print production, email build and send, and website publishing are not mentioned in `brief.md` as this workstream's responsibility — this is a copy workstream. Do not take on layout, sending, or CMS publishing without asking. Note also the gap in section 13: `brief.md` promises 8 pages and 6 cards, but only 4 pages and 2 cards are tracked; the remaining 4 pages and 4 cards are **unaccounted for, not confirmed out of scope**.

---

## 3. Locked Principles and Decisions

- **Decision: Marcus Bell's written sign-off is mandatory before any copy is published. No exceptions.**
  - Rationale: A contract condition, imposed after a 2025 incident in which a price was published wrong.
  - Date: Set at engagement start; recorded in `brief.md`.
  - Status: **Locked / binding.**
  - Approval source: The engagement contract, via `brief.md`.
  - Practical effect: Verbal approval on a call is **not** sign-off. "In review with Marcus" is not "approved". The only approved assets are those with a recorded sign-off date in `content-calendar.csv`.

- **Decision: The tone of voice is locked as of 2026-07-18.**
  - Rationale: Approved by the client as a deliverable in its own right; it is the standard every other asset is reviewed against.
  - Date: 2026-07-18.
  - Status: **Locked.** Do not edit `tone-of-voice.md`.
  - Approval source: Client approval, recorded in `content-calendar.csv` (`tone-of-voice`, approved, "locked").
  - The rules, in full: warm, plain, specific; second person; short sentences; **never** use "artisanal", "curated", or "journey"; prices always written as **"GBP 3.20"**, never "3.20 GBP".

---

## 4. Project Structure

**Workstreams:** A single content workstream, split by asset type — website pages, in-store cards, launch emails, tone of voice.

**Repositories:** None. This is a content project with no code repository, no build, and no deployment pipeline. The project folder holds plain files only.

**Project folder contents:**
- `brief.md` — engagement brief
- `content-calendar.csv` — asset tracker
- `tone-of-voice.md` — locked style rules
- `session-notes.md` — Aisha's raw notes, 2026-07-30
- `docs/handoffs/` — this Master plus dated Daily Handoffs

**Systems / platforms:** A shared sheet is used for the tracker and budget (referenced in `brief.md` and `session-notes.md`); Northwind's live website is where published copy lands. **Neither has a link recorded in this folder** — see section 6.

**Ownership:**
| Asset | Owner |
|---|---|
| homepage, about-page, menu-page, sourcing-page | Aisha (Dan acting, w/c 2026-08-03) |
| store-card-1, store-card-2 | Tom |
| email-1-welcome, email-2-offer, email-3-loyalty | Aisha (Dan acting, w/c 2026-08-03) |
| tone-of-voice | Aisha (delivered, locked) |
| Sign-off on everything | Marcus Bell, client |

---

## 5. Architecture and Workflow

**Content architecture:** Assets are independent deliverables tracked one row per asset in `content-calendar.csv`, each with an owner, status, due date, and note. Due dates are staged backwards from the 2026-09-01 launch.

**Workflow:** Write draft → internal review against `tone-of-voice.md` → send to Marcus Bell → written sign-off → publish/print. Status values in use: `not started`, `draft`, `in review`, `approved`.

**Roles:** Aisha writes pages and emails and reviews Tom's cards. Tom drafts store cards. Marcus Bell approves everything. Northwind's ops team supplies factual detail. Dan holds the account for the week of 2026-08-03.

**Tools and integrations:** Email to the client; a shared sheet for tracking and budget. No automation, no CI, nothing that runs.

**Approval gates:**
1. **Internal tone check** against `tone-of-voice.md` before anything goes to the client. This gate is real — it caught two uses of the banned word "curated" in Tom's store card 2 draft on 2026-07-30.
2. **Marcus Bell's written sign-off** before publication. Hard gate, contract-level, no exceptions.

**Access restrictions / gaps:** Marcus Bell's and Northwind ops' contact details, the links to the copy assets themselves, and the shared tracker/budget sheet are **not recorded in this folder**. Dan must obtain them from Aisha before she leaves (2026-07-31 at the latest). This is the single most likely day-one blocker.

---

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| This Master Handoff | `docs/handoffs/_master-handoff.md` | Canonical project state and cold-start guide | Canonical for project state | Current as of 2026-07-30 |
| Engagement brief | `brief.md` | Scope, deliverables, client contact, sign-off condition, 40-hour budget | Canonical for scope and contract terms | Current |
| Tone of voice | `tone-of-voice.md` | Binding style rules | Canonical for style; **locked** | Approved 2026-07-18 |
| Asset tracker | `content-calendar.csv` | Per-asset owner, status, due date, notes | Canonical for asset status and due dates | Updated 2026-07-30 |
| Daily Handoff 2026-07-30 | `docs/handoffs/2026-07-30_001_northwind-copy-handoff.md` | What happened on 2026-07-30 | Authoritative for that session | Current |
| Aisha's raw notes | `session-notes.md` | Untidied source notes for 2026-07-30 | Supporting evidence only | Current |
| Northwind live website | URL not recorded | Currently published copy; source of the "2011" founding year | Reflects what is live, not what is correct | Live |
| Deck from Marcus | Not in this folder | Source of the "2009" founding year | Unverified | Conflicting — see section 13 |
| Shared tracker / budget sheet | Link not recorded — **get from Aisha** | Hours against the 40-hour budget | Canonical for budget | Not verified since ~2026-07-30 |
| Marcus Bell (client) | Contact details not recorded — **get from Aisha** | Sign-off, offer terms, factual confirmations | **Final authority on all client facts and approvals** | Unresponsive on the menu page since 2026-07-29 |

**Precedence when sources conflict:**
1. **Marcus Bell in writing** overrides everything. He is the sign-off authority and the arbiter of client facts.
2. `brief.md` overrides working assumptions on scope, budget, and process.
3. `tone-of-voice.md` overrides any stylistic preference in any draft, including a client-supplied one.
4. `content-calendar.csv` is authoritative for asset status and due dates over anyone's recollection.
5. The live website shows what is **published**, which is not the same as what is **correct** — it does not settle a factual dispute (see the founding-year contradiction, section 13).

---

## 7. Workstream Status

### Website copy (8 pages promised; 4 tracked)

Purpose: Rewrite Northwind's website copy for the new brand.
Owner: Aisha; **Dan acting from 2026-08-03**.
Current Status: **In Progress / partly Blocked.**
Completed: `homepage` — approved by Marcus 2026-07-24.
In Progress: `about-page` — founder story section written 2026-07-30, rest of page not written, founding year unresolved; due 2026-08-03. `menu-page` — rewrite finished, **Under Review** with Marcus since 2026-07-29; due 2026-07-31; no response.
Blocked: `sourcing-page` — not started; needs farm names from Northwind ops (asked 2026-07-24 and 2026-07-29, no reply); due 2026-08-07; **critical path**.
Open Decisions: Northwind's founding year — 2011 (live website) or 2009 (Marcus's deck). Draft currently uses 2011.
Dependencies: Northwind ops for farm names and the founding year; Marcus Bell for sign-off.
Next Action: Escalate the farm names to Marcus (section 17), then finish the about page, then draft everything on the sourcing page that does not depend on farm names.
Relevant Sources: `content-calendar.csv`, `tone-of-voice.md`, `docs/handoffs/2026-07-30_001_northwind-copy-handoff.md`.

### In-store printed cards (6 promised; 2 tracked)

Purpose: Printed cards for the 12 cafes.
Owner: Tom.
Current Status: **In Progress.**
Completed: `store-card-1` — approved 2026-07-22 and **already printed**.
In Progress: `store-card-2` — Tom's draft reviewed by Aisha on 2026-07-30; failed the tone check with two uses of the banned word "curated"; returned to Tom, **not yet fixed**; due 2026-08-05.
Blocked: Nothing blocked externally.
Open Decisions: None.
Dependencies: Tom to correct the draft; Marcus to sign off; print lead time (duration unknown — not recorded).
Next Action: Chase Tom for the corrected draft, re-check against `tone-of-voice.md`, then send to Marcus.
Relevant Sources: `content-calendar.csv`, `tone-of-voice.md`.

### Launch email sequence (3 emails)

Purpose: Three-email sequence supporting the 2026-09-01 launch.
Owner: Aisha; **Dan acting from 2026-08-03**.
Current Status: **Blocked** (2 of 3).
Completed: None.
In Progress: `email-1-welcome` — draft exists per the tracker; not worked on 2026-07-30; draft's state unverified; due 2026-08-10.
Blocked: `email-2-offer` — the offer amount is not agreed. Marcus said "probably 20% off first order" verbally on a call, nothing in writing; due 2026-08-12. `email-3-loyalty` — the loyalty scheme is being replaced in September and the new terms are not drafted, so there is nothing valid to write from; due 2026-08-14.
Open Decisions: The offer amount; the content or timing of email 3 given the loyalty change.
Dependencies: Marcus Bell for the offer in writing; Northwind for the new loyalty terms.
Next Action: Get the offer confirmed in writing (bundled into the escalation email, section 17) and raise email 3's dependency explicitly as a dated risk.
Relevant Sources: `content-calendar.csv`, `docs/handoffs/2026-07-30_001_northwind-copy-handoff.md`.

### Tone-of-voice one-pager

Purpose: The agreed voice every other asset is measured against.
Owner: Aisha.
Current Status: **Complete.** Approved 2026-07-18 and locked.
Next Action: None. Do not edit.
Relevant Sources: `tone-of-voice.md`.

---

## 8. Important Project History

- **2025 (date not recorded) —** A price was published wrong for Northwind. This is the origin of the mandatory written-sign-off condition in the contract. Without knowing this, the sign-off gate looks like bureaucracy; it is not, and it must not be shortcut.
- **2026-07-18 —** Tone-of-voice one-pager approved and **locked**. It became the internal review standard for every asset.
- **2026-07-22 —** `store-card-1` approved and **printed**. Printed output means changes are no longer free.
- **2026-07-24 —** `homepage` signed off by Marcus. First approved page; the model for the sign-off flow. Same day, the first request went to Northwind ops for the sourcing page's farm names.
- **2026-07-29 —** Menu page sent to Marcus for sign-off. Second request sent to Northwind ops for farm names. Neither has been answered.
- **2026-07-30 —** Menu page rewrite finished; about page founder story written; the **founding-year conflict** surfaced (website 2011 vs Marcus's deck 2009); the **loyalty scheme replacement** surfaced, invalidating the 2024 loyalty terms as a basis for email 3 after roughly an hour was spent that way; store card 2 reviewed and returned to Tom over banned-word use; tracker updated; budget reported at ~26 of 40 hours.
- **2026-08-03 (planned) —** Account passes to Dan for one week while Aisha is on leave.

---

## 9. Final Decisions

- Decision: Written sign-off from Marcus Bell before any publication, no exceptions.
  - Date: Engagement start.
  - Rationale: Contract condition following the 2025 wrong-price publication.
  - Impact: Nothing ships on verbal approval. Gates every asset.
  - Source: `brief.md`.
  - Supersedes: Any informal approval practice.

- Decision: Tone of voice locked 2026-07-18 — banned words "artisanal", "curated", "journey"; second person; short sentences; prices as "GBP 3.20".
  - Date: 2026-07-18.
  - Rationale: Client-approved deliverable and the review standard for all other assets.
  - Impact: Any draft breaching it is returned regardless of author. Applied to store card 2 on 2026-07-30.
  - Source: `tone-of-voice.md`; `content-calendar.csv`.
  - Supersedes: All pre-refresh Northwind copy style.

- Decision: Do not base email 3 on the 2024 loyalty terms.
  - Date: 2026-07-30.
  - Rationale: The loyalty scheme is being replaced in September; the 2024 terms will be wrong, and the new terms are not drafted.
  - Impact: Email 3 is blocked rather than in progress. Prevents a repeat of the hour already lost.
  - Source: Marcus, verbally, recorded in `session-notes.md`.
  - Supersedes: The initial plan to write email 3 from existing terms.

- Decision: Treat the "probably 20% off first order" offer as unconfirmed and do not draft against it.
  - Date: 2026-07-30.
  - Rationale: Verbal only. Publishing an unagreed figure is the exact failure class the sign-off rule exists to prevent.
  - Impact: Email 2 stays `not started` until written confirmation.
  - Source: `session-notes.md`.
  - Supersedes: Nothing.

---

## 10. Open Decisions

- Decision Needed: **Northwind's founding year — 2011 or 2009?**
  - Why It Matters: It is a factual claim in the about page founder story. Publishing it wrong is the same category of error as the 2025 price incident. The about page cannot go to sign-off with it unresolved.
  - Available Options: 2011 (currently on Northwind's live website, and the value used in the draft) or 2009 (the deck Marcus sent). Both came from Northwind's own ops team.
  - Required Evidence: Written confirmation from Marcus Bell or Northwind ops naming the correct year.
  - Decision Owner: Marcus Bell.
  - Deadline or Trigger: Before the about page goes for sign-off. Page due 2026-08-03.

- Decision Needed: **The email 2 offer amount.**
  - Why It Matters: Email 2 cannot be written without it. Due 2026-08-12.
  - Available Options: 20% off first order (Marcus's verbal suggestion) or something else.
  - Required Evidence: Marcus confirming the offer in writing.
  - Decision Owner: Marcus Bell.
  - Deadline or Trigger: Needs to land well before 2026-08-12 to leave writing and sign-off time.

- Decision Needed: **What email 3 says, given the loyalty scheme is being replaced in September.**
  - Why It Matters: Email 3 is due 2026-08-14 and there are no valid terms to write from. The answer may be to rescope or reschedule the email, not to write it.
  - Available Options: Wait for the new terms; write email 3 generically without terms; move email 3 after the September switchover; drop it from the launch sequence.
  - Required Evidence: The drafted new loyalty terms, or a client decision on rescoping.
  - Decision Owner: Marcus Bell, with Northwind's loyalty owner.
  - Deadline or Trigger: Raise immediately — this needs a decision, not a chase.

- Decision Needed: **Are the untracked deliverables still in scope — 4 further website pages and 4 further store cards?**
  - Why It Matters: `brief.md` promises 8 pages and 6 cards; `content-calendar.csv` tracks 4 and 2. With ~14 hours left of 40, the difference decides whether this engagement is nearly done or barely half done.
  - Available Options: They are tracked elsewhere; they are not yet scheduled; they were descoped without the brief being updated.
  - Required Evidence: Confirmation from Aisha, and if she cannot confirm, from Marcus against the contract.
  - Decision Owner: Aisha, then Marcus Bell.
  - Deadline or Trigger: Ask Aisha before she leaves (by 2026-07-31).

- Decision Needed: **Who covers the menu page on Friday 2026-07-31?**
  - Why It Matters: The menu page is due 2026-07-31, before Dan's Monday 2026-08-03 start. Aisha's notes say she is on leave "all next week" but do not say whether she works Friday.
  - Available Options: Aisha closes it Friday; it carries into Dan's week.
  - Required Evidence: Aisha confirming.
  - Decision Owner: Aisha.
  - Deadline or Trigger: Before end of 2026-07-30.

---

## 11. Changes Since the Previous Baseline

This is version 1.0 — the first Master Handoff for this project. There is no previous baseline. It consolidates `brief.md`, `content-calendar.csv`, `tone-of-voice.md`, and the 2026-07-30 Daily Handoff into one canonical document, created because the account is transferring to a contributor with no project history.

Future updates record their diff here.

---

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| 2024 Northwind loyalty terms (as a basis for email 3) | New loyalty terms — **not yet drafted** | Loyalty scheme is being replaced in September 2026; the 2024 terms will be wrong. An hour was lost writing against them. | 2026-07-30 |
| Pre-refresh Northwind copy style | `tone-of-voice.md` (locked 2026-07-18) | Superseded by the client-approved new brand voice | 2026-07-18 |
| Verbal client approval as a basis for publishing | Written sign-off from Marcus Bell | Contract condition after the 2025 wrong-price publication | Engagement start |

---

## 13. Contradictions and Resolution

- **Contradiction:** Northwind's founding year is given as both **2011** and **2009**.
  - Conflicting sources: Northwind's live website says 2011; the deck Marcus sent says 2009. Both trace back to Northwind's own ops team.
  - Verified current state: **Unresolved.** Nobody at Northwind has confirmed which is correct.
  - Authoritative source: Marcus Bell, in writing. The live website only proves what is published, not what is true.
  - Resolution: Provisionally using **2011** in the about page founder story, because it matches what is currently published and is therefore the lower-risk holding value.
  - Reason for precedence: Client facts are the client's to confirm; the sign-off authority is the arbiter.
  - Corrective action required: Get the year in writing before the about page goes for sign-off. If 2009 is correct, correct the founder story **and** check every other asset for the year — including the already-approved `homepage`, which has not been checked for it.

- **Contradiction:** `brief.md` promises **8 website pages and 6 in-store cards**; `content-calendar.csv` tracks only **4 pages** (homepage, about, menu, sourcing) and **2 store cards**.
  - Conflicting sources: `brief.md` (contract scope) vs `content-calendar.csv` (tracker).
  - Verified current state: **Unresolved.** Nothing in the project folder explains the gap. There is no evidence of a descope and no evidence of a second tracker.
  - Authoritative source: `brief.md` for contracted scope; Marcus Bell for any change to it.
  - Resolution: None yet. Treat the brief's numbers as the contracted commitment until told otherwise.
  - Reason for precedence: The brief records the engagement terms; a tracker can be incomplete without the terms changing.
  - Corrective action required: Ask Aisha before she leaves where the remaining 4 pages and 4 cards are tracked. If they are genuinely outstanding, the ~14 remaining hours will not cover them and that must be escalated immediately.

---

## 14. Risks, Constraints, and Dependencies

**Active risks:**
1. **Sourcing page misses 2026-08-07.** High impact (longest page, critical path, launch depends on complete signed-off website copy), high likelihood (input requested twice over six days with no reply, and the person chasing it is on leave). Mitigation: escalate to Marcus rather than ops; draft the non-farm-dependent copy in parallel.
2. **Email 3 cannot be written at all before 2026-08-14.** High impact (breaks the 3-email sequence), high likelihood (the new loyalty terms do not exist and depend on a September scheme change). Mitigation: raise as a decision, not a chase; propose rescoping or rescheduling.
3. **The founding-year error reaches published copy.** High impact (same failure class as the 2025 price incident), medium likelihood (flagged, but flags get lost across a handover). Mitigation: no about-page sign-off request without the year confirmed in writing.
4. **Budget overrun.** Medium-to-high impact, medium likelihood: ~14 of 40 hours remain against the largest remaining page, most of the about page, three emails, and remaining reviews — and the ~26-hour figure is itself unverified. Mitigation: reconcile against the shared sheet before starting new work; flag early.
5. **Handover context loss.** Medium-to-high impact, medium likelihood. Highest exposures are redoing the rejected 2024-loyalty-terms approach, publishing on a verbal, or editing the locked tone doc. Mitigation: this document plus section 18 point 6.
6. **Scope may be much larger than tracked** (see section 13). Impact potentially severe on both budget and timeline. Mitigation: resolve with Aisha before 2026-07-31.

**Constraints:**
- Written sign-off from Marcus Bell before any publication. Contract-level. No exceptions.
- Tone of voice locked 2026-07-18 — banned words "artisanal", "curated", "journey"; second person; short sentences; prices as "GBP 3.20", never "3.20 GBP".
- 40-hour budget; ~26 reported used, unverified.
- Launch date 2026-09-01 is fixed and drives every due date.
- Aisha unavailable all of the week beginning 2026-08-03; return date not recorded (likely 2026-08-10, unconfirmed).
- No repository, build, or deployment — plain files and email only. Nothing here to run or test.

**Dependencies:**
- **External — Northwind ops team:** farm names (blocking the sourcing page), founding-year confirmation. Unresponsive since 2026-07-24.
- **External — Marcus Bell:** menu page sign-off (outstanding since 2026-07-29), offer amount, founding year, all future sign-offs.
- **External — Northwind loyalty owner:** new loyalty terms, tied to a September scheme replacement.
- **Internal — Tom:** corrected store card 2 draft, due 2026-08-05.
- **Internal — Aisha:** contact details, asset links, tracker and budget sheet links, scope clarification. **Available only until she leaves.**

**Failure points:** Client responsiveness is the single biggest one — three of the four remaining major deliverables are blocked on a client input, and the escalation path (Marcus) is himself not currently replying.

---

## 15. Operational State

*(This project has no repository, branch, build, test suite, or deployment pipeline. The equivalent operational state is recorded below.)*

Repository / build / tests / CI / deployment: **None — not applicable.** Do not look for them.
Project folder: `D:\Projects\Skills\project-relay-workspace\iteration-1\eval-2-full-nontechnical-handover\with_skill\project`
Files present: `brief.md`, `content-calendar.csv`, `tone-of-voice.md`, `session-notes.md`, `docs/handoffs/`
**Published / live:** `homepage` copy approved 2026-07-24 (whether it is live on the website is **not verified**). Northwind's live website currently states founding year 2011.
**Printed:** `store-card-1` — printed. Changes to it now carry a reprint cost.
**With the client:** `menu-page`, awaiting Marcus's sign-off since 2026-07-29.
**Scheduled sends:** None. No launch email has been built or scheduled; all three are copy-stage only.
**Copy assets:** The page and email copy documents themselves are **not in this folder** — only the brief, tracker, tone doc, and notes. Their location must be obtained from Aisha.
**Tracker:** `content-calendar.csv` updated 2026-07-30 and consistent with `session-notes.md`. Whether the separate shared sheet referenced in `brief.md` is the same artifact is unverified.
**Budget standing:** ~26 of 40 hours used per Aisha's estimate; **not formally reconciled**.
**Account standing:** Active engagement, launch 2026-09-01, client currently unresponsive on two open requests.

---

## 16. Current Project State

**Current phase:** Copy production with client sign-off gating, four to five weeks from launch.

**Latest approved output:** `homepage`, signed off by Marcus Bell 2026-07-24.

**Active work:** `about-page` (founder story written, rest outstanding, due 2026-08-03); `email-1-welcome` (draft exists, state unverified).

**Completed work (approved):** `tone-of-voice` (2026-07-18, locked); `store-card-1` (2026-07-22, printed); `homepage` (2026-07-24).

**Awaiting client:** `menu-page` — with Marcus since 2026-07-29, due 2026-07-31.

**Incomplete:** `store-card-2` — reviewed, failed the tone check, back with Tom, due 2026-08-05.

**Blockers:**
- `sourcing-page` — no farm names. Due 2026-08-07. Critical path.
- `email-2-offer` — offer not agreed in writing. Due 2026-08-12.
- `email-3-loyalty` — new loyalty terms do not exist. Due 2026-08-14.

**Open decisions:** Founding year; offer amount; email 3's content or timing; whether the untracked 4 pages and 4 cards are in scope; Friday 2026-07-31 cover for the menu page.

**Readiness for next phase:** **Not ready.** Website copy cannot be declared complete while the sourcing page is unwritten, and the email sequence cannot be completed while two of three emails are blocked on client decisions.

**Overall status:** **At risk.** 3 of 10 tracked assets approved. Every remaining critical item depends on a client who has not replied to two requests, ~14 of 40 hours remain, and the account owner is on leave for the week.

---

## 17. Immediate Next Action

Immediate Next Action: Send Marcus Bell one escalation email that (1) escalates the missing **farm names** for the sourcing page, (2) asks him to confirm the **founding year — 2011 or 2009**, (3) requests his **written sign-off on the menu page**, and (4) asks him to **confirm the email 2 offer in writing**. Then record the escalation date in the `sourcing-page` note in the tracker.
Responsible Role or Agent: Dan, acting owner, Monday 2026-08-03, first task of the day.
Start From: This document, then `docs/handoffs/2026-07-30_001_northwind-copy-handoff.md`, then the `sourcing-page` row of `content-calendar.csv`.
Required Inputs: Marcus Bell's email address (**get from Aisha before 2026-07-31**); the dates Northwind ops were already asked — 2026-07-24 and 2026-07-29; the sourcing page due date 2026-08-07.
Expected Deliverable: One sent email with four separately numbered asks and a named response deadline, plus the tracker updated with the escalation date.
Acceptance Criteria: The email states that the sourcing page is the critical path item due 2026-08-07; states that Northwind ops were asked on 2026-07-24 and 2026-07-29 with no reply; asks for the farm names by a named date (2026-08-04, leaving three working days to write the page); and separates the four asks so none is lost in a partial reply.
Dependencies: Marcus Bell's contact details from Aisha. If Marcus is also away, ask for a named Northwind ops contact who can supply the farm names directly.
Stop Conditions: If the farm names have not arrived by 2026-08-05, stop treating this as a chase and escalate it as a schedule risk to the 2026-09-01 launch — the sourcing page will not be written and signed off in time.
Do Not Change: Do not send a third identical request to Northwind ops — that channel has failed twice. Do not change the about page founding year to 2009 without written confirmation. Do not edit `tone-of-voice.md`. Do not rewrite the menu page while it is under review with Marcus. Do not publish anything, ever, without Marcus's written sign-off.

**Prioritized queue after that:**
1. Finish the `about-page` beyond the founder story section — due Monday 2026-08-03, Dan's first day. Do not send it for sign-off until the founding year is confirmed.
2. Draft the `sourcing-page` structure and all copy that does not depend on farm names, with clearly marked placeholders, so it is one edit from complete when the names arrive.
3. Chase Tom for the corrected `store-card-2` draft (due 2026-08-05); re-check it against `tone-of-voice.md` before it goes to Marcus.
4. Raise **email 3** with Marcus as a decision, not a chase: the new loyalty terms do not exist, so ask whether email 3 should be rescoped or moved past the September switchover.
5. Reconcile hours against the shared budget sheet; flag immediately if the remaining ~14 hours do not cover the remaining scope.
6. Resolve the scope gap in section 13 — 8 pages vs 4 tracked, 6 cards vs 2 tracked — with Aisha before she leaves.

---

## 18. New-Session Start Guide

1. **Read first, in this order:** this Master (`docs/handoffs/_master-handoff.md`) → `brief.md` → `tone-of-voice.md` → `content-calendar.csv` → `docs/handoffs/2026-07-30_001_northwind-copy-handoff.md`. `session-notes.md` is Aisha's raw notes and is supporting evidence only.
2. **Canonical source:** this Master for project state; `brief.md` for scope and contract terms; `tone-of-voice.md` for style; `content-calendar.csv` for asset status and due dates. **Marcus Bell in writing overrides all of them.**
3. **Current state:** mid-production, **at risk**. Approved: tone of voice (locked), store card 1 (printed), homepage. With the client: menu page. In draft: about page (partly written), store card 2 (Tom, failed tone check), email 1. Blocked: sourcing page (farm names), email 2 (offer not agreed), email 3 (loyalty terms do not exist). ~14 of 40 hours remain, unverified.
4. **Start here:** section 17 — the escalation email to Marcus Bell, first task Monday 2026-08-03. Then the queue below it.
5. **Final decisions (do not reopen):** written sign-off from Marcus before any publication; the tone of voice locked 2026-07-18, including the banned words "artisanal", "curated", "journey" and the "GBP 3.20" price format; email 3 is not to be built on the 2024 loyalty terms; the "20% off" offer is unconfirmed until it is in writing.
6. **Do not repeat:**
   - Do not build email 3 on the 2024 loyalty terms — an hour was already lost there; the scheme is being replaced in September.
   - Do not send a third identical farm-names request to Northwind ops — two attempts (2026-07-24, 2026-07-29) went unanswered; escalate to Marcus instead.
   - Do not re-review the current store card 2 draft — already reviewed 2026-07-30; the finding is two uses of "curated"; review Tom's corrected version instead.
   - Do not rewrite the menu page — finished and under review with Marcus since 2026-07-29.
   - Do not reopen the tone of voice, the homepage, or store card 1 — all approved; store card 1 is already printed.
   - Do not treat 2011 as a verified founding year, and do not switch to 2009 without written confirmation.
7. **Access required (get from Aisha before she leaves on 2026-07-31):** Marcus Bell's email address; a Northwind ops contact; links to the page and email copy documents (they are **not** in this folder); links to the shared tracker sheet and the shared budget sheet; Tom's contact details; and confirmation of where the remaining brief deliverables are tracked.
8. **Requires explicit human approval — never do these on your own initiative:**
   - **Publishing or printing any copy.** Marcus Bell's **written** sign-off is required first, without exception. This is a contract condition following a 2025 incident where a price was published wrong.
   - **Stating any offer, discount, or price** in copy. The "20% off first order" figure is verbal only and unconfirmed. Prices must also follow the locked format: "GBP 3.20".
   - **Stating the founding year, farm names, or any other Northwind fact** that is not confirmed in writing. Use a marked placeholder instead.
   - **Changing scope, due dates, or budget**, including agreeing to move a deliverable — that is Marcus's call, with Aisha informed.
   - **Reprinting or amending store card 1**, which is already printed and approved.

---

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-30 | `docs/handoffs/2026-07-30_001_northwind-copy-handoff.md` | Menu page completion, about page founder story, sourcing/email blockers, tracker update, handover to Dan | Yes — v1.0, 2026-07-30 |
