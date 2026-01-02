# Delete all .md files except README.md

$mdFiles = Get-ChildItem -Path "." -Filter "*.md" -File | Where-Object { $_.Name -ne "README.md" }

Write-Host "Found $($mdFiles.Count) files to delete:"
Write-Host ""

foreach ($file in $mdFiles) {
    Write-Host "Deleting: $($file.Name)"
    Remove-Item $file.FullName -Force
}

Write-Host ""
Write-Host "Done! Deleted $($mdFiles.Count) files"
Write-Host "Kept: README.md"
