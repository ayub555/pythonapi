from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from app.database import mysqldbaccess
from app.logging_config import logger
from app.middleware import RequestLoggingMiddleware
from app.models.user import AuthRequest
from app.routers import education, employee, states, users

app = FastAPI(title="HDFC Bank API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(states.router)
app.include_router(education.router)
app.include_router(users.router)
app.include_router(employee.router)


@app.exception_handler(MySQLError)
async def mysql_exception_handler(request: Request, exc: MySQLError):
    logger.error("Database error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(status_code=503, content={"detail": "Database error occurred"})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/")
def root():
    return {"message": "HDFC Bank API is running"}


@app.post("/authenticateuser")
def authenticate_user(credentials: AuthRequest):
    user = mysqldbaccess.fetch_one(
        "SELECT userId FROM users WHERE username = %s AND password = %s",
        (credentials.username, credentials.password),
    )
    return user is not None
