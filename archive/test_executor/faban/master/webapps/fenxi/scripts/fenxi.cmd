@echo off

REM ########################################################################
REM # Project FenXi
REM #
REM # fenxi -	Wrapper script for "process" and "compare"
REM #
REM # Shell script to process or compare a set of benchmark runs. It sets
REM # the environment variables and path and executes the ProcessRun
REM # program.
REM # 
REM # FenXi uses Derby.jar to implement backend DB, JFreeChart.jar to
REM # implement the Charting and JRuby.jar for ruby script processing.
REM #
REM ########################################################################

REM Get the process, and profile if any
set ARG_COUNT=0
set PROCESS=%1
SHIFT
if "%2"=="-p" (
	set PROFILE=%3_profile
	SHIFT
	SHIFT
	)
if "%2"=="-profile" (
	set PROFILE=%3_profile
	SHIFT
	SHIFT
	)
REM Get the command line arguments
set CMD_LINE_ARGS=
:setArgs
 set /A ARG_COUNT += 1
 if ""%1""=="""" goto doneSetArgs
 if ""%3""=="""" (
 	if NOT ""%2""=="""" set LAST_ARG=%2
 	if NOT ""%2""=="""" set PRE_LAST_ARG=%1
	)
 set CMD_LINE_ARGS=%CMD_LINE_ARGS% %1
 shift
 goto setArgs
:doneSetArgs

call :CHECK_JAVA

REM set BINDIR and VERSION
set BINDIR=%~dp0
set VERSION=2.1

REM %~d0
cd %BINDIR%
cd ..

REM Set FenXi home directory
set FENXI_HOME=%CD%

REM Set the scripts directory and txt2db directory
cd scripts
set FENXI_SCRIPTS=%FENXI_HOME%\scripts
set FENXI_HOST=localhost

REM Set the prog to fenxi
set PROG=%FENXI_SCRIPTS%\fenxi

REM Set the path and classpath to access the libraries
set PATH=%FENXI_HOME%\WEB-INF\lib;%PATH%
set PERL5LIB=%FENXI_HOME%\txt2db
set CLASSPATH=%FENXI_HOME%\WEB-INF\lib\spark.jar;%FENXI_HOME%\WEB-INF\classes;%FENXI_HOME%\WEB-INF\lib\derby.jar;%FENXI_HOME%\WEB-INF\lib\jfreechart.jar;%FENXI_HOME%\WEB-INF\lib\jcommon.jar;%FENXI_HOME%\WEB-INF\lib\jruby-complete-1.1.6.jar
set IJ_CLASSPATH=%FENXI_HOME%\WEB-INF\lib\derbytools.jar;%FENXI_HOME%\WEB-INF\lib\derby.jar

REM Set the java arguments
set JAVA_ARGS=-mx1536m -Dderby.storage.pageReservedSpace=0 -Dderby.language.logQueryPlan=true -Dderby.storage.rowLocking=false -Dfenxi.basedir=%FENXI_HOME% -Djava.awt.headless=true -Dsun.java2d.pmoffscreen=false

REM Check the PATHEXT and set it to the default if if does not exist
if not defined PATHEXT set PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;

rmdir /s /q txt
mkdir txt

REM Shift does not change the value in %*.
if "%PROCESS%"=="process" (
	echo %ARG_COUNT%
	if %ARG_COUNT% NEQ 4 (
		call :USAGE
	)
	rmdir /s /q %PRE_LAST_ARG%
	%JAVA% -cp %CLASSPATH% %JAVA_ARGS% -Dfenxi.profile=%PROFILE% org.fenxi.cmd.process.FenxiProcess %CMD_LINE_ARGS%
	%JAVA% -cp %CLASSPATH% %JAVA_ARGS% org.jruby.Main %FENXI_HOME%\ruby\main.rb view %CMD_LINE_ARGS%
	GOTO:EOF
)
if "%PROCESS%"=="compare" (
	if %ARG_COUNT% LSS 3 (
		call :USAGE
	)
	rmdir /s /q %LAST_ARG%
	%JAVA% -cp %CLASSPATH% %JAVA_ARGS% org.jruby.Main %FENXI_HOME%\ruby\main.rb comp %CMD_LINE_ARGS%
	GOTO:EOF
)
if "%PROCESS%"=="ij" (
	%JAVA% -cp %IJ_CLASSPATH% %JAVA_ARGS% -Dij.protocol=jdbc:derby: -Dij.database=%CMD_LINE_ARGS% org.apache.derby.tools.ij
	GOTO:EOF
)

REM ** Usage function
:USAGE
echo. FenXi version %VERSION%
echo. usage
echo. 	fenxi process [-p ^| -profile name] rawdir htmldir expt_name
echo. 	fenxi compare rundir1 rundir2 [...] outdir
echo.	fenxi ij htmldir\xanaDB ^> ^&2
PAUSE
EXIT

REM ** Check for JAVA
:CHECK_JAVA
REM ** Check if JAVA_HOME is specified.
if exist %JAVA_HOME% set JAVA=%JAVA_HOME%\bin\java.exe

REM ** If JAVA is not in JAVA_HOME, then search PATH
if not exist %JAVA% for %%j in ( %PATH% ) do if exist %%j\java.exe	set JAVA=%%j\java.exe

REM ** Couldn't find it, so exit with an error
if not exist %JAVA% (
       echo "JAVA_HOME was not specified correctly. Please re-run FenXi with the JAVA_HOME set to the right directory."
       PAUSE
       EXIT
)
GOTO:EOF
