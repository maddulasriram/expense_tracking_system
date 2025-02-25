# Expense Tracking System

## Overview
A simple yet useful expense tracking system that allows users to track expenses by date and provides analytics for a specified time frame. The system includes a FastAPI backend, a Streamlit-based frontend, and a MySQL database for storage.

## Features
- Add, update, and retrieve expenses by date
- View expense analytics over a time frame
- Interactive web UI for ease of use
- API with FastAPI backend
- Asynchronous database operations with aiomysql
- Styled Streamlit UI with black theme and red highlights

## Tech Stack
- **Backend**: Python, FastAPI, asyncio, aiomysql
- **Frontend**: Streamlit, Pandas, requests
- **Database**: MySQL
- **Other Libraries**: Logging, Pydantic, Contextlib, Typing, Pytest

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL database installed and configured
- (ensure the schema is set up correctly)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd expense-tracker
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the MySQL database:
   - Ensure MySQL is running
   - Update the database connection settings in `db_helper.py`

### Running the Backend
Start the FastAPI backend using Uvicorn:
```bash
uvicorn api:app --reload
```

### Running the Frontend
Start the Streamlit UI:
```bash
streamlit run frontend.py
```

## API Endpoints

### 1. Get Expenses for a Date
```http
GET /expenses/{expense_date}
```
**Response**:
```json
[
  {
    "amount": 500.0,
    "category": "Food",
    "notes": "Lunch at restaurant"
  }
]
```

### 2. Add or Update Expenses
```http
POST /expenses/{expense_date}
```
**Request Body**:
```json
[
  {
    "amount": 200.0,
    "category": "Transport",
    "notes": "Cab ride"
  }
]
```
**Response**:
```json
{"message": "Expenses added/updated successfully"}
```

### 3. Get Analytics for a Date Range
```http
POST /analytics/
```
**Request Body**:
```json
{
  "startdate": "2024-02-01",
  "enddate": "2024-02-20"
}
```



## Testing
Run the tests using pytest:
```bash
pytest
```


