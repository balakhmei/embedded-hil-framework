# ADR-003: Composable vision pipeline

Status: Accepted for initial architecture (2026-11-03)

## Decision

Separate frame capture, analysis algorithms, and structured results. Static HSV first; temporal/blink analysis later.

## Consequences

This decision guides interfaces and configuration, but does not imply that the described feature is already implemented. Revisit after real bench integration if needed.
