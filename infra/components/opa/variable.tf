variable "prefix" {
  description = "What prefix will be used for the resources used for the deployment."
}

variable "namespace" {
  description = "Kubernetes namespace where OPA will be installed."
}

variable "opa_image" {
  description = "What docker image to use for Open Policy Agent."
}