# Bug Report API

This project provides a REST API for managing bug reports using the Django REST Framework.

## Endpoint

**`http://<domain>/bug-reports/`**

### Methods Supported

#### 1. GET Method
Retrieves a list of bug reports. You can filter the bug reports by severity or status using query parameters.

**Parameters (Optional):**
- `severity` (string): Filter by the severity of the bug.
- `status` (string): Filter by the status of the bug.

**Example Request:**
```
GET /bug-reports/?severity=high&status=open
```

**Response:**
Returns a JSON array containing the bug reports.
```json
[
  {
    "id": 1,
    "title": "Bug title",
    "description": "Bug description",
    "severity": "high",
    "status": "open"
  }
]
```

#### 2. POST Method
Creates a new bug report.

**Request Body:**
Provide a JSON object containing the bug details. The required fields depend on the `BugReportSerializer` (typically including title, description, severity, status, etc.).

**Example Request:**
```json
POST /bug-reports/
Content-Type: application/json

{
  "title": "Application crash on login",
  "description": "The app crashes when clicking the login button on iOS 15.",
  "severity": "critical",
  "status": "new"
}
```

**Response:**
Returns the newly created bug report with a `201 Created` status code if successful. Returns a `400 Bad Request` with error details if the validation fails.

## How it works

1. **Routing:** The request hits `bug/urls.py` where `/bug-reports/` is mapped to the `BugReportAPI` view.
2. **View (`bug/views.py`):**
   - **GET:** Extracts `severity` and `status` filters, passes them to `BugService.list_bugs()`, serializes the results, and returns them.
   - **POST:** Validates the incoming JSON payload using `BugReportSerializer`. If valid, it passes the data to `BugService.create_bug()` to save the new record to the database, and then returns the newly created record.
3. **Service layer (`bug/service.py`):** Handles the business logic for creating and querying bug records.
4. **Serializer (`bug/serializer.py`):** Handles data conversion between Python objects/QuerySets and JSON formats, as well as data validation.
