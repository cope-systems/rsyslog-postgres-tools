from rsyslog_postgres_tools.common.models import SystemEventRecord
from rsyslog_postgres_tools import MIGRATIONS_DIR
from yoyo import read_migrations, get_backend


BASE_SYSTEM_EVENT_SELECT = """
SELECT id, customerid, receivedat, devicereportedtime, facility, priority, fromhost, message, 
  ntseverity, importance,
  eventsource, eventuser, eventcategory, eventid, eventbinarydata, maxavailable, 
  currusage, minusage, maxusage, infounitid, syslogtag, eventlogtype, genericfilename 
FROM SystemEvents
"""


def migrate_database_up(connection_url):
    backend = get_backend(connection_url)
    migrations = read_migrations(MIGRATIONS_DIR)

    with backend.lock(60):
        backend.apply_migrations(backend.to_apply(migrations))


def search_system_events(connection, opt_facility=None, opt_priority=None, opt_from_host=None,
                         opt_event_source=None, opt_syslog_tag_search=None,
                         opt_message_search=None, opt_start_received_at=None,
                         opt_end_received_at=None, opt_start_device_reported_time=None,
                         opt_end_device_reported_time=None, limit=None, offset=None):
    where_clauses = []
    params = []
    
    if opt_facility:
        where_clauses.append(" Facility=ANY(%s) ")
        params.append(opt_facility)
    if opt_priority:
        where_clauses.append(" Priority=ANY(%s) ")
        params.append(opt_priority)
    if opt_from_host:
        where_clauses.append(" FromHost=ANY(%s) ")
        params.append(opt_from_host)
    if opt_event_source:
        where_clauses.append(" EventSource=ANY(%s) ")
        params.append(opt_event_source)
    if opt_syslog_tag_search:
        where_clauses.append(" SysLogTag SIMILAR TO %s ")
        params.append(opt_syslog_tag_search)
    if opt_message_search:
        where_clauses.append(" Message SIMILAR TO %s ")
        params.append(opt_message_search)
    if opt_start_received_at:
        where_clauses.append(" ReceivedAt >= %s")
        params.append(opt_start_received_at)
    if opt_end_received_at:
        where_clauses.append(" ReceivedAt <= %s")
        params.append(opt_end_received_at)
    if opt_start_device_reported_time:
        where_clauses.append(" DeviceReportedTime >= %s ")
        params.append(opt_start_device_reported_time)
    if opt_end_device_reported_time:
        where_clauses.append(" DeviceReportedTime <= %s ")
        params.append(opt_end_device_reported_time)

    if where_clauses:
        clause = " WHERE " + " AND ".join(where_clauses)
    else:
        clause = ""
        
    clause += " ORDER BY DeviceReportedTime DESC LIMIT %s OFFSET %s "
    params.extend([limit, offset])
    
    with connection.cursor() as c:
        c.execute(
            BASE_SYSTEM_EVENT_SELECT + clause,
            params
        )
        return [SystemEventRecord.from_row(r) for r in c.fetchall()]


def select_latest_events(connection, min_received_at=None, limit=None, offset=None):
    params = []
    clause = ""
    if min_received_at:
        clause += " WHERE ReceivedAt > %s "
        params.append(min_received_at)

    clause += " ORDER BY DeviceReportedTime DESC LIMIT %s OFFSET %s "
    params.extend([limit, offset])
    with connection.cursor() as c:
        c.execute(
            BASE_SYSTEM_EVENT_SELECT + clause,
            params
        )
        return [SystemEventRecord.from_row(r) for r in c.fetchall()]


def select_system_event_by_id(connection, system_event_id):
    with connection.cursor() as c:
        c.execute(BASE_SYSTEM_EVENT_SELECT + " WHERE id = %s", (system_event_id,))
        return SystemEventRecord.from_row(c.fetchone())


def select_distinct_hosts_from_system_events(connection, limit=None, offset=None):
    with connection.cursor() as c:
        c.execute(
            "SELECT DISTINCT fromhost FROM SystemEvents ORDER BY fromHost LIMIT %s OFFSET %s",
            (limit, offset)
        )
        return [r['fromhost'] for r in c.fetchall()]


def insert_system_event(transaction, system_event):
    if not isinstance(system_event, SystemEventRecord):
        raise TypeError("system_event is not of type SystemEventRecord!")
    with transaction.cursor() as c:
        c.execute("""
        INSERT INTO SystemEvents(
            customerid, receivedat, devicereportedtime, facility, priority, fromhost, 
            message, ntseverity, importance,
            eventsource, eventuser, eventcategory, eventid, eventbinarydata, maxavailable, 
            currusage, minusage, maxusage, infounitid, syslogtag, 
            eventlogtype, genericfilename 
        ) VALUES (
            %(CustomerID)s, %(ReceivedAt)s, %(DeviceReportedTime)s, %(Facility)s, 
            %(Priority)s, %(FromHost)s, %(Message)s, %(NTSeverity)s, %(Importance)s,
            %(EventSource)s, %(EventUser)s, %(EventCategory)s, %(EventID)s, 
            %(EventBinaryData)s, %(MaxAvailable)s, %(CurrUsage)s, %(MinUsage)s, 
            %(MaxUsage)s, %(InfoUnitID)s, %(SysLogTag)s, %(EventLogType)s, %(GenericFileName)s
        ) RETURNING id
        """, system_event.to_row())
        return c.fetchone()["id"]


def delete_system_event(transaction, system_event):
    if isinstance(system_event, SystemEventRecord):
        event_id = system_event.id
    else:
        event_id = system_event
    with transaction.cursor() as c:
        c.execute("DELETE FROM SystemEvents WHERE id = %s", (event_id,))


def delete_old_system_events(transaction, how_old):
    with transaction.cursor() as c:
        c.execute(
            "DELETE FROM SystemEvents WHERE ReceivedAt < NOW() - INTERVAL %s",
            (how_old,)
        )
        return c.rowcount
