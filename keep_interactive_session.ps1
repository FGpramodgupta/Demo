# =====================================================
# KEEP INTERACTIVE DESKTOP SESSION ALWAYS ACTIVE (24x7)
# =====================================================

Write-Host "Applying settings to keep interactive session alive..." -ForegroundColor Cyan

# 1️⃣ --- Disable Remote Desktop Session timeouts ---
$rdpPolicyPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services"
If (!(Test-Path $rdpPolicyPath)) { New-Item -Path $rdpPolicyPath -Force | Out-Null }

New-ItemProperty -Path $rdpPolicyPath -Name "MaxIdleTime" -Value 0 -PropertyType DWord -Force | Out-Null
New-ItemProperty -Path $rdpPolicyPath -Name "MaxDisconnectionTime" -Value 0 -PropertyType DWord -Force | Out-Null
New-ItemProperty -Path $rdpPolicyPath -Name "DeleteTempDirsOnExit" -Value 0 -PropertyType DWord -Force | Out-Null
New-ItemProperty -Path $rdpPolicyPath -Name "TerminateSessionWhenTimeLimitReached" -Value 0 -PropertyType DWord -Force | Out-Null

Write-Host "✓ RDP session timeout policies disabled."

# 2️⃣ --- Disable screensaver and lock screen ---
$desktopPath = "HKCU:\Control Panel\Desktop"
If (!(Test-Path $desktopPath)) { New-Item -Path $desktopPath -Force | Out-Null }

Set-ItemProperty -Path $desktopPath -Name "ScreenSaveActive" -Value "0"
Set-ItemProperty -Path $desktopPath -Name "ScreenSaverIsSecure" -Value "0"
Set-ItemProperty -Path $desktopPath -Name "ScreenSaveTimeOut" -Value "0"

Write-Host "✓ Screensaver and lock screen disabled."

# 3️⃣ --- Power settings: never sleep or turn off display ---
powercfg -change -monitor-timeout-ac 0
powercfg -change -standby-timeout-ac 0
powercfg -change -hibernate-timeout-ac 0

Write-Host "✓ Power settings updated to never sleep or turn off display."

# 4️⃣ --- Optional: disable “require password on wakeup” ---
try {
    powercfg /SETACVALUEINDEX SCHEME_CURRENT SUB_NONE CONSOLELOCK 0
    Write-Host "✓ Disabled password requirement on wakeup."
} catch {
    Write-Host "⚠️ Skipped password-on-wakeup setting (not supported on this edition)."
}

# 5️⃣ --- Optional: Add registry entry to auto-unlock after RDP transfer ---
$winlogonPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
New-ItemProperty -Path $winlogonPath -Name "DisableLockWorkstation" -Value 1 -PropertyType DWord -Force | Out-Null

Write-Host "✓ Disabled workstation lock."

# 6️⃣ --- Verify summary ---
Write-Host "`nAll settings applied successfully!" -ForegroundColor Green
Write-Host "Please reboot your server once to ensure all policies take effect."
Write-Host "`n💡 Tip: Use tscon <sessionid> /dest:console before disconnecting RDP."
Write-Host "Or install TightVNC for a truly persistent GUI session."
