# latex-index-tool 一键安装脚本 (Windows PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "=== latex-index-tool 安装脚本 ===" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
$python = $null
foreach ($cmd in @("python", "python3")) {
    try {
        $ver = & $cmd -c "import sys; print(sys.version_info[:2])" 2>$null
        if ($ver -match "\((\d+),") {
            $major = [int]$Matches[1]
            if ($major -ge 3) {
                $python = $cmd
                break
            }
        }
    } catch {}
}

if (-not $python) {
    Write-Host "错误: 未找到 Python 3.10+。请从 https://www.python.org/downloads/ 安装" -ForegroundColor Red
    exit 1
}

Write-Host "检测到 Python: $(& $python --version)"

# 安装
Write-Host ""
Write-Host ">>> 安装 latex-index-tool ..."
& $python -m pip install --upgrade pip -q
& $python -m pip install latex-index-tool -q

Write-Host ""
Write-Host "可选组件:"
Write-Host "  pip install latex-index-tool[tui]        # Rich TUI 界面"
Write-Host "  pip install latex-index-tool[xindy]      # 中文拼音排序"
Write-Host "  pip install latex-index-tool[progress]   # 进度条"
Write-Host "  pip install latex-index-tool[all]        # 全部"

# 验证
Write-Host ""
Write-Host ">>> 验证安装 ..."
try {
    & $python -m latex_index --help | Out-Null
    Write-Host "安装成功！" -ForegroundColor Green
    Write-Host ""
    Write-Host "快速开始:"
    Write-Host "  latex-index insert --chapter 1 --dry-run"
    Write-Host "  latex-index --help"
} catch {
    Write-Host "安装后无法运行，请检查 PATH" -ForegroundColor Yellow
}
