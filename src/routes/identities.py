from typing import Union
from fastapi import APIRouter
from identities.services.get_dni_service import get_dni_service, DniData
from identities.services.get_ruc_service import get_ruc_service, RucData
from pydantic import BaseModel

identities_router = APIRouter(
    prefix="/identities",
    tags=["identities"],
)


class DniResponse(BaseModel):
    success: bool
    data: DniData | None


class RucResponse(BaseModel):
    success: bool
    data: RucData | None


class NotFoundResponse(BaseModel):
    success: bool
    data: None
    message: str


@identities_router.get("/dni/{dni}", response_model=DniResponse | NotFoundResponse)
async def get_dni(dni: str, q: Union[str, None] = None):
    try:
        dniData = get_dni_service(dni)
        print(dniData)
        return DniResponse(success=True, data=dniData)
    except:
        return NotFoundResponse(
            success=False, data=None, message="No se encontraron registros"
        )


@identities_router.get("/ruc/{ruc}", response_model=RucResponse | NotFoundResponse)
async def get_ruc(ruc: str, q: Union[str, None] = None):
    try:
        rucData = get_ruc_service(ruc)
        print(rucData)
        return RucResponse(success=True, data=rucData)
    except:
        return NotFoundResponse(
            success=False, data=None, message="No se encontraron registros"
        )
