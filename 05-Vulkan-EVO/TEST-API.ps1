param([int]$Port=8091)
$ErrorActionPreference = 'Stop'
if ($Port -lt 1024 -or $Port -gt 65535) { throw 'Invalid port.' }
$url = "http://127.0.0.1:$Port"
Invoke-RestMethod "$url/health" -TimeoutSec 15
$request = @{model='lokales-modell';messages=@(@{role='user';content='Reply with only the word ready.'});max_tokens=32;temperature=0;stream=$false} | ConvertTo-Json -Depth 8
$reply = Invoke-RestMethod "$url/v1/chat/completions" -Method Post -ContentType 'application/json' -Body $request -TimeoutSec 180
$reply.choices[0].message.content
# A returned response is the check; do not report a result before your own test.
