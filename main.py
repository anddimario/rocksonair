import configparser
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from typing import List
import itertools

from security import check_authentication_header
from models import Item, User, ItemBatch
from rocks import init, create_write_batch

config = configparser.ConfigParser()
config.read('config.ini')

db = init()

app = FastAPI()

@app.post("/storage/single", status_code=201)
def put_item(item: Item, user: User = Depends(check_authentication_header)):
    db.put(bytes(item.key, 'utf-8'), bytes(item.value, 'utf-8'))
    return {"detail": "success"}


@app.get("/storage/single/{key}", status_code=200)
def get_item(key: str, user: User = Depends(check_authentication_header)):
    value = db.get(bytes(key, 'utf-8'))
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

@app.post("/storage/batch", status_code=200)
def put_items(items: List[ItemBatch], user: User = Depends(check_authentication_header)):
    batch = create_write_batch(items)
    db.write(batch)
    return {"detail": "success"}

@app.get("/storage/batch", status_code=200)
def get_items(keys: str, user: User = Depends(check_authentication_header)):
    print(keys)
    new_keys = []
    # create bytes keys
    for key in keys.split(","):
        new_keys.append(bytes(key, 'utf-8'))
    values = db.multi_get(new_keys)
    return {"detail": "success", "value": values}
    
@app.get("/storage/keys", status_code=200)
def iterate(order: str, limit: Optional[int] = None, user: User = Depends(check_authentication_header)):
    it = db.iterkeys()
    if order == "last":
        it.seek_to_last()
    elif order == "first":
        it.seek_to_first()
    else:
        raise HTTPException(
            status_code=400,
            detail="Order not allowed",
        )
    keys = list(it)
    if limit != None:
        keys = keys[0:limit]
    return {"detail": "success", "value": keys}

@app.get("/storage/iterate/{prefix}", status_code=200)
def iterate_prefix(prefix: Optional[str] = None, limit: Optional[int] = None, user: User = Depends(check_authentication_header)):
    max_prefix_length = int(config['rocksdb']['prefix_length'])
    if len(prefix) > max_prefix_length:
        raise HTTPException(
            status_code=400,
            detail="Prefix length must be {}".format(max_prefix_length),
        )
    encoded_prefix = bytes(prefix, 'utf-8')
    it = db.iteritems()
    it.seek(encoded_prefix)
    keys = dict(itertools.takewhile(lambda item: item[0].startswith(encoded_prefix), it))
    if limit != None:
        keys = keys[0:limit]
    return {"detail": "success", "value": keys}