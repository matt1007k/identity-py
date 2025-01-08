from typing import Union
from fastapi import APIRouter
from identities.services.get_ruc_service import get_ruc_service, RucData
from pydantic import BaseModel
from .dni import NotFoundResponse

ruc_router = APIRouter(
    prefix="/ruc",
    tags=["ruc"],
)


class RucResponse(BaseModel):
    success: bool
    data: RucData | None


@ruc_router.get("/{ruc}", response_model=RucResponse | NotFoundResponse)
async def get_ruc(ruc: str, api_key: Union[str, None] = None):
    try:
        rucData = get_ruc_service(ruc)
        print(rucData)
        return RucResponse(success=True, data=rucData)
    except:
        return NotFoundResponse(
            success=False, data=None, message="No se encontraron registros"
        )
