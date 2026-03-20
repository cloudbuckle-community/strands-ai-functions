from ai_functions import ai_function, PostConditionResult
from src.models import PRSummary


VALID_RISK_LEVELS = {"low", "medium", "high"}


def validate_risk_level(summary: PRSummary) -> PostConditionResult:
    if summary.risk_level not in VALID_RISK_LEVELS:
        return PostConditionResult(
            passed=False,
            message=f"risk_level must be one of {VALID_RISK_LEVELS}, got '{summary.risk_level}'"
        )
    return PostConditionResult(passed=True)


def validate_file_changes(summary: PRSummary) -> PostConditionResult:
    if not summary.what_changed:
        return PostConditionResult(
            passed=False,
            message="what_changed cannot be empty. Extract at least one file change from the diff."
        )
    return PostConditionResult(passed=True)


def validate_testing_suggestions(summary: PRSummary) -> PostConditionResult:
    if not summary.testing_suggestions:
        return PostConditionResult(
            passed=False,
            message="Include at least one testing suggestion."
        )
    return PostConditionResult(passed=True)


@ai_function(
    post_conditions=[
        validate_risk_level,
        validate_file_changes,
        validate_testing_suggestions,
    ],
    max_attempts=3,
)
def generate_pr_summary(diff: str, commit_messages: str) -> PRSummary:
    """You are a senior software engineer reviewing a pull request.

    Analyze the following git diff and commit messages to produce a structured
    PR summary. Be specific about what changed and why it matters to the team.

    For suggested_reviewers, infer the right reviewers based on the areas of
    the codebase that were touched (e.g., "backend team" for API changes,
    "frontend team" for UI changes, "devops" for infra changes).

    For risk_level, use "low" for cosmetic or doc changes, "medium" for logic
    changes with limited blast radius, and "high" for changes that affect
    authentication, payments, data models, or public APIs.

    <diff>
    {diff}
    </diff>

    <commit_messages>
    {commit_messages}
    </commit_messages>
    """
