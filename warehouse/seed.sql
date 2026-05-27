INSERT INTO agencies (agency_id, agency_label, region) VALUES
  ('EPA', 'Environmental Protection Agency', 'US'),
  ('FTC', 'Federal Trade Commission', 'US'),
  ('EMA', 'European Medicines Agency', 'EU');

INSERT INTO dockets (docket_id, agency_id, title, due_date, severity) VALUES
  ('DK-104', 'EPA', 'Industrial emissions rule comment packet', '2026-06-05', 'high'),
  ('DK-212', 'FTC', 'Consumer disclosure enforcement response', '2026-06-11', 'medium'),
  ('DK-330', 'EMA', 'Clinical evidence publication update', '2026-06-18', 'high'),
  ('DK-411', 'EPA', 'Supply-chain environmental attestation', '2026-06-21', 'low');

INSERT INTO evidence_packets (packet_id, docket_id, packet_label, status, reviewer) VALUES
  ('PK-1', 'DK-104', 'Air quality methodology appendix', 'complete', 'policy'),
  ('PK-2', 'DK-104', 'Plant variance evidence binder', 'blocked', 'legal'),
  ('PK-3', 'DK-212', 'Consumer notice redline', 'blocked', 'brand'),
  ('PK-4', 'DK-330', 'Clinical validation citation set', 'review', 'medical'),
  ('PK-5', 'DK-330', 'Audit-trace integrity bundle', 'complete', 'quality'),
  ('PK-6', 'DK-411', 'Supplier attestation packet', 'draft', 'ops');

INSERT INTO submissions (submission_id, docket_id, owner, readiness_score, blockers, late_risk) VALUES
  ('SUB-104', 'DK-104', 'policy-ops', 74, 2, 68),
  ('SUB-212', 'DK-212', 'revops-counsel', 81, 1, 34),
  ('SUB-330', 'DK-330', 'clinical-programs', 77, 1, 57),
  ('SUB-411', 'DK-411', 'supplier-assurance', 66, 2, 44);
