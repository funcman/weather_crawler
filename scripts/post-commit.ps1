# �ύ��ű� - ���ύ��ɺ�����
# ʹ�÷��������˽ű�����ΪGit���� - .git/hooks/post-commit

# ��鱸���ļ��Ƿ����
if (Test-Path .env.bak) {
    # �ָ�ԭʼ�ļ�
    Copy-Item .env.bak .env -Force
    Remove-Item .env.bak -Force
    
    Write-Host "�ѻָ�ԭʼ.env�ļ���API��Կ"
} else {
    Write-Host "δ�ҵ�.env�����ļ����޷��ָ�"
}

# �˳��ɹ�
exit 0 