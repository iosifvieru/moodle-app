# Iosif Vieru 1409A
# 3.11.2024

from fastapi import APIRouter, HTTPException
from idm_client import validate

"""
Maximum char length accepted by the request
"""
MAX_SIZE = 200

"""
Generates hateoas links for a specific route.
"""
def generate_hateoas_links(router: APIRouter, route_name: str, **kwargs) -> dict:
    try:
        url = router.url_path_for(route_name, **kwargs)
    except:
        url = router.url_path_for(route_name)
    
    query_params = "&".join(f"{key}={value}" for key, value in kwargs.items() if value is not None)
    
    if query_params:
        url = f"{url}?{query_params}"
    
    return {"href": url}

"""
validates the bearer token
calls grpc server
"""

def validate_token(jwt: str):
    if jwt is None:
        raise HTTPException(status_code=401, detail="Invalid authorization.")

    if jwt:
        parts = jwt.split(" ")
        bearer = parts[0]
        token = parts[1]

        if validate(token) == False:
            raise HTTPException(status_code=401, detail="Invalid authorization.")

