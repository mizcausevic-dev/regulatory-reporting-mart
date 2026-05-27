CREATE VIEW mart_reporting_readiness AS
SELECT
  d.docket_id,
  a.agency_label,
  d.title,
  d.due_date,
  d.severity,
  s.owner,
  s.readiness_score,
  s.blockers,
  s.late_risk,
  COUNT(e.packet_id) AS packet_count,
  SUM(CASE WHEN e.status = 'complete' THEN 1 ELSE 0 END) AS complete_packets,
  SUM(CASE WHEN e.status IN ('blocked', 'draft') THEN 1 ELSE 0 END) AS blocked_or_draft_packets
FROM dockets d
JOIN agencies a ON a.agency_id = d.agency_id
JOIN submissions s ON s.docket_id = d.docket_id
LEFT JOIN evidence_packets e ON e.docket_id = d.docket_id
GROUP BY
  d.docket_id,
  a.agency_label,
  d.title,
  d.due_date,
  d.severity,
  s.owner,
  s.readiness_score,
  s.blockers,
  s.late_risk;
