# ADR-004: Pico 2 W as independent sensor emulator

Status: Accepted for initial architecture (2026-11-03)

## Decision

Keep the HC-SR04 PIO emulator firmware independent; control it from the host through a dedicated adapter. Preserve its separate repository.

## Consequences

This decision guides interfaces and configuration, but does not imply that the described feature is already implemented. Revisit after real bench integration if needed.
