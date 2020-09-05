import syslog

SYSLOG_PRIORITIES = {
    syslog.LOG_EMERG: "Emergency",
    syslog.LOG_ALERT: "Alert",
    syslog.LOG_CRIT: "Critical",
    syslog.LOG_ERR: "Error",
    syslog.LOG_WARNING: "Warning",
    syslog.LOG_NOTICE: "Notice",
    syslog.LOG_INFO: "Info",
    syslog.LOG_DEBUG: "Debug"
}

SYSLOG_FACILITIES = {
    syslog.LOG_KERN//8: "Kernel Messages",
    syslog.LOG_USER//8: "User-Level Messages",
    syslog.LOG_MAIL//8: "Mail Daemon",
    syslog.LOG_DAEMON//8: "Daemon Logs",
    syslog.LOG_AUTH//8: "Auth Logs",
    syslog.LOG_LPR//8: "Line Print (LPR) Logs",
    syslog.LOG_NEWS//8: "Network News Logs",
    syslog.LOG_UUCP//8: "UUCP Logs",
    syslog.LOG_CRON//8: "Cron Logs",
    syslog.LOG_SYSLOG//8: "Internal Syslog Logs",
    10: "Security/Authentication Messages",
    11: "FTP Messages",
    12: "NTP Messages",
    13: "Log Audit",
    14: "Log Alert",
    15: "Solaris Cron",
    syslog.LOG_LOCAL0//8: "Local0",
    syslog.LOG_LOCAL1//8: "Local1",
    syslog.LOG_LOCAL2//8: "Local2",
    syslog.LOG_LOCAL3//8: "Local3",
    syslog.LOG_LOCAL4//8: "Local4",
    syslog.LOG_LOCAL5//8: "Local5",
    syslog.LOG_LOCAL6//8: "Local6",
    syslog.LOG_LOCAL7//8: "Local7"
}