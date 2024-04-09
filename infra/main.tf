module "components" {
  source = "./components"

  namespace = var.namespace
  prefix    = var.prefix

  opa_image             = var.opa_image
  postgres_image        = var.postgres_image
  my_cool_service_image = var.my_cool_service_image

  postgres_db       = var.postgres_db
  postgres_user     = var.postgres_user
}