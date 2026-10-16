# HawkerLah! - SC2006 Software Engineering Project

**AY 25/26 Semester 2 | MACS Group 3**

A full-stack food recommendation web application for hawker stalls in Singapore, built for the SC2006 Software Engineering module at NTU.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite + Tailwind CSS v4 + React Router v6 |
| Backend | Python + FastAPI + SQLAlchemy |
| Database | PostgreSQL |
| Auth | JWT (python-jose + passlib/bcrypt) |
| Maps | Google Maps (external links) + OneMap API (geocoding) |

## External APIs (Singapore Government)

| API | Source | Purpose | Auth |
|---|---|---|---|
| **Hawker Centre List** | [data.gov.sg](https://data.gov.sg/datasets/d_68a42f09f350881996d83f9cd73ab02f/view) (NEA) | 107 hawker centres – names, addresses, stall counts | None (open data) |
| **Hawker Centre GeoJSON** | [data.gov.sg](https://data.gov.sg/datasets/d_4a086da0a5553be1d89383cd90d07ecd/view) (NEA) | Coordinates, photos, postal codes | None (open data) |
| **OneMap Search & Geocoding** | [OneMap](https://www.onemap.gov.sg/apidocs/) (SLA) | Address search, reverse geocoding, routing | JWT token (free registration) |

### How the APIs are used
## Take note to fill everything up into the .env file

1. **Seeding (startup):** `python seed.py` fetches all 107 NEA hawker centres from data.gov.sg, merges the CSV list with the GeoJSON coordinates/photos, and inserts them into the database.
2. **Admin sync:** Admins can click "Sync Now" on the dashboard to re-fetch the latest government data without restarting the server.
3. **Geocoding:** When users set a manual location (Nearby page, filter proximity), the app calls the OneMap Search API to convert addresses to coordinates.
4. **Routing:** The `/api/geocode/route` endpoint wraps OneMap's routing service for walk/drive/PT directions.

## Prerequisites

- **Node.js** v18+ and npm
- **Python** 3.11+
- **PostgreSQL** 14+ (running locally or via Docker)

## Setup

### 1. Database

Create a PostgreSQL database:

```sql
CREATE DATABASE sc2006_hawker;
```

### 2. Backend

```bash
cd server

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from example)
copy .env.example .env
# Edit .env with your PostgreSQL credentials

# (Optional) Add OneMap credentials for geocoding
# Register at https://www.onemap.gov.sg/apidocs/register
# Add ONEMAP_EMAIL and ONEMAP_PASSWORD to .env

# Run the seed script (fetches gov data + creates users + sample stalls)
python seed.py

# Start the server
uvicorn app.main:app --reload --port 8000
```

**Default accounts after seeding:**
- Admin: `admin@hawker.sg` / `admin123`
- User: `user@test.com` / `user123`

### 3. Frontend

```bash
cd client

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend runs on `http://localhost:5173` and proxies API calls to the backend at `http://localhost:8000`.

## Project Structure

```
SC2006/
├── client/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   │   ├── admin/
│   │   │   └── *.jsx
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── server/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── stalls.py
│   │   │   ├── recommendations.py
│   │   │   ├── reviews.py
│   │   │   ├── reports.py
│   │   │   ├── favourites.py
│   │   │   ├── notifications.py
│   │   │   ├── admin.py
│   │   │   └── geocode.py
│   │   ├── services/
│   │   │   ├── sg_data.py
│   │   │   ├── onemap.py
│   │   │   ├── recommendation.py
│   │   │   └── location.py
│   │   └── middleware/
│   │       └── auth.py
│   ├── seed.py
│   └── requirements.txt
└── README.md
```

## Features

### User Features
- **Food Recommendations** with filters (budget, dietary, proximity, popularity, favourites per FR 2 as per filtering and also FR 1)
- **Recommendation Flow** (Confirm / Reject / View Later interaction per FR 3.1)
- **Search** stalls by keyword (Searching by store name etc as per FR 4.3.1 and nearby search 4.3.2)
- **Nearby Eateries** based on GPS or manual location (OneMap as per 4.3.2)
- **Browse by Category** (Chinese, Malay, Indian, Western, etc. as per 4.3.3)
- **Stall Details** with menu, hours, reviews, crowd level bar, directions as per 4.1.1.5
- **Favourites** management (4.3.1 favourites)
- **Write Reviews** with mandatory photo upload (pending admin approval per FR 7.1 and 7.2 (visible by admins))
- **Submit Crowd Reports** (percentage-based crowd bar per FR 4.3.4 and 4.3.5 crowd levels)
- **Submit New Stalls** (pending admin approval per FR 6.2)
- **Report Bugs** and **Suggest Features** (per FR 5.1, 5.2)
- **Notifications** (approval/rejection alerts, admin broadcasts as per Admin notifications)
- **Google Maps** integration (open directions or copy address per FR 3.3.4, 4.1.1.5)

### Admin Features
- **Dashboard** with stats overview ()
- **Sync Government Data** from data.gov.sg (NEA hawker centres if anything gets out of date)
- **Manage Stalls** (CRUD operations per FR Admin 1.2 admin will be allowed to modify stall specific tasks)
- **Approve/Reject** stall submissions, reviews, crowd reports (per FR Admin 14-1, 15-1, 16-1)
- **User Reports** management (bugs, features, incorrect info per FR Admin 1.3 and 1.5, reporting system etc.)
- **Push Notifications** (notifications management etc per FR Admin 1.4)
- **User Management** (deactivate abusive users per FR Admin 1.3.2)

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for the interactive Swagger UI with all endpoints.

## White-box testing design

Functions chosen:
- approve_reject_stall() : Admin's role, CC score of 5 with 5 paths
- submit_new_stall() : User's role, CC score of 7 with 7 paths
- Test cases are created using Pytest with accordance to the paths
- Chose the above 2 functions due to their complex branching and logic, allowing us to test more in depth
