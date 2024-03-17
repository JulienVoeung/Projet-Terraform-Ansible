# Create public IPs
resource "azurerm_public_ip" "myterraformpublicip" {
  name                = "myPublicIP"
  location            = var.region
  resource_group_name = azurerm_resource_group.myterraformgroup.name
  allocation_method   = "Dynamic"

  tags = {
    environment = var.environment_name
  }
}

data "azurerm_public_ip" "example" {
  name                = azurerm_public_ip.myterraformpublicip.name
  resource_group_name = azurerm_linux_virtual_machine.myterraformvm.resource_group_name
}
