## Getting Started

1. Rename ```.env.dist``` to ```.env```

2. Generate two keys using the following command

> Make sure you have ```pycryptodome==3.20.0``` installed

```
python -c "from base64 import b64encode; from Crypto.Random import get_random_bytes; print(b64encode(get_random_bytes(32)))"
```

3. Fill in the values for ```JWT_SECRET_KEY``` and ```SECRET_KEY``` in .env

4. Set a desired username and password for the super admin. And a strong password!

> Please note: for security reasons it is not allowed to login using the super admin using the API.

5. ```docker-compose up```

6. The frontend is accessible on port ```80```, the api docs are accessible on ```/api/v1/docs```.
