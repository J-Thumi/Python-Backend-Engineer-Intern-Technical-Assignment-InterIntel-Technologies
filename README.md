
# InterIntel Python Backend Engineer Technical Assessment

This repository contains a robust, highly performant Django REST Framework (DRF) backend implementation designed to handle bulk notification payloads efficiently. Built with atomic database integrity, structured logging, and bulk query optimizations.

---

## Key Architectural Highlights

* **Atomic Transactions:** Uses Django's `@transaction.atomic` block to guarantee database consistency. If any notification in a batch fails to insert, the entire payload (including the sender) safely rolls back.
* **Performance Optimization:** Leverages Django’s `bulk_create` interface to write all nested notification records in a single database round-trip rather than executing individual $N$ queries.
* **Structured File Logging:** Custom logging pipelines write system processes, validation alerts, and error stack traces to a centralized log file (`logs/django.log`) for streamlined debugging.
* **Clean API Separation:** Cleanly separates nested input serialization (`SenderSerializer`) from the concise output projection (`SenderResponseSerializer`) to optimize payload response sizes.

---

## Prerequisites

Before getting started, ensure you have the following installed on your machine:
* **Python 3.10+** (Recommended: Python 3.12+)
* **Git**
* **pip** (Python package installer)

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/J-Thumi/Python-Backend-Engineer-Intern-Technical-Assignment-InterIntel-Technologies
cd Python-Backend-Engineer-Intern-Technical-Assignment-InterIntel-Technologies

```

### 2. Create and Activate a Virtual Environment

#### On Linux & macOS:

```bash
python3 -m venv venv
source venv/bin/activate

```

#### On Windows (Command Prompt):

```cmd
python -m venv venv
venv\Scripts\activate.bat

```

#### On Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1

```

### 3. Install Project Dependencies

Ensure your virtual environment is active, then install the required libraries:

```bash
pip install -r requirements.txt

```

### 4. Create Log Directory

Since the custom logger writes to a local file, ensure the directory exists before booting up:

```bash
mkdir logs

```

### 5. Apply Database Migrations

Initialize your SQLite database schema by running:

```bash
python manage.py migrate

```

---

## Running the Application

Start the local Django development server:

```bash
python manage.py runserver

```

The server will boot up and be accessible locally at **`http://127.0.0.1:8000/`**.

When you are done developing, you can turn off the virtual environment by executing:

```bash
deactivate

```

---

## API Endpoints & Usage

### Create Bulk Notifications

* **URL:** `/api/notifications/bulk`
* **Method:** `POST`
* **Headers:** `Content-Type: application/json`

#### Sample Request Payload

```json

{
    "name": "Alice Kamau",
    "email": "alice@example.com",
    "notifications": [
        {
            "title": "Welcome",
            "message": "Thank you for joining us.",
            "channel": "email"
        },
        {
            "title": "Reminder",
            "message": "Your subscription renews tomorrow.",
            "channel": "sms"
        }
    ]
}

```

#### Successful Response (`201 Created`)

```json
{
    "message": "Notifications created successfully.",
    "sender": {
        "id": 7,
        "name": "Alice Kamau",
        "email": "alice@example.com"
    },
    "notifications_created": 2
}

```

#### Validation Error Response (`400 Bad Request`)

If invalid data is sent (e.g., missing required fields, invalid email format):

```json

// response if invalid email

{
  "success": false,
  "message": "Validation failed.",
  "errors": {
    "email": [
      "Enter a valid email address."
    ]
  }
}

// Response if the channel is not either sms/email/push

{
    "success": false,
    "message": "Validation failed.",
    "errors": {
        "notifications": [
            {
                "channel": [
                    "\"emai\" is not a valid choice."
                ]
            },
            {}
        ]
    }
}

// Response if any of the required data is missing

{
    "success": false,
    "message": "Validation failed.",
    "errors": {
        "notifications": [
            {},
            {
                "message": [
                    "This field is required."
                ]
            }
        ]
    }
}

```

---

## Logging System

The application logs crucial processing events and exceptions to a persistent file located in **`logs/django.log`**.

### Configured Loggers:

* **`django`**: Configured at the `INFO` level to capture framework routing, runtime issues, and database interactions.
* **`notifications`**: Configured at the `INFO` level to track incoming endpoint payloads, validate data formats, monitor successful transactional rollouts, and log exact stack traces if processing breaks down.

#### Sample Log Output:

```text
Bulk notification request received
Creating sender with email=joe@gmail.com and notifications_count=2
Successfully created sender id=6 with 2 notifications
Bulk notification processing completed for sender id=6
"POST /api/notifications/bulk HTTP/1.1" 201 130

Bulk notification request received
Notification validation failed. Errors={'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]}
Bad Request: /api/notifications/bulk
"POST /api/notifications/bulk HTTP/1.1" 400 100

Bulk notification request received
Notification validation failed. Errors={'notifications': [{}, {'channel': [ErrorDetail(string='"sm" is not a valid choice.', code='invalid_choice')]}]}
Bad Request: /api/notifications/bulk
"POST /api/notifications/bulk HTTP/1.1" 400 126

```
