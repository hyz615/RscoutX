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
async function loadMapPage() {
    console.log('Loading map page...');
}

let pathPoints = [];

function addPathPoint() {
    const x = parseFloat(document.getElementById('pathX').value);
    const y = parseFloat(document.getElementById('pathY').value);
    
    if (isNaN(x) || isNaN(y)) {
        showMessage('Please enter valid coordinates', 'error');
        return;
    }
    
    pathPoints.push({ x, y });
    updatePathPointsList();
    
    // Clear inputs
    document.getElementById('pathX').value = '';
    document.getElementById('pathY').value = '';
}

function updatePathPointsList() {
    const list = document.getElementById('pathPointsList');
    list.innerHTML = pathPoints.map((p, i) => 
        `<div>Point ${i + 1}: (${p.x}, ${p.y}) <button class="btn btn-danger" onclick="removePathPoint(${i})">Remove</button></div>`
    ).join('');
}

function removePathPoint(index) {
    pathPoints.splice(index, 1);
    updatePathPointsList();
}

function clearPathPoints() {
    pathPoints = [];
    updatePathPointsList();
}

async function renderPath() {
    if (pathPoints.length < 2) {
        showMessage('Please add at least 2 points', 'error');
        return;
    }
    
    const method = document.getElementById('renderMethod').value;
    const coordSystem = document.getElementById('coordSystem').value;
    
    try {
        showMessage('Rendering path...', 'info');
        
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
                    arrow: true
                },
                return_image: true
            })
        });
        
        if (!response.ok) throw new Error('Render failed');
        
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        
        const container = document.getElementById('mapPreview');
        container.innerHTML = `<img src="${imageUrl}" class="map-image" alt="Rendered path">`;
        
        showMessage('Path rendered successfully', 'success');
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
