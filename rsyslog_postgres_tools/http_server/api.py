from rsyslog_postgres_tools.common.queries import search_system_events, \
    select_distinct_hosts_from_system_events
from rsyslog_postgres_tools.common.eventlet_pg import get_pool_connection
from rsyslog_postgres_tools.common.syslog_helpers import SYSLOG_FACILITIES, SYSLOG_PRIORITIES
from bottle import request


def attach_api_routes(app, database_pool):
    @app.route("/api/1.0/systemEvents", method=["GET"], name="search_system_events")
    def search_system_events_api():
        with get_pool_connection(database_pool) as conn:
            with conn:
                swagger_data = request.swagger_data
                facilities = swagger_data.get("facilities")
                priorities = swagger_data.get("priorities")
                from_hosts = swagger_data.get("fromHosts")
                event_sources = swagger_data.get("eventSources")
                message_filter = swagger_data.get("messageFilter")
                syslog_tag_filter = swagger_data.get("syslogTagFilter")
                start_received_at = swagger_data.get("startReceivedAt")
                end_receieved_at = swagger_data.get("endReceivedAt")
                start_device_reported_time = swagger_data.get("startDeviceReportedTime")
                end_device_reported_time = swagger_data.get("endDeviceReportedTime")
                limit = swagger_data.get('limit')
                offset = swagger_data.get('offset')
                system_events = search_system_events(
                    conn,
                    opt_facility=facilities,
                    opt_priority=priorities,
                    opt_from_host=from_hosts,
                    opt_event_source=event_sources,
                    opt_message_search=message_filter,
                    opt_syslog_tag_search=syslog_tag_filter,
                    opt_start_received_at=start_received_at,
                    opt_end_received_at=end_receieved_at,
                    opt_start_device_reported_time=start_device_reported_time,
                    opt_end_device_reported_time=end_device_reported_time,
                    limit=limit,
                    offset=offset
                )
            return [s.to_api_response() for s in system_events]

    @app.route("/api/1.0/systemEvents/fromHosts", method=["GET"], name="get_system_events_unique_hosts")
    def get_system_events_unique_hosts_api():
        with get_pool_connection(database_pool) as conn:
            with conn:
                swagger_data = request.swagger_data
                queued = select_distinct_hosts_from_system_events(
                    conn,
                    limit=swagger_data.get('limit'),
                    offset=swagger_data.get('offset')
                )
                return queued

    @app.route("/api/1.0/systemEvents/facilities", method=["GET"], name="get_syslog_facilities")
    def get_syslog_facilities_api():
        return SYSLOG_FACILITIES

    @app.route("/api/1.0/systemEvents/priorities", method=["GET"], name="get_syslog_priorities")
    def get_syslog_priorities_api():
        return SYSLOG_PRIORITIES
