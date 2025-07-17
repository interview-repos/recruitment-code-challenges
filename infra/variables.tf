variable "function_app_name" {
  description = "Function App Name"
  type        = string
}

variable "app_service_plan_name" {
  description = "The name of the app service plan"
  type        = string
}

variable "location" {
  description = "Azure region where resources will be deployed, e.g., East US."
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Deployment environment identifier, e.g., dev, staging, prod."
  type        = string
  default     = "dev"
}

variable "resource_group_name" {
  description = "Name of the existing Azure Resource Group to deploy resources into."
  type        = string
}

variable "storage_account_name" {
  description = "Name of the Azure Storage Account for the Function App. Must be globally unique and lowercase, 3-24 characters."
  type        = string
}
