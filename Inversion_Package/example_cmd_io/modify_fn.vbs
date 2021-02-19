Option Explicit  ' Checks that you have declared all variables

Dim objFSO, objFile, objFolder, colFiles, item

Dim currDir
Dim strSearchString, strSearchFor, strFoundName, strModifiedName, intFoundName, charIndex, intAdd

intAdd = Wscript.Arguments.Item(0)

'Wscript.Echo intAdd

CONST ForReading = 1
CONST ForWriting = 2

Set objFSO = CreateObject("Scripting.FileSystemObject")
currDir = objFSO.GetParentFolderName(Wscript.ScriptFullName)

Set objFolder = objFSO.GetFolder(currDir)
'Wscript.Echo objFolder.Path
Set colFiles = objFolder.Files

strSearchFor = "num_"
For each item In colFiles
	'Wscript.Echo item.Name
	If InStr(1, item.Name, strSearchFor) > 0 then
		'Wscript.Echo item.Name
		strFoundName = item.Name
	End If
Next

'Wscript.Echo Mid(strFoundName, 1, 4)
'charIndex = InStr(strFoundName, ".")
'Wscript.Echo Mid(strFoundName, 5)
intFoundName = CInt(Mid(strFoundName, 5)) + intAdd

strModifiedName = Mid(strFoundName,1,4) + CStr(intFoundName) '+ ".txt"


'Wscript.Echo charIndex

'Wscript.Echo strModifiedName

objFso.MoveFile strFoundName, strModifiedName

