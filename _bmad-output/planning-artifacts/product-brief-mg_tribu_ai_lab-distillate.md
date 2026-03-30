---
title: "Product Brief Distillate: mg_tribu_ai_lab"
type: llm-distillate
source: "product-brief-mg_tribu_ai_lab.md"
created: "2026-03-30"
purpose: "Token-efficient context for downstream PRD creation"
---

# Product Brief Distillate: MG TRIBU AI Lab

## Rejected Ideas and Explicit Non-Decisions

- **Task sharing between users:** Explicitly out of scope. Rationale: requires a permission model that isn't defined. Mentioned in decisions.md as a conscious non-decision, not an oversight.
- **Admin roles / RBAC:** Out of scope. Would add complexity that distracts from the governance lesson.
- **Web UI or REST API:** Out of scope. CLI-only keeps focus on logic and decisions, not presentation.
- **CRM features (contacts, pipeline, audit trail, tags):** Out of scope for implementation. Mentioned only as future extensions to prove the governance model scales.
- **Stage 3 (Spec-Driven, automated validation):** Out of scope for this workshop version. Exists as a conceptual horizon only.
- **CI/CD, testing infrastructure, external dependencies:** Deliberately excluded. The minimal stack is pedagogically intentional.

## Requirements Hints

- E1 must be a **rehearsed, reproducible script** with pinned prompts and expected AI outputs. Fallback talking points needed if live AI diverges.
- E2 must include **explicit "questions a PO should ask"** at each Think phase — giving POs a reusable checklist.
- E2 closing must include a **`decisions.md` template handout** as a concrete transfer mechanism.
- E1 vs E2 **prompt comparison** should be a visible artifact (side-by-side on screen).
- E2 should include a **5-minute E1 recap** for partial attendees.
- E1 autopsy should use a structured format: for each bug, identify "who decided" and "when."
- **Show-of-hands exercise** at session end to informally assess learning (can participants identify implicit decisions?).
- **1-week follow-up survey** for adoption tracking.
- **1-month async check:** "Does your repo have a `decisions.md` or equivalent?"

## Technical Context and Constraints

- **Language:** Python stdlib only — sqlite3, argparse, enum, datetime
- **Architecture:** Single file (todo.py), SQLite persistence, CLI with argparse
- **No external dependencies** — runs anywhere Python runs
- **Branch structure:** `encuentro1` (anti-pattern), `encuentro2` (solution), `encuentro2-bmad` (planning with BMAD agents)
- **Documentation language:** Spanish (runbooks, workshop materials). Code identifiers in English.
- **Task status:** Python Enum — PENDING, IN_PROGRESS, BLOCKED, REVIEW, DONE, CANCELLED
- **Terminal states:** DONE, CANCELLED — defined once in `TaskStatus.terminal_states()`
- **Priority:** IntEnum — LOW=1, MEDIUM=2, HIGH=3, URGENT=4. Sort by integer value.
- **Ownership:** `created_by` (required int) + `owner_id` (optional int, None = unassigned)
- **Visibility:** No `list_all`. Every listing requires explicit `user_id`. User sees tasks where `owner_id = user_id OR created_by = user_id`.
- **Due date:** Optional. Overdue = `due_date < today AND status NOT IN terminal_states`. Notify owner; fallback to creator.

## Detailed User Scenarios

- **PO in E1:** Watches instructor prompt Claude freely. Sees "it works." Then sees features compound into unfixable state. During autopsy, realizes every broken behavior traces to a question nobody asked.
- **PO in E2:** Sees instructor pause before each stage. Hears the Think questions. Sees the Decide answers written into `decisions.md`. Understands that those pauses prevent the E1 collapse.
- **Senior dev in E1:** Notices status is a string, priority sorts wrong, `list_all` leaks data. Watches the fix loop cascade. Recognizes this pattern from their own codebase.
- **Senior dev in E2:** Sees Enum instead of string, `terminal_states()` instead of hardcoded list, `list_tasks_for_user()` instead of `list_all`. Gets concrete patterns to apply Monday.

## The Infinite Fix Loop (E1 Etapas 3-4) — Detailed Sequence

1. Add `due_date` → breaks schema (no migration for existing tasks)
2. Add `DEFAULT NULL` → reveals status inconsistency ("done" vs "completed")
3. Unify states to "done" → tasks marked "completed" now unrecognized as terminal
4. Find-replace "completed" → "cancelled" states still not recognized as terminal
5. Add "cancelled" to hardcoded terminal list → conflicts with separate hardcoded list elsewhere
6. No Fix 6 possible. System breaks on any change. **Loop cannot be escaped without redesign.**

Key insight: each fix is locally correct but globally inconsistent because no decision document exists to validate against.

## E1 vs E2 Comparison Data

| Metric | E1 (Code-Centric) | E2 (System-Centric) |
|---|---|---|
| Status definitions | String in 4 places | 1 Enum, 1 decision rule |
| Terminal states | Hardcoded in notification function | `TaskStatus.terminal_states()` |
| Priority sort | Alphabetic (broken) | Integer value DESC |
| Visibility | `list_all` unfiltered | Always filtered by user_id |
| New feature cost | Fix loop, debugging > building | 0 debugging |
| System state at stage 3 | Unfixable | Stable, extensible |

## Three-Stage Evolution Context

| Level | Controls system | Think | Decide | Execute | Verify |
|---|---|---|---|---|---|
| Stage 1: Code | AI | None | Implicit in code | AI free | Manual "does it work?" |
| Stage 2: Rules | Human | Exploratory prompts | decisions.md | AI bounded | Human checklist |
| Stage 3: Spec | System | Structured problem spec | Executable contracts | Spec-derived tasks | Automated validation |

Workshop covers Stages 1 and 2. Stage 3 is the aspirational horizon.

## Open Questions

- Should Stage 3 get a brief 5-minute preview at the end of E2? (e.g., a single test that asserts a `decisions.md` rule)
- Should the workshop include a "failure taxonomy" segment — naming the 3 categories of implicit AI decisions (type decisions, visibility decisions, state machine decisions) so participants can spot them in their own codebases?
- What is the ideal time gap between E1 and E2? Same day allows direct comparison; one week allows reflection and anticipation.
- Should CRM-level decisions be introduced as a closing thought experiment? (e.g., "a contact can be owned by multiple users — now what?")

## Scope Signals

- **MVP:** Two encounters, TODO app, decisions.md, runbooks, side-by-side comparison
- **Nice-to-have:** Template handout, follow-up survey, prompt comparison artifact
- **Future:** Stage 3 preview, failure taxonomy, CRM thought experiment, curriculum expansion
