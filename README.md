# FastAPI_robes

yo, so this is basically a simple CRUD API I built using FastAPI. nothing fancy, just learning the core stuff.

## what's this about?

it's a patient management system — create, read, update, delete patient records through API endpoints. the backend is FastAPI and there's a streamlit frontend to actually test it out without hitting raw endpoints.

right now it's using a JSON file (`store.json`) as the database. yeah i know, not production-ready at all, but it's just for learning the flow.

## what i learned here

- **FastAPI basics** — routing, path parameters, HTTP methods (GET, POST, PUT, DELETE)
- **Pydantic models** — schema validation, type hints, computed fields (like BMI calculation)
- **HTTPException** — proper error handling and status codes
- **JSONResponse** — returning custom responses
- **Streamlit integration** — building a simple frontend that calls the API

## project structure

```
.
├── api.py                 # main FastAPI app with full CRUD
├── web.py                 # streamlit frontend
├── store.json             # JSON database
├── 1_Basics/             # initial learning — basic routes
├── 2_GET_method/         # GET operations
├── 3_path_param/         # path parameters
├── 4_HTTP_exception_handling/  # error handling
├── 6_Post/               # POST endpoint
└── 7_Put_&_Delete/       # UPDATE and DELETE operations
```

## how to run

1. start the FastAPI server:
```bash
uvicorn api:app --reload
```

2. in another terminal, run the streamlit frontend:
```bash
streamlit run web.py
```

3. open `http://localhost:8501` in your browser

the API docs are at `http://localhost:8000/docs` (thanks to FastAPI's automatic swagger UI)

## endpoints

- `GET /` — root route, just a status check
- `GET /about` — tells you what this API does
- `GET /view` — get all patients
- `GET /view/{pid}` — get a specific patient
- `POST /create` — add a new patient
- `PUT /edit/{pid}` — update patient details
- `DELETE /delete/{pid}` — remove a patient

## patient schema

each patient has:
- `id` — unique identifier (like P001)
- `name` — patient name
- `city` — where they're from
- `age` — 0 to 120
- `gender` — male, female, or others
- `h` — height in feet
- `w` — weight in kg
- `bmi` — auto-calculated using `@computed_field`

## what's next?

- replace JSON with an actual database (probably PostgreSQL or MongoDB)
- add authentication (JWT tokens maybe?)
- better validation and error messages
- deploy this thing somewhere

that's it. just a learning project to get comfortable with FastAPI before i move to more complex stuff.