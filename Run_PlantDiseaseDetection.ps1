Write-Host "Lancement de localtunnel dans une nouvelle fenêtre..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "lt --port 5000 --subdomain docfarm"

Start-Sleep -Seconds 3

Write-Host "Lancement de l'API Flask dans une nouvelle fenêtre..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'Flask Deployed App'; python app_V2.py"


