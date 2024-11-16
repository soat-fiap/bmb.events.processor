terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.62.0"
    }
  }
  required_version = "~>1.9.4"
}

provider "aws" {
  region  = var.region
  alias   = "us-east-1"

  default_tags {
    tags = {
      ManagedBy = "Terraform"
    }
  }
}

##############################
# EKS CLUSTER
##############################

data "aws_eks_cluster" "techchallenge_cluster" {
  name = var.eks_cluster_name
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.techchallenge_cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.techchallenge_cluster.certificate_authority[0].data)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    # This requires the awscli to be installed locally where Terraform is executed
    args = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.techchallenge_cluster.name]
  }
}