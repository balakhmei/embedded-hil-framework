# Embedded HIL & Computer Vision Test Automation Framework

Portable Python/pytest framework for embedded hardware-in-the-loop testing. The Raspberry Pi 5 is the target autonomous HIL host; macOS and simulation are supported development targets.

## Status

**M0.4 scaffold only.** Real UART, relay, camera and Pico drivers have **not** been migrated. Configuration files are architectural examples, not executable hardware profiles. No physical bench is required for the current unit test.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest
```

For an optional Allure plugin, install `pip install -e '.[test,report]'` and run `pytest --alluredir artifacts/allure-results`. Generating the HTML report additionally requires the Allure command-line tool.

## Roadmap

- M0.4: package scaffold, architecture decisions, first offline unit test
- M1: typed configuration, hardware interfaces, fake adapters, lifecycle
- M2: real adapter migration, Allure evidence, CI
- M3: vision algorithms and Pico HC-SR04 integration
- Later: PSU, UART switching, FastAPI dashboard, optional Docker and MQTT

## Hardware target

Raspberry Pi 5 hosts pytest and connects FT232R UART, USB relay, Camera Module 3 (CSI), and Pico 2 W (USB). The DUT is ESP32-S3 SENTRY SWM-2.

## Safety

Do not store credentials or secrets in tracked configuration. Physical adapters must enforce resource ownership, deterministic cleanup, and fail-safe startup; the current scaffold makes no hardware safety guarantees.

## Repository

This directory is ready for a **new** Git repository. It does not modify the original `embedded-qa` diploma project.
