param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$python = "C:\Users\IkerVélezdeMendizaba\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (-not (Test-Path $python)) {
    Write-Error "No se encontro el runtime Python de Codex en: $python"
    exit 1
}

& $python @Args
exit $LASTEXITCODE
