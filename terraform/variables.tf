variable "environment_name" {
  type    = string
  default = "Terraform Demo"
}

variable "region" {
  type    = string
  default = "eastus"
}

variable "vm_user" {
  type    = string
  default = "azureuser"
}

variable "ubuntu_version" {
  type    = string
  default = "20_04-lts"
}

variable "nb_back_vms" {
  type    = number
  default = 1
}