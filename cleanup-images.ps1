# Manual Image Cleanup Script
# Run this anytime to clean up old Docker images from Artifact Registry

Write-Host "🧹 Starting GCP Artifact Registry Cleanup..." -ForegroundColor Cyan

# Configuration
$PROJECT_ID = "gymbite"
$LOCATION = "europe-west1"
$REPOSITORY = "cloud-run-source-deploy"
$KEEP_COUNT = 2

Write-Host "`n📊 Fetching current images..." -ForegroundColor Yellow

# Get all images sorted by creation time (newest first)
$images = gcloud artifacts docker images list `
    "europe-west1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY" `
    --include-tags `
    --format="value(DIGEST)" `
    --sort-by="~CREATE_TIME" | Out-String -Stream | Where-Object { $_ -ne "" }

$totalImages = ($images | Measure-Object).Count
Write-Host "Found $totalImages images" -ForegroundColor White

if ($totalImages -le $KEEP_COUNT) {
    Write-Host "✅ Only $totalImages images found. No cleanup needed (keeping minimum $KEEP_COUNT)." -ForegroundColor Green
    Write-Host "`n📦 Current images:" -ForegroundColor Cyan
    gcloud artifacts docker images list `
        "europe-west1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY" `
        --include-tags `
        --format="table(IMAGE,CREATE_TIME)" `
        --sort-by="~CREATE_TIME"
    exit 0
}

$toDelete = $totalImages - $KEEP_COUNT
Write-Host "🗑️  Will delete $toDelete old images (keeping $KEEP_COUNT most recent)" -ForegroundColor Yellow

# Confirm deletion
$confirm = Read-Host "`nProceed with deletion? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Cleanup cancelled." -ForegroundColor Red
    exit 0
}

Write-Host "`n🚀 Starting deletion..." -ForegroundColor Cyan

# Delete old images (skip the first KEEP_COUNT newest ones)
$images | Select-Object -Skip $KEEP_COUNT | ForEach-Object {
    $digest = $_
    Write-Host "  Deleting: $digest" -ForegroundColor Gray
    gcloud artifacts docker images delete `
        "europe-west1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/gymbite_model/gymbite-model@$digest" `
        --quiet --async 2>&1 | Out-Null
}

Write-Host "`n✅ Cleanup completed! Kept $KEEP_COUNT most recent images, deleted $toDelete old images." -ForegroundColor Green

# Show remaining images
Write-Host "`n📦 Remaining images:" -ForegroundColor Cyan
Start-Sleep -Seconds 2  # Brief pause to let async deletes register
gcloud artifacts docker images list `
    "europe-west1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY" `
    --include-tags `
    --format="table(IMAGE,CREATE_TIME)" `
    --sort-by="~CREATE_TIME"

Write-Host "`n💰 Expected monthly cost: ~`$0.01-0.02 (for $KEEP_COUNT images)" -ForegroundColor Green
