# CHOSEN Risk Analysis

This document identifies key risks for the CHOSEN project and their mitigations.

## Risk Summary

| Risk | Severity | Probability | Mitigation Status |
|------|----------|-------------|-------------------|
| Anthropic API unavailable | High | Medium | Planned (AI Resilience Layer) |
| YAML data corruption | High | Medium | Planned (Atomic writes) |
| Prompt engineering costs | Medium | High | Planned (Budget tracking) |
| Agent quality untestable | Medium | High | Planned (Snapshot tests) |
| Context window exhaustion | Medium | Medium | Designed (Context management) |
| Schema evolution breaks data | Medium | Low | Planned (Versioning) |

---

## Detailed Risk Analysis

### 1. Anthropic API Unavailable

**Severity**: High
**Probability**: Medium (API has ~99.9% uptime = ~8 hours downtime/year)

**Impact**:
- All agent features fail during outage
- Development blocked during rate limiting
- Demo scenarios fail unpredictably

**Mitigations**:
1. **AI Resilience Layer** (P0 - New Issue)
   - Exponential backoff retry (3 attempts)
   - Cached response fallback for similar prompts
   - Graceful degradation with user-friendly error messages

2. **Development Safeguards**
   - Mock responses for offline development
   - Use Haiku for testing (lower cost, faster)
   - Cache prompt→response pairs in `data/cache/prompts/`

3. **Monitoring**
   - Log all API failures for debugging
   - Track response times and error rates
   - Alert on sustained failures

**Implementation**:
```python
# app/agents/client.py
class AIClient:
    async def generate(self, prompt: str, model: str = "sonnet") -> str:
        for attempt in range(3):
            try:
                return await self._anthropic_call(prompt, model)
            except RateLimitError:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        cached = self._cached_fallback(prompt)
        if cached:
            return cached
        raise ServiceUnavailable()
```

---

### 2. YAML Data Corruption

**Severity**: High
**Probability**: Medium

**Impact**:
- User loses conversation data
- Repository exceptions cascade to API errors
- All downstream features fail

**Triggers**:
- Malformed YAML (unicode, special characters, nested quotes)
- Partial writes (power loss, disk full)
- Manual file edits by user
- Git-crypt decryption failures

**Mitigations**:
1. **Atomic Writes** (RepositoryBase #68)
   - Write to temp file first
   - Validate temp file parses correctly
   - Backup existing file before overwrite
   - Atomic rename temp → target

2. **Recovery Mechanism**
   - On parse error, attempt load from `.backup` file
   - Log corruption for manual review
   - Document recovery procedure

3. **Schema Validation**
   - Add `_schema_version` field to all YAML files
   - Validate on load, migrate if needed

**Implementation**:
```python
# app/data/handlers/yaml_handler.py
def save(self, filepath: Path, data: dict) -> None:
    temp_path = filepath.with_suffix('.tmp')
    backup_path = filepath.with_suffix('.backup')

    # Write to temp
    temp_path.write_text(yaml.dump(data))

    # Validate
    yaml.safe_load(temp_path.read_text())

    # Backup and rename
    if filepath.exists():
        shutil.copy(filepath, backup_path)
    temp_path.rename(filepath)
```

---

### 3. Prompt Engineering Costs

**Severity**: Medium
**Probability**: High

**Impact**:
- Unexpected API bills
- Budget overruns during development
- Opus calls are expensive for iteration

**Mitigations**:
1. **Budget Tracking**
   - Add `MONTHLY_API_BUDGET_USD` env var
   - Track token usage per request
   - Alert when approaching limit

2. **Development Practices**
   - Use Haiku for development/testing
   - Reserve Sonnet/Opus for production
   - Cache responses during prompt iteration

3. **Cost Optimization**
   - Minimize context window usage
   - Batch similar requests when possible
   - Use shorter prompts where quality allows

---

### 4. Agent Quality Untestable

**Severity**: Medium
**Probability**: High

**Impact**:
- Can't detect quality regressions
- Prompt changes may degrade output
- No baseline for comparison

**Challenge**:
AI outputs are non-deterministic. Same prompt → different response each run.

**Mitigations**:
1. **Snapshot Testing**
   - Golden dataset of 20 example messages
   - Run agent, save outputs to `data/test-snapshots/`
   - Manual review on major changes
   - Detect regressions via diff

2. **Evaluation Metrics**
   - Response length (150-300 words target)
   - Tone detection (professional/friendly)
   - Contains required elements (greeting, CTA)
   - Automated scoring heuristics

3. **Human-in-Loop Validation**
   - Weekly review of sample responses
   - User feedback collection
   - Prompt iteration based on failures

---

### 5. Context Window Exhaustion

**Severity**: Medium
**Probability**: Medium

**Impact**:
- API errors for long conversations
- Incomplete responses
- Corrupted conversation state

**Mitigations**:
1. **Context Management** (AgentOrchestrator)
   - Track token count per conversation
   - Truncate older messages when approaching limit
   - Summarize conversation history periodically

2. **Model Selection**
   - Use appropriate model for context size
   - Haiku: 200K context (sufficient for most)
   - Sonnet: 200K context
   - Opus: 200K context

---

### 6. Schema Evolution Breaks Data

**Severity**: Medium
**Probability**: Low (careful planning)

**Impact**:
- Old YAML files unreadable
- Data migration required
- Potential data loss

**Mitigations**:
1. **Schema Versioning**
   - Add `_schema_version: 1` to all YAML files
   - Increment on breaking changes
   - Maintain migration scripts

2. **Backward Compatibility**
   - Optional fields have defaults
   - Graceful handling of unknown fields
   - Document breaking changes in CHANGELOG

---

## Risk Monitoring

### Development Phase
- Track API error rates in logs
- Monitor test coverage for new code
- Review YAML file integrity after writes

### Production Phase (Future)
- Add structured logging
- Implement error tracking (Sentry or similar)
- Dashboard for API usage and costs

---

## Risk Review Schedule

- **Weekly**: Review API costs and error logs
- **Per Milestone**: Reassess risk severity and probability
- **On Incident**: Post-mortem and mitigation update

---

*Last updated: 2025-12-27*
