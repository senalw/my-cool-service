package authz

import rego.v1

# Define input data
input_method := input.method
input_path := input.path
input_token := input.token

# Function to decode JWT token and extract payload
decode_jwt(token) = payload if {
    secret := opa.runtime()["env"]["SECRET_KEY"]
    io.jwt.verify_hs256(token, secret)
    [_, payload, _] := io.jwt.decode(token)
    print("Decoded JWT: ", payload)
}

# Function to validate token
valid_token(token) if {
    payload := decode_jwt(token)
    current_time := time.now_ns() / (1000 * 1000 * 1000)  # Convert to seconds
    payload.exp >= current_time
}

# Logging function
log_request(method, path, allowed) if {
    message := sprintf("Request: Method=%v Path=%v Allowed=%v", [method, path, allowed])
    print(message)
}

# Default policy
default allow := false

# Allow POST requests to "api/v1/users" only if user is an admin and token is valid
allow_post_users_api = allowed if {
    valid_token(input_token)
    payload := decode_jwt(input_token)
    allowed := payload.is_admin
}

# Allow GET requests to "api/v1/users" with a valid token
allow_get_users_api = allowed if {
    valid_token(input_token)
    allowed := true
}

# Allow POST requests if below conditions are met
allow if {
    input_method == "POST"
    input_path == "/api/v1/users"
    allowed := allow_post_users_api
    log_request(input_method, input_path, allowed)
    allowed == true
}

#Allow GET requests if below conditions are met
allow if {
    input_method == "GET"
    input_path == "/api/v1/users"
    allowed := allow_get_users_api
    log_request(input_method, input_path, allowed)
    allowed == true
}
