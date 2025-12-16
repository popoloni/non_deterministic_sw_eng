---
tool: claude
tool_version: "1.0"
last_verified: 2025-12-16
book_chapter: 10
book_section: "Static Context Engineering"
---

# Project Context

FastAPI REST API for user authentication and management.
Uses SQLAlchemy ORM and Pydantic for validation.

## Tech Stack
- Python 3.11+
- FastAPI with async handlers
- SQLAlchemy 2.0 (async)
- Pydantic v2 for validation
- PostgreSQL database
- Redis for caching/sessions
- pytest for testing

## Bash Commands
- `poetry install` - Install dependencies
- `poetry run uvicorn app.main:app --reload` - Start dev server
- `poetry run pytest` - Run test suite
- `poetry run pytest --cov` - Run with coverage
- `poetry run black .` - Format code
- `poetry run mypy .` - Type check

## Code Style
- Use type hints on all functions
- Async functions where possible
- Pydantic models for all request/response schemas
- Dependency injection via FastAPI `Depends`

## Project Structure
```
app/
├── main.py           # FastAPI app entry
├── api/
│   └── routes/       # Route handlers
├── core/
│   ├── config.py     # Settings
│   └── security.py   # Auth utilities
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
└── db/
    └── session.py    # Database connection
```

## Workflow
- Run type checker after making code changes
- Prefer running single tests during development
- Use `pytest -k "test_name"` for specific tests

## Key Patterns

### Route Handler
```python
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    user = await user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return UserResponse.model_validate(user)
```

### Service Layer
```python
class UserService:
    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
```

## Key Directories
- `app/api/routes/` - Route handlers
- `app/models/` - Database models  
- `app/schemas/` - Pydantic schemas
- `app/services/` - Business logic
- `app/core/` - Configuration and utilities

## Security Requirements
- Validate all input with Pydantic
- Use parameterized queries (SQLAlchemy handles this)
- Hash passwords with bcrypt
- JWT tokens for authentication
- Rate limiting on auth endpoints

## Reference Files
- Route example: `app/api/routes/users.py`
- Model example: `app/models/user.py`
- Schema example: `app/schemas/user.py`
- Service example: `app/services/user_service.py`
- Test example: `tests/api/test_users.py`
