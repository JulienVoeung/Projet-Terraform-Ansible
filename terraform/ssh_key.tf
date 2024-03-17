# Create the SSH key
resource "tls_private_key" "example_ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_sensitive_file" "pem_file" {
  content              = tls_private_key.example_ssh.private_key_pem
  filename             = pathexpand("~/.ssh/${azurerm_linux_virtual_machine.myterraformvm.name}.pem")
  file_permission      = "600"
  directory_permission = "700"
}