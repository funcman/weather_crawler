# PowerShell�ű��������������ļ��е�API��Կ

# ����������������ΪUTF-8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$input | ForEach-Object {
    $_ -replace 'API_KEY=.*', 'API_KEY=your_openweathermap_api_key_here' `
       -replace 'WEATHERAPI_KEY=.*', 'WEATHERAPI_KEY=your_weatherapi_key_here' `
       -replace 'VISUALCROSSING_KEY=.*', 'VISUALCROSSING_KEY=your_visualcrossing_key_here'
} 