# 预提交脚本 - 将在提交前运行
# 使用方法：将此脚本设置为Git钩子 - .git/hooks/pre-commit

# 设置UTF-8编码
$OutputEncoding = [System.Text.Encoding]::UTF8

# 备份原始.env文件
Copy-Item .env .env.bak -Force

# 创建一个临时的.env文件，替换所有API密钥
$envContent = Get-Content .env -Encoding UTF8
$cleanedContent = $envContent -replace 'API_KEY=.*', 'API_KEY=your_openweathermap_api_key_here' `
                             -replace 'WEATHERAPI_KEY=.*', 'WEATHERAPI_KEY=your_weatherapi_key_here' `
                             -replace 'VISUALCROSSING_KEY=.*', 'VISUALCROSSING_KEY=your_visualcrossing_key_here'

# 写入临时文件
Set-Content .env.clean -Value $cleanedContent -Encoding UTF8

# 替换原始文件
Move-Item .env.clean .env -Force

# 输出处理信息
Write-Host "API密钥已替换为占位符，准备提交..."

# 退出成功
exit 0 