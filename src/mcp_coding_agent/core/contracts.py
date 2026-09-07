"""Canonical contracts used by planning, execution and verification."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Phase(StrEnum):
    ANALYZE = "analyze"
    ARCHITECT = "architect"
    PLAN = "plan"
    IMPLEMENT = "implement"
    TEST = "test"
    REVIEW = "review"
    REPAIR = "repair"
    SECURITY = "security"
    INTEGRATE = "integrate"
    VERIFY = "verify"
    FINALIZE = "finalize"


class AcceptanceCriterion(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9_-]+$")
    description: str
    verification: str
    required: bool = True


class WorkItem(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9_-]+$")
    title: str
    phase: Phase
    owner: str
    dependencies: list[str] = Field(default_factory=list)
    acceptance_criteria: list[AcceptanceCriterion] = Field(default_factory=list)
    status: str = "pending"
    metadata: dict[str, Any] = Field(default_factory=dict)


class VerificationReport(BaseModel):
    passed: bool
    checks: list[dict[str, Any]] = Field(default_factory=list)
    failures: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class BuilderRequest(BaseModel):
    task: str
    workspace: str | None = None
    constraints: list[str] = Field(default_factory=list)
    requested_deliverables: list[str] = Field(default_factory=list)
