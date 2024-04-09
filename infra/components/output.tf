output "postgres_address" {
  value = module.postgres.internal_address
}

output "opa_address" {
  value = module.opa.internal_address
}

output "postgres_kubernetes_deployment" {
  value = module.postgres.postgres_kubernetes_deployment
}

output "opa_kubernetes_deployment" {
  value = module.opa.opa_kubernetes_deployment
}
