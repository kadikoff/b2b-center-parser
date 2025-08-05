from fastapi import APIRouter

from .routes_tenders import router as tenders_router

router = APIRouter()
router.include_router(tenders_router, tags=["Tenders"])
