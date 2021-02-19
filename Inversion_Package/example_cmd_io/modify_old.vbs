Option Explicit  ' Checks that you have declared all variables

Dim objFSO, objFile, maxRetry, numRetries, newRetries
Dim strText, strLine  ' declare these also
CONST ForReading = 1
CONST ForWriting = 2

Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.OpenTextFile(MICacheFilename(), ForReading)
maxRetry = CInt(MIGetTaskParam("maxRetry"))

' strText = objFile.ReadAll  ' Not needed

numRetries = CInt(objFile.ReadLine)  ' just read the one line in the file


newRetries = numRetries + 1
'WScript.Echo "numRetries = [" & numRetries & "]"
'WScript.Echo "newRetries = [" & newRetries & "]"
'strLine = Replace(numRetries,numRetries ,newRetries)  ' does nothing, 'strline' is empty

Set objFile = objFSO.OpenTextFile(MICacheFilename(), ForWriting)
objFile.WriteLine newRetries
objFile.Close

'WScript.Echo "strLine = [" & strLine & "]"

' Dummy Function.
Function MICacheFilename()
    MICacheFilename = "num.txt"
End Function

' Dummy Function.
Function MIGetTaskParam(key)
    MIGetTaskParam = 13
End Function

' Dummy Sub.
Sub MISetTaskParam(arg1, arg2)
End Sub