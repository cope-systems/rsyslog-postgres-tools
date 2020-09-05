<html>
    <head>
        <title>{{ title or 'Syslog Viewer' }}</title>
        <link rel="stylesheet" type="text/css" href="{{ get_url("static_file_handler", path="css/bootstrap.css") }}"/>
        <link rel="stylesheet" type="text/css" href="{{ get_url("static_file_handler", path="css/syslog-viewer.css") }}"/>
        <script src="{{ get_url("static_file_handler", path="js/popper.min.js") }}"></script>
        <script src="{{ get_url("static_file_handler", path="js/jquery-3.4.1.min.js") }}"></script>
        <script src="{{ get_url("static_file_handler", path="js/bootstrap.js") }}"></script>
        <script src="{{ get_url("static_file_handler", path="js/syslog-viewer.js") }}"></script>
        <script src="{{ get_url("static_file_handler", path="js/moment-with-locales.min.js") }}"></script>
        <script>{{! run_script or '' }}</script>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="{{ get_url("index_handler") }}">Syslog Viewer</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                  <li class="nav-item">
                    <a class="nav-link" href="{{ get_url("index_handler") }}">Log Viewer</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="{{ get_url("index_handler") + "api/1.0/ui/" }}">API Docs</a>
                  </li>
                </ul>
            </div>
        </nav>
        {{! base }}
        <div class="navbar footer fixed-bottom">
            <p><i>rsyslog-postgres-tools</i> Syslog Viewer Version ({{ version or '???'}}) 2020 -- Cope Systems</p>
        </div>
    </body>
</html>