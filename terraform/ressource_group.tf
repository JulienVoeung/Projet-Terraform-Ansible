# Create a resource group if it doesn't exist
resource "azurerm_resource_group" "myterraformgroup" {
  name     = "myResourceGroup"
  location = var.region

  tags = {
    environment = var.environment_name
  }
}