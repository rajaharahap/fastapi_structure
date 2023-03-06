import router
from fastapi.middleware.cors import CORSMiddleware

"""
setting origins for request

example :
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
"""

origins = [
    "*"
]

"""
add middleware cors
"""
app = router.app

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)