from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.database import Base, engine
from app.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task Management API",
    description="API sederhana untuk demonstrasi testing & inspeksi CI/CD",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tasks.router)


@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    return """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Manager - CI/CD Demo</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-color: #0b0f17;
                --panel-bg: rgba(22, 27, 34, 0.65);
                --border-color: #30363d;
                --text-color: #c9d1d9;
                --text-muted: #8b949e;
                --primary: #58a6ff;
                --primary-hover: #1f6feb;
                --success: #2ea44f;
                --danger: #f85149;
                --radius: 16px;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }

            body {
                background-color: var(--bg-color);
                color: var(--text-color);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                background-image: radial-gradient(circle at top right, rgba(88, 166, 255, 0.08), transparent 350px),
                                  radial-gradient(circle at bottom left, rgba(188, 140, 255, 0.08), transparent 350px);
            }

            .container {
                width: 100%;
                max-width: 550px;
                background: var(--panel-bg);
                backdrop-filter: blur(16px);
                border: 1px solid var(--border-color);
                border-radius: var(--radius);
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            }

            h1 {
                font-size: 26px;
                font-weight: 700;
                margin-bottom: 6px;
                background: linear-gradient(45deg, #58a6ff, #bc8cff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .subtitle {
                font-size: 13px;
                color: var(--text-muted);
                margin-bottom: 25px;
                display: flex;
                justify-content: space-between;
            }

            .subtitle a {
                color: var(--primary);
                text-decoration: none;
            }

            .subtitle a:hover {
                text-decoration: underline;
            }

            .form-group {
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-bottom: 25px;
            }

            input, textarea {
                background-color: rgba(22, 27, 34, 0.85);
                border: 1px solid var(--border-color);
                border-radius: 10px;
                padding: 12px 16px;
                color: var(--text-color);
                font-size: 14px;
                transition: all 0.2s ease;
            }

            input:focus, textarea:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
            }

            button.btn-add {
                background: linear-gradient(135deg, var(--primary), #1f6feb);
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(31, 111, 235, 0.25);
                transition: all 0.2s ease;
            }

            button.btn-add:hover {
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(31, 111, 235, 0.35);
            }

            .divider {
                height: 1px;
                background-color: var(--border-color);
                margin-bottom: 20px;
            }

            .task-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
                max-height: 350px;
                overflow-y: auto;
                padding-right: 4px;
            }

            /* Custom Scrollbar */
            .task-list::-webkit-scrollbar {
                width: 6px;
            }
            .task-list::-webkit-scrollbar-track {
                background: transparent;
            }
            .task-list::-webkit-scrollbar-thumb {
                background: var(--border-color);
                border-radius: 3px;
            }

            .task-item {
                background: rgba(33, 38, 45, 0.4);
                border: 1px solid var(--border-color);
                border-radius: 10px;
                padding: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.2s ease;
            }

            .task-item:hover {
                background: rgba(33, 38, 45, 0.6);
                border-color: #444c56;
            }

            .task-item.completed {
                border-color: rgba(46, 164, 79, 0.3);
                background: rgba(46, 164, 79, 0.03);
            }

            .task-info {
                display: flex;
                flex-direction: column;
                gap: 4px;
                flex-grow: 1;
                margin-right: 15px;
            }

            .task-title {
                font-size: 15px;
                font-weight: 600;
                transition: color 0.2s;
            }

            .completed .task-title {
                text-decoration: line-through;
                color: var(--text-muted);
            }

            .task-desc {
                font-size: 13px;
                color: var(--text-muted);
            }

            .task-actions {
                display: flex;
                gap: 8px;
            }

            .btn-action {
                background: none;
                border: none;
                cursor: pointer;
                font-size: 16px;
                padding: 6px;
                border-radius: 6px;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .btn-check {
                color: var(--text-muted);
                border: 1px solid var(--border-color);
                width: 24px;
                height: 24px;
                border-radius: 50%;
                font-size: 11px;
            }

            .completed .btn-check {
                background-color: var(--success);
                border-color: var(--success);
                color: #ffffff;
            }

            .btn-delete {
                color: var(--text-muted);
            }

            .btn-delete:hover {
                color: var(--danger);
                background: rgba(248, 81, 73, 0.1);
            }

            .empty-state {
                text-align: center;
                color: var(--text-muted);
                font-size: 14px;
                padding: 30px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Task Manager</h1>
            <div class="subtitle">
                <span>CI/CD Demo Project</span>
                <a href="/docs" target="_blank">Swagger API Docs ↗</a>
            </div>

            <div class="form-group">
                <input type="text" id="taskTitle" placeholder="Judul tugas baru..." required>
                <textarea id="taskDesc" placeholder="Deskripsi tugas (opsional)..." rows="2"></textarea>
                <button class="btn-add" onclick="createTask()">Tambah Tugas</button>
            </div>

            <div class="divider"></div>

            <div class="task-list" id="taskList">
                <div class="empty-state">Memuat daftar tugas...</div>
            </div>
        </div>

        <script>
            const API_URL = '/tasks/';

            async function fetchTasks() {
                try {
                    const response = await fetch(API_URL);
                    const tasks = await response.json();
                    const taskList = document.getElementById('taskList');
                    taskList.innerHTML = '';

                    if (tasks.length === 0) {
                        taskList.innerHTML = '<div class="empty-state">Belum ada tugas. Silakan tambahkan tugas baru di atas!</div>';
                        return;
                    }

                    tasks.forEach(task => {
                        const taskItem = document.createElement('div');
                        taskItem.className = `task-item ${task.is_completed ? 'completed' : ''}`;
                        taskItem.innerHTML = `
                            <div class="task-info">
                                <span class="task-title">${escapeHTML(task.title)}</span>
                                ${task.description ? `<span class="task-desc">${escapeHTML(task.description)}</span>` : ''}
                            </div>
                            <div class="task-actions">
                                <button class="btn-action btn-check" onclick="toggleTask(${task.id}, ${task.is_completed})">
                                    ${task.is_completed ? '✓' : ''}
                                </button>
                                <button class="btn-action btn-delete" onclick="deleteTask(${task.id})">
                                    🗑️
                                </button>
                            </div>
                        `;
                        taskList.appendChild(taskItem);
                    });
                } catch (error) {
                    console.error('Error fetching tasks:', error);
                }
            }

            async function createTask() {
                const titleInput = document.getElementById('taskTitle');
                const descInput = document.getElementById('taskDesc');
                
                if (!titleInput.value.trim()) {
                    alert('Judul tugas tidak boleh kosong!');
                    return;
                }

                try {
                    const response = await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            title: titleInput.value.trim(),
                            description: descInput.value.trim() || null
                        })
                    });

                    if (response.ok) {
                        titleInput.value = '';
                        descInput.value = '';
                        fetchTasks();
                    }
                } catch (error) {
                    console.error('Error creating task:', error);
                }
            }

            async function toggleTask(id, currentStatus) {
                try {
                    const response = await fetch(`${API_URL}${id}`, {
                        method: 'PATCH',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            is_completed: !currentStatus
                        })
                    });

                    if (response.ok) {
                        fetchTasks();
                    }
                } catch (error) {
                    console.error('Error toggling task:', error);
                }
            }

            async function deleteTask(id) {
                if (!confirm('Apakah Anda yakin ingin menghapus tugas ini?')) return;
                
                try {
                    const response = await fetch(`${API_URL}${id}`, {
                        method: 'DELETE'
                    });

                    if (response.ok) {
                        fetchTasks();
                    }
                } catch (error) {
                    console.error('Error deleting task:', error);
                }
            }

            function escapeHTML(str) {
                return str.replace(/[&<>'"]/g, 
                    tag => ({
                        '&': '&amp;',
                        '<': '&lt;',
                        '>': '&gt;',
                        "'": '&#39;',
                        '"': '&quot;'
                    }[tag] || tag)
                );
            }

            // Load tasks on startup
            fetchTasks();
        </script>
    </body>
    </html>
    """
