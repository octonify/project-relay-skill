# Master Handoff — Northwind Coffee brand refresh content

Project: Northwind Coffee — brand refresh content workstream
Document Type: Master Handoff
Version: 1.0
Last Updated: 2026-07-30
Current Phase: Mid-delivery — copy production and client sign-off, ahead of the 2026-09-01 brand launch
Overall Status: At risk. Three of the remaining deliverables are blocked on the client, the critical-path page has not started, and the account is changing hands for a week.
Canonical File: `docs/handoffs/_master-handoff.md`

> **If you are Dan and it is Monday 3 August 2026, read this document top to bottom before doing
> anything. It is written for someone who has never worked on this account. Section 18 tells you
> exactly what to do first. Section 17 is the one action to take before anything else.**

---

## 1. Executive Summary

**What the project is:** A content workstream for Northwind Coffee, a 12-cafe chain across Manchester and Leeds. We are rewriting all their customer-facing copy for a brand refresh that launches on **2026-09-01**.

**Primary objective:** Deliver rewritten website copy, in-store printed cards, a three-email launch sequence, and a tone-of-voice one-pager — all signed off in writing by the client before the launch date.

**Current phase:** Mid-delivery. Three items are approved (homepage, store card 1, tone of voice). One is with the client for review (menu page). One is in draft (about page). Four are not started, three of them because the client has not given us information or a decision.

**Latest major progress:** On 2026-07-30 the menu page rewrite was finished and the About page founder story section was written.

**Most important blocker:** The **sourcing page** cannot start because Northwind's ops team has not supplied the actual farm names. They were asked on 2026-07-24 and again on 2026-07-29 and have not replied. It is the longest page, it is due **2026-08-07**, and it is the critical path.

**Immediate next action:** Escalate to Marcus Bell in one written email covering the farm names, the founding year, the offer amount, and the menu page sign-off. Full detail in section 17.

**Ownership right now:** Aisha ran this account and is on leave for the week beginning 2026-08-03. **Dan is covering that week and has never worked on Northwind before.** Assume Aisha is unreachable.

---

## 2. Project Purpose and Definition

**Problem being solved:** Northwind Coffee is relaunching its brand on 2026-09-01. Every piece of customer-facing copy — website, in-store, email — has to be rewritten to match the new brand before that date.

**Primary objective:** Produce and get written client sign-off on all customer-facing copy for the new brand, within 40 hours of budget, before 2026-09-01.

**Intended final output:**
- Rewritten website copy — **8 pages** per `brief.md` (only 4 are tracked; see section 13)
- **6** in-store printed cards per `brief.md` (only 2 are tracked; see section 13)
- Launch email sequence — 3 emails
- Tone-of-voice one-pager — **delivered and approved**

**Users / stakeholders:**
- **Marcus Bell** — Marketing Lead at Northwind Coffee. Our client contact and **the only person who can sign anything off.**
- **Northwind ops team** — holds operational facts we need (farm names, company history). Currently unresponsive.
- **Aisha** — our lead on the account; owns most assets. On leave from 2026-08-03.
- **Dan** — covering the account from 2026-08-03. New to it.
- **Tom** — ours; owns the in-store printed cards.
- Northwind's customers across 12 cafes in Manchester and Leeds — the end audience.

**Success criteria:** Every deliverable written, compliant with the locked tone of voice, factually correct, and **signed off in writing by Marcus Bell** before 2026-09-01, inside 40 hours.

**Current scope:** As listed in `brief.md`. Note the mismatch flagged in section 13 — the tracked scope is smaller than the contracted scope and this has not been reconciled.

**Out of scope / not ours:** Design, print production, web build and publishing, and the loyalty scheme's own terms and conditions (Northwind is rewriting those internally for a September replacement). We write copy; we do not publish it.

---

## 3. Locked Principles and Decisions

- **Decision:** All published copy requires Marcus Bell's **written** sign-off before it goes live. No exceptions.
  - Rationale: Contract condition, imposed after a 2025 incident in which a price was published incorrectly.
  - Date: Contract stage (predates this record); recorded in `brief.md`.
  - Status: Locked, binding.
  - Approval source: `brief.md`.
  - Supersedes: Any informal or verbal approval route. **A verbal "yes" on a call is not sign-off.**

- **Decision:** The tone of voice is locked and binding on every deliverable.
  - Rules: Warm, plain, specific. Second person. Short sentences. **Never** "artisanal", "curated", or "journey". Prices always written as "GBP 3.20", never "3.20 GBP".
  - Rationale: Approved by the client as a deliverable in its own right; it is the standard everything else is checked against.
  - Date: 2026-07-18.
  - Status: Locked (`tone-of-voice.md` header reads "LOCKED 2026-07-18"; `content-calendar.csv` records it approved and "locked").
  - Approval source: Marcus Bell.
  - Supersedes: Any earlier style guidance.

- **Decision:** Do not build the loyalty email on the 2024 loyalty terms.
  - Rationale: The loyalty scheme is being replaced in September and the new terms are not drafted. Copy written against the 2024 terms is wrong on arrival. This was attempted on 2026-07-30 and roughly an hour was discarded.
  - Date: 2026-07-30.
  - Status: Final.
  - Approval source: Marcus Bell stated the September replacement on a call.
  - Supersedes: The assumption that the 2024 terms were a usable base.

---

## 4. Project Structure

**Workstreams:** A single content workstream with four asset groups — website pages, in-store printed cards, launch emails, and the tone-of-voice one-pager (complete).

**Repositories:** None. **This is a content project — there is no code repository, no branch, no build, and no deployment pipeline.** The project folder is a plain set of documents.

**Project folder contents:**
- `brief.md` — engagement scope, client contact, sign-off condition, budget
- `content-calendar.csv` — per-asset tracker: owner, status, due date, notes
- `tone-of-voice.md` — the locked style rules
- `session-notes.md` — Aisha's raw notes, 2026-07-30
- `docs/handoffs/` — this Master plus dated Daily Handoffs

**Environments / systems:** The copy drafts themselves are **not in this folder** and their location is not recorded anywhere. A "shared sheet" holds budget tracking; its location is also not recorded. Both are gaps Dan must close — see section 14.

**Ownership:**
| Area | Owner |
|---|---|
| Website pages, launch emails, tone of voice | Aisha (Dan covering from 2026-08-03) |
| In-store printed cards | Tom |
| All sign-off | Marcus Bell (client) |
| Farm names, company history facts | Northwind ops team (client) |

Note: the `owner` column in `content-calendar.csv` still reads "Aisha" for her assets and has not been changed for the cover week.

---

## 5. Architecture and Workflow

**Content workflow (per asset):**

1. Draft written by the owner (Aisha, or Tom for store cards).
2. Internal check against `tone-of-voice.md` — banned words, second person, short sentences, price format.
3. Sent to Marcus Bell for review.
4. **Written sign-off from Marcus.** This is a hard gate.
5. Published or printed by Northwind (not us).

An asset is only "done" after step 4. Steps 1-3 being finished means the asset is *in review*, not complete.

**Tracker status values used in `content-calendar.csv`:** `not started`, `draft`, `in review`, `approved`.

**Roles:** Aisha (lead writer, account owner), Dan (covering w/c 2026-08-03), Tom (store cards), Marcus Bell (client approver), Northwind ops (factual source, currently unresponsive).

**Tools:** The tracker CSV in this folder; a separate "shared sheet" for budget (location unrecorded); email as the client channel.

**Approval gates — the ones that matter:**
- **Nothing is published without Marcus Bell's written sign-off.** Contract condition after the 2025 published-price error.
- Copy that breaches the locked tone of voice does not go to the client — it goes back to its author. This already happened once, on 2026-07-30, with store card 2.
- Factual claims about Northwind (founding year, farm names, offer amounts) need a client source. Do not fill them in from inference or from the website alone.

**Access restrictions:** Dan currently has **no recorded contact details** for Marcus Bell, Tom, or Northwind ops, and **no recorded location** for the copy drafts or the shared budget sheet. These must be obtained from Aisha before she leaves on 2026-07-31.

---

## 6. Sources of Truth

| Source | Location | Purpose | Authority | Status |
|---|---|---|---|---|
| Master Handoff | `docs/handoffs/_master-handoff.md` | Canonical project state and onboarding | Authoritative for project state | Current (v1.0, 2026-07-30) |
| Daily Handoff 2026-07-30 | `docs/handoffs/2026-07-30_001_menu-about-pages-handoff.md` | What happened on 30 July | Authoritative for that session | Current |
| Engagement brief | `brief.md` | Contracted scope, deliverables, budget, sign-off condition | Authoritative for scope and contract terms | Current |
| Content tracker | `content-calendar.csv` | Per-asset status, owner, due date | Authoritative for asset status | Current as of 2026-07-30 |
| Tone of voice | `tone-of-voice.md` | Binding style rules | Authoritative and locked | Locked 2026-07-18 |
| Session notes | `session-notes.md` | Aisha's raw notes for 30 July | Raw input, superseded by the Daily Handoff | Historical |
| Marcus Bell (written) | Email | Sign-off, offer amounts, factual confirmations | **Highest authority on anything client-facing** | Active; slow to respond |
| Northwind ops | Email | Farm names, company history | Client factual source | **Unresponsive since 2026-07-24** |
| Shared sheet | Not recorded | Budget / hours tracking | Authoritative for budget | Location unknown — Dan needs it |

**Precedence when sources conflict:**
1. **Marcus Bell in writing** beats everything. He is the sign-off authority.
2. `brief.md` beats the tracker on *scope and contract terms* (what we owe, the sign-off condition, the budget).
3. `content-calendar.csv` beats the brief and the handoffs on *current per-asset status and due dates*.
4. `tone-of-voice.md` beats any draft, any preference, and any client verbal suggestion that contradicts it — it was signed off as a deliverable.
5. The Daily Handoff beats `session-notes.md`.
6. **Verbal statements from the client do not beat anything.** They are leads to be confirmed in writing.

---

## 7. Workstream Status

Current tracker snapshot (from `content-calendar.csv`, accurate as of 2026-07-30):

| Asset | Owner | Status | Due | Note |
|---|---|---|---|---|
| homepage | Aisha | **approved** | 2026-07-24 | Signed off by Marcus 24 Jul |
| about-page | Aisha | draft | 2026-08-03 | Founder story written; founding year unresolved |
| menu-page | Aisha | in review | 2026-07-31 | With Marcus since 29 Jul, no response |
| sourcing-page | Aisha | **not started** | 2026-08-07 | **Blocked** — waiting on farm names |
| store-card-1 | Tom | **approved** | 2026-07-22 | Printed |
| store-card-2 | Tom | draft | 2026-08-05 | Returned to Tom — uses banned word "curated" |
| email-1-welcome | Aisha | draft | 2026-08-10 | |
| email-2-offer | Aisha | **not started** | 2026-08-12 | **Blocked** — offer amount not agreed |
| email-3-loyalty | Aisha | **not started** | 2026-08-14 | **Blocked** — new loyalty terms not drafted |
| tone-of-voice | Aisha | **approved** | 2026-07-18 | Locked |

### Website pages

Purpose: Rewrite customer-facing website copy for the new brand.
Owner: Aisha (Dan covering w/c 2026-08-03).
Current Status: In Progress, partly Blocked.
Completed: Homepage — approved 2026-07-24.
In Progress: Menu page — rewrite finished 2026-07-30, with Marcus since 2026-07-29, awaiting sign-off, due 2026-07-31. About page — founder story section written 2026-07-30, page not finished, due 2026-08-03.
Blocked: Sourcing page — not started, no farm names from Northwind ops (asked 2026-07-24 and 2026-07-29), due 2026-08-07. **This is the critical path.**
Open Decisions: Northwind's founding year — 2009 or 2011 (see section 10). Whether four further pages exist beyond the four tracked (see section 13).
Dependencies: Northwind ops for farm names; Marcus Bell for the founding year and for all sign-off.
Next Action: Escalate the farm names and the founding year to Marcus in one email — section 17.
Relevant Sources: `content-calendar.csv`, `tone-of-voice.md`, `docs/handoffs/2026-07-30_001_menu-about-pages-handoff.md`.

### In-store printed cards

Purpose: Printed cards for the 12 cafes.
Owner: Tom.
Current Status: In Progress.
Completed: Store card 1 — approved 2026-07-22 and **already physically printed**. Changing it means a reprint.
In Progress: Store card 2 — draft reviewed on 2026-07-30 and returned to Tom because it uses "curated" twice, which the locked tone of voice bans. Due 2026-08-05.
Blocked: Nothing externally; waiting on Tom.
Open Decisions: Whether the four further cards implied by `brief.md` are in scope (see section 13).
Dependencies: Tom's turnaround; then Marcus's sign-off; then print lead time — note that print adds time the tracker does not show.
Next Action: Chase Tom for the corrected draft and re-check "curated" is gone before it goes to Marcus.
Relevant Sources: `content-calendar.csv`, `tone-of-voice.md`.

### Launch emails

Purpose: Three-email launch sequence for the 2026-09-01 brand launch.
Owner: Aisha (Dan covering).
Current Status: Blocked.
Completed: None.
In Progress: Email 1 (welcome) — draft, due 2026-08-10.
Blocked:
- Email 2 (offer), due 2026-08-12 — the offer amount has not been agreed in writing. Marcus said "probably 20% off first order" verbally; that is not an agreement.
- Email 3 (loyalty), due 2026-08-14 — the loyalty scheme is being replaced in September and the new terms are not drafted. **There may be no terms to write against before the due date.**
Open Decisions: The offer amount; what email 3 does given the terms will not exist in time (section 10).
Dependencies: Marcus Bell for both.
Next Action: Get the offer confirmed in writing (part of the section 17 email); separately ask Marcus what happens to email 3.
Relevant Sources: `content-calendar.csv`, `docs/handoffs/2026-07-30_001_menu-about-pages-handoff.md`.

### Tone-of-voice one-pager

Purpose: Define and lock the brand's written voice.
Owner: Aisha.
Current Status: **Complete.** Approved 2026-07-18 and locked.
Next Action: None. Do not re-open it — it is now a constraint on everything else.
Relevant Sources: `tone-of-voice.md`.

---

## 8. Important Project History

- **2025 (date not recorded) —** A price was published incorrectly for Northwind. As a direct result, the contract now requires **Marcus Bell's written sign-off on all published copy**. This is why the approval gate is strict and why verbal approvals are refused. Anyone tempted to shortcut sign-off should read this line first.
- **2026-07-18 —** Tone-of-voice one-pager approved and **locked**. It became the binding standard for every later deliverable, and it is the reason store card 2 was rejected on 30 July.
- **2026-07-22 —** Store card 1 approved and printed. Printing makes it effectively immutable.
- **2026-07-24 —** Homepage signed off by Marcus. First page approved. Same day, the first request to Northwind ops for farm names went out — the request that is still unanswered.
- **2026-07-29 —** Menu page sent to Marcus for review. Second request to Northwind ops for farm names. Neither has been answered.
- **2026-07-30 —** Menu page rewrite finished; About page founder story written; the founding-year conflict (2009 vs 2011) surfaced; store card 2 rejected for a banned word; the loyalty email approach was tried against the 2024 terms and abandoned after Marcus revealed the September scheme replacement.
- **2026-08-03 (planned) —** Account passes to Dan for one week while Aisha is on leave.

---

## 9. Final Decisions

- Decision: Written sign-off from Marcus Bell required before any copy is published.
  - Date: Contract stage.
  - Rationale: Consequence of the 2025 published-price error.
  - Impact: No asset counts as complete until Marcus confirms in writing; verbal approval is worthless here.
  - Source: `brief.md`.
  - Supersedes: Informal approval routes.

- Decision: Tone of voice locked.
  - Date: 2026-07-18.
  - Rationale: Approved deliverable; the standard all copy is measured against.
  - Impact: Binding. Drafts breaching it are returned to their author, not forwarded to the client.
  - Source: `tone-of-voice.md`, `content-calendar.csv`.
  - Supersedes: Earlier style guidance.

- Decision: Do not draft email 3 against the 2024 loyalty terms.
  - Date: 2026-07-30.
  - Rationale: Scheme is replaced in September; new terms not drafted.
  - Impact: Email 3 stays blocked; its 2026-08-14 due date is at risk.
  - Source: `session-notes.md`, 2026-07-30 Daily Handoff.
  - Supersedes: The earlier assumption that the 2024 terms were a usable base.

- Decision: Treat the "20% off first order" offer as unconfirmed.
  - Date: 2026-07-30.
  - Rationale: Verbal only. Offer amounts are precisely the category of error the sign-off condition exists to prevent.
  - Impact: Email 2 does not start until the offer is in writing.
  - Source: `session-notes.md`.
  - Supersedes: Nothing.

---

## 10. Open Decisions

- **Decision Needed:** Was Northwind founded in 2009 or 2011?
  - Why It Matters: It is stated in the About page founder story. Publishing the wrong founding year is a factual error about the client's own history, under a contract already tightened because of a published error.
  - Available Options: 2011 (Northwind's live website) or 2009 (the deck Marcus sent). 2011 is currently in the draft as a flagged placeholder because it is what is published today.
  - Required Evidence: Marcus Bell confirming in writing.
  - Decision Owner: Marcus Bell.
  - Deadline or Trigger: About page is due **2026-08-03**.

- **Decision Needed:** What is the launch offer?
  - Why It Matters: Email 2 is entirely built on it and cannot start without it.
  - Available Options: "Probably 20% off first order" (verbal, from Marcus) — or anything else he decides.
  - Required Evidence: Written confirmation from Marcus.
  - Decision Owner: Marcus Bell.
  - Deadline or Trigger: Email 2 is due **2026-08-12**.

- **Decision Needed:** What does email 3 (loyalty) say, given the new loyalty terms will not exist by its due date?
  - Why It Matters: The scheme is being replaced in September — after the 2026-09-01 launch — and the new terms are not drafted. The email is due 2026-08-14. Writing it against the old terms is already ruled out.
  - Available Options: Move the email later; write it without scheme specifics; drop it from the launch sequence; wait for the terms and accept the delay.
  - Required Evidence: A decision from Marcus, ideally with a date for the new terms.
  - Decision Owner: Marcus Bell.
  - Deadline or Trigger: **Raise this now** — waiting until 2026-08-14 removes every option except delay.

- **Decision Needed:** Who supplies the farm names, and by when?
  - Why It Matters: The sourcing page — the longest page and the critical path — cannot start without them. Due 2026-08-07.
  - Available Options: Northwind ops (asked twice, no reply); escalate to Marcus to chase or supply them; agree a reduced-scope sourcing page without named farms.
  - Required Evidence: A written list of farm names, or a named owner and a date from Marcus.
  - Decision Owner: Marcus Bell (escalation).
  - Deadline or Trigger: **Immediately** — the page still has to be written after the names arrive.

- **Decision Needed:** Is the real deliverable list 8 pages and 6 cards, or 4 and 2?
  - Why It Matters: `brief.md` contracts for 8 website pages and 6 in-store cards; `content-calendar.csv` tracks only 4 pages and 2 cards. If the other 10 items are real and untracked, the remaining ~14 hours of budget is nowhere near enough and the 2026-09-01 launch is in serious doubt.
  - Available Options: The untracked items were descoped; they were completed before tracking started; they are genuinely outstanding and missing from the tracker.
  - Required Evidence: Aisha or Marcus confirming the true list.
  - Decision Owner: Aisha (fastest), then Marcus if contractual.
  - Deadline or Trigger: This week — it changes the whole plan.

---

## 11. Changes Since the Previous Baseline

This is version 1.0 — the first Master Handoff for this project. There is no previous baseline. It establishes state as of end of day 2026-07-30, drawn from `brief.md`, `content-calendar.csv`, `tone-of-voice.md`, `session-notes.md`, and the Daily Handoff `docs/handoffs/2026-07-30_001_menu-about-pages-handoff.md`.

New blockers recorded at baseline: sourcing page (farm names), email 2 (offer amount), email 3 (loyalty terms), store card 2 (awaiting Tom's fix).

Resolved blockers: none.

---

## 12. Superseded or Replaced Items

| Superseded Item | Replacement | Reason | Date |
|---|---|---|---|
| 2024 loyalty scheme terms | New loyalty terms, not yet drafted | Scheme is being replaced in September 2026. Do not write copy against the 2024 terms. | 2026-07-30 |
| `session-notes.md` (30 July) | `docs/handoffs/2026-07-30_001_menu-about-pages-handoff.md` | The Daily Handoff is the structured, verified version of those raw notes. | 2026-07-30 |
| Any style guidance predating 2026-07-18 | `tone-of-voice.md` (LOCKED) | Tone of voice approved as a deliverable and locked. | 2026-07-18 |
| Informal / verbal approval | Written sign-off from Marcus Bell | Contract condition following the 2025 published-price incident. | Contract stage |

---

## 13. Contradictions and Resolution

- **Contradiction:** Northwind's founding year — 2009 vs 2011.
  - Conflicting sources: Northwind's live website says 2011; the deck Marcus sent says 2009. Both originate from the client.
  - Verified current state: **Unresolved.** Nobody has confirmed which is right.
  - Authoritative source: Marcus Bell, in writing.
  - Resolution: 2011 is used provisionally in the About page draft and is flagged in the copy, because 2011 is what is currently published.
  - Reason for precedence: Matching what is already public is the lower-risk placeholder; it is not evidence of correctness.
  - Corrective action required: Get Marcus to confirm before the About page goes for sign-off. **Do not remove the flag from the draft until he has.**

- **Contradiction:** Deliverable counts — `brief.md` vs `content-calendar.csv`.
  - Conflicting sources: `brief.md` commits to 8 rewritten website pages and 6 in-store printed cards. `content-calendar.csv` tracks 4 pages (homepage, about, menu, sourcing) and 2 store cards.
  - Verified current state: **Unresolved.** The remaining 4 pages and 4 cards appear nowhere in the project folder.
  - Authoritative source: `brief.md` for contracted scope; only Aisha or Marcus can say what actually happened to the rest.
  - Resolution: Not resolved. Recorded here so it is not discovered late.
  - Reason for precedence: The brief states the contract; the tracker only states what someone chose to track.
  - Corrective action required: Confirm the true deliverable list this week. If the extra items are live, the budget and the launch date both need re-planning.

- **Contradiction:** Which version of the menu page is with Marcus?
  - Conflicting sources: `session-notes.md` says the rewrite was finished on the morning of 2026-07-30 but was sent to Marcus on 2026-07-29.
  - Verified current state: **Unresolved.** Marcus may be holding a superseded draft.
  - Authoritative source: Aisha, or a comparison of the sent version against the current one.
  - Resolution: Not resolved.
  - Reason for precedence: n/a.
  - Corrective action required: Confirm before treating any sign-off Marcus gives as covering the current text. If he approves an older version, the difference has to go back to him.

- **Contradiction:** Is `content-calendar.csv` the same thing as "the shared sheet" in `brief.md`?
  - Conflicting sources: `brief.md` says the budget is "tracked in the shared sheet"; the project folder contains `content-calendar.csv`, which has no budget or hours columns.
  - Verified current state: **Probably two different artefacts, but unverified.** No location is recorded for the shared sheet.
  - Authoritative source: Aisha.
  - Resolution: Not resolved.
  - Corrective action required: Get the shared sheet's location and access before Aisha goes on leave.

---

## 14. Risks, Constraints, and Dependencies

**Active risks:**

| Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| Sourcing page misses 2026-08-07 | High — longest page, critical path, squeezes everything before the 2026-09-01 launch | High — two unanswered requests, and the person with the client relationship is on leave that week | Escalate to Marcus on 2026-08-03; ask for names or an owner and a date | Dan → Marcus |
| Email 3 cannot be written by 2026-08-14 | Medium-high — new loyalty terms do not exist and the scheme changes after launch | High | Get a decision from Marcus now on rescoping or moving it | Marcus |
| About page publishes the wrong founding year | High — factual error about the client's own history, under a contract tightened by a prior published error | Medium | Keep the flag in the draft; get written confirmation before sign-off | Marcus |
| Budget overrun | Medium — roughly 14 hours left against the longest page, an unfinished page, three emails, and possibly 10 untracked items | Medium-high | Reconcile hours against the shared sheet early in the week and flag before the budget is spent | Dan |
| Untracked deliverables turn out to be real | High — would make the current plan and budget unachievable | Unknown | Confirm the deliverable list this week | Dan → Aisha/Marcus |
| Handover friction | Medium-high — Dan has no contacts, no draft locations, no sheet access, and no relationship history | Certain unless fixed before 2026-07-31 | Aisha to hand over contacts, locations and access before leaving | Aisha |
| Store card 2 misses 2026-08-05 | Medium — printing adds lead time not shown in the tracker | Medium | Chase Tom early in the week, not on the due date | Dan |

**Constraints:**
- **Written sign-off from Marcus Bell is mandatory before publication. No exceptions.**
- Tone of voice is locked: warm, plain, specific; second person; short sentences; never "artisanal", "curated", or "journey"; prices as "GBP 3.20", never "3.20 GBP".
- Budget: 40 hours. Roughly 26 used as of 2026-07-30 — **an estimate, not formally checked**. Roughly 14 remaining.
- Hard external date: brand launch **2026-09-01**.
- Aisha unavailable for the week beginning 2026-08-03.
- Store card 1 is printed; any change is a reprint, not an edit.

**Dependencies:**
- Northwind ops → farm names (sourcing page) and the founding year. **Currently unresponsive.**
- Marcus Bell → all sign-off, the offer amount, the founding year, the email 3 decision. Slow to respond.
- Tom → corrected store card 2.
- Aisha → contact details, draft locations, shared-sheet access, and the deliverable-count answer. **Available only until 2026-07-31.**

**Failure points:** A single client approver who is slow to respond, an unresponsive client ops team on the critical path, and a lead going on leave during the week that contains two deadlines.

---

## 15. Operational State

*(This project has no repository, branch, build, test suite, or deployment pipeline. This section records the equivalent operational reality instead.)*

- **Repository / branch / commit / build / tests / CI / deployment:** None — not applicable. This is a documents-and-copy project.
- **Published / live assets:** Homepage copy approved 2026-07-24. Store card 1 approved 2026-07-22 and **physically printed** — in circulation, changing it requires a reprint.
- **With the client, awaiting response:** Menu page, with Marcus Bell since 2026-07-29, due 2026-07-31, no response as of 2026-07-30.
- **Internal, awaiting a colleague:** Store card 2, returned to Tom on 2026-07-30, due 2026-08-05.
- **Outstanding client requests:** Farm names — requested from Northwind ops 2026-07-24 and 2026-07-29, no reply. Founding year — raised, unconfirmed. Offer amount — verbal only, unconfirmed.
- **Scheduled sends:** None. No launch email has been scheduled or sent; all three are unfinished. Nothing in this project sends automatically.
- **Tracker state:** `content-calendar.csv` updated 2026-07-30 and believed accurate.
- **Budget standing:** ~26 of 40 hours used. **Unverified** — not reconciled against the shared sheet.
- **Access standing:** Dan has the project folder. Dan does **not** have recorded contact details for Marcus, Tom or Northwind ops, the location of the copy drafts, or access to the shared sheet.

---

## 16. Current Project State

**Current phase:** Mid-delivery, with a one-week ownership handover starting 2026-08-03.

**Latest approved output:** Homepage copy, signed off by Marcus Bell on 2026-07-24.

**Active work:** About page (founder story written, page unfinished, due 2026-08-03); menu page awaiting client sign-off; store card 2 awaiting Tom's correction.

**Completed work:** Homepage (approved). Store card 1 (approved and printed). Tone-of-voice one-pager (approved and locked).

**Incomplete work:** About page, sourcing page, store card 2, and all three launch emails.

**Blockers:** Farm names (sourcing page). Offer amount (email 2). New loyalty terms (email 3). Tom's fix (store card 2). All but the last are client-side.

**Open decisions:** Founding year; offer amount; email 3 scope; farm-name ownership; true deliverable count. See section 10.

**Readiness for next phase:** **Not ready.** Only 3 of the tracked 10 assets are approved. Three are blocked on the client, and the critical-path page has not started with 8 days to its due date and roughly a month to launch.

**Overall status:** **At risk.** The controllable work is in reasonable shape; the schedule risk sits almost entirely in client responsiveness, and the week in which several deadlines fall is the week the account is covered by someone new.

---

## 17. Immediate Next Action

Immediate Next Action: On **Monday 2026-08-03**, send **one written email to Marcus Bell** containing four numbered asks:
1. **Farm names for the sourcing page.** State that Northwind ops were asked on 24 and 29 July with no reply, that the page is due 2026-08-07, that it is the longest page, and ask him to either supply the names or name someone and a date.
2. **Founding year.** Ask him to confirm in writing whether Northwind was founded in 2009 or 2011 — the website says 2011, the deck he sent says 2009 — and note the About page is due today.
3. **Launch offer.** Ask him to confirm the offer in writing so email 2 can start, referencing the "probably 20% off first order" from the call, and note email 2 is due 2026-08-12.
4. **Menu page sign-off.** Chase it — with him since 2026-07-29, due 2026-07-31.

Also tell him Aisha is on leave this week and that Dan is covering, so he replies to the right person.

Responsible Role or Agent: Dan (covering the account w/c 2026-08-03).

Start From: This Master Handoff, then `docs/handoffs/2026-07-30_001_menu-about-pages-handoff.md`, then `content-calendar.csv`.

Required Inputs: **Marcus Bell's email address — not recorded anywhere in this project folder. Get it from Aisha before Friday 2026-07-31.** Plus the dates and history in this document.

Expected Deliverable: One sent email with four numbered, individually answerable asks and the cover note about Dan.

Acceptance Criteria: One message, not four. Each ask answerable with a single fact. Each states the deadline it is holding up. The message asks for answers **in writing** — a verbal reply does not satisfy the sign-off condition.

Dependencies: Marcus's contact details; Marcus's responsiveness.

Stop Conditions: If Marcus's contact details cannot be obtained, stop and escalate internally — nothing else on the list can proceed. If there is no reply on the farm names by **Wednesday 2026-08-05**, treat 2026-08-07 as at risk and escalate internally rather than continuing to wait.

Do Not Change:
- Do not remove the founding-year flag from the About page draft. It is deliberate.
- Do not write email 3 against the 2024 loyalty terms. Already tried and discarded.
- Do not treat "probably 20% off first order" as agreed.
- Do not treat the menu page as done — it has no sign-off.
- Do not use "artisanal", "curated", or "journey", and do not pass on a draft that does.
- Do not publish or send anything without Marcus's written sign-off.
- Do not revise store card 1 — approved and printed.

**Prioritized queue after that (week of 2026-08-03):**

1. Finish the About page (due 2026-08-03) as far as it can go with the founding year flagged, and send it to Marcus for sign-off.
2. Chase Tom for the corrected store card 2 (due 2026-08-05); re-check against `tone-of-voice.md`, specifically that "curated" is gone, before it goes to Marcus.
3. Reconcile hours against the shared sheet and flag if the remaining budget will not cover the remaining work.
4. Ask Marcus what happens to email 3 given the loyalty terms will not exist by 2026-08-14.
5. Resolve the deliverable-count mismatch: `brief.md` says 8 pages and 6 cards, the tracker has 4 and 2.
6. Write the sourcing page the moment the farm names arrive — longest page, least slack.
7. Progress email 1 (welcome), due 2026-08-10 — the only email not blocked by anyone.

---

## 18. New-Session Start Guide

**For Dan, Monday 2026-08-03 — in this order.**

1. **Read first:** this file, then `docs/handoffs/2026-07-30_001_menu-about-pages-handoff.md`, then `content-calendar.csv`, then `tone-of-voice.md`. Read `brief.md` for the contract terms. `session-notes.md` is Aisha's raw notes and is superseded by the Daily Handoff.

2. **Canonical source:** this Master Handoff for project state; `content-calendar.csv` for per-asset status; `brief.md` for scope and contract terms; `tone-of-voice.md` for style. When they conflict, use the precedence order in section 6. Marcus Bell in writing beats all of them.

3. **Current state:** 3 of 10 tracked assets approved (homepage, store card 1, tone of voice). Menu page with the client awaiting sign-off. About page in draft and due today. Sourcing page not started and blocked. Store card 2 back with Tom. Emails 2 and 3 blocked on the client. Overall: at risk.

4. **Start here:** section 17 — the single email to Marcus Bell. **Before that, if you have not already, get Marcus's, Tom's and Northwind ops' contact details from Aisha — they are recorded nowhere in this project and without them nothing moves.**

5. **Final decisions (do not re-open):** written sign-off from Marcus is mandatory; the tone of voice is locked; email 3 is not written against the 2024 loyalty terms; the "20% off" offer is unconfirmed until it is in writing.

6. **Do not repeat:**
   - Drafting email 3 from the 2024 loyalty terms — cost about an hour on 2026-07-30 and was discarded; the scheme is replaced in September.
   - Sending a third identical chase to Northwind ops for the farm names — two direct requests failed; the channel is not working, escalate through Marcus.
   - Re-reviewing Tom's current store card 2 draft — already reviewed; the fault is known ("curated" twice). Review the corrected version when it arrives.
   - Re-opening the tone of voice, re-writing the homepage, or revising store card 1 (approved, and printed).
   - Reasoning your way to a founding year — both figures came from the client; only Marcus's written answer resolves it.

7. **Access required:** contact details for Marcus Bell, Tom, and Northwind ops; the location of the actual copy drafts (not in this folder); access to the shared budget sheet. **All three are currently missing and all three come from Aisha, who is available only until 2026-07-31.**

8. **Requires explicit human approval — do not do these on your own authority:**
   - **Publishing or sending any copy.** Every published asset needs Marcus Bell's **written** sign-off. This is a contract condition after a 2025 incident where a price was published wrong. A verbal yes is not sign-off.
   - **Committing to any offer, price, or factual claim about Northwind** (offer percentages, founding year, farm names) without a written client source.
   - **Changing store card 1**, which is approved and already printed — that is a reprint and a cost conversation.
   - **Agreeing scope or deadline changes** with the client, including anything arising from the deliverable-count mismatch — raise internally first.

---

## 19. Incorporated Daily Handoffs

| Date | Handoff File | Scope | Incorporated into Master |
|---|---|---|---|
| 2026-07-30 | `docs/handoffs/2026-07-30_001_menu-about-pages-handoff.md` | Menu page rewrite, About page founder story, store card 2 review, tracker update | Yes — v1.0, 2026-07-30 |
