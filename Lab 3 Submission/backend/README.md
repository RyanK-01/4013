# SC2006 HawkerLah! — Backend Skeleton Code

## Overview

Skeleton for Lab 3 Submission.

Skeleton has:
- Full class/function declarations with type annotations
- Comprehensive docstrings documenting design intent and usage
- Import structure and dependency relationships
- Method signatures with `...` placeholders for implementation bodies

## Package Structure (Design-Class Stereotypes)

```
backend/
├── requirements.txt              # Python dependencies with pinned versions
├── README.md                     
└── app/
    ├── __init__.py               # Package docstring & structure overview
    ├── config.py                 
    ├── database.py               
    ├── main.py                   
    │
    ├── models/                   # <<entity>>  ORM models (database tables)
    │   ├── __init__.py           
    │   ├── user.py               
    │   ├── stall.py              
    │   ├── review.py             
    │   ├── favourite.py          
    │   ├── crowd_report.py       
    │   ├── report.py             
    │   ├── notification.py       
    │   └── saved_search.py       
    │
    ├── schemas/                  # <<datatype>>  Pydantic request/response DTOs
    │   ├── user.py               
    │   ├── stall.py               
    │   ├── review.py             
    │   ├── recommendation.py     
    │   └── report.py             
    │
    ├── middleware/                # <<control>>  Cross-cutting auth guards
    │   └── auth.py               
    │
    ├── services/                 # <<control>>  Domain logic & external integrations
    │   ├── location.py           
    │   ├── recommendation.py     
    │   ├── onemap.py             
    │   └── sg_data.py            
    │
    └── routes/                   # <<boundary>>  API endpoint handlers
        ├── auth.py               
        ├── stalls.py             
        ├── recommendations.py    
        ├── reviews.py            
        ├── reports.py            
        ├── favourites.py         
        ├── notifications.py      
        ├── geocode.py            
        └── admin.py              
```

## Design Decisions

| Decision | Rationale |
|---|---|
| **FastAPI + Pydantic** | Data validation |
| **SQLAlchemy ORM** | Declarative models, ORM to allow python code to interact with db |
| **JWT (python-jose)** | Authentication |
| **bcrypt** | Hashing |
| **Admin approval workflow** | Stalls, reviews, and crowd reports require moderation |
| **Haversine distance** | For calculating shortest path between 2 points on earth's surface (used for our apps navigation) |

## Getting Started (Skeleton Code where we removed all the core functionalities, sqlalchemy won't work without the db, so it can't run since we use PASS for the db but our actual submission would have everything runnable. The code below is just for reference for when we have our actual setup.)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env       # Edit DATABASE_URL, SECRET_KEY, etc.

# Run the development server
uvicorn app.main:app --reload
```

API documentation is available at `http://localhost:8000/docs` (Swagger UI).
