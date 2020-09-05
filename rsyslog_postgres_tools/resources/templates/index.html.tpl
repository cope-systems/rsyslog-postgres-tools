% rebase('base.tpl', title='Syslog Viewer')
<div class="container logsys-container">
    <div class="row">
        <div class="col">
            <h1>System Logs</h1>
            <div id="logs-container" class="logs-container">
                <ul id="logs-list" class="logs-list">

                </ul>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col">
        <span id="event-count"></span> events retrieved at <span id="retrieved-time">???</span>
        </div>
    </div>
    <div class="row">
        <div class="col">
            <h3>Log Format</h3>
            <input type="text" id="format-string">
            <p>Available parameters: <span id="available-parameters"></span></p>
        </div>
    </div>
    <div class="row">
        <div class="col">
            <h3>Search</h3>
            <form id="search-form">
              <div class="form-row">
                <div class="form-group col">
                    <label for="search-limit">Limit:</label>
                    <input type="number" step="1" id="search-limit" class="form-control" name="limit" value="500">
                </div>
                <div class="form-group col">
                    <label for="search-offset">Offset:</label>
                    <input type="number" step="1" id="search-offset" class="form-control" name="offset" value="0">
                </div>
                <div class="form-group col">
                    <label for="search-message-filter">Message Filter:</label>
                    <input type="text" id="search-message-filter" class="form-control" name="messageFilter" value="">
                </div>
                <div class="form-group col">
                    <label for="search-syslog-tag-filter">Syslog Tag Filter:</label>
                    <input type="text" id="search-syslog-tag-filter" class="form-control" name="syslogTagFilter" value="">
                </div>
              </div>
              <div class="form-row">
                <div class="form-group col">
                    <label for="search-from-hosts">From Hostnames:</label>
                    <select id="search-from-hosts" class="form-control" name="fromHosts" multiple>
                        <option value="all" selected>All</option>
                    </select>
                </div>
                <div class="form-group col">
                    <label for="search-syslog-facilities">Syslog Facilities:</label>
                    <select id="search-syslog-facilities" class="form-control" name="syslogFacilities" multiple>
                        <option value="all" selected>All</option>
                        % for facility_num, facility_description in sorted(syslog_facilities.items()):
                        <option value="{{ facility_num }}">{{ facility_description }} ({{facility_num}})</option>
                        % end
                    </select>
                </div>
                <div class="form-group col">
                    <label for="search-syslog-priorities">Syslog Priorities:</label>
                    <select id="search-syslog-priorities" class="form-control" name="syslogPriorities" multiple>
                        <option value="all" selected>All</option>
                        % for priority_num, priority_description in sorted(syslog_priorities.items()):
                        <option value="{{ priority_num }}">{{ priority_description }} ({{priority_num}})</option>
                        % end
                    </select>
                </div>
              </div>
              <div class="form-row">
                <div class="col">
                    <button type="submit" id="search-button" class="btn btn-block btn-primary">Search</button>
                </div>
              </div>
            </form>
        </div>
    </div>
</div>