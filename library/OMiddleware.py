from fastapi import Request, HTTPException, status, responses, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from library.router import app
import time
from library.auth import AuthAction


# def check_path(self, path: str):
#     data = path_config.path_routes_not_auth
#     for pathx in data:
#         # print(pathx)
#         if path.find(pathx) != -1:
#             return False
#     return True

# app = router.app

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    token = request.headers.get('Authorization')
    base_path = request.base_url
    path = str(request.url).replace(str(base_path), "")
    # print(path)

    if AuthAction.validate(token, path):
        return await call_next(request)
    else:
        return responses.JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                  content="Could not validate credentials",
                                  headers={"WWW-Authenticate": "Bearer"})
