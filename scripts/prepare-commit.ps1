# Ԥ�ύ�ű� - �����ύǰ����
# ʹ�÷��������˽ű�����ΪGit���� - .git/hooks/pre-commit

# ����UTF-8����
$OutputEncoding = [System.Text.Encoding]::UTF8

# ����ԭʼ.env�ļ�
Copy-Item .env .env.bak -Force

# ����һ����ʱ��.env�ļ����滻����API��Կ
$envContent = Get-Content .env -Encoding UTF8
$cleanedContent = $envContent -replace 'API_KEY=.*', 'API_KEY=your_openweathermap_api_key_here' `
                             -replace 'WEATHERAPI_KEY=.*', 'WEATHERAPI_KEY=your_weatherapi_key_here' `
                             -replace 'VISUALCROSSING_KEY=.*', 'VISUALCROSSING_KEY=your_visualcrossing_key_here'

# д����ʱ�ļ�
Set-Content .env.clean -Value $cleanedContent -Encoding UTF8

# �滻ԭʼ�ļ�
Move-Item .env.clean .env -Force

# ���������Ϣ
Write-Host "API��Կ���滻Ϊռλ����׼���ύ..."

# �˳��ɹ�
exit 0 