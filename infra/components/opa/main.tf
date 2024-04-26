provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context_cluster = "minikube"
}

locals {
  opa_name = "${var.prefix}-opa"

  opa_labels = {
    app       = "opa"
    prefix    = var.prefix
    component = "opa"
  }

  opa_port = 8181
}

resource "random_password" "client-secret" {
  length = 16
}

resource "kubernetes_secret" "client-secret" {
  metadata {
    namespace = var.namespace
    name      = local.opa_name
  }

  data = {
    client-secret = random_password.client-secret.result
  }
}

resource "kubernetes_config_map" "opa-authz-policies" {
  metadata {
    namespace = var.namespace
    name      = "${local.opa_name}-policies"
  }

  data = {
    "authz.rego" = file("${path.cwd}/../authz/authz.rego")
  }
}

resource "kubernetes_config_map" "opa-authz-certs" {
  metadata {
    namespace = var.namespace
    name      = "${local.opa_name}-certs"
  }

  data = {
    "private.key" = file("${path.cwd}/../certs/opa/private.key")
    "public.crt" = file("${path.cwd}/../certs/opa/public.crt")
  }
}

resource "kubernetes_deployment" "opa" {
  metadata {
    namespace = var.namespace
    name      = local.opa_name
    labels    = local.opa_labels
  }

  spec {
    replicas = 1

    selector {
      match_labels = local.opa_labels
    }

    template {
      metadata {
        labels = local.opa_labels
      }

      spec {
        volume {
          name = "${local.opa_name}-policies"

          config_map {
            name = kubernetes_config_map.opa-authz-policies.metadata[0].name
          }
        }

        volume {
          name = "${local.opa_name}-certs"

          config_map {
            name = kubernetes_config_map.opa-authz-certs.metadata[0].name
          }
        }

        hostname = local.opa_name

        container {
          name  = local.opa_name
          image = var.opa_image
          image_pull_policy = "IfNotPresent"

          port {
            container_port = local.opa_port
          }

          # Mount local auth directory volume
          volume_mount {
            name       = "${local.opa_name}-policies"
            mount_path = "~/authz"
            read_only  = true
          }

          # Mount local certs/opa directory volume
          volume_mount {
            name        = "${local.opa_name}-certs"
            mount_path  = "~/certs"
            read_only   = true
          }

          env {
            name = "SECRET_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.client-secret.metadata[0].name
                key  = "client-secret"
              }
            }
          }

          # OPA container arguments
          command = ["opa"]
          args    = ["run", "--server", "--log-level", "info", "--ignore=.*", "--tls-cert-file", "~/certs/public.crt", "--tls-private-key-file", "~/certs/private.key", "~/authz"]
        }
      }
    }
  }
}

# Define Kubernetes Service for OPA
resource "kubernetes_service" "opa_service" {
  metadata {
    name      = local.opa_name
    namespace = var.namespace
  }

  spec {
    selector = {
      app = local.opa_labels.app
    }

    port {
      port        = local.opa_port
      target_port = local.opa_port
    }
  }
}
