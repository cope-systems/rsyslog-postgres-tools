from rsyslog_postgres_tools import STATIC_DIR, TEMPLATES_DIR, __version__
from rsyslog_postgres_tools.common.syslog_helpers import SYSLOG_FACILITIES, SYSLOG_PRIORITIES

import bottle
import json


bottle.TEMPLATE_PATH.append(TEMPLATES_DIR)


def attach_view_routes(app, database_pool):
    @app.route("/", name="index_handler")
    def index_handler():
        return bottle.template(
            "index.html.tpl",
            get_url=app.get_url,
            json=json,
            run_script='indexPageSetup({0}, {1}, {2})'.format(
                json.dumps(app.get_url("index_handler") + "api/1.0/"),
                json.dumps(SYSLOG_FACILITIES),
                json.dumps(SYSLOG_PRIORITIES)
            ),
            version=__version__,
            syslog_priorities=SYSLOG_PRIORITIES,
            syslog_facilities=SYSLOG_FACILITIES
        )

    @app.route("/static/<path:path>", name="static_file_handler")
    def static_asset_handler(path):
        return bottle.static_file(path, STATIC_DIR)
