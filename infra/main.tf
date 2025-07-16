module "function_app" {
  source               = "/modules/function_app"
  name                 = var.name
  location             = var.location
  resource_group_name  = var.resource_group_name
  storage_account_name = var.storage_account_name
  environment          = var.environment
}
