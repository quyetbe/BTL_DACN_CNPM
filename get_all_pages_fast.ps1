$outputFile = "D:\Vibe code\BTL_DACN_CNPM\actual_pages_log.txt"
if (Test-Path $outputFile) { Remove-Item $outputFile }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("D:\Vibe code\BTL_DACN_CNPM\BTL_DACN_CNPM.docx")
    foreach ($p in $doc.Paragraphs) {
        $t = $p.Range.Text.Trim()
        if ($t.Length -gt 3 -and $t -notmatch "\.{4,}") {
            if ($t -match "^(CHƯƠNG\s+[I|V|X]+|KẾT LUẬN|TÀI LIỆU|PHỤ LỤC|4\.[1-2]\.\d|5\.[1-4]|Hình\s+[4-5]\.\d+|Bảng\s+\d+\.\d+)") {
                $pg = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
                $line = "$t ===> Page $pg"
                Add-Content -Path $outputFile -Value $line -Encoding utf8
                Write-Host $line
            }
        }
    }
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
