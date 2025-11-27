const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3001;

const DATA_FILE = path.join(__dirname, 'data', 'timers.json');

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Helper Functions
function readTimers() {
  try {
    const data = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

function writeTimers(timers) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(timers, null, 2));
}

// Format elapsed time in HH:MM:SS format
function formatElapsedTime(milliseconds) {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  
  return {
    formatted: `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`,
    totalSeconds: totalSeconds,
    hours: hours,
    minutes: minutes,
    seconds: seconds
  };
}

// POST /timers/start - Start a new timer
app.post('/timers/start', (req, res) => {
  const { label } = req.body;
  
  const timers = readTimers();
  const newTimer = {
    id: Date.now(),
    label: label || 'Unnamed Timer',
    startTime: Date.now(),
    endTime: null,
    elapsedTime: null,
    status: 'running',
    createdAt: new Date().toISOString()
  };

  timers.push(newTimer);
  writeTimers(timers);

  res.status(201).json({
    success: true,
    timer: {
      id: newTimer.id,
      label: newTimer.label,
      startTime: new Date(newTimer.startTime).toISOString(),
      status: newTimer.status
    },
    message: 'Timer started successfully.'
  });
});

// POST /timers/:id/stop - Stop a running timer
app.post('/timers/:id/stop', (req, res) => {
  const timerId = parseInt(req.params.id);
  const timers = readTimers();
  
  const timer = timers.find(t => t.id === timerId);
  
  if (!timer) {
    return res.status(404).json({
      success: false,
      error: 'Timer not found.',
      message: `No timer found with ID: ${timerId}`
    });
  }
  
  if (timer.status === 'stopped') {
    return res.status(400).json({
      success: false,
      error: 'Timer already stopped.',
      message: `Timer ${timerId} was already stopped.`,
      elapsedTime: timer.elapsedTime
    });
  }
  
  // Stop the timer
  timer.endTime = Date.now();
  timer.status = 'stopped';
  const elapsed = timer.endTime - timer.startTime;
  timer.elapsedTime = formatElapsedTime(elapsed);
  
  writeTimers(timers);
  
  res.json({
    success: true,
    timer: {
      id: timer.id,
      label: timer.label,
      startTime: new Date(timer.startTime).toISOString(),
      endTime: new Date(timer.endTime).toISOString(),
      elapsedTime: timer.elapsedTime,
      status: timer.status
    },
    message: 'Timer stopped successfully.'
  });
});

// GET /timers/:id - Get timer details (including elapsed time for running timers)
app.get('/timers/:id', (req, res) => {
  const timerId = parseInt(req.params.id);
  const timers = readTimers();
  
  const timer = timers.find(t => t.id === timerId);
  
  if (!timer) {
    return res.status(404).json({
      success: false,
      error: 'Timer not found.',
      message: `No timer found with ID: ${timerId}`
    });
  }
  
  // Calculate current elapsed time
  let currentElapsed;
  if (timer.status === 'running') {
    currentElapsed = formatElapsedTime(Date.now() - timer.startTime);
  } else {
    currentElapsed = timer.elapsedTime;
  }
  
  res.json({
    success: true,
    timer: {
      id: timer.id,
      label: timer.label,
      startTime: new Date(timer.startTime).toISOString(),
      endTime: timer.endTime ? new Date(timer.endTime).toISOString() : null,
      elapsedTime: currentElapsed,
      status: timer.status
    }
  });
});

// GET /timers - Get all timers
app.get('/timers', (req, res) => {
  const timers = readTimers();
  
  // Add current elapsed time for running timers
  const timersWithElapsed = timers.map(timer => {
    let currentElapsed;
    if (timer.status === 'running') {
      currentElapsed = formatElapsedTime(Date.now() - timer.startTime);
    } else {
      currentElapsed = timer.elapsedTime;
    }
    
    return {
      id: timer.id,
      label: timer.label,
      startTime: new Date(timer.startTime).toISOString(),
      endTime: timer.endTime ? new Date(timer.endTime).toISOString() : null,
      elapsedTime: currentElapsed,
      status: timer.status
    };
  });
  
  res.json({
    success: true,
    timers: timersWithElapsed,
    count: timersWithElapsed.length
  });
});

// DELETE /timers/:id - Delete a timer
app.delete('/timers/:id', (req, res) => {
  const timerId = parseInt(req.params.id);
  let timers = readTimers();
  
  const index = timers.findIndex(t => t.id === timerId);
  
  if (index === -1) {
    return res.status(404).json({
      success: false,
      error: 'Timer not found.',
      message: `No timer found with ID: ${timerId}`
    });
  }
  
  const deletedTimer = timers.splice(index, 1)[0];
  writeTimers(timers);
  
  res.json({
    success: true,
    message: 'Timer deleted successfully.',
    deletedTimer: {
      id: deletedTimer.id,
      label: deletedTimer.label
    }
  });
});

// POST /timers/:id/reset - Reset a timer (restart from zero)
app.post('/timers/:id/reset', (req, res) => {
  const timerId = parseInt(req.params.id);
  const timers = readTimers();
  
  const timer = timers.find(t => t.id === timerId);
  
  if (!timer) {
    return res.status(404).json({
      success: false,
      error: 'Timer not found.',
      message: `No timer found with ID: ${timerId}`
    });
  }
  
  // Reset the timer
  timer.startTime = Date.now();
  timer.endTime = null;
  timer.elapsedTime = null;
  timer.status = 'running';
  
  writeTimers(timers);
  
  res.json({
    success: true,
    timer: {
      id: timer.id,
      label: timer.label,
      startTime: new Date(timer.startTime).toISOString(),
      status: timer.status
    },
    message: 'Timer reset successfully.'
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`⏱️  Timer microservice running at http://localhost:${PORT}`);
  console.log(`📊 Test the API at http://localhost:${PORT}/index.html`);
});
