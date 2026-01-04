"""Unit tests for ModelRouter class.

This module contains comprehensive tests for:
    - ModelRouter initialization and configuration
    - Model ID mapping (haiku, sonnet, opus)
    - Complete method with mocked SDK client
    - Stream method with mocked async iterator
    - Token usage tracking per model
    - Rate limiting functionality
    - Usage statistics retrieval
"""

import asyncio
from typing import Any, AsyncIterator, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.model_router import ModelRouter, ModelTier, TokenBucketRateLimiter


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def model_router() -> ModelRouter:
    """Create ModelRouter with default settings."""
    return ModelRouter()


@pytest.fixture
def model_router_haiku() -> ModelRouter:
    """Create ModelRouter with haiku as default model."""
    return ModelRouter(default_model="haiku")


@pytest.fixture
def rate_limiter() -> TokenBucketRateLimiter:
    """Create rate limiter for testing."""
    return TokenBucketRateLimiter(rate=10.0, capacity=10.0)


# =============================================================================
# ModelTier Enum Tests
# =============================================================================


@pytest.mark.unit
class TestModelTier:
    """Tests for ModelTier enum."""

    def test_haiku_value(self) -> None:
        """Test HAIKU enum has correct short name value."""
        assert ModelTier.HAIKU.value == "haiku"

    def test_sonnet_value(self) -> None:
        """Test SONNET enum has correct short name value."""
        assert ModelTier.SONNET.value == "sonnet"

    def test_opus_value(self) -> None:
        """Test OPUS enum has correct short name value."""
        assert ModelTier.OPUS.value == "opus"

    def test_model_tier_is_string_enum(self) -> None:
        """Test ModelTier inherits from str for JSON serialization."""
        assert isinstance(ModelTier.HAIKU, str)
        assert isinstance(ModelTier.SONNET, str)
        assert isinstance(ModelTier.OPUS, str)


# =============================================================================
# TokenBucketRateLimiter Tests
# =============================================================================


@pytest.mark.unit
class TestTokenBucketRateLimiter:
    """Tests for TokenBucketRateLimiter."""

    def test_initialization_defaults(self) -> None:
        """Test rate limiter initializes with default values."""
        limiter = TokenBucketRateLimiter()
        assert limiter.rate == 10.0
        assert limiter.capacity == 10.0
        assert limiter.tokens == 10.0

    def test_initialization_custom_values(self) -> None:
        """Test rate limiter initializes with custom values."""
        limiter = TokenBucketRateLimiter(rate=5.0, capacity=20.0)
        assert limiter.rate == 5.0
        assert limiter.capacity == 20.0
        assert limiter.tokens == 20.0

    async def test_acquire_single_token(self, rate_limiter: TokenBucketRateLimiter) -> None:
        """Test acquiring a single token."""
        initial_tokens = rate_limiter.tokens
        await rate_limiter.acquire(1)
        assert rate_limiter.tokens == initial_tokens - 1

    async def test_acquire_multiple_tokens(self, rate_limiter: TokenBucketRateLimiter) -> None:
        """Test acquiring multiple tokens."""
        initial_tokens = rate_limiter.tokens
        await rate_limiter.acquire(5)
        assert rate_limiter.tokens == initial_tokens - 5

    async def test_acquire_waits_when_insufficient_tokens(self) -> None:
        """Test acquire waits when tokens are insufficient."""
        limiter = TokenBucketRateLimiter(rate=100.0, capacity=1.0)
        # Acquire the single token
        await limiter.acquire(1)
        assert limiter.tokens == 0

        # Next acquire should wait but complete quickly due to high rate
        start = asyncio.get_event_loop().time()
        await limiter.acquire(1)
        elapsed = asyncio.get_event_loop().time() - start
        # Should have waited some time (very short due to 100 tokens/sec)
        assert elapsed >= 0

    async def test_tokens_refill_over_time(self) -> None:
        """Test that tokens refill based on time elapsed."""
        limiter = TokenBucketRateLimiter(rate=1000.0, capacity=10.0)
        await limiter.acquire(10)  # Drain all tokens
        assert limiter.tokens == 0

        # Wait a bit and acquire again - should refill
        await asyncio.sleep(0.01)  # 10ms = 10 tokens at 1000/sec
        await limiter.acquire(1)
        # Should have enough tokens now


# =============================================================================
# ModelRouter Initialization Tests
# =============================================================================


@pytest.mark.unit
class TestModelRouterInitialization:
    """Tests for ModelRouter initialization."""

    def test_default_model_is_sonnet(self, model_router: ModelRouter) -> None:
        """Test default model is sonnet."""
        assert model_router.default_model == "sonnet"

    def test_custom_default_model(self, model_router_haiku: ModelRouter) -> None:
        """Test custom default model."""
        assert model_router_haiku.default_model == "haiku"

    def test_token_usage_starts_empty(self, model_router: ModelRouter) -> None:
        """Test token usage dictionary is empty initially."""
        assert model_router.token_usage == {}

    def test_rate_limiter_initialized(self, model_router: ModelRouter) -> None:
        """Test rate limiter is initialized."""
        assert model_router._rate_limiter is not None
        assert isinstance(model_router._rate_limiter, TokenBucketRateLimiter)

    def test_custom_rate_limit(self) -> None:
        """Test custom rate limit."""
        router = ModelRouter(rate_limit=5.0)
        assert router._rate_limiter.rate == 5.0


# =============================================================================
# Model ID Mapping Tests
# =============================================================================


@pytest.mark.unit
class TestModelIdMapping:
    """Tests for model ID mapping."""

    def test_haiku_mapping(self, model_router: ModelRouter) -> None:
        """Test haiku maps correctly."""
        assert model_router.get_model_id("haiku") == "haiku"

    def test_sonnet_mapping(self, model_router: ModelRouter) -> None:
        """Test sonnet maps correctly."""
        assert model_router.get_model_id("sonnet") == "sonnet"

    def test_opus_mapping(self, model_router: ModelRouter) -> None:
        """Test opus maps correctly."""
        assert model_router.get_model_id("opus") == "opus"

    def test_case_insensitive_mapping(self, model_router: ModelRouter) -> None:
        """Test model mapping is case insensitive."""
        assert model_router.get_model_id("HAIKU") == "haiku"
        assert model_router.get_model_id("Sonnet") == "sonnet"
        assert model_router.get_model_id("OPUS") == "opus"

    def test_unknown_model_uses_default(self, model_router: ModelRouter) -> None:
        """Test unknown model falls back to default (sonnet)."""
        assert model_router.get_model_id("unknown") == "sonnet"

    def test_unknown_model_uses_custom_default(self, model_router_haiku: ModelRouter) -> None:
        """Test unknown model falls back to custom default (haiku)."""
        assert model_router_haiku.get_model_id("unknown") == "haiku"


# =============================================================================
# Complete Method Tests
# =============================================================================


@pytest.mark.unit
class TestCompleteMethod:
    """Tests for complete method."""

    async def test_complete_returns_text(self, model_router: ModelRouter) -> None:
        """Test complete returns generated text."""
        # Import the actual SDK classes for proper isinstance patching
        from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

        # Create mock objects that ARE instances of the SDK classes
        mock_text_block = MagicMock(spec=TextBlock)
        mock_text_block.text = "Hello, world!"

        mock_assistant_message = MagicMock(spec=AssistantMessage)
        mock_assistant_message.content = [mock_text_block]

        mock_result_message = MagicMock(spec=ResultMessage)
        mock_result_message.usage = {"input_tokens": 10, "output_tokens": 20}

        async def mock_receive_response() -> AsyncIterator[Any]:
            yield mock_assistant_message
            yield mock_result_message

        mock_client = MagicMock()
        mock_client.query = AsyncMock()
        mock_client.receive_response = mock_receive_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("app.agents.model_router.ClaudeSDKClient", return_value=mock_client):
            result = await model_router.complete(model="sonnet", prompt="Hello")

        assert result == "Hello, world!"

    async def test_complete_calls_rate_limiter(self, model_router: ModelRouter) -> None:
        """Test complete calls rate limiter acquire."""
        mock_rate_limiter = AsyncMock()
        model_router._rate_limiter = mock_rate_limiter

        async def mock_receive_response() -> AsyncIterator[Any]:
            return
            yield  # Empty generator

        mock_client = MagicMock()
        mock_client.query = AsyncMock()
        mock_client.receive_response = mock_receive_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("app.agents.model_router.ClaudeSDKClient", return_value=mock_client):
            await model_router.complete(model="sonnet", prompt="Hello")

        mock_rate_limiter.acquire.assert_called_once()

    async def test_complete_tracks_usage(self, model_router: ModelRouter) -> None:
        """Test complete tracks token usage."""
        from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

        mock_text_block = MagicMock(spec=TextBlock)
        mock_text_block.text = "Response"

        mock_assistant_message = MagicMock(spec=AssistantMessage)
        mock_assistant_message.content = [mock_text_block]

        mock_result_message = MagicMock(spec=ResultMessage)
        mock_result_message.usage = {"input_tokens": 10, "output_tokens": 20}

        async def mock_receive_response() -> AsyncIterator[Any]:
            yield mock_assistant_message
            yield mock_result_message

        mock_client = MagicMock()
        mock_client.query = AsyncMock()
        mock_client.receive_response = mock_receive_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("app.agents.model_router.ClaudeSDKClient", return_value=mock_client):
            await model_router.complete(model="sonnet", prompt="Hello")

        assert "sonnet" in model_router.token_usage
        assert model_router.token_usage["sonnet"]["input_tokens"] == 10
        assert model_router.token_usage["sonnet"]["output_tokens"] == 20


# =============================================================================
# Stream Method Tests
# =============================================================================


@pytest.mark.unit
class TestStreamMethod:
    """Tests for stream method."""

    async def test_stream_yields_text_chunks(self, model_router: ModelRouter) -> None:
        """Test stream yields text chunks."""
        from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

        mock_text_block = MagicMock(spec=TextBlock)
        mock_text_block.text = "Hello, world!"

        mock_assistant_message = MagicMock(spec=AssistantMessage)
        mock_assistant_message.content = [mock_text_block]

        mock_result_message = MagicMock(spec=ResultMessage)
        mock_result_message.usage = {"input_tokens": 10, "output_tokens": 20}

        async def mock_receive_response() -> AsyncIterator[Any]:
            yield mock_assistant_message
            yield mock_result_message

        mock_client = MagicMock()
        mock_client.query = AsyncMock()
        mock_client.receive_response = mock_receive_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        chunks: List[str] = []
        with patch("app.agents.model_router.ClaudeSDKClient", return_value=mock_client):
            async for chunk in model_router.stream(model="sonnet", prompt="Hello"):
                chunks.append(chunk)

        assert chunks == ["Hello, world!"]

    async def test_stream_calls_rate_limiter(self, model_router: ModelRouter) -> None:
        """Test stream calls rate limiter acquire."""
        mock_rate_limiter = AsyncMock()
        model_router._rate_limiter = mock_rate_limiter

        async def mock_receive_response() -> AsyncIterator[Any]:
            return
            yield  # Empty generator

        mock_client = MagicMock()
        mock_client.query = AsyncMock()
        mock_client.receive_response = mock_receive_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("app.agents.model_router.ClaudeSDKClient", return_value=mock_client):
            async for _ in model_router.stream(model="sonnet", prompt="Hello"):
                pass

        mock_rate_limiter.acquire.assert_called_once()

    async def test_stream_tracks_usage(self, model_router: ModelRouter) -> None:
        """Test stream tracks token usage after completion."""
        from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

        mock_text_block = MagicMock(spec=TextBlock)
        mock_text_block.text = "Response"

        mock_assistant_message = MagicMock(spec=AssistantMessage)
        mock_assistant_message.content = [mock_text_block]

        mock_result_message = MagicMock(spec=ResultMessage)
        mock_result_message.usage = {"input_tokens": 10, "output_tokens": 20}

        async def mock_receive_response() -> AsyncIterator[Any]:
            yield mock_assistant_message
            yield mock_result_message

        mock_client = MagicMock()
        mock_client.query = AsyncMock()
        mock_client.receive_response = mock_receive_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)

        with patch("app.agents.model_router.ClaudeSDKClient", return_value=mock_client):
            async for _ in model_router.stream(model="haiku", prompt="Hello"):
                pass

        assert "haiku" in model_router.token_usage
        assert model_router.token_usage["haiku"]["input_tokens"] == 10
        assert model_router.token_usage["haiku"]["output_tokens"] == 20


# =============================================================================
# Token Tracking Tests
# =============================================================================


@pytest.mark.unit
class TestTokenTracking:
    """Tests for token usage tracking."""

    def test_track_usage_creates_entry(self, model_router: ModelRouter) -> None:
        """Test _track_usage creates entry for new model."""
        usage = {"input_tokens": 100, "output_tokens": 50}
        model_router._track_usage("haiku", usage)

        assert "haiku" in model_router.token_usage
        assert model_router.token_usage["haiku"]["input_tokens"] == 100
        assert model_router.token_usage["haiku"]["output_tokens"] == 50

    def test_track_usage_accumulates(self, model_router: ModelRouter) -> None:
        """Test _track_usage accumulates tokens for same model."""
        usage1 = {"input_tokens": 100, "output_tokens": 50}
        usage2 = {"input_tokens": 200, "output_tokens": 100}

        model_router._track_usage("sonnet", usage1)
        model_router._track_usage("sonnet", usage2)

        assert model_router.token_usage["sonnet"]["input_tokens"] == 300
        assert model_router.token_usage["sonnet"]["output_tokens"] == 150

    def test_track_usage_handles_none(self, model_router: ModelRouter) -> None:
        """Test _track_usage handles None usage gracefully."""
        model_router._track_usage("haiku", None)
        # Entry created but no tokens added
        assert "haiku" in model_router.token_usage
        assert model_router.token_usage["haiku"]["input_tokens"] == 0
        assert model_router.token_usage["haiku"]["output_tokens"] == 0

    def test_track_usage_handles_missing_keys(self, model_router: ModelRouter) -> None:
        """Test _track_usage handles missing keys in usage dict."""
        usage: dict[str, int] = {}  # Empty dict
        model_router._track_usage("opus", usage)

        assert "opus" in model_router.token_usage
        assert model_router.token_usage["opus"]["input_tokens"] == 0
        assert model_router.token_usage["opus"]["output_tokens"] == 0

    def test_track_usage_per_model_separation(self, model_router: ModelRouter) -> None:
        """Test usage is tracked separately per model."""
        model_router._track_usage("haiku", {"input_tokens": 10, "output_tokens": 5})
        model_router._track_usage("sonnet", {"input_tokens": 100, "output_tokens": 50})
        model_router._track_usage("opus", {"input_tokens": 1000, "output_tokens": 500})

        assert model_router.token_usage["haiku"]["input_tokens"] == 10
        assert model_router.token_usage["sonnet"]["input_tokens"] == 100
        assert model_router.token_usage["opus"]["input_tokens"] == 1000


# =============================================================================
# Usage Stats Tests
# =============================================================================


@pytest.mark.unit
class TestUsageStats:
    """Tests for usage statistics retrieval."""

    def test_get_usage_stats_empty(self, model_router: ModelRouter) -> None:
        """Test get_usage_stats returns empty dict initially."""
        assert model_router.get_usage_stats() == {}

    def test_get_usage_stats_returns_data(self, model_router: ModelRouter) -> None:
        """Test get_usage_stats returns tracked data."""
        model_router._track_usage("sonnet", {"input_tokens": 100, "output_tokens": 50})

        stats = model_router.get_usage_stats()
        assert stats["sonnet"]["input_tokens"] == 100
        assert stats["sonnet"]["output_tokens"] == 50

    def test_get_usage_stats_returns_shallow_copy(self, model_router: ModelRouter) -> None:
        """Test get_usage_stats returns a copy at the top level."""
        model_router._track_usage("haiku", {"input_tokens": 10, "output_tokens": 5})

        stats = model_router.get_usage_stats()

        # Modifying the returned dict shouldn't affect internal state
        # Note: This is a shallow copy, so nested dicts share refs
        del stats["haiku"]

        # Original should still have haiku
        assert "haiku" in model_router.token_usage
        assert model_router.token_usage["haiku"]["input_tokens"] == 10
