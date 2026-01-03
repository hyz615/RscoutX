// Configuration
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api' 
    : `${window.location.origin}/api`;

// Global state
let currentTeam = null;
let currentEvent = null;

// Utility: Fetch wrapper
async function apiFetch(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Request failed');
    }
    
    return response.json();
}

// Utility: Show message
function showMessage(message, type = 'info') {
    const container = document.getElementById('messageContainer');
    if (!container) return;
    
    const div = document.createElement('div');
    div.className = `message message-${type}`;
    div.textContent = message;
    container.appendChild(div);
    
    setTimeout(() => div.remove(), 5000);
}

// Navigation
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const pages = document.querySelectorAll('.page');
    
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const target = item.dataset.page;
            
            // Update nav
            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
            
            // Update pages
            pages.forEach(p => p.classList.remove('active'));
            document.getElementById(`${target}Page`).classList.add('active');
            
            // Load page data
            loadPageData(target);
        });
    });
}

// Load page data
async function loadPageData(page) {
    switch(page) {
        case 'dashboard':
            await loadDashboard();
            break;
        case 'map':
            await loadMapPage();
            break;
        case 'admin':
            await loadAdminPage();
            break;
        case 'report':
            await loadReportPage();
            break;
    }
}

// Dashboard
async function loadDashboard() {
    // This would load team overview, stats, etc.
    console.log('Loading dashboard...');
}

async function syncMatches() {
    const team = document.getElementById('dashTeamNumber').value;
    const event = document.getElementById('dashEventId').value;
    
    if (!team || !event) {
        showMessage('Please enter team number and event ID', 'error');
        return;
    }
    
    try {
        showMessage('Syncing matches...', 'info');
        const result = await apiFetch(`/matches/sync?team=${team}&event=${event}`);
        showMessage(`Synced ${result.total_matches} matches (${result.new_matches} new, ${result.updated_matches} updated)`, 'success');
        
        currentTeam = team;
        currentEvent = event;
        
        await loadTeamStats();
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

async function loadTeamStats() {
    if (!currentTeam) return;
    
    try {
        // Get team by number
        const teams = await apiFetch('/teams/');
        const team = teams.find(t => t.team_number === currentTeam);
        
        if (!team) {
            showMessage('Team not found', 'error');
            return;
        }
        
        // Get stats
        const stats = await apiFetch(`/matches/stats/${team.id}?event_id=${currentEvent || ''}`);
        
        // Display stats
        const statsHtml = `
            <div class="stat-card">
                <div class="stat-value">${stats.total_matches}</div>
                <div class="stat-label">Total Matches</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${(stats.win_rate * 100).toFixed(1)}%</div>
                <div class="stat-label">Win Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.avg_score.toFixed(1)}</div>
                <div class="stat-label">Avg Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.highest_score}</div>
                <div class="stat-label">Highest Score</div>
            </div>
        `;
        
        document.getElementById('statsContainer').innerHTML = statsHtml;
    } catch (error) {
        showMessage(`Error loading stats: ${error.message}`, 'error');
    }
}

// Map Page
let pathPoints = [];
let mapCanvas, mapCtx;
let baseMapImage = null;
let currentInputMode = 'click';

async function loadMapPage() {
    console.log('Loading map page...');
    
    // Initialize canvas
    mapCanvas = document.getElementById('mapCanvas');
    mapCtx = mapCanvas.getContext('2d');
    
    // Load base map image
    await loadBaseMap();
    
    // Add click listener
    mapCanvas.addEventListener('click', handleMapClick);
    
    // Initialize input mode
    toggleInputMode();
}

async function loadBaseMap() {
    try {
        // Try to load the pushback map
        const img = new Image();
        img.crossOrigin = 'anonymous';
        
        img.onload = function() {
            // Set canvas size to match image
            mapCanvas.width = img.width;
            mapCanvas.height = img.height;
            baseMapImage = img;
            
            // Draw initial map
            redrawMap();
            
            showMessage('Map loaded! Click to add path points.', 'success');
        };
        
        img.onerror = function() {
            // Create a blank map if image not found
            mapCanvas.width = 600;
            mapCanvas.height = 600;
            
            mapCtx.fillStyle = '#1a1a1a';
            mapCtx.fillRect(0, 0, mapCanvas.width, mapCanvas.height);
            
            // Draw grid
            mapCtx.strokeStyle = '#333';
            mapCtx.lineWidth = 1;
            for (let i = 0; i <= 600; i += 50) {
                mapCtx.beginPath();
                mapCtx.moveTo(i, 0);
                mapCtx.lineTo(i, 600);
                mapCtx.stroke();
                
                mapCtx.beginPath();
                mapCtx.moveTo(0, i);
                mapCtx.lineTo(600, i);
                mapCtx.stroke();
            }
            
            mapCtx.fillStyle = '#fff';
            mapCtx.font = '20px Arial';
            mapCtx.textAlign = 'center';
            mapCtx.fillText('VEX Pushback Field Map', 300, 300);
            mapCtx.font = '14px Arial';
            mapCtx.fillText('Click to add path points', 300, 330);
            
            showMessage('Using blank map. Click to add points.', 'info');
        };
        
        // Try multiple possible paths for the map image
        const possiblePaths = [
            '/pushback_map.png',            // Root of server (backend serves this)
            './pushback_map.png',           // Same directory as HTML
            '../pushback_map.png',          // Parent directory
            'pushback_map.png'              // Current directory
        ];
        
        let loaded = false;
        for (const path of possiblePaths) {
            img.onerror = null; // Reset error handler
            img.onload = null;  // Reset load handler
            
            img.onload = function() {
                console.log(`✓ Map loaded from: ${path}`);
                loaded = true;
            };
            
            img.onerror = function() {
                console.log(`✗ Failed to load from: ${path}`);
            };
            
            img.src = path;
            
            // Wait a bit to see if it loads
            await new Promise(resolve => setTimeout(resolve, 100));
            if (loaded) break;
        }
        
        if (!loaded) {
            console.warn('Could not load pushback_map.png from any path');
        }
        
    } catch (error) {
        console.error('Error loading map:', error);
        showMessage('Error loading map', 'error');
    }
}

function toggleInputMode() {
    const mode = document.querySelector('input[name="inputMode"]:checked').value;
    currentInputMode = mode;
    
    const manualInputs = document.getElementById('manualInputs');
    const pathX = document.getElementById('pathX');
    const pathY = document.getElementById('pathY');
    
    if (mode === 'manual') {
        manualInputs.style.display = 'block';
        pathX.parentElement.style.display = 'block';
        pathY.parentElement.style.display = 'block';
        mapCanvas.style.cursor = 'default';
        showMessage('Manual input mode: Enter coordinates and click Add Point', 'info');
    } else {
        manualInputs.style.display = 'none';
        pathX.parentElement.style.display = 'none';
        pathY.parentElement.style.display = 'none';
        mapCanvas.style.cursor = 'crosshair';
        showMessage('Click mode: Click on the map to add points', 'info');
    }
}

function handleMapClick(event) {
    if (currentInputMode !== 'click') return;
    
    const rect = mapCanvas.getBoundingClientRect();
    const scaleX = mapCanvas.width / rect.width;
    const scaleY = mapCanvas.height / rect.height;
    
    const x = Math.round((event.clientX - rect.left) * scaleX);
    const y = Math.round((event.clientY - rect.top) * scaleY);
    
    const robotState = document.getElementById('robotState').value;
    
    const point = { x, y };
    if (robotState) {
        point.robot_state = { state: robotState };
    }
    
    pathPoints.push(point);
    updatePathPointsList();
    redrawMap();
    
    showMessage(`Point ${pathPoints.length} added at (${x}, ${y})`, 'success');
}

function redrawMap() {
    if (!mapCanvas) return;
    
    // Clear canvas
    mapCtx.clearRect(0, 0, mapCanvas.width, mapCanvas.height);
    
    // Draw base map
    if (baseMapImage) {
        mapCtx.drawImage(baseMapImage, 0, 0);
    } else {
        mapCtx.fillStyle = '#1a1a1a';
        mapCtx.fillRect(0, 0, mapCanvas.width, mapCanvas.height);
    }
    
    // Draw path points and connections
    if (pathPoints.length > 0) {
        // Draw connections
        if (pathPoints.length > 1) {
            mapCtx.strokeStyle = '#FF0000';
            mapCtx.lineWidth = 2;
            mapCtx.setLineDash([5, 5]);
            mapCtx.beginPath();
            mapCtx.moveTo(pathPoints[0].x, pathPoints[0].y);
            for (let i = 1; i < pathPoints.length; i++) {
                mapCtx.lineTo(pathPoints[i].x, pathPoints[i].y);
            }
            mapCtx.stroke();
            mapCtx.setLineDash([]);
        }
        
        // Draw points
        const stateColors = {
            'idle': '#808080',
            'moving': '#1E90FF',
            'intaking': '#00FF00',
            'wingpushing': '#FF4500',
            'releasing': '#FFD700'
        };
        
        pathPoints.forEach((point, index) => {
            const color = point.robot_state ? 
                (stateColors[point.robot_state.state] || '#FFFFFF') : 
                '#FFFFFF';
            
            // Draw point circle
            mapCtx.fillStyle = color;
            mapCtx.strokeStyle = '#FFFFFF';
            mapCtx.lineWidth = 2;
            mapCtx.beginPath();
            mapCtx.arc(point.x, point.y, 8, 0, Math.PI * 2);
            mapCtx.fill();
            mapCtx.stroke();
            
            // Draw point number
            mapCtx.fillStyle = '#FFFFFF';
            mapCtx.font = 'bold 12px Arial';
            mapCtx.textAlign = 'center';
            mapCtx.textBaseline = 'middle';
            mapCtx.fillText(index + 1, point.x, point.y);
            
            // Draw state label
            if (point.robot_state) {
                mapCtx.fillStyle = '#000000';
                mapCtx.fillRect(point.x - 30, point.y - 25, 60, 15);
                mapCtx.fillStyle = color;
                mapCtx.font = '10px Arial';
                mapCtx.fillText(point.robot_state.state, point.x, point.y - 18);
            }
        });
    }
}

function addPathPoint() {
    const x = parseFloat(document.getElementById('pathX').value);
    const y = parseFloat(document.getElementById('pathY').value);
    const robotState = document.getElementById('robotState').value;
    
    if (isNaN(x) || isNaN(y)) {
        showMessage('Please enter valid coordinates', 'error');
        return;
    }
    
    const point = { x, y };
    
    // Add robot state if selected
    if (robotState) {
        point.robot_state = { state: robotState };
    }
    
    pathPoints.push(point);
    updatePathPointsList();
    redrawMap();  // Redraw to show new point
    
    // Clear inputs
    document.getElementById('pathX').value = '';
    document.getElementById('pathY').value = '';
    document.getElementById('robotState').value = '';
}

function updatePathPointsList() {
    const stateEmojis = {
        'idle': '⭕',
        'moving': '🔵',
        'intaking': '🟢',
        'wingpushing': '🟠',
        'releasing': '🟡'
    };
    
    const list = document.getElementById('pathPointsList');
    list.innerHTML = pathPoints.map((p, i) => {
        const stateText = p.robot_state ? 
            ` ${stateEmojis[p.robot_state.state] || '●'} ${p.robot_state.state}` : 
            '';
        return `<div style="margin: 5px 0; padding: 5px; background: rgba(255,255,255,0.1); border-radius: 4px;">
            Point ${i + 1}: (${p.x}, ${p.y})${stateText} 
            <button class="btn btn-danger" onclick="removePathPoint(${i})" style="float: right; padding: 2px 8px;">×</button>
        </div>`;
    }).join('');
}

function removePathPoint(index) {
    pathPoints.splice(index, 1);
    updatePathPointsList();
    redrawMap();  // Redraw to update visualization
}

function clearPathPoints() {
    pathPoints = [];
    updatePathPointsList();
    redrawMap();  // Clear the map visualization
}

async function renderPath() {
    if (pathPoints.length < 2) {
        showMessage('Please add at least 2 points', 'error');
        return;
    }
    
    const method = document.getElementById('renderMethod').value;
    const coordSystem = document.getElementById('coordSystem').value;
    const showStateLabels = document.getElementById('showStateLabels').checked;
    const showArrows = document.getElementById('showArrows').checked;
    
    try {
        showMessage('Rendering final path with robot states...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/path/render/image`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                method,
                points: pathPoints,
                coordinate_system: coordSystem,
                style: {
                    color: '#FF0000',
                    width: 3,
                    opacity: 0.8,
                    arrow: showArrows,
                    show_state_labels: showStateLabels,
                    state_icon_size: 20
                },
                return_image: true
            })
        });
        
        if (!response.ok) throw new Error('Render failed');
        
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        
        // Show rendered image in a popup or replace canvas
        const container = document.getElementById('mapPreview');
        container.innerHTML = `
            <div style="text-align: center;">
                <img src="${imageUrl}" style="max-width: 100%; border: 2px solid #4CAF50; border-radius: 8px;" alt="Rendered path">
                <div style="margin-top: 10px;">
                    <button class="btn btn-primary" onclick="loadMapPage()">Edit Path</button>
                    <a href="${imageUrl}" download="robot_path.png" class="btn btn-success">Download</a>
                </div>
            </div>
        `;
        
        showMessage('Path rendered successfully! Click "Edit Path" to continue editing.', 'success');
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

// Admin Page
async function loadAdminPage() {
    await loadRobotsList();
    await loadDriversList();
}

async function loadRobotsList() {
    try {
        const robots = await apiFetch('/robots/');
        const tbody = document.getElementById('robotsTableBody');
        
        tbody.innerHTML = robots.map(r => `
            <tr>
                <td>${r.id}</td>
                <td>${r.team_id}</td>
                <td>${r.robot_base}</td>
                <td>${r.foldable ? 'Yes' : 'No'}</td>
                <td>${r.drivetrain}</td>
                <td>${r.tire_count}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteRobot(${r.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        showMessage(`Error loading robots: ${error.message}`, 'error');
    }
}

async function createRobot() {
    const data = {
        team_id: parseInt(document.getElementById('robotTeamId').value),
        robot_base: document.getElementById('robotBase').value,
        foldable: document.getElementById('robotFoldable').checked,
        drivetrain: document.getElementById('robotDrivetrain').value,
        tire_count: parseInt(document.getElementById('robotTireCount').value),
        notes: document.getElementById('robotNotes').value
    };
    
    try {
        await apiFetch('/robots/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        showMessage('Robot created successfully', 'success');
        await loadRobotsList();
        
        // Reset form
        document.getElementById('robotForm').reset();
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

async function deleteRobot(id) {
    if (!confirm('Are you sure?')) return;
    
    try {
        await apiFetch(`/robots/${id}`, { method: 'DELETE' });
        showMessage('Robot deleted', 'success');
        await loadRobotsList();
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

async function loadDriversList() {
    try {
        const drivers = await apiFetch('/drivers/');
        const tbody = document.getElementById('driversTableBody');
        
        tbody.innerHTML = drivers.map(d => `
            <tr>
                <td>${d.id}</td>
                <td>${d.team_id}</td>
                <td>${d.driver_name}</td>
                <td>${d.playstyle}</td>
                <td>${d.control_agility}/10</td>
                <td>${d.speed_preference}</td>
                <td>
                    <button class="btn btn-danger" onclick="deleteDriver(${d.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        showMessage(`Error loading drivers: ${error.message}`, 'error');
    }
}

async function createDriver() {
    const data = {
        team_id: parseInt(document.getElementById('driverTeamId').value),
        driver_name: document.getElementById('driverName').value,
        playstyle: document.getElementById('driverPlaystyle').value,
        likes_claw: document.getElementById('driverLikesClaw').checked,
        control_agility: parseInt(document.getElementById('driverAgility').value),
        speed_preference: document.getElementById('driverSpeed').value,
        tire_count: parseInt(document.getElementById('driverTireCount').value) || null,
        notes: document.getElementById('driverNotes').value
    };
    
    try {
        await apiFetch('/drivers/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        showMessage('Driver created successfully', 'success');
        await loadDriversList();
        
        // Reset form
        document.getElementById('driverForm').reset();
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

async function deleteDriver(id) {
    if (!confirm('Are you sure?')) return;
    
    try {
        await apiFetch(`/drivers/${id}`, { method: 'DELETE' });
        showMessage('Driver deleted', 'success');
        await loadDriversList();
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

// Report Page
async function loadReportPage() {
    console.log('Loading report page...');
}

async function generateReport() {
    const teamId = parseInt(document.getElementById('reportTeamId').value);
    const eventId = document.getElementById('reportEventId').value || null;
    const language = document.getElementById('reportLanguage').value;
    
    if (!teamId) {
        showMessage('Please enter team ID', 'error');
        return;
    }
    
    try {
        showMessage('Generating report... This may take a moment.', 'info');
        
        const result = await apiFetch('/report/generate', {
            method: 'POST',
            body: JSON.stringify({
                team_id: teamId,
                event_id: eventId,
                include_map: true,
                include_driver: true,
                include_robot: true,
                language
            })
        });
        
        if (result.success) {
            document.getElementById('reportMarkdown').textContent = result.report_markdown;
            document.getElementById('reportJson').textContent = JSON.stringify(result.report_json, null, 2);
            showMessage('Report generated successfully', 'success');
        } else {
            showMessage(`Error: ${result.message}`, 'error');
        }
    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    }
}

function copyMarkdown() {
    const text = document.getElementById('reportMarkdown').textContent;
    navigator.clipboard.writeText(text);
    showMessage('Markdown copied to clipboard', 'success');
}

function copyJson() {
    const text = document.getElementById('reportJson').textContent;
    navigator.clipboard.writeText(text);
    showMessage('JSON copied to clipboard', 'success');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    loadDashboard();
});
