package authz

import rego.v1

# Define input data
input_method := input.method
input_path := input.path
input_token := input.token

# Function to decode JWT token and extract payload
decode_jwt(token) = payload if{
   [_, encoded_payload, _] := split(token, ".")
    payload_bytes := base64url.decode(encoded_payload)
    payload := json.unmarshal(payload_bytes)
}

# Function to validate token
valid_token(token) if {
    payload := decode_jwt(token)
    current_time := time.now_ns() / (1000 * 1000 * 1000)  # Convert to seconds
    payload.exp >= current_time
}

# Default policy
default allow := false

# Allow POST requests to "api/v1/users" only if user is an admin and token is valid
allow_post_users_api if {
    valid_token(input_token)
    payload := decode_jwt(input_token)
    payload.is_admin == true
}

# Allow GET requests to "api/v1/users" with a valid token
allow_get_users_api if {
    valid_token(input_token)
}

# Allow POST requests if below conditions are met
allow if {
    input_method == "POST"
    input_path == "/api/v1/users"
    allow_post_users_api
}

#Allow GET requests if below conditions are met
allow if {
    input_method == "GET"
    input_path == "/api/v1/users"
    allow_get_users_api
}
