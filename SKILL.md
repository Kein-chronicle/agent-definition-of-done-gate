---
name: done-state-honesty
description: Stop pipelines and agents from announcing "done" when work is merely unclaimed. Use when designing a status/completion function for a multi-gate pipeline, when a status line says "everything the factory can do is finished" while a human or device step is still pending, when HUMAN/N-A/EXEMPT verdicts are counted as complete, or when an agent keeps stopping early because the status text told it to.
---

# done-state-honesty

`HUMAN` is not a synonym for "a person must do this". Far more often it means **nobody has done it yet**.
If the completion rule counts HUMAN as done, the pipeline prints "all automated work finished"
while a test ad ID is still in the build and the store listing is empty. In one real run an agent
read that sentence and stopped **three times in one session**. No gate was wrong. The *definition of done* was.

## The rule

> A gate that has an instrument (an automated measurement) is **not closed by a HUMAN verdict.**
> A gate with no instrument may be closed by HUMAN - otherwise that state could never be reached.

## Checklist when you write the completion function

1. Read the done-set first. If it contains `HUMAN`, ask why.
2. For every item labelled "human's job": could a machine do it? Console registration, store
   upload and build upload usually all can be automated. Prove it before accepting the label.
3. Name the unfinished state after **what remains**, not after the finish line:
   `AWAITING_DEVICE`, not `AWAITING_VIDEO`; never `DONE_EXCEPT_HUMAN`.
4. Status text must print **the next action**, not "complete up to the line".
5. Ship a forgery test that turns red if someone puts HUMAN back into the done-set.

## Delegated work that stops early

A delegated run ended "complete" after one stage because the agent read a sensible reason ("a similar product exists") as enough
to stop and the status screen showed only the delegated scope. Fixes that held: (1) completion is verified against the **physical artifacts and
approval fingerprints of every stage**, not the delegation scope; (2) "HOLD is a normal end state" must not be confused with "delegation finished";
(3) a park/HOLD requires a reason, **per-attempt evidence with fingerprints, and explicit resume conditions** (`validate_park`);
(4) a status for delegated mode must say it is *not an executor*; (5) never let HOLD/KILL be approved in place of a GO;
(6) tell "similar apps exist" from "obviously infeasible" by measuring - more competitor research and a real prototype/test, not a shrug.
Regression tests were written to fail on the old behaviour first (unevidenced park accepted; no completion check; HOLD treated as a valid approval of the next stage).

## Reference implementation

`scripts/completion.py` - `status(gates)` returns `DONE`, `AWAITING_<what>` or `BLOCKED`.
`tests/test_completion.py` covers the regression (HUMAN on an instrumented gate must not close it).

```bash
python3 tests/test_completion.py
```
