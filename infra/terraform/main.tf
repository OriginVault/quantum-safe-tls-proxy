provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

# AWS ECS Cluster
resource "aws_ecs_cluster" "proxy_cluster" {
  name = "QuantumSafeTLSProxyCluster"
}

resource "aws_security_group" "proxy_security_group" {
  name        = "proxy_security_group"
  description = "Security group for the Quantum Safe TLS Proxy"
  vpc_id      = var.aws_vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Azure Network Security Group
resource "azurerm_network_security_group" "proxy_nsg" {
  name                = "proxy-nsg"
  location            = var.azure_location
  resource_group_name = var.azure_resource_group

  security_rule {
    name                       = "allow_https"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# GCP Firewall Rule
resource "google_compute_firewall" "proxy_firewall" {
  name    = "proxy-firewall"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  source_ranges = ["0.0.0.0/0"]

  target_tags = ["proxy-service"]
}
