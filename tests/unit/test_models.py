from embedded_hil.core.models import RunOutcome, ResultRecord

def test_result_is_hardware_independent():
    result = ResultRecord(name="offline-smoke", outcome=RunOutcome.PASSED)
    assert result.outcome is RunOutcome.PASSED
    assert result.details == ""

def test_infrastructure_error_is_distinct_from_failure():
    assert RunOutcome.INFRASTRUCTURE_ERROR != RunOutcome.FAILED
