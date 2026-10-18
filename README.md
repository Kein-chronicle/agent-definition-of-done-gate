# agent-definition-of-done-gate

**A completion rule for AI agents: a human can't close a gate that has an automated measurement, and parking work needs evidence.**

[![test](https://github.com/Kein-chronicle/agent-definition-of-done-gate/actions/workflows/test.yml/badge.svg)](https://github.com/Kein-chronicle/agent-definition-of-done-gate/actions/workflows/test.yml) ![license](https://img.shields.io/badge/license-MIT-blue.svg) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

## Why

If "waiting for a human" counts as done, a pipeline reports completion with a test ad id still in the build. This module makes `HUMAN` close only gates that have no instrument, requires a reason for every exemption or `NA`, and lists what is missing when an agent wants to stop early without evidence and a way back.

## Install

**As a Claude Code skill** (Claude uses it when the task matches the skill description):

```sh
git clone https://github.com/Kein-chronicle/agent-definition-of-done-gate.git ~/.claude/skills/done-state-honesty
```

For a single project, clone into `<project>/.claude/skills/done-state-honesty` instead, then start a new Claude Code session.

**As a library** (Python 3.10+, standard library only): copy `scripts/completion.py` into your project, or put the `scripts/` folder on `sys.path`:

```python
import sys; sys.path.insert(0, 'path/to/agent-definition-of-done-gate/scripts')
import completion
```

**From source:**

```sh
git clone https://github.com/Kein-chronicle/agent-definition-of-done-gate.git
cd agent-definition-of-done-gate
```

**Requires:** Python 3.10+.

## Quick start

Run the quickstart:

```console
$ python3 examples/quickstart.py
all pass              -> DONE
nothing declared      -> BLOCKED: no gates declared (measured nothing is not done)
HUMAN on measured gate-> AWAITING_CONSOLE: next -> real-ad-id (1 open)
HUMAN on judgment gate-> DONE
bare exemption        -> AWAITING_UNCLAIMED: next -> legacy (1 open)
reasoned exemption    -> DONE
one FAIL              -> BLOCKED: fix b

park without evidence -> ['park needs evidence per attempt (what was tried + fingerprint of the artifact)', 'park needs resume conditions (what would make this go again)']
park with a way back  -> []
```

The output above is real: it is produced by the files in `examples/`.

## What it checks

- `status(gates)` returns `DONE`, `BLOCKED: ...` or `AWAITING_<what>: next -> <gate>`.
- An empty gate list is `BLOCKED` (measuring nothing is not done).
- `validate_park(park)` returns the missing pieces: a reason, per-attempt evidence with a fingerprint, resume conditions. It checks that they exist; it cannot verify the evidence is true.

## Limits

- Pure decision logic; you wire it to your own gate list.

## Related projects

These solve neighbouring problems; use them when they fit better.

- **GitHub required reviews / checks**: gate automated checks and approvals but not the HUMAN-versus-instrumented distinction

## More from the same collection

Small, tested tools that grew out of running AI agents and game/app pipelines for months:

- [**llm-verdict-gate**](https://github.com/Kein-chronicle/llm-verdict-gate): Make AI and human review gates impossible to pass by silence: machine-parsed PASS/FAIL, missing verdict = FAIL.
- [**ci-gate-forgery-test**](https://github.com/Kein-chronicle/ci-gate-forgery-test): Prove your CI gates can actually fail: feed each gate forged-bad, empty and missing input and flag the ones that stay green.
- [**stale-verdict-guard**](https://github.com/Kein-chronicle/stale-verdict-guard): Bind a pass/fail verdict to a fingerprint of the source it judged, so an edit after review makes the verdict stale.

## Development

```sh
python3 tests/test_completion.py
```

The tests include inputs that are supposed to be rejected, so a green run also shows the checks can fail. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

If this saved you a debugging session, a star helps other people find it. Bug reports and failing test cases are even better.

<sub>Keywords: ai-agents, agent-skills, claude-code, claude-skills, definition-of-done, quality-gates, workflow</sub>
