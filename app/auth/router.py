from fastapi.routing import APIRouter
from .schemas import RegisterRequest, RegisterResponse

router = APIRouter(prefix="auth")


@router.post("/signup", response_model=RegisterResponse)
async def authorize(request: RegisterRequest) -> bool:

    return RegisterResponse(verified=False)


@router.post("/login")
async def login(): ...


@router.post("/refresh")
async def refresh(): ...
