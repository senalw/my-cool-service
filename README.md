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
    E.g. Get JWT token for authentication,
   ![authorization.png](static%2Fauthorization.png)

2. `POST -> /api/v1/user`
   * This endpoint is used to add new users to the system. Only admin users can add new users to the system.
   * Sample request,
    ``` 
   curl -X 'POST' \
     'http://localhost:8010/api/v1/users' \
     -H 'accept: application/json' \
     -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTI2NjE1NzEuNjgwODQ2LCJpZCI6MiwidXNlcm5hbWUiOiJTZW5hbCIsImlzX2FkbWluIjpmYWxzZX0.8IjI2EAD9vPThrBe47-HYxHoHulZ2Um2ZBMsiYXEF24' \
     -H 'Content-Type: application/json' \
     -d '{
     "username": "Adam",
     "email": "adam@example.com",
     "password": "Adam@123",
     "is_admin": true
   }'
    ```
   
   E.g. Trying to create a new user by a non-admin user,
     ![non-admin-user-creation.png](static%2Fnon-admin-user-creation.png)


3. `GET -> /api/v1/user`
   * Authenticated user can use this endpoint to list all the users in the system.
   * Sample request,
    ```
   curl -X 'GET' \
   'http://localhost:8010/api/v1/users' \
   -H 'accept: application/json' \
   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTI2NjE1NzEuNjgwODQ2LCJpZCI6MiwidXNlcm5hbWUiOiJTZW5hbCIsImlzX2FkbWluIjpmYWxzZX0.8IjI2EAD9vPThrBe47-HYxHoHulZ2Um2ZBMsiYXEF24'
    ```
   E.g: Get users by an authenticated user,
      ![non-admin-get-users.png](static%2Fnon-admin-get-users.png)

Swagger UI: http://localhost:8010/docs

E.g.

![swagger-ui.png](static%2Fswagger-ui.png)

## Running App in a minikube cluster
* Run `deploy.sh` [here](./infra/deploy.sh) to deploy the application on a minicube cluster. 
* Three pods will be deployed. i.e. postgres, OPA, and my-cool-service respectively.
* Then, it's possible to use [swagger-ui](http://localhost:8010/docs) to access the API.

Note: Two dummy users (admin and non-admin) will be added to the database when deploying the app.

| user     | username| password |
|----------|---------|----------|
| admin    | john    | 1234     |
| non-admin| Senal   |Senal@123 |

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

### Improvements 
1. Implement TLS communication between the my-cool-service and the Open Policy Agent.
2. Implement unit tests to cover at least basic scenarios.