provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context_cluster = "minikube"
}

locals {
  service_name = "${var.prefix}-cool-service"

  service_labels = {
    app       = "cool-service"
    prefix    = var.prefix
    component = "cool-service"
  }

  service_port = 8010
}


resource "kubernetes_deployment" "my-cool-service" {

  depends_on = [
    var.postgres_kubernetes_deployment,
    var.opa_kubernetes_deployment
  ]
  metadata {
    namespace = var.namespace
    name      = local.service_name
    labels    = local.service_labels
  }

  spec {
    replicas = 1

    selector {
      match_labels = local.service_labels
    }

    template {
      metadata {
        labels = local.service_labels
      }

      spec {
        container {
          name  = local.service_name
          image = var.my_cool_service_image
          image_pull_policy = "IfNotPresent"

          env {
            name  = "DB_URL"
            value = "postgresql+psycopg2://${var.postgres_user}:${urlencode(var.postgres_password)}@${var.postgres_address}/${var.postgres_db}"
          }

          env{
            name = "TOKEN_URL"
            value = "https://localhost:${local.service_port}/api/v1/auth/token"
          }

          env {
            name = "OPA_URL"
            value = "https://${var.opa_address}/v1/data/authz"
          }

          env {
            name = "SECRET_KEY"
            value_from {
              secret_key_ref {
                name = var.client_secret
                key  = "client-secret"
              }
            }
          }

          port {
            container_port = local.service_port
          }
        }
      }
    }
  }
}

# Define Kubernetes Service for My Cool Service
resource "kubernetes_service" "my-cool-service" {
  metadata {
    name      = local.service_name
    namespace = var.namespace
  }

  spec {
    selector = {
      app = local.service_labels.app
    }

    port {
      port        = local.service_port
      target_port = local.service_port
    }
  }
}
