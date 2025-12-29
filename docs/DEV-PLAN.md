# Multi-Agent Development Process

**Version**: 2.0.0
**Created**: 2025-12-09
**Status**: Development Process Specification
**Purpose**: Define practical multi-agent workflows for CHOSEN implementation

---

## Table of Contents

1. [Overview](#1-overview)
2. [Development Agent Types](#2-development-agent-types)
3. [Worktree Strategy](#3-worktree-strategy)
4. [TDD Workflow Adaptation](#4-tdd-workflow-adaptation)
5. [Phase-Specific Workflows](#5-phase-specific-workflows)
6. [Quality Gates](#6-quality-gates)
7. [Agent Orchestration Patterns](#7-agent-orchestration-patterns)
8. [Development Rituals](#8-development-rituals)
9. [Parallel Development Patterns](#9-parallel-development-patterns)
10. [Context Management](#10-context-management)
11. [Integration Points](#11-integration-points)

---

## 1. Overview

### 1.1 Purpose

This document defines the multi-agent development process for implementing the AI Message Writer Assistant v2. It adapts the base coding-task-workflow.md to this specific project's needs, providing practical guidance for developers working with Claude Code.

### 1.2 Key Principles

1. **Test-Driven Development**: All code preceded by tests
2. **Agent Specialization**: Different agents for different concerns
3. **Phased Approach**: Progressive complexity from Phase 1 to Phase 4
4. **Quality First**: Multiple review cycles ensure excellence
5. **Context Awareness**: Agents understand project architecture and patterns

### 1.3 Process Flow

```
GitHub Issue → Worktree Creation → TDD Workflow → Implementation →
Review → Quality Gates → PR → Merge → Cleanup
```

### 1.4 Success Metrics

1. **Test Coverage**: >90% for core modules
2. **Code Quality**: No critical issues from linters/type checkers
3. **Agent Efficiency**: Clear handoffs, minimal context loss
4. **Velocity**: Predictable task completion times
5. **Quality**: Minimal bugs in production

---

## 2. Development Agent Types

### 2.1 Core Development Agents

#### 2.1.1 Test Design Agent

**Purpose**: Design comprehensive test suites before implementation

**When to Invoke**:
- At the start of any new feature or bug fix
- When refactoring existing code
- When adding new API endpoints or services

**Input**:
- Task description from GitHub issue
- System design documents
- Related code files
- Existing test patterns

**Output**:
- Detailed test design document with:
  - Test scenarios (happy path, edge cases, error cases)
  - Unit test structure
  - Integration test structure
  - Mocking strategy
  - Test data requirements
  - Expected coverage targets

**Example Invocation**:
```
Task: Design tests for ConversationRepository

Create comprehensive test design for the ConversationRepository class.

Context:
- File: backend/app/data/conversation_repo.py
- System Design: docs/SYSTEM-DESIGN.md

Design should include:
1. Unit tests for each CRUD operation
2. Edge cases (file not found, malformed YAML, concurrent access)
3. Integration tests with actual file system
4. Mocking strategy for file I/O
5. Test data fixtures
```

#### 2.1.2 Test Implementation Agent

**Purpose**: Write test code based on test design

**When to Invoke**:
- After test design is approved
- Following the TDD workflow

**Input**:
- Approved test design document
- Code templates and patterns
- Pytest configuration
- Fixture definitions

**Output**:
- Complete test files with:
  - Test functions/classes
  - Fixtures
  - Mocks
  - Test data
  - Proper assertions
  - Clear docstrings

**Example Invocation**:
```
Task: Implement tests for ConversationRepository

Implement the test suite designed in the previous step.

Test Design: [paste test design document]

Requirements:
- Use pytest
- Follow existing fixture patterns in conftest.py
- Mock file I/O appropriately
- Ensure tests fail initially (no implementation yet)
- Include docstrings for each test
```

#### 2.1.3 Solution Design Agent

**Purpose**: Design implementation to pass tests

**When to Invoke**:
- After tests are written and failing
- Before implementation begins

**Input**:
- Test code
- Interface/contract definitions
- System architecture
- Design patterns to follow

**Output**:
- Detailed implementation design:
  - Class/function structure
  - Algorithm descriptions
  - Data flow diagrams
  - Error handling approach
  - Dependencies and imports
  - Code organization

**Example Invocation**:
```
Task: Design ConversationRepository implementation

Design the implementation for ConversationRepository that will make the tests pass.

Tests: backend/tests/unit/test_conversation_repo.py
Interface: Must extend RepositoryBase
System Design: See docs/SYSTEM-DESIGN.md section 5.4

Design should include:
1. Method implementations
2. File naming strategy
3. YAML serialization approach
4. Index management
5. Error handling patterns
6. Performance considerations
```

#### 2.1.4 Implementation Agent

**Purpose**: Write production code based on design

**When to Invoke**:
- After solution design is approved
- Following TDD red-green-refactor cycle

**Input**:
- Solution design document
- Test code
- Code style guidelines
- Type hints requirements

**Output**:
- Production code that:
  - Passes all tests
  - Follows design
  - Adheres to style guidelines
  - Includes type hints
  - Has comprehensive docstrings
  - Handles errors gracefully

**Example Invocation**:
```
Task: Implement ConversationRepository

Implement the ConversationRepository based on the approved design.

Design: [paste design document]
Tests: backend/tests/unit/test_conversation_repo.py

Requirements:
- Make all tests pass
- Use Python 3.11+ features
- Include type hints
- Add docstrings (Google style)
- Follow black/isort formatting
- Handle all error cases in design
```

#### 2.1.5 Code Review Agent

**Purpose**: Review code for quality, correctness, and adherence to standards

**When to Invoke**:
- After implementation is complete
- Before committing code
- During PR review

**Input**:
- Implementation code
- Test code
- Design documents
- Project standards

**Output**:
- Review report with:
  - Code quality assessment
  - Design adherence check
  - Test coverage analysis
  - Style compliance
  - Potential bugs/issues
  - Suggestions for improvement
  - Approval or change requests

**Example Invocation**:
```
Task: Review ConversationRepository implementation

Review the ConversationRepository implementation for quality and correctness.

Implementation: backend/app/data/conversation_repo.py
Tests: backend/tests/unit/test_conversation_repo.py
Design: [paste design document]

Check for:
1. All tests passing
2. Design adherence
3. Code style (black, isort, flake8, mypy)
4. Error handling completeness
5. Performance concerns
6. Documentation quality
7. Security issues
```

#### 2.1.6 Refactoring Evaluation Agent

**Purpose**: Evaluate if code needs refactoring

**When to Invoke**:
- After initial implementation is complete and reviewed
- Periodically during development
- When code smells are detected

**Input**:
- Production code
- Test code
- Complexity metrics
- Design patterns

**Output**:
- Refactoring report:
  - Code quality score
  - Identified code smells
  - Complexity analysis
  - Refactoring recommendations (if any)
  - Priority and impact assessment
  - Decision: refactor now, later, or never

**Example Invocation**:
```
Task: Evaluate ConversationRepository for refactoring

Analyze the ConversationRepository implementation and determine if refactoring is needed.

Code: backend/app/data/conversation_repo.py
Tests: backend/tests/unit/test_conversation_repo.py

Evaluate:
1. Method length and complexity
2. Code duplication
3. Separation of concerns
4. SOLID principles adherence
5. Testability
6. Performance
7. Maintainability

Recommend refactoring if significant improvements possible.
```

### 2.2 Specialized Development Agents

#### 2.2.1 Prompt Engineering Agent

**Purpose**: Design and optimize LLM prompts for AI agents

**When to Invoke**:
- When implementing new agent types (ContextAnalyzer, ResponseGenerator, etc.)
- When agent output quality is unsatisfactory
- When optimizing for different models (Haiku, Sonnet, Opus)

**Input**:
- Agent requirements
- Input/output schemas
- Example data
- Quality criteria

**Output**:
- Optimized prompts:
  - System prompt
  - User prompt templates
  - Few-shot examples (if needed)
  - Output format specifications
  - Testing strategy for prompt quality

**Example Invocation**:
```
Task: Design prompt for ContextAnalyzer agent

Design the system and user prompts for the ContextAnalyzer agent.

Agent: app/agents/analysis/context_analyzer.py
Input Schema: Conversation object with message history
Output Schema: ContextAnalysis (summary, sentiment_trend, conversation_stage, etc.)
Model: Sonnet

Requirements:
1. Extract conversation patterns
2. Identify sentiment trends
3. Determine conversation stage
4. Generate actionable recommendations
5. Return structured JSON output
6. Handle edge cases (short conversations, unclear context)

Include:
- System prompt defining role and capabilities
- User prompt template with placeholders
- Output format specification
- Example test cases
```

#### 2.2.2 API Design Agent

**Purpose**: Design RESTful API endpoints

**When to Invoke**:
- Before implementing new API routes
- When designing public APIs
- When planning endpoint structure

**Input**:
- Feature requirements
- Data models
- API standards
- OpenAPI/Swagger guidelines

**Output**:
- API design specification:
  - Endpoint paths
  - HTTP methods
  - Request/response schemas
  - Status codes
  - Error responses
  - Examples
  - OpenAPI documentation

**Example Invocation**:
```
Task: Design Analysis API endpoints

Design the REST API endpoints for conversation analysis features.

Features:
- Trigger context analysis
- Calculate fit score
- Optimize follow-up timing
- Get multi-conversation analytics
- Score response quality

Requirements:
- RESTful design
- Pydantic schemas for validation
- Proper HTTP status codes
- Error handling
- OpenAPI documentation

Existing patterns: app/api/routes/conversations.py
```

#### 2.2.3 Integration Test Design Agent

**Purpose**: Design integration tests for end-to-end workflows

**When to Invoke**:
- After multiple components are implemented
- Before phase completion
- For complex multi-step workflows

**Input**:
- System architecture
- Component interfaces
- User workflows
- Test infrastructure

**Output**:
- Integration test design:
  - Test scenarios
  - Setup/teardown procedures
  - Data fixtures
  - Assertion strategies
  - External dependency mocking

**Example Invocation**:
```
Task: Design integration tests for conversation workflow

Design integration tests for the complete conversation management workflow.

Workflow:
1. Parse raw message
2. Create conversation
3. Analyze context
4. Generate response
5. Update conversation

Components:
- MessageService
- ConversationService
- AnalysisService
- Agent Orchestrator
- File-based repositories

Design should cover:
- Happy path end-to-end
- Error handling at each step
- Concurrent operations
- Data persistence verification
```

#### 2.2.4 Documentation Agent

**Purpose**: Write comprehensive documentation

**When to Invoke**:
- After feature implementation
- Before PR creation
- For public APIs
- Phase completion

**Input**:
- Code
- Docstrings
- API specifications
- User workflows

**Output**:
- Documentation:
  - README updates
  - API documentation
  - User guides
  - Code comments
  - Architecture diagrams

**Example Invocation**:
```
Task: Document the Agent System

Write comprehensive documentation for the Agent System.

Code:
- app/agents/base_agent.py
- app/agents/orchestrator.py
- app/agents/model_router.py
- app/agents/analysis/
- app/agents/generation/

Include:
1. Architecture overview
2. How to create new agents
3. Agent lifecycle
4. Orchestration patterns
5. Model selection guidelines
6. Testing strategies
7. Examples and code snippets

Target audience: Developers extending the system
```

---

## 3. Worktree Strategy

### 3.1 When to Create Worktrees

**Always create a worktree for**:
1. New feature development (from GitHub issue)
2. Bug fixes (non-trivial)
3. Refactoring tasks
4. Parallel development work

**Work directly in main branch for**:
1. Documentation updates (minor)
2. Config file changes (minor)
3. One-line bug fixes (reviewed)

### 3.2 Worktree Naming Convention

```
Branch naming: <type>/<short-description>

Examples:
- feature/conversation-repository
- fix/yaml-parsing-error
- refactor/agent-orchestrator
- test/integration-workflow
- docs/api-documentation
```

### 3.3 Worktree Location

```
Base: D:\src\chosen\
Main: D:\src\chosen\v2\
Worktrees: D:\src\chosen\<branch-name>\
```

### 3.4 Worktree Creation Process

```bash
# From main branch working directory
cd D:\src\chosen\v2

# Create worktree
git worktree add -b feature/task-name ../task-name

# Link data folder (if needed)
cd ../task-name
mklink /J data ..\v2\data

# Verify
git branch --show-current
ls data  # Should show linked directory
```

### 3.5 Worktree Workflow

```
1. Create worktree from main
2. Implement feature/fix (TDD workflow)
3. Commit changes
4. Push branch
5. Create PR
6. After merge, remove worktree
7. Return to main, pull latest
```

### 3.6 Worktree Cleanup

```bash
# After PR is merged
cd D:\src\chosen\v2
git worktree remove ../task-name
git branch -d feature/task-name
```

### 3.7 Parallel Development Strategy

**Independent Tasks** (can be developed in parallel):
- Different modules (e.g., repositories, services, agents)
- Different API routes
- Different test suites
- Documentation

**Dependent Tasks** (must be sequential):
- Base class → Derived classes
- Data models → Repositories
- Repositories → Services
- Services → API endpoints

**Parallel Workflow Example**:

Developer A:
```
Worktree: feature/conversation-repository
Task: Implement ConversationRepository
Dependencies: None (base task)
```

Developer B (in parallel):
```
Worktree: feature/settings-repository
Task: Implement SettingsRepository
Dependencies: None (independent)
```

Developer C (waits for A):
```
Worktree: feature/conversation-service
Task: Implement ConversationService
Dependencies: ConversationRepository (wait for A's PR)
```

---

## 4. TDD Workflow Adaptation

### 4.1 Standard TDD Cycle for This Project

```
Phase 1: Test Design
├── Agent: Test Design Agent
├── Input: GitHub issue, system design
├── Output: Comprehensive test design
└── Review: Test Design Review Agent

Phase 2: Test Implementation
├── Agent: Test Implementation Agent
├── Input: Approved test design
├── Output: Failing tests (red)
└── Review: Test Code Review Agent

Phase 3: Solution Design
├── Agent: Solution Design Agent
├── Input: Tests, architecture docs
├── Output: Implementation plan
└── Review: Design Review Agent

Phase 4: Implementation
├── Agent: Implementation Agent
├── Input: Design, failing tests
├── Output: Code making tests pass (green)
└── Review: Code Review Agent

Phase 5: Refactoring (if needed)
├── Agent: Refactoring Evaluation Agent
├── Decision: Refactor now, later, or skip
├── If refactor: Implementation Agent
└── Review: Code Review Agent

Phase 6: Integration
├── Run all tests (unit + integration)
├── Type checking (mypy)
├── Linting (black, isort, flake8)
└── Coverage check (pytest-cov)
```

### 4.2 Project-Specific Test Patterns

#### 4.2.1 Testing Pydantic Models

```python
# Pattern for model tests
def test_conversation_model_creation():
    """Test that Conversation model validates correctly."""
    conversation = Conversation(
        platform=Platform.LINKEDIN,
        recruiter_name="John Doe",
        company="TechCorp"
    )
    assert conversation.id is not None
    assert conversation.platform == Platform.LINKEDIN
    assert conversation.archived is False

def test_conversation_model_validation_errors():
    """Test that invalid data raises validation errors."""
    with pytest.raises(ValidationError):
        Conversation(platform="invalid_platform")
```

#### 4.2.2 Testing Repositories

```python
# Pattern for repository tests
@pytest.fixture
def temp_data_dir(tmp_path):
    """Create temporary data directory."""
    return tmp_path / "conversations"

@pytest.fixture
def conversation_repo(temp_data_dir):
    """Create ConversationRepository with temp directory."""
    return ConversationRepository(temp_data_dir)

async def test_save_and_get_conversation(conversation_repo):
    """Test saving and retrieving a conversation."""
    conversation = Conversation(
        platform=Platform.LINKEDIN,
        recruiter_name="John Doe",
        company="TechCorp"
    )

    # Save
    saved = await conversation_repo.save(conversation)
    assert saved.id == conversation.id

    # Retrieve
    retrieved = await conversation_repo.get(conversation.id)
    assert retrieved is not None
    assert retrieved.id == conversation.id
    assert retrieved.company == "TechCorp"
```

#### 4.2.3 Testing Agents

```python
# Pattern for agent tests
@pytest.fixture
def mock_model_router():
    """Mock ModelRouter for testing."""
    router = Mock(spec=ModelRouter)
    router.complete = AsyncMock(return_value='{"result": "mocked"}')
    return router

@pytest.fixture
def context_analyzer(mock_model_router):
    """Create ContextAnalyzerAgent with mocked router."""
    return ContextAnalyzerAgent(model_router=mock_model_router)

async def test_context_analyzer_with_valid_conversation(
    context_analyzer,
    sample_conversation
):
    """Test context analyzer produces valid analysis."""
    result = await context_analyzer.execute({
        "conversation": sample_conversation
    })

    assert result.success is True
    assert "sentiment_trend" in result.data
    assert "conversation_stage" in result.data
```

#### 4.2.4 Testing API Endpoints

```python
# Pattern for API endpoint tests
@pytest.fixture
def client():
    """Create test client."""
    from app.main import app
    return TestClient(app)

def test_list_conversations(client):
    """Test GET /api/v1/conversations."""
    response = client.get("/api/v1/conversations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_conversation(client, conversation_payload):
    """Test POST /api/v1/conversations."""
    response = client.post(
        "/api/v1/conversations",
        json=conversation_payload
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["company"] == conversation_payload["company"]
```

### 4.3 Coverage Targets

```yaml
Overall: >85%

Critical Modules: >90%
  - app/models/
  - app/data/
  - app/agents/base_agent.py
  - app/agents/orchestrator.py

Services: >85%
  - app/services/

API Routes: >80%
  - app/api/routes/

Utilities: >75%
  - app/utils/
```

---

## 5. Phase-Specific Workflows

> **Note**: See [ROADMAP.md](../ROADMAP.md) for the canonical issue tracking and priorities.

### 5.1 P0 Workflow (Minimal Working Backend)

**Focus**: Data layer, basic API, AI resilience

**Status**:
| Issue | Description | Status |
|-------|-------------|--------|
| #66 | FileHandler - File operations | ✅ Done |
| #67 | YAMLHandler - YAML serialization | ✅ Done |
| #68 | RepositoryBase - CRUD interface | Pending |
| #69 | ConversationRepository - Conversation CRUD | Pending |
| #70 | Conversation REST endpoints | Pending |
| NEW | AI Resilience Layer - Anthropic client with retries | Pending |

#### 5.1.1 Data Layer Tasks (Weeks 1-2)

**Task Pattern**: Setup + Core Models

```
1. GitHub Issue Created
   ↓
2. Create Worktree (feature/core-models)
   ↓
3. Agent: Test Design Agent
   - Design tests for all Pydantic models
   - Edge cases: validation, serialization, defaults
   ↓
4. Agent: Test Implementation Agent
   - Write model tests (should fail - no models yet)
   ↓
5. Agent: Solution Design Agent
   - Design model classes with proper inheritance
   - Define enums and validators
   ↓
6. Agent: Implementation Agent
   - Implement models (tests should pass)
   ↓
7. Agent: Code Review Agent
   - Review for type safety, validation completeness
   ↓
8. Commit & Push
   ↓
9. Create PR
```

#### 5.1.2 AI Resilience Layer

**Task Pattern**: Anthropic Client with Resilience

```
1. Create Worktree (feature/ai-resilience)
   ↓
2. Agent: Test Design Agent
   - Retry logic tests (exponential backoff)
   - Cache fallback tests
   - Error handling tests
   ↓
3. Agent: Test Implementation Agent
   - Write tests with mocked API responses
   ↓
4. Agent: Solution Design Agent
   - Design AIClient class per SYSTEM-DESIGN.md section 4.5
   ↓
5. Agent: Implementation Agent
   - Implement retry with exponential backoff
   - Implement cache fallback
   ↓
6. Agent: Code Review Agent
   ↓
7. Integration tests with real API
   ↓
8. Commit & PR
```

#### 5.1.3 Repository Layer Tasks

**Task Pattern**: Repository Implementation

```
For each repository (Conversation, Settings, etc.):

1. Create Worktree (feature/<repo-name>-repository)
   ↓
2. Agent: Test Design Agent
   - CRUD operation tests
   - Filtering and pagination tests
   - Concurrent access tests
   - Error handling tests
   ↓
3. Agent: Test Implementation Agent
   - Write repository tests with file mocking
   ↓
4. Agent: Solution Design Agent
   - Design repository class
   - File naming strategy
   - Index management approach
   ↓
5. Agent: Implementation Agent
   - Implement repository
   ↓
6. Agent: Code Review Agent
   ↓
7. Agent: Integration Test Design Agent
   - Design tests with real file system
   ↓
8. Agent: Test Implementation Agent
   - Implement integration tests
   ↓
9. Verify all tests pass
   ↓
10. Commit & Push
    ↓
11. Create PR
```

### 5.2 P1 Workflow (Core Features + CLI)

**Focus**: Agent foundation, response generation, CLI interface

**Issues**:
| Issue | Description | Status |
|-------|-------------|--------|
| #71 | ModelRouter - Claude API routing | Pending |
| #72 | BaseAgent - Abstract agent base | Pending |
| #73 | AgentOrchestrator - Multi-agent manager | Pending |
| #74 | ResponseGeneratorAgent - Response generation | Pending |
| #75-77 | Service layer | Pending |
| #51 | GitHub Actions workflow | Pending |
| NEW | CLI Tool - Command-line interface | Pending |

#### 5.2.1 Agent System Tasks

**Task Pattern**: Agent Implementation

```
1. Base Agent & Orchestrator First (sequential):

   a) Worktree: feature/base-agent
      ↓
   b) TDD workflow for BaseAgent class (#72)
      ↓
   c) TDD workflow for ModelRouter (#71)
      ↓
   d) TDD workflow for AgentOrchestrator (#73)
      ↓
   e) Integration tests for agent system
      ↓
   f) PR & Merge

2. Response Generator Agent (#74):

   a) Worktree: feature/response-generator
      ↓
   b) Agent: Prompt Engineering Agent
      - Design prompts for response generation
      ↓
   c) Agent: Test Design Agent
      - Design tests with mocked LLM responses
      ↓
   d) TDD workflow as normal
      ↓
   e) Manual testing with real API
      ↓
   f) Prompt iteration based on quality
      ↓
   g) PR & Merge
```

#### 5.2.2 CLI Tool Implementation

**Task Pattern**: CLI Development

```
1. Create Worktree (feature/cli-tool)
   ↓
2. Agent: API Design Agent
   - Define CLI commands: generate, list, analyze, config
   - Map to backend endpoints
   ↓
3. Agent: Test Design Agent
   - Unit tests for CLI commands
   - Integration tests with mock backend
   ↓
4. Agent: Implementation Agent
   - Implement CLI using typer
   - Add HTTP client for backend API
   - Add output formatters
   ↓
5. Agent: Code Review Agent
   ↓
6. Manual testing with running backend
   ↓
7. Commit & PR
```

**CLI Commands Reference** (see SYSTEM-DESIGN.md section 2.4):
- `chosen generate "msg"` → POST /api/v1/messages/generate
- `chosen list` → GET /api/v1/conversations
- `chosen analyze <id>` → GET /api/v1/conversations/{id}/analysis

### 5.3 P2 Workflow (Intelligence Layer)

**Focus**: Analysis agents, intelligent features, caching

**Issues**:
| Issue | Description | Status |
|-------|-------------|--------|
| #78 | ContextAnalyzerAgent | Pending |
| #79 | JobFitAnalyzerAgent | Pending |
| #80-81 | Analysis endpoints + service | Pending |
| #82 | FollowUpTimingOptimizer | Pending |
| #48, #50, #54 | Model refinements | Pending |

#### 5.3.1 Analysis Agent Pattern

```
For each analysis agent (Context, JobFit, Timing, Quality):

1. Create Worktree (feature/<agent-name>)
   ↓
2. Agent: Prompt Engineering Agent
   - Design system prompt
   - Define output schema
   - Create test cases
   ↓
3. Agent: Test Design Agent
   - Unit tests with mocked LLM
   - Integration tests with real API (small dataset)
   - Quality validation tests
   ↓
4. Agent: Test Implementation Agent
   ↓
5. Agent: Solution Design Agent
   - Agent class structure
   - Input validation
   - Output parsing
   - Error handling
   ↓
6. Agent: Implementation Agent
   ↓
7. Manual Prompt Iteration
   - Test with real conversations
   - Measure quality
   - Iterate prompts
   - Update tests if needed
   ↓
8. Agent: Code Review Agent
   ↓
9. Commit & PR
```

#### 5.2.2 Parallel Agent Development

Multiple analysis agents can be developed in parallel:

```
Developer A: feature/context-analyzer
Developer B: feature/job-analyzer
Developer C: feature/timing-optimizer

All following the same pattern, merging as completed.
```

### 5.4 P3 Workflow (Polish & Advanced Features)

**Focus**: Production readiness, frontend, advanced agents

**Issues**:
| Issue | Description | Status |
|-------|-------------|--------|
| #83 | CompanyResearcherAgent | Pending |
| #84 | CompensationNegotiationAgent | Pending |
| #85 | Settings REST endpoints | Pending |
| #86 | React frontend | Pending |
| #46-47, 52-53, 58-65 | Model refinements | Pending |

#### 5.4.1 Specialized Agent Pattern

Same as P2 analysis agents, but more complex:

```
feature/company-researcher-agent (#83)
feature/compensation-negotiation-agent (#84)
```

Each requires:
- More sophisticated prompts
- External tool integration (web search)
- Complex output schemas
- Extensive testing

#### 5.4.2 Frontend Development

```
1. Worktree: feature/react-frontend (#86)
   ↓
2. Initialize React + TypeScript project
   ↓
3. Design component architecture
   ↓
4. Implement core components
   ↓
5. Integrate with backend API
   ↓
6. Manual testing
   ↓
7. PR & Merge
```

#### 5.4.3 Integration Development

```
1. Worktree: feature/<integration-name>
   ↓
2. Research external API/service
   ↓
3. Design integration interface
   ↓
4. Mock external service for tests
   ↓
5. TDD workflow with mocks
   ↓
6. Manual testing with real service
   ↓
7. Error handling refinement
   ↓
8. Documentation
```

#### 5.4.2 Performance Optimization

```
1. Profiling
   - Identify bottlenecks
   - Measure baseline performance
   ↓
2. Optimization Design
   - Caching strategy
   - Query optimization
   - Async improvements
   ↓
3. Implement with benchmarks
   ↓
4. Verify improvements
```

---

## 6. Quality Gates

### 6.1 Pre-Commit Quality Gate

**Enforced by**: Pre-commit hooks

```yaml
Checks:
  - black formatting
  - isort import sorting
  - flake8 linting
  - mypy type checking
  - trailing whitespace
  - YAML validation

Action on Failure:
  - Auto-fix if possible (black, isort)
  - Block commit if cannot fix
  - Display errors to developer
```

### 6.2 Pre-Push Quality Gate

**Enforced by**: Local developer discipline

```bash
# Run before pushing
pytest tests/ --cov=app --cov-report=term

# Must achieve:
# - All tests pass
# - Coverage >= target (85% overall, 90% critical)
```

### 6.3 PR Quality Gate

**Enforced by**: GitHub Actions CI

```yaml
CI Pipeline Checks:
  1. Linting (black, isort, flake8, mypy)
  2. Unit Tests (all pass)
  3. Integration Tests (all pass)
  4. Coverage (meets targets)
  5. Security Scan (Bandit, Safety)
  6. Build Success (Docker image)

PR Requirements:
  - All CI checks pass
  - At least 1 review approval
  - No merge conflicts
  - Branch up to date with main
  - Linked to GitHub issue
```

### 6.4 Milestone Completion Quality Gate

**Enforced by**: Manual checklist (per milestone)

```markdown
P0 Completion Checklist:
- [ ] All P0 tasks from ROADMAP.md completed (#68-70, AI Resilience)
- [ ] CRUD operations for conversations work via REST API
- [ ] AI client handles API outages gracefully
- [ ] All tests passing (unit + integration)
- [ ] Coverage >80% for new code
- [ ] YAML files survive read/write cycles without corruption
- [ ] All P0 PRs merged

P1 Completion Checklist:
- [ ] All P1 tasks from ROADMAP.md completed (#71-77, CLI, #51)
- [ ] CLI command: `chosen generate "message"` returns AI response
- [ ] CLI command: `chosen list` shows conversation history
- [ ] All agents have snapshot tests
- [ ] GitHub Actions runs tests on every PR
- [ ] All P1 PRs merged
```

### 6.5 Merge Quality Gate

**Enforced by**: Branch protection rules

```yaml
Branch Protection (main):
  - Require pull request reviews: 1
  - Require status checks to pass: true
    - ci/lint
    - ci/test
    - ci/security
  - Require branches to be up to date: true
  - Include administrators: true
  - Require linear history: false
  - Require signed commits: false
```

---

## 7. Agent Orchestration Patterns

### 7.1 Sequential Agent Pattern

**Use When**: Each step depends on previous output

**Example**: TDD Workflow

```
Test Design Agent
    ↓ (output: test design doc)
Test Implementation Agent
    ↓ (output: failing tests)
Solution Design Agent
    ↓ (output: implementation design)
Implementation Agent
    ↓ (output: working code)
Code Review Agent
    ↓ (output: review feedback)
```

**Implementation**:
```
/compact to save context between agents
Create new Task agent for each step
Pass previous output as input to next agent
```

### 7.2 Parallel Agent Pattern

**Use When**: Multiple independent tasks

**Example**: Multiple repositories

```
     Main Agent
         |
    ┌────┴────┬────────┐
    ↓         ↓        ↓
ConvRepo  SettingsRepo  MsgRepo
Agent     Agent         Agent
```

**Implementation**:
```
Launch multiple Task agents simultaneously
Each follows TDD workflow independently
Coordinate merge timing
```

### 7.3 Review Loop Pattern

**Use When**: Iterative refinement needed

**Example**: Prompt Engineering

```
Prompt Design Agent → Prompt Review Agent
         ↑                      ↓
         └──── (if changes) ────┘
                    ↓
              (approved)
```

**Implementation**:
```
1. Design agent creates prompt
2. Review agent evaluates
3. If changes needed, loop
4. If approved, proceed
5. Max 3 iterations before escalating
```

### 7.4 Conditional Agent Pattern

**Use When**: Decision point in workflow

**Example**: Refactoring Decision

```
Code Complete
     ↓
Refactoring Evaluation Agent
     ↓
  Decision?
     ├─ Refactor Now → Implementation Agent → Review Agent
     ├─ Refactor Later → Create GitHub Issue
     └─ No Refactor → Proceed to Commit
```

**Implementation**:
```
1. Evaluation agent provides recommendation
2. Main agent interprets decision
3. Route to appropriate next agent
4. Continue workflow
```

### 7.5 Hierarchical Agent Pattern

**Use When**: Complex task with subtasks

**Example**: API Endpoint Development

```
        Main Development Agent
               ↓
    ┌──────────┼──────────┐
    ↓          ↓          ↓
Schema      Endpoint   Service
Design      Design     Design
    ↓          ↓          ↓
Schema      Endpoint   Service
Impl        Impl       Impl
    ↓          ↓          ↓
    └──────────┴──────────┘
               ↓
        Integration Test
```

**Implementation**:
```
1. Break task into subtasks
2. Launch Task agent for each subtask
3. Each follows mini TDD workflow
4. Integrate at the end
5. Run integration tests
```

---

## 8. Development Rituals

### 8.1 Before Starting a Task

```
1. Read GitHub Issue
   - Understand requirements
   - Check acceptance criteria
   - Review linked documents

2. Review Relevant Documentation
   - SYSTEM-DESIGN.md (architecture)
   - PLAN.md (implementation order)
   - INTERFACE-DESIGN.md (UI/UX)

3. Identify Dependencies
   - What must be completed first?
   - What can be parallel?
   - Who else is working on related tasks?

4. Create Worktree
   - Follow naming convention
   - Link data folder if needed

5. Plan Agent Workflow
   - Which agents will be needed?
   - What's the sequence?
   - Where are the decision points?

6. Start TodoWrite
   - Break task into steps
   - Track with todo list
```

### 8.2 During Development

```
1. Follow TDD Workflow Strictly
   - Red: Write failing test
   - Green: Make test pass
   - Refactor: Improve code
   - Repeat

2. Use /compact Regularly
   - Before switching agents
   - When context gets large
   - Remember: task, worktree, current step

3. Commit Frequently
   - Small, focused commits
   - Clear commit messages (conventional commits)
   - One logical change per commit

4. Run Tests Often
   - After each implementation
   - Before committing
   - Full suite before pushing

5. Review Your Own Code
   - Read through changes
   - Check for issues
   - Improve clarity
```

### 8.3 Before Committing

```
1. Run All Quality Checks
   pytest tests/ -v
   black backend/app
   isort backend/app
   flake8 backend/app
   mypy backend/app

2. Check Coverage
   pytest tests/ --cov=app --cov-report=term
   Ensure targets met

3. Review Changes
   git diff
   Check nothing unintended

4. Update Documentation
   - Docstrings
   - README if needed
   - API docs if new endpoints

5. Prepare Commit Message
   - Agent: Write commit message
   - Agent: Review commit message
   - Format: conventional commits
```

### 8.4 Before Creating PR

```
1. Ensure Branch Up to Date
   git fetch origin
   git rebase origin/main
   Resolve conflicts

2. Run Full Test Suite
   pytest tests/
   All must pass

3. Review All Changes
   git diff origin/main
   Ensure coherent changeset

4. Prepare PR Description
   - Agent: Write PR message
   - Agent: Review PR message
   - Include:
     - Summary
     - Changes made
     - Testing done
     - Screenshots (if UI)
     - Related issues

5. Push and Create PR
   git push -u origin <branch>
   gh pr create --fill
```

### 8.5 After PR Review

```
1. Check Review Comments
   - Agent: Parse review comments
   - Create checklist of changes

2. Address Feedback
   - Create sub-tasks if needed
   - Follow TDD for fixes
   - Commit changes

3. Respond to Comments
   - Mark resolved
   - Explain changes

4. Request Re-review
   Comment: "Changes addressed, ready for re-review"

5. After Approval
   - Squash and merge (or merge)
   - Delete branch
   - Remove worktree
   - Close related issue
```

---

## 9. Parallel Development Patterns

### 9.1 Independent Module Development

**Pattern**: Different modules, no dependencies

```
Developer A                    Developer B
feature/conversation-repo      feature/settings-repo
    ↓                              ↓
TDD Workflow                   TDD Workflow
    ↓                              ↓
PR #1                          PR #2
    ↓                              ↓
Merge independently
```

**Coordination**:
- No coordination needed
- Merge in any order
- No conflicts expected

### 9.2 Sequential Module Development

**Pattern**: Module B depends on Module A

```
Developer A                    Developer B
feature/base-agent             (waits)
    ↓
TDD Workflow
    ↓
PR #1 → Merge
    ↓                          ↓
                        feature/context-analyzer
                               ↓
                        TDD Workflow (uses BaseAgent)
                               ↓
                        PR #2 → Merge
```

**Coordination**:
- B waits for A to merge
- B pulls latest main
- B starts development

### 9.3 Parallel with Integration Point

**Pattern**: Multiple modules merge to integration

```
Developer A              Developer B              Developer C
feature/msg-service      feature/conv-service     feature/analysis-service
    ↓                        ↓                        ↓
TDD Workflow             TDD Workflow             TDD Workflow
    ↓                        ↓                        ↓
PR #1 → Merge            PR #2 → Merge            PR #3 → Merge
    └────────────────────────┴────────────────────────┘
                              ↓
                  feature/api-integration
                              ↓
                  Integration Tests
                              ↓
                  PR #4 → Merge
```

**Coordination**:
- Services developed independently
- Integration happens after all merged
- Integration tests verify everything works together

### 9.4 Layered Development

**Pattern**: Bottom-up layer implementation

```
Layer 1 (Data Models):
  Developer A: Conversation model
  Developer B: Message model
  Developer C: Analysis model
  → All merge

Layer 2 (Repositories):
  Developer A: ConversationRepository (depends on Layer 1)
  Developer B: MessageRepository (depends on Layer 1)
  → All merge

Layer 3 (Services):
  Developer A: ConversationService (depends on Layer 2)
  Developer B: MessageService (depends on Layer 2)
  → All merge

Layer 4 (API):
  Developer A: Conversation endpoints (depends on Layer 3)
  Developer B: Message endpoints (depends on Layer 3)
  → All merge
```

**Coordination**:
- Clear layer dependencies
- Wait for layer completion before starting next
- Can parallelize within layer

### 9.5 Feature Branch with Sub-branches

**Pattern**: Complex feature with multiple developers

```
feature/agent-system (main feature branch)
    ├── feature/agent-system-base-agent (Developer A)
    ├── feature/agent-system-orchestrator (Developer B, waits for A)
    ├── feature/agent-system-model-router (Developer C, parallel with A)
    └── feature/agent-system-integration (Developer D, waits for all)

Each sub-branch:
1. Branches from feature/agent-system
2. Develops component with TDD
3. PR to feature/agent-system (not main)
4. After all merged to feature/agent-system
5. PR feature/agent-system → main
```

**Coordination**:
- Feature branch serves as integration point
- Sub-branches merge to feature branch
- Final PR from feature branch to main

---

## 10. Context Management

### 10.1 When to Use /compact

```
1. Before switching agents (always)
   /compact
   Remember: task, worktree, design doc, current step

2. After completing major step
   /compact
   Remember: what's done, what's next

3. When context gets large (>50% of limit)
   /compact
   Preserve critical information only

4. Before long-running operations
   /compact
   Clean slate for agent execution

5. After reading large files
   /compact
   Summarize key points, discard details
```

### 10.2 What to Preserve in /compact

```
Always Remember:
1. Current task description
2. Worktree name and location
3. Current workflow step number
4. Key design decisions
5. Test results or issues
6. Next immediate action

Sometimes Remember:
1. Full design documents (if needed soon)
2. Test code (if implementing)
3. Error messages (if debugging)

Never Remember:
1. Full file contents (re-read if needed)
2. Detailed logs
3. Repeated information
4. Obsolete context
```

### 10.3 Context Handoff Between Agents

```
Main Agent → Sub-agent (via Task tool):

Main Agent:
1. /compact (clean context)
2. Prepare clear instructions for sub-agent
3. Include:
   - Task description
   - Input files/data
   - Expected output format
   - Success criteria
   - Context (relevant only)
4. Launch Task agent
5. Wait for completion

Sub-agent (Task):
1. Receives clear instructions
2. Executes task
3. Returns structured output
4. Main agent receives output

Main Agent (after):
1. /compact
2. Remember: task, step, sub-agent output
3. Continue workflow
```

### 10.4 Session Management

```
Long Development Session:

Hour 0:
  - Start task
  - Create worktree
  - Launch first agent

Hour 1:
  - /compact
  - Progress check
  - Continue

Hour 2:
  - /compact
  - Consider break

Hour 3:
  - /compact
  - Review overall progress
  - Adjust plan if needed

Hour 4:
  - /compact
  - Push work so far
  - End session or continue

Resuming Session:
  - Read commit history
  - Check current branch
  - Review last step in todo
  - /compact
  - Continue
```

---

## 11. Integration Points

### 11.1 Git Integration

```
Workflow Integration:

1. Issue Tracking
   - All tasks from GitHub issues
   - Link commits to issues (#123)
   - Link PRs to issues (fixes #123)

2. Branch Management
   - Feature branches from issues
   - Worktrees for isolation
   - Clean merge history

3. Commit Messages
   - Agent: Write commit message
   - Agent: Review commit message
   - Format: Conventional Commits
   - Example: "feat(repo): add ConversationRepository with YAML storage"

4. Pull Requests
   - Agent: Write PR description
   - Agent: Review PR description
   - Template: GitHub PR template
   - Automation: CI checks, project board
```

### 11.2 GitHub Actions Integration

```
CI/CD Pipeline:

1. On Push:
   - Lint check
   - Type check
   - Unit tests
   - Security scan

2. On PR:
   - All above +
   - Integration tests
   - E2E tests
   - Coverage report
   - Build verification

3. On Merge to Main:
   - Deploy to staging
   - Run smoke tests
   - Tag version (if applicable)

4. On Tag:
   - Deploy to production
   - Create GitHub release
   - Generate changelog
```

### 11.3 Project Board Integration

```
GitHub Project Board:

Columns:
1. Backlog (Issues created)
2. Ready (Assigned, requirements clear)
3. In Progress (Worktree created)
4. In Review (PR created)
5. Done (PR merged)

Automation:
- Issue created → Backlog
- Issue assigned → Ready
- PR created → In Review
- PR merged → Done

Developer Actions:
- Move to "In Progress" when starting
- Update status in comments
- Link PRs to issues
```

### 11.4 Documentation Integration

```
Documentation Workflow:

1. Code Documentation
   - Docstrings in code (Google style)
   - Type hints
   - Inline comments for complex logic

2. API Documentation
   - Auto-generated from FastAPI
   - Available at /api/docs
   - Updated automatically

3. User Documentation
   - Updated with features
   - Agent: Documentation Agent
   - Markdown in docs/

4. Architecture Documentation
   - Keep SYSTEM-DESIGN.md updated
   - Add diagrams for new components
   - Update after significant changes
```

---

## 12. Practical Examples

### 12.1 Example: Implementing ConversationRepository

**Full workflow from start to finish**

```
1. GitHub Issue
   Title: Implement ConversationRepository
   Description: Create repository for managing conversation data with YAML storage
   Acceptance Criteria:
   - CRUD operations
   - Filtering and pagination
   - Index management
   - Error handling
   - >90% test coverage

2. Create Worktree
   cd D:\src\chosen\v2
   git worktree add -b feature/conversation-repository ../conversation-repository
   cd ../conversation-repository
   mklink /J data ..\v2\data

3. Initialize TodoWrite
   TodoWrite:
   1. Design unit tests (pending)
   2. Implement unit tests (pending)
   3. Design solution (pending)
   4. Implement solution (pending)
   5. Review code (pending)
   6. Integration tests (pending)
   7. Commit and PR (pending)

4. Launch Test Design Agent
   Task: Design comprehensive unit tests for ConversationRepository

   Input:
   - Interface: RepositoryBase (from SYSTEM-DESIGN.md)
   - Requirements: CRUD, filtering, pagination
   - Data format: YAML files

   Output: [Test design document with all test cases]

   Update TodoWrite: Step 1 → completed, Step 2 → in_progress

5. /compact
   Remember:
   - Task: ConversationRepository
   - Worktree: D:\src\chosen\conversation-repository
   - Test design: [summary]
   - Current step: 2 (implement tests)

6. Launch Test Implementation Agent
   Task: Implement unit tests based on design

   Input: Test design document
   Output: D:\...\tests\unit\test_conversation_repo.py

   Update TodoWrite: Step 2 → completed, Step 3 → in_progress

7. Run Tests (should fail)
   cd backend
   pytest tests/unit/test_conversation_repo.py
   Result: All tests fail (no implementation yet) ✓

8. /compact
   Remember:
   - Task: ConversationRepository
   - Worktree: D:\src\chosen\conversation-repository
   - Tests: Failing as expected
   - Current step: 3 (design solution)

9. Launch Solution Design Agent
   Task: Design ConversationRepository implementation

   Input:
   - Tests
   - RepositoryBase interface
   - YAML storage requirements

   Output: [Implementation design document]

   Update TodoWrite: Step 3 → completed, Step 4 → in_progress

10. /compact
    Remember:
    - Task: ConversationRepository
    - Worktree: D:\src\chosen\conversation-repository
    - Design: [summary]
    - Current step: 4 (implement)

11. Launch Implementation Agent
    Task: Implement ConversationRepository

    Input: Design document, failing tests
    Output: D:\...\app\data\conversation_repo.py

    Update TodoWrite: Step 4 → completed, Step 5 → in_progress

12. Run Tests (should pass)
    pytest tests/unit/test_conversation_repo.py
    Result: All tests pass ✓
    Coverage: 92% ✓

13. /compact
    Remember:
    - Task: ConversationRepository
    - Worktree: D:\src\chosen\conversation-repository
    - Implementation: Complete, tests passing
    - Current step: 5 (review)

14. Launch Code Review Agent
    Task: Review ConversationRepository implementation

    Input:
    - Implementation code
    - Test code
    - Design document

    Output: [Review report - approved with minor suggestions]

    Apply suggestions, re-run tests

    Update TodoWrite: Step 5 → completed, Step 6 → in_progress

15. /compact
    Remember:
    - Task: ConversationRepository
    - Worktree: D:\src\chosen\conversation-repository
    - Status: Code reviewed and approved
    - Current step: 6 (integration tests)

16. Launch Integration Test Design Agent
    Task: Design integration tests with real file system

    Output: [Integration test design]

17. Launch Test Implementation Agent
    Task: Implement integration tests

    Output: D:\...\tests\integration\test_conversation_repo_integration.py

18. Run Integration Tests
    pytest tests/integration/test_conversation_repo_integration.py
    Result: All pass ✓

    Update TodoWrite: Step 6 → completed, Step 7 → in_progress

19. Pre-commit Checks
    black backend/app
    isort backend/app
    flake8 backend/app
    mypy backend/app
    Result: All pass ✓

20. Commit
    Launch: Write Commit Message Agent
    Output: "feat(data): implement ConversationRepository with YAML storage

    - Add ConversationRepository with CRUD operations
    - Implement file-based storage with YAML format
    - Add index management for fast lookups
    - Include comprehensive error handling
    - Achieve 92% test coverage

    Closes #42"

    git add .
    git commit -m "[message above]"

21. Push
    git push -u origin feature/conversation-repository

    Update TodoWrite: Step 7 → completed

22. Create PR
    Launch: Write PR Description Agent

    Output: [PR description with summary, changes, testing]

    gh pr create --fill

    TodoWrite: All completed

23. Wait for Review
    - CI checks pass
    - Reviewer approves

24. Merge PR
    gh pr merge --squash

25. Cleanup
    cd D:\src\chosen\v2
    git worktree remove ../conversation-repository
    git branch -d feature/conversation-repository

26. /clear
```

### 12.2 Example: Implementing Context Analyzer Agent

**Agent implementation with prompt engineering**

```
1. GitHub Issue
   Title: Implement Context Analyzer Agent
   Description: Create agent to analyze conversation context and patterns

2. Create Worktree
   feature/context-analyzer

3. Launch Prompt Engineering Agent
   Task: Design prompts for ContextAnalyzer

   Input:
   - Requirements: sentiment, stage, patterns, recommendations
   - Model: Sonnet
   - Output: ContextAnalysis schema

   Output:
   - System prompt
   - User prompt template
   - Output format specification
   - Test cases

4. /compact
   Remember: Task, worktree, prompt design

5. Standard TDD Workflow
   - Test Design Agent
   - Test Implementation Agent (mock LLM responses)
   - Solution Design Agent
   - Implementation Agent
   - Code Review Agent

6. Manual Prompt Testing
   - Test with 5-10 real conversations
   - Evaluate quality of analysis
   - Iterate on prompts if needed
   - Update tests with better examples

7. Integration with Orchestrator
   - Test agent via orchestrator
   - Verify streaming works
   - Test error handling

8. Commit, PR, Merge

9. Cleanup
```

---

## Summary

This multi-agent development process provides:

1. **Clear Agent Roles**: Specialized agents for each concern (test design, implementation, review, etc.)

2. **Structured Workflows**: Phase-specific patterns adapted from base TDD workflow

3. **Worktree Strategy**: Isolation for parallel development with clear conventions

4. **Quality Gates**: Multiple checkpoints ensure high quality code

5. **Orchestration Patterns**: Sequential, parallel, conditional, hierarchical agent patterns

6. **Development Rituals**: Clear processes for before, during, and after development

7. **Parallel Patterns**: Strategies for coordinating multiple developers

8. **Context Management**: When and how to use /compact for efficiency

9. **Integration Points**: Git, GitHub Actions, documentation workflows

10. **Practical Examples**: Real-world walkthroughs of common tasks

**Key Success Factors**:

1. Follow TDD strictly (red-green-refactor)
2. Use specialized agents for different concerns
3. /compact regularly to manage context
4. Run tests frequently
5. Commit small, focused changes
6. Review your own code before submitting
7. Communicate with team on dependencies
8. Keep documentation up to date
9. Respect quality gates
10. Learn from each iteration

This process is designed to be practical and actionable, providing clear guidance for developers at every step while maintaining flexibility for the project's unique needs.
