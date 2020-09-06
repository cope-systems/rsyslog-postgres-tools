def test_get_base_url(syslog_viewer_app):
    resp = syslog_viewer_app.get("/")
    assert resp.status_code == 200
    assert resp.content_type == "text/html"


def test_get_static_assets(syslog_viewer_app):
    resp = syslog_viewer_app.get("/static/css/syslog-viewer.css")
    assert resp.status_code == 200

