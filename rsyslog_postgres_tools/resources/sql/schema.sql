CREATE TABLE SystemEvents
(
  ID serial not null primary key,
  CustomerID bigint,
  ReceivedAt timestamp without time zone NULL,
  DeviceReportedTime timestamp without time zone NULL,
  Facility smallint NULL,
  Priority smallint NULL,
  FromHost varchar(60) NULL,
  Message text,
  NTSeverity int NULL,
  Importance int NULL,
  EventSource varchar(60),
  EventUser varchar(60) NULL,
  EventCategory int NULL,
  EventID int NULL,
  EventBinaryData text NULL,
  MaxAvailable int NULL,
  CurrUsage int NULL,
  MinUsage int NULL,
  MaxUsage int NULL,
  InfoUnitID int NULL ,
  SysLogTag varchar(60),
  EventLogType varchar(60),
  GenericFileName VarChar(60),
  SystemID int NULL
);

CREATE INDEX IF NOT EXISTS SystemEvents_ReceivedAt_IDX ON SystemEvents(ReceivedAt);
CREATE INDEX IF NOT EXISTS SystemEvents_DeviceReportedTime_IDX ON SystemEvents(DeviceReportedTime);
CREATE INDEX IF NOT EXISTS SystemEvents_FromHost_IDX ON SystemEvents(FromHost);

CREATE TABLE SystemEventsProperties
(
  ID serial not null primary key,
  SystemEventID int NULL ,
  ParamName varchar(255) NULL ,
  ParamValue text NULL
);