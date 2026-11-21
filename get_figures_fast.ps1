$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("D:\Vibe code\BTL_DACN_CNPM\BTL_DACN_CNPM_3.docx")
    Write-Host "=== DANH SÁCH HÌNH VẼ CHƯƠNG 4 ==="
    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^Hình\s+4\.\d+" -and $txt -notmatch "\.{4,}") {
            $page = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
            Write-Host "$txt ===> Page $page"
        }
    }
    Write-Host "`n=== DANH SÁCH BẢNG BIỂU CHƯƠNG 4 ==="
    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^Bảng\s+4\.\d+" -and $txt -notmatch "\.{4,}") {
            $page = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
            Write-Host "$txt ===> Page $page"
        }
    }
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
