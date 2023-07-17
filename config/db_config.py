from dotenv import dotenv_values

config = dotenv_values(".env")

db_config = {
    "host": config["DB_HOST"],
    "port": config["DB_PORT"],
    "db": config["DB_NAME"],
    "username": config["DB_USER"],
    "password": config["DB_PASSWORD"],
    "dbType": config["DB_TYPE"],
}
