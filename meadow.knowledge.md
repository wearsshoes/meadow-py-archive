# Meadow
A macOS menubar app that acts as an AI research assistant by analyzing your screen activity using Claude API.

## Project Mission
- Assist researchers by tracking and analyzing topic-relevant content
- Filter and analyze content based on configured research topics
- Generate detailed summaries of relevant research material
- Contribute new information to the user's existing markdown notes

## Architecture

### Core
- monitor.py
  - runs the monitoring loop and saves logs
  - captures active window or falls back to full screen
  - handles browser URL capture
  - manages screenshot lifecycle
- screenshot_analyzer.py
  - analyzes screenshots and extracts text using Vision/EasyOCR
  - filters content by topic relevance before analysis
  - integrates with Claude API for content analysis
- topic_similarity.py
  - uses sentence-transformers for embeddings
  - configurable similarity threshold
  - filters irrelevant content before API calls
- pdf_analyzer.py
  - analyzes PDFs and extracts content
- manicode_wrapper.py
  - used to create notes from analysis
  - PTY-based wrapper implementation
  - handles timeouts and process management

### UI
- menubar_app.py: UI and coordination
  - monitor continuously or analyze current screen
  - open web viewer
  - read-only access to configuration

### Web
- web_viewer.py: settings and configuration management
  - Handles all config file modifications
  - Provides config API for menubar app
  - / (main page)
    - View details from captured logs
    - Show thumbnails and analysis results
    - Collapsible details with OCR text and prompts
  - /settings
    - Configure intervals and directories
    - Set research topics
    - Store API keys securely
  - /open_log_file
    - Open log directory in Finder

## Data Storage
Application data in ~/Library/Application Support/Meadow/:
- config/config.json - User preferences
- data/screenshots/ - Screenshot images
- data/logs/ - Analysis logs (includes prompts and responses for debugging)
- cache/thumbnails/ - Web viewer thumbnail

Notes folder (Location set by user):
```
   notes/                                     # parent folder, may be named differently
      _machine/                               # App-managed source notes
         _staging/                            # Temporary staging area for new notes
            lognotes/                         # Raw converted log notes
      city_governance/                        # Organized by topic
         san_mateo_budget_pdf/                # Organized by source
            fiscal_summary.md                 # Subtopic
            public_works.md                   # Subtopic
         city_governance.knowledge.md         # Compares sources
      machine_notes.knowledge.md              # Tracks research topics
      research/                              # User knowledge space
      meadow_notes.knowledge.md              # Overall description of research folder
```

## Core Design Principles

### Architecture Patterns

- Screenshot lifecycle management:
  - Only save screenshots permanently if relevant to research
  - Clean up irrelevant screenshots at exit
  - Save to temp location until analysis complete
  - Move to permanent storage only after confirming research relevance
  - Testing considerations:
    - Verify window capture with fallback to full screen
    - Confirm temp file cleanup on irrelevant content
    - Check permanent storage path for relevant content
    - Test file permissions and directory creation
    - Validate file naming patterns and uniqueness

- Timestamp handling:
  - Record actual timestamps for API calls
  - Capture separate timestamps for request and response
  - Skip timestamps in OCR logging
  - Focus logging on method selection over timing

- Separate UI concerns from configuration management
  - Web interface handles all config modifications
  - Menubar app has read-only access to config
  - Prevents race conditions between interfaces
  - Makes config changes traceable through web UI

### Code Quality Standards

- Performance Standards:
  - Keep startup time under 1 second
  - Lazy load expensive resources
  - Initialize singletons only when first accessed
  - Defer file operations until needed
  - Profile startup path regularly

- Error Handling:
  - Log all exceptions with context
  - Provide user-friendly error messages
  - Use custom exceptions for domain-specific errors
  - Handle all file operations with appropriate try/except
  - Never suppress KeyboardInterrupt or SystemExit

### Configuration Management Patterns

- Config Change Handling:
  - Web viewer owns all config modifications
  - Config changes affect next app start
  - Clear menu item references during cleanup
  - Handle quick start/stop cycles gracefully

- Race condition prevention:
  - Web viewer validates before saving
  - Menubar app reloads on timer
  - Use atomic writes for config updates
  - Watch for external config changes

- Performance patterns:
  - Lazy initialize Config singleton on first access
  - Cache file paths but not content
  - Load config file only when values needed
  - Use atomic file operations for updates
  - Keep config operations off startup path

### Debug Logging
- Log all state transitions:
  - Start/stop of key operations (monitoring, analysis)
  - Before/after values for config changes
  - Entry/exit of long-running operations
  - Failures and fallback behavior
  - Config changes with old/new values
  - Monitoring lifecycle events
  - Settings changes with new values
- Avoid repetitive logging:
  - Log state changes once, not per iteration
  - Use counters for repeated operations
  - Summarize batch operations
  - Only log meaningful state changes

## How manicode.ai works
- Designed for code editing, also works well for other tasks
- NPM library which is an API to a backend server, which itself sends requests to LLMs
- Simple interface where the user can enter a prompt
- Can also accept a folderpath and a prompt as an argument when being called
- Reads *.knowledge.md files in working directory
- Reads relevant subset of other files from directory
- Uses LLM backend to determine what changes are needed to satisfy user request and generate those changes
- Can edit files directly and run shell commands

## How manicode_wrapper.py works with the Meadow note system
- json_to_markdown.py bridges the raw notes from the JSON into the markdown
- manicode_wrapper.py creates a PTY terminal to instantiate manicode at the notes/ folder
- calls manicode with instructions to process the raw notes into the research structure
- kills the process once the action is complete or if the API times out
- does not work well with long prompts due to PTY and API issues
- manicode is fairly expensive, but can do a lot in one go, so should be called less and asked to do more each time.

## TODO

### Critical Path

1. Testing Coverage
   - Add tests for pdf_analyzer.py
   - Add tests for markdown_bridge.py
   - Add tests for config.py
   - Add integration tests for note generation
   - Add tests for privacy level enforcement

2. Documentation
   - Installation guide for non-technical users
   - Configuration guide
   - API key setup walkthrough
   - Add screenshots/demo video

3. Privacy Implementation
   - Add privacy levels to metadata
   - Implement content redaction
   - Add privacy filtering system
   - Track redactions in metadata

4. Knowledge State Tracking
   - Implement epistemic status tracking
   - Add evidence chain tracking
   - Improve contradiction handling
   - Enhance metadata linking

### Future Improvements
- Enhanced metadata and linking
- Improved contradiction handling
- Better evidence quality tracking
- Expanded Obsidian integration
- User editing interface
- Enhanced privacy controls
- Additional note types
- Advanced knowledge mapping

## Dependencies
- rumps - macOS menubar app framework
- pillow - Image processing and screenshots
- anthropic - Claude API client
- pyobjc-framework-Quartz - Native macOS window management
- Flask - Web viewer server
- EasyOCR - Text extraction fallback
- py2app - macOS app bundling
- keyring - Secure API key storage
- manicode - Note generation (Beta)

### Dependency Management
- Use setup.py as single source of truth for dependencies
- Generate requirements.txt only when needed: `pip install . && pip freeze > requirements.txt`
