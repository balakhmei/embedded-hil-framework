# ADR-002: Modular monolith and ports/adapters

Status: Accepted for initial architecture (2026-11-03)

## Decision

Use one installable Python package with hardware contracts and replaceable real/fake adapters. Keep DUT-specific logic outside framework core.

## Consequences

This decision guides interfaces and configuration, but does not imply that the described feature is already implemented. Revisit after real bench integration if needed.
