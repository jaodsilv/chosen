# GitHub Actions Setup

This directory contains GitHub Actions workflows for automating project management.

## Setup Required

To enable the project automation workflows, you need to:

### 1. Configure Repository Variables

Set up the project URL as a repository variable for portability:

1. Go to repository Settings → Secrets and variables → Actions → Variables tab
2. Click "New repository variable"
3. Name: `PROJECT_URL`
4. Value: `https://github.com/users/YOUR_USERNAME/projects/YOUR_PROJECT_NUMBER`
5. Click "Add variable"

**Note**: If no repository variable is set, workflows will default to `https://github.com/users/jaodsilv/projects/3`

### 2. Create Personal Access Token

Create a Personal Access Token (PAT) with the following permissions:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Click "Generate new token"
3. Select the repository: `jaodsilv/chosen`
4. Set expiration as needed
5. Grant the following permissions:
   - **Issues**: Read and write
   - **Pull requests**: Read and write
   - **Projects**: Write
   - **Metadata**: Read

### 3. Add Token to Repository Secrets

1. Go to repository Settings → Secrets and variables → Actions → Secrets tab
2. Click "New repository secret"
3. Name: `ADD_TO_PROJECT_PAT`
4. Value: Your generated PAT token
5. Click "Add secret"

## Workflow Files

### `add-issues-to-project.yml`

- **Triggers**: When issues are opened or labeled
- **Function**: Automatically adds issues with specific labels to Project 3
- **Labels that trigger**: `enhancement`, `feature`, `bug`
- **Additional**: Sets priority and phase fields based on labels

### `add-prs-to-project.yml`

- **Triggers**: When pull requests are opened or labeled
- **Function**: Automatically adds PRs to Project 3 and sets status to "In Progress"
- **Labels that trigger**: `enhancement`, `feature`, `bug`, `hotfix`

### `project-automation.yml`

- **Triggers**: When issues/PRs are closed, merged, or reopened
- **Function**: Updates project status fields automatically
- **Status Updates**:
  - Closed issues → "Done"
  - Merged PRs → "Done"
  - Reopened issues → "Todo"
  - Reopened PRs → "In Progress"

## Issue Templates

### `enhancement.yml`

- Structured template for enhancement requests
- Automatically applies `enhancement` label
- Includes priority and phase dropdowns
- Triggers automatic project addition

### `bug_report.yml`

- Structured template for bug reports
- Automatically applies `bug` label
- Includes priority selection and browser information
- Triggers automatic project addition

## Label-Based Automation

The workflows use labels to determine:

### Priority Mapping

- `critical` → Critical priority
- `high` → High priority
- `medium` → Medium priority
- `low` → Low priority

### Phase Mapping

- `phase-1` → "Phase 1: Foundation"
- `phase-2` → "Phase 2: State Management"
- `phase-3` → "Phase 3: Core Features"
- `phase-4` → "Phase 4: Advanced Features"
- `phase-5` → "Phase 5: Polish"

## Usage

Once the PAT is configured, the workflows will automatically:

1. **Add new issues/PRs** with relevant labels to the project
2. **Set priority levels** based on priority labels
3. **Categorize by development phase** using phase labels
4. **Update status** when items are closed, merged, or reopened
5. **Provide structured templates** for consistent issue creation

All automation happens in the background - no manual intervention required after setup.
