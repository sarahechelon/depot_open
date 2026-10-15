from app import flags


def test_flag_defaults_to_off(monkeypatch: object) -> None:
    monkeypatch.delenv("DEPOT_FLAG_WEBHOOKS", raising=False)
    assert flags.is_enabled("webhooks") is False


def test_flag_can_be_enabled(monkeypatch: object) -> None:
    monkeypatch.setenv("DEPOT_FLAG_WEBHOOKS", "true")
    assert flags.is_enabled("webhooks") is True


def test_unknown_flag_raises() -> None:
    try:
        flags.is_enabled("does_not_exist")
    except ValueError as exc:
        assert "unknown feature flag" in str(exc)
    else:
        raise AssertionError("expected ValueError")
