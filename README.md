# PR Review Summarizer with Strands AI Functions

A self-correcting CLI tool and GitHub Action that generates structured, validated PR review summaries from git diffs using [Strands AI Functions](https://strandsagents.com/docs/labs/ai-functions/).

## What It Does

1. Reads a git diff and commit messages from your feature branch
2. Feeds them to an AI agent that produces a structured summary
3. Validates the output using post-conditions (risk level, file changes, testing suggestions)
4. If validation fails, the agent retries with feedback until the output meets all conditions
5. Optionally posts the summary as a formatted comment on your PR via GitHub Actions

## Prerequisites

- Python 3.12+
- AWS credentials configured (for Amazon Bedrock) or another supported model provider

## Setup

```bash
git clone https://github.com/cloudbuckle-community/strands-ai-functions.git
cd strands-ai-functions

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Try It Out

Create a feature branch with some changes and run the summarizer against `main`:

```bash
source venv/bin/activate

# Create a feature branch and make some changes
git checkout -b feature/my-test-branch
# ... make some code changes and commit them ...

# Run the summarizer
python -m src.main

# Review the output
cat pr_summary.json

# Switch back when done
git checkout main
```

You can also specify a different base branch:

```bash
python -m src.main develop
```

## Output

The tool prints a structured JSON summary to the console and saves it to `pr_summary.json`. The summary includes:

- File-level change descriptions
- Risk assessment (low/medium/high) with reasoning
- Testing suggestions
- Suggested reviewers based on affected code areas

## GitHub Action: Automated PR Comments

This repo includes a GitHub Action that automatically posts a formatted summary as a comment on every pull request.

To enable it, add these secrets to your repository under Settings > Secrets and variables > Actions:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

Once configured, every PR will get a comment with the summary, risk assessment, a testing checklist with checkboxes, and suggested reviewers.

## How It Works

The tool uses `@ai_function` with post-conditions to ensure the generated summary is always valid and complete. If the AI output fails validation (wrong risk level, missing file changes, no testing suggestions), the framework automatically retries with feedback.

Key components:

- `src/models.py` - Pydantic models defining the PR summary contract
- `src/pr_reviewer.py` - AI function with post-conditions for validation
- `src/main.py` - CLI entry point
- `.github/workflows/pr-summary.yml` - GitHub Action for automated PR comments

## Articles

- [Part 1: How I Built a Self-Correcting PR Review Summarizer with Strands AI Functions](https://blog.cloudbuckle.com/how-i-built-a-self-correcting-pr-review-summarizer-with-strands-ai-functions-52c4314b7340)
- [Part 2: I Automated PR Reviews So My Team Never Has to Write Another Summary Again](https://blog.cloudbuckle.com/i-automated-pr-reviews-so-my-team-never-has-to-write-another-summary-again-1abb64a9b9f8)

## License

[MIT](LICENSE)
