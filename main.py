from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from security import check_authentication_header
from models import Item, User, ItemBatch
from rocks import init, createWriteBatch
from typing import List

db = init()

app = FastAPI()

@app.post("/storage/single", status_code=201)
def put_item(item: Item, user: User = Depends(check_authentication_header)):
    db.put(bytes(item.key, 'utf-8'), bytes(item.value, 'utf-8'))
    return {"detail": "success"}


@app.get("/storage/single/{key}", status_code=200)
def get_item(key: str, user: User = Depends(check_authentication_header)):
    value = db.get(bytes(key, 'utf-8'))
    print(value)
    if value == None:  
        raise HTTPException(
            status_code=404,
            detail="Not found",
        )
    return {"key": key, "value": value.decode('utf-8')}


@app.delete("/storage/single/{key}", status_code=200)
def delete_item(key: str, user: User = Depends(check_authentication_header)):
    db.delete(bytes(key, 'utf-8'))
    return {"detail": "success"}

# TODO batch https://python-rocksdb.readthedocs.io/en/latest/tutorial/
@app.post("/storage/batch", status_code=201)
def put_items(items: List[ItemBatch], user: User = Depends(check_authentication_header)):
    batch = createWriteBatch(items)
    db.write(batch)
    return {"detail": "success"}

    
# TODO prefix ? https://python-rocksdb.readthedocs.io/en/latest/tutorial/#prefixextractor
