# Automatic Image Cleanup Setup

This GitHub Actions workflow automatically deletes old Docker images from your GCP Artifact Registry, keeping only the 2 most recent versions.

## Setup Instructions

### 1. Create a GCP Service Account

Run these commands in your terminal:

```bash
# Create a service account
gcloud iam service-accounts create github-actions-cleanup \
  --display-name="GitHub Actions Image Cleanup"

# Grant necessary permissions
gcloud projects add-iam-policy-binding gymbite \
  --member="serviceAccount:github-actions-cleanup@gymbite.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.admin"

# Create and download the key
gcloud iam service-accounts keys create gcp-key.json \
  --iam-account=github-actions-cleanup@gymbite.iam.gserviceaccount.com
```

### 2. Add Secret to GitHub

1. Go to your GitHub repository: https://github.com/Nouman13388/gymbite_model
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GCP_SA_KEY`
5. Value: Copy the entire content of `gcp-key.json` file
6. Click **Add secret**

### 3. Push the Workflow

```bash
git add .github/workflows/cleanup-images.yml
git commit -m "Add automatic image cleanup workflow"
git push origin dev
```

### 4. Test the Workflow (Optional)

1. Go to **Actions** tab in GitHub
2. Select "Cleanup Old Docker Images"
3. Click **Run workflow**
4. Choose branch `dev`
5. Click **Run workflow**

## How It Works

- **Automatic**: Runs every Sunday at 2 AM UTC
- **Manual**: Can be triggered anytime from GitHub Actions tab
- **Policy**: Keeps 2 most recent images, deletes everything older
- **Safety**: Will never delete if you have 2 or fewer images

## Cost Impact

- **Current**: 0 images = $0/month
- **With workflow**: 1-2 images = ~$0.01-0.02/month
- **Without cleanup**: Could grow to $0.10-0.20/month over time

## Security Note

After creating `gcp-key.json`, **delete it immediately** after uploading to GitHub:

```bash
rm gcp-key.json
```

Never commit this file to git!
