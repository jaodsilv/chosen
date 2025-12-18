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

### In Progress
- Model refinements and documentation
- GitHub Actions for automated testing (#51)

---

## Milestone 1: Minimal Working Backend (MVP)

**Goal**: Persist conversations and generate AI responses via API

### P0 - Critical Path (Must Complete First)

| # | Issue | Description |
|---|-------|-------------|
| 66 | [feat(data): Implement FileHandler](../../issues/66) | File operations (read/write/lock) |
| 67 | [feat(data): Implement YAMLHandler](../../issues/67) | YAML serialization with validation |
| 68 | [feat(data): Implement RepositoryBase](../../issues/68) | Abstract CRUD interface |
| 69 | [feat(data): Implement ConversationRepository](../../issues/69) | Conversation CRUD with indexing |
| 70 | [feat(api): Implement Conversation REST endpoints](../../issues/70) | CRUD API for conversations |
| 71 | [feat(agents): Implement ModelRouter](../../issues/71) | Claude API routing (Haiku/Sonnet/Opus) |
| 72 | [feat(agents): Implement BaseAgent](../../issues/72) | Abstract agent base class |
| 73 | [feat(agents): Implement AgentOrchestrator](../../issues/73) | Multi-agent execution manager |

**Dependency Order**:
```
FileHandler → YAMLHandler → RepositoryBase → ConversationRepository → Conversation API
                                    ↓
                            ModelRouter → BaseAgent → AgentOrchestrator
```

---

## Milestone 2: Core Features

**Goal**: Generate responses, parse messages, basic analysis

### P1 - High Priority

| # | Issue | Description |
|---|-------|-------------|
| 74 | [feat(agents): Implement ResponseGeneratorAgent](../../issues/74) | Generate professional responses |
| 75 | [feat(api): Implement Message REST endpoints](../../issues/75) | Message parsing and generation API |
| 76 | [feat(services): Implement ConversationService](../../issues/76) | Business logic layer |
| 77 | [feat(services): Implement MessageService](../../issues/77) | Message handling logic |
| 51 | [Add GitHub Actions workflow](../../issues/51) | CI/CD automation |

**After Milestone 2, the system can**:
1. Store and retrieve conversations
2. Parse incoming messages
3. Generate AI-powered responses
4. Basic conversation management

---

## Milestone 3: Intelligence Layer

**Goal**: Advanced analysis and insights

### P2 - Medium Priority

| # | Issue | Description |
|---|-------|-------------|
| 78 | [feat(agents): Implement ContextAnalyzerAgent](../../issues/78) | Conversation analysis |
| 79 | [feat(agents): Implement JobFitAnalyzerAgent](../../issues/79) | Job-candidate fit scoring |
| 80 | [feat(api): Implement Analysis REST endpoints](../../issues/80) | Analysis API |
| 81 | [feat(services): Implement AnalysisService](../../issues/81) | Analysis orchestration |
| 82 | [feat(agents): Implement FollowUpTimingOptimizer](../../issues/82) | Follow-up timing |
| 48 | [Integrate Participant model into Conversation](../../issues/48) | Model integration |
| 50 | [Add length constraints to string fields](../../issues/50) | Input validation |
| 54 | [Link Participant model to Conversation](../../issues/54) | Model relationships |

---

## Milestone 4: Polish and Advanced Features

**Goal**: Production readiness, frontend, advanced agents

### P3 - Lower Priority

| # | Issue | Description |
|---|-------|-------------|
| 83 | [feat(agents): Implement CompanyResearcherAgent](../../issues/83) | Company research |
| 84 | [feat(agents): Implement CompensationNegotiationAgent](../../issues/84) | Negotiation guidance |
| 85 | [feat(api): Implement Settings REST endpoints](../../issues/85) | User settings API |
| 86 | [feat(frontend): Initialize React frontend](../../issues/86) | Web UI |
| 45-47, 52-53, 58-65 | Model refinements | Documentation and edge cases |

---

## Priority Definitions

| Label | Meaning | Impact |
|-------|---------|--------|
| **P0** | Critical | Blocks all progress; must be done first |
| **P1** | High | Core feature; needed for basic functionality |
| **P2** | Medium | Important but not blocking; enhances value |
| **P3** | Low | Nice to have; can be deferred |

---

## Quick Start Guide

To get a minimal working system:

1. **Complete P0 issues in order**:
   ```
   #66 → #67 → #68 → #69 → #70 (Data Layer)
   #71 → #72 → #73 (Agent Foundation)
   ```

2. **Then P1 issues**:
   ```
   #74 → #75 → #76 → #77 (Core Features)
   ```

3. **Test the system**:
   - Create a conversation via API
   - Add messages to conversation
   - Generate a response
   - Retrieve conversation

---

## Issue Statistics

| Priority | Count | Status |
|----------|-------|--------|
| P0 | 8 | Pending |
| P1 | 5 | Pending |
| P2 | 8 | Pending |
| P3 | 17 | Pending |
| **Total Open** | **38** | - |

---

## References

- [SYSTEM-DESIGN.md](../.thoughts/v2/SYSTEM-DESIGN.md) - Technical architecture
- [DEV-PLAN.md](../.thoughts/v2/DEV-PLAN.md) - Development phases
- [requirements.md](../.thoughts/v2/requirements.md) - Product requirements
- [INTERFACE-DESIGN.md](../.thoughts/v2/INTERFACE-DESIGN.md) - UI/UX specification

---

*Last updated: 2025-12-18*
