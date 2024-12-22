from typing import Union
from fastapi import APIRouter
from src.identities.services.get_dni_service import get_dni_service, DniResponse

identities_router = APIRouter(
    prefix="/identities",
    tags=["identities"],
)


@identities_router.get("/dni/{dni}", response_model=DniResponse)
async def get_dni(dni: str, q: Union[str, None] = None):
    response = get_dni_service(dni)
    return response
