param(
    [ValidateSet("smoke", "logs", "books", "db", "flow", "all")]
    [string]$Suite = "all"
)

$ErrorActionPreference = "Stop"

$ApiTestsRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ApiTestsRoot

$PythonCommand = "python"
try {
    & $PythonCommand --version | Out-Null
}
catch {
    $PythonCommand = "py"
}

switch ($Suite) {
    "smoke" {
        & $PythonCommand -m pytest -m smoke
    }
    "logs" {
        & $PythonCommand -m pytest -m logs
    }
    "books" {
        & $PythonCommand -m pytest -m books
    }
    "db" {
        & $PythonCommand -m pytest -m "db and consistency"
    }
    "flow" {
        & $PythonCommand -m pytest -m flow
    }
    "all" {
        & $PythonCommand -m pytest --alluredir=allure-results
    }
}
