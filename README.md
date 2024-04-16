# My-Cool-Service 

Overview
---------
This API has below user stories implemented from FastAPI:

* As an authenticated user, I want to list all the users existing in the system.
* As an admin user, I want to add users to the system.
* Non-admin users should be able to add users to the system.
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

1. Generate certificates
```shell
cd infra && ./generate_certificates.sh
```

2. Build the image,
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

### Security Best Practices Followed
* Store only hashed passwords in the database. 
* Always generate random passwords/secrets in terraform when deploying applications
* Secrets are not hard-coded in config files or source code.
* Input field validations. E.g email, password (validate password strength)
* Running service docker container as non-root user to limit the potential damage in case of security breach.
* Enable encrypted communication between my-cool-service and the Open Policy Agent. (HTTPS)
* When sign-in, JWT token validity period is set to 20 mins. (Configurable in config file [here](./resources/config.ini))
* Logging all authentication and authorization requests.
* Only admin users can add users to the system.
* Use OPA for authorization.

### Improvements
1. Implement unit tests to cover at least basic scenarios.
2. Use secret management solution like AWS Secret Manager or HashiCorp Vault.
3. Enable encryption in my-cool-service. (HTTPS)
4. Implement RBAC (Role Based Access Control) in the K8S cluster.
5. Scan codebase from static code analysis tool to find security issues. E.g. Snyc code
