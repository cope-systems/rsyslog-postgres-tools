from string import Template


def opt_isoformat(field):
    if field:
        return field.isoformat()
    else:
        return field


DEFAULT_SYSTEM_EVENT_TEMPLATE_STR = "[$DeviceReportedTime] $FromHost -- $Message : $SysLogTag"


class SystemEventRecord(object):
    def __init__(
        self, id, customer_id, received_at, device_reported_time, facility, priority, from_host, message, nt_severity,
        importance, event_source, event_user, event_category, event_id, event_binary_data, max_available, curr_usage,
        min_usage, max_usage, info_unit_id, sys_log_tag, event_log_type, generic_file_name
    ):
        """
        SystemeventsRecord database record type.
        :param id: serial
            Database Modifier:  not null primary key
        :param customer_id: bigint
            Database Modifier:
        :param received_at: timestamp
            Database Modifier:  without time zone null
        :param device_reported_time: timestamp
            Database Modifier:  without time zone null
        :param facility: smallint
            Database Modifier:  null
        :param priority: smallint
            Database Modifier:  null
        :param from_host: varchar(60)
            Database Modifier:  null
        :param message: text
            Database Modifier:
        :param nt_severity: int
            Database Modifier:  null
        :param importance: int
            Database Modifier:  null
        :param event_source: varchar(60)
            Database Modifier:
        :param event_user: varchar(60)
            Database Modifier:  null
        :param event_category: int
            Database Modifier:  null
        :param event_id: int
            Database Modifier:  null
        :param event_binary_data: text
            Database Modifier:  null
        :param max_available: int
            Database Modifier:  null
        :param curr_usage: int
            Database Modifier:  null
        :param min_usage: int
            Database Modifier:  null
        :param max_usage: int
            Database Modifier:  null
        :param info_unit_id: int
            Database Modifier:  null
        :param sys_log_tag: varchar(60)
            Database Modifier:
        :param event_log_type: varchar(60)
            Database Modifier:
        :param generic_file_name: varchar(60)
            Database Modifier:
        """
        self.id = id
        self.customer_id = customer_id
        self.received_at = received_at
        self.device_reported_time = device_reported_time
        self.facility = facility
        self.priority = priority
        self.from_host = from_host
        self.message = message
        self.nt_severity = nt_severity
        self.importance = importance
        self.event_source = event_source
        self.event_user = event_user
        self.event_category = event_category
        self.event_id = event_id
        self.event_binary_data = event_binary_data
        self.max_available = max_available
        self.curr_usage = curr_usage
        self.min_usage = min_usage
        self.max_usage = max_usage
        self.info_unit_id = info_unit_id
        self.sys_log_tag = sys_log_tag
        self.event_log_type = event_log_type
        self.generic_file_name = generic_file_name

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        else:
            return cls(
                id=row['ID'],
                customer_id=row['CustomerID'],
                received_at=row['ReceivedAt'],
                device_reported_time=row['DeviceReportedTime'],
                facility=row['Facility'],
                priority=row['Priority'],
                from_host=row['FromHost'],
                message=row['Message'],
                nt_severity=row['NTSeverity'],
                importance=row['Importance'],
                event_source=row['EventSource'],
                event_user=row['EventUser'],
                event_category=row['EventCategory'],
                event_id=row['EventID'],
                event_binary_data=row['EventBinaryData'],
                max_available=row['MaxAvailable'],
                curr_usage=row['CurrUsage'],
                min_usage=row['MinUsage'],
                max_usage=row['MaxUsage'],
                info_unit_id=row['InfoUnitID'],
                sys_log_tag=row['SysLogTag'],
                event_log_type=row['EventLogType'],
                generic_file_name=row['GenericFileName']
            )

    def copy(self, **kwargs):
        return SystemEventRecord(
            id=kwargs.get('id', self.id),
            customer_id=kwargs.get('customer_id', self.customer_id),
            received_at=kwargs.get('received_at', self.received_at),
            device_reported_time=kwargs.get('device_reported_time', self.device_reported_time),
            facility=kwargs.get('facility', self.facility),
            priority=kwargs.get('priority', self.priority),
            from_host=kwargs.get('from_host', self.from_host),
            message=kwargs.get('message', self.message),
            nt_severity=kwargs.get('nt_severity', self.nt_severity),
            importance=kwargs.get('importance', self.importance),
            event_source=kwargs.get('event_source', self.event_source),
            event_user=kwargs.get('event_user', self.event_user),
            event_category=kwargs.get('event_category', self.event_category),
            event_id=kwargs.get('event_id', self.event_id),
            event_binary_data=kwargs.get('event_binary_data', self.event_binary_data),
            max_available=kwargs.get('max_available', self.max_available),
            curr_usage=kwargs.get('curr_usage', self.curr_usage),
            min_usage=kwargs.get('min_usage', self.min_usage),
            max_usage=kwargs.get('max_usage', self.max_usage),
            info_unit_id=kwargs.get('info_unit_id', self.info_unit_id),
            sys_log_tag=kwargs.get('sys_log_tag', self.sys_log_tag),
            event_log_type=kwargs.get('event_log_type', self.event_log_type),
            generic_file_name=kwargs.get('generic_file_name', self.generic_file_name)
        )

    def to_row(self):
        return {
            'ID': self.id,
            'CustomerID': self.customer_id,
            'ReceivedAt': self.received_at,
            'DeviceReportedTime': self.device_reported_time,
            'Facility': self.facility,
            'Priority': self.priority,
            'FromHost': self.from_host,
            'Message': self.message,
            'NTSeverity': self.nt_severity,
            'Importance': self.importance,
            'EventSource': self.event_source,
            'EventUser': self.event_user,
            'EventCategory': self.event_category,
            'EventID': self.event_id,
            'EventBinaryData': self.event_binary_data,
            'MaxAvailable': self.max_available,
            'CurrUsage': self.curr_usage,
            'MinUsage': self.min_usage,
            'MaxUsage': self.max_usage,
            'InfoUnitID': self.info_unit_id,
            'SysLogTag': self.sys_log_tag,
            'EventLogType': self.event_log_type,
            'GenericFileName': self.generic_file_name
        }

    def to_api_response(self):
        return {
            'ID': self.id,
            'CustomerID': self.customer_id,
            'ReceivedAt': opt_isoformat(self.received_at),
            'DeviceReportedTime': opt_isoformat(self.device_reported_time),
            'Facility': self.facility,
            'Priority': self.priority,
            'FromHost': self.from_host,
            'Message': self.message,
            'NTSeverity': self.nt_severity,
            'Importance': self.importance,
            'EventSource': self.event_source,
            'EventUser': self.event_user,
            'EventCategory': self.event_category,
            'EventID': self.event_id,
            'EventBinaryData': self.event_binary_data,
            'MaxAvailable': self.max_available,
            'CurrUsage': self.curr_usage,
            'MinUsage': self.min_usage,
            'MaxUsage': self.max_usage,
            'InfoUnitID': self.info_unit_id,
            'SysLogTag': self.sys_log_tag,
            'EventLogType': self.event_log_type,
            'GenericFileName': self.generic_file_name
        }

    def format(self, format_str):
        return Template(format_str).substitute(self.to_api_response())


class SystemEventsPropertyRecord(object):
    def __init__(self, id, system_event_id, param_name):
        """
        SystemeventspropertiesRecord database record type.
        :param id: serial
            Database Modifier:  not null primary key
        :param system_event_id: int
            Database Modifier:  null
        :param param_name: varchar(255)
            Database Modifier:  null
        """
        self.id = id
        self.system_event_id = system_event_id
        self.param_name = param_name

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None
        else:
            return cls(
                id=row['ID'],
                system_event_id=row['SystemEventID'],
                param_name=row['ParamName']
            )

    def copy(self, **kwargs):
        return SystemEventsPropertyRecord(
            id=kwargs.get('id', self.id),
            system_event_id=kwargs.get('system_event_id', self.system_event_id),
            param_name=kwargs.get('param_name', self.param_name)
        )

    def to_row(self):
        return {
            'ID': self.id,
            'SystemEventID': self.system_event_id,
            'ParamName': self.param_name
        }

    def to_api_response(self):
        return {
            'ID': self.id,
            'SystemEventID': self.system_event_id,
            'ParamName': self.param_name
        }
