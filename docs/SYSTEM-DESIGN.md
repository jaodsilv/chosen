# CHOSEN - System Design

**Version**: 2.0.0
**Created**: 2025-12-09
**Status**: Design Document - Ready for Implementation
**Author**: Agent 30 - System Design Specialist

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Backend Architecture](#3-backend-architecture)
4. [Agent System Design](#4-agent-system-design)
5. [Data Architecture](#5-data-architecture)
6. [Real-time Communication](#6-real-time-communication)
7. [Security Design](#7-security-design)
8. [Error Handling & Recovery](#8-error-handling--recovery)
9. [Testing Strategy](#9-testing-strategy)
10. [Implementation Roadmap](#10-implementation-roadmap)
11. [Appendices](#11-appendices)

---

## 1. Executive Summary

### 1.1 System Purpose

CHOSEN (Candidate's Helper for Optimized Seeker-Employer Networking) is a comprehensive system designed to automate and enhance professional recruitment communication. It combines intelligent conversation analysis, strategic response generation, and data-driven insights to help users manage job hunting workflows efficiently.

### 1.2 Key Design Principles

1. **Modularity**: Each component has a single, well-defined responsibility
2. **Intelligence**: AI-driven analysis and pattern detection at every layer
3. **User Control**: Automation with human oversight and easy overrides
4. **Data Privacy**: Local-first storage with encryption for sensitive data
5. **Extensibility**: Plugin architecture for agents, commands, and output styles

### 1.3 Technology Stack

```yaml
Backend:
  Framework: FastAPI (Python 3.11+)
  API Client: Anthropic Claude SDK
  Data Storage: File-based (YAML, JSON)
  Encryption: git-crypt for sensitive data

Frontend:
  Primary: CLI (Claude Code Agent SDK)
  Secondary: Web UI (React + TypeScript)
  Real-time: WebSocket (FastAPI WebSocket)

Infrastructure:
  Runtime: Python 3.11+
  Package Manager: pip
  Version Control: Git
  Testing: pytest, unittest.mock
```

### 1.4 Core Use Cases

1. **Conversation Management**: Track and organize recruiter communications
2. **Intelligent Response Generation**: Context-aware, strategic message drafting
3. **Follow-up Optimization**: Timing recommendations and automated reminders
4. **Job Fit Analysis**: Automated scoring and gap analysis
5. **Compensation Negotiation**: Strategic guidance and market intelligence
6. **Multi-Conversation Analytics**: Aggregate insights across all opportunities

---

## 2. High-Level Architecture

### 2.1 System Components Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interfaces                          │
├──────────────────────────────┬──────────────────────────────────┤
│    Claude Code CLI Agent     │      Web UI (Optional)           │
│      - Commands              │      - Dashboard                 │
│      - Agents                │      - Message Editor            │
│      - Output Styles         │      - Analytics View            │
└──────────────┬───────────────┴──────────────┬───────────────────┘
               │                              │
               │  HTTP/REST API               │  WebSocket
               │                              │
┌──────────────┴──────────────────────────────┴───────────────────┐
│                      FastAPI Backend                             │
├──────────────────────────────────────────────────────────────────┤
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │  API Layer     │  │  Service Layer  │  │  Agent System    │  │
│  │  - Endpoints   │  │  - Business     │  │  - Orchestrator  │  │
│  │  - Validation  │  │    Logic        │  │  - Agent Pool    │  │
│  │  - WebSocket   │  │  - Workflows    │  │  - Model Router  │  │
│  └────────┬───────┘  └────────┬────────┘  └────────┬─────────┘  │
│           │                   │                    │             │
│  ┌────────┴───────────────────┴────────────────────┴─────────┐  │
│  │              Data Access Layer (DAL)                       │  │
│  │  - File Operations                                         │  │
│  │  - YAML/JSON Parsing                                       │  │
│  │  - Schema Validation                                       │  │
│  │  - Encryption/Decryption                                   │  │
│  └────────────────────────────┬───────────────────────────────┘  │
└────────────────────────────────┼──────────────────────────────────┘
                                 │
┌────────────────────────────────┴──────────────────────────────────┐
│                     Data Storage Layer                            │
├───────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │ Conversation    │  │ Settings &       │  │ Analysis Cache  │  │
│  │ History Files   │  │ User Data        │  │ (Optional)      │  │
│  │ (YAML)          │  │ (Encrypted)      │  │ (JSON)          │  │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘  │
└───────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────┐
│                    External Services                              │
├───────────────────────────────────────────────────────────────────┤
│  - Anthropic Claude API (Haiku, Sonnet, Opus)                     │
│  - Web Search (Optional - for research agents)                    │
└───────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow Architecture

```
User Input (Raw Message)
    │
    ▼
┌─────────────────────────────────┐
│  1. Message Parser Service      │
│     - Platform Detection        │
│     - Information Extraction    │
│     - Template Matching         │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  2. Conversation Service         │
│     - History Update             │
│     - Status Inference           │
│     - Metadata Enrichment        │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  3. Analysis Agent System        │
│     - Context Analysis           │
│     - Fit Scoring                │
│     - Sentiment Tracking         │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  4. Response Generation          │
│     - Template Selection         │
│     - Content Generation         │
│     - Quality Scoring            │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  5. User Review & Edit           │
│     - Display to User            │
│     - Collect Feedback           │
│     - Track Modifications        │
└─────────┬───────────────────────┘
          │
          ▼
    User Sends Message
```

### 2.3 Technology Stack Rationale

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Backend Framework** | FastAPI | Modern, async, type-safe, automatic API docs, WebSocket support |
| **Language** | Python 3.11+ | Rich ecosystem, AI/ML libraries, user familiarity, type hints |
| **AI Client** | Anthropic SDK | Official SDK, streaming support, model routing |
| **Data Format** | YAML/JSON | Human-readable, version-controllable, easy to edit |
| **Encryption** | git-crypt | Transparent encryption, Git integration, key management |
| **CLI Agent SDK** | Claude Code | Native integration, agent architecture, command system |
| **Frontend (Optional)** | React + TS | Component-based, type-safe, rich ecosystem |
| **Real-time** | WebSocket | Bidirectional, low-latency, native FastAPI support |
| **Testing** | pytest | Python standard, fixtures, mocking, async support |

---

## 3. Backend Architecture

### 3.1 FastAPI Application Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI application entry point
│   ├── config.py                    # Configuration management
│   ├── dependencies.py              # Dependency injection
│   │
│   ├── api/                         # API Layer
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── conversations.py    # Conversation endpoints
│   │   │   ├── messages.py         # Message endpoints
│   │   │   ├── analysis.py         # Analysis endpoints
│   │   │   ├── settings.py         # Settings endpoints
│   │   │   └── websocket.py        # WebSocket endpoints
│   │   ├── schemas/                # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   ├── analysis.py
│   │   │   └── settings.py
│   │   └── middleware/             # Custom middleware
│   │       ├── __init__.py
│   │       ├── error_handler.py
│   │       └── logging.py
│   │
│   ├── services/                    # Service Layer (Business Logic)
│   │   ├── __init__.py
│   │   ├── conversation_service.py
│   │   ├── message_service.py
│   │   ├── analysis_service.py
│   │   ├── response_service.py
│   │   └── settings_service.py
│   │
│   ├── agents/                      # Agent System
│   │   ├── __init__.py
│   │   ├── orchestrator.py         # Agent orchestration
│   │   ├── base_agent.py           # Base agent class
│   │   ├── model_router.py         # Model selection logic
│   │   ├── streaming.py            # Streaming support
│   │   │
│   │   ├── analysis/               # Analysis agents
│   │   │   ├── __init__.py
│   │   │   ├── context_analyzer.py
│   │   │   ├── job_analyzer.py
│   │   │   ├── timing_optimizer.py
│   │   │   └── quality_scorer.py
│   │   │
│   │   ├── generation/             # Generation agents
│   │   │   ├── __init__.py
│   │   │   ├── response_generator.py
│   │   │   ├── followup_generator.py
│   │   │   └── negotiation_generator.py
│   │   │
│   │   └── specialized/            # Specialized agents
│   │       ├── __init__.py
│   │       ├── company_researcher.py
│   │       ├── gap_researcher.py
│   │       └── multi_analytics.py
│   │
│   ├── data/                        # Data Access Layer
│   │   ├── __init__.py
│   │   ├── repository_base.py      # Base repository
│   │   ├── conversation_repo.py
│   │   ├── message_repo.py
│   │   ├── settings_repo.py
│   │   ├── file_handler.py         # File I/O operations
│   │   ├── yaml_handler.py         # YAML operations
│   │   └── encryption.py           # Encryption/decryption
│   │
│   ├── models/                      # Data Models
│   │   ├── __init__.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── participant.py
│   │   ├── analysis.py
│   │   └── settings.py
│   │
│   ├── utils/                       # Utilities
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   ├── datetime_utils.py
│   │   └── template_engine.py
│   │
│   └── core/                        # Core functionality
│       ├── __init__.py
│       ├── exceptions.py           # Custom exceptions
│       ├── constants.py            # System constants
│       └── events.py               # Event system
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── conftest.py                 # pytest fixtures
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── data/                            # Data storage (git-crypt encrypted)
│   ├── conversations/
│   ├── settings/
│   └── cache/
│
├── prompts/                         # Prompt templates
│   ├── system_prompts/
│   └── templates/
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

### 3.2 FastAPI Main Application

```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.api.routes import (
    conversations,
    messages,
    analysis,
    settings,
    websocket
)
from app.api.middleware.error_handler import error_handling_middleware
from app.core.exceptions import AppException
from app.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CHOSEN API",
    description="Backend API for intelligent recruitment communication",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Get settings
settings = get_settings()

# CORS middleware (for web UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom error handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "message": exc.message,
            "details": exc.details
        }
    )

# Include routers
app.include_router(
    conversations.router,
    prefix="/api/v1/conversations",
    tags=["conversations"]
)
app.include_router(
    messages.router,
    prefix="/api/v1/messages",
    tags=["messages"]
)
app.include_router(
    analysis.router,
    prefix="/api/v1/analysis",
    tags=["analysis"]
)
app.include_router(
    settings.router,
    prefix="/api/v1/settings",
    tags=["settings"]
)
app.include_router(
    websocket.router,
    prefix="/api/v1/ws",
    tags=["websocket"]
)

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting CHOSEN API v2.0.0")
    # Initialize agent system
    # Load configurations
    # Verify data directories

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down CHOSEN API")
    # Cleanup resources
```

### 3.3 API Endpoints Specification

#### 3.3.1 Conversation Endpoints

```python
# app/api/routes/conversations.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.api.schemas.conversation import (
    ConversationResponse,
    ConversationCreate,
    ConversationUpdate,
    ConversationQuery
)
from app.services.conversation_service import ConversationService

router = APIRouter()

@router.get("/", response_model=List[ConversationResponse])
async def list_conversations(
    status: Optional[str] = None,
    platform: Optional[str] = None,
    company: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    service: ConversationService = Depends()
):
    """
    List all conversations with optional filtering.

    Query Parameters:
    - status: Filter by process status
    - platform: Filter by platform (linkedin, email)
    - company: Filter by company name
    - limit: Max results (default 50)
    - offset: Pagination offset (default 0)
    """
    return await service.list_conversations(
        status=status,
        platform=platform,
        company=company,
        limit=limit,
        offset=offset
    )

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    service: ConversationService = Depends()
):
    """Get a specific conversation by ID."""
    conversation = await service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    service: ConversationService = Depends()
):
    """Create a new conversation."""
    return await service.create_conversation(conversation)

@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    update: ConversationUpdate,
    service: ConversationService = Depends()
):
    """Update an existing conversation."""
    return await service.update_conversation(conversation_id, update)

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    service: ConversationService = Depends()
):
    """Delete (archive) a conversation."""
    await service.archive_conversation(conversation_id)
    return {"status": "archived"}

@router.post("/{conversation_id}/analyze")
async def analyze_conversation(
    conversation_id: str,
    service: ConversationService = Depends()
):
    """Trigger analysis for a conversation."""
    return await service.analyze_conversation(conversation_id)
```

#### 3.3.2 Message Endpoints

```python
# app/api/routes/messages.py
from fastapi import APIRouter, Depends
from app.api.schemas.message import (
    MessageResponse,
    MessageCreate,
    ResponseGenerateRequest,
    ResponseGenerateResponse
)
from app.services.message_service import MessageService

router = APIRouter()

@router.post("/parse")
async def parse_message(
    raw_message: str,
    platform: str,
    service: MessageService = Depends()
):
    """Parse raw message text and extract structured data."""
    return await service.parse_message(raw_message, platform)

@router.post("/conversations/{conversation_id}/messages")
async def add_message(
    conversation_id: str,
    message: MessageCreate,
    service: MessageService = Depends()
):
    """Add a new message to a conversation."""
    return await service.add_message(conversation_id, message)

@router.post("/generate-response")
async def generate_response(
    request: ResponseGenerateRequest,
    service: MessageService = Depends()
):
    """
    Generate a response to a recruiter message.

    Request Body:
    - conversation_id: ID of the conversation
    - response_type: Type of response (initial, followup, negotiation, etc.)
    - customization: Optional customization parameters
    """
    return await service.generate_response(request)

@router.post("/quick-reply")
async def quick_reply(
    conversation_id: str,
    pattern_type: str,
    customization: Optional[dict] = None,
    service: MessageService = Depends()
):
    """Generate a quick template-based reply."""
    return await service.quick_reply(
        conversation_id,
        pattern_type,
        customization
    )
```

#### 3.3.3 Analysis Endpoints

```python
# app/api/routes/analysis.py
from fastapi import APIRouter, Depends
from app.services.analysis_service import AnalysisService

router = APIRouter()

@router.post("/context")
async def analyze_context(
    conversation_id: str,
    service: AnalysisService = Depends()
):
    """Analyze conversation context and patterns."""
    return await service.analyze_context(conversation_id)

@router.post("/fit-score")
async def calculate_fit_score(
    conversation_id: str,
    job_description: Optional[str] = None,
    service: AnalysisService = Depends()
):
    """Calculate job fit score."""
    return await service.calculate_fit_score(conversation_id, job_description)

@router.post("/follow-up-timing")
async def optimize_followup_timing(
    conversation_id: str,
    service: AnalysisService = Depends()
):
    """Get optimal follow-up timing recommendation."""
    return await service.optimize_followup_timing(conversation_id)

@router.get("/multi-conversation")
async def get_multi_conversation_analytics(
    service: AnalysisService = Depends()
):
    """Get analytics across all conversations."""
    return await service.get_multi_conversation_analytics()

@router.post("/quality-score")
async def score_response_quality(
    draft_response: str,
    conversation_id: str,
    service: AnalysisService = Depends()
):
    """Score the quality of a draft response."""
    return await service.score_response_quality(draft_response, conversation_id)
```

### 3.4 Service Layer Design

```python
# app/services/conversation_service.py
from typing import List, Optional
from app.data.conversation_repo import ConversationRepository
from app.agents.orchestrator import AgentOrchestrator
from app.models.conversation import Conversation
from app.api.schemas.conversation import ConversationCreate, ConversationUpdate

class ConversationService:
    """Business logic for conversation management."""

    def __init__(
        self,
        repo: ConversationRepository,
        orchestrator: AgentOrchestrator
    ):
        self.repo = repo
        self.orchestrator = orchestrator

    async def list_conversations(
        self,
        status: Optional[str] = None,
        platform: Optional[str] = None,
        company: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Conversation]:
        """List conversations with filtering."""
        return await self.repo.list(
            filters={
                "status": status,
                "platform": platform,
                "company": company
            },
            limit=limit,
            offset=offset
        )

    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a conversation by ID."""
        return await self.repo.get(conversation_id)

    async def create_conversation(
        self,
        data: ConversationCreate
    ) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(**data.dict())
        return await self.repo.save(conversation)

    async def update_conversation(
        self,
        conversation_id: str,
        update: ConversationUpdate
    ) -> Conversation:
        """Update an existing conversation."""
        conversation = await self.repo.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        # Update fields
        for field, value in update.dict(exclude_unset=True).items():
            setattr(conversation, field, value)

        return await self.repo.save(conversation)

    async def analyze_conversation(self, conversation_id: str):
        """
        Trigger comprehensive analysis for a conversation.
        Uses agent orchestrator to run multiple analysis agents.
        """
        conversation = await self.repo.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        # Orchestrate multiple analysis agents
        analysis_tasks = [
            ("context_analyzer", {"conversation": conversation}),
            ("timing_optimizer", {"conversation": conversation}),
        ]

        # If job description exists, run fit analysis
        if conversation.job_description:
            analysis_tasks.append(
                ("job_analyzer", {
                    "conversation": conversation,
                    "job_description": conversation.job_description
                })
            )

        results = await self.orchestrator.run_parallel(analysis_tasks)

        # Update conversation with analysis results
        conversation.analysis = results
        await self.repo.save(conversation)

        return results

    async def archive_conversation(self, conversation_id: str):
        """Archive a conversation."""
        conversation = await self.repo.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        conversation.archived = True
        conversation.archived_at = datetime.utcnow()
        await self.repo.save(conversation)
```

---

## 4. Agent System Design

### 4.1 Agent Architecture Overview

```
┌───────────────────────────────────────────────────────────────┐
│                    Agent Orchestrator                          │
│  - Agent Pool Management                                       │
│  - Request Routing                                             │
│  - Parallel Execution                                          │
│  - Result Aggregation                                          │
└────────────────┬──────────────────────────────────────────────┘
                 │
    ┌────────────┴────────────┬──────────────┬─────────────┐
    │                         │              │             │
┌───▼────────┐  ┌────────────▼───┐  ┌──────▼──────┐  ┌──▼─────────┐
│   Model    │  │   Streaming    │  │   Cache     │  │   Tool     │
│   Router   │  │   Handler      │  │   Manager   │  │ Integration│
└───┬────────┘  └────────────┬───┘  └──────┬──────┘  └──┬─────────┘
    │                        │              │             │
┌───┴────────────────────────┴──────────────┴─────────────┴────────┐
│                        Base Agent Class                           │
│  - Common Interface                                               │
│  - Error Handling                                                 │
│  - Logging                                                        │
│  - Metrics                                                        │
└────────────────────────────┬──────────────────────────────────────┘
                             │
    ┌────────────────────────┼────────────────────────┐
    │                        │                        │
┌───▼─────────────┐  ┌──────▼──────────┐  ┌─────────▼──────────┐
│  Analysis       │  │  Generation     │  │  Specialized       │
│  Agents         │  │  Agents         │  │  Agents            │
│                 │  │                 │  │                    │
│ - Context       │  │ - Response      │  │ - Company          │
│   Analyzer      │  │   Generator     │  │   Researcher       │
│ - Job Analyzer  │  │ - Follow-up     │  │ - Gap Researcher   │
│ - Timing        │  │   Generator     │  │ - Multi-Conv       │
│   Optimizer     │  │ - Negotiation   │  │   Analytics        │
│ - Quality       │  │   Generator     │  │                    │
│   Scorer        │  │                 │  │                    │
└─────────────────┘  └─────────────────┘  └────────────────────┘
```

### 4.2 Base Agent Class

```python
# app/agents/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, AsyncIterator
from pydantic import BaseModel
import logging
from datetime import datetime

from app.agents.model_router import ModelRouter
from app.core.exceptions import AgentException

class AgentConfig(BaseModel):
    """Configuration for an agent."""
    name: str
    model: str  # haiku, sonnet, opus
    temperature: float = 1.0
    max_tokens: int = 4096
    system_prompt: Optional[str] = None
    streaming: bool = False
    cache_enabled: bool = True
    timeout: int = 120  # seconds

class AgentResult(BaseModel):
    """Standard agent result format."""
    agent_name: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}
    timestamp: datetime = datetime.utcnow()
    tokens_used: Optional[int] = None
    duration_ms: Optional[int] = None

class BaseAgent(ABC):
    """
    Base class for all agents.

    Provides common functionality:
    - Model routing
    - Error handling
    - Logging
    - Streaming support
    - Metrics collection
    """

    def __init__(
        self,
        config: AgentConfig,
        model_router: ModelRouter,
        logger: Optional[logging.Logger] = None
    ):
        self.config = config
        self.model_router = model_router
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Process input and return result.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def build_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        Build the prompt for the LLM.
        Must be implemented by subclasses.
        """
        pass

    async def execute(self, input_data: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent with error handling and metrics.
        """
        start_time = datetime.utcnow()

        try:
            self.logger.info(f"Agent {self.config.name} starting execution")

            # Validate input
            self.validate_input(input_data)

            # Process
            result = await self.process(input_data)

            # Calculate duration
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            result.duration_ms = duration

            self.logger.info(
                f"Agent {self.config.name} completed successfully "
                f"in {duration}ms"
            )

            return result

        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds() * 1000
            self.logger.error(
                f"Agent {self.config.name} failed: {str(e)}",
                exc_info=True
            )

            return AgentResult(
                agent_name=self.config.name,
                success=False,
                error=str(e),
                metadata={"duration_ms": duration}
            )

    async def call_llm(
        self,
        prompt: str,
        system: Optional[str] = None
    ) -> str:
        """Call LLM via model router."""
        return await self.model_router.complete(
            model=self.config.model,
            prompt=prompt,
            system=system or self.config.system_prompt,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )

    async def stream_llm(
        self,
        prompt: str,
        system: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream LLM response via model router."""
        async for chunk in self.model_router.stream(
            model=self.config.model,
            prompt=prompt,
            system=system or self.config.system_prompt,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        ):
            yield chunk

    def validate_input(self, input_data: Dict[str, Any]):
        """
        Validate input data.
        Override in subclasses for custom validation.
        """
        pass
```

### 4.3 Agent Orchestrator

```python
# app/agents/orchestrator.py
from typing import List, Dict, Any, Tuple
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.agents.base_agent import BaseAgent, AgentResult
from app.agents.model_router import ModelRouter
from app.agents.registry import AgentRegistry

class AgentOrchestrator:
    """
    Orchestrates multiple agents.

    Features:
    - Parallel agent execution
    - Sequential workflows
    - Result aggregation
    - Error handling
    - Resource management
    """

    def __init__(
        self,
        registry: AgentRegistry,
        model_router: ModelRouter,
        max_parallel: int = 5
    ):
        self.registry = registry
        self.model_router = model_router
        self.max_parallel = max_parallel
        self.executor = ThreadPoolExecutor(max_workers=max_parallel)

    async def run_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any]
    ) -> AgentResult:
        """Run a single agent."""
        agent = self.registry.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found in registry")

        return await agent.execute(input_data)

    async def run_parallel(
        self,
        tasks: List[Tuple[str, Dict[str, Any]]]
    ) -> Dict[str, AgentResult]:
        """
        Run multiple agents in parallel.

        Args:
            tasks: List of (agent_name, input_data) tuples

        Returns:
            Dict mapping agent_name to AgentResult
        """
        # Create tasks
        agent_tasks = [
            self.run_agent(agent_name, input_data)
            for agent_name, input_data in tasks
        ]

        # Execute in parallel with limit
        results = []
        for i in range(0, len(agent_tasks), self.max_parallel):
            batch = agent_tasks[i:i + self.max_parallel]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            results.extend(batch_results)

        # Build result dict
        result_dict = {}
        for (agent_name, _), result in zip(tasks, results):
            if isinstance(result, Exception):
                result_dict[agent_name] = AgentResult(
                    agent_name=agent_name,
                    success=False,
                    error=str(result)
                )
            else:
                result_dict[agent_name] = result

        return result_dict

    async def run_sequential(
        self,
        workflow: List[Tuple[str, Dict[str, Any]]],
        pass_results: bool = False
    ) -> List[AgentResult]:
        """
        Run agents sequentially.

        Args:
            workflow: List of (agent_name, input_data) tuples
            pass_results: If True, pass previous result to next agent

        Returns:
            List of AgentResults in execution order
        """
        results = []
        previous_result = None

        for agent_name, input_data in workflow:
            # Optionally merge previous result
            if pass_results and previous_result:
                input_data = {**input_data, "previous_result": previous_result}

            # Execute agent
            result = await self.run_agent(agent_name, input_data)
            results.append(result)
            previous_result = result

            # Stop on failure if configured
            if not result.success:
                break

        return results

    async def run_conditional(
        self,
        condition_agent: str,
        condition_input: Dict[str, Any],
        true_agent: str,
        false_agent: str,
        agent_input: Dict[str, Any]
    ) -> AgentResult:
        """
        Run an agent conditionally based on another agent's result.
        """
        # Run condition agent
        condition_result = await self.run_agent(condition_agent, condition_input)

        if not condition_result.success:
            return condition_result

        # Determine which agent to run
        condition_value = condition_result.data.get("condition", False)
        next_agent = true_agent if condition_value else false_agent

        # Run selected agent
        return await self.run_agent(next_agent, agent_input)
```

### 4.4 Model Router

```python
# app/agents/model_router.py
from typing import AsyncIterator, Optional
from anthropic import AsyncAnthropic
from enum import Enum

class ModelTier(Enum):
    """Model tiers for routing."""
    HAIKU = "claude-3-5-haiku-20241022"
    SONNET = "claude-3-5-sonnet-20241022"
    OPUS = "claude-opus-4-5-20251101"

class ModelRouter:
    """
    Routes requests to appropriate Claude models.

    Features:
    - Model selection logic
    - Streaming support
    - Token tracking
    - Error handling
    """

    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.token_usage = {}  # Track usage per model

    def get_model_id(self, model: str) -> str:
        """Map friendly name to model ID."""
        model_map = {
            "haiku": ModelTier.HAIKU.value,
            "sonnet": ModelTier.SONNET.value,
            "opus": ModelTier.OPUS.value
        }
        return model_map.get(model.lower(), ModelTier.SONNET.value)

    async def complete(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 4096
    ) -> str:
        """
        Get completion from Claude.

        Args:
            model: Model tier (haiku, sonnet, opus)
            prompt: User prompt
            system: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        model_id = self.get_model_id(model)

        messages = [{"role": "user", "content": prompt}]

        response = await self.client.messages.create(
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system if system else None,
            messages=messages
        )

        # Track usage
        self._track_usage(model_id, response.usage)

        return response.content[0].text

    async def stream(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 4096
    ) -> AsyncIterator[str]:
        """
        Stream completion from Claude.

        Yields text chunks as they arrive.
        """
        model_id = self.get_model_id(model)

        messages = [{"role": "user", "content": prompt}]

        async with self.client.messages.stream(
            model=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system if system else None,
            messages=messages
        ) as stream:
            async for text in stream.text_stream:
                yield text

            # Track usage after stream completes
            final_message = await stream.get_final_message()
            self._track_usage(model_id, final_message.usage)

    def _track_usage(self, model_id: str, usage):
        """Track token usage per model."""
        if model_id not in self.token_usage:
            self.token_usage[model_id] = {
                "input_tokens": 0,
                "output_tokens": 0
            }

        self.token_usage[model_id]["input_tokens"] += usage.input_tokens
        self.token_usage[model_id]["output_tokens"] += usage.output_tokens

    def get_usage_stats(self) -> dict:
        """Get usage statistics."""
        return self.token_usage.copy()
```

### 4.5 Example Agent: Context Analyzer

```python
# app/agents/analysis/context_analyzer.py
from typing import Dict, Any
from pydantic import BaseModel

from app.agents.base_agent import BaseAgent, AgentResult, AgentConfig
from app.models.conversation import Conversation

class ContextAnalysis(BaseModel):
    """Result of context analysis."""
    summary: str
    sentiment_trend: Dict[str, str]
    conversation_stage: Dict[str, str]
    action_items: Dict[str, list]
    patterns_detected: list
    recommendations: list

class ContextAnalyzerAgent(BaseAgent):
    """
    Analyzes conversation context to extract insights.

    Model: Sonnet (balanced performance)
    """

    def __init__(self, model_router, logger=None):
        config = AgentConfig(
            name="context_analyzer",
            model="sonnet",
            temperature=0.7,
            max_tokens=2048,
            system_prompt=self._get_system_prompt()
        )
        super().__init__(config, model_router, logger)

    def validate_input(self, input_data: Dict[str, Any]):
        """Validate that conversation is provided."""
        if "conversation" not in input_data:
            raise ValueError("conversation is required in input_data")

    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Process conversation and analyze context."""
        conversation: Conversation = input_data["conversation"]

        # Build prompt
        prompt = self.build_prompt(input_data)

        # Call LLM
        response = await self.call_llm(prompt)

        # Parse response (assumes JSON output from LLM)
        try:
            import json
            analysis_data = json.loads(response)
            analysis = ContextAnalysis(**analysis_data)

            return AgentResult(
                agent_name=self.config.name,
                success=True,
                data=analysis.dict()
            )
        except Exception as e:
            return AgentResult(
                agent_name=self.config.name,
                success=False,
                error=f"Failed to parse LLM response: {str(e)}"
            )

    def build_prompt(self, input_data: Dict[str, Any]) -> str:
        """Build analysis prompt."""
        conversation: Conversation = input_data["conversation"]

        # Format conversation history
        history_text = self._format_history(conversation)

        prompt = f"""Analyze this recruiter conversation and provide insights.

# Conversation History

{history_text}

# Analysis Required

Provide a JSON response with the following structure:

```json
{{
  "summary": "2-3 sentence overview of the conversation",
  "sentiment_trend": {{
    "initial": "positive|neutral|negative",
    "current": "positive|neutral|negative",
    "direction": "improving|stable|declining",
    "indicators": ["list of evidence"]
  }},
  "conversation_stage": {{
    "current": "initial_outreach|screening|interviewing|negotiation|...",
    "progression_quality": "smooth|stalled|fast_tracked"
  }},
  "action_items": {{
    "candidate_pending": ["actions candidate needs to take"],
    "recruiter_pending": ["actions recruiter needs to take"]
  }},
  "patterns_detected": ["list of detected patterns"],
  "recommendations": ["list of recommendations for next steps"]
}}
```

Provide ONLY the JSON response, no other text."""

        return prompt

    def _format_history(self, conversation: Conversation) -> str:
        """Format conversation history for prompt."""
        lines = []
        for msg in conversation.messages:
            timestamp = msg.timestamp.strftime("%Y-%m-%d %H:%M")
            lines.append(f"[{timestamp}] {msg.from_name}:")
            lines.append(msg.body)
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _get_system_prompt() -> str:
        """Get system prompt for context analyzer."""
        return """You are an expert at analyzing professional recruitment conversations.

Your role is to:
1. Identify sentiment trends and engagement levels
2. Detect patterns in communication (responsiveness, interest, red flags)
3. Extract action items and commitments
4. Assess conversation stage and progression quality
5. Provide strategic recommendations

Be thorough, insightful, and strategic in your analysis."""
```

### 4.6 Streaming Implementation

```python
# app/agents/streaming.py
from typing import AsyncIterator
from fastapi import WebSocket
import json

class StreamHandler:
    """
    Handle streaming responses from agents.

    Supports:
    - WebSocket streaming to clients
    - Server-Sent Events (SSE)
    - Chunked HTTP responses
    """

    @staticmethod
    async def stream_to_websocket(
        websocket: WebSocket,
        agent_stream: AsyncIterator[str],
        event_type: str = "agent_response"
    ):
        """
        Stream agent response to WebSocket client.

        Args:
            websocket: FastAPI WebSocket connection
            agent_stream: Async iterator of text chunks
            event_type: Event type for client
        """
        try:
            async for chunk in agent_stream:
                await websocket.send_json({
                    "type": event_type,
                    "chunk": chunk
                })

            # Send completion event
            await websocket.send_json({
                "type": f"{event_type}_complete"
            })

        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "error": str(e)
            })

    @staticmethod
    async def stream_to_sse(
        agent_stream: AsyncIterator[str]
    ) -> AsyncIterator[str]:
        """
        Convert agent stream to Server-Sent Events format.

        Yields SSE formatted strings.
        """
        try:
            async for chunk in agent_stream:
                # SSE format: data: <content>\n\n
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            # Send completion
            yield f"data: {json.dumps({'complete': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
```

---

## 5. Data Architecture

### 5.1 Data Storage Structure

```
data/
├── conversations/                   # Conversation files
│   ├── company-a-recruiter1.yaml   # Full-time position
│   ├── agency-x-recruiter2-company-b.yaml  # Contract position
│   └── ...
│
├── settings/                        # User settings (encrypted)
│   ├── personal-info.yaml          # Personal data
│   ├── resume.md                   # Resume
│   ├── preferences.yaml            # Job search preferences
│   └── compensation.yaml           # Compensation expectations
│
├── analysis_cache/                  # Cached analysis results
│   ├── context/
│   ├── fit_scores/
│   └── timing/
│
└── metadata/                        # System metadata
    ├── conversation_index.json     # Index for fast lookups
    └── stats.json                  # System statistics
```

### 5.2 Conversation Data Model

```python
# app/models/conversation.py
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class Platform(str, Enum):
    """Communication platforms."""
    LINKEDIN = "linkedin"
    EMAIL = "email"
    PHONE = "phone"
    IN_PERSON = "in_person"

class ProcessStatus(str, Enum):
    """Process status values."""
    NEW = "new"
    REVIEWING = "reviewing"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    APPLIED = "applied"
    AWAITING_RESPONSE = "awaiting_response"
    INTERVIEWING = "interviewing"
    OFFER = "offer"
    NEGOTIATING = "negotiating"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    GHOSTED = "ghosted"

class Message(BaseModel):
    """Individual message in conversation."""
    timestamp: datetime
    from_name: str
    to_name: Optional[str] = None
    subject: Optional[str] = None
    body: str
    attachments: List[str] = []

class SentimentTrend(BaseModel):
    """Sentiment analysis for conversation."""
    initial: str
    current: str
    direction: str
    indicators: List[str]

class ConversationStage(BaseModel):
    """Current stage of conversation."""
    current: str
    progression_quality: str

class ActionItems(BaseModel):
    """Pending action items."""
    candidate_pending: List[str] = []
    recruiter_pending: List[str] = []

class ContextAnalysis(BaseModel):
    """Analysis of conversation context."""
    summary: str
    sentiment_trend: SentimentTrend
    conversation_stage: ConversationStage
    action_items: ActionItems
    patterns_detected: List[str] = []
    recommendations: List[str] = []
    last_analyzed: datetime

class FitScore(BaseModel):
    """Job fit scoring."""
    overall_score: float  # 0-100
    required_skills_score: float
    preferred_skills_score: float
    experience_match: float
    strengths: List[str]
    gaps: List[Dict[str, Any]]
    breakdown: Dict[str, float]

class ResponseMetrics(BaseModel):
    """Response time metrics."""
    recruiter_avg_hours: Optional[float] = None
    candidate_avg_hours: Optional[float] = None
    recruiter_message_count: int = 0
    candidate_message_count: int = 0

class Conversation(BaseModel):
    """
    Complete conversation model.

    This is the primary data structure for tracking
    all recruiter communications.
    """
    # Metadata
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Basic info
    platform: Platform
    company: Optional[str] = None
    recruiting_company: Optional[str] = None  # For contract positions
    recruiter_name: str
    process_status: ProcessStatus = ProcessStatus.NEW

    # Context
    context: List[str] = []  # Additional context notes

    # Messages
    messages: List[Message] = []

    # Analysis (optional, populated by agents)
    context_analysis: Optional[ContextAnalysis] = None
    fit_score: Optional[FitScore] = None
    response_metrics: Optional[ResponseMetrics] = None

    # Linked data
    job_description: Optional[str] = None
    job_description_filepath: Optional[str] = None
    resume_filepath: Optional[str] = None

    # Archival
    archived: bool = False
    archived_at: Optional[datetime] = None
    archive_reason: Optional[str] = None

    # Related conversations
    related_conversation_ids: List[str] = []

    class Config:
        use_enum_values = True
```

### 5.3 YAML Schema for Conversation Files

```yaml
# Example: data/conversations/company-a-recruiter1.yaml

id: "550e8400-e29b-41d4-a716-446655440000"
created_at: 2025-12-09T10:00:00-07:00
updated_at: 2025-12-09T15:30:00-07:00

platform: linkedin
company: Company A
recruiter_name: John Recruiter
process_status: interested

context:
  - "$150,000 yearly is in the lower range of my acceptable range"
  - "Do not forget to mention that I require H1B Visa Sponsorship"

messages:
  - timestamp: 2025-12-09T10:00:00-07:00
    from_name: John Recruiter
    subject: "Senior Engineer Position at Company A"
    body: |
      Hi! I came across your profile and think you'd be a great fit
      for our Senior Software Engineer position...
    attachments: []

  - timestamp: 2025-12-09T15:30:00-07:00
    from_name: User
    to_name: John Recruiter
    body: |
      Thank you for reaching out! I'm definitely interested in learning
      more about the position...

context_analysis:
  summary: "Initial recruiter outreach for senior engineering role..."
  sentiment_trend:
    initial: positive
    current: positive
    direction: stable
    indicators:
      - "Enthusiastic initial message"
      - "Personalized outreach"
  conversation_stage:
    current: initial_outreach
    progression_quality: smooth
  action_items:
    candidate_pending:
      - "Wait for recruiter's response with more details"
    recruiter_pending:
      - "Provide job description and compensation range"
  patterns_detected:
    - "Recruiter mentioned specific skills from profile"
  recommendations:
    - "Ask about H1B sponsorship in next message"
  last_analyzed: 2025-12-09T15:35:00-07:00

fit_score:
  overall_score: 85.0
  required_skills_score: 90.0
  preferred_skills_score: 75.0
  experience_match: 85.0
  strengths:
    - "Strong match on Python and distributed systems"
    - "Relevant leadership experience"
  gaps:
    - skill: "Kubernetes"
      severity: "medium"
      mitigation: "Can learn quickly, have Docker experience"
  breakdown:
    technical_skills: 88.0
    experience_level: 92.0
    domain_knowledge: 75.0

response_metrics:
  recruiter_avg_hours: null
  candidate_avg_hours: 5.5
  recruiter_message_count: 1
  candidate_message_count: 1

job_description_filepath: data/conversations/company-a-recruiter1-jd.txt
resume_filepath: data/settings/resume.md

archived: false
related_conversation_ids: []
```

### 5.4 Data Access Layer

```python
# app/data/repository_base.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Type, TypeVar
from pathlib import Path

T = TypeVar('T')

class RepositoryBase(ABC):
    """
    Base repository for data access.

    Provides common CRUD operations for file-based storage.
    """

    def __init__(self, data_dir: Path, model_class: Type[T]):
        self.data_dir = data_dir
        self.model_class = model_class

        # Ensure directory exists
        self.data_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[T]:
        """List entities with optional filtering."""
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save (create or update) entity."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        pass

# app/data/conversation_repo.py
from pathlib import Path
from typing import List, Optional, Dict, Any
import yaml
from datetime import datetime

from app.data.repository_base import RepositoryBase
from app.models.conversation import Conversation

class ConversationRepository(RepositoryBase):
    """
    Repository for conversation data.

    Handles YAML file operations for conversations.
    """

    def __init__(self, data_dir: Path):
        super().__init__(data_dir / "conversations", Conversation)
        self.index_file = data_dir / "metadata" / "conversation_index.json"

    async def get(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID."""
        # Load index to find file
        index = await self._load_index()

        file_path = index.get(conversation_id)
        if not file_path:
            return None

        # Load YAML file
        full_path = self.data_dir / file_path
        if not full_path.exists():
            return None

        with open(full_path, 'r') as f:
            data = yaml.safe_load(f)

        return Conversation(**data)

    async def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Conversation]:
        """List conversations with filtering."""
        conversations = []

        # Get all conversation files
        for file_path in self.data_dir.glob("*.yaml"):
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)

            conversation = Conversation(**data)

            # Apply filters
            if filters:
                if not self._matches_filters(conversation, filters):
                    continue

            conversations.append(conversation)

        # Sort by updated_at (most recent first)
        conversations.sort(key=lambda c: c.updated_at, reverse=True)

        # Apply pagination
        return conversations[offset:offset + limit]

    async def save(self, conversation: Conversation) -> Conversation:
        """Save conversation to YAML file."""
        # Update timestamp
        conversation.updated_at = datetime.utcnow()

        # Generate filename
        filename = self._generate_filename(conversation)
        file_path = self.data_dir / filename

        # Save to YAML
        with open(file_path, 'w') as f:
            yaml.dump(
                conversation.dict(),
                f,
                default_flow_style=False,
                sort_keys=False
            )

        # Update index
        await self._update_index(conversation.id, filename)

        return conversation

    async def delete(self, conversation_id: str) -> bool:
        """Delete conversation file."""
        index = await self._load_index()
        file_path = index.get(conversation_id)

        if not file_path:
            return False

        full_path = self.data_dir / file_path
        if full_path.exists():
            full_path.unlink()

        # Remove from index
        await self._remove_from_index(conversation_id)

        return True

    def _generate_filename(self, conversation: Conversation) -> str:
        """Generate filename for conversation."""
        if conversation.recruiting_company:
            # Contract position
            parts = [
                conversation.recruiting_company,
                conversation.recruiter_name.split()[0],  # First name
                conversation.company or "unknown"
            ]
        else:
            # Full-time position
            parts = [
                conversation.company or "unknown",
                conversation.recruiter_name.split()[0]
            ]

        # Sanitize and join
        sanitized = [p.lower().replace(" ", "-") for p in parts]
        return f"{'- '.join(sanitized)}.yaml"

    def _matches_filters(
        self,
        conversation: Conversation,
        filters: Dict[str, Any]
    ) -> bool:
        """Check if conversation matches filters."""
        for key, value in filters.items():
            if value is None:
                continue

            conv_value = getattr(conversation, key, None)
            if conv_value != value:
                return False

        return True

    async def _load_index(self) -> Dict[str, str]:
        """Load conversation index."""
        if not self.index_file.exists():
            return {}

        import json
        with open(self.index_file, 'r') as f:
            return json.load(f)

    async def _update_index(self, conversation_id: str, filename: str):
        """Update conversation index."""
        index = await self._load_index()
        index[conversation_id] = filename

        import json
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_file, 'w') as f:
            json.dump(index, f, indent=2)

    async def _remove_from_index(self, conversation_id: str):
        """Remove conversation from index."""
        index = await self._load_index()
        if conversation_id in index:
            del index[conversation_id]

            import json
            with open(self.index_file, 'w') as f:
                json.dump(index, f, indent=2)
```

### 5.5 Thread Management

The system supports multiple threads within a single conversation (e.g., LinkedIn message + email follow-up). This is handled through the `messages` array in the Conversation model, with each message having platform-specific metadata.

```python
# Example: Multi-platform conversation
conversation = Conversation(
    platform=Platform.LINKEDIN,  # Primary platform
    messages=[
        Message(
            timestamp=datetime(...),
            from_name="Recruiter",
            body="Initial LinkedIn message",
            platform_metadata={"platform": "linkedin"}
        ),
        Message(
            timestamp=datetime(...),
            from_name="Recruiter",
            subject="Follow-up via email",
            body="Email follow-up",
            platform_metadata={"platform": "email", "thread_id": "..."}
        )
    ]
)
```

---

## 6. Real-time Communication

### 6.1 WebSocket Architecture

```python
# app/api/routes/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
import asyncio

from app.agents.orchestrator import AgentOrchestrator
from app.agents.streaming import StreamHandler

router = APIRouter()

# Active WebSocket connections
active_connections: Dict[str, WebSocket] = {}

@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates.

    Protocol:
    - Client sends: {"type": "subscribe", "topics": ["conversations", "analysis"]}
    - Server sends: {"type": "event", "topic": "...", "data": {...}}
    """
    await websocket.accept()

    # Generate connection ID
    import uuid
    connection_id = str(uuid.uuid4())
    active_connections[connection_id] = websocket

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "connection_id": connection_id
        })

        # Message handling loop
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)

            # Route message
            await handle_websocket_message(
                connection_id,
                websocket,
                message
            )

    except WebSocketDisconnect:
        # Clean up on disconnect
        if connection_id in active_connections:
            del active_connections[connection_id]

async def handle_websocket_message(
    connection_id: str,
    websocket: WebSocket,
    message: dict
):
    """Handle incoming WebSocket message."""
    message_type = message.get("type")

    if message_type == "subscribe":
        # Handle subscription
        topics = message.get("topics", [])
        await websocket.send_json({
            "type": "subscribed",
            "topics": topics
        })

    elif message_type == "generate_response":
        # Generate response with streaming
        conversation_id = message.get("conversation_id")

        # Get orchestrator
        from app.dependencies import get_orchestrator
        orchestrator = get_orchestrator()

        # Stream response generation
        await stream_response_generation(
            websocket,
            orchestrator,
            conversation_id
        )

    elif message_type == "ping":
        # Heartbeat
        await websocket.send_json({"type": "pong"})

async def stream_response_generation(
    websocket: WebSocket,
    orchestrator: AgentOrchestrator,
    conversation_id: str
):
    """
    Stream response generation to WebSocket.

    Sends real-time updates as the agent generates the response.
    """
    try:
        # Send start event
        await websocket.send_json({
            "type": "generation_started",
            "conversation_id": conversation_id
        })

        # Get response generator agent
        agent = orchestrator.registry.get_agent("response_generator")

        # Stream generation
        async for chunk in agent.stream_generate({"conversation_id": conversation_id}):
            await websocket.send_json({
                "type": "generation_chunk",
                "chunk": chunk
            })

        # Send completion event
        await websocket.send_json({
            "type": "generation_complete",
            "conversation_id": conversation_id
        })

    except Exception as e:
        await websocket.send_json({
            "type": "generation_error",
            "error": str(e)
        })

# Broadcast to all connected clients
async def broadcast_event(topic: str, data: dict):
    """
    Broadcast event to all connected WebSocket clients.

    Used for system-wide events like:
    - New conversation created
    - Conversation status changed
    - Analysis completed
    """
    message = {
        "type": "event",
        "topic": topic,
        "data": data
    }

    # Send to all connections
    disconnected = []
    for connection_id, websocket in active_connections.items():
        try:
            await websocket.send_json(message)
        except:
            disconnected.append(connection_id)

    # Clean up disconnected clients
    for connection_id in disconnected:
        del active_connections[connection_id]
```

### 6.2 Event Types and Payloads

```typescript
// WebSocket Event Types

// Client -> Server
type ClientMessage =
  | { type: "subscribe", topics: string[] }
  | { type: "unsubscribe", topics: string[] }
  | { type: "generate_response", conversation_id: string, response_type: string }
  | { type: "analyze_conversation", conversation_id: string }
  | { type: "ping" }

// Server -> Client
type ServerMessage =
  | { type: "connected", connection_id: string }
  | { type: "subscribed", topics: string[] }
  | { type: "pong" }
  | { type: "event", topic: string, data: any }
  | { type: "generation_started", conversation_id: string }
  | { type: "generation_chunk", chunk: string }
  | { type: "generation_complete", conversation_id: string }
  | { type: "generation_error", error: string }
  | { type: "analysis_started", conversation_id: string, agent: string }
  | { type: "analysis_complete", conversation_id: string, agent: string, result: any }
  | { type: "error", error: string }

// Event Topics
type EventTopic =
  | "conversations"        // Conversation CRUD events
  | "messages"            // New messages
  | "analysis"            // Analysis completion
  | "status_changes"      // Status updates
  | "follow_ups"          // Follow-up reminders
```

### 6.3 Client Connection Management

```python
# app/core/websocket_manager.py
from typing import Dict, Set, Optional
from fastapi import WebSocket
import asyncio

class WebSocketManager:
    """
    Manage WebSocket connections and subscriptions.

    Features:
    - Connection lifecycle management
    - Topic-based subscriptions
    - Broadcast to specific topics
    - Heartbeat/keepalive
    """

    def __init__(self):
        # connection_id -> WebSocket
        self.connections: Dict[str, WebSocket] = {}

        # connection_id -> set of subscribed topics
        self.subscriptions: Dict[str, Set[str]] = {}

        # topic -> set of connection_ids
        self.topic_subscribers: Dict[str, Set[str]] = {}

    async def connect(self, connection_id: str, websocket: WebSocket):
        """Register new connection."""
        await websocket.accept()
        self.connections[connection_id] = websocket
        self.subscriptions[connection_id] = set()

    def disconnect(self, connection_id: str):
        """Remove connection and clean up subscriptions."""
        if connection_id in self.connections:
            # Remove from all topic subscriptions
            for topic in self.subscriptions.get(connection_id, set()):
                if topic in self.topic_subscribers:
                    self.topic_subscribers[topic].discard(connection_id)

            # Remove connection
            del self.connections[connection_id]
            del self.subscriptions[connection_id]

    async def subscribe(self, connection_id: str, topics: list[str]):
        """Subscribe connection to topics."""
        for topic in topics:
            # Add to connection's subscriptions
            self.subscriptions[connection_id].add(topic)

            # Add to topic's subscribers
            if topic not in self.topic_subscribers:
                self.topic_subscribers[topic] = set()
            self.topic_subscribers[topic].add(connection_id)

    async def unsubscribe(self, connection_id: str, topics: list[str]):
        """Unsubscribe connection from topics."""
        for topic in topics:
            self.subscriptions[connection_id].discard(topic)
            if topic in self.topic_subscribers:
                self.topic_subscribers[topic].discard(connection_id)

    async def send_to_connection(
        self,
        connection_id: str,
        message: dict
    ):
        """Send message to specific connection."""
        if connection_id in self.connections:
            websocket = self.connections[connection_id]
            try:
                await websocket.send_json(message)
            except:
                # Connection failed, remove it
                self.disconnect(connection_id)

    async def broadcast_to_topic(
        self,
        topic: str,
        message: dict
    ):
        """Broadcast message to all subscribers of a topic."""
        if topic not in self.topic_subscribers:
            return

        # Get subscriber IDs
        subscriber_ids = list(self.topic_subscribers[topic])

        # Send to all (with error handling)
        for connection_id in subscriber_ids:
            await self.send_to_connection(connection_id, message)

    async def broadcast_to_all(self, message: dict):
        """Broadcast message to all connected clients."""
        connection_ids = list(self.connections.keys())
        for connection_id in connection_ids:
            await self.send_to_connection(connection_id, message)
```

---

## 7. Security Design

### 7.1 API Key Management

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings."""

    # API Keys
    ANTHROPIC_API_KEY: str

    # Security
    SECRET_KEY: str = os.urandom(32).hex()
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Data paths
    DATA_DIR: str = "./data"
    ENCRYPTED_DATA_DIR: str = "./data/settings"

    # Git-crypt
    GIT_CRYPT_KEY_PATH: str = "./git-crypt-key"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
```

```bash
# .env.example
ANTHROPIC_API_KEY=sk-ant-...
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
DATA_DIR=./data
LOG_LEVEL=INFO
```

### 7.2 Data Encryption (git-crypt)

```python
# app/data/encryption.py
import subprocess
from pathlib import Path
from typing import Optional

class GitCryptHandler:
    """
    Handle git-crypt encryption/decryption.

    Sensitive data files are encrypted using git-crypt,
    which provides transparent encryption in Git repositories.
    """

    def __init__(self, repo_path: Path, key_path: Optional[Path] = None):
        self.repo_path = repo_path
        self.key_path = key_path

    def is_initialized(self) -> bool:
        """Check if git-crypt is initialized."""
        try:
            result = subprocess.run(
                ["git-crypt", "status"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def unlock(self) -> bool:
        """
        Unlock git-crypt encrypted files.

        Uses symmetric key if provided, otherwise assumes
        GPG key is configured.
        """
        try:
            if self.key_path and self.key_path.exists():
                # Unlock with symmetric key
                subprocess.run(
                    ["git-crypt", "unlock", str(self.key_path)],
                    cwd=self.repo_path,
                    check=True
                )
            else:
                # Unlock with GPG
                subprocess.run(
                    ["git-crypt", "unlock"],
                    cwd=self.repo_path,
                    check=True
                )
            return True
        except subprocess.CalledProcessError:
            return False

    def lock(self) -> bool:
        """Lock git-crypt encrypted files."""
        try:
            subprocess.run(
                ["git-crypt", "lock"],
                cwd=self.repo_path,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
```

```.gitattributes
# .gitattributes for git-crypt

# Encrypt sensitive settings
data/settings/*.yaml filter=git-crypt diff=git-crypt
data/settings/*.json filter=git-crypt diff=git-crypt
data/settings/*.md filter=git-crypt diff=git-crypt

# Keep conversation files unencrypted
# (they don't contain sensitive personal data)
data/conversations/*.yaml !filter !diff
```

### 7.3 Input Validation

```python
# app/utils/validators.py
import re
from typing import Optional
from datetime import datetime

class Validators:
    """Input validation utilities."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        pattern = r'^https?://[^\s<>\"{}|\\^`\[\]]+$'
        return bool(re.match(pattern, url))

    @staticmethod
    def validate_conversation_id(conversation_id: str) -> bool:
        """Validate conversation ID format (UUID)."""
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(pattern, conversation_id.lower()))

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal.

        Removes: ../ ./ absolute paths, special characters
        """
        # Remove path components
        filename = filename.replace('..', '').replace('/', '').replace('\\', '')

        # Keep only alphanumeric, dash, underscore, dot
        filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)

        return filename

    @staticmethod
    def validate_iso_datetime(dt_string: str) -> Optional[datetime]:
        """
        Validate and parse ISO datetime string.

        Returns datetime object if valid, None otherwise.
        """
        try:
            return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
```

### 7.4 Security Best Practices

1. **API Key Protection**:
   - Never hardcode API keys
   - Load from environment variables
   - Validate on startup
   - Use separate keys for dev/prod

2. **Data Encryption**:
   - Use git-crypt for sensitive files
   - Personal info, resume, compensation data encrypted
   - Conversation history files unencrypted (no PII)

3. **Input Validation**:
   - Validate all user inputs
   - Sanitize filenames
   - Prevent path traversal
   - Validate data types

4. **Error Handling**:
   - Don't expose internal details in errors
   - Log security events
   - Rate limit API endpoints

---

## 8. Error Handling & Recovery

### 8.1 Error Types and Hierarchy

```python
# app/core/exceptions.py
from typing import Optional, Dict, Any

class AppException(Exception):
    """Base exception for application."""

    def __init__(
        self,
        message: str,
        error_type: str = "ApplicationError",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_type = error_type
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class ValidationError(AppException):
    """Input validation error."""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_type="ValidationError",
            status_code=400,
            details=details
        )

class NotFoundError(AppException):
    """Resource not found error."""
    def __init__(self, resource: str, id: str):
        super().__init__(
            message=f"{resource} with id '{id}' not found",
            error_type="NotFoundError",
            status_code=404,
            details={"resource": resource, "id": id}
        )

class AgentError(AppException):
    """Agent execution error."""
    def __init__(self, agent_name: str, message: str):
        super().__init__(
            message=f"Agent '{agent_name}' failed: {message}",
            error_type="AgentError",
            status_code=500,
            details={"agent": agent_name}
        )

class DataStorageError(AppException):
    """Data storage/retrieval error."""
    def __init__(self, operation: str, message: str):
        super().__init__(
            message=f"Data {operation} failed: {message}",
            error_type="DataStorageError",
            status_code=500,
            details={"operation": operation}
        )

class APIError(AppException):
    """External API error (e.g., Claude API)."""
    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"{service} API error: {message}",
            error_type="APIError",
            status_code=502,
            details={"service": service}
        )
```

### 8.2 Retry Strategies

```python
# app/utils/retry.py
import asyncio
from typing import Callable, Optional, Type, Tuple
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def async_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Retry decorator for async functions.

    Args:
        max_attempts: Maximum retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Multiplier for delay after each attempt
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)

                except exceptions as e:
                    if attempt == max_attempts:
                        # Last attempt, re-raise
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise

                    # Log and retry
                    logger.warning(
                        f"{func.__name__} attempt {attempt} failed: {e}. "
                        f"Retrying in {current_delay}s..."
                    )

                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator

# Usage example:
@async_retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(APIError,))
async def call_claude_api(prompt: str):
    """Call Claude API with retry logic."""
    # API call here
    pass
```

### 8.3 Graceful Degradation

```python
# app/agents/orchestrator.py (extended)

class AgentOrchestrator:
    """Extended with graceful degradation."""

    async def run_with_fallback(
        self,
        primary_agent: str,
        fallback_agent: str,
        input_data: Dict[str, Any]
    ) -> AgentResult:
        """
        Run primary agent with fallback to simpler agent on failure.

        Example: Try Opus for complex analysis, fallback to Sonnet if fails.
        """
        try:
            return await self.run_agent(primary_agent, input_data)
        except Exception as e:
            logger.warning(
                f"Primary agent {primary_agent} failed: {e}. "
                f"Falling back to {fallback_agent}"
            )
            return await self.run_agent(fallback_agent, input_data)

    async def run_with_timeout(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        timeout_seconds: int = 120
    ) -> AgentResult:
        """Run agent with timeout."""
        try:
            return await asyncio.wait_for(
                self.run_agent(agent_name, input_data),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            return AgentResult(
                agent_name=agent_name,
                success=False,
                error=f"Agent timed out after {timeout_seconds}s"
            )
```

### 8.4 Error Recovery Workflows

```
┌─────────────────────────────────────┐
│  Agent Execution Error              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Is it a retryable error?           │
│  (API rate limit, timeout, etc.)    │
└────────┬────────────┬───────────────┘
         │ Yes        │ No
         ▼            ▼
┌─────────────────┐  ┌──────────────────────┐
│  Retry with     │  │  Log error           │
│  backoff        │  │  Return error result │
└────────┬────────┘  │  Continue workflow   │
         │           └──────────────────────┘
         ▼
┌─────────────────────────────────────┐
│  Max retries exceeded?              │
└────────┬────────────┬───────────────┘
         │ Yes        │ No
         ▼            ▼
┌─────────────────┐  ┌──────────────────┐
│  Try fallback   │  │  Success         │
│  agent          │  │  Return result   │
└────────┬────────┘  └──────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Fallback succeeded?                │
└────────┬────────────┬───────────────┘
         │ Yes        │ No
         ▼            ▼
┌─────────────────┐  ┌──────────────────────┐
│  Return fallback│  │  Alert user          │
│  result         │  │  Provide manual path │
└─────────────────┘  └──────────────────────┘
```

---

## 9. Testing Strategy

### 9.1 Test Pyramid

```
        ┌─────────────────┐
        │   E2E Tests     │  ← 10% (Complete workflows)
        │   (Slow)        │
        ├─────────────────┤
        │ Integration     │  ← 30% (API, Agents, Data)
        │   Tests         │
        ├─────────────────┤
        │  Unit Tests     │  ← 60% (Individual functions)
        │  (Fast)         │
        └─────────────────┘
```

### 9.2 Unit Test Approach

```python
# tests/unit/test_conversation_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.conversation_service import ConversationService
from app.models.conversation import Conversation, ProcessStatus

@pytest.fixture
def mock_repo():
    """Mock conversation repository."""
    repo = AsyncMock()
    return repo

@pytest.fixture
def mock_orchestrator():
    """Mock agent orchestrator."""
    orchestrator = AsyncMock()
    return orchestrator

@pytest.fixture
def service(mock_repo, mock_orchestrator):
    """Create service with mocked dependencies."""
    return ConversationService(
        repo=mock_repo,
        orchestrator=mock_orchestrator
    )

@pytest.mark.asyncio
async def test_get_conversation_success(service, mock_repo):
    """Test getting a conversation successfully."""
    # Arrange
    conversation_id = "test-id-123"
    expected_conversation = Conversation(
        id=conversation_id,
        platform="linkedin",
        recruiter_name="Test Recruiter"
    )
    mock_repo.get.return_value = expected_conversation

    # Act
    result = await service.get_conversation(conversation_id)

    # Assert
    assert result == expected_conversation
    mock_repo.get.assert_called_once_with(conversation_id)

@pytest.mark.asyncio
async def test_get_conversation_not_found(service, mock_repo):
    """Test getting a non-existent conversation."""
    # Arrange
    mock_repo.get.return_value = None

    # Act
    result = await service.get_conversation("non-existent")

    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_analyze_conversation(service, mock_repo, mock_orchestrator):
    """Test conversation analysis orchestration."""
    # Arrange
    conversation_id = "test-id"
    conversation = Conversation(
        id=conversation_id,
        platform="linkedin",
        recruiter_name="Test"
    )
    mock_repo.get.return_value = conversation

    mock_analysis_results = {
        "context_analyzer": {"success": True, "data": {}},
        "timing_optimizer": {"success": True, "data": {}}
    }
    mock_orchestrator.run_parallel.return_value = mock_analysis_results

    # Act
    result = await service.analyze_conversation(conversation_id)

    # Assert
    assert result == mock_analysis_results
    mock_orchestrator.run_parallel.assert_called_once()
    mock_repo.save.assert_called_once()
```

### 9.3 Integration Tests

```python
# tests/integration/test_message_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

def test_parse_linkedin_message(client):
    """Test parsing a LinkedIn message via API."""
    # Arrange
    raw_message = """
    John Recruiter
    1st degree connection
    Senior Recruiter at Company A
    Monday
    John Recruiter sent the following messages at 10:00 AM

    Hi! I came across your profile...
    """

    # Act
    response = client.post(
        "/api/v1/messages/parse",
        json={
            "raw_message": raw_message,
            "platform": "linkedin"
        }
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["recruiter_name"] == "John Recruiter"
    assert data["company"] == "Company A"
    assert data["platform"] == "linkedin"

def test_generate_response(client):
    """Test response generation via API."""
    # Arrange
    # (Assumes a conversation exists)

    # Act
    response = client.post(
        "/api/v1/messages/generate-response",
        json={
            "conversation_id": "test-conversation-id",
            "response_type": "initial_interest"
        }
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "draft_response" in data
    assert "timing_recommendation" in data
```

### 9.4 Mock Strategies for Claude API

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_claude_client():
    """
    Mock Anthropic Claude client.

    Returns predefined responses for testing without API calls.
    """
    mock_client = AsyncMock()

    # Mock messages.create response
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Mock response text")]
    mock_response.usage = MagicMock(input_tokens=100, output_tokens=50)

    mock_client.messages.create.return_value = mock_response

    return mock_client

@pytest.fixture
def mock_model_router(mock_claude_client):
    """Mock model router with fake Claude client."""
    with patch('app.agents.model_router.AsyncAnthropic') as mock:
        mock.return_value = mock_claude_client
        from app.agents.model_router import ModelRouter
        router = ModelRouter(api_key="test-key")
        yield router

# Usage in tests
@pytest.mark.asyncio
async def test_agent_with_mock_claude(mock_model_router):
    """Test agent using mocked Claude API."""
    from app.agents.analysis.context_analyzer import ContextAnalyzerAgent

    agent = ContextAnalyzerAgent(model_router=mock_model_router)

    result = await agent.execute({
        "conversation": mock_conversation
    })

    assert result.success
```

### 9.5 E2E Test Example

```python
# tests/e2e/test_full_workflow.py
import pytest
from pathlib import Path
import yaml

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_full_conversation_workflow(client, test_data_dir):
    """
    Test complete workflow:
    1. Parse incoming message
    2. Create conversation
    3. Analyze context
    4. Generate response
    5. Verify response quality
    """
    # 1. Parse message
    raw_message = """..."""
    parse_response = client.post(
        "/api/v1/messages/parse",
        json={"raw_message": raw_message, "platform": "linkedin"}
    )
    assert parse_response.status_code == 200
    parsed_data = parse_response.json()

    # 2. Create conversation
    create_response = client.post(
        "/api/v1/conversations/",
        json={
            "platform": parsed_data["platform"],
            "recruiter_name": parsed_data["recruiter_name"],
            "company": parsed_data["company"]
        }
    )
    assert create_response.status_code == 200
    conversation_id = create_response.json()["id"]

    # 3. Analyze context
    analyze_response = client.post(
        f"/api/v1/conversations/{conversation_id}/analyze"
    )
    assert analyze_response.status_code == 200

    # 4. Generate response
    generate_response = client.post(
        "/api/v1/messages/generate-response",
        json={
            "conversation_id": conversation_id,
            "response_type": "initial_interest"
        }
    )
    assert generate_response.status_code == 200
    response_data = generate_response.json()

    # 5. Verify response quality
    assert "draft_response" in response_data
    assert len(response_data["draft_response"]) > 50
    assert "timing_recommendation" in response_data
```

---

## 10. Implementation Roadmap

### 10.1 Phase 1: Core Foundation (Weeks 1-2)

**Goal**: Establish basic infrastructure and core workflows

**Tasks**:
1. Set up FastAPI application structure
2. Implement data models (Conversation, Message, etc.)
3. Create file-based repository layer
4. Build base agent class and orchestrator
5. Implement model router
6. Create basic API endpoints (conversations, messages)
7. Set up git-crypt encryption
8. Write unit tests for core components

**Deliverables**:
- Working FastAPI backend
- CRUD operations for conversations
- Basic agent system
- File storage operational
- 70%+ test coverage

### 10.2 Phase 2: Analysis Agents (Weeks 3-4)

**Goal**: Implement intelligent analysis capabilities

**Tasks**:
1. Develop Context Analyzer agent
2. Develop Job Description Analyzer agent
3. Develop Follow-up Timing Optimizer agent
4. Develop Response Quality Scorer agent
5. Integrate agents with API endpoints
6. Create analysis caching system
7. Add WebSocket support for real-time updates
8. Write integration tests for agents

**Deliverables**:
- 4 working analysis agents
- Real-time analysis updates via WebSocket
- Analysis API endpoints
- Cached analysis results

### 10.3 Phase 3: Response Generation (Weeks 5-6)

**Goal**: Implement response generation system

**Tasks**:
1. Develop Response Generator agent
2. Develop Follow-up Generator agent
3. Create template system for quick replies
4. Implement streaming response generation
5. Build quality scoring into generation
6. Add response editing/refinement workflow
7. Create prompt templates
8. Write tests for generation system

**Deliverables**:
- Response generation agents
- Template-based quick replies
- Streaming support
- Quality-checked responses

### 10.4 Phase 4: Specialized Features (Weeks 7-8)

**Goal**: Add advanced capabilities

**Tasks**:
1. Develop Compensation Negotiation agent
2. Develop Multi-Conversation Analytics agent
3. Implement follow-up reminder system
4. Create opportunity comparison features
5. Build knowledge base and learning system
6. Add conversation archiving
7. Implement status inference
8. Write E2E tests

**Deliverables**:
- Negotiation support
- Analytics dashboard
- Automated follow-up system
- Learning from past conversations

### 10.5 Phase 5: Polish & Documentation (Week 9)

**Goal**: Finalize system and prepare for production

**Tasks**:
1. Performance optimization
2. Error handling improvements
3. Logging and monitoring setup
4. API documentation (OpenAPI/Swagger)
5. User documentation
6. Deployment guide
7. Security audit
8. Load testing

**Deliverables**:
- Production-ready system
- Complete documentation
- Deployment instructions
- Performance benchmarks

---

## 11. Appendices

### 11.1 API Reference

Complete API documentation available at `/api/docs` (Swagger UI) when running the backend.

**Base URL**: `http://localhost:8000/api/v1`

**Endpoints**:
- `GET /conversations` - List conversations
- `POST /conversations` - Create conversation
- `GET /conversations/{id}` - Get conversation
- `PATCH /conversations/{id}` - Update conversation
- `DELETE /conversations/{id}` - Archive conversation
- `POST /conversations/{id}/analyze` - Analyze conversation
- `POST /messages/parse` - Parse raw message
- `POST /messages/generate-response` - Generate response
- `POST /messages/quick-reply` - Quick template reply
- `POST /analysis/context` - Analyze context
- `POST /analysis/fit-score` - Calculate fit score
- `POST /analysis/follow-up-timing` - Optimize timing
- `WS /ws/connect` - WebSocket connection

### 11.2 Agent Catalog

| Agent Name | Model | Purpose | Input | Output |
|-----------|-------|---------|-------|--------|
| Context Analyzer | Sonnet | Conversation analysis | Conversation | ContextAnalysis |
| Job Analyzer | Sonnet | JD parsing & fit scoring | JD + Resume | FitScore |
| Timing Optimizer | Haiku | Follow-up timing | Conversation | TimingRecommendation |
| Quality Scorer | Haiku | Response quality check | Draft Response | QualityScore |
| Response Generator | Sonnet | Draft response | Conversation | Response |
| Followup Generator | Sonnet | Follow-up message | Conversation | Response |
| Negotiation Agent | Sonnet | Compensation strategy | Offer Details | NegotiationPlan |
| Multi-Analytics | Sonnet | Cross-conversation insights | All Conversations | Analytics |

### 11.3 Data Flow Diagrams

See Section 2.2 for primary data flow.

**Analysis Flow**:
```
Conversation
    ↓
Context Analyzer → ContextAnalysis
    ↓
Timing Optimizer → TimingRecommendation
    ↓
(if JD exists) Job Analyzer → FitScore
    ↓
Update Conversation with Analysis
    ↓
Broadcast Update (WebSocket)
```

**Response Generation Flow**:
```
User Request
    ↓
Load Conversation + Analysis
    ↓
Select Template/Style
    ↓
Response Generator (Streaming)
    ↓
Quality Scorer
    ↓
    ├─ Score > 80 → Present to User
    └─ Score < 80 → Suggest Improvements → Regenerate
```

### 11.4 Glossary

- **Agent**: AI-powered component that performs a specific task
- **Orchestrator**: System that coordinates multiple agents
- **Model Router**: Component that selects and routes to appropriate LLM
- **Repository**: Data access layer for specific entity type
- **Service Layer**: Business logic layer between API and data
- **git-crypt**: Transparent file encryption for Git repositories
- **WebSocket**: Bidirectional real-time communication protocol
- **Conversation**: Top-level entity representing recruiter interaction
- **Thread**: Sequence of messages within a conversation
- **Process Status**: Current stage in the hiring process
- **Fit Score**: Calculated match between candidate and job requirements

### 11.5 References

1. **FastAPI Documentation**: https://fastapi.tiangolo.com/
2. **Anthropic Claude API**: https://docs.anthropic.com/
3. **Pydantic**: https://docs.pydantic.dev/
4. **git-crypt**: https://github.com/AGWA/git-crypt
5. **pytest**: https://docs.pytest.org/
6. **WebSocket Protocol**: https://datatracker.ietf.org/doc/html/rfc6455

---

## Document Status

**Status**: ✅ Complete - Ready for Implementation
**Last Updated**: 2025-12-09
**Version**: 2.0.0
**Review Status**: Pending User Review

This system design provides a comprehensive blueprint for implementing CHOSEN. All major components, data flows, and architectural decisions are documented with code examples and diagrams.

The design prioritizes:
- **Modularity**: Clean separation of concerns
- **Scalability**: Parallel agent execution, caching
- **Security**: Encryption, validation, error handling
- **Testability**: Mock strategies, test pyramid
- **User Experience**: Real-time updates, quality assurance

Next steps: User review and approval before beginning Phase 1 implementation.
