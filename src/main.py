import subprocess
import sys
import json

from src.pr_reviewer import generate_pr_summary


def get_git_diff(base_branch: str = "main") -> str:
    result = subprocess.run(
        ["git", "diff", base_branch],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def get_commit_messages(base_branch: str = "main") -> str:
    result = subprocess.run(
        ["git", "log", f"{base_branch}..HEAD", "--pretty=format:%s"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def main():
    base_branch = sys.argv[1] if len(sys.argv) > 1 else "main"

    print(f"Generating PR summary against '{base_branch}'...")

    diff = get_git_diff(base_branch)
    commits = get_commit_messages(base_branch)

    if not diff:
        print("No diff found. Are you on a feature branch?")
        sys.exit(1)

    summary = generate_pr_summary(diff=diff, commit_messages=commits)

    output = json.dumps(summary.model_dump(), indent=2)
    print("\n" + output)

    output_file = "pr_summary.json"
    with open(output_file, "w") as f:
        f.write(output)
    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    main()
