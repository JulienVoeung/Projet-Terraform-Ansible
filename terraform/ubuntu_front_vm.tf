# Create virtual machine
resource "azurerm_linux_virtual_machine" "myterraformvm" {
  name                  = "myVM"
  location              = var.region
  resource_group_name   = azurerm_resource_group.myterraformgroup.name
  network_interface_ids = [azurerm_network_interface.myterraformnic.id]
  size                  = "Standard_DS1_v2"

  os_disk {
    name                 = "myOsDisk"
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = var.ubuntu_version
    version   = "latest"
  }

  computer_name                   = "myvm"
  admin_username                  = var.vm_user
  disable_password_authentication = true

  admin_ssh_key {
    username   = var.vm_user
    public_key = tls_private_key.example_ssh.public_key_openssh
  }

  boot_diagnostics {
    storage_account_uri = azurerm_storage_account.mystorageaccount.primary_blob_endpoint
  }

  tags = {
    environment = var.environment_name
  }
}
