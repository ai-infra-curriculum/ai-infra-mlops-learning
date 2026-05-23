from src.audit import AuditChain


def test_chain_verifies_clean():
    c = AuditChain()
    for i in range(10):
        c.append("test", "actor", {"i": i})
    ok, broken = c.verify()
    assert ok and broken is None


def test_chain_detects_tampering():
    c = AuditChain()
    c.append("a", "x", {"v": 1})
    c.append("b", "x", {"v": 2})
    # Tamper with event 0
    bad = c._events[0]
    c._events[0] = type(bad)(**{**bad.__dict__, "actor": "evil"})
    ok, broken = c.verify()
    assert not ok and broken == 0


def test_prev_hash_chains():
    c = AuditChain()
    e1 = c.append("a", "x", {})
    e2 = c.append("b", "x", {})
    assert e2.prev_hash == e1.this_hash
