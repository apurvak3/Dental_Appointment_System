# Dental Appointment System

A conversational dental scheduling assistant built with Flask, LangGraph, and Google Gemini. The application supports appointment discovery, booking, cancellation, and rescheduling through a chat interface backed by tool-based CSV operations.

Live Demo: https://dental-appointment-system-1jy3.onrender.com/

## Overview

This project combines a lightweight Flask frontend with a multi-agent orchestration layer. User requests are routed through a supervisor and handled by specialized agents for:

- Appointment information and slot discovery
- New appointment booking
- Existing appointment cancellation
- Appointment rescheduling

Appointment availability is currently stored in `doctor_availability.csv`, which is read and updated through dedicated tool functions.

## Features

- Conversational interface for dental appointment workflows
- Multi-agent routing using LangGraph
- Gemini-powered intent handling and task execution
- CSV-backed appointment storage for quick prototyping
- Responsive frontend with a custom chat UI
- Render deployment support with `gunicorn`

## Tech Stack

- Python
- Flask
- LangGraph
- LangChain Core
- Google Gemini via `langchain-google-genai`
- Pandas
- HTML, CSS, JavaScript

## Project Structure

```text
Dental_Appointment_System/
├── main.py
├── doctor_availability.csv
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── dental_agent/
    ├── agent.py
    ├── llm.py
    ├── config/
    │   └── settings.py
    ├── agents/
    │   ├── supervisor.py
    │   ├── info_agent.py
    │   ├── booking_agent.py
    │   ├── cancellation_agent.py
    │   └── rescheduling_agent.py
    ├── tools/
    │   ├── csv_reader.py
    │   ├── csv_writer.py
    │   └── csv_writter.py
    └── workflow/
        └── graph.py
```

## How It Works

1. The Flask app serves the chat UI and accepts user messages through `/chat`.
2. The LangGraph workflow receives conversation history.
3. A supervisor determines whether the request is informational, booking-related, cancellation-related, or rescheduling-related.
4. The selected agent uses tool calls to read or update `doctor_availability.csv`.
5. The final response is returned to the frontend as a single chat reply.

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Dental_Appointment_System
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

## Run Locally

```bash
python main.py
```

The app will be available at:

```text
http://127.0.0.1:5000
```

## Deployment

This project is deployed on Render.

Recommended Render settings:

- Root Directory: leave blank
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn main:app`

Required environment variable:

- `GOOGLE_API_KEY`

## Current Data Layer

The project currently uses `doctor_availability.csv` as its source of truth for appointment data. This is suitable for demos and prototypes, but not ideal for production because:

- filesystem writes may be ephemeral on some hosting providers
- CSV does not provide concurrency control
- querying and validation become harder as data grows

For a production-ready version, a database-backed persistence layer would be the next step.

## API Notes

Primary route:

- `GET /` renders the frontend
- `POST /chat` sends a message to the assistant and returns a JSON response

Example request:

```json
{
  "message": "Book an appointment with an orthodontist next week"
}
```

## Future Improvements

- Replace CSV storage with a relational database
- Add authentication for patients and admins
- Persist conversation history per user
- Add doctor-side dashboard and appointment management
- Add structured validation around appointment IDs and duplicate records

## License

This project is intended for educational and portfolio use unless you define a separate license for distribution.
