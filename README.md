# PR Review Summarizer with Strands AI Functions

A CLI tool that generates structured PR summaries from git diffs using [Strands AI Functions](https://strandsagents.com/docs/labs/ai-functions/).

## Prerequisites

- Python 3.12+
- AWS credentials configured (for Amazon Bedrock) or another supported model provider

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Try It Out

The quickest way to test is to create a feature branch with some changes and run the summarizer against `main`.

```bash
# 1. Make sure you are in the project directory with the venv activated
source venv/bin/activate

# 2. Create a feature branch and make some changes
git checkout -b feature/my-test-branch
# ... make some code changes and commit them ...

# 3. Run the summarizer
python -m src.main

# 4. Review the output
cat pr_summary.json

# 5. Switch back when done
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

## How It Works

The tool uses `@ai_function` with post-conditions to ensure the generated summary is always valid and complete. If the AI output fails validation (wrong risk level, missing file changes, no testing suggestions), the framework automatically retries with feedback.

See the [companion article](https://blog.cloudbuckle.com/how-i-built-a-self-correcting-pr-review-summarizer-with-strands-ai-functions-52c4314b7340) for a full walkthrough.
