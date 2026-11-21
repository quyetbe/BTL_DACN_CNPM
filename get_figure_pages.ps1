$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("D:\Vibe code\BTL_DACN_CNPM\BTL_DACN_CNPM.docx")
    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        $page = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
        if ($page -gt 10 -and $txt -match "^Hình\s+4\.\d+") {
            Write-Host "$txt ===> Page $page"
        }
    }
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
