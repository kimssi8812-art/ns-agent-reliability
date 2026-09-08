from ns_agent_reliability.leases import LeaseError, LeaseRegistry


def test_released_lease_can_be_reacquired_while_old_session_is_alive():
    sessions_alive = {"client-a", "client-b"}
    leases = LeaseRegistry()

    a = leases.acquire("run-1", "client-a", now=10.0, ttl_seconds=60.0)
    leases.release("run-1", "client-a", a.epoch)

    assert "client-a" in sessions_alive
    b = leases.acquire("run-1", "client-b", now=20.0, ttl_seconds=60.0)
    assert b.epoch == a.epoch + 1
    assert b.holder_session_id == "client-b"


def test_unexpired_foreign_lease_cannot_be_stolen():
    leases = LeaseRegistry()
    leases.acquire("run-1", "client-a", now=10.0, ttl_seconds=60.0)

    try:
        leases.acquire("run-1", "client-b", now=20.0, ttl_seconds=60.0)
    except LeaseError as exc:
        assert str(exc) == "ACTIVE_LEASE_HELD_BY_OTHER_SESSION"
    else:
        raise AssertionError("an active foreign lease must not be stolen")


def test_expired_lease_can_be_reacquired_without_closing_old_session():
    sessions_alive = {"client-a", "client-b"}
    leases = LeaseRegistry()

    a = leases.acquire("run-1", "client-a", now=10.0, ttl_seconds=5.0)
    assert "client-a" in sessions_alive
    b = leases.acquire("run-1", "client-b", now=16.0, ttl_seconds=30.0)

    assert b.epoch == a.epoch + 1


def test_old_holder_is_rejected_after_new_epoch_is_acquired():
    leases = LeaseRegistry()
    a = leases.acquire("run-1", "client-a", now=10.0, ttl_seconds=5.0)
    b = leases.acquire("run-1", "client-b", now=16.0, ttl_seconds=30.0)

    try:
        leases.authorize("run-1", "client-a", a.epoch, now=17.0)
    except LeaseError as exc:
        assert str(exc) in {"LEASE_HOLDER_MISMATCH", "STALE_FENCING_EPOCH"}
    else:
        raise AssertionError("a stale holder must be fenced after reacquire")

    assert leases.authorize("run-1", "client-b", b.epoch, now=17.0) == b


def test_same_holder_reacquire_after_expiry_advances_epoch():
    leases = LeaseRegistry()
    first = leases.acquire("run-1", "client-a", now=10.0, ttl_seconds=5.0)
    second = leases.acquire("run-1", "client-a", now=16.0, ttl_seconds=5.0)

    assert second.epoch == first.epoch + 1


def test_checkpoint_safe_finish_releases_immediately_without_waiting_for_ttl():
    leases = LeaseRegistry()
    a = leases.acquire("run-1", "client-a", now=10.0, ttl_seconds=900.0)

    finished = leases.finish("run-1", "client-a", a.epoch, checkpoint_safe=True)
    assert finished.released is True

    b = leases.acquire("run-1", "client-b", now=11.0, ttl_seconds=60.0)
    assert b.epoch == a.epoch + 1
    assert b.holder_session_id == "client-b"


def test_finish_requires_checkpoint_safe_and_does_not_weaken_active_lease():
    leases = LeaseRegistry()
    a = leases.acquire("run-1", "client-a", now=10.0, ttl_seconds=900.0)

    try:
        leases.finish("run-1", "client-a", a.epoch, checkpoint_safe=False)
    except LeaseError as exc:
        assert str(exc) == "WORKFLOW_FINISH_REQUIRES_CHECKPOINT_SAFE"
    else:
        raise AssertionError("finish must require checkpoint-safe completion")

    assert leases.authorize("run-1", "client-a", a.epoch, now=11.0) == a
