module "postgres" {
  source = "./postgres"

  namespace = var.namespace
  prefix    = var.prefix

  postgres_image = var.postgres_image

  postgres_db       = var.postgres_db
  postgres_user     = var.postgres_user
}

module "opa" {
  source = "./opa"

  namespace = var.namespace
  prefix    = var.prefix

  opa_image = var.opa_image
}

module "cool-service" {
  source = "./cool-service"

  namespace = var.namespace
  prefix    = var.prefix

  my_cool_service_image = var.my_cool_service_image

  opa_address                    = module.opa.internal_address
  postgres_address               = module.postgres.internal_address
  postgres_password              = module.postgres.postgres_password
  postgres_kubernetes_deployment = module.postgres.postgres_kubernetes_deployment
  opa_kubernetes_deployment      = module.opa.opa_kubernetes_deployment
  client_secret                  = module.opa.client_secret

  postgres_db   = var.postgres_db
  postgres_user = var.postgres_user
}
