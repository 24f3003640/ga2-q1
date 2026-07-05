import time
import uuid
import statistics
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS Middleware ---
# The grader checks preflights from allowed origin (dash-z34fht.example.com) and evil origin.
origins = [
    "https://dash-z34fht.example.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Custom Headers Middleware ---
# X-Request-ID and X-Process-Time are required on every response.
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response


# --- Stats Endpoint ---
@app.get("/stats")
def calculate_stats(values: str):
    # Parse comma-separated integers
    try:
        numbers = [int(n.strip()) for n in values.split(",") if n.strip()]
    except ValueError:
        return {"error": "Invalid input, expected comma-separated integers"}

    if not numbers:
        return {"error": "No values provided"}

    # Compute statistics
    count = len(numbers)
    total_sum = sum(numbers)
    min_val = min(numbers)
    max_val = max(numbers)
    mean_val = statistics.mean(numbers)

    return {
        "email": "24f3003640@ds.study.iitm.ac.in",
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }
