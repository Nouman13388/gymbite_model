# Git LFS setup (Windows PowerShell)

This file explains how to enable Git LFS for `enhanced_diet_predictor.pkl` so you can push the model to remote (e.g., GitHub or Hugging Face Spaces backed by Git).

Important notes before you begin:

- If `enhanced_diet_predictor.pkl` was already committed in history, you must migrate it into LFS and rewrite history (see the "Migrate existing large files into LFS" section).

- If your `.gitignore` currently contains a rule that ignores `*.pkl` or `enhanced_diet_predictor.pkl`, remove that line before tracking the file with LFS.

## Install Git LFS (one-time per machine)

If you don't already have Git LFS installed, follow one of these options:

- Use the official installer from the [Git LFS site](https://git-lfs.github.com/) (download and run the installer for Windows).

- If you have Chocolatey: `choco install git-lfs` (run PowerShell as Administrator first).

After installing, run (PowerShell):

```powershell
git lfs install
```

## Ensure `.gitignore` will not block the file

Check whether `enhanced_diet_predictor.pkl` is ignored:

```powershell
git check-ignore -v enhanced_diet_predictor.pkl
```

If that shows a matching rule (for example `*.pkl`), open `.gitignore` and remove or comment out the line that blocks the specific file you want to track.

## Track the file with Git LFS and commit

```powershell
# Track the specific file (creates/updates .gitattributes)
git lfs track "enhanced_diet_predictor.pkl"

# Add .gitattributes and the model file
git add .gitattributes
git add enhanced_diet_predictor.pkl

# Commit and push as usual
git commit -m "chore: track enhanced_diet_predictor.pkl with Git LFS"
git push origin dev
```

## (Optional) Track all .pkl files instead of a single file

```powershell
git lfs track "*.pkl"
git add .gitattributes
git commit -m "chore: track .pkl files with Git LFS"
```

## Migrate existing local history into LFS (only if the large file already exists in commits)

If the large file was previously committed and you need to move it into LFS across history, use git-lfs migrate. This rewrites history — coordinate with your team.

```powershell
# Example: migrate the file into LFS on the current branch
git lfs migrate import --include="enhanced_diet_predictor.pkl" --include-ref=refs/heads/dev

# After migration, force-push the rewritten branch (careful: this rewrites history)
git push --force origin dev
```

## Platform notes for Hugging Face Spaces

- Spaces backed by a Git repo will accept LFS-tracked files if LFS is configured on the repository provider (e.g., GitHub supports Git LFS). Ensure your remote supports LFS and your account has storage/bandwidth available.

- Alternatively, host the model externally (S3, GCS, HF Hub release, or a direct download URL) and download at startup — this avoids LFS quotas for very large models.

If you'd like, I can:

- Remove the `*.pkl` entry from `.gitignore` for you (if it exists) and commit that change.
- Run the exact `git lfs track` and `git add` commands for the repo here (I can provide the terminal commands for your PowerShell), but I can't run them unless you ask me to run commands in your terminal environment.
