$sourceDir = "D:\Mano Projaktai\Pretty Much\PM-GlowingMushrums\source"
$destDir = "/home/eimansun/PM-GlowingMushrooms/source"

function Start-SSHTransfer {
    param ($sourceDir, $destDir)
    foreach ($file in Get-Childitem -Path $sourceDir ) {
        
        if ($file.PSIsContainer) {
            Start-SSHTransfer -sourceDir $file.FullName -destDir ($destDir + "/$($file.Name)")
        } 
        else {
            scp $file.FullName eimansun@RPI-Z.local:$destDir
        }

        write-host $destDir

        
    }
}


Start-SSHTransfer  -sourceDir $sourceDir -destDir $destDir

#Invoke-Command -HostName "eimansun@RPI-Z.local" -ScriptBlock { touch yo } -KeyFilePath /Eiman/UserAKey_rsa
# ssh eimansun@RPI-Z.local 'uname;hostname;date;touch yo && exit &'
