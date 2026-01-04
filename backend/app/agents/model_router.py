"""Model router for routing requests to Claude models via Agent SDK.

This module provides the ModelRouter class which routes requests to different
Claude models (Haiku, Sonnet, Opus) using the Claude Agent SDK. It supports
both streaming and non-streaming completions, token usage tracking, and
basic rate limiting.

Example:
    >>> router = ModelRouter(default_model="sonnet")
    >>> response = await router.complete(model="haiku", prompt="Hello!")
    >>> print(response)
    "Hello! How can I help you today?"
"""

import asyncio
from enum import Enum
from time import monotonic
from typing import AsyncIterator, Dict, Literal, Optional

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
)


class ModelTier(str, Enum):
    """Model tiers for routing.

    Inherits from str for JSON serialization compatibility.
    Uses short names recognized by Claude Agent SDK.

    Attributes:
        HAIKU: Fast, lightweight model for quick tasks.
        SONNET: Balanced model for most use cases.
        OPUS: Most capable model for complex tasks.
    """

    HAIKU = "haiku"
    SONNET = "sonnet"
    OPUS = "opus"


class TokenBucketRateLimiter:
    """Simple token bucket rate limiter for controlling request rate.

    Uses a token bucket algorithm where tokens are added at a fixed rate
    and requests consume tokens. If tokens are insufficient, the request
    waits until enough tokens are available.

    Attributes:
        rate: Tokens added per second.
        capacity: Maximum tokens in the bucket.
        tokens: Current token count.
    """

    def __init__(self, rate: float = 10.0, capacity: float = 10.0) -> None:
        """Initialize the rate limiter.

        Args:
            rate: Tokens added per second. Default is 10.0.
            capacity: Maximum tokens in bucket. Default is 10.0.
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> None:
        """Wait until the specified number of tokens are available.

        Args:
            tokens: Number of tokens to acquire. Default is 1.
        """
        async with self._lock:
            while self.tokens < tokens:
                now = monotonic()
                elapsed = now - self.last_update
                refill = elapsed * self.rate
                self.tokens = min(self.capacity, self.tokens + refill)
                self.last_update = now

                if self.tokens < tokens:
                    wait_time = (tokens - self.tokens) / self.rate
                    await asyncio.sleep(wait_time)

            self.tokens -= tokens
            self.last_update = monotonic()


class ModelRouter:
    """Routes requests to appropriate Claude models via Agent SDK.

    Provides a unified interface for sending requests to different Claude
    models with support for both streaming and non-streaming completions.
    Tracks token usage per model and implements basic rate limiting.

    Features:
        - Model selection (haiku, sonnet, opus)
        - Streaming support via async iterator
        - Token tracking per model
        - Basic rate limiting
        - No API key management (uses Claude Code CLI)

    Attributes:
        default_model: Default model to use when unknown model is requested.
        token_usage: Dictionary tracking token usage per model.

    Example:
        >>> router = ModelRouter(default_model="sonnet", rate_limit=10.0)
        >>> response = await router.complete(
        ...     model="haiku",
        ...     prompt="Summarize this text",
        ...     system="You are a helpful assistant"
        ... )
    """

    def __init__(
        self,
        default_model: Literal["haiku", "sonnet", "opus"] = "sonnet",
        rate_limit: float = 10.0,
    ) -> None:
        """Initialize the ModelRouter.

        Args:
            default_model: Default model when unknown model is requested.
                Defaults to "sonnet".
            rate_limit: Maximum requests per second. Defaults to 10.0.
        """
        self.default_model = default_model
        self.token_usage: Dict[str, Dict[str, int]] = {}
        self._rate_limiter = TokenBucketRateLimiter(
            rate=rate_limit, capacity=rate_limit
        )

    def get_model_id(self, model: str) -> str:
        """Map model name to standardized form.

        Args:
            model: Model name (case-insensitive). Can be "haiku",
                "sonnet", or "opus".

        Returns:
            Standardized model name. Returns default_model for unknown models.
        """
        model_map = {
            "haiku": ModelTier.HAIKU.value,
            "sonnet": ModelTier.SONNET.value,
            "opus": ModelTier.OPUS.value,
        }
        return model_map.get(model.lower(), self.default_model)

    async def complete(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
    ) -> str:
        """Get non-streaming completion from Claude.

        Sends a prompt to the specified model and returns the complete
        response. Token usage is tracked after the response is received.

        Args:
            model: Model tier (haiku, sonnet, opus).
            prompt: User prompt to send.
            system: Optional system prompt.

        Returns:
            Generated text response.

        Raises:
            CLINotFoundError: If Claude Code CLI is not installed.
            CLIConnectionError: If connection to CLI fails.
        """
        await self._rate_limiter.acquire()
        model_id = self.get_model_id(model)

        options = ClaudeAgentOptions(
            model=model_id,
            system_prompt=system,
        )

        response_text = ""
        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_text += block.text
                elif isinstance(message, ResultMessage):
                    self._track_usage(model_id, message.usage)

        return response_text

    async def stream(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """Stream completion from Claude.

        Sends a prompt to the specified model and yields text chunks
        as they arrive. Token usage is tracked after the stream completes.

        Args:
            model: Model tier (haiku, sonnet, opus).
            prompt: User prompt to send.
            system: Optional system prompt.

        Yields:
            Text chunks as they are received.

        Raises:
            CLINotFoundError: If Claude Code CLI is not installed.
            CLIConnectionError: If connection to CLI fails.
        """
        await self._rate_limiter.acquire()
        model_id = self.get_model_id(model)

        options = ClaudeAgentOptions(
            model=model_id,
            system_prompt=system,
        )

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            yield block.text
                elif isinstance(message, ResultMessage):
                    self._track_usage(model_id, message.usage)

    def _track_usage(
        self, model_id: str, usage: Optional[Dict[str, int]]
    ) -> None:
        """Track token usage per model.

        Args:
            model_id: Model identifier (haiku, sonnet, opus).
            usage: Dictionary with input_tokens and output_tokens counts.
        """
        if model_id not in self.token_usage:
            self.token_usage[model_id] = {
                "input_tokens": 0,
                "output_tokens": 0,
            }

        if usage:
            input_tokens = usage.get("input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)
            self.token_usage[model_id]["input_tokens"] += input_tokens
            self.token_usage[model_id]["output_tokens"] += output_tokens

    def get_usage_stats(self) -> Dict[str, Dict[str, int]]:
        """Get usage statistics.

        Returns a copy of the token usage dictionary to prevent
        external modification of internal state.

        Returns:
            Dictionary mapping model IDs to usage dictionaries containing
            input_tokens and output_tokens counts.
        """
        return self.token_usage.copy()
