document.addEventListener('DOMContentLoaded', () => {
    const minutesDisplay = document.getElementById('minutes');
    const secondsDisplay = document.getElementById('seconds');
    const startButton = document.getElementById('start');
    const resetButton = document.getElementById('reset');
    const taskForm = document.getElementById('task-form');
    const taskInput = document.getElementById('task-input');
    const taskList = document.getElementById('task-list');
    const hand = document.querySelector('.hand');
    
    let interval;
    let totalTime = 25 * 60;
    let timeLeft = totalTime;

    function updateClock() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        minutesDisplay.textContent = String(minutes).padStart(2, '0');
        secondsDisplay.textContent = String(seconds).padStart(2, '0');

        const angle = (360 * timeLeft) / totalTime;
        hand.style.transform = `rotate(${angle}deg)`;
    }

    function startTimer() {
        if (interval) return;
        interval = setInterval(() => {
            timeLeft--;
            updateClock();
            if (timeLeft <= 0) {
                clearInterval(interval);
                interval = null;
            }
        }, 1000);
    }

    function resetTimer() {
        clearInterval(interval);
        interval = null;
        timeLeft = totalTime;
        updateClock();
    }

    startButton.addEventListener('click', startTimer);
    resetButton.addEventListener('click', resetTimer);

    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const taskText = taskInput.value.trim();
        if (taskText === '') return;
        const li = document.createElement('li');
        li.textContent = taskText;
        taskList.appendChild(li);
        taskInput.value = '';
    });

    updateClock();
});