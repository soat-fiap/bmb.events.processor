variable "neo4j_uri" {
  description = "The URI for the Neo4j database"
  type        = string
  default     = "neo4j+s://5a219891.databases.neo4j.io"
}

variable "neo4j_user" {
  description = "The username for the Neo4j database"
  type        = string
  default     = "neo4j"
}

variable "neo4j_password" {
  description = "The password for the Neo4j database"
  type        = string
  sensitive   = true
  default     = "bk3AI_CP8USMsqc_9uf4YcoDEu1Bv5_cktZlY2tNY4s"
}

variable "docker_image" {
  default     = "bmb-events-processor:latest"
  description = "Docker image"
  type        = string
}

variable "access_key_id" {
  description = "AWS Access Key ID"
  type        = string
  default     = "value"
  sensitive   = true
}

variable "secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
  default     = "value"
  sensitive   = true
}

variable "region" {
  description = "The AWS region"
  type        = string
  default     = "us-east-1"
}

variable "eks_cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
  default     = "quixada"
}
