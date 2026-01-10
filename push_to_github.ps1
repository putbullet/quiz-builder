# GitHub Setup Script - Quiz Builder
# This script helps you push your Quiz Builder to GitHub

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Quiz Builder - GitHub Repository Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "[OK] Git is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git from: https://git-scm.com/downloads" -ForegroundColor Yellow
    Write-Host "After installation, restart PowerShell and run this script again." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""

# Check if already a git repository
if (Test-Path .git) {
    Write-Host "[!] This directory is already a Git repository" -ForegroundColor Yellow
    $response = Read-Host "Do you want to reinitialize? (y/n)"
    if ($response -ne 'y') {
        Write-Host "Aborted." -ForegroundColor Yellow
        pause
        exit 0
    }
}

# Get GitHub repository details
Write-Host ""
Write-Host "Please provide your GitHub repository details:" -ForegroundColor Cyan
Write-Host ""

$githubUsername = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter repository name (e.g. quiz-builder)"

if ([string]::IsNullOrWhiteSpace($githubUsername) -or [string]::IsNullOrWhiteSpace($repoName)) {
    Write-Host ""
    Write-Host "[ERROR] Username and repository name are required!" -ForegroundColor Red
    pause
    exit 1
}

$repoUrl = "https://github.com/$githubUsername/$repoName.git"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Repository URL: $repoUrl" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Confirmation
Write-Host "Before proceeding, make sure you have:" -ForegroundColor Yellow
Write-Host "  1. Created a repository on GitHub: $repoName" -ForegroundColor White
Write-Host "  2. Have your GitHub credentials ready" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Ready to proceed? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "Aborted." -ForegroundColor Yellow
    pause
    exit 0
}

Write-Host ""
Write-Host "Initializing Git repository..." -ForegroundColor Cyan

# Initialize git if needed
if (-not (Test-Path .git)) {
    git init
    Write-Host "[OK] Git repository initialized" -ForegroundColor Green
}

# Configure git (optional)
$configName = git config user.name
if ([string]::IsNullOrWhiteSpace($configName)) {
    Write-Host ""
    $name = Read-Host "Enter your name for Git commits"
    $email = Read-Host "Enter your email for Git commits"
    
    git config user.name "$name"
    git config user.email "$email"
    Write-Host "[OK] Git user configured" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "Adding files to Git..." -ForegroundColor Cyan
git add .
Write-Host "[OK] Files added" -ForegroundColor Green

# Create initial commit
Write-Host ""
Write-Host "Creating initial commit..." -ForegroundColor Cyan
git commit -m "Initial commit: Quiz Builder application with GUI and live exam delivery"
Write-Host "[OK] Commit created" -ForegroundColor Green

# Add remote
Write-Host ""
Write-Host "Adding remote repository..." -ForegroundColor Cyan
git remote remove origin 2>$null
git remote add origin $repoUrl
Write-Host "[OK] Remote added" -ForegroundColor Green

# Push to GitHub
Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
Write-Host "You may be prompted for your GitHub credentials..." -ForegroundColor Yellow
Write-Host ""

git push -u origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[!] Push failed. Trying 'master' branch..." -ForegroundColor Yellow
    git branch -M main
    git push -u origin main
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Repository pushed to GitHub" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your repository is now available at:" -ForegroundColor Cyan
    Write-Host "  https://github.com/$githubUsername/$repoName" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Visit your repository on GitHub" -ForegroundColor White
    Write-Host "  2. Add a description and topics" -ForegroundColor White
    Write-Host "  3. Share with others!" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  1. Repository doesn't exist on GitHub - Create it first" -ForegroundColor White
    Write-Host "  2. Wrong credentials - Check username/password" -ForegroundColor White
    Write-Host "  3. Need Personal Access Token instead of password" -ForegroundColor White
    Write-Host "     Get token at: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host ""
    Write-Host "Manual push command:" -ForegroundColor Yellow
    Write-Host "  git push -u origin main" -ForegroundColor White
}

Write-Host ""
pause
