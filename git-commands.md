# GitHub Commands for QuizXMentor Project

## Initial Setup
```bash
# Initialize repository
git init

# Add remote repository
git remote add origin https://github.com/Maithiligithub19/MentorBaba-CICD.git

# Check remote
git remote -v
```

## Daily Workflow
```bash
# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Add CI/CD pipeline and deployment scripts"

# Push to main branch
git push origin main
```

## Branch Management
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge branch
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature
```

## Pipeline Trigger Commands
```bash
# Deploy to production (triggers Jenkins)
git add .
git commit -m "Deploy: Update quiz functionality"
git push origin main

# Hotfix deployment
git add .
git commit -m "Hotfix: Fix login issue"
git push origin main
```

## Quick Deploy
```bash
git add . && git commit -m "Deploy updates" && git push origin main
```