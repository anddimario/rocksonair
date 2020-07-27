from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

X_API_KEY = APIKeyHeader(name='X-API-Key')

# based on https://github.com/tiangolo/fastapi/issues/142#issuecomment-563274226
def check_authentication_header(x_api_key: str = Depends(X_API_KEY)):
    # Get api keys from config
    api_keys = config["auth"]["api_keys"]

    if x_api_key in api_keys.split(","):
        # if passes validation check, return user data for API Key
        return {
            "api_key": x_api_key,
        }
    # else raise 401
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key"
    )