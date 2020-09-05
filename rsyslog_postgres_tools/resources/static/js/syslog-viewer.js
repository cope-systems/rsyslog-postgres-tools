function indexPageSetup(apiUrl, facilities=null, priorities=null){
    let logOutputList = null;
    let retrievedTimeSpan = null;
    let eventCountSpan = null;
    let availableParametersSpan = null;
    let formatStringInput = null;

    let searchForm = null;
    let searchLimitField = null;
    let searchOffsetField = null;
    let searchMessageFilterField = null;
    let searchSyslogTagFilterField = null;
    let searchFromHostsFilterField = null;
    let searchSyslogFacilitiesFilterField = null;
    let searchSyslogPrioritiesFilterField = null;

    let formatData = {
        logColorScheme: {
            default: '#D8DEE9',
            DeviceReportedTime: '#EC5f67',
            Facility: '#F99157',
            FromHost: '#FAC863',
            Priority: '#99C794',
            SysLogTag: '#5FF3B3',
            ReceivedAt: '#C594C5'
        },
        defaultFormatString: '{DeviceReportedTime} {FromHost} -- {Message:#CDD3DE} : {SysLogTag}',
        dateFormatString: 'YYYY-MM-DD LT'
    };

    function toNull(s){
        return s ? s : null;
    }

    function alterAttributeValue(event, attributeName){
        if(attributeName === 'Priority'){
            let priority = event[attributeName];
            return priorities[priority] || `Unknown (${priority})`;
        }
        else if(attributeName === 'Facility'){
            let facility = event[attributeName];
            return facilities[facility] || `Unkown (${facility})`;
        }
        else if(attributeName === 'ReceivedAt'){
            let receivedAt = moment.utc(event[attributeName]);
            return receivedAt.local().format(formatData.dateFormatString);
        }
        else if(attributeName === 'DeviceReportedTime'){
            let deviceReportedTime = moment.utc(event[attributeName]);
            return deviceReportedTime.local().format(formatData.dateFormatString);
        }
        else {
            return event[attributeName];
        }
    }

    function selectedElementValueArray(e){
        let values = e.find('option:selected').map(function(){ return this.value }).get();
        if(values.includes("all")) return null;
        else return values.filter(v => v !== "all").join(",");
    }

    function eventToItem(event, formatString){
        let str = '<li class="event">';
        let formatStringTokens = formatString.split(/({[A-z0-9#:]+})/);
        for(let token of formatStringTokens) {
            if(/{([A-z0-9]+)}/.test(token)) {
                let attributeName = /{([A-z0-9]+)}/.exec(token)[1];
                let color = formatData.logColorScheme[attributeName] || formatData.logColorScheme.default;
                str += `<span style="color: ${color}">${alterAttributeValue(event, attributeName)}</span>`
            }
            else if(/{([A-z0-9]+):(#[A-z0-9]+)}/.test(token)) {
                let match = /{([A-z0-9]+):(#[A-z0-9]+)}/.exec(token);
                let attributeName = match[1];
                let color = match[2];
                str += `<span style="color: ${color}">${alterAttributeValue(event, attributeName)}</span>`
            }
            else {
                str += `<span style="color: ${formatData.logColorScheme.default}">${token}</span>`;
            }
        }
        return str + "</li>";
    }

    function loadLogs(){
        $.getJSON(
            `${apiUrl}systemEvents`,
            {
              limit: parseInt(searchLimitField.val()),
              offset: parseInt(searchOffsetField.val()),
              messageFilter: toNull(searchMessageFilterField.val()),
              syslogTagFilter: toNull(searchSyslogTagFilterField.val()),
              facilities: selectedElementValueArray(searchSyslogFacilitiesFilterField),
              priorities: selectedElementValueArray(searchSyslogPrioritiesFilterField),
              fromHosts: selectedElementValueArray(searchFromHostsFilterField)
            },
            function(data){
                let formatString = formatStringInput.val();
                data = data.reverse();
                logOutputList.empty();

                for(let event of data){
                    logOutputList.append(eventToItem(event, formatString));
                }
                eventCountSpan.empty();
                eventCountSpan.text(data.length);
                retrievedTimeSpan.empty();
                retrievedTimeSpan.text(new Date().toISOString());
                loadFromHosts();
            }
        );
    }

    function loadFromHosts(){
        $.getJSON(
            `${apiUrl}systemEvents/fromHosts`,
            function(data){
                let previouslySelectedElements = searchFromHostsFilterField.find('option:selected').map(function(){ return this.value }).get();
                searchFromHostsFilterField.empty();
                if(previouslySelectedElements.includes("all")){
                    searchFromHostsFilterField.append("<option value=\"all\" selected>All</option>");
                } else{
                    searchFromHostsFilterField.append("<option value=\"all\">All</option>");
                }

                for(let host of data){
                    let extra = "";
                    if(previouslySelectedElements.includes(host)){
                        extra = "selected";
                    }
                    searchFromHostsFilterField.append(
                        `<option value="${host}"${extra}> ${host}</option>`
                    )
                }
            }
        )
    }

    function setupSearchForm(){
        searchForm.submit(function(e){
            e.preventDefault();
            loadLogs();
        });
    }

    function setupFilterInput(){
        formatStringInput.val(formatData.defaultFormatString);
    }

    function fetchAvailableParameters(){
        $.getJSON(
            `${apiUrl}swagger.json`,
            function(data){
                let parameters = Object.keys(data.definitions.SystemEvent.properties);
                availableParametersSpan.empty();
                availableParametersSpan.text(parameters.join(", "))
            }
        )
    }


    $(document).ready(function(){
        logOutputList = $("#logs-list");
        retrievedTimeSpan = $("#retrieved-time");
        eventCountSpan = $("#event-count");
        availableParametersSpan = $("#available-parameters");
        formatStringInput = $("#format-string");

        searchForm = $("#search-form");
        searchLimitField = $("#search-limit");
        searchOffsetField = $("#search-offset");
        searchMessageFilterField = $("#search-message-filter");
        searchSyslogTagFilterField = $("#search-syslog-tag-filter");
        searchFromHostsFilterField = $("#search-from-hosts");
        searchSyslogFacilitiesFilterField = $("#search-syslog-facilities");
        searchSyslogPrioritiesFilterField = $("#search-syslog-priorities");

        setupFilterInput();
        fetchAvailableParameters();
        setupSearchForm();
        loadLogs();
    });
}