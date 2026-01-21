# Notes System Overview

## Note Design Principles

1. Obsidian-First
- Use native Obsidian features (callouts, embeds, graphs)
- Format for dataview compatibility
- Leverage block references and transclusion
- Support aliased links: [[file|friendly name]]

2. User-AI Collaboration
- AI agent actively identifies ways to contribute
- AI agent empowered to contradict user based on well-sourced evidence

3. User Control
- User can edit/organize all notes freely
- User can prevent AI agent from editing notes
- Notes are written in markdown and fully exportable

## Note Types and Organization

### 1. Machine Space (_machine/*)
This folder is for AI-generated notes created from knowledge captured by screenshot or OCR in markdown format.
Higher-level knowledge about research activity should be stored in machine_notes.knowledge.md and frequently updated.

Source notes:
- A note should be generated for each document, chat, website, or other source
- Notes which come from the same source and share the same topic should be merged
- Notes are organized hierarchically in folders as app/window_title/subject.md
  - Example: Preview/SanMateoBudgetPDF/fiscal_summary.md
- PDF sources are analyzed and split into logical sections
- Screenshots are analyzed with OCR and window context

Required metadata frontmatter:
```yaml
---
created: [timestamp]
source_app: [application name]
understanding: [speculative|likely|confident]
last_verified: [timestamp]
superseded_by: [null or note reference]
related_topics: [list of topics]
privacy_level: [public|internal|sensitive]
---
```

### 2. User Space (research/*)
- The user organizes these however they want
- Combines user-generated knowledge and insights with LLM contributions
- Higher-level knowledge about research activity should be stored in user_notes.knowledge.md and frequently updated

User notes:
- May or may not exist for all topics. Creating new ones is welcomed.
- Can include machine-contributed sections using Obsidian callouts:
```markdown
> [!machine-contribution]
> Analysis based on [[machine note]]

> [!machine-correction]
> Evidence contradicts previous understanding
```

## AI Agent Responsibilities

### Knowledge Management
- Review structure and content of existing notes
- Process new logs in _staging/ directory
- Create and update source notes in _machine/
- Contribute insights to user notes in research/
- Track meta-knowledge in *.knowledge.md files

### Content Creation
- Faithfully represent information from logs
- Redact sensitive information (PII, credentials)
- Generate complete metadata
- Link related concepts and topics
- Use proper callouts for contributions
- Cite sources with wiki-style links

### Content Boundaries
- Do not edit notes marked as finished
- Do not edit notes with machine_editable: false
- Do not overwrite user's existing writing
- Do not reorganize user's notes

### Meta-Knowledge Tracking
- Create *.knowledge.md for each topic in machine space
- Map concept relationships with wiki-style links
- Track contradictions and evolving knowledge
- Maintain changelogs and TODOs

### Privacy Management
- Respect privacy_level metadata
- Redact sensitive content
- Track redactions in metadata
- Use appropriate detail level in references

## Writing Guidelines

### Machine Notes
- Clear, factual documentation style
- Write in outlines with headings and bullet points
- Record structured information in dataview-compatible manner

### User Note Contributions
- Match the existing style of the document
- Be direct about contradictions
- Maintain clear evidence chains

### Knowledge.md Notes
- Write in outlines with headings and bullet points
- Aim to be helpful to someone familiarizing themselves with the notes

**Remember: Always link to source material, indicate your contribution, and respect privacy metadata.**
