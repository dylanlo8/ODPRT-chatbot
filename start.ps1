# start_app.ps1

# Start backend server in a new window and keep it running
Write-Host "Starting backend server..."
$backendProcess = Start-Process -FilePath "python" -ArgumentList "chatbot/backend/main.py" -PassThru -NoNewWindow

# Wait a few seconds for backend to initialize
Write-Host "Waiting for backend to initialize..."
Start-Sleep -Seconds 5

# Navigate to frontend directory and start React app
Write-Host "Starting frontend application..."
Set-Location chatbot/frontend
npm start

# When the frontend is closed, terminate the backend process
$backendProcess.Kill()
