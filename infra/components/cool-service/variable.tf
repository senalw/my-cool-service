variable "prefix" {
  description = "What prefix will be used for the resources used for the deployment."
}

variable "namespace" {
  description = "Kubernetes namespace where OPA will be installed."
}

variable "my_cool_service_image" {
  description = "What docker image to use for My Cool Service."
}

variable "postgres_db"{
  description = "Name of the database in Postgres."
}

variable "postgres_user" {
  description = "User name of the Postgres database"
}

variable "postgres_password" {
  description = "Password of the Postgres database"
}

variable "postgres_address" {
  description = "Address of the postgres service"
}

variable "opa_address" {
  description = "Address of the Open Policy Agent"
}

variable "postgres_kubernetes_deployment" {
  description = "Name of the postgres k8s deployment"
}

variable "opa_kubernetes_deployment" {
  description = "Name of the postgres k8s deployment"
}

variable "client_secret" {
  description = "Client secret for OPA token decode"
}
