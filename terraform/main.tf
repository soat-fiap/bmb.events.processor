##############################
# EKS CLUSTER
##############################

data "aws_eks_cluster" "techchallenge_cluster" {
  name = var.eks_cluster_name
}

locals {
  neo4j_uri             = base64encode(var.neo4j_uri)
  neo4j_user            = base64encode(var.neo4j_user)
  neo4j_password        = base64encode(var.neo4j_password)
  image_name            = var.docker_image
  aws_access_key_id     = base64encode(var.access_key_id)
  aws_secret_access_key = base64encode(var.secret_access_key)
}

resource "kubernetes_secret" "bmb_event_processor_neo4j" {
  metadata {
    name = "secret-bmb-event-processor-neo4j"
    labels = {
      app = "bmb-event-processor-neo4j"
    }
  }
  type = "Opaque"
  data = {
    NEO4J_URI             = local.neo4j_uri
    NEO4J_USER            = local.neo4j_user
    NEO4J_PASSWORD        = local.neo4j_password
    AWS_ACCESS_KEY_ID     = local.aws_access_key_id
    AWS_SECRET_ACCESS_KEY = local.aws_secret_access_key
  }
}

resource "kubernetes_cron_job" "bmb_event_processor_neo4j" {
  metadata {
    name = "bmb-event-processor-neo4j"
  }
  spec {
    schedule = "*/1 * * * *"
    job_template {
      metadata {}
      spec {
        template {
          metadata {}
          spec {
            container {
              name              = "bmb-event-processor"
              image             = local.image_name
              image_pull_policy = "IfNotPresent"
              env_from {
                secret_ref {
                  name = kubernetes_secret.bmb_event_processor_neo4j.metadata[0].name
                }
              }
            }
            restart_policy = "OnFailure"
          }
        }
      }
    }
  }
}
