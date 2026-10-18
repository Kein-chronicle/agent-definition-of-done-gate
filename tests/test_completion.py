import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from completion import Gate, status

def expect(name, got, prefix):
    ok = got.startswith(prefix)
    print(("ok   " if ok else "FAIL ") + f"{name}: {got}")
    return ok

r = []
r.append(expect("all pass", status([Gate("a", "PASS", True)]), "DONE"))
r.append(expect("empty gate list is not done", status([]), "BLOCKED"))
# regression: HUMAN on an instrumented gate (e.g. ad id is still a test id) must NOT close it
r.append(expect("HUMAN on instrumented gate stays open",
                status([Gate("ads-real-id", "HUMAN", True, awaiting="CONSOLE")]), "AWAITING_CONSOLE"))
r.append(expect("HUMAN on judgment-only gate may close",
                status([Gate("tone-ok", "HUMAN", False)]), "DONE"))
r.append(expect("bare exemption stays open", status([Gate("x", "EXEMPT", True, exempt_reason=" ")]), "AWAITING_UNCLAIMED"))
r.append(expect("exemption with reason closes", status([Gate("x", "EXEMPT", True, exempt_reason="vendored")]), "DONE"))
r.append(expect("FAIL blocks", status([Gate("a", "PASS", True), Gate("b", "FAIL", True)]), "BLOCKED"))
r.append(expect("NA without a reason stays open", status([Gate("x", "NA", True)]), "AWAITING_UNCLAIMED"))
r.append(expect("NA with a reason closes", status([Gate("x", "NA", True, exempt_reason="feature removed")]), "DONE"))
from completion import validate_park
r.append(expect("park with no evidence is refused", ",".join(validate_park({"reason": "competitor exists"})), "park needs evidence per attempt (what was tried + fingerprint of the artifact),park needs resume conditions (what would make this go again)"))
r.append(expect("park with reason, evidence and resume conditions is accepted", str(validate_park({"reason": "demand unproven", "evidence": [{"attempt": "survey", "fingerprint": "ab12"}], "resume_conditions": ["a source of demand data"]})), "[]"))
sys.exit(0 if all(r) else 1)
