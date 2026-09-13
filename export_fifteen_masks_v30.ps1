$ErrorActionPreference='Stop'
$encoder='C:\Users\matts\AppData\Local\Programs\Python\Python313\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
$movie=Join-Path $PSScriptRoot 'petals_fifteen_masks_v30_video.mov'
$output=Join-Path $PSScriptRoot 'petals_fifteen_masks_v30.mp4'
& $encoder -hide_banner -loglevel error -y -i $movie -i 'C:\Users\matts\Music\petals.wav' -map 0:v:0 -map 1:a:0 -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 256k -t 283.65 -movflags +faststart $output
if ($LASTEXITCODE -ne 0) { throw 'Thirteen-mask encoding failed' }





