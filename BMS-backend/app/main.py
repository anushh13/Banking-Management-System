from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database.connection import engine
from app.routers import customers, accounts, transactions

app = FastAPI(
    title="Banking Management System API",
    description="Customer/account management and core banking transaction APIs",
    version="1.0.0",
)

# Local development only. Restrict origins to the actual frontend URL before deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)

app.include_router(customers.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Banking Management System API is running"}


@app.get("/api/v1/health")
def health():
    return {"status": "healthy"}


@app.get("/api/v1/database-test")
def database_test():
    with engine.connect() as connection:
        value = connection.execute(text("SELECT 1")).scalar()
    return {"database": "connected", "test_result": value}
