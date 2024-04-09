variable "namespace" {
  description = "Kubernetes namespace where components will be installed."
  default = "default"
  type = string
}

variable "prefix"{
  description = "What prefix will be used for the resources used for the deployment. This will also be used as the next level subdomain"
  default = "swisscom"
  type = string
}

variable "opa_image" {
  description = "What docker image to use for Open Policy Agent"
}

variable "postgres_image" {
  description = "What docker image to use for Postgres"
}

variable "my_cool_service_image" {
  description = "What docker image to use for My Cool Service."
}

variable "postgres_db"{
  description = "Name of the database in Postgres."
  default = "my-cool-service"
}

variable "postgres_user" {
  description = "User name of the Postgres database"
  default = "cool-service"
}