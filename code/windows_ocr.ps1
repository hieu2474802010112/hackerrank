param([Parameter(Mandatory=$true)][string]$ImagePath)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
} | Select-Object -First 1
function Await-Result($Operation, $ResultType) {
    $task = $asTask.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.Wait()
    return $task.Result
}
$fileType = [Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime]
$streamType = [Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType=WindowsRuntime]
$decoderType = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
$bitmapType = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType=WindowsRuntime]
$resultType = [Windows.Media.Ocr.OcrResult, Windows.Foundation, ContentType=WindowsRuntime]
$engineType = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
$languageType = [Windows.Globalization.Language, Windows.Globalization, ContentType=WindowsRuntime]
$language = $languageType::new('en-US')
$engine = $engineType::TryCreateFromLanguage($language)
if ($null -eq $engine) { throw 'Windows English OCR language is unavailable' }
$file = Await-Result ($fileType::GetFileFromPathAsync($ImagePath)) $fileType
$stream = Await-Result ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) $streamType
try {
    $decoder = Await-Result ($decoderType::CreateAsync($stream)) $decoderType
    $bitmap = Await-Result ($decoder.GetSoftwareBitmapAsync()) $bitmapType
    try {
        $result = Await-Result ($engine.RecognizeAsync($bitmap)) $resultType
        $lines = @($result.Lines | ForEach-Object { $_.Text })
        @{text=($lines -join "`n"); lines=$lines; backend='windows-ocr'; language='en-US'} | ConvertTo-Json -Depth 5 -Compress
    } finally { $bitmap.Dispose() }
} finally { $stream.Dispose() }
