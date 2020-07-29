# Rocksonair

A simple python api that expose rocksdb over internet

## Run

- create the virtualenv: `python3 -m venv env`
- active: `. env/bin/activate`
- install deps: `pip install -r requirements.txt`
- create a `config.ini` like:

```ini
[rocksdb]
db_file = test.db
max_open_files = 300000
write_buffer_size = 67108864
max_write_buffer_number = 3
target_file_size_base = 67108864
filter_policy = 10
prefix_length = 5

[auth]
api_keys = apikey1,apikey2,testkpi
```

- run: `uvicorn main:app --reload`

## Docs

Open browser on <http://127.0.0.1/8000/docs>

### Tests

Run: `pytest`
**Note** in `config.js` the value `api_keys` must have `testkey`

## License

MIT
