"""Completion rule where HUMAN cannot close an instrumented gate."""
from dataclasses import dataclass
from typing import List, Optional

CLOSED = {"PASS"}


@dataclass
class Gate:
    id: str
    verdict: str                     # PASS / FAIL / NA / EXEMPT / HUMAN / PENDING
    instrumented: bool               # an automated measurement exists for this gate
    exempt_reason: Optional[str] = None
    awaiting: Optional[str] = None   # name of the remaining human/device step, e.g. "DEVICE"


def is_closed(g: Gate) -> bool:
    if g.verdict in ("EXEMPT", "NA"):
        return bool(g.exempt_reason and g.exempt_reason.strip())   # a bare exemption or "not applicable" reopens the hole
    if g.verdict == "HUMAN":
        return not g.instrumented     # only judgment gates with NO instrument may close by HUMAN
    return g.verdict in CLOSED


def status(gates: List[Gate]) -> str:
    if not gates:
        return "BLOCKED: no gates declared (measured nothing is not done)"
    failed = [g for g in gates if g.verdict == "FAIL"]
    if failed:
        return f"BLOCKED: fix {failed[0].id}"
    open_ = [g for g in gates if not is_closed(g)]
    if not open_:
        return "DONE"
    g = open_[0]
    what = g.awaiting or "UNCLAIMED"
    return f"AWAITING_{what}: next -> {g.id} ({len(open_)} open)"


def validate_park(park):
    """Report what is missing before stopping a delegated task early. It checks that the pieces EXIST; it cannot verify that the evidence is true.
    Stopping a delegated task early (HOLD/KILL/park) is legitimate only with evidence and a way back.
    Real incident: an agent treated 'a competitor already exists' as sufficient grounds to stop, then the status showed the
    delegated scope in large letters and nobody verified overall completion. Rules: reason + per-attempt evidence fingerprints +
    explicit resume conditions. 'Similar apps exist' is not 'infeasible' - measure."""
    errs = []
    if not str(park.get("reason", "")).strip(): errs.append("park without a reason")
    ev = park.get("evidence") or []
    if not ev or not all(e.get("attempt") and e.get("fingerprint") for e in ev): errs.append("park needs evidence per attempt (what was tried + fingerprint of the artifact)")
    if not (park.get("resume_conditions") or []): errs.append("park needs resume conditions (what would make this go again)")
    return errs
