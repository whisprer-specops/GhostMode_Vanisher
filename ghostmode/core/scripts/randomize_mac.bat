@echo off
REM Randomize MAC address on Windows using PowerShell
echo [*] Attempting MAC address randomization...

powershell -Command "& {
    Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | ForEach-Object {
        $newMAC = ((Get-Random -Minimum 0 -Maximum 255).ToString("X2") + '-' + `
                   (Get-Random -Minimum 0 -Maximum 255).ToString("X2") + '-' + `
                   (Get-Random -Minimum 0 -Maximum 255).ToString("X2") + '-' + `
                   (Get-Random -Minimum 0 -Maximum 255).ToString("X2") + '-' + `
                   (Get-Random -Minimum 0 -Maximum 255).ToString("X2") + '-' + `
                   (Get-Random -Minimum 0 -Maximum 255).ToString("X2"))
        Set-NetAdapterAdvancedProperty -Name $_.Name -RegistryKeyword "NetworkAddress" -RegistryValue $newMAC
        Write-Output ('[+] New MAC for ' + $_.Name + ': ' + $newMAC)
    }
}"
pause
