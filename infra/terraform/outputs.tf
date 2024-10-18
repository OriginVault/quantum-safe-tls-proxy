output "aws_ecs_cluster_name" {
  description = "The name of the AWS ECS cluster"
  value       = aws_ecs_cluster.proxy_cluster.name
}

output "aws_security_group_id" {
  description = "The ID of the AWS Security Group"
  value       = aws_security_group.proxy_security_group.id
}

output "azure_nsg_id" {
  description = "The ID of the Azure Network Security Group"
  value       = azurerm_network_security_group.proxy_nsg.id
}

output "gcp_firewall_rule_name" {
  description = "The name of the GCP Firewall rule"
  value       = google_compute_firewall.proxy_firewall.name
}
