from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.simulations import router as simulations_router
from app.routes.metrics import router as metrics_router
from app.routes.product import router as product_router
from app.routes.team import router as team_router
from app.routes.market import router as market_router

app = FastAPI(title="Market Sim Platform")
app.include_router(simulations_router)
app.include_router(product_router)
app.include_router(metrics_router)
app.include_router(market_router)
app.include_router(team_router)

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