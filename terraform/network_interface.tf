# Create network interface
resource "azurerm_network_interface" "myterraformnic" {
  name                = "myNIC"
  location            = var.region
  resource_group_name = azurerm_resource_group.myterraformgroup.name

  ip_configuration {
    name                          = "myNicConfiguration"
    subnet_id                     = azurerm_subnet.myterraformsubnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.myterraformpublicip.id
  }

  tags = {
    environment = var.environment_name
  }
}

# Create network interface
resource "azurerm_network_interface" "internal_network" {
  count               = var.nb_back_vms
  name                = "internalNIC-${count.index}"
  location            = var.region
  resource_group_name = azurerm_resource_group.myterraformgroup.name

  ip_configuration {
    name                          = "internalNIC-${count.index}"
    subnet_id                     = azurerm_subnet.myterraformsubnet.id
    private_ip_address_allocation = "Dynamic"
  }

  tags = {
    environment = var.environment_name
  }
}

# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "example" {
  network_interface_id      = azurerm_network_interface.myterraformnic.id
  network_security_group_id = azurerm_network_security_group.myterraformnsg.id
}