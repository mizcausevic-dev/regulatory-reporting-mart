CREATE VIEW mart_deadline_pressure AS
SELECT
  docket_id,
  title,
  due_date,
  CASE
    WHEN late_risk >= 60 THEN 'red'
    WHEN late_risk >= 40 THEN 'yellow'
    ELSE 'green'
  END AS pressure_status,
  late_risk,
  blockers,
  readiness_score
FROM mart_reporting_readiness
ORDER BY late_risk DESC, blockers DESC, readiness_score ASC;
