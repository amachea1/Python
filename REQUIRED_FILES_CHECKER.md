# Required File Presence Checker

A CI/CD pipeline built with GitHub Actions and AWS CloudWatch that enforces baseline repo structure. It validates that every pull request and every push to `main` includes required files (`README.md` and `.gitignore`), and audit-logs successful runs to environment-specific CloudWatch log groups.

## Why This Exists

Platform engineering teams often require baseline documentation and structure in every service repository. Manually checking this is slow and unreliable. This project automates the check at the source — the moment code is proposed — and creates an audit trail so leadership can verify compliance.

## How It Works

### The Check Script

`check_required_files.py` is a small Python script that:

- Verifies `README.md` and `.gitignore` exist in the repo root
- Exits silently with code 0 if both files are present
- Prints missing files and exits with code 1 if any are missing

### The Workflows

Two GitHub Actions workflows trigger the check at different points in the development lifecycle:

| Workflow | Trigger | Environment | CloudWatch Log Group |
|---|---|---|---|
| `on_pull_request.yml` | PR opened against `main` | beta | `/github-actions/required-files-checker/beta` |
| `on_merge.yml` | Push to `main` (PR merged) | prod | `/github-actions/required-files-checker/prod` |

Both workflows:

1. Check out the repo's code on a fresh Ubuntu runner
2. Set up Python
3. Run `check_required_files.py`
4. If the check passes, configure AWS credentials
5. Send an audit log entry to CloudWatch under the environment's log group

## How to Run the File Presence Check Manually

From the repo root:

    python check_required_files.py

- Silent exit (no output) → all required files present. Check passed.
- Prints missing filenames and exits with code 1 → check failed.

## What Happens When Required Files Are Missing

When the script fails, the GitHub Actions step that ran it also fails. This cascades:

- The job fails
- The workflow fails
- The pull request is blocked from merging until the missing files are added
- The CloudWatch logging step never executes — guaranteeing only validated runs produce audit logs

## How the AWS CLI Log Step Works

After the file check passes, the workflow:

1. Captures the current UTC timestamp in ISO 8601-like format (with dashes between time pieces instead of colons — AWS log stream names cannot contain colons)
2. Captures the same time in milliseconds since epoch (required by AWS for log event timestamps)
3. Creates a new log stream named with the timestamp using `aws logs create-log-stream`
4. Sends a single log event with `aws logs put-log-events` containing:
   - Workflow name (from `github.workflow`)
   - Commit SHA (from `github.sha`)
   - GitHub actor / username (from `github.actor`)
   - Timestamp

## Where to Find Logs in CloudWatch

1. Sign in to the AWS Console
2. Navigate to **CloudWatch → Logs → Log groups**
3. Click into the appropriate log group:
   - Beta runs (pull requests): `/github-actions/required-files-checker/beta`
   - Prod runs (merges to main): `/github-actions/required-files-checker/prod`
4. Each successful run creates a new log stream named with the UTC timestamp
5. Click a stream to see the log event with workflow, SHA, actor, and timestamp

## GitHub Secrets Configuration

All AWS credentials and environment-specific values are stored as GitHub Secrets. No values are hardcoded in any workflow or script.

### Repository Secrets

Defined under: **Repository → Settings → Secrets and variables → Actions → Repository secrets**

| Secret Name | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user's access key ID |
| `AWS_SECRET_ACCESS_KEY` | IAM user's secret access key |
| `AWS_REGION` | AWS region where the log groups live (e.g., `us-east-1`) |

### Environment Secrets

Defined under: **Repository → Settings → Environments**

Two environments are configured:

- `beta` — referenced by `on_pull_request.yml`
- `prod` — referenced by `on_merge.yml`

Each environment has its own `LOG_GROUP_NAME` secret with the appropriate log group path:

- Beta value: `/github-actions/required-files-checker/beta`
- Prod value: `/github-actions/required-files-checker/prod`

### Adding a Secret

1. Navigate to **Settings → Secrets and variables → Actions** (or **Environments** for environment-scoped)
2. Click **New repository secret** (or **Add environment secret**)
3. Enter the exact name listed above
4. Paste the value
5. Click **Add secret**

Secret values cannot be viewed after saving. To rotate a secret, delete it and re-add with the new value.

## IAM Permissions Required

The IAM user whose credentials are stored needs permission to:

- Create log streams (`logs:CreateLogStream`)
- Put log events (`logs:PutLogEvents`)

