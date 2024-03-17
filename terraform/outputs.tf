output "instance_ip_addr" {
  value = data.azurerm_public_ip.example.ip_address
}

output "all_internal_ips" {
  value = azurerm_network_interface.internal_network[*].ip_configuration[*].private_ip_address
}