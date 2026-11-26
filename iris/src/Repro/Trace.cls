/// Read-only investigation helpers: print what IRIS recorded for one HL7 control id.
Class Repro.Trace
{

/// Everything the article's investigation needs for one message, in order:
/// 1. message headers of the session (who sent what to whom, status)
/// 2. the Event Log entries of that session (warnings/errors/info)
ClassMethod Report(pControlId As %String)
{
	Set tSession = ..SessionFor(pControlId)
	If tSession = "" { Write "no session found for ",pControlId,! Quit }
	Write "== message headers (session ",tSession,")",!
	Set rs = ##class(%SQL.Statement).%ExecDirect(,"SELECT ID, TimeCreated, SourceConfigName, TargetConfigName, MessageBodyClassName, Status, Type, Description FROM Ens.MessageHeader WHERE SessionId = ? ORDER BY ID", tSession)
	While rs.%Next() {
		Write $Justify(rs.ID,4)," ",$Extract(rs.TimeCreated,12,23)," ",rs.SourceConfigName," -> ",rs.TargetConfigName,"  [",$Case(rs.Type,1:"Request",2:"Response",:rs.Type),"/",rs.Status,"] ",rs.Description,!
	}
	Write "== event log",!
	Set rs = ##class(%SQL.Statement).%ExecDirect(,"SELECT TimeLogged, Type, ConfigName, Text FROM Ens_Util.Log WHERE SessionId = ? AND Type IN (1,2,3,4) ORDER BY ID", tSession)
	While rs.%Next() {
		Write $Extract(rs.TimeLogged,12,23)," ",$Case(rs.Type,1:"ASSERT",2:"ERROR",3:"WARNING",4:"INFO",:rs.Type)," [",rs.ConfigName,"] ",rs.Text,!
	}
}

/// One machine-readable line per message for the test matrix:
///   SUMMARY|<final status of the request to the operation>|<action codes seen, in order>|<error count>
ClassMethod Summary(pControlId As %String)
{
	Set tSession = ..SessionFor(pControlId)
	If tSession = "" { Write "SUMMARY|NOSESSION||",! Quit }
	Set tStatus = ""
	Set rs = ##class(%SQL.Statement).%ExecDirect(,"SELECT %EXTERNAL(Status) AS S FROM Ens.MessageHeader WHERE SessionId = ? AND TargetConfigName LIKE 'out.%' AND Type = 1 ORDER BY ID DESC", tSession)
	If rs.%Next() Set tStatus = rs.S
	Set tActions = "", tErrs = 0
	Set rs = ##class(%SQL.Statement).%ExecDirect(,"SELECT Type, Text FROM Ens_Util.Log WHERE SessionId = ? AND Type IN (2,3) ORDER BY ID", tSession)
	While rs.%Next() {
		If rs.Type = 2 Set tErrs = tErrs + 1
		Set tPos = $Find(rs.Text, "resulting in Action code ")
		If tPos { Set tCode = $Piece($Extract(rs.Text, tPos, *), " ", 1), tActions = tActions _ $Select(tActions="":"",1:",") _ tCode }
	}
	Write "SUMMARY|",tStatus,"|",tActions,"|",tErrs,!
}

/// Drop the operation's TCP connection (disable then re-enable the item), so that bytes still sitting in the
/// socket - e.g. an ACK that arrived after ResponseTimeout - cannot show up as
/// "Discarding data found in buffer before HL7 send" in the NEXT, unrelated test.
ClassMethod ResetOperation(pConfigName As %String)
{
	Set tSC = ##class(Ens.Director).EnableConfigItem(pConfigName, 0)
	Set tSC2 = ##class(Ens.Director).EnableConfigItem(pConfigName, 1)
	Write "RESET|",pConfigName,"|",$$$ISOK(tSC),"|",$$$ISOK(tSC2),!
}

/// Session id of the inbound request whose MSH-10 equals pControlId (lab-scale scan, newest first)
ClassMethod SessionFor(pControlId As %String) As %String
{
	Set rs = ##class(%SQL.Statement).%ExecDirect(,"SELECT ID, SessionId, MessageBodyId FROM Ens.MessageHeader WHERE MessageBodyClassName = 'EnsLib.HL7.Message' AND SourceConfigName LIKE 'in.%' ORDER BY ID DESC")
	While rs.%Next() {
		Set tMsg = ##class(EnsLib.HL7.Message).%OpenId(rs.MessageBodyId)
		If $IsObject(tMsg), tMsg.GetValueAt("MSH:10") = pControlId Quit
	}
	Quit rs.SessionId
}

}
