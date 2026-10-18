import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from completion import Gate, status, validate_park

print("all pass              ->", status([Gate("build", "PASS", True), Gate("tests", "PASS", True)]))
print("nothing declared      ->", status([]))
print("HUMAN on measured gate->", status([Gate("real-ad-id", "HUMAN", True, awaiting="CONSOLE")]))
print("HUMAN on judgment gate->", status([Gate("tone-ok", "HUMAN", False)]))
print("bare exemption        ->", status([Gate("legacy", "EXEMPT", True, exempt_reason=" ")]))
print("reasoned exemption    ->", status([Gate("legacy", "EXEMPT", True, exempt_reason="vendored; upstream owns it")]))
print("one FAIL              ->", status([Gate("a", "PASS", True), Gate("b", "FAIL", True)]))
print()
print("park without evidence ->", validate_park({"reason": "a competitor exists"}))
print("park with a way back  ->", validate_park({"reason": "demand unproven", "evidence": [{"attempt": "survey of 40 users", "fingerprint": "ab12"}], "resume_conditions": ["10 paying testers"]}))
