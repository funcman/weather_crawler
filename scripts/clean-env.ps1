# PowerShell脚本，用于清理环境文件中的API密钥

# 设置输入和输出编码为UTF-8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$input | ForEach-Object {
    $_ -replace 'API_KEY=.*', 'API_KEY=your_openweathermap_api_key_here' `
       -replace 'WEATHERAPI_KEY=.*', 'WEATHERAPI_KEY=your_weatherapi_key_here' `
       -replace 'VISUALCROSSING_KEY=.*', 'VISUALCROSSING_KEY=your_visualcrossing_key_here'
} 