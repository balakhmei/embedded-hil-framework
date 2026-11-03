# Architecture

See `decisions/` for ADR-001 through ADR-007. Configuration is planned as bench + DUT + vision profiles. Test lifecycle: validate -> acquire resources -> preflight -> execute -> capture evidence -> cleanup/recovery -> finalize. Cleanup must run even when tests fail, but hardware safety requires additional physical protections.
