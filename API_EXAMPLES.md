# API Usage Examples - RscoutX

This document provides comprehensive API usage examples using curl and PowerShell.

## Base URL
```
http://localhost:8000/api
```

---

## 🏆 Teams API

### Create Team
```bash
# curl (bash/Linux/Mac)
curl -X POST "http://localhost:8000/api/teams/" \
  -H "Content-Type: application/json" \
  -d '{
    "team_number": "1234A",
    "team_name": "Dragon Robotics",
    "organization": "Dragon High School",
    "region": "China - Guangdong"
  }'

# PowerShell (Windows)
$headers = @{"Content-Type"="application/json"}
$body = @{
    team_number = "1234A"
    team_name = "Dragon Robotics"
    organization = "Dragon High School"
    region = "China - Guangdong"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/teams/" `
  -Method Post -Headers $headers -Body $body
```

### Get All Teams
```bash
# curl
curl "http://localhost:8000/api/teams/"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/teams/"
```

### Get Team by ID
```bash
# curl
curl "http://localhost:8000/api/teams/1"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/teams/1"
```

### Update Team
```bash
# curl
curl -X PUT "http://localhost:8000/api/teams/1" \
  -H "Content-Type: application/json" \
  -d '{"team_name": "Updated Team Name"}'

# PowerShell
$body = @{team_name = "Updated Team Name"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/teams/1" `
  -Method Put -Headers $headers -Body $body
```

### Delete Team
```bash
# curl
curl -X DELETE "http://localhost:8000/api/teams/1"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/teams/1" -Method Delete
```

---

## 🤖 Robots API

### Create Robot
```bash
# curl
curl -X POST "http://localhost:8000/api/robots/" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 1,
    "robot_base": "sbot",
    "foldable": true,
    "drivetrain": "4-motor X-drive",
    "tire_count": 4,
    "notes": "High-speed design with omni wheels"
  }'

# PowerShell
$body = @{
    team_id = 1
    robot_base = "sbot"
    foldable = $true
    drivetrain = "4-motor X-drive"
    tire_count = 4
    notes = "High-speed design with omni wheels"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/robots/" `
  -Method Post -Headers $headers -Body $body
```

### Get All Robots (filtered by team)
```bash
# curl
curl "http://localhost:8000/api/robots/?team_id=1"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/robots/?team_id=1"
```

### Update Robot
```bash
# curl
curl -X PUT "http://localhost:8000/api/robots/1" \
  -H "Content-Type: application/json" \
  -d '{"tire_count": 6, "notes": "Updated to 6 wheels"}'

# PowerShell
$body = @{tire_count = 6; notes = "Updated to 6 wheels"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/robots/1" `
  -Method Put -Headers $headers -Body $body
```

---

## 👤 Drivers API

### Create Driver
```bash
# curl
curl -X POST "http://localhost:8000/api/drivers/" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 1,
    "driver_name": "Alex Chen",
    "playstyle": "aggressive",
    "likes_claw": true,
    "control_agility": 9,
    "speed_preference": "fast",
    "tire_count": 4,
    "notes": "Experienced driver with 2 years history"
  }'

# PowerShell
$body = @{
    team_id = 1
    driver_name = "Alex Chen"
    playstyle = "aggressive"
    likes_claw = $true
    control_agility = 9
    speed_preference = "fast"
    tire_count = 4
    notes = "Experienced driver"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/drivers/" `
  -Method Post -Headers $headers -Body $body
```

### Get All Drivers
```bash
# curl
curl "http://localhost:8000/api/drivers/?team_id=1"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/drivers/?team_id=1"
```

---

## 🏁 Matches API

### Sync Team Matches
```bash
# curl
curl "http://localhost:8000/api/matches/sync?team=1234A&event=RE-VRC-24-1234"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/matches/sync?team=1234A&event=RE-VRC-24-1234"
```

### Get Team Statistics
```bash
# curl
curl "http://localhost:8000/api/matches/stats/1?event_id=RE-VRC-24-1234"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/matches/stats/1?event_id=RE-VRC-24-1234"
```

### Get All Matches
```bash
# curl - All matches for a team
curl "http://localhost:8000/api/matches/?team_id=1"

# curl - Matches for specific event
curl "http://localhost:8000/api/matches/?team_id=1&event_id=RE-VRC-24-1234"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/matches/?team_id=1&event_id=RE-VRC-24-1234"
```

---

## 🗺️ Path Rendering API

### Render Path (JSON Response)
```bash
# curl - Polyline
curl -X POST "http://localhost:8000/api/path/render" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "polyline",
    "points": [
      {"x": 100, "y": 100},
      {"x": 300, "y": 200},
      {"x": 500, "y": 100}
    ],
    "style": {
      "color": "#FF0000",
      "width": 3,
      "opacity": 0.8,
      "arrow": true
    },
    "coordinate_system": "pixel",
    "return_image": true,
    "return_overlay": false
  }'

# PowerShell
$body = @{
    method = "polyline"
    points = @(
        @{x=100; y=100},
        @{x=300; y=200},
        @{x=500; y=100}
    )
    style = @{
        color = "#FF0000"
        width = 3
        opacity = 0.8
        arrow = $true
    }
    coordinate_system = "pixel"
    return_image = $true
    return_overlay = $false
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/path/render" `
  -Method Post -Headers $headers -Body $body
```

### Render Path (Image Response)
```bash
# curl - Save as image
curl -X POST "http://localhost:8000/api/path/render/image" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "bezier",
    "points": [
      {"x": 100, "y": 100},
      {"x": 200, "y": 300},
      {"x": 300, "y": 100},
      {"x": 400, "y": 200}
    ],
    "style": {"color": "#0000FF", "width": 4},
    "coordinate_system": "pixel"
  }' \
  --output path_render.png

# PowerShell - Save as image
$body = @{
    method = "bezier"
    points = @(
        @{x=100; y=100},
        @{x=200; y=300},
        @{x=300; y=100},
        @{x=400; y=200}
    )
    style = @{color="#0000FF"; width=4}
    coordinate_system = "pixel"
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/api/path/render/image" `
  -Method Post -Headers $headers -Body $body -OutFile "path_render.png"
```

### A* Pathfinding with Obstacles
```bash
# curl
curl -X POST "http://localhost:8000/api/path/render/image" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "astar",
    "points": [
      {"x": 50, "y": 50},
      {"x": 550, "y": 550}
    ],
    "obstacles": [
      {"x": 200, "y": 200, "w": 100, "h": 100},
      {"x": 300, "y": 300, "w": 80, "h": 80}
    ],
    "style": {"color": "#00FF00", "width": 3},
    "coordinate_system": "pixel"
  }' \
  --output astar_path.png
```

### Heatline Rendering
```bash
# curl
curl -X POST "http://localhost:8000/api/path/render/image" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "heatline",
    "points": [
      {"x": 100, "y": 100, "speed": 1.0},
      {"x": 200, "y": 150, "speed": 5.0},
      {"x": 300, "y": 100, "speed": 10.0},
      {"x": 400, "y": 200, "speed": 3.0}
    ],
    "style": {"width": 5},
    "coordinate_system": "pixel"
  }' \
  --output heatline.png
```

---

## 📄 Report Generation API

### Generate Team Report (Chinese)
```bash
# curl
curl -X POST "http://localhost:8000/api/report/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 1,
    "event_id": "RE-VRC-24-1234",
    "include_map": true,
    "include_driver": true,
    "include_robot": true,
    "language": "zh"
  }'

# PowerShell
$body = @{
    team_id = 1
    event_id = "RE-VRC-24-1234"
    include_map = $true
    include_driver = $true
    include_robot = $true
    language = "zh"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:8000/api/report/generate" `
  -Method Post -Headers $headers -Body $body

# Display markdown report
$result.report_markdown

# Display JSON report
$result.report_json | ConvertTo-Json -Depth 5
```

### Generate Team Report (English)
```bash
# curl
curl -X POST "http://localhost:8000/api/report/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": 1,
    "language": "en"
  }'

# PowerShell
$body = @{team_id = 1; language = "en"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/report/generate" `
  -Method Post -Headers $headers -Body $body
```

---

## 🔍 Health Check

```bash
# curl
curl "http://localhost:8000/api/health"

# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/health"
```

---

## 📚 API Documentation

Interactive API documentation (Swagger UI):
```
http://localhost:8000/api/docs
```

Alternative documentation (ReDoc):
```
http://localhost:8000/api/redoc
```

---

## 💡 Tips

1. **Authentication**: Currently no authentication required. Add in production.

2. **Error Handling**: All endpoints return JSON with error details on failure.

3. **Rate Limiting**: No rate limiting currently. Implement in production.

4. **CORS**: Configured for localhost. Update for production domains.

5. **Database**: Using SQLite. Consider PostgreSQL for production.

6. **LLM Provider**: Configure OpenAI or Ollama in `.env` for report generation.

---

## 🔧 Complete Workflow Example

```bash
# 1. Create a team
TEAM_ID=$(curl -s -X POST "http://localhost:8000/api/teams/" \
  -H "Content-Type: application/json" \
  -d '{"team_number":"TEST1","team_name":"Test Team","organization":"Test","region":"Test"}' \
  | jq -r '.id')

echo "Created team with ID: $TEAM_ID"

# 2. Add robot
curl -X POST "http://localhost:8000/api/robots/" \
  -H "Content-Type: application/json" \
  -d "{\"team_id\":$TEAM_ID,\"robot_base\":\"sbot\",\"foldable\":true,\"drivetrain\":\"4-motor\",\"tire_count\":4}"

# 3. Add driver
curl -X POST "http://localhost:8000/api/drivers/" \
  -H "Content-Type: application/json" \
  -d "{\"team_id\":$TEAM_ID,\"driver_name\":\"Test Driver\",\"playstyle\":\"balanced\",\"control_agility\":7,\"speed_preference\":\"medium\",\"likes_claw\":false}"

# 4. Sync matches
curl "http://localhost:8000/api/matches/sync?team=TEST1&event=TEST-2024"

# 5. Generate report
curl -X POST "http://localhost:8000/api/report/generate" \
  -H "Content-Type: application/json" \
  -d "{\"team_id\":$TEAM_ID,\"language\":\"en\"}"
```

---

**Happy Scouting! 🚀**
