Function Get-NeglectedFiles
{
	Param([string[]]$path, [int]$numberDays, [string[]]$_exclude)
	$cutOffDate = (Get-Date).AddDays(-$numberDays)
	Write-Host "Cut Off Date:" $cutOffDate
	Get-ChildItem -Path $path -exclude $_exclude -recurse -ErrorAction Continue | Where-Object {$_.LastAccessTime -le $cutOffDate}
} 

#Get-NeglectedFiles -path $env:userprofile -_exclude *.tmp, *html -numberDays 90 | select DirectoryName,name, *time > $env:userprofile\desktop\used_within_last_90_days.txt
Get-NeglectedFiles -path "\\srv-dc\staff$" -_exclude *.tmp, *html -numberDays 1460 | Measure-Object -Property length -sum
