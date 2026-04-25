# block-dangerous.ps1 — Blocks destructive shell commands before execution
# Fires on PreToolUse (Bash tool). Exit code 2 = block with message.

param([string]$Command = "")

$dangerous = @(
    'rm -rf /',
    'rm -rf ~',
    'Remove-Item -Recurse -Force C:\',
    'Format-Volume',
    'del /s /q C:\',
    'git push --force origin main',
    'git push --force origin dev',
    'git reset --hard',
    'DROP DATABASE',
    'DROP TABLE',
    'db.dropDatabase()'
)

foreach ($pattern in $dangerous) {
    if ($Command -like "*$pattern*") {
        Write-Error "BLOCKED: Dangerous command detected: '$pattern'. Review CLAUDE.md unbreakable rules."
        exit 2
    }
}

exit 0
