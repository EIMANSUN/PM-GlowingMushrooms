$sourceDir = "D:\Mano Projaktai\Pretty Much\PM-GlowingMushrums\source"
$destDir = "/home/eimansun/PM-GlowingMushrooms"
foreach ($file in Get-Childitem -Path $sourceDir) {
    scp $file.FullName eimansun@RPI-Z.local:$destDir
}

#Invoke-Command -HostName "eimansun@RPI-Z.local" -ScriptBlock { touch yo } -KeyFilePath /Eiman/UserAKey_rsa
# ssh eimansun@RPI-Z.local 'uname;hostname;date;touch yo && exit &'
