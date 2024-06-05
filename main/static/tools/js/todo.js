document.addEventListener('DOMContentLoaded', loadTasks);

document.getElementById('add-task-btn').addEventListener('click', addTask);
document.getElementById('new-task').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        addTask();
    }
});

function addTask() {
    const taskInput = document.getElementById('new-task');
    const taskText = taskInput.value.trim();

    if (taskText !== '') {
        const taskId = Date.now().toString();
        const task = { id: taskId, text: taskText, completed: false };
        saveTask(task);
        appendTaskToDOM(task);
        taskInput.value = '';
    }
}

function appendTaskToDOM(task) {
    const taskList = document.getElementById('task-list');
    const taskItem = document.createElement('li');
    taskItem.className = 'list-group-item';
    taskItem.dataset.id = task.id;
    taskItem.innerHTML = `
        <span class="${task.completed ? 'completed' : ''}">${task.text}</span>
        <div class="task-actions">
            <button class="btn btn-complete btn-sm">${task.completed ? 'Undo' : 'Complete'}</button>
            <button class="btn btn-delete btn-sm">Delete</button>
        </div>
    `;

    taskItem.querySelector('.btn-complete').addEventListener('click', toggleCompleteTask);
    taskItem.querySelector('.btn-delete').addEventListener('click', deleteTask);

    taskList.appendChild(taskItem);
}

function toggleCompleteTask(event) {
    const taskItem = event.target.closest('.list-group-item');
    const taskId = taskItem.dataset.id;
    const task = getTaskById(taskId);

    task.completed = !task.completed;
    saveTask(task);

    taskItem.querySelector('span').classList.toggle('completed', task.completed);
    event.target.textContent = task.completed ? 'Undo' : 'Complete';
}

function deleteTask(event) {
    const taskItem = event.target.closest('.list-group-item');
    const taskId = taskItem.dataset.id;

    removeTask(taskId);
    taskItem.remove();
}

function saveTask(task) {
    const tasks = getTasks();
    const existingTaskIndex = tasks.findIndex(t => t.id === task.id);

    if (existingTaskIndex >= 0) {
        tasks[existingTaskIndex] = task;
    } else {
        tasks.push(task);
    }

    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function getTasks() {
    return JSON.parse(localStorage.getItem('tasks')) || [];
}

function getTaskById(taskId) {
    return getTasks().find(task => task.id === taskId);
}

function removeTask(taskId) {
    let tasks = getTasks();
    tasks = tasks.filter(task => task.id !== taskId);
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function loadTasks() {
    const tasks = getTasks();
    tasks.forEach(task => appendTaskToDOM(task));
}