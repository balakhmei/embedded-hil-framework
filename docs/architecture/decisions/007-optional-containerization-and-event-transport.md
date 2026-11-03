# ADR-007: Optional containerization and event transport

Status: Accepted for initial architecture (2026-11-03)

## Decision

Keep physical HIL runner native on Raspberry Pi initially. Containerize API/dashboard and CI later. Introduce MQTT only for a demonstrated telemetry or distributed-agent use case; never make it a core dependency.

## Consequences

This decision guides interfaces and configuration, but does not imply that the described feature is already implemented. Revisit after real bench integration if needed.
