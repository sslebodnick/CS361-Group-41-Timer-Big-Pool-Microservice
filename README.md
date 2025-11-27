# Timer / Stopwatch Microservice

A flexible and easy-to-use timer/stopwatch microservice that allows you to track elapsed time for tasks and activities. Built with Node.js and Express, featuring both a RESTful API and a user-friendly web interface.

## Features

✅ **Start Timers** - Create timers with optional custom labels  
✅ **Stop Timers** - Stop running timers and get elapsed time in multiple formats  
✅ **Query Timer Status** - Check elapsed time for running or stopped timers  
✅ **Reset Timers** - Restart stopped timers from zero  
✅ **Delete Timers** - Remove timers when no longer needed  
✅ **Multiple Time Formats** - Get time as HH:MM:SS, total seconds, and broken down by hours/minutes/seconds  
✅ **Web Interface** - Simple HTML interface for testing and demonstration  
✅ **RESTful API** - Easy integration with any application  

## How to Run

### 1. Install Dependencies
```bash
npm install
```

### 2. Start the Server
```bash
node server.js
```

### 3. Access the Application
Open your browser and navigate to:
```
http://localhost:3001/index.html
```

The microservice API runs on **port 3001** (different from the Reminder microservice which uses port 3000).

## API Documentation

### Base URL
```
http://localhost:3001
```

### Endpoints

#### 1. Start a Timer
**Request:**
```http
POST /timers/start
Content-Type: application/json

{
  "label": "My Task"  // Optional - defaults to "Unnamed Timer"
}
```

**Response:**
```json
{
  "success": true,
  "timer": {
    "id": 1701234567890,
    "label": "My Task",
    "startTime": "2025-11-27T10:30:00.000Z",
    "status": "running"
  },
  "message": "Timer started successfully."
}
```

**User Story Alignment:** This fulfills the first user story - "Start timer". The microservice records the current time as the start time and returns a unique timer ID that can be used to stop or query that timer later.

---

#### 2. Stop a Timer
**Request:**
```http
POST /timers/{id}/stop
```

**Response (Success):**
```json
{
  "success": true,
  "timer": {
    "id": 1701234567890,
    "label": "My Task",
    "startTime": "2025-11-27T10:30:00.000Z",
    "endTime": "2025-11-27T10:35:00.000Z",
    "elapsedTime": {
      "formatted": "00:05:00",
      "totalSeconds": 300,
      "hours": 0,
      "minutes": 5,
      "seconds": 0
    },
    "status": "stopped"
  },
  "message": "Timer stopped successfully."
}
```

**Response (Timer Not Found):**
```json
{
  "success": false,
  "error": "Timer not found.",
  "message": "No timer found with ID: 999999"
}
```

**User Story Alignment:** This fulfills the second user story - "Stop timer and get elapsed time". When a valid timer ID is provided, the microservice records the end time, calculates elapsed time, and returns it in a clear format (HH:MM:SS). When an invalid timer ID is provided, it returns an error message.

---

#### 3. Get Timer Status
**Request:**
```http
GET /timers/{id}
```

**Response:**
```json
{
  "success": true,
  "timer": {
    "id": 1701234567890,
    "label": "My Task",
    "startTime": "2025-11-27T10:30:00.000Z",
    "endTime": null,
    "elapsedTime": {
      "formatted": "00:02:30",
      "totalSeconds": 150,
      "hours": 0,
      "minutes": 2,
      "seconds": 30
    },
    "status": "running"
  }
}
```

---

#### 4. Get All Timers
**Request:**
```http
GET /timers
```

**Response:**
```json
{
  "success": true,
  "timers": [
    {
      "id": 1701234567890,
      "label": "Task 1",
      "startTime": "2025-11-27T10:30:00.000Z",
      "endTime": "2025-11-27T10:35:00.000Z",
      "elapsedTime": {
        "formatted": "00:05:00",
        "totalSeconds": 300,
        "hours": 0,
        "minutes": 5,
        "seconds": 0
      },
      "status": "stopped"
    }
  ],
  "count": 1
}
```

---

#### 5. Reset a Timer
**Request:**
```http
POST /timers/{id}/reset
```

**Response:**
```json
{
  "success": true,
  "timer": {
    "id": 1701234567890,
    "label": "My Task",
    "startTime": "2025-11-27T10:40:00.000Z",
    "status": "running"
  },
  "message": "Timer reset successfully."
}
```

---

#### 6. Delete a Timer
**Request:**
```http
DELETE /timers/{id}
```

**Response:**
```json
{
  "success": true,
  "message": "Timer deleted successfully.",
  "deletedTimer": {
    "id": 1701234567890,
    "label": "My Task"
  }
}
```

## User Stories Implementation

### User Story 1: Start Timer ✅

**As a user I want to start a timer so that I can measure how long a specific task or activity takes while I'm using my application.**

**Implementation:**
- Endpoint: `POST /timers/start`
- Records current time as start time
- Returns unique timer ID
- Responds within 1 second under normal load

### User Story 2: Stop Timer and Get Elapsed Time ✅

**As a user I want to stop a running timer and see the elapsed time so that I can know how long my task or activity took.**

**Implementation:**
- Endpoint: `POST /timers/{id}/stop`
- Records end time when stopped
- Calculates elapsed time between start and end
- Returns time in multiple formats: `HH:MM:SS`, total seconds, and broken down
- Returns clear error message for invalid timer IDs

## Python Integration Example

Here's how to integrate this microservice with your habit tracker or any Python application:

```python
import requests
import time

BASE_URL = 'http://localhost:3001'

# Start a timer
def start_timer(label):
    response = requests.post(f'{BASE_URL}/timers/start', json={'label': label})
    data = response.json()
    if data['success']:
        return data['timer']['id']
    return None

# Stop a timer and get elapsed time
def stop_timer(timer_id):
    response = requests.post(f'{BASE_URL}/timers/{timer_id}/stop')
    data = response.json()
    if data['success']:
        return data['timer']['elapsedTime']
    return None

# Example usage
timer_id = start_timer("Exercise Session")
print(f"Timer started with ID: {timer_id}")

# Do your task...
time.sleep(5)

elapsed = stop_timer(timer_id)
print(f"Task completed in: {elapsed['formatted']}")
print(f"Total seconds: {elapsed['totalSeconds']}")
```

## Testing

A comprehensive test client is included to verify all functionality:

```bash
python test_client.py
```

The test client validates:
- Starting timers
- Getting timer status while running
- Stopping timers and receiving elapsed time
- Error handling for invalid timer IDs
- Managing multiple timers simultaneously
- Resetting timers
- Deleting timers

## Web Interface

The microservice includes a user-friendly web interface with three pages:

1. **Home** (`index.html`) - Overview and documentation
2. **Start Timer** (`start-timer.html`) - Create new timers with custom labels
3. **View Timers** (`view-timers.html`) - See all timers with real-time updates

Navigate between pages using the top navigation bar. The View Timers page automatically refreshes every second to show current elapsed times for running timers.

## UML Sequence Diagram

```
┌──────┐                 ┌─────────────────┐                 ┌──────────┐
│Client│                 │Timer Microservice│                │timers.json│
└──┬───┘                 └────────┬─────────┘                └────┬─────┘
   │                              │                               │
   │  POST /timers/start          │                               │
   │  { "label": "Task" }         │                               │
   ├─────────────────────────────>│                               │
   │                              │                               │
   │                              │  Generate timer ID            │
   │                              │  Record start time            │
   │                              │                               │
   │                              │  Save timer data              │
   │                              ├──────────────────────────────>│
   │                              │                               │
   │  { "success": true,          │                               │
   │    "timer": {                │                               │
   │      "id": 12345,            │                               │
   │      "status": "running" }}  │                               │
   │<─────────────────────────────┤                               │
   │                              │                               │
   │                              │                               │
   │  POST /timers/12345/stop     │                               │
   ├─────────────────────────────>│                               │
   │                              │                               │
   │                              │  Find timer by ID             │
   │                              │  Record end time              │
   │                              │  Calculate elapsed time       │
   │                              │                               │
   │                              │  Update timer data            │
   │                              ├──────────────────────────────>│
   │                              │                               │
   │  { "success": true,          │                               │
   │    "timer": {                │                               │
   │      "id": 12345,            │                               │
   │      "elapsedTime": {        │                               │
   │        "formatted": "00:05:30",                             │
   │        "totalSeconds": 330 },│                               │
   │      "status": "stopped" }}  │                               │
   │<─────────────────────────────┤                               │
   │                              │                               │
   │  GET /timers/12345           │                               │
   ├─────────────────────────────>│                               │
   │                              │                               │
   │                              │  Read timer data              │
   │                              │<──────────────────────────────┤
   │                              │                               │
   │  { "success": true,          │                               │
   │    "timer": { ... }}         │                               │
   │<─────────────────────────────┤                               │
   │                              │                               │
```

### Error Handling Flow

```
┌──────┐                 ┌─────────────────┐
│Client│                 │Timer Microservice│
└──┬───┘                 └────────┬─────────┘
   │                              │
   │  POST /timers/99999/stop     │
   ├─────────────────────────────>│
   │                              │
   │                              │  Search for timer ID 99999
   │                              │  Timer not found
   │                              │
   │  { "success": false,         │
   │    "error": "Timer not found.",
   │    "message": "No timer found with ID: 99999" }
   │<─────────────────────────────┤
   │                              │
```

## Project Structure

```
CS361-Group-41-Timer-Big-Pool-Microservice/
├── server.js              # Main Express server with all endpoints
├── package.json           # Node.js dependencies and scripts
├── index.html            # Home page with documentation
├── start-timer.html      # Interface for creating new timers
├── view-timers.html      # Interface for viewing all timers
├── test_client.py        # Comprehensive Python test suite
├── data/
│   └── timers.json       # Persistent storage for timer data
└── README.md             # This file
```

## Data Storage

Timer data is persisted in `data/timers.json` with the following structure:

```json
[
  {
    "id": 1701234567890,
    "label": "Exercise Session",
    "startTime": 1701234567890,
    "endTime": 1701234867890,
    "elapsedTime": {
      "formatted": "00:05:00",
      "totalSeconds": 300,
      "hours": 0,
      "minutes": 5,
      "seconds": 0
    },
    "status": "stopped",
    "createdAt": "2025-11-27T10:30:00.000Z"
  }
]
```

## Architecture

This microservice follows the same architectural patterns as the Reminder microservice:

- **Express.js** server for RESTful API
- **CORS** enabled for cross-origin requests
- **JSON file storage** for persistence
- **Static file serving** for HTML interface
- **Modular helper functions** for clean code organization

## Port Configuration

- **Timer Microservice:** Port 3001
- **Reminder Microservice:** Port 3000

Both services can run simultaneously without conflicts.

## Quality Attributes

### Responsiveness ✅
- Timer start/stop requests complete within 1 second under normal load
- Lightweight JSON storage ensures fast read/write operations

### Usability ✅
- Elapsed time returned in multiple formats for flexibility
- Simple, documented API easy to integrate with any CLI program
- Clear error messages for all failure cases
- Consistent JSON response structure

### Reliability
- Error handling for all edge cases (invalid IDs, already stopped timers, etc.)
- Data persistence ensures timers survive server restarts
- Input validation prevents invalid data

## Version

**v1.0.0** - Initial release

---

**Author:** CS361 Group 41  
**License:** ISC
