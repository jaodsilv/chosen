# V2 Requirements Questionnaire

**Created**: 2025-12-09
**Status**: Awaiting User Responses
**Purpose**: Capture detailed requirements, validate assumptions, and discover use-cases for the v2 message writer assistant

---

## Introduction

This questionnaire is designed to gather detailed requirements for the v2 system. It's structured around seven key areas, with questions ranging from workflow understanding to feature priorities to technical preferences.

**How to use this document**:
1. Read each question carefully
2. Provide detailed answers where applicable
3. Skip questions that aren't relevant to your workflow
4. Add notes or additional context wherever helpful
5. Highlight any assumptions that are incorrect

---

## Section 1: User Workflow Questions

**Goal**: Understand your current process and pain points to design a system that fits naturally into your workflow.

### 1.1 Current Message Processing Workflow

**Q1.1.1**: Walk me through your current process when you receive a recruiter message on LinkedIn. What are the steps from receiving the message to sending a response?

```
Your answer:
[Example:
1. Read message in LinkedIn
2. Copy to notes app
3. Research company on Glassdoor
4. Check if role matches interests
5. Draft response
6. Edit for tone
7. Copy back to LinkedIn
8. Send
]
```

**Q1.1.2**: How does your workflow differ for email messages vs LinkedIn messages?

```
Your answer:
```

**Q1.1.3**: What tools/apps do you currently use in your job hunting process? (e.g., spreadsheets, note-taking apps, calendar apps, CRM tools)

```
Your answer:
```

**Q1.1.4**: What percentage of recruiter messages do you respond to? What determines whether you respond?

```
Your answer (e.g., "~40%, I respond if role is relevant and compensation is mentioned"):
```

### 1.2 Response Timing

**Q1.2.1**: What's your typical target response time for recruiter messages?
- [ ] Within 1 hour
- [ ] Same business day
- [ ] Within 24 hours
- [ ] Within 48 hours
- [ ] Within 1 week
- [ ] Variable (depends on interest level)
- [ ] Other: _______________

**Q1.2.2**: Do you intentionally delay responses for strategic reasons? If yes, in what situations?

```
Your answer:
```

**Q1.2.3**: How do you currently track when to follow up if a recruiter doesn't respond?
- [ ] Manual calendar reminders
- [ ] Mental tracking
- [ ] Spreadsheet with dates
- [ ] Email/LinkedIn reminders
- [ ] I don't track follow-ups
- [ ] Other: _______________

### 1.3 Conversation Management

**Q1.3.1**: On average, how many active recruiter conversations are you managing simultaneously during an active job search?
- [ ] 1-3
- [ ] 4-7
- [ ] 8-15
- [ ] 16-30
- [ ] 30+

**Q1.3.2**: How do you currently organize and track these conversations?

```
Your answer:
```

**Q1.3.3**: What information do you wish you could easily reference across all conversations? (e.g., "which companies offered what salary range", "which recruiters are most responsive")

```
Your answer:
```

### 1.4 Response Creation Process

**Q1.4.1**: Do you currently use templates, craft each response from scratch, or a mix?
- [ ] Always use templates (with minor customization)
- [ ] Mostly templates, some from scratch
- [ ] Mix of both equally
- [ ] Mostly from scratch, some templates for common scenarios
- [ ] Always craft from scratch

**Q1.4.2**: If you use templates, what are the most common template types you need? (Select all that apply)
- [ ] Initial interest expression
- [ ] Polite decline
- [ ] Request for more information
- [ ] Follow-up after no response
- [ ] Interview scheduling
- [ ] Thank you after interview
- [ ] Negotiation/counter-offer
- [ ] Acceptance
- [ ] Other: _______________

**Q1.4.3**: How much time do you typically spend crafting a single response?
- [ ] 1-5 minutes (quick replies)
- [ ] 5-15 minutes (standard responses)
- [ ] 15-30 minutes (important responses)
- [ ] 30-60 minutes (high-stakes like negotiation)
- [ ] Variable: _______________

**Q1.4.4**: What aspects of response writing take the most time or mental energy? (Select top 3)
- [ ] Getting the tone right (professional but not stiff)
- [ ] Deciding what information to include/exclude
- [ ] Crafting strategic language (maintaining leverage)
- [ ] Addressing compensation expectations
- [ ] Asking the right questions
- [ ] Structuring the message
- [ ] Proofreading and editing
- [ ] Deciding on timing
- [ ] Other: _______________

---

## Section 2: Feature Priority Questions

**Goal**: Identify which proposed features would provide the most value and should be prioritized.

### 2.1 Proposed Agent Priorities

Below are the 7 proposed agents. **Rank them from 1 (most important) to 7 (least important)** based on what would provide the most immediate value to you.

- [ ] **Rank ___**: Conversation Context Analyzer (analyzes conversation threads for sentiment, patterns, action items)
- [ ] **Rank ___**: Job Description Analyzer (deep analysis of JDs, fit scoring, requirement extraction)
- [ ] **Rank ___**: Follow-up Timing Optimizer (intelligent follow-up timing recommendations)
- [ ] **Rank ___**: Compensation Negotiation Agent (specialized negotiation strategy and response crafting)
- [ ] **Rank ___**: Multi-Conversation Analytics (aggregate insights across all conversations)
- [ ] **Rank ___**: Response Quality Scorer (pre-send quality assessment and optimization)
- [ ] **Rank ___**: Knowledge Gap Researcher (research gaps and provide learning resources/mitigation)

**Q2.1.1**: Are there any agents you would NOT use? Why?

```
Your answer:
```

**Q2.1.2**: Are there any critical agent capabilities missing from this list?

```
Your answer:
```

### 2.2 Command Priorities

Below are the 6 proposed commands. **Select all that you would use regularly** (at least weekly during active job search).

- [ ] `/jobs:quick-reply` - Fast template-based responses for common patterns
- [ ] `/jobs:compare-opportunities` - Side-by-side comparison of active opportunities
- [ ] `/jobs:follow-up-check` - Scan conversations and identify which need follow-ups
- [ ] `/jobs:archive-conversation` - Archive completed/dead conversations
- [ ] `/jobs:debug-parse` - Debug message parsing issues
- [ ] `/jobs:batch-update-status` - Update status for multiple conversations at once

**Q2.2.1**: Which command would you use most frequently?

```
Your answer:
```

**Q2.2.2**: What commands or workflows are missing that you'd use regularly?

```
Your answer:
```

### 2.3 Pain Point Priorities

**Q2.3.1**: What are your top 3 pain points in your current job hunting communication process? (Describe in detail)

```
1. [Your answer]

2. [Your answer]

3. [Your answer]
```

**Q2.3.2**: Which proposed features would best address your top pain point?

```
Your answer:
```

### 2.4 Workflow Scenarios

**Q2.4.1**: Which scenarios do you encounter most frequently? (Select all that apply and mark frequency)

- [ ] **___x/week**: Cold recruiter outreach on LinkedIn (recruiter found you)
- [ ] **___x/week**: Application response (you applied, they responded)
- [ ] **___x/week**: Recruiter follow-up (continuing existing conversation)
- [ ] **___x/week**: Interview scheduling coordination
- [ ] **___x/month**: Post-interview follow-up/thank you
- [ ] **___x/month**: Compensation negotiation
- [ ] **___x/month**: Declining opportunities
- [ ] **___x/month**: Multiple competing offers to evaluate
- [ ] **___x/month**: Following up when recruiter goes silent
- [ ] Other: _______________

**Q2.4.2**: Are there any workflows or scenarios not covered in the current proposals?

```
Your answer:
```

---

## Section 3: Data & Privacy Questions

**Goal**: Understand your data security, privacy, and portability requirements.

### 3.1 Data Storage and Security

**Q3.1.1**: What data MUST stay local and never be sent to the cloud?
- [ ] All data (everything stays local)
- [ ] Resume/personal info only
- [ ] Compensation details only
- [ ] Company names and recruiter names
- [ ] Message content
- [ ] No restrictions (cloud storage is fine)
- [ ] Other specific data: _______________

**Q3.1.2**: The current system uses git-crypt for encryption of sensitive data. Is this approach acceptable?
- [ ] Yes, git-crypt is fine
- [ ] Prefer different encryption method (specify): _______________
- [ ] Don't need encryption
- [ ] Need stronger encryption (specify requirements): _______________

**Q3.1.3**: Are you comfortable with your conversation data being processed by Claude API (Anthropic) for response generation?
- [ ] Yes, fully comfortable
- [ ] Yes, but with data sanitization (remove personal identifiers first)
- [ ] Only if data doesn't leave my machine (local models only)
- [ ] Need to review Anthropic's data policies first
- [ ] Other concerns: _______________

### 3.2 Conversation Export and Portability

**Q3.2.1**: How important is the ability to export your conversation data?
- [ ] Critical (must have)
- [ ] Important (nice to have)
- [ ] Low priority
- [ ] Not needed

**Q3.2.2**: If you needed to export data, what formats would be most useful? (Select all that apply)
- [ ] JSON (structured data)
- [ ] CSV (for spreadsheet analysis)
- [ ] Markdown (human-readable)
- [ ] PDF (for archival)
- [ ] HTML (for viewing in browser)
- [ ] Other: _______________

**Q3.2.3**: What would you want to do with exported data?
- [ ] Analyze in spreadsheet (compensation trends, response rates, etc.)
- [ ] Import into another job tracking system
- [ ] Archive for future reference
- [ ] Share with career coach or mentor
- [ ] Generate reports
- [ ] Other: _______________

### 3.3 Cross-Device and Backup

**Q3.3.1**: Do you need to access this system from multiple machines?
- [ ] No, single machine only
- [ ] Yes, 2-3 machines (e.g., work laptop, personal desktop)
- [ ] Yes, many machines
- [ ] Need mobile access too

**Q3.3.2**: If multi-machine access is needed, what's your preferred sync approach?
- [ ] Git repository (push/pull manually)
- [ ] Cloud sync (Dropbox, OneDrive, Google Drive)
- [ ] Custom sync service
- [ ] No preference
- [ ] Other: _______________

**Q3.3.3**: How important is automatic backup?
- [ ] Critical (must have automated backup)
- [ ] Important (nice to have)
- [ ] Low priority (manual backup is fine)
- [ ] Not needed

---

## Section 4: Integration Questions

**Goal**: Understand desired integrations with existing tools and services.

### 4.1 CLI vs Web Interface

**Q4.1.1**: The current system uses Claude Code CLI. For v2, what's your preference?
- [ ] CLI only (current approach)
- [ ] Web interface only (browser-based)
- [ ] Both CLI and web (use whichever is convenient)
- [ ] CLI primary, minimal web UI for viewing
- [ ] Web primary, CLI for advanced features
- [ ] Other: _______________

**Q4.1.2**: If web interface is desired, what features would you want in the web UI? (Select all that apply)
- [ ] Dashboard showing all active conversations
- [ ] Side-by-side opportunity comparison
- [ ] Message composition and editing
- [ ] Analytics and charts
- [ ] Calendar integration for interview scheduling
- [ ] Mobile-responsive design
- [ ] Keyboard shortcuts
- [ ] Other: _______________

### 4.2 Email and LinkedIn Integration

**Q4.2.1**: Would you want automatic message import from email/LinkedIn?
- [ ] Yes, automatic import is critical (scrape messages automatically)
- [ ] Yes, but semi-automatic (browser extension to capture messages)
- [ ] No, manual copy-paste is fine
- [ ] Unsure, need to understand privacy/security implications

**Q4.2.2**: If automatic import, what's your preferred approach?
- [ ] Browser extension (capture messages when viewing in browser)
- [ ] Email client integration (plugin for Outlook/Gmail)
- [ ] API integration (use LinkedIn/email APIs)
- [ ] Email forwarding (forward messages to system)
- [ ] Other: _______________

**Q4.2.3**: Would you want the ability to send messages directly from the system?
- [ ] Yes, send directly from system to LinkedIn/email
- [ ] No, I'll copy-paste to send manually (prefer control)
- [ ] Optional (nice to have but not critical)

### 4.3 Calendar Integration

**Q4.3.1**: Would calendar integration for interview scheduling be valuable?
- [ ] Very valuable (critical feature)
- [ ] Somewhat valuable (nice to have)
- [ ] Not valuable (don't need it)

**Q4.3.2**: If calendar integration is desired, which calendar systems do you use? (Select all that apply)
- [ ] Google Calendar
- [ ] Microsoft Outlook Calendar
- [ ] Apple Calendar
- [ ] Other: _______________

**Q4.3.3**: What calendar features would be most useful?
- [ ] Show availability when scheduling interviews
- [ ] Auto-add confirmed interviews to calendar
- [ ] Send interview reminders
- [ ] Track time-to-interview metrics
- [ ] Block time for interview prep
- [ ] Other: _______________

### 4.4 Job Board and Company Research Integration

**Q4.4.1**: Would integration with job boards be useful?
- [ ] Yes, critical (auto-import job descriptions)
- [ ] Yes, nice to have
- [ ] No, not needed

**Q4.4.2**: Which job boards do you use most? (Select all that apply)
- [ ] LinkedIn Jobs
- [ ] Indeed
- [ ] Glassdoor
- [ ] AngelList (Wellfound)
- [ ] Dice
- [ ] ZipRecruiter
- [ ] Company career pages directly
- [ ] Other: _______________

**Q4.4.3**: Would automatic company research be valuable? (e.g., auto-fetch Glassdoor ratings, recent news, funding, culture info)
- [ ] Very valuable
- [ ] Somewhat valuable
- [ ] Not needed

### 4.5 CRM and Tracking Tools

**Q4.5.1**: Do you currently use any CRM or job tracking tools?
- [ ] Yes: _______________ (specify tool)
- [ ] No, but interested in using one
- [ ] No, and not interested

**Q4.5.2**: If you use external tracking tools, would you want to integrate with them?
- [ ] Yes, critical (bidirectional sync)
- [ ] Yes, nice to have (export to them)
- [ ] No, prefer standalone system

---

## Section 5: UI/UX Questions

**Goal**: Understand interface preferences and usability requirements.

### 5.1 Interface Style Preference

**Q5.1.1**: What interface style do you prefer?
- [ ] Minimal (focus on core features, simple interface)
- [ ] Balanced (key features visible, advanced features available)
- [ ] Feature-rich (all capabilities easily accessible)
- [ ] Adaptive (start minimal, reveal features as needed)

**Q5.1.2**: How much detail do you want in agent outputs?
- [ ] High detail (show full analysis, reasoning, alternatives)
- [ ] Medium detail (show key insights and recommendations)
- [ ] Low detail (just give me the answer)
- [ ] Configurable (let me choose per situation)

**Q5.1.3**: For generated responses, how do you want to review and edit?
- [ ] Show in terminal, copy-paste when ready
- [ ] Open in text editor for modification
- [ ] In-browser editor with preview
- [ ] Direct edit in command output
- [ ] No preference

### 5.2 Mobile Access

**Q5.2.1**: How important is mobile access (phone/tablet)?
- [ ] Critical (I often handle recruiter messages on mobile)
- [ ] Important (occasionally need mobile access)
- [ ] Low priority (rarely use mobile for job hunting)
- [ ] Not needed (desktop/laptop only)

**Q5.2.2**: If mobile access is needed, what features must work on mobile?
- [ ] View all conversations
- [ ] Read conversation history
- [ ] Send quick replies
- [ ] Schedule interviews
- [ ] Review and edit generated responses
- [ ] Access analytics
- [ ] Other: _______________

### 5.3 Keyboard Shortcuts and Efficiency

**Q5.3.1**: How important are keyboard shortcuts for efficiency?
- [ ] Critical (I'm a power user, keyboard shortcuts are essential)
- [ ] Important (nice to have for common actions)
- [ ] Low priority (mouse/touch interaction is fine)
- [ ] Not needed

**Q5.3.2**: What actions would you want keyboard shortcuts for? (Select all that apply)
- [ ] Generate response
- [ ] Edit response
- [ ] Send/copy response
- [ ] Next/previous conversation
- [ ] Archive conversation
- [ ] Change conversation status
- [ ] Search conversations
- [ ] Quick reply templates
- [ ] Other: _______________

### 5.4 Visual Preferences

**Q5.4.1**: For analytics and dashboards, what visualization style do you prefer?
- [ ] Text-based tables and lists (CLI-friendly)
- [ ] ASCII charts and graphs (CLI-friendly)
- [ ] Rich visualizations (charts, graphs, interactive - requires GUI)
- [ ] Mix of both (text primary, visuals optional)

**Q5.4.2**: How do you prefer to see conversation status/progress?
- [ ] Text labels only (e.g., "interviewing")
- [ ] Colored indicators (e.g., green/yellow/red)
- [ ] Progress bars or stages
- [ ] Timeline visualization
- [ ] Kanban board style
- [ ] No preference

---

## Section 6: Automation Level Questions

**Goal**: Determine the right balance between automation and manual control.

### 6.1 Message Analysis Automation

**Q6.1.1**: Should conversation analysis (sentiment, patterns, context) run automatically?
- [ ] Yes, always analyze automatically in background
- [ ] Yes, but only when I request it
- [ ] Yes, but only for new messages (not retroactive)
- [ ] No, I'll manually trigger analysis when needed

**Q6.1.2**: Should the system automatically detect and suggest status changes? (e.g., "This message mentions scheduling an interview, change status to 'interviewing'?")
- [ ] Yes, auto-update status (I'll review changes log)
- [ ] Yes, but ask for confirmation before changing
- [ ] Yes, suggest but don't change automatically
- [ ] No, I'll manually update status

### 6.2 Response Generation Automation

**Q6.2.1**: Should responses be auto-generated when new messages arrive?
- [ ] Yes, auto-generate draft response immediately
- [ ] Yes, but only for certain message types (specify): _______________
- [ ] No, I'll request response generation when ready
- [ ] Optional (configurable per conversation)

**Q6.2.2**: Should the system auto-select the best response template/style?
- [ ] Yes, always auto-select based on context
- [ ] Yes, but show me why and let me override
- [ ] No, I'll always manually choose template/style
- [ ] Sometimes (auto-select for routine, manual for important)

### 6.3 Follow-up Automation

**Q6.3.1**: How should follow-up checking work?
- [ ] Automatic daily scan with notification of needed follow-ups
- [ ] Automatic scan on-demand when I run command
- [ ] Manual tracking only (no automatic scanning)
- [ ] Automatic scan with auto-draft follow-up messages

**Q6.3.2**: If a follow-up is needed, should the system automatically draft the follow-up message?
- [ ] Yes, always auto-draft
- [ ] Yes, but only for simple follow-ups
- [ ] No, just notify me that follow-up is needed
- [ ] Optional (configurable)

### 6.4 Auto-Send and Notifications

**Q6.4.1**: Should the system ever auto-send messages without your explicit confirmation?
- [ ] Yes, for certain low-risk message types (specify): _______________
- [ ] No, NEVER auto-send (always require manual confirmation)
- [ ] Optional (I can enable for specific scenarios)

**Q6.4.2**: What notification preferences do you have?
- [ ] No notifications (I'll check system when ready)
- [ ] Desktop notifications for new recruiter messages
- [ ] Desktop notifications for follow-up reminders
- [ ] Email digest (daily/weekly summary)
- [ ] Mobile push notifications
- [ ] Other: _______________

### 6.5 Learning and Adaptation

**Q6.5.1**: Should the system automatically learn from your edits to generated responses?
- [ ] Yes, track my edits and adapt future responses
- [ ] Yes, but let me review what it learned
- [ ] No, keep responses consistent per templates
- [ ] Optional (I can enable/disable learning)

**Q6.5.2**: Should the system track which approaches work best (e.g., response rates, time-to-interview)?
- [ ] Yes, always track and apply learnings
- [ ] Yes, track but let me review insights before applying
- [ ] Yes, track for information only (don't auto-apply)
- [ ] No, don't track effectiveness

---

## Section 7: Edge Cases & Advanced Features

**Goal**: Identify complex scenarios and advanced use cases.

### 7.1 Multi-Company Negotiations

**Q7.1.1**: Do you typically negotiate with multiple companies simultaneously?
- [ ] Yes, frequently (common scenario)
- [ ] Yes, occasionally (happens sometimes)
- [ ] Rarely (uncommon)
- [ ] Never (don't juggle multiple offers)

**Q7.1.2**: If yes, what support would be most valuable?
- [ ] Track all offer details in one view
- [ ] Calculate best total compensation across offers
- [ ] Timeline coordination (alignment of deadlines)
- [ ] Leverage one offer against another (strategy and messaging)
- [ ] Compare non-compensation factors (culture, growth, etc.)
- [ ] Other: _______________

### 7.2 Team Communication Tracking

**Q7.2.1**: Do you sometimes communicate with multiple people at the same company (recruiter, hiring manager, team members)?
- [ ] Yes, very common
- [ ] Yes, occasionally
- [ ] Rarely
- [ ] Never

**Q7.2.2**: If yes, how should the system handle this?
- [ ] Separate conversation threads, loosely linked
- [ ] Single conversation with multiple participants tracked
- [ ] Consolidated view showing all interactions with company
- [ ] Other: _______________

### 7.3 Interview Preparation Workflows

**Q7.3.1**: How do you currently prepare for interviews?

```
Your answer:
```

**Q7.3.2**: Would interview preparation features be valuable? (Select all that apply)
- [ ] Auto-research company and generate prep notes
- [ ] Common interview questions for role/company
- [ ] Generate STAR method answers from resume
- [ ] Track questions you've been asked (build question bank)
- [ ] Prep checklist (research company, prepare questions, test tech setup)
- [ ] Post-interview debrief template
- [ ] Other: _______________

### 7.4 Long-Running Relationships

**Q7.4.1**: Do you have recurring relationships with certain recruiters (multiple roles over time)?
- [ ] Yes, frequently (recruiters I work with regularly)
- [ ] Yes, occasionally
- [ ] Rarely
- [ ] Never

**Q7.4.2**: If yes, should the system maintain recruiter relationship history?
- [ ] Yes, track all conversations with each recruiter over time
- [ ] Yes, track basic info (responsiveness, companies, outcomes)
- [ ] No, treat each conversation independently
- [ ] Optional

### 7.5 Contract vs Full-Time Positions

**Q7.5.1**: Do you pursue both contract and full-time positions?
- [ ] Full-time only
- [ ] Contract only
- [ ] Both equally
- [ ] Primarily full-time, occasionally contract
- [ ] Primarily contract, occasionally full-time

**Q7.5.2**: If both, how different are your requirements/approach?

```
Your answer:
```

**Q7.5.3**: Should contract and full-time be treated differently by the system?
- [ ] Yes, different compensation templates and logic
- [ ] Yes, different conversation stages/workflows
- [ ] Mostly the same, minor differences
- [ ] No, treat identically

### 7.6 Passive vs Active Job Search

**Q7.6.1**: Are you typically in passive or active job search mode?
- [ ] Always passive (not actively looking, respond to good opportunities)
- [ ] Usually passive, occasionally active
- [ ] Alternates between passive and active
- [ ] Usually active, occasionally passive
- [ ] Always active (actively applying and seeking)

**Q7.6.2**: Should the system adapt behavior based on search mode?
- [ ] Yes, different response tone (passive = higher bar, active = more open)
- [ ] Yes, different urgency for follow-ups
- [ ] Yes, different compensation approach
- [ ] No, keep consistent regardless of mode
- [ ] Optional (configurable per conversation)

### 7.7 Specialized Scenarios

**Q7.7.1**: Do any of these specialized scenarios apply to you? (Select all that apply)
- [ ] International relocation (visa, remote from different country)
- [ ] Remote work from non-standard location
- [ ] Return to work after career break
- [ ] Career transition (changing domains/roles)
- [ ] Leadership roles (management/executive)
- [ ] Startup equity heavy roles
- [ ] Government/security clearance roles
- [ ] Academic/research positions
- [ ] Other: _______________

**Q7.7.2**: For any selected scenarios, what specific support would you need?

```
Your answer:
```

---

## Section 8: Default Assumptions to Validate

**Goal**: Review assumptions made in the design proposals and validate or correct them.

### 8.1 Platform Assumptions

**Assumption**: Most recruiter communication happens on LinkedIn and email.

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

**Assumption**: Phone calls and in-person meetings are less common and can be tracked via manual notes.

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

### 8.2 Workflow Assumptions

**Assumption**: You typically respond to multiple recruiter messages per week during active job search.

- [ ] ✅ Correct (approximately ___ messages/week)
- [ ] ❌ Incorrect: _______________

**Assumption**: Response quality and professionalism are more important than response speed.

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

**Assumption**: You prefer to review and edit all generated responses before sending (no auto-send).

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

### 8.3 Compensation Assumptions

**Assumption**: You have clear minimum compensation thresholds (below which you auto-decline).

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

**Assumption**: Total compensation (base + equity + benefits) is more important than base salary alone.

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

**Assumption**: You want compensation mentioned strategically in responses (not too early, not too aggressive).

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

### 8.4 Data and Privacy Assumptions

**Assumption**: You're comfortable with YAML files for data storage (human-readable, version-controllable).

- [ ] ✅ Correct
- [ ] ❌ Incorrect, prefer: _______________

**Assumption**: Git-crypt encryption for sensitive data is sufficient.

- [ ] ✅ Correct
- [ ] ❌ Incorrect, need: _______________

**Assumption**: You want all data stored locally in files (not database).

- [ ] ✅ Correct
- [ ] ❌ Incorrect, prefer: _______________

### 8.5 Feature Assumptions

**Assumption**: Analytics and insights across conversations are valuable.

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

**Assumption**: Automated fit scoring (job requirements vs resume) is valuable.

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

**Assumption**: You want the system to proactively identify patterns and suggest optimizations.

- [ ] ✅ Correct
- [ ] ❌ Incorrect: _______________

### 8.6 User Experience Assumptions

**Assumption**: CLI (command-line) interface is acceptable as primary interface.

- [ ] ✅ Correct
- [ ] ❌ Incorrect, need: _______________

**Assumption**: You're comfortable with YAML input/output for structured data.

- [ ] ✅ Correct
- [ ] ❌ Incorrect, prefer: _______________

**Assumption**: You prefer seeing agent reasoning/analysis in addition to final recommendations.

- [ ] ✅ Correct (show me the thinking)
- [ ] ❌ Incorrect (just give me the answer)
- [ ] Configurable (sometimes want details, sometimes just answer)

---

## Section 9: Additional Context and Use Cases

**Goal**: Capture scenarios, requirements, or use cases not yet addressed.

### 9.1 Unaddressed Workflows

**Q9.1.1**: Are there any common workflows in your job search process that haven't been addressed in this questionnaire?

```
Your answer:
```

**Q9.1.2**: Are there any specific pain points or frustrations not covered?

```
Your answer:
```

### 9.2 Success Metrics

**Q9.2.1**: How would you measure success for this system? What would make it invaluable to you?

```
Your answer:
```

**Q9.2.2**: What would cause you to stop using this system?

```
Your answer:
```

### 9.3 Inspiration from Other Tools

**Q9.3.1**: Are there any tools (job hunting or otherwise) whose features you'd like to see incorporated?

```
Your answer:
```

### 9.4 Future Vision

**Q9.4.1**: If this system could do anything (no technical limitations), what would be your dream features?

```
Your answer:
```

### 9.5 Context on Your Situation

**Q9.5.1**: What's your current job search situation?
- [ ] Actively looking, need job soon
- [ ] Actively looking, can be selective
- [ ] Passively open to opportunities
- [ ] Employed, exploring options
- [ ] Between jobs
- [ ] Other: _______________

**Q9.5.2**: What's your typical job search timeline?
- [ ] Always ongoing (continuous networking)
- [ ] 1-3 months when actively searching
- [ ] 3-6 months when actively searching
- [ ] 6+ months when actively searching
- [ ] Variable

**Q9.5.3**: Any other context about your job hunting process that would help inform the design?

```
Your answer:
```

---

## Section 10: Technical Preferences

**Goal**: Understand technical constraints and preferences.

### 10.1 Development Environment

**Q10.1.1**: What operating system(s) do you use?
- [ ] Windows (version: _______)
- [ ] macOS (version: _______)
- [ ] Linux (distribution: _______)
- [ ] Multiple: _______________

**Q10.1.2**: What's your comfort level with technical tools?
- [ ] Very comfortable (developer, use CLI daily)
- [ ] Comfortable (use technical tools regularly)
- [ ] Moderate (can follow instructions)
- [ ] Prefer GUI (avoid CLI when possible)

### 10.2 Dependencies and Installation

**Q10.2.1**: Are you comfortable installing and managing:
- [ ] Node.js and npm packages
- [ ] Python and pip packages
- [ ] Git and git-crypt
- [ ] Claude API key setup
- [ ] All of the above
- [ ] Prefer minimal dependencies

**Q10.2.2**: What installation method do you prefer?
- [ ] npm install (Node.js package)
- [ ] pip install (Python package)
- [ ] Binary download (no language runtime needed)
- [ ] Docker container
- [ ] Git clone and manual setup
- [ ] No preference

### 10.3 Performance and Cost

**Q10.3.1**: How important is response generation speed?
- [ ] Critical (must be near-instant)
- [ ] Important (within a few seconds is fine)
- [ ] Low priority (happy to wait 30+ seconds for quality)

**Q10.3.2**: What's your Claude API usage budget comfort level?
- [ ] Cost-sensitive (minimize API calls, use Haiku when possible)
- [ ] Moderate (balance cost and quality)
- [ ] Cost not a concern (use best model for each task)

**Q10.3.3**: Would you want the system to estimate API costs before running expensive operations?
- [ ] Yes, always show estimated cost
- [ ] Yes, for operations over $X (specify): _______________
- [ ] No, don't show costs

---

## Completion

**Thank you for taking the time to complete this questionnaire!**

Your responses will be invaluable in designing a v2 system that truly fits your workflow and provides maximum value.

### Next Steps

1. **Review your answers** - Take a moment to review and ensure all critical information is captured
2. **Add any additional notes** - Feel free to add context anywhere
3. **Highlight priorities** - Mark or annotate which features/capabilities are most important
4. **Share feedback** - Return this document so we can refine the design

### Additional Notes/Comments

```
[Add any additional thoughts, concerns, or ideas here]
```

---

**Document Status**: ⏳ Awaiting User Completion
**Created**: 2025-12-09
**Last Updated**: 2025-12-09
