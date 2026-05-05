# API Reference

Base URL: `http://localhost:3000` (configurable via `PORT` env variable)

## Authentication

All endpoints (except `GET /`) require a Bearer token in the `Authorization` header and a JSON body.

```
Authorization: Bearer <your_token>
Content-Type: application/json
```

The token is configured via the `VALID_TOKEN` environment variable (default: `sample`).

---

## Response format

All endpoints return a standard JSON envelope:

```json
{
  "status": "OK" | "ERROR",
  "message": <result or error description>,
  "time": <elapsed seconds>
}
```

HTTP status codes:

| Code | Meaning |
|------|---------|
| `200` | Success |
| `400` | Bad request / controller error |
| `401` | Unauthorized (missing or invalid token) |

---

## Endpoints

### `GET /`

Health check. Returns a plain text string.

**Auth required:** No

**Response:**

```
selenium-scraper-quickstarter
```

---

### `GET /course_registration`

Registers a course attendance entry in [asismetro.org](https://asismetro.org) and returns the current list of registrations.

**Auth required:** Yes

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Login username for asismetro.org |
| `password` | string | Yes | Login password for asismetro.org |
| `date` | string | Yes | Date in `DD/MM/YYYY` format, e.g. `"04/05/2026"` |
| `shift` | string | Yes | Shift number. Allowed values: `"1"`, `"2"`, `"3"`, `"4"` |
| `activity` | string | Yes | Activity type. Allowed values: `"Curso Bíblico Iniciado"`, `"Sin Cursos Bíblicos"`, `"Turno Anulado"` |
| `number` | string | Yes | Registration number |

**Example request:**

```bash
curl -X GET http://localhost:3000/course_registration \
  -H "Authorization: Bearer sample" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myuser",
    "password": "mypassword",
    "date": "04/05/2026",
    "shift": "1",
    "activity": "Curso Bíblico Iniciado",
    "number": "123"
  }'
```

**Success response (`200`):**

```json
{
  "status": "OK",
  "message": [ ... ],
  "time": 12.34
}
```

**Error responses:**

```json
{ "status": "ERROR", "message": "The field 'date' has not been sent", "time": 0.01 }
{ "status": "ERROR", "message": "The field 'activity' must be one of: Curso Bíblico Iniciado, Sin Cursos Bíblicos, Turno Anulado", "time": 0.01 }
{ "status": "ERROR", "message": "The field 'shift' must be one of: 1, 2, 3, 4", "time": 0.01 }
{ "status": "ERROR", "message": "The field 'date' must have the format DD/MM/YYYY, e.g. '04/05/2026'", "time": 0.01 }
```

---

### `GET /get-calendar`

Retrieves the shift calendar for the current month and the next month from [asismetro.org](https://asismetro.org).

**Auth required:** Yes

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Login username for asismetro.org |
| `password` | string | Yes | Login password for asismetro.org |

**Example request:**

```bash
curl -X GET http://localhost:3000/get-calendar \
  -H "Authorization: Bearer sample" \
  -H "Content-Type: application/json" \
  -d '{"username": "myuser", "password": "mypassword"}'
```

**Success response (`200`):**

```json
{
  "status": "OK",
  "message": {
    "actual_calendar": { "sections": [ ... ] },
    "next_calendar":   { "sections": [ ... ] }
  },
  "time": 15.42
}
```

Both `actual_calendar` and `next_calendar` share the same structure:

```json
{
  "sections": [
    {
      "days": [
        { "weekday": "Lunes", "date": "1 MAYO" },
        { "weekday": "Martes", "date": "2 MAYO" }
      ],
      "slots": [
        {
          "time_range": "09:00 - 12:00",
          "entries": [
            {
              "weekday": "Lunes",
              "date": "1 MAYO",
              "status": "warning" | "danger" | "info" | "active" | null,
              "request_button": {
                "label": "Solicitar Turno",
                "onclick": "cambio('A','1234567890','1','MAYO','T1')",
                "parsed_onclick": {
                  "raw": "cambio('A','1234567890','1','MAYO','T1')",
                  "action_code": "A",
                  "unix_time": "1234567890",
                  "day_number": "1",
                  "month": "MAYO",
                  "slot_code": "T1"
                }
              },
              "assignees": [
                { "id": "1", "name": "Carlos Castellanos", "phone": "607297573" }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

Each calendar is split into **sections** (one per week). Each section contains:

| Field | Type | Description |
|-------|------|-------------|
| `days` | object[] | Ordered list of days in the week (`weekday`, `date`) |
| `slots` | object[] | Time slots for that week |
| `slots[].time_range` | string | Time range label, e.g. `"09:00 - 12:00"` |
| `slots[].entries` | object[] | One entry per day — mirrors the `days` order |
| `entries[].weekday` | string \| null | Weekday name |
| `entries[].date` | string \| null | Date label, e.g. `"1 MAYO"` |
| `entries[].status` | string \| null | CSS class indicating slot state: `"warning"`, `"danger"`, `"info"`, `"active"`, or `null` |
| `entries[].request_button` | object \| null | Present when the slot can be requested; `null` otherwise |
| `entries[].assignees` | object[] | People assigned to the slot (may be empty) |
| `assignees[].id` | string \| null | Internal toggle ID |
| `assignees[].name` | string \| null | Assignee full name |
| `assignees[].phone` | string \| null | Assignee phone number |

---

### `GET /sample`

Sample/demo endpoint for testing controller wiring. Requires credentials but performs no real action.

**Auth required:** Yes

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Any username |
| `password` | string | Yes | Any password |

**Example request:**

```bash
curl -X GET http://localhost:3000/sample \
  -H "Authorization: Bearer sample" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}'
```

**Success response (`200`):**

```json
{
  "status": "OK",
  "message": "ok",
  "time": 1.23
}
```

---

### `GET /test` · `POST /test`

Runs browser automation tests across Chrome and/or Firefox and returns a summary of results.

**Auth required:** Yes

**Request body (all fields optional):**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `browsers` | string[] | `["chrome", "firefox"]` | Browsers to test |
| `test_search` | boolean | `true` | Enable element search tests |
| `test_writes` | boolean | `true` | Enable text write tests |
| `screenshots` | boolean | `true` | Save screenshots during tests |
| `urls` | string[] | `["https://www.google.com", "https://www.github.com"]` | URLs to visit |

**Example request:**

```bash
curl -X POST http://localhost:3000/test \
  -H "Authorization: Bearer sample" \
  -H "Content-Type: application/json" \
  -d '{
    "browsers": ["chrome"],
    "test_search": true,
    "test_writes": false,
    "screenshots": false,
    "urls": ["https://www.google.com"]
  }'
```

**Success response (`200`):**

```json
{
  "status": "OK",
  "message": {
    "total_tests": 4,
    "passed_tests": 4,
    "failed_tests": 0,
    "browser_results": { ... },
    "errors": []
  },
  "time": 8.76
}
```

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3000` | Port the server listens on |
| `STAGE` | `staging` | Set to `production` to disable Flask debug mode |
| `VALID_TOKEN` | `sample` | Bearer token required to authenticate requests |
| `HEADLESS_MODE` | `auto` | `True` to force headless, `auto` to detect display |
| `BROWSER_LANGUAGE` | `en` | Browser locale |
| `AUTO_DELETE_LOGS` | `true` | Automatically clean up old log files |
