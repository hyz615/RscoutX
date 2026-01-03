# 清理临时文档文件脚本
# 保留 README.md 和 UBUNTU_DEPLOY.md

Write-Host "🧹 清理临时文档文件..." -ForegroundColor Cyan

# 定义要删除的文件模式
$patterns = @(
    "*_FIX*.md",
    "*_GUIDE.md",
    "*_SUMMARY.md",
    "*_UPDATE.md",
    "*_DEBUG.md",
    "*_SOLUTION.md",
    "*_FEATURE.md",
    "*_SETUP.md",
    "*_EXAMPLES.md",
    "BUGFIX*.md",
    "CHANGELOG.md",
    "CHECKLIST.md",
    "CURRENT_STATUS.md",
    "PROJECT_SUMMARY.md",
    "QUICKSTART*.md",
    "QUICK_STATUS.txt"
)

# 计数器
$count = 0

# 遍历每个模式
foreach ($pattern in $patterns) {
    $files = Get-ChildItem -Path . -Filter $pattern -File -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        # 排除 README.md 和 UBUNTU_DEPLOY.md
        if ($file.Name -ne "README.md" -and $file.Name -ne "UBUNTU_DEPLOY.md") {
            Write-Host "删除: $($file.Name)" -ForegroundColor Yellow
            Remove-Item $file.FullName -Force
            $count++
        }
    }
}

Write-Host ""
Write-Host "✅ 完成! 共删除 $count 个临时文档文件" -ForegroundColor Green
Write-Host ""
Write-Host "保留的文档:" -ForegroundColor Cyan
Get-ChildItem -Path . -Filter *.md -File | Select-Object Name | Format-Table -AutoSize
