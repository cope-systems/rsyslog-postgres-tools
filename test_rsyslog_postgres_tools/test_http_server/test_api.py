from rsyslog_postgres_tools.common.queries import insert_system_event


def test_get_syslog_facilities(syslog_viewer_app):
    resp = syslog_viewer_app.get("/api/1.0/systemEvents/facilities")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert isinstance(resp.json, dict)


def test_get_syslog_priorities(syslog_viewer_app):
    resp = syslog_viewer_app.get("/api/1.0/systemEvents/priorities")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert isinstance(resp.json, dict)


def test_get_unique_syslog_hosts(syslog_viewer_app, initialized_db_connection, fake_system_event_record):
    # Initially there are no system events, so this should be empty.
    resp = syslog_viewer_app.get("/api/1.0/systemEvents/fromHosts")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert isinstance(resp.json, list)
    assert not resp.json

    fake_events = [
        fake_system_event_record.copy(from_host="foo"),
        fake_system_event_record.copy(from_host="baz"),
        fake_system_event_record.copy(from_host="bar")
    ]

    with initialized_db_connection:
        for e in fake_events:
            e.id = insert_system_event(initialized_db_connection, e)

    resp = syslog_viewer_app.get("/api/1.0/systemEvents/fromHosts")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert isinstance(resp.json, list)
    assert len(resp.json) == 3
    for host in ["foo", "bar", "baz"]:
        assert host in resp.json


def test_search_syslog_records(syslog_viewer_app, initialized_db_connection, fake_system_event_record):
    # Initially there are no system events, so this should be empty.
    resp = syslog_viewer_app.get("/api/1.0/systemEvents")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert isinstance(resp.json, list)
    assert not resp.json

    fake_events = [
        fake_system_event_record.copy(message="foo", from_host="foo"),
        fake_system_event_record.copy(message="baz", from_host="baz"),
        fake_system_event_record.copy(message="bar", from_host="bar")
    ]

    with initialized_db_connection:
        for e in fake_events:
            e.id = insert_system_event(initialized_db_connection, e)

    resp = syslog_viewer_app.get("/api/1.0/systemEvents")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert isinstance(resp.json, list)
    assert len(resp.json) == 3
    for o in resp.json:
        assert isinstance(o, dict)
        assert "FromHost" in o
        assert "Message" in o
        assert o["FromHost"] == o["Message"]

    resp = syslog_viewer_app.get("/api/1.0/systemEvents", {"fromHosts": ["foo"]})
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert isinstance(resp.json, list)
    assert len(resp.json) == 1

    resp = syslog_viewer_app.get("/api/1.0/systemEvents", {"fromHosts": ["noneSuch"]})
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert isinstance(resp.json, list)
    assert len(resp.json) == 0
