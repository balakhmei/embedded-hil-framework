# ADR-006: API-ready runner without direct hardware access

Status: Accepted for initial architecture (2026-11-03)

## Decision

pytest is the test engine. Future FastAPI/dashboard requests go through the runner/resource manager, not directly to GPIO/UART.

## Consequences

This decision guides interfaces and configuration, but does not imply that the described feature is already implemented. Revisit after real bench integration if needed.
