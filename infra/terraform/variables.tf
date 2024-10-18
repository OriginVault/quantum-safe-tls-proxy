# AWS Variables
variable "aws_region" {
  description = "The AWS region to deploy the ECS cluster"
  type        = string
  default     = "us-west-2"
}

variable "aws_vpc_id" {
  description = "The ID of the VPC where resources will be deployed"
  type        = string
}

# Azure Variables
variable "azure_location" {
  description = "The location for Azure resources"
  type        = string
  default     = "East US"
}

variable "azure_resource_group" {
  description = "The name of the Azure Resource Group"
  type        = string
}

# GCP Variables
variable "gcp_project" {
  description = "The GCP project ID"
  type        = string
}

variable "gcp_region" {
  description = "The GCP region for deployment"
  type        = string
  default     = "us-central1"
}
