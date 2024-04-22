from fastapi import APIRouter
from src.api.v1.endpoints import auth_router, user_router

routers = APIRouter()
router_list = [
    auth_router,
    user_router,
]  # Add to this list, if there are multiple routers.

for router in router_list:
    routers.include_router(router)
