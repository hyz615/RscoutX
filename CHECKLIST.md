# 🚀 RscoutX - Startup Checklist

Use this checklist to verify your RscoutX installation.

---

## ✅ Pre-Installation Checklist

- [ ] Python 3.10 or higher installed
  ```powershell
  python --version
  ```
  Expected output: `Python 3.10.x` or higher

- [ ] Git installed (optional, for cloning)
  ```powershell
  git --version
  ```

- [ ] Windows PowerShell or Command Prompt available

---

## ✅ Installation Checklist

- [ ] Project files extracted/cloned
- [ ] Navigate to project directory
  ```powershell
  cd path\to\RscoutX
  ```

- [ ] Backend `.env` configured (optional for first run)
  ```powershell
  cd backend
  copy .env.example .env
  # Edit .env if needed
  ```

---

## ✅ First Startup Checklist

- [ ] Run startup script
  ```powershell
  start.bat
  ```

- [ ] Wait for virtual environment creation (first time only)
- [ ] Wait for dependency installation (may take 2-3 minutes)
- [ ] Two windows should open:
  - [ ] Backend terminal (FastAPI/Uvicorn)
  - [ ] Frontend terminal (Python HTTP server)

- [ ] Check for errors in both terminals
- [ ] Backend should show:
  ```
  INFO:     Uvicorn running on http://0.0.0.0:8000
  INFO:     Application startup complete.
  ```

- [ ] Frontend should show:
  ```
  Serving HTTP on :: port 3000 (http://[::]:3000/) ...
  ```

---

## ✅ Access Checklist

Open in browser:

- [ ] Frontend: http://localhost:3000
  - Should show RscoutX homepage with 4 tabs
  - Purple/blue gradient header
  - Navigation: Dashboard | Map | Admin | Report

- [ ] API Docs: http://localhost:8000/api/docs
  - Should show Swagger UI
  - List of all API endpoints
  - Try the health check endpoint

- [ ] API: http://localhost:8000/api/health
  - Should return: `{"status":"healthy"}`

---

## ✅ Seed Data Checklist

- [ ] Open new terminal in backend directory
  ```powershell
  cd backend
  venv\Scripts\activate
  python seed_data.py
  ```

- [ ] Should see output:
  ```
  ✓ Created teams: 1234A, 5678B
  ✓ Created robots for both teams
  ✓ Created drivers for both teams
  ✓ Created 5 matches for Team 1
  ✓ Created 3 matches for Team 2
  ```

- [ ] Verify data in frontend:
  - Go to Admin tab
  - Should see 2 robots in table
  - Should see 2 drivers in table

---

## ✅ Functionality Checklist

### Dashboard Tab
- [ ] Enter team number: `1234A`
- [ ] Enter event ID: `RE-VRC-24-1234`
- [ ] Click "Load Stats"
- [ ] Should see statistics cards populated
- [ ] Win rate, average score, etc. displayed

### Map Tab
- [ ] Select rendering method (try "Bezier")
- [ ] Add 3-4 path points
- [ ] Click "Render Path"
- [ ] Should see rendered path image

### Admin Tab
- [ ] Robots section shows existing robots
- [ ] Drivers section shows existing drivers
- [ ] Try creating a new robot:
  - Team ID: 1
  - Robot Base: sbot
  - Drivetrain: test
  - Tire Count: 4
  - Click "Create Robot"
  - [ ] Should appear in table below

### Report Tab
- [ ] Enter Team ID: 1
- [ ] Select language: Chinese or English
- [ ] Click "Generate Report"
- [ ] Wait 10-30 seconds (if LLM configured)
- [ ] Should see report in Markdown preview
- [ ] Click "Copy" to copy to clipboard

---

## ✅ API Testing Checklist

Test with curl or PowerShell:

- [ ] Get all teams
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8000/api/teams/"
  ```

- [ ] Get team statistics
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8000/api/matches/stats/1"
  ```

- [ ] Render simple path
  ```powershell
  $headers = @{"Content-Type"="application/json"}
  $body = @{
      method = "polyline"
      points = @(@{x=100;y=100}, @{x=200;y=200})
      style = @{color="#FF0000"; width=3}
      coordinate_system = "pixel"
      return_image = $true
  } | ConvertTo-Json -Depth 3
  
  Invoke-RestMethod -Uri "http://localhost:8000/api/path/render" `
    -Method Post -Headers $headers -Body $body
  ```

---

## ✅ LLM Configuration Checklist (Optional)

### For OpenAI:
- [ ] Get API key from https://platform.openai.com/
- [ ] Edit `backend/.env`:
  ```ini
  LLM_PROVIDER=openai
  OPENAI_API_KEY=sk-your-key-here
  OPENAI_MODEL=gpt-4
  ```
- [ ] Restart backend
- [ ] Try generating a report

### For Ollama (Local):
- [ ] Install Ollama from https://ollama.ai/
- [ ] Pull a model: `ollama pull llama2`
- [ ] Start Ollama service
- [ ] Edit `backend/.env`:
  ```ini
  LLM_PROVIDER=ollama
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_MODEL=llama2
  ```
- [ ] Restart backend
- [ ] Try generating a report

---

## ✅ Testing Checklist

- [ ] Navigate to backend directory
  ```powershell
  cd backend
  venv\Scripts\activate
  pip install pytest httpx
  ```

- [ ] Run tests
  ```powershell
  pytest tests/ -v
  ```

- [ ] All tests should pass:
  ```
  test_api.py::test_create_team PASSED
  test_api.py::test_get_teams PASSED
  test_api.py::test_path_render PASSED
  test_api.py::test_health_check PASSED
  test_path_renderer.py::test_path_renderer_polyline PASSED
  test_path_renderer.py::test_path_renderer_bezier PASSED
  test_path_renderer.py::test_coordinate_conversion PASSED
  ```

---

## ✅ Different Port Startup Checklist

### Port 80:
- [ ] Run: `start.bat 80`
- [ ] Access: http://localhost/api

### Port 443 (HTTPS):
- [ ] Set SSL certificates:
  ```powershell
  set SSL_CERTFILE=path\to\cert.pem
  set SSL_KEYFILE=path\to\key.pem
  ```
- [ ] Run: `start.bat 443`
- [ ] Access: https://localhost/api

### Custom Port:
- [ ] Run: `start.bat 8080`
- [ ] Access: http://localhost:8080/api

---

## ❌ Troubleshooting Checklist

### Python not found:
- [ ] Install Python 3.10+ from python.org
- [ ] Add to PATH during installation
- [ ] Restart terminal

### Port already in use:
- [ ] Check process: `netstat -ano | findstr :8000`
- [ ] Kill process: `taskkill /PID <pid> /F`
- [ ] Or use different port: `start.bat 8080`

### Dependencies failed to install:
- [ ] Update pip:
  ```powershell
  cd backend
  venv\Scripts\activate
  python -m pip install --upgrade pip
  ```
- [ ] Install dependencies manually:
  ```powershell
  pip install -r requirements.txt
  ```

### Frontend not loading:
- [ ] Check if frontend terminal is running
- [ ] Try accessing: http://127.0.0.1:3000
- [ ] Check firewall settings

### Database errors:
- [ ] Delete database file:
  ```powershell
  cd backend
  del rscoutx.db
  ```
- [ ] Re-run seed data:
  ```powershell
  python seed_data.py
  ```

### LLM report generation fails:
- [ ] Check `.env` configuration
- [ ] Verify API key (OpenAI)
- [ ] Verify Ollama is running (Ollama)
- [ ] Check terminal for error messages

---

## ✅ Final Verification

- [ ] All endpoints accessible
- [ ] Sample data loaded
- [ ] Frontend UI working
- [ ] Path rendering functional
- [ ] CRUD operations working
- [ ] No errors in terminal
- [ ] Tests passing (if run)

---

## 🎉 Success!

If all items are checked, your RscoutX installation is complete and working!

**Next steps:**
1. Explore the web interface
2. Add your own team data
3. Configure LLM for reports
4. Start scouting competitors!

---

## 📚 Additional Resources

- Full documentation: `README.md`
- API examples: `API_EXAMPLES.md`
- Quick start: `QUICKSTART.md`
- Project summary: `PROJECT_SUMMARY.md`

---

**Need help?** Check the troubleshooting section or refer to the documentation files.

**Happy Scouting! 🤖🏆**
