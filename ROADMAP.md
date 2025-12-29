# CHOSEN Roadmap

**CHOSEN** - Candidate's Helper for Optimized Seeker-Employer Networking

This roadmap outlines the development path toward a minimal working system where users can perform basic recruitment communication tasks.

## Current State

### Completed
1. **Core Data Models** - Pydantic models implemented and tested
   - Enums: Platform, ProcessStatus, ParticipantRole
   - Models: Message, Participant, Conversation, UserSettings
   - Analysis: SentimentTrend, ConversationStage, ContextAnalysis, JobFitScore
   - Metrics: ResponseMetrics
   - Validators: Path validation, field constraints

2. **Project Infrastructure**
   - Python backend structure (FastAPI)
   - Testing framework (pytest with coverage)
   - Pre-commit hooks (black, isort, flake8, mypy)
   - Basic health endpoint

3. **Data Layer Foundation**
   - FileHandler: File operations with read/write/lock (#66)
   - YAMLHandler: YAML serialization with validation (#67)

### In Progress
- Model refinements and documentation
- GitHub Actions for automated testing (#51)

---

## Timeline Estimates

| Milestone | Issues | Estimate | Cumulative |
|-----------|--------|----------|------------|
| P0: Minimal Backend | 6 | 4-5 weeks | 4-5 weeks |
| P1: Core + CLI | 9 | 5-7 weeks | 9-12 weeks |
| P2: Intelligence | 8 | 6-8 weeks | 15-20 weeks |
| P3: Polish | 16 | 8-12 weeks | 23-32 weeks |

**Assumptions**:
- Solo developer, 15-20 hours/week
- Claude Code assistance accelerates development
- Anthropic API available (see [RISKS.md](docs/planning/RISKS.md) for fallback)
- Prompt engineering iteration included (20% buffer)

---

## Milestone 1: Minimal Working Backend (MVP)

**Goal**: Persist conversations and provide basic API with AI resilience

### P0 - Critical Path (Must Complete First)

| # | Issue | Description | Status |
|---|-------|-------------|--------|
| 66 | feat(data): Implement FileHandler | File operations (read/write/lock) | Done |
| 67 | feat(data): Implement YAMLHandler | YAML serialization with validation | Done |
| 68 | feat(data): Implement RepositoryBase | Abstract CRUD interface with atomic writes | Pending |
| 69 | feat(data): Implement ConversationRepository | Conversation CRUD with indexing | Pending |
| 70 | feat(api): Implement Conversation REST endpoints | CRUD API for conversations | Pending |
| NEW | feat(agents): Implement AI Resilience Layer | Anthropic client with retries/fallback | Pending |

**Dependency Order**:
```
FileHandler → YAMLHandler → RepositoryBase → ConversationRepository → Conversation API
                                                                            ↓
                                                                   AI Resilience Layer
```

### P0 Success Criteria

- [ ] Can create conversation via POST /api/v1/conversations
- [ ] Can retrieve conversation via GET /api/v1/conversations/{id}
- [ ] Can update and delete conversations
- [ ] API returns proper error codes (400/404/500)
- [ ] Conversations persist to YAML in data/conversations/
- [ ] YAML files survive read/write cycles without corruption
- [ ] AI client handles Anthropic API outages gracefully (retry + fallback)
- [ ] Unit test coverage >80% for new code
- [ ] Integration test demonstrates full CRUD flow

---

## Milestone 2: Core Features

**Goal**: Generate responses, parse messages, CLI tool for "ready version"

### P1 - High Priority

| # | Issue | Description |
|---|-------|-------------|
| 71 | feat(agents): Implement ModelRouter | Claude API routing (Haiku/Sonnet/Opus) |
| 72 | feat(agents): Implement BaseAgent | Abstract agent base class |
| 73 | feat(agents): Implement AgentOrchestrator | Multi-agent execution manager |
| 74 | feat(agents): Implement ResponseGeneratorAgent | Generate professional responses |
| 75 | feat(api): Implement Message REST endpoints | Message parsing and generation API |
| 76 | feat(services): Implement ConversationService | Business logic layer |
| 77 | feat(services): Implement MessageService | Message handling logic |
| NEW | feat(cli): Implement CLI Tool | Command-line interface for generating responses |
| 51 | Add GitHub Actions workflow | CI/CD automation |

### P1 Success Criteria

- [ ] CLI command: `chosen generate "message text"` returns AI response
- [ ] CLI command: `chosen list` shows conversation history
- [ ] ResponseGeneratorAgent produces professional recruitment responses
- [ ] AgentOrchestrator routes to correct agent based on task type
- [ ] Non-technical user can use CLI to generate responses
- [ ] All agents have snapshot tests for quality regression
- [ ] GitHub Actions runs tests on every PR

**After Milestone 2, the system can**:
1. Store and retrieve conversations
2. Parse incoming messages
3. Generate AI-powered responses via CLI
4. Basic conversation management
5. Automated CI/CD pipeline

---

## Milestone 3: Intelligence Layer

**Goal**: Advanced analysis and insights

### P2 - Medium Priority

| # | Issue | Description |
|---|-------|-------------|
| 78 | feat(agents): Implement ContextAnalyzerAgent | Conversation analysis |
| 79 | feat(agents): Implement JobFitAnalyzerAgent | Job-candidate fit scoring |
| 80 | feat(api): Implement Analysis REST endpoints | Analysis API |
| 81 | feat(services): Implement AnalysisService | Analysis orchestration |
| 82 | feat(agents): Implement FollowUpTimingOptimizer | Follow-up timing |
| 48 | Integrate Participant model into Conversation | Model integration |
| 50 | Add length constraints to string fields | Input validation |
| 54 | Link Participant model to Conversation | Model relationships |

### P2 Success Criteria

- [ ] CLI command: `chosen analyze <conversation_id>` shows context analysis
- [ ] JobFitAnalyzerAgent produces scores with explanations
- [ ] FollowUpTimingOptimizer suggests optimal follow-up timing
- [ ] Analysis endpoints return structured JSON results
- [ ] Participant model fully integrated with conversations

---

## Milestone 4: Polish and Advanced Features

**Goal**: Production readiness, frontend, advanced agents

### P3 - Lower Priority

| # | Issue | Description |
|---|-------|-------------|
| 83 | feat(agents): Implement CompanyResearcherAgent | Company research |
| 84 | feat(agents): Implement CompensationNegotiationAgent | Negotiation guidance |
| 85 | feat(api): Implement Settings REST endpoints | User settings API |
| 86 | feat(frontend): Initialize React frontend | Web UI |
| 46-47, 52-53, 58-65 | Model refinements | Documentation and edge cases |

### P3 Success Criteria

- [ ] React frontend deployed and functional
- [ ] CompanyResearcherAgent provides relevant company context
- [ ] User settings persist and affect agent behavior
- [ ] All model documentation complete
- [ ] Production deployment guide available

---

## Priority Definitions

| Label | Meaning | Impact |
|-------|---------|--------|
| **P0** | Critical | Blocks all progress; must be done first |
| **P1** | High | Core feature; needed for basic functionality |
| **P2** | Medium | Important but not blocking; enhances value |
| **P3** | Low | Nice to have; can be deferred |

---

## Risks and Mitigations

See [docs/planning/RISKS.md](docs/planning/RISKS.md) for detailed risk analysis.

**Top Risks**:
| Risk | Severity | Mitigation |
|------|----------|------------|
| Anthropic API unavailable | High | AI Resilience Layer with retries + caching |
| YAML data corruption | High | Atomic writes + backups in RepositoryBase |
| Prompt engineering costs | Medium | Budget tracking + Haiku for development |
| Agent quality untestable | Medium | Snapshot testing + evaluation metrics |

---

## Quick Start Guide

To get a minimal working system:

1. **Complete P0 issues in order**:
   ```
   #66 → #67 → #68 → #69 → #70 (Data Layer) - #66, #67 DONE
   AI Resilience Layer (Anthropic client)
   ```

2. **Then P1 issues**:
   ```
   #71 → #72 → #73 (Agent Foundation)
   #74 → #75 → #76 → #77 (Core Features)
   CLI Tool (user interface)
   ```

3. **Test the system**:
   - Create a conversation via API
   - Add messages to conversation
   - Generate a response via CLI: `chosen generate "message"`
   - Retrieve conversation

---

## Issue Statistics

| Priority | Count | Status |
|----------|-------|--------|
| P0 | 6 | 2 Done, 3 Pending, 1 New |
| P1 | 9 | 8 Pending, 1 New |
| P2 | 8 | Pending |
| P3 | 16 | Pending |
| **Total Open** | **37** | - |

*Note: Issue #45 (archive consistency validation) completed in PR #87. Issues #66, #67 completed.*

---

## References

- [SYSTEM-DESIGN.md](docs/SYSTEM-DESIGN.md) - Technical architecture
- [DEV-PLAN.md](docs/DEV-PLAN.md) - Development phases
- [requirements.md](docs/requirements.md) - Product requirements
- [INTERFACE-DESIGN.md](docs/INTERFACE-DESIGN.md) - UI/UX specification
- [RISKS.md](docs/planning/RISKS.md) - Risk analysis and mitigations

---

*Last updated: 2025-12-27*
