# CHOSEN - Interface Design Specification

**Created**: 2025-12-09
**Status**: Draft - Comprehensive Design
**Purpose**: Complete interface design for CHOSEN

---

## Table of Contents

1. [Design System](#1-design-system)
2. [Layout Architecture](#2-layout-architecture)
3. [Core Views](#3-core-views)
4. [Interactive Components](#4-interactive-components)
5. [State Management](#5-state-management)
6. [Animations & Transitions](#6-animations--transitions)
7. [Accessibility](#7-accessibility)
8. [Mobile Considerations](#8-mobile-considerations)
9. [Implementation Strategy](#9-implementation-strategy)

---

## 1. Design System

### 1.1 Color Palette

#### Light Mode

**Primary Colors**:
```
Primary Brand:     #2563EB (Blue 600)  - Main actions, links
Primary Hover:     #1D4ED8 (Blue 700)  - Hover states
Primary Light:     #DBEAFE (Blue 100)  - Backgrounds, highlights
Primary Dark:      #1E40AF (Blue 800)  - Text emphasis
```

**Semantic Colors**:
```
Success:           #10B981 (Green 500)  - Positive actions, completed
Success Light:     #D1FAE5 (Green 100)  - Success backgrounds
Warning:           #F59E0B (Amber 500)  - Warnings, pending actions
Warning Light:     #FEF3C7 (Amber 100)  - Warning backgrounds
Error:             #EF4444 (Red 500)    - Errors, rejections
Error Light:       #FEE2E2 (Red 100)    - Error backgrounds
Info:              #3B82F6 (Blue 500)   - Information
Info Light:        #DBEAFE (Blue 100)   - Info backgrounds
```

**Neutrals**:
```
Background:        #FFFFFF (White)      - Main background
Surface:           #F9FAFB (Gray 50)    - Cards, panels
Surface Alt:       #F3F4F6 (Gray 100)   - Alternate surfaces
Border:            #E5E7EB (Gray 200)   - Dividers, borders
Border Dark:       #D1D5DB (Gray 300)   - Strong borders
Text Primary:      #111827 (Gray 900)   - Primary text
Text Secondary:    #6B7280 (Gray 500)   - Secondary text
Text Tertiary:     #9CA3AF (Gray 400)   - Tertiary text
```

#### Dark Mode

**Primary Colors**:
```
Primary Brand:     #60A5FA (Blue 400)   - Main actions, links
Primary Hover:     #3B82F6 (Blue 500)   - Hover states
Primary Light:     #1E3A8A (Blue 900)   - Backgrounds, highlights
Primary Dark:      #93C5FD (Blue 300)   - Text emphasis
```

**Semantic Colors**:
```
Success:           #34D399 (Green 400)  - Positive actions
Success Light:     #064E3B (Green 900)  - Success backgrounds
Warning:           #FBBF24 (Amber 400)  - Warnings
Warning Light:     #78350F (Amber 900)  - Warning backgrounds
Error:             #F87171 (Red 400)    - Errors
Error Light:       #7F1D1D (Red 900)    - Error backgrounds
Info:              #60A5FA (Blue 400)   - Information
Info Light:        #1E3A8A (Blue 900)   - Info backgrounds
```

**Neutrals**:
```
Background:        #0F172A (Slate 900)  - Main background
Surface:           #1E293B (Slate 800)  - Cards, panels
Surface Alt:       #334155 (Slate 700)  - Alternate surfaces
Border:            #475569 (Slate 600)  - Dividers, borders
Border Dark:       #64748B (Slate 500)  - Strong borders
Text Primary:      #F1F5F9 (Slate 100)  - Primary text
Text Secondary:    #94A3B8 (Slate 400)  - Secondary text
Text Tertiary:     #64748B (Slate 500)  - Tertiary text
```

### 1.2 Typography Scale

**Font Families**:
```css
/* Sans-serif for UI */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Monospace for code, data */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

/* Serif for content (optional) */
--font-serif: 'Georgia', 'Times New Roman', serif;
```

**Type Scale**:
```css
/* Display - Large headings */
--text-display-2xl: 4.5rem;    /* 72px */ line-height: 1;
--text-display-xl:  3.75rem;   /* 60px */ line-height: 1;
--text-display-lg:  3rem;      /* 48px */ line-height: 1;

/* Headings */
--text-h1:  2.25rem;  /* 36px */ line-height: 1.2;
--text-h2:  1.875rem; /* 30px */ line-height: 1.3;
--text-h3:  1.5rem;   /* 24px */ line-height: 1.3;
--text-h4:  1.25rem;  /* 20px */ line-height: 1.4;

/* Body */
--text-lg:  1.125rem; /* 18px */ line-height: 1.6;
--text-base:1rem;     /* 16px */ line-height: 1.5;
--text-sm:  0.875rem; /* 14px */ line-height: 1.5;
--text-xs:  0.75rem;  /* 12px */ line-height: 1.4;

/* Weights */
--font-light:   300;
--font-normal:  400;
--font-medium:  500;
--font-semibold:600;
--font-bold:    700;
```

### 1.3 Spacing System

**Base Unit**: 4px (0.25rem)

```css
--space-0:   0;
--space-1:   0.25rem;  /* 4px */
--space-2:   0.5rem;   /* 8px */
--space-3:   0.75rem;  /* 12px */
--space-4:   1rem;     /* 16px */
--space-5:   1.25rem;  /* 20px */
--space-6:   1.5rem;   /* 24px */
--space-8:   2rem;     /* 32px */
--space-10:  2.5rem;   /* 40px */
--space-12:  3rem;     /* 48px */
--space-16:  4rem;     /* 64px */
--space-20:  5rem;     /* 80px */
--space-24:  6rem;     /* 96px */
```

### 1.4 Component Library (shadcn/ui customizations)

#### Base Components

**Button Variants**:
```
1. Primary:   Solid background, white text (main actions)
2. Secondary: Outlined, colored border (secondary actions)
3. Ghost:     Transparent, hover background (subtle actions)
4. Danger:    Red variant (destructive actions)
5. Link:      Text only, underline on hover (navigation)
```

**Card Styles**:
```
1. Default:   White/surface background, subtle border
2. Elevated:  Drop shadow, no border
3. Outlined:  Border emphasis, no shadow
4. Filled:    Colored background for status
```

**Input Styles**:
```
1. Default:   Border-based, focus ring
2. Filled:    Background-based, no border
3. Inline:    Borderless until focus
```

#### Custom Components

**Status Badge**:
```tsx
// Visual representation of conversation status
<Badge variant="success|warning|error|info|neutral">
  {statusText}
</Badge>
```

**Sentiment Indicator**:
```tsx
// Shows conversation sentiment trend
<SentimentIndicator
  current="positive|neutral|negative"
  trend="improving|stable|declining"
/>
```

**Score Display**:
```tsx
// Visual representation of fit score
<ScoreDisplay
  score={85}
  breakdown={categoryScores}
  max={100}
/>
```

### 1.5 Icon Set

**Primary Icons**: Lucide Icons (consistent, open-source, tree-shakeable)

**Key Icons Mapping**:
```
Navigation:
- Home:              Home
- Inbox:             Inbox
- Analytics:         BarChart3
- Settings:          Settings

Actions:
- Compose:           PenSquare
- Send:              Send
- Edit:              Edit2
- Delete:            Trash2
- Archive:           Archive
- Star/Favorite:     Star
- Filter:            Filter
- Search:            Search
- Refresh:           RefreshCw

Status:
- New:               CircleDot
- In Progress:       Clock
- Completed:         CheckCircle2
- Rejected:          XCircle
- Warning:           AlertTriangle

Communication:
- Email:             Mail
- LinkedIn:          Linkedin
- Phone:             Phone
- Calendar:          Calendar

Analysis:
- Sentiment Up:      TrendingUp
- Sentiment Down:    TrendingDown
- Sentiment Flat:    Minus
- Info:              Info
- Help:              HelpCircle

Expand/Collapse:
- Expand:            ChevronDown
- Collapse:          ChevronUp
- Next:              ChevronRight
- Previous:          ChevronLeft
```

---

## 2. Layout Architecture

### 2.1 Main App Shell Structure

```
┌─────────────────────────────────────────────────────────────┐
│ Top Navigation Bar (Fixed)                           [User] │
├───────────┬─────────────────────────────────────────────────┤
│           │                                                 │
│           │                                                 │
│  Sidebar  │          Main Content Area                      │
│  (Fixed)  │          (Scrollable)                           │
│           │                                                 │
│           │                                                 │
│           │                                                 │
│           │                                                 │
│           │                                                 │
└───────────┴─────────────────────────────────────────────────┘
```

#### Top Navigation Bar (60px height)

```
┌─────────────────────────────────────────────────────────────┐
│ [Logo]  AI Message Writer    [Search...]      [🔔] [👤]    │
└─────────────────────────────────────────────────────────────┘
```

**Elements**:
1. Logo + App Name (left)
2. Global Search (center-left, expandable)
3. Notifications Badge (right)
4. User Menu (right)

#### Sidebar (240px width, collapsible to 64px)

```
┌──────────────┐
│              │
│ [Home]       │  ← Navigation Items
│ [Inbox] (5)  │  ← Badge shows unread count
│ [Analytics]  │
│ [Settings]   │
│              │
│ ─────────── │
│              │
│ SHORTCUTS    │
│ Company A    │  ← Quick access to pinned conversations
│ Company B    │
│              │
│ ─────────── │
│              │
│ [+ Quick]    │  ← Quick compose button
│              │
└──────────────┘
```

**Collapsible State**:
```
┌────┐
│ 🏠 │  ← Icon only
│ 📥 │
│ 📊 │
│ ⚙️  │
│    │
│ ── │
│    │
│ A  │  ← First letter
│ B  │
│    │
└────┘
```

### 2.2 Responsive Breakpoints

```css
/* Mobile */
--breakpoint-xs: 0px;       /* 0 - 639px */
--breakpoint-sm: 640px;     /* 640px - 767px */

/* Tablet */
--breakpoint-md: 768px;     /* 768px - 1023px */
--breakpoint-lg: 1024px;    /* 1024px - 1279px */

/* Desktop */
--breakpoint-xl: 1280px;    /* 1280px - 1535px */
--breakpoint-2xl: 1536px;   /* 1536px+ */
```

**Responsive Behavior**:

```
Mobile (< 768px):
- Sidebar: Hidden by default, overlay when opened
- Top Nav: Hamburger menu, search icon
- Main: Full width

Tablet (768px - 1024px):
- Sidebar: Collapsible, icons only by default
- Top Nav: Full search bar
- Main: Full width minus sidebar

Desktop (> 1024px):
- Sidebar: Expanded by default
- Top Nav: Full features
- Main: Content centered with max-width or split view
```

### 2.3 Grid System

**12-Column Grid** for complex layouts:
```
┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
│  │  │  │  │  │  │  │  │  │  │  │  │
└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
```

**Common Layouts**:

1. **Split View (8-4)**:
```
┌──────────────────┬─────────┐
│  Main Content    │ Sidebar │
│  (8 columns)     │ (4 col) │
└──────────────────┴─────────┘
```

2. **Centered Content**:
```
┌────────────────────────┐
│    Max-width: 960px    │
│    Centered            │
└────────────────────────┘
```

3. **Three Panel (3-6-3)**:
```
┌─────┬────────────┬─────┐
│ Nav │   Main     │Info │
└─────┴────────────┴─────┘
```

---

## 3. Core Views

### 3.1 Inbox View

**Purpose**: Browse and manage all recruiter conversations.

#### Wireframe

```
┌──────────────────────────────────────────────────────────────────────┐
│ Inbox                                           [Filter ▾] [+ New]   │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ ┌─────────────────────┐  ┌───────────────────────────────────────┐ │
│ │  Filters & Status   │  │  Conversation List                     │ │
│ │                     │  │                                         │ │
│ │ All (23)            │  │  ┌─────────────────────────────────┐  │ │
│ │ Active (12)         │  │  │ ●  TechCorp - Sarah M.          │  │ │
│ │ Awaiting (5)        │  │  │    Senior Engineer Role         │  │ │
│ │ Interview (3)       │  │  │    Following up on interview... │  │ │
│ │ Offer (1)           │  │  │    2 hours ago    📧    ⭐      │  │ │
│ │ Archived (45)       │  │  └─────────────────────────────────┘  │ │
│ │                     │  │                                         │ │
│ │ PLATFORMS           │  │  ┌─────────────────────────────────┐  │ │
│ │ □ LinkedIn          │  │  │    StartupXYZ - John D.         │  │ │
│ │ □ Email             │  │  │    Full-Stack Position          │  │ │
│ │                     │  │  │    Thanks for your interest...  │  │ │
│ │ TIMING              │  │  │    Yesterday      💼            │  │ │
│ │ □ Needs Follow-up   │  │  └─────────────────────────────────┘  │ │
│ │ □ Overdue           │  │                                         │ │
│ │                     │  │  ┌─────────────────────────────────┐  │ │
│ │ FIT SCORE           │  │  │    BigCo - Michael R.           │  │ │
│ │ ●──────○────── 80%  │  │  │    Staff Engineer Opportunity   │  │ │
│ │                     │  │  │    Compensation discussion...    │  │ │
│ │                     │  │  │    3 days ago     💬    🚀      │  │ │
│ └─────────────────────┘  └───────────────────────────────────────┘ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

#### Components Breakdown

**Filter Sidebar** (240px width):
```
┌──────────────────────┐
│ STAGE                │
│ ☑ All (23)           │  ← Radio/Checkbox groups
│ ☐ Active (12)        │
│ ☐ Awaiting (5)       │
│ ☐ Interview (3)      │
│ ☐ Offer (1)          │
│ ☐ Archived (45)      │
│                      │
│ PLATFORMS            │
│ ☐ LinkedIn (15)      │
│ ☐ Email (8)          │
│                      │
│ TIMING               │
│ ☐ Needs Follow-up (7)│
│ ☐ Overdue (2)        │
│ ☐ Recent (5)         │
│                      │
│ FIT SCORE            │
│ ●──────○────── 80%   │  ← Range slider
│                      │
│ COMPANY              │
│ [Search companies]   │  ← Autocomplete
│                      │
│ [Clear Filters]      │
└──────────────────────┘
```

**Conversation List Item**:
```
┌─────────────────────────────────────────────────────────┐
│ ●  [Company] - [Recruiter Name]          [Actions ⋮]    │  ← Status dot, star, menu
│    [Role Title]                          [Platform Icon] │
│    [Message Preview...]                  [Metadata]      │
│    [Timestamp]  [Tags]  [Quick Actions]                 │
└─────────────────────────────────────────────────────────┘

Status Dot Colors:
● Green:  Active, positive sentiment
● Yellow: Awaiting response, neutral
● Red:    Problem, negative
● Blue:   New, unread
● Gray:   Archived, completed
```

**Top Action Bar**:
```
┌─────────────────────────────────────────────────────────┐
│ Inbox                    [Filter ▾]  [Sort ▾]  [+ New]  │
│ [Search conversations...]                      [⚙️View]  │
└─────────────────────────────────────────────────────────┘
```

**Empty State**:
```
┌─────────────────────────────────────────┐
│                                         │
│             📭                          │
│                                         │
│    No conversations yet                 │
│                                         │
│    Start by importing a recruiter       │
│    message or composing a new one       │
│                                         │
│    [Import Message]  [+ New Message]    │
│                                         │
└─────────────────────────────────────────┘
```

### 3.2 Conversation View

**Purpose**: View full conversation thread, analysis, and compose responses.

#### Wireframe

```
┌────────────────────────────────────────────────────────────────────────────────┐
│ ← Back   TechCorp - Sarah Martinez                          [Actions ▾]        │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│ ┌────────────────────────────────────┐  ┌──────────────────────────────────┐ │
│ │  Thread History                    │  │  Context Panel                   │ │
│ │                                    │  │                                  │ │
│ │  Sarah M. (TechCorp)               │  │  STATUS                          │ │
│ │  Monday, 2:34 PM                   │  │  ●  Interviewing                 │ │
│ │  ┌────────────────────────────┐    │  │                                  │ │
│ │  │ Hi! I came across your     │    │  │  FIT SCORE                       │ │
│ │  │ profile and think you'd be │    │  │  ████████── 85%  Excellent       │ │
│ │  │ a great fit for...         │    │  │                                  │ │
│ │  └────────────────────────────┘    │  │  SENTIMENT                       │ │
│ │                                    │  │  📈 Positive & Improving         │ │
│ │  You (Candidate)                   │  │                                  │ │
│ │  Monday, 4:15 PM                   │  │  NEXT ACTION                     │ │
│ │  ┌────────────────────────────┐    │  │  Follow up in 2-3 days          │ │
│ │  │ Thanks for reaching out!   │    │  │                                  │ │
│ │  │ I'd love to learn more...  │    │  │  ──────────────                  │ │
│ │  └────────────────────────────┘    │  │                                  │ │
│ │                                    │  │  COMPANY                         │ │
│ │  Sarah M. (TechCorp)               │  │  TechCorp                        │ │
│ │  Tuesday, 10:22 AM                 │  │  Series B Startup                │ │
│ │  ┌────────────────────────────┐    │  │  200-500 employees               │ │
│ │  │ Great! Let's schedule a    │    │  │  [Research Notes]                │ │
│ │  │ call for this Friday...    │    │  │                                  │ │
│ │  └────────────────────────────┘    │  │  ROLE                            │ │
│ │                                    │  │  Senior Software Engineer        │ │
│ │  [Compose Response]                │  │  Full-time, Remote               │ │
│ │                                    │  │  [View JD Analysis]              │ │
│ └────────────────────────────────────┘  │                                  │ │
│                                         │  TIMELINE                        │ │
│                                         │  ┌──────────────────────┐        │ │
│                                         │  │ Dec 5: Initial reach │        │ │
│                                         │  │ Dec 6: Expressed int │        │ │
│                                         │  │ Dec 7: Call scheduled│        │ │
│                                         │  └──────────────────────┘        │ │
│                                         └──────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────┘
```

#### Components Breakdown

**Message Bubble**:
```
Recruiter Message:
┌─────────────────────────────────────────┐
│ Sarah M. (TechCorp Recruiting)          │  ← Sender
│ Monday at 2:34 PM · via LinkedIn        │  ← Timestamp + Platform
│                                         │
│ Hi João,                                │  ← Message body
│                                         │     (formatted, links)
│ I came across your profile and think    │
│ you'd be a great fit for our Senior     │
│ Software Engineer role...               │
│                                         │
│ [Attachment: job-description.pdf]       │  ← Optional attachment
│                                         │
│ [Quick Reply] [Generate Response]       │  ← Action buttons
└─────────────────────────────────────────┘

Candidate Message:
                  ┌─────────────────────────────────────┐
                  │ You (Candidate)                     │
                  │ Monday at 4:15 PM · via LinkedIn    │
                  │                                     │
                  │ Hi Sarah,                           │
                  │                                     │
                  │ Thanks for reaching out! I'd love   │
                  │ to learn more about the role...     │
                  │                                     │
                  │ [Edit] [Mark Important]             │
                  └─────────────────────────────────────┘
```

**Context Panel Sections**:

1. **Status & Metrics**:
```
┌─────────────────────────────┐
│ STATUS                      │
│ ●  Interviewing             │  ← Current stage
│ [Change Status ▾]           │
│                             │
│ FIT SCORE                   │
│ ████████── 85%              │  ← Visual bar
│ Excellent match             │
│ [View Breakdown]            │
│                             │
│ SENTIMENT                   │
│ 📈 Positive & Improving     │  ← Trend indicator
│ [Analysis Details]          │
└─────────────────────────────┘
```

2. **Next Actions**:
```
┌─────────────────────────────┐
│ NEXT ACTION                 │
│ ⏰ Follow up in 2-3 days    │
│                             │
│ PENDING                     │
│ □ Send availability         │  ← Checklist
│ □ Research company          │
│ ☑ Prepare questions         │
└─────────────────────────────┘
```

3. **Entity Info**:
```
┌─────────────────────────────┐
│ COMPANY                     │
│ TechCorp                    │
│ Series B Startup            │
│ 200-500 employees           │
│ San Francisco, CA (Remote)  │
│                             │
│ [View Research Notes]       │  ← Expandable
│ [Glassdoor] [LinkedIn]      │  ← External links
│                             │
│ ROLE                        │
│ Senior Software Engineer    │
│ Full-time · Remote          │
│ $150-180k + equity          │
│                             │
│ [View Full JD]              │
│ [View Fit Analysis]         │
└─────────────────────────────┘
```

### 3.3 Compose Panel

**Purpose**: Create or edit message responses with AI assistance.

#### Wireframe - Expanded Compose

```
┌────────────────────────────────────────────────────────────────────┐
│ Compose Response                                       [✕ Close]    │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ TO: Sarah Martinez <sarah.m@techcorp.com>                         │
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐│
│ │ RESPONSE DRAFT                                      [Quality: A]││
│ │                                                                 ││
│ │ Hi Sarah,                                                       ││
│ │                                                                 ││
│ │ Thanks for following up! I'm definitely interested in          ││
│ │ discussing the Senior Software Engineer role further.          ││
│ │                                                                 ││
│ │ For Friday's call, I'm available:                              ││
│ │ - 10:00 AM - 12:00 PM PST                                      ││
│ │ - 2:00 PM - 4:00 PM PST                                        ││
│ │                                                                 ││
│ │ Before our call, could you share more about the team           ││
│ │ structure and tech stack?                                      ││
│ │                                                                 ││
│ │ Looking forward to speaking with you.                          ││
│ │                                                                 ││
│ │ Best,                                                           ││
│ │ João                                                            ││
│ │                                                                 ││
│ └────────────────────────────────────────────────────────────────┘│
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐│
│ │ 💡 AI SUGGESTIONS                                   [Hide ▴]   ││
│ │                                                                 ││
│ │ ✓ Tone: Professional and enthusiastic (appropriate)            ││
│ │ ✓ Length: 112 words (optimal for this stage)                  ││
│ │ ⚠️ Consider: Mentioning H1B sponsorship requirement            ││
│ │ ℹ️  Timing: Best sent between 2-4 PM today                     ││
│ │                                                                 ││
│ │ [Apply Suggestions] [Regenerate] [Alternative Version]         ││
│ └────────────────────────────────────────────────────────────────┘│
│                                                                    │
│ ┌────────────────────────────────────────────────────────────────┐│
│ │ AGENT REASONING                                     [Show ▾]   ││
│ └────────────────────────────────────────────────────────────────┘│
│                                                                    │
│ [Template ▾] [Model ▾]           [Save Draft] [Copy] [Send →]    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

#### Components Breakdown

**Editor Toolbar**:
```
┌──────────────────────────────────────────────────────────────┐
│ [B] [I] [U] [Link] | [Bullets] [Numbers] | [⚡ Quick Reply] │
└──────────────────────────────────────────────────────────────┘
```

**Quick Actions Panel**:
```
┌─────────────────────────────────────────┐
│ QUICK REPLIES                           │
│ [✓ Express Interest]                    │  ← Pre-built templates
│ [? Request Info]                        │
│ [📅 Schedule Interview]                 │
│ [👋 Polite Decline]                     │
│ [⏰ Follow-up]                          │
└─────────────────────────────────────────┘
```

**Quality Assessment Display**:
```
┌─────────────────────────────────────────┐
│ RESPONSE QUALITY              Score: A   │
│                                         │
│ Grammar & Spelling        ✓ Excellent   │
│ Tone Appropriateness      ✓ Excellent   │
│ Strategic Alignment       ✓ Good        │
│ Completeness             ⚠️  Missing info│
│                                         │
│ [View Full Analysis]                    │
└─────────────────────────────────────────┘
```

**Timing Recommendation**:
```
┌─────────────────────────────────────────┐
│ ⏰ TIMING RECOMMENDATION                │
│                                         │
│ Ideal timing:                           │
│ Today, 2:00 PM - 4:00 PM PST           │
│                                         │
│ Why: Professional hours, matches        │
│ recruiter's active time pattern         │
│                                         │
│ [Schedule Send]  [Send Now]            │
└─────────────────────────────────────────┘
```

### 3.4 Settings View

**Purpose**: Configure user profile, resumes, signatures, and system preferences.

#### Wireframe

```
┌────────────────────────────────────────────────────────────────────┐
│ Settings                                                           │
├─────────────────┬──────────────────────────────────────────────────┤
│                 │                                                  │
│ Profile         │  PROFILE INFORMATION                             │
│ Resumes         │                                                  │
│ Signatures      │  Name                                            │
│ Preferences     │  [João da Silva]                                 │
│ Notifications   │                                                  │
│ Data & Privacy  │  Email                                           │
│ Integrations    │  [joao@example.com]                              │
│ API Keys        │                                                  │
│                 │  LinkedIn URL                                    │
│                 │  [linkedin.com/in/joaodasilva]                   │
│                 │                                                  │
│                 │  VISA STATUS                                     │
│                 │  ☑ Require H1B Sponsorship                       │
│                 │  Current Status: [H1B ▾]                         │
│                 │                                                  │
│                 │  JOB SEARCH MODE                                 │
│                 │  ○ Passive  ● Active  ○ Not Looking              │
│                 │                                                  │
│                 │  TARGET ROLES                                    │
│                 │  [+ Add Role]                                    │
│                 │  • Senior Software Engineer                      │
│                 │  • Staff Software Engineer                       │
│                 │                                                  │
│                 │  [Save Changes]                                  │
│                 │                                                  │
└─────────────────┴──────────────────────────────────────────────────┘
```

#### Settings Sections

**1. Profile Tab**:
```
┌──────────────────────────────────────────┐
│ PROFILE INFORMATION                      │
│ Name:          [João da Silva]           │
│ Email:         [joao@example.com]        │
│ LinkedIn:      [linkedin.com/in/...]     │
│ Location:      [San Francisco, CA ▾]     │
│                                          │
│ VISA STATUS                              │
│ ☑ Require H1B Sponsorship                │
│ Current: [H1B ▾]                         │
│                                          │
│ JOB SEARCH                               │
│ Mode: ○ Passive ● Active ○ Not Looking  │
│                                          │
│ Target Roles:                            │
│ • Senior Software Engineer               │
│ • Staff Software Engineer                │
│ [+ Add]                                  │
│                                          │
│ [Save]                                   │
└──────────────────────────────────────────┘
```

**2. Resumes Tab**:
```
┌──────────────────────────────────────────┐
│ MY RESUMES                    [+ Upload] │
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │ ⭐ General_Resume_2024.pdf            │ │
│ │    Last updated: Dec 1, 2024         │ │
│ │    [View] [Edit] [Download] [Delete] │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │    Senior_Engineer_Resume.pdf        │ │
│ │    Last updated: Nov 15, 2024        │ │
│ │    [View] [Edit] [Download] [Delete] │ │
│ └──────────────────────────────────────┘ │
│                                          │
│ DEFAULT RESUME                           │
│ [General_Resume_2024.pdf ▾]              │
│                                          │
│ HIDDEN SECTIONS                          │
│ ☑ Include commented lines in analysis   │
│   (for gap assessment)                   │
│                                          │
└──────────────────────────────────────────┘
```

**3. Signatures Tab**:
```
┌──────────────────────────────────────────┐
│ EMAIL SIGNATURE                          │
│ ┌──────────────────────────────────────┐ │
│ │ Best regards,                        │ │
│ │ João da Silva                        │ │
│ │ Senior Software Engineer             │ │
│ │ joao@example.com                     │ │
│ └──────────────────────────────────────┘ │
│ [Edit]                                   │
│                                          │
│ LINKEDIN SIGNATURE                       │
│ ┌──────────────────────────────────────┐ │
│ │ Best,                                │ │
│ │ João                                 │ │
│ └──────────────────────────────────────┘ │
│ [Edit]                                   │
│                                          │
│ PLATFORM DEFAULTS                        │
│ Email:    [Use Email Signature]          │
│ LinkedIn: [Use LinkedIn Signature]       │
│                                          │
│ [Save]                                   │
└──────────────────────────────────────────┘
```

**4. Preferences Tab**:
```
┌──────────────────────────────────────────┐
│ COMPENSATION EXPECTATIONS                │
│                                          │
│ Full-Time (Yearly)                       │
│ Minimum:  [$150,000]                     │
│ Target:   [$180,000]                     │
│ Display:  "$180k+"                       │
│                                          │
│ Contract (Hourly)                        │
│ Minimum:  [$85/hr]                       │
│ Target:   [$100/hr]                      │
│ Display:  "$100+/hr"                     │
│                                          │
│ RESPONSE PREFERENCES                     │
│ Default tone: [Professional ▾]           │
│ Auto-analyze: ☑ Yes                      │
│ Show reasoning: ☑ Always                 │
│                                          │
│ TIMING PREFERENCES                       │
│ Work hours: [9 AM] to [6 PM] [PST ▾]    │
│ Avoid weekends: ☑ Yes                    │
│                                          │
│ [Save]                                   │
└──────────────────────────────────────────┘
```

---

## 4. Interactive Components

### 4.1 Agent Transparency Viewer

**Purpose**: Show AI reasoning process in an understandable, collapsible format.

#### Component Structure

```
┌─────────────────────────────────────────────────────────────┐
│ 🤖 AGENT REASONING                          [Hide ▴] [Copy] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ▶ Conversation History Analysis                            │  ← Collapsible sections
│                                                             │
│ ▼ Job Position Fit Analysis                                │
│   ┌───────────────────────────────────────────────────┐   │
│   │ Required Skills (AND logic):                      │   │
│   │ ✓ Python (3 years) - Match                       │   │
│   │ ✓ React (2 years) - Match                        │   │
│   │ ✓ System Design - Match                          │   │
│   │ ⚠️ Kubernetes - Partial (some experience)         │   │
│   │                                                   │   │
│   │ Preferred Skills (OR logic):                      │   │
│   │ ✓ AWS - Match                                     │   │
│   │ ✗ GCP - No match                                  │   │
│   │ ✓ Docker - Match                                  │   │
│   │                                                   │   │
│   │ Calculated Fit Score: 85/100                      │   │
│   └───────────────────────────────────────────────────┘   │
│                                                             │
│ ▶ Knowledge Gap Analysis                                   │
│                                                             │
│ ▼ Response Timing Strategy                                 │
│   ┌───────────────────────────────────────────────────┐   │
│   │ Last message from recruiter: 2 days ago           │   │
│   │ Recruiter's avg response time: 8 hours           │   │
│   │ Conversation stage: Interviewing                  │   │
│   │ Interest level: High                              │   │
│   │                                                   │   │
│   │ Recommendation: Respond within 4-6 hours          │   │
│   │ Reasoning: Shows enthusiasm without desperation   │   │
│   └───────────────────────────────────────────────────┘   │
│                                                             │
│ ▶ Response Building Strategy                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns

**Collapsed State**:
```
┌─────────────────────────────────────────────────┐
│ 🤖 Agent Reasoning                   [Show ▾]  │
└─────────────────────────────────────────────────┘
```

**Section Expand/Collapse**:
```
Click section header to toggle:
▶ Collapsed (shows only title)
▼ Expanded (shows content)
```

**Copy Functionality**:
```
[Copy] button copies all reasoning to clipboard
Format: Markdown for easy sharing
```

### 4.2 Response Editor

**Purpose**: Edit AI-generated responses with inline suggestions.

#### Component Structure

```
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE DRAFT                           [Quality: A] [⋮]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Hi Sarah,                                                   │
│                                                             │
│ Thanks for following up! I'm definitely interested in       │
│ discussing the Senior Software Engineer role further.       │
│                                                    ⚠️       │  ← Inline suggestion indicator
│                                                             │
│ For Friday's call, I'm available:                          │
│ - 10:00 AM - 12:00 PM PST                                  │
│ - 2:00 PM - 4:00 PM PST                                    │
│                                                             │
│ Before our call, could you share more about the team       │
│ structure and tech stack?                                  │
│                                                             │
│ Looking forward to speaking with you.                      │
│                                                             │
│ Best,                                                       │
│ João                                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Suggestion Popup (on ⚠️ hover/click):
┌──────────────────────────────────────────┐
│ 💡 Consider mentioning                   │
│                                          │
│ You may want to mention your H1B         │
│ sponsorship requirement at this stage    │
│                                          │
│ Suggested addition:                      │
│ "I should also mention that I'll need    │
│  H1B sponsorship for this role."         │
│                                          │
│ [Insert] [Dismiss] [Remind Later]       │
└──────────────────────────────────────────┘
```

#### Editor Features

**Inline Editing**:
- Click anywhere to edit
- Real-time character/word count
- Markdown support (optional)

**Suggestion Types**:
```
⚠️  Warning: Missing critical info
💡 Suggestion: Improvement opportunity
ℹ️  Info: Contextual information
✨ Enhancement: Tone/style improvement
```

**Toolbar Actions**:
```
[Undo] [Redo] | [Format ▾] | [✓ Check Quality] | [↻ Regenerate]
```

### 4.3 Timing Recommendation Display

**Purpose**: Show optimal response timing with visual timeline.

#### Component Structure

```
┌─────────────────────────────────────────────────────────────┐
│ ⏰ TIMING RECOMMENDATION                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ IDEAL WINDOW                                                │
│ Today, 2:00 PM - 4:00 PM PST                               │
│                                                             │
│ Timeline:                                                   │
│ ──────────■■■■──────────────────────                       │  ← Visual timeline
│ 12PM    2PM  4PM    6PM    8PM                             │
│         └──────┘                                            │
│         Optimal                                             │
│                                                             │
│ WHY THIS TIMING?                                            │
│ • Matches recruiter's active hours (10 AM - 5 PM)          │
│ • 2 days since last message (appropriate gap)              │
│ • Mid-week, mid-afternoon (high engagement)                │
│ • Avoids Monday morning and Friday afternoon               │
│                                                             │
│ ALTERNATIVES                                                │
│ ▸ Tomorrow, 10:00 AM - 12:00 PM PST                        │  ← Collapsible
│                                                             │
│ [Schedule Send]  [Send Now]  [Custom Time]                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Schedule Send Dialog

```
┌─────────────────────────────────────────┐
│ Schedule Message                   [✕]  │
├─────────────────────────────────────────┤
│                                         │
│ Date: [Dec 9, 2024 ▾]                  │
│                                         │
│ Time: [2:00 PM ▾] [PST ▾]              │
│                                         │
│ Or select preset:                       │
│ ○ Tomorrow morning (9-10 AM)            │
│ ● This afternoon (2-4 PM) ⭐           │
│ ○ Tomorrow afternoon (2-4 PM)           │
│ ○ Custom                                │
│                                         │
│ ☑ Remind me 15 min before              │
│                                         │
│ [Cancel]              [Schedule →]     │
│                                         │
└─────────────────────────────────────────┘
```

### 4.4 A/B Testing Panel

**Purpose**: Manage response variant testing and track effectiveness.

#### Component Structure

```
┌─────────────────────────────────────────────────────────────┐
│ 🧪 A/B TESTING                              [+ New Test]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ACTIVE TEST: Response Enthusiasm Level                      │
│                                                             │
│ Variant A: High Enthusiasm                  [View]         │
│ ┌─────────────────────────────────────────────────────┐   │
│ │ Conversations: 8                                     │   │
│ │ Response rate: 87.5% (7/8)                          │   │
│ │ Avg response time: 4.2 hours                        │   │
│ │ Advanced to interview: 4 (50%)                      │   │
│ └─────────────────────────────────────────────────────┘   │
│                                                             │
│ Variant B: Moderate Professional              [View]        │
│ ┌─────────────────────────────────────────────────────┐   │
│ │ Conversations: 9                                     │   │
│ │ Response rate: 77.8% (7/9)                          │   │
│ │ Avg response time: 6.8 hours                        │   │
│ │ Advanced to interview: 3 (33%)                      │   │
│ └─────────────────────────────────────────────────────┘   │
│                                                             │
│ Statistical Confidence: 68% (needs more data)               │
│                                                             │
│ PRELIMINARY INSIGHT:                                        │
│ Variant A (high enthusiasm) showing better results          │
│ Recommend continuing test until 85% confidence              │
│                                                             │
│ [View Details] [Stop Test] [Apply Winning Variant]         │
│                                                             │
│ ──────────────────────────────────────────────────────────│
│                                                             │
│ COMPLETED TESTS                                   [View All]│
│                                                             │
│ ▸ Compensation Mention Timing (Winner: Variant A)          │
│ ▸ Question Approach Style (Winner: Variant B)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Test Creation Dialog

```
┌─────────────────────────────────────────┐
│ Create A/B Test                    [✕]  │
├─────────────────────────────────────────┤
│                                         │
│ Test Name:                              │
│ [Response Enthusiasm Level]             │
│                                         │
│ What are you testing?                   │
│ ○ Tone/enthusiasm level                 │
│ ○ Response length                       │
│ ○ Timing strategy                       │
│ ○ Compensation approach                 │
│ ○ Custom                                │
│                                         │
│ VARIANT A                               │
│ Name: [High Enthusiasm]                 │
│ Template: [Select ▾]                    │
│                                         │
│ VARIANT B                               │
│ Name: [Moderate Professional]           │
│ Template: [Select ▾]                    │
│                                         │
│ Target Conversations: [10 ▾]            │
│ Success Metric: [Response Rate ▾]       │
│                                         │
│ [Cancel]                 [Start Test]  │
│                                         │
└─────────────────────────────────────────┘
```

### 4.5 Alert/Follow-up Panel

**Purpose**: Proactive notifications for actions needed.

#### Component Structure

```
┌─────────────────────────────────────────────────────────────┐
│ 🔔 ALERTS & FOLLOW-UPS                      [Mark All Read] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ URGENT (2)                                                  │
│                                                             │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ ⚠️  Offer deadline approaching                         │ │
│ │     BigCo Inc - Offer expires in 2 days                │ │
│ │     [View Offer] [Respond]                             │ │
│ │     2 hours ago                                        │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ 🔴 Follow-up overdue                                   │ │
│ │     StartupXYZ - No response for 8 days                │ │
│ │     [Draft Follow-up] [Archive]                        │ │
│ │     1 day ago                                          │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                             │
│ NEEDS ATTENTION (5)                                         │
│                                                             │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ ⏰ Follow-up recommended                               │ │
│ │     TechCorp - 3 days since last message               │ │
│ │     [Draft Follow-up] [Snooze]                         │ │
│ │     4 hours ago                                        │ │
│ └───────────────────────────────────────────────────────┘ │
│                                                             │
│ ▸ Show 4 more...                                           │
│                                                             │
│ INFORMATION (3)                                             │
│                                                             │
│ ▸ Show all...                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Alert Types & Icons

```
⚠️  Urgent:      Deadline imminent, critical action
🔴 Overdue:      Past expected follow-up time
⏰ Recommended:  Optimal follow-up window
💡 Suggestion:   Opportunity or optimization
ℹ️  Info:        FYI, non-critical update
📈 Analytics:    Insight or pattern detected
✅ Success:      Positive outcome achieved
```

#### Notification Badge

```
Sidebar icon with badge:
📥 Inbox (5)  ← Number of unread alerts
```

---

## 5. State Management

### 5.1 Component State vs Global State

#### Local Component State

**Use Cases**:
- UI-only state (dropdowns open/closed, modal visibility)
- Form inputs before submission
- Temporary editing state
- Animation/transition states
- Collapsed/expanded sections

**Examples**:
```typescript
// Compose panel visibility
const [isComposeOpen, setIsComposeOpen] = useState(false);

// Filter sidebar expansion
const [showFilters, setShowFilters] = useState(true);

// Message edit mode
const [editingMessageId, setEditingMessageId] = useState(null);
```

#### Global State (Context/Store)

**Use Cases**:
- User profile and settings
- Conversation list and data
- Current conversation context
- Authentication state
- Global alerts/notifications
- Filter and sort preferences
- Recent activity

**State Structure**:
```typescript
type GlobalState = {
  // User
  user: {
    profile: UserProfile;
    settings: UserSettings;
    preferences: Preferences;
  };

  // Conversations
  conversations: {
    list: Conversation[];
    current: Conversation | null;
    filters: ConversationFilters;
    sort: SortConfig;
  };

  // UI State
  ui: {
    sidebarCollapsed: boolean;
    theme: 'light' | 'dark';
    activeView: ViewType;
  };

  // Notifications
  alerts: Alert[];

  // Cache
  cache: {
    companies: Map<string, Company>;
    recruiters: Map<string, Recruiter>;
    analyses: Map<string, Analysis>;
  };
};
```

### 5.2 Loading States and Skeletons

#### Skeleton Components

**Conversation List Skeleton**:
```
┌─────────────────────────────────────┐
│ ▭▭▭▭▭▭▭▭▭ ▭▭▭▭▭▭▭▭               │  ← Shimmer animation
│ ▭▭▭▭▭▭▭▭▭▭▭▭▭▭                    │
│ ▭▭▭▭▭ ▭▭▭▭                        │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ ▭▭▭▭▭▭▭▭▭ ▭▭▭▭▭▭▭▭               │
│ ▭▭▭▭▭▭▭▭▭▭▭▭▭▭                    │
│ ▭▭▭▭▭ ▭▭▭▭                        │
└─────────────────────────────────────┘
```

**Conversation View Skeleton**:
```
┌───────────────────────────────────────┐
│ ▭▭▭▭▭▭▭▭ ▭▭▭▭▭▭                     │
│                                       │
│ ┌─────────────────────┐              │
│ │ ▭▭▭▭▭▭▭▭▭          │              │
│ │ ▭▭▭▭▭▭▭▭▭▭▭▭▭▭    │              │
│ │ ▭▭▭▭▭▭              │              │
│ └─────────────────────┘              │
│                                       │
└───────────────────────────────────────┘
```

#### Loading Indicators

**Inline Spinner** (for buttons):
```
[⏳ Generating...]  ← Small spinner + text
```

**Overlay Loader** (for panels):
```
┌──────────────────────────────┐
│                              │
│         ⏳                   │  ← Centered spinner
│    Analyzing conversation... │  ← Loading message
│                              │
└──────────────────────────────┘
```

**Progress Bar** (for multi-step operations):
```
Analyzing Job Description...
████████████░░░░░░░░ 60%  ← Progress bar
Step 2 of 3: Calculating fit score
```

### 5.3 Error States and Recovery UI

#### Error Display Patterns

**Inline Error** (field validation):
```
┌─────────────────────────────────────┐
│ Email                               │
│ [invalid-email@]                    │
│ ❌ Please enter a valid email       │
└─────────────────────────────────────┘
```

**Banner Error** (non-critical):
```
┌─────────────────────────────────────────────────────┐
│ ⚠️  Could not load analytics. [Retry] [Dismiss]    │
└─────────────────────────────────────────────────────┘
```

**Modal Error** (critical):
```
┌──────────────────────────────────┐
│ ❌ Error                    [✕]  │
├──────────────────────────────────┤
│                                  │
│ Failed to generate response      │
│                                  │
│ The AI service is temporarily    │
│ unavailable. Please try again.   │
│                                  │
│ Error code: API_TIMEOUT          │
│                                  │
│ [Copy Error]  [Try Again]        │
│                                  │
└──────────────────────────────────┘
```

**Empty State with Error Recovery**:
```
┌──────────────────────────────────┐
│                                  │
│         ⚠️                       │
│                                  │
│   Failed to load conversations   │
│                                  │
│   [↻ Retry]  [Contact Support]  │
│                                  │
└──────────────────────────────────┘
```

#### Error Types and Recovery

```typescript
type ErrorType =
  | 'network'        // Network connectivity issue
  | 'api_timeout'    // API request timeout
  | 'api_error'      // API returned error
  | 'validation'     // User input validation
  | 'not_found'      // Resource not found
  | 'permission'     // Authorization/permission
  | 'unknown';       // Unknown error

// Recovery actions
type RecoveryAction =
  | 'retry'          // Retry the operation
  | 'dismiss'        // Dismiss and continue
  | 'refresh'        // Refresh the page
  | 'contact_support'// Contact support
  | 'manual_fix';    // User must fix manually
```

### 5.4 Optimistic Updates

#### Pattern: Optimistic UI Updates

**Sending a message**:
```typescript
// 1. Immediately add message to UI
addMessageOptimistically(message);

// 2. Show sending indicator
message.status = 'sending';

try {
  // 3. Send to server
  await sendMessage(message);

  // 4. Update to sent
  message.status = 'sent';

} catch (error) {
  // 5. Revert on error
  message.status = 'failed';
  showRetryOption();
}
```

**Visual Feedback**:
```
┌─────────────────────────────────────┐
│ You                                 │
│ Just now · Sending...    ⏳        │  ← Sending state
│                                     │
│ Thanks for reaching out!            │
│                                     │
└─────────────────────────────────────┘

After success:
┌─────────────────────────────────────┐
│ You                                 │
│ Just now · via LinkedIn    ✓       │  ← Sent successfully
│                                     │
│ Thanks for reaching out!            │
│                                     │
└─────────────────────────────────────┘

On error:
┌─────────────────────────────────────┐
│ You                                 │
│ Just now · Failed to send   ❌     │  ← Failed state
│                                     │
│ Thanks for reaching out!            │
│                                     │
│ [Retry] [Edit] [Discard]           │  ← Recovery actions
└─────────────────────────────────────┘
```

---

## 6. Animations & Transitions

### 6.1 Agent Streaming Text Effect

**Purpose**: Simulate AI "thinking" and writing in real-time.

**Implementation**:
```
Initial state:
┌─────────────────────────────────────┐
│ ⏳ Generating response...           │
│                                     │
│ [Blinking cursor]                   │
└─────────────────────────────────────┘

Streaming (character by character):
┌─────────────────────────────────────┐
│ Hi Sarah,█                          │
│                                     │
│ Thanks for following u█             │
└─────────────────────────────────────┘

Complete:
┌─────────────────────────────────────┐
│ Hi Sarah,                           │
│                                     │
│ Thanks for following up! I'm...    │
│                                     │
│ ✓ Response generated                │
└─────────────────────────────────────┘
```

**Timing**:
- Character delay: 15-30ms (fast but readable)
- Sentence pause: 100ms
- Paragraph pause: 200ms

### 6.2 Panel Expand/Collapse

**Animation**: Smooth height transition with content fade

```
Collapsed:
┌──────────────────────────────────┐
│ Agent Reasoning         [Show ▾] │
└──────────────────────────────────┘

Expanding (200ms duration):
┌──────────────────────────────────┐
│ Agent Reasoning         [Hide ▴] │
├──────────────────────────────────┤
│ [Content fading in]              │  ← Opacity: 0 → 1
│                                  │     Height: 0 → auto
└──────────────────────────────────┘

Expanded:
┌──────────────────────────────────┐
│ Agent Reasoning         [Hide ▴] │
├──────────────────────────────────┤
│ Conversation Analysis:           │
│ • Sentiment: Positive            │
│ • Stage: Interviewing            │
│ • Recommendations: Follow up     │
└──────────────────────────────────┘
```

**CSS**:
```css
.panel-content {
  transition: max-height 0.2s ease-out, opacity 0.15s ease-out;
  overflow: hidden;
}

.panel-content.collapsed {
  max-height: 0;
  opacity: 0;
}

.panel-content.expanded {
  max-height: 1000px; /* Or calculated */
  opacity: 1;
}
```

### 6.3 Toast Notifications

**Purpose**: Non-intrusive feedback for actions.

**Positions**:
- Top-right: Success, info, warnings
- Bottom-center: Status updates
- Top-center: Critical errors

**Animation**:
```
Slide in from right (300ms):
              ┌────────────────────────┐
              │ ✓ Message sent!        │ →
              └────────────────────────┘

Stay (3-5 seconds)

Slide out to right (300ms):
┌────────────────────────┐
│ ✓ Message sent!        │ →
└────────────────────────┘
```

**Types**:
```
Success:
┌─────────────────────────────────┐
│ ✓ Message sent successfully     │
└─────────────────────────────────┘

Info:
┌─────────────────────────────────┐
│ ℹ️  Analysis complete            │
└─────────────────────────────────┘

Warning:
┌─────────────────────────────────┐
│ ⚠️  Offer deadline in 2 days     │
└─────────────────────────────────┘

Error:
┌─────────────────────────────────┐
│ ❌ Failed to send message        │
│ [Retry]                          │
└─────────────────────────────────┘
```

### 6.4 Page Transitions

**Route Change Animation**:
```
Fade out current (150ms) → Fade in new (150ms)

Total: 300ms transition between views
```

**Loading Transition**:
```
Content → Loading skeleton (fade 150ms)
Skeleton → Content (fade 150ms)
```

**Modal Transitions**:
```
Open:
- Backdrop: Fade in (200ms)
- Modal: Scale up (0.95 → 1) + Fade in (200ms)

Close:
- Modal: Scale down (1 → 0.95) + Fade out (150ms)
- Backdrop: Fade out (200ms)
```

---

## 7. Accessibility

### 7.1 Keyboard Navigation

#### Focus Management

**Tab Order**:
1. Skip to main content link (first tab)
2. Top navigation
3. Sidebar navigation
4. Main content (logical order)
5. Modals/dialogs (trap focus)

**Keyboard Shortcuts**:
```
Global:
- Ctrl/Cmd + K: Global search
- Ctrl/Cmd + N: New message
- Ctrl/Cmd + /: Keyboard shortcuts help
- Esc: Close modal/panel

Navigation:
- G then I: Go to Inbox
- G then A: Go to Analytics
- G then S: Go to Settings
- N: Next conversation
- P: Previous conversation

Actions:
- C: Compose reply
- R: Mark as read
- A: Archive conversation
- F: Follow up
- S: Star/favorite

Editor:
- Ctrl/Cmd + Enter: Send message
- Ctrl/Cmd + S: Save draft
- Ctrl/Cmd + Shift + R: Regenerate
```

**Visual Focus Indicators**:
```css
*:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: 4px;
}
```

### 7.2 Screen Reader Support

#### ARIA Labels and Roles

**Conversation List**:
```html
<nav aria-label="Conversations">
  <ul role="list">
    <li role="listitem">
      <article
        aria-label="Conversation with Sarah Martinez at TechCorp"
        aria-describedby="conv-123-meta"
      >
        <h3>TechCorp - Sarah M.</h3>
        <p id="conv-123-meta">
          Senior Engineer Role,
          Status: Interviewing,
          Last message 2 hours ago
        </p>
      </article>
    </li>
  </ul>
</nav>
```

**Status Indicators**:
```html
<span
  class="status-badge"
  role="status"
  aria-label="Conversation status: Interviewing"
>
  Interviewing
</span>
```

**Interactive Elements**:
```html
<button
  aria-label="Generate response"
  aria-describedby="gen-help"
>
  Generate
</button>
<span id="gen-help" class="sr-only">
  Uses AI to create a professional response based on conversation context
</span>
```

#### Live Regions

**Dynamic Updates**:
```html
<!-- Toast notifications -->
<div
  role="status"
  aria-live="polite"
  aria-atomic="true"
  class="toast-container"
>
  <!-- Toasts injected here -->
</div>

<!-- Loading states -->
<div
  role="status"
  aria-live="polite"
  aria-busy="true"
>
  Loading conversations...
</div>

<!-- Error announcements -->
<div
  role="alert"
  aria-live="assertive"
>
  Failed to send message. Please try again.
</div>
```

### 7.3 Focus Management

#### Modal/Dialog Focus Trap

**Pattern**:
```typescript
function trapFocus(element: HTMLElement) {
  const focusableElements = element.querySelectorAll(
    'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
  );

  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  // Focus first element when modal opens
  firstFocusable.focus();

  // Trap focus within modal
  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      } else if (!e.shiftKey && document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }
  });
}
```

#### Skip Links

**Implementation**:
```html
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<!-- Visible only on focus -->
<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: white;
  padding: 8px;
  z-index: 9999;
}

.skip-link:focus {
  top: 0;
}
</style>
```

### 7.4 Color Contrast

#### WCAG AA Compliance

**Minimum Ratios**:
- Normal text (< 18pt): 4.5:1
- Large text (≥ 18pt or 14pt bold): 3:1
- UI components: 3:1

**Tested Combinations**:
```
Light Mode:
- Text Primary (#111827) on Background (#FFFFFF): 16.2:1 ✓
- Text Secondary (#6B7280) on Background (#FFFFFF): 5.9:1 ✓
- Primary Button (#2563EB) on White: 5.3:1 ✓

Dark Mode:
- Text Primary (#F1F5F9) on Background (#0F172A): 15.8:1 ✓
- Text Secondary (#94A3B8) on Background (#0F172A): 8.3:1 ✓
- Primary Button (#60A5FA) on Dark (#1E293B): 5.1:1 ✓
```

#### Color + Icon/Text

**Never rely on color alone**:
```
❌ Bad:
Green dot = positive
Red dot = negative

✓ Good:
🟢 Active (text label + green)
🔴 Error (text label + red)
✓ Success (checkmark + green)
```

---

## 8. Mobile Considerations

### 8.1 Touch Targets

**Minimum Size**: 44x44px (iOS) / 48x48px (Android)

**Button Sizing**:
```
Desktop:
[Button]  ← 36px height, 12px padding

Mobile:
[  Button  ]  ← 48px height, 16px padding, more spacing
```

**Tap Areas**:
```
Extend tap area beyond visual button:

Visual button: 32px
┌────────┐
│  [X]   │  ← Visible
└────────┘

Tap area: 48px
┌──────────┐
│  ┌────┐  │
│  │ X  │  │  ← Actual tap target
│  └────┘  │
└──────────┘
```

### 8.2 Simplified Mobile Layout

#### Inbox View Mobile

```
┌─────────────────────────┐
│ ☰ Inbox        🔔  ⚙️   │  ← Hamburger, title, actions
├─────────────────────────┤
│ [Search...]      [Filter]│
├─────────────────────────┤
│                         │
│ ●  TechCorp - Sarah M.  │  ← Conversation cards
│    Senior Engineer...   │     (full width)
│    2 hours ago          │
│    ───────────────────  │
│                         │
│    StartupXYZ - John D. │
│    Full-Stack...        │
│    Yesterday            │
│    ───────────────────  │
│                         │
│                         │
│                         │
│                         │
└─────────────────────────┘
```

#### Conversation View Mobile

```
┌─────────────────────────┐
│ ← TechCorp - Sarah M.   │  ← Back button, title
├─────────────────────────┤
│                         │
│ Sarah M.                │  ← Message thread
│ Monday 2:34 PM          │     (full width, stacked)
│ ┌─────────────────────┐ │
│ │ Hi! I came across...│ │
│ └─────────────────────┘ │
│                         │
│             You         │
│      Monday 4:15 PM     │
│ ┌─────────────────────┐ │
│ │ Thanks for reaching │ │
│ │ out! I'd love to... │ │
│ └─────────────────────┘ │
│                         │
│ [Compose Reply ✏️]      │  ← Bottom action bar
│                         │
└─────────────────────────┘

Tap "Compose Reply":
┌─────────────────────────┐
│ Compose Reply      [✕]  │  ← Full-screen compose
├─────────────────────────┤
│                         │
│ [Message text area]     │
│                         │
│                         │
│                         │
│                         │
│                         │
│                         │
├─────────────────────────┤
│ [Send] [AI Generate]    │  ← Fixed bottom bar
└─────────────────────────┘
```

#### Mobile Navigation

**Bottom Tab Bar** (instead of sidebar):
```
┌─────────────────────────┐
│                         │
│   Main Content Area     │
│                         │
│                         │
│                         │
│                         │
├─────────────────────────┤
│ 🏠    📥    📊    ⚙️    │  ← Bottom navigation
│Home  Inbox  Stats  More │
└─────────────────────────┘
```

### 8.3 Gesture Support

#### Swipe Gestures

**Conversation List**:
```
Swipe right on item:
┌──────────────────────────────┐
│ → [Archive] TechCorp - Sara..│  ← Reveal archive action
└──────────────────────────────┘

Swipe left on item:
┌──────────────────────────────┐
│ TechCorp - Sara.. [Follow-up]←│  ← Reveal follow-up
└──────────────────────────────┘
```

**Message View**:
```
Swipe left/right:
← Previous conversation | Next conversation →
```

**Compose Panel**:
```
Swipe down: Minimize to draft
Swipe up: Expand from draft
```

#### Pull to Refresh

```
Pull down from top:
┌─────────────────────────┐
│     ↓  Release to       │  ← Pull indicator
│        refresh...       │
├─────────────────────────┤
│ Conversation list...    │
```

---

## 9. Implementation Strategy

### 9.1 Tech Stack Recommendations

#### Frontend Framework

**React + TypeScript** (Primary recommendation)
- Mature ecosystem
- Excellent TypeScript support
- Large talent pool
- Component reusability

**Alternative**: Svelte/SvelteKit
- Better performance
- Less boilerplate
- Smaller bundle size

#### UI Component Library

**shadcn/ui** (Recommended)
- Tailwind-based
- Copy-paste components (no npm dependency)
- Full customization
- TypeScript support
- Accessible by default

**Styling**: Tailwind CSS
- Utility-first
- Design system friendly
- Dark mode support
- Responsive design

#### State Management

**Phase 1**: React Context + hooks
- Built-in
- Sufficient for initial scope
- No extra dependencies

**Phase 2+**: Zustand or Jotai
- Lightweight
- TypeScript-first
- Less boilerplate than Redux

#### Routing

**React Router v6** (if web app)
- Standard solution
- Type-safe with TypeScript
- Nested routes support

**TanStack Router** (alternative)
- Type-safe routing
- Better DX
- Built-in data loading

### 9.2 Component Architecture

#### Component Hierarchy

```
App
├── Layout
│   ├── TopNav
│   │   ├── Logo
│   │   ├── GlobalSearch
│   │   └── UserMenu
│   ├── Sidebar
│   │   ├── NavItem[]
│   │   └── QuickAccessLinks[]
│   └── MainContent
│       └── [Active View]
│
├── Views
│   ├── InboxView
│   │   ├── FilterSidebar
│   │   └── ConversationList
│   │       └── ConversationCard[]
│   ├── ConversationView
│   │   ├── MessageThread
│   │   │   └── MessageBubble[]
│   │   ├── ContextPanel
│   │   │   ├── StatusDisplay
│   │   │   ├── FitScoreDisplay
│   │   │   ├── SentimentIndicator
│   │   │   └── NextActions
│   │   └── ComposePanel
│   │       ├── Editor
│   │       ├── QualityScore
│   │       ├── TimingRecommendation
│   │       └── AgentReasoning
│   ├── AnalyticsView
│   └── SettingsView
│
└── Shared Components
    ├── Button
    ├── Card
    ├── Badge
    ├── Input
    ├── Select
    ├── Modal
    ├── Toast
    ├── Skeleton
    └── ...
```

#### Atomic Design Approach

**Atoms**:
- Button, Input, Badge, Icon, etc.

**Molecules**:
- SearchBar (Input + Button)
- StatusBadge (Icon + Text + Badge)
- ScoreDisplay (Progress Bar + Label)

**Organisms**:
- ConversationCard (multiple molecules)
- MessageBubble (molecules + metadata)
- ComposePanel (editor + toolbar + actions)

**Templates**:
- InboxTemplate (layout structure)
- ConversationTemplate (layout structure)

**Pages**:
- InboxView (template + data)
- ConversationView (template + data)

### 9.3 Progressive Enhancement

#### Phase 1: Core Features (MVP)

**Must Have**:
1. Conversation list (inbox)
2. Conversation view with message thread
3. Basic compose/reply functionality
4. AI response generation (simple)
5. Basic status tracking
6. Settings (profile, preferences)

**Interface**:
- Desktop-first
- Light mode only
- Basic responsive (mobile usable)

#### Phase 2: Enhanced Intelligence

**Add**:
1. Agent transparency viewer
2. Response quality scoring
3. Fit score analysis
4. Timing recommendations
5. Follow-up alerts
6. Analytics dashboard (basic)

**Interface**:
- Dark mode
- Improved mobile layouts
- Keyboard shortcuts

#### Phase 3: Advanced Features

**Add**:
1. A/B testing
2. Multi-conversation analytics
3. Compensation negotiation flow
4. Interview prep features
5. Knowledge gap research
6. Advanced analytics

**Interface**:
- Full mobile app experience
- Advanced animations
- Gesture support
- Accessibility audit & fixes

#### Phase 4: Integrations & Polish

**Add**:
1. Email/LinkedIn import
2. Calendar integration
3. Export functionality
4. Browser extension
5. API for external tools

**Interface**:
- Performance optimization
- Animation polish
- Accessibility certification
- Internationalization (if needed)

### 9.4 Accessibility Testing Checklist

**Automated Testing**:
- [ ] axe DevTools
- [ ] Lighthouse accessibility score > 90
- [ ] WAVE evaluation

**Manual Testing**:
- [ ] Keyboard navigation (no mouse)
- [ ] Screen reader testing (NVDA/JAWS/VoiceOver)
- [ ] Color contrast verification
- [ ] Focus visible on all interactive elements
- [ ] Forms fully accessible
- [ ] Proper heading hierarchy
- [ ] Alt text for all images
- [ ] ARIA labels where needed

**User Testing**:
- [ ] Test with assistive technology users
- [ ] Gather feedback on usability
- [ ] Iterate based on findings

---

## Summary

This comprehensive interface design provides:

1. **Complete Design System**: Colors, typography, spacing, components all defined with light/dark mode support

2. **Detailed Layouts**: App shell, responsive breakpoints, grid system specified

3. **Core Views**: Wireframes and component breakdowns for Inbox, Conversation, Compose, and Settings

4. **Interactive Components**: Agent transparency, response editor, timing display, A/B testing, alerts

5. **State Management**: Clear separation of local vs global state, loading patterns, error handling

6. **Animations**: Streaming text, panel transitions, toasts, page transitions

7. **Accessibility**: Keyboard navigation, screen reader support, focus management, color contrast

8. **Mobile Design**: Touch targets, simplified layouts, gesture support

9. **Implementation Strategy**: Tech stack, component architecture, progressive enhancement phases

This design balances:
- **Professional aesthetics** with **functional clarity**
- **Rich features** with **performance**
- **Desktop power user** needs with **mobile accessibility**
- **AI transparency** with **user control**
- **Quick actions** with **thoughtful analysis**

The design supports both CLI and web interfaces, with a clear path from MVP to advanced features.
