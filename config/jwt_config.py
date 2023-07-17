from dotenv import dotenv_values

config = dotenv_values(".env")

jwt_profile = {
    "key": config["JWT_KEY"],
    "algoritma": config["JWT_ALGORITHM"],
}
