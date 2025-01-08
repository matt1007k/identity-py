from typing import Union
from fastapi import APIRouter
from identities.services.get_dni_service import get_dni_service, DniData
from pydantic import BaseModel

dni_router = APIRouter(
    prefix="/dni",
    tags=["dni"],
)


class DniResponse(BaseModel):
    success: bool
    data: DniData | None


class NotFoundResponse(BaseModel):
    success: bool
    data: None
    message: str


@dni_router.get("/{dni}", response_model=DniResponse | NotFoundResponse)
async def get_dni(dni: str, api_key: Union[str, None] = None):
    try:
        dniData = get_dni_service(dni)
        print(dniData)
        return DniResponse(success=True, data=dniData)
    except:
        return NotFoundResponse(
            success=False, data=None, message="No se encontraron registros"
        )
