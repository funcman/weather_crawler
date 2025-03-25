# 提交后脚本 - 在提交完成后运行
# 使用方法：将此脚本设置为Git钩子 - .git/hooks/post-commit

# 检查备份文件是否存在
if (Test-Path .env.bak) {
    # 恢复原始文件
    Copy-Item .env.bak .env -Force
    Remove-Item .env.bak -Force
    
    Write-Host "已恢复原始.env文件与API密钥"
} else {
    Write-Host "未找到.env备份文件，无法恢复"
}

# 退出成功
exit 0 