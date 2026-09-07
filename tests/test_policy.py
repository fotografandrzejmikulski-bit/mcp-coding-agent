from mcp_coding_agent.core.guardrails import ExecutionPolicy, PolicyViolation, validate_command, validate_finalize


def test_command_policy() -> None:
    policy = ExecutionPolicy(max_command_timeout=10)
    validate_command(policy, "python -V", 10)
    try:
        validate_command(policy, "python -V", 11)
    except PolicyViolation:
        pass
    else:
        raise AssertionError("timeout policy did not reject an invalid timeout")


def test_finalize_requires_verification() -> None:
    policy = ExecutionPolicy()
    try:
        validate_finalize(policy, False)
    except PolicyViolation:
        pass
    else:
        raise AssertionError("unverified finalize was accepted")
