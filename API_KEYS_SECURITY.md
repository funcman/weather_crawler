# API密钥安全处理指南

## API密钥保护机制

本项目包含了自动保护API密钥的Git钩子设置。此机制确保您可以在本地使用真实的API密钥进行开发，但在提交到GitHub时会自动将密钥替换为占位符。

### 工作原理

1. 提交前（pre-commit钩子）：
   - 自动备份您的`.env`文件
   - 替换所有API密钥为占位符（例如：`your_openweathermap_api_key_here`）
   - 提交替换后的文件到Git

2. 提交后（post-commit钩子）：
   - 自动恢复您的原始`.env`文件
   - 删除备份文件

### 项目设置

- `.gitattributes`：配置Git对`.env`文件使用过滤器
- `scripts/prepare-commit.ps1`：在提交前替换API密钥
- `scripts/post-commit.ps1`：在提交后恢复原始文件

### 首次克隆仓库

首次克隆仓库后，您需要：

1. 复制`.env.example`到`.env`
2. 在`.env`文件中填入您的真实API密钥

```bash
cp .env.example .env
# 然后编辑.env文件添加您的API密钥
```

### 钩子设置（新团队成员）

当新团队成员克隆此仓库时，他们需要启用钩子：

```bash
# 确保钩子目录存在
mkdir -p .git/hooks

# 复制钩子脚本
cp scripts/prepare-commit.ps1 .git/hooks/pre-commit.ps1
cp scripts/post-commit.ps1 .git/hooks/post-commit.ps1

# 创建钩子引导文件
echo '#!/bin/sh
powershell.exe -ExecutionPolicy Bypass -File ".git/hooks/pre-commit.ps1"
exit $?' > .git/hooks/pre-commit

echo '#!/bin/sh
powershell.exe -ExecutionPolicy Bypass -File ".git/hooks/post-commit.ps1"
exit $?' > .git/hooks/post-commit

# 设置执行权限
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit
```

## 其他安全建议

除了使用这些Git钩子外，还建议：

1. 不要在代码、日志或错误报告中暴露API密钥
2. 定期轮换API密钥
3. 为不同环境（开发、测试、生产）使用不同的API密钥
4. 考虑使用环境变量或专用的密钥管理服务（如AWS Secrets Manager或HashiCorp Vault） 