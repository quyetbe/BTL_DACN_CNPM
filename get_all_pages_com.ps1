$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("D:\Vibe code\BTL_DACN_CNPM\BTL_DACN_CNPM.docx")
    
    Write-Host "=== HEADINGS ==="
    foreach ($p in $doc.Paragraphs) {
        $t = $p.Range.Text.Trim()
        $pg = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
        if ($pg -ge 11 -and ($t -match "^(CHƯƠNG|[1-5]\.\d|KẾT LUẬN|TÀI LIỆU|PHỤ LỤC)") -and ($t -notmatch "\.{4,}")) {
            Write-Host "$t ===> Page $pg"
        }
    }

    Write-Host "`n=== FIGURES ==="
    foreach ($p in $doc.Paragraphs) {
        $t = $p.Range.Text.Trim()
        $pg = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
        if ($pg -ge 11 -and ($t -match "^Hình\s+4\.\d+") -and ($t -notmatch "\.{4,}")) {
            Write-Host "$t ===> Page $pg"
        }
    }

    Write-Host "`n=== TABLES ==="
    foreach ($p in $doc.Paragraphs) {
        $t = $p.Range.Text.Trim()
        $pg = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
        if (($t -match "^Bảng\s+\d+\.\d+") -and ($t -notmatch "\.{4,}")) {
            Write-Host "$t ===> Page $pg"
        }
    }

    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
