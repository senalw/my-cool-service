provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context_cluster = "minikube"
}

locals {
  postgres_name = "${var.prefix}-postgres"

  postgres_labels = {
    app       = "postgres"
    prefix    = var.prefix
    component = "postgres"
  }

  postgres_port = 5432
}

resource "random_password" "postgres_password" {
  length = 16
}

resource "kubernetes_secret" "postgres-user" {
  metadata {
    namespace = var.namespace
    name      = var.postgres_user
  }

  data = {
    username = var.postgres_user
    password = random_password.postgres_password.result
  }
}

resource "kubernetes_deployment" "postgres" {
  metadata {
    namespace = var.namespace
    name      = local.postgres_name
    labels    = local.postgres_labels
  }

  spec {
    replicas = 1
    strategy {
      // Due to the volume claims, we cannot do a RollingUpdate here. As the claims would block the
      // new instance(s) from ever becoming healthy, thus blocking the update forever.
      type = "Recreate"
    }
    selector {
      match_labels = local.postgres_labels
    }

    template {
      metadata {
        labels = local.postgres_labels
      }

      spec {
        volume {
          name = "postgres-data"

          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.postgres_data.metadata[0].name
          }
        }
        hostname = local.postgres_name

        container {
          name  = local.postgres_name
          image = var.postgres_image
          image_pull_policy = "IfNotPresent"

          port {
            container_port = local.postgres_port
          }

          env {
            name  = "POSTGRES_DB"
            value = var.postgres_db
          }

          env {
            name = "POSTGRES_USER"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.postgres-user.metadata[0].name
                key  = "username"
              }
            }
          }

          env {
            name  = "POSTGRES_PASSWORD"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.postgres-user.metadata[0].name
                key  = "password"
              }
            }
          }

          volume_mount {
            name       = "postgres-data"
            mount_path = "/var/lib/postgresql/data"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "postgres" {
  metadata {
    name      = local.postgres_name
    namespace = var.namespace
  }

  spec {
    selector = {
      app = local.postgres_labels.app
    }

    port {
      port        = local.postgres_port
      target_port = local.postgres_port
    }
  }
}

resource "kubernetes_persistent_volume_claim" "postgres_data" {
  metadata {
    namespace = var.namespace
    name      = "postgres-data"
    labels    = local.postgres_labels
  }

  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }
  }

  wait_until_bound = false
}
