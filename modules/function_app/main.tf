resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_storage_account" "sa" {
  name                     = var.storage_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "function_code" {
  name                  = "function-code"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "blob" # Public read access to blobs
}

resource "azurerm_storage_blob" "function_package" {
  name                   = "functionapp.zip"
  storage_account_name   = azurerm_storage_account.sa.name
  storage_container_name = azurerm_storage_container.function_code.name
  type                   = "Block"
  source                 = "path/to/functionapp.zip" # Your local zip file
}


resource "azurerm_app_service_plan" "plan" {
  name                = "${var.name}-plan"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "FunctionApp"

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_linux_function_app" "app" {
  name                       = var.function_name
  location                   = var.location
  resource_group_name        = var.resource_group_name
  service_plan_id            = azurerm_app_service_plan.plan.id
  storage_account_name       = var.storage_name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
    APP_ENVIRONMENT          = var.environment
    WEBSITE_RUN_FROM_PACKAGE = azurerm_storage_blob.function_package.url
  }
}
