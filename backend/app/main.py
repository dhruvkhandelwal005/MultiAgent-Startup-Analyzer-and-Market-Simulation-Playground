from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.simulations import router as simulations_router
from app.routes.product import router as product_router

app = FastAPI(title="Market Sim Platform")
app.include_router(simulations_router)
app.include_router(product_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}