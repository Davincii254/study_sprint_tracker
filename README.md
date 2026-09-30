# Study Sprint Tracker Practical Example

This example helps students cement client-server applications, `fetch()`, Flask routes, JSON responses, cookies, and sessions.

The example is intentionally different from the source examples. Instead of a task app, internal dashboard, or paywall, students build a **Study Sprint Tracker**.

## What students will practice

1. Sending `GET`, `POST`, `PATCH`, and `DELETE` requests from JavaScript using `fetch()`.
2. Building Flask routes that receive requests and return JSON.
3. Updating the browser page without reloading.
4. Using Flask `session` to remember a learner's username and visit count.
5. Setting a manual cookie for a non-sensitive preference called `focus_mode`.
6. Inspecting cookies in browser developer tools.

## Folder structure

```text
study_sprint_tracker/
├── README.md
├── requirements.txt
└── server/
    ├── app.py
    └── static/
        └── index.html
```

## Setup

From inside the `study_sprint_tracker` folder:

```bash
python -m venv .venv
```

Activate the virtual environment.

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install Flask:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python server/app.py
```

Open the browser at:

```text
http://127.0.0.1:5000
```

## Route plan

| User action | Method | Endpoint | What happens |
|---|---:|---|---|
| See current learner | GET | `/api/me` | Reads session and cookie data |
| Log in | POST | `/api/login` | Stores username in the session |
| Log out | POST | `/api/logout` | Clears session data |
| List study sprints | GET | `/api/study-sessions` | Returns all study sessions as JSON |
| Add a study sprint | POST | `/api/study-sessions` | Creates a new in-memory item |
| Mark sprint complete | PATCH | `/api/study-sessions/<id>` | Updates one item |
| Delete sprint | DELETE | `/api/study-sessions/<id>` | Removes one item |
| Save focus mode | POST | `/api/focus-mode` | Sets a manual cookie |

## Student tasks

1. Run the app and open the browser console.
2. Open the Network tab and perform each user action.
3. For each action, write down the method, endpoint, status code, and JSON response.
4. Log in using a username, refresh the page, and observe that the session still remembers the learner.
5. Change the focus mode, then inspect the `focus_mode` cookie in DevTools.
6. Add a new route: `PATCH /api/study-sessions/<id>/reset` to mark a sprint as incomplete again.

## Discussion questions

1. Why does the page update without a full reload?
2. Which data is stored in memory, which data is stored in the session, and which data is stored in a cookie?
3. Why should sensitive information not be stored in a manually set cookie?
4. What would change if the study sessions were stored in a database instead of a Python list?
