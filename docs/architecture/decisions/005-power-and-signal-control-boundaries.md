# ADR-005: Power and signal control boundaries

Status: Accepted for initial architecture (2026-11-03)

## Decision

Reserve independently testable interfaces for future PSU and UART switch; enforce safe states and limits before enabling real hardware.

## Consequences

This decision guides interfaces and configuration, but does not imply that the described feature is already implemented. Revisit after real bench integration if needed.
