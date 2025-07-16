variable "name" {
  description = "Base name for all resources, e.g., function app name prefix."
  type        = string
  validation {
    condition     = length(var.name) >= 3
    error_message = "The 'name' must be at least 3 characters long."
  }
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
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "resource_group_name" {
  description = "Name of the existing Azure Resource Group to deploy resources into."
  type        = string
}

variable "storage_account_name" {
  description = "Name of the Azure Storage Account for the Function App. Must be globally unique and lowercase, 3-24 characters."
  type        = string
  validation {
    condition     = length(var.storage_account_name) >= 3 && length(var.storage_account_name) <= 24
    error_message = "Storage account name must be between 3 and 24 characters."
  }
}
