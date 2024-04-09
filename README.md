# My-Cool-Service 

Overview
---------
This API has below user stories implemented from FastAPI:

* As an authenticated user, I want to list all the users existing in the system.
* As an admin user, I want to add users to the system.
* As a user, I want to get JWT token for authentication.

This app contains three endpoints,
1. `POST -> /api/v1/auth/token`
   * This endpoint is used to get JWT token for user authentication. Default token validation time is 20 mins.
   * Sample request,
    ```
    curl -X 'POST' \
    'http://localhost:8010/api/v1/auth/token' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=&username=john&password=1234&scope=&client_id=&client_secret='
    ```
2. `POST -> /api/v1/user`
   * This endpoint is used to add new users to the system. Only admin users can add new users to the system.
   * Sample payload,
    ``` 
    curl -X 'POST' \
     'http://localhost:8010/api/v1/users' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
     "username": "string",
     "email": "user@example.com",
     "password": "********",
     "is_admin": true
   }'
    ```
3. `GET -> /api/v1/user`
   * Authenticated user can use this endpoint to list all the users in the system.
   * Sample request,
    ```
     curl -X 'GET' \
    'http://localhost:8010/api/v1/users' \
    -H 'accept: application/json'
    ```

Swagger UI: http://localhost:8010/docs

E.g.

![Screenshot 2024-04-09 at 08.30.45.png](..%2F..%2F..%2FDesktop%2FScreenshot%202024-04-09%20at%2008.30.45.png)

## Running App in minikube cluster
* Run `deploy.sh` [here](./infra/deploy.sh) to deploy the application on a minicube cluster. 
* Three pods will be deployed, postgres, OPA, service respectively.
* Then, it's possible to use [swagger-ui](http://localhost:8010/docs) to access the API.

Note: Two dummy admin and non-admin users will be added to the database when deploying the app.

| user     | username| password  |
|----------|---------|-----------|
| admin    | john    | 1234      |
| non-admin| Senal   |Senal@1234 |

## Running App in a single docker container

1. Build the image,
```shell
docker compose build
```

2. Run the services
```shell
docker compose up
```

Point your browser to [http://localhost:8010/docs](http://localhost:8010/docs) to access swagger UI.

### System Requirements
* Docker
* kubectl
* Terraform