## Getting Started

1. Rename .env.dist to .env

2. Generate ```SECRET_KEY```

```
pip install pycryptodome==3.20.0
python -c "from base64 import b64encode; from Crypto.Random import get_random_bytes; print(b64encode(get_random_bytes(32)))"
```

3. Copy output from the commands above into the ```SECRET_KEY``` variable in .env

4. docker-compose up

The frontent is accessible on ```localhost:80/```, and the api docs are accessible on ```localhost:80/api/v1/docs```.
