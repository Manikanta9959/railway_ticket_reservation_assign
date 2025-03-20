from fastapi import APIRouter
from endpoints.api_v1.test import router as test_router
from endpoints.api_v1.passenger import router as passenger_router
router = APIRouter()

router.include_router(test_router, prefix="", tags=["Test"])
router.include_router(passenger_router, prefix="", tags=["Passeneger"])