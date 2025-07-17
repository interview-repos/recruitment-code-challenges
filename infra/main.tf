module "function_app" {
  source                = "../modules/function_app"
  function_app_name     = var.function_app_name
  app_service_plan_name = var.app_service_plan_name
  location              = var.location
  resource_group_name   = var.resource_group_name
  storage_account_name  = var.storage_account_name
  environment           = var.environment
}
