CREATE TABLE agencies (
  agency_id TEXT PRIMARY KEY,
  agency_label TEXT NOT NULL,
  region TEXT NOT NULL
);

CREATE TABLE dockets (
  docket_id TEXT PRIMARY KEY,
  agency_id TEXT NOT NULL REFERENCES agencies(agency_id),
  title TEXT NOT NULL,
  due_date TEXT NOT NULL,
  severity TEXT NOT NULL
);

CREATE TABLE evidence_packets (
  packet_id TEXT PRIMARY KEY,
  docket_id TEXT NOT NULL REFERENCES dockets(docket_id),
  packet_label TEXT NOT NULL,
  status TEXT NOT NULL,
  reviewer TEXT NOT NULL
);

CREATE TABLE submissions (
  submission_id TEXT PRIMARY KEY,
  docket_id TEXT NOT NULL REFERENCES dockets(docket_id),
  owner TEXT NOT NULL,
  readiness_score INTEGER NOT NULL,
  blockers INTEGER NOT NULL,
  late_risk INTEGER NOT NULL
);
