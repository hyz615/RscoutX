# Test Robot State Visualization
# 测试机器人状态可视化功能

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Testing Robot State Visualization" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend is running
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/health" -Method Get
    Write-Host "✓ Backend is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Backend is not running. Please start it first." -ForegroundColor Red
    Write-Host "  Run: .\debug_backend.bat" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Test 1: Simple path with states" -ForegroundColor Yellow
Write-Host "--------------------------------------"

$testPath1 = @{
    method = "polyline"
    coordinate_system = "pixel"
    points = @(
        @{
            x = 100
            y = 100
            robot_state = @{
                state = "idle"
            }
        },
        @{
            x = 200
            y = 150
            robot_state = @{
                state = "moving"
            }
        },
        @{
            x = 300
            y = 200
            robot_state = @{
                state = "intaking"
            }
        },
        @{
            x = 400
            y = 250
            robot_state = @{
                state = "wingpushing"
            }
        },
        @{
            x = 500
            y = 300
            robot_state = @{
                state = "releasing"
            }
        }
    )
    style = @{
        color = "#FF0000"
        width = 3
        show_state_labels = $true
        state_icon_size = 20
    }
} | ConvertTo-Json -Depth 5

try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/path/render/image" `
        -Method Post `
        -Headers @{"Content-Type"="application/json"} `
        -Body $testPath1 `
        -OutFile "test_path_polyline.png"
    
    Write-Host "✓ Test 1 passed: test_path_polyline.png" -ForegroundColor Green
} catch {
    Write-Host "✗ Test 1 failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Test 2: Bezier curve with states" -ForegroundColor Yellow
Write-Host "--------------------------------------"

$testPath2 = @{
    method = "bezier"
    coordinate_system = "pixel"
    points = @(
        @{
            x = 150
            y = 150
            robot_state = @{
                state = "idle"
            }
        },
        @{
            x = 250
            y = 250
            robot_state = @{
                state = "intaking"
                color = "#00FFFF"  # Custom cyan color
            }
        },
        @{
            x = 350
            y = 200
            robot_state = @{
                state = "wingpushing"
            }
        },
        @{
            x = 450
            y = 300
            robot_state = @{
                state = "releasing"
            }
        }
    )
    style = @{
        color = "#0000FF"
        width = 4
        arrow = $true
        show_state_labels = $true
        state_icon_size = 25
    }
} | ConvertTo-Json -Depth 5

try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/path/render/image" `
        -Method Post `
        -Headers @{"Content-Type"="application/json"} `
        -Body $testPath2 `
        -OutFile "test_path_bezier.png"
    
    Write-Host "✓ Test 2 passed: test_path_bezier.png" -ForegroundColor Green
} catch {
    Write-Host "✗ Test 2 failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Test 3: VEX match simulation path" -ForegroundColor Yellow
Write-Host "--------------------------------------"

$testPath3 = @{
    method = "spline"
    coordinate_system = "field"  # Using field coordinates (mm)
    points = @(
        @{
            x = 500
            y = 500
            robot_state = @{
                state = "idle"
            }
        },
        @{
            x = 1000
            y = 800
            robot_state = @{
                state = "moving"
            }
        },
        @{
            x = 1500
            y = 1000
            robot_state = @{
                state = "intaking"
            }
        },
        @{
            x = 2000
            y = 1500
            robot_state = @{
                state = "moving"
            }
        },
        @{
            x = 2500
            y = 2000
            robot_state = @{
                state = "wingpushing"
            }
        },
        @{
            x = 3000
            y = 2500
            robot_state = @{
                state = "moving"
            }
        },
        @{
            x = 3200
            y = 2800
            robot_state = @{
                state = "releasing"
            }
        },
        @{
            x = 3000
            y = 3000
            robot_state = @{
                state = "idle"
            }
        }
    )
    style = @{
        color = "#FF00FF"
        width = 5
        arrow = $true
        show_state_labels = $true
        state_icon_size = 30
    }
} | ConvertTo-Json -Depth 5

try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/path/render/image" `
        -Method Post `
        -Headers @{"Content-Type"="application/json"} `
        -Body $testPath3 `
        -OutFile "test_path_vex_match.png"
    
    Write-Host "✓ Test 3 passed: test_path_vex_match.png" -ForegroundColor Green
} catch {
    Write-Host "✗ Test 3 failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Test 4: Mixed states (some points without states)" -ForegroundColor Yellow
Write-Host "--------------------------------------"

$testPath4 = @{
    method = "spline"
    coordinate_system = "pixel"
    points = @(
        @{ x = 100; y = 100 },  # No state
        @{
            x = 200
            y = 200
            robot_state = @{ state = "intaking" }
        },
        @{ x = 300; y = 250 },  # No state
        @{
            x = 400
            y = 300
            robot_state = @{ state = "wingpushing" }
        },
        @{ x = 500; y = 350 },  # No state
        @{
            x = 600
            y = 400
            robot_state = @{ state = "releasing" }
        }
    )
    style = @{
        color = "#00FF00"
        width = 3
        show_state_labels = $true
        state_icon_size = 20
    }
} | ConvertTo-Json -Depth 5

try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/path/render/image" `
        -Method Post `
        -Headers @{"Content-Type"="application/json"} `
        -Body $testPath4 `
        -OutFile "test_path_mixed.png"
    
    Write-Host "✓ Test 4 passed: test_path_mixed.png" -ForegroundColor Green
} catch {
    Write-Host "✗ Test 4 failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Test 5: States without labels" -ForegroundColor Yellow
Write-Host "--------------------------------------"

$testPath5 = @{
    method = "bezier"
    coordinate_system = "pixel"
    points = @(
        @{
            x = 100
            y = 300
            robot_state = @{ state = "idle" }
        },
        @{
            x = 200
            y = 350
            robot_state = @{ state = "intaking" }
        },
        @{
            x = 300
            y = 400
            robot_state = @{ state = "wingpushing" }
        },
        @{
            x = 400
            y = 450
            robot_state = @{ state = "releasing" }
        }
    )
    style = @{
        color = "#FFA500"
        width = 4
        show_state_labels = $false  # Only show icons, no text
        state_icon_size = 15
    }
} | ConvertTo-Json -Depth 5

try {
    Invoke-RestMethod -Uri "http://localhost:8000/api/path/render/image" `
        -Method Post `
        -Headers @{"Content-Type"="application/json"} `
        -Body $testPath5 `
        -OutFile "test_path_no_labels.png"
    
    Write-Host "✓ Test 5 passed: test_path_no_labels.png" -ForegroundColor Green
} catch {
    Write-Host "✗ Test 5 failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "All tests completed!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Generated files:" -ForegroundColor Green
Write-Host "  - test_path_polyline.png" -ForegroundColor White
Write-Host "  - test_path_bezier.png" -ForegroundColor White
Write-Host "  - test_path_vex_match.png" -ForegroundColor White
Write-Host "  - test_path_mixed.png" -ForegroundColor White
Write-Host "  - test_path_no_labels.png" -ForegroundColor White
Write-Host ""
Write-Host "Open these images to see the robot state visualizations!" -ForegroundColor Yellow
Write-Host ""
Write-Host "You can also test in the web UI:" -ForegroundColor Cyan
Write-Host "  http://localhost:3000" -ForegroundColor White
Write-Host ""
