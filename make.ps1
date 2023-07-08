param([string]$command)

$venv = $env:VENV
if ([string]::IsNullOrEmpty($venv)) {
    $venv = "venv"
}

function Activate-Venv([string]$venv) {
    python -m venv "$venv"
    Write-Host "Activating environment '$venv'"
    & ./$venv/Scripts/Activate.ps1
}

function Pip-Tools-Compile {
    Write-Host "Compile  packages into 'requirements-win.txt'..."
    python -m piptools compile --extra=dev --resolver=backtracking --no-emit-index-url -o requirements-win.txt pyproject.toml
}

function Pip-Tools-Sync {
    Write-Host "Syncing packages in 'requirements-win.txt' with the activated environment..."
    python -m piptools sync "requirements-win.txt"
    python -m pip install -e .
}


switch ($command) {
    "install_dev" {
        Activate-Venv -venv $venv
        python -m pip install -r requirements-win.txt
        python -m pip install -e .
        python -m pre_commit install
        break
    }
    "compile" {
        Activate-Venv -venv $venv
        Pip-Tools-Compile
        break
    }
    "sync" {
        Activate-Venv -venv $venv
        Pip-Tools-Sync
        break
    }
    "up" {
        Activate-Venv -venv $venv
        Pip-Tools-Compile
        Pip-Tools-Sync
        break
    }
    "compile-docs" {
        Activate-Venv -venv $venv
        Write-Host "Compile packages into 'docs/requirements-docs-win.txt'..."
        python -m piptools compile --extra=docs --resolver=backtracking --no-emit-index-url -o docs/requirements-docs.txt pyproject.toml
    }
}