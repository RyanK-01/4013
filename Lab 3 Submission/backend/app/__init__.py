"""
SC2006 HawkerApp (TODO: THINK OF GOOD NAME)! — Backend Application Package

Package structure (organised by design-class stereotypes):

    app/
    ├── config.py          # Application settings (<<infrastructure>>)
    ├── database.py        # SQLAlchemy engine & session (<<infrastructure>>)
    ├── main.py            # FastAPI entry point (<<infrastructure>>)
    ├── models/            # ORM entity classes (<<entity>>)
    ├── schemas/           # Pydantic request/response DTOs (<<datatype>>)
    ├── routes/            # API endpoint handlers (<<boundary>>)
    ├── services/          # Domain logic & external integrations (<<control>>)
    └── middleware/        # Cross-cutting auth guards (<<control>>)
"""
