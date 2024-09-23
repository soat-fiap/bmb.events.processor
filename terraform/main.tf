##############################
# EKS CLUSTER
##############################

data "aws_eks_cluster" "techchallenge_cluster" {
  name = var.eks_cluster_name
}

##############################
# SQS QUEUE
##############################

data "aws_sqs_queue" "queue" {
  name = var.queue_name
}

locals {
  neo4j_uri             = var.neo4j_uri
  neo4j_user            = var.neo4j_user
  neo4j_password        = var.neo4j_password
  image_name            = var.docker_image
  aws_access_key_id     = var.access_key_id
  aws_secret_access_key = var.secret_access_key
  queue_url             = data.aws_sqs_queue.queue.url
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


resource "kubernetes_manifest" "bmb_event_processor_neo4j_cronjob" {
  manifest = {
    apiVersion = "batch/v1"
    kind       = "CronJob"
    metadata = {
      name      = "bmb-event-processor-neo4j"
      namespace = "default"
    }
    spec = {
      schedule = "*/3 * * * *"
      jobTemplate = {
        spec = {
          template = {
            spec = {
              containers = [
                {
                  name  = "bmb-event-processor"
                  image = local.image_name
                  env = [
                    {
                      name  = "QUEUE_URL"
                      value = local.queue_url
                    },
                    {
                      name = "NEO4J_URI"
                      valueFrom = {
                        secretKeyRef = {
                          name = kubernetes_secret.bmb_event_processor_neo4j.metadata[0].name
                          key  = "NEO4J_URI"
                        }
                      }
                    },
                    {
                      name = "NEO4J_USER"
                      valueFrom = {
                        secretKeyRef = {
                          name = kubernetes_secret.bmb_event_processor_neo4j.metadata[0].name
                          key  = "NEO4J_USER"
                        }
                      }
                    },
                    {
                      name = "NEO4J_PASSWORD"
                      valueFrom = {
                        secretKeyRef = {
                          name = kubernetes_secret.bmb_event_processor_neo4j.metadata[0].name
                          key  = "NEO4J_PASSWORD"
                        }
                      }
                    }
                  ]
                }
              ]
              restartPolicy = "OnFailure"
            }
          }
        }
      }
    }
  }
}