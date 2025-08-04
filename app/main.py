from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.database import Base, engine, SessionLocal
from app.routes import auth, user, budget, category, transaction
from app.utils.global_base_categories import ensure_global_base_categories
from app.utils import error_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Budget App")

# CORS middleware for mobile app support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict to your mobile app's domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom error handlers for consistent JSON errors
app.add_exception_handler(RequestValidationError, error_handlers.validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, error_handlers.http_exception_handler)
app.add_exception_handler(Exception, error_handlers.generic_exception_handler)

@app.on_event("startup")
def create_global_base_categories():
    db = SessionLocal()
    try:
        ensure_global_base_categories(db)
    finally:
        db.close()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(budget.router, prefix="/api/budgets", tags=["budgets"])
app.include_router(category.router, prefix="/api/categories", tags=["categories"])
app.include_router(transaction.router, prefix="/api/transactions", tags=["transactions"])
