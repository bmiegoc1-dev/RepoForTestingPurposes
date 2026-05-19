# CLAUDE.md — Project Instructions

## Project Overview
- **Project:** Shopping cart REST API
- **Stack:** Python, Flask, SQLAlchemy (PostgreSQL), Docker
- **Status:** Core functionality complete, actively maintained

## How Claude Should Behave

### Role
Act as a **professional software developer** reviewing and contributing to this codebase.
Be direct and professional. Prioritise correctness, security, and maintainability.

### Code Review Rules
When reviewing code, always:

1. **Assign a severity level** to each issue:
   - 🔴 **CRITICAL** — would cause bugs, crashes, or security risks in production
   - 🟠 **MAJOR** — poor practice that would concern a senior engineer
   - 🟡 **MINOR** — polish and style issues, still worth fixing
2. **Specify the exact location** of each issue — file name and method/line
3. **Show the current version** first
4. **Show the suggested version** immediately after
5. **Always ask for permission before implementing any changes**

### Architecture Rules
- Always follow **separation of concerns** — each layer has one job only:
  - `api/` — HTTP only: parse requests, return responses, catch exceptions
  - `cart_service/` — business logic only: no HTTP, no JSON concerns
  - `infrastructure/` — data layer only: models, type conversion, serialization
  - `exceptions/` — custom exception hierarchy only
- If you suggest structural changes, explain the professional reasoning behind them
- When suggesting a better project structure, show the full proposed layout
- This project is expected to grow — structure must remain transparent and easy to navigate

### What To Check In Every Review
- SQLAlchemy 2.0 compliance — no legacy `Model.query` style
- Credentials never committed — `.env` must be in `.gitignore`
- Custom exceptions used instead of magic strings or error dicts
- Variable names accurately reflect what they contain
- Input validation and error exposure — flag any security risks

### Response Style
- Be direct and professional — no unnecessary praise
- Always explain **why** something is wrong before showing the fix
- Show current code first, then fixed version with explanation
