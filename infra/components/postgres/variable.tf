variable "prefix" {
  description = "What prefix will be used for the resources used for the deployment."
}

variable "namespace" {
  description = "Kubernetes namespace where PostgreSQL will be installed."
}

variable "postgres_image" {
  description = "What docker image to use for Postgres."
}

variable "postgres_db"{
  description = "Name of the database in Postgres."
}

variable "postgres_user" {
  description = "User name of the Postgres database"
}
