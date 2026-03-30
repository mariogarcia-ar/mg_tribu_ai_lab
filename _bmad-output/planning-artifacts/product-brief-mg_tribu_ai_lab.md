---
title: "Product Brief: MG TRIBU AI Lab"
status: "complete"
created: "2026-03-30"
updated: "2026-03-30"
review_passes: ["skeptic", "opportunity", "educational-effectiveness"]
inputs:
  - idea.md
  - README.md
  - 3-stages.md
  - docs/encuentro1/readme.md
  - docs/encuentro2/readme.md
  - CLAUDE.md
  - my-prompt.md
---

# Product Brief: MG TRIBU AI Lab

## Executive Summary

Organizations are adopting AI-assisted development at unprecedented speed — and breaking their systems just as fast. The problem isn't that AI writes bad code. The problem is that AI makes decisions humans never made, and those invisible choices compound into unmaintainable systems. **MG TRIBU AI Lab** is a hands-on live-coding workshop that makes this failure mode visceral and teaches the governance model that eliminates it.

The lab uses a deliberately simple vehicle — a TODO app that evolves toward CRM — to demonstrate two radically different approaches to AI-assisted development. In **Encuentro 1**, participants watch a system built with Claude and Copilot collapse under its own implicit decisions: status strings that fragment, priorities that sort incorrectly, and a cascading fix loop that cannot be escaped. In **Encuentro 2**, the same system is rebuilt using the **Think / Decide / Execute / Verify** framework, where every design decision is documented before a line of code is generated. Same features, same tools, zero debugging.

The takeaway is concrete: the advantage isn't in using AI — it's in using it without losing control.

## The Problem

Development teams using AI assistants are experiencing a pattern they can't name: systems that work when they're built, then resist every change. The root cause is **implicit decision-making** — when a developer prompts "build a TODO app," the AI silently decides that status is a string, that priorities sort alphabetically, that any user can see any task. These decisions are reasonable in isolation but contradictory at scale, and they're invisible until the system breaks.

The cost is real:
- In the lab's E1 demo, **Fix 5 consumes more time than building features 1-4 combined** — and the system is still broken
- Features that "work" individually but create **infinite fix loops** when combined
- Systems that **cannot be explained** to new team members — because no one decided how they should work
- Technical debt that's invisible until it's structural

Teams know something is wrong, but they lack the vocabulary and the model to fix it. They blame the AI, or they blame the developer, when the actual failure is the absence of governance.

## The Solution

MG TRIBU AI Lab is a two-session live-coding workshop that transforms how participants think about AI-assisted development.

**Encuentro 1 — "How a system breaks even though it seems to work"**
Participants watch the instructor build a TODO app with Claude and Copilot, no questions asked. It works. Then users are added, priorities introduced, states expanded — and the system enters a cascading failure loop where each fix breaks something new. The instructor stops at Fix 5, with the system in an unrecoverable state. The group performs a structured **decision autopsy**: for each bug, the group identifies who made the decision and when. The answer is always "the AI, implicitly." The autopsy itself is the most transferable skill — participants learn to audit their own systems for implicit decisions.

Note: E1 runs from a rehearsed, reproducible script with pinned prompts and expected AI outputs. The runbook includes fallback talking points if the live AI behaves differently than expected.

**Encuentro 2 — "The same system. Without the loop."**
Same features, same order, same tools. But before every stage, the instructor pauses and applies the **Think / Decide / Execute / Verify** cycle:

| Phase | Owner | Produces |
|---|---|---|
| **Think** | Human | Unanswered questions about the design |
| **Decide** | Human | Explicit rules documented in `decisions.md` |
| **Execute** | AI (bounded) | Code that respects the documented rules |
| **Verify** | Human | Confirmation that code matches decisions |

The result: every feature works on the first try. No fix loop. No debugging. The AI doesn't disappear — it changes role, from decision-maker to proposal engine operating within human-defined constraints.

## What Makes This Different

- **Experiential, not theoretical.** Participants don't hear about governance — they watch a system collapse without it and succeed with it, in real time, with the same AI tools they use daily.
- **Same system, same tools, different process.** The contrast is undeniable because every variable is controlled except the governance model.
- **The infinite fix loop is unforgettable.** Watching Fix 1 break Fix 2 break Fix 3 in live code creates visceral understanding that slides cannot replicate.
- **Immediately applicable.** The Think/Decide/Execute/Verify framework and the `decisions.md` pattern require zero new tooling. E2 closes with a concrete first step: participants receive a blank `decisions.md` template to copy into their next repo.
- **Prompt contrast as visible artifact.** E1's unbounded prompt ("build a TODO app") is shown side-by-side with E2's bounded prompt (referencing `decisions.md`). The governance difference is visible in the input, not just the output.
- **Scales to a three-stage vision.** The workshop covers Stages 1 (Code-Centric) and 2 (Rules-Centric), with Stage 3 (Spec-Driven, with automated validation) as a natural evolution for advanced teams.

## Who This Serves

**Product Owners and Technical Decision-Makers**
They need to understand *when* to stop and ask questions, and *what* those questions are. The lab teaches them to recognize the governance gap before it becomes technical debt. They observe the instructor's pauses — the moments where Think and Decide happen — and learn that those pauses are the product. Each Think phase in E2 includes explicit "questions a PO should ask," giving them a checklist they can use in backlog refinement.

Both audiences attend the same session. The instructor bridges the gap explicitly: "This next part is for devs — POs, watch for *when* the question gets asked, not *the answer*."

**Senior Developers**
They need to see *how* documented decisions translate into code structure. The lab shows them concretely: an Enum instead of a string, a `terminal_states()` method instead of hardcoded checks, a `list_tasks_for_user()` instead of `list_all`. They leave with patterns, not just principles.

## Success Criteria

**Immediate (end of session):**
- Participants can **articulate the difference** between Code-Centric and System-Centric AI-assisted development
- Participants can **identify implicit decisions** in a code snippet (assessed informally via show-of-hands exercise at session close)

**Short-term (1 week):**
- Participants **adopt the Think/Decide/Execute/Verify cycle** in their own workflows — measured via a 1-week follow-up survey

**Medium-term (1 month):**
- The `decisions.md` pattern (or equivalent) appears in participant teams' repositories — measured via a single async follow-up question: "Does your current repo have a `decisions.md` or equivalent?"

**Health signal:**
- Workshop NPS consistently above 8/10

## Scope

**Delivery format:**
- Two live-coding sessions (~2 hours each), delivered same day or one week apart
- Mixed audience (POs + senior devs) in the same room
- E2 includes a 5-minute E1 recap for partial attendees

**In scope (this version):**
- TODO app with: task lifecycle (Enum states), priority (IntEnum), multi-user (owner + creator), visibility control, overdue notifications
- Python stdlib only (sqlite3, argparse, enum, datetime) — single file CLI
- `decisions.md` as governance artifact
- Runbooks for both encounters (instructor-facing, in Spanish)
- Side-by-side comparison of E1 vs E2 codebases

**Explicitly out of scope:**
- Task sharing between users (decided, not overlooked)
- Admin roles and RBAC
- Web UI or API — CLI only
- CRM features (contacts, pipeline, audit trail, tags) — mentioned as future extensions to show the model scales
- Automated spec validation (Stage 3 of the evolution)
- CI/CD, testing infrastructure, external dependencies

## Vision

If the lab succeeds, it becomes the standard onboarding experience for teams adopting AI-assisted development. The three-stage evolution provides the roadmap:

1. **Stage 1 — Code:** Teams recognize they're here (AI decides everything)
2. **Stage 2 — Rules:** Teams adopt `decisions.md` and the TDEV cycle (humans decide, AI executes)
3. **Stage 3 — Spec:** Teams evolve to executable specifications with automated validation (the system enforces decisions)

The TODO-to-CRM vehicle scales naturally: contacts, pipelines, roles, and audit trails introduce the same governance challenges at higher complexity, proving that the model doesn't just work for toy examples — it works precisely because complexity makes governance more necessary, not less.

> "La complejidad no cambia el modelo — lo hace más necesario."
