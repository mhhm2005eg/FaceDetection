import os
import shlex, subprocess
import sys, getopt
import logging
import glob
from os.path import basename , dirname
#import CppHeaderParser
import shutil
import common
from config import TargetsToBuild , Components , Compile_Wrappers , Compile_Main , LINK , Generate_Main , Compile_Aux , Debug , Lib_SCAN





FilesToBuild=["main.c"]
TargetToBuild_IncludeOptions={"ti_c674x": "IncludeOption_ti_c674x", "ti_arp32": "IncludeOption_ti_arp32", "ti_cortex_a15": "IncludeOption_ti_cortex_a15", "ti_cortex_a8": "IncludeOption_ti_cortex_a8"}

IncludeOption={"ti_c674x":"","ti_arp32":"","ti_cortex_a8":"","ti_cortex_a15":""}

Cores = ["ti_arp32","ti_c674x","ti_cortex_a8","ti_cortex_a15"]
LinkerRelative = {"ti_c674x":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\c6000\\bin\\cl6x.exe", \
				   "ti_arp32":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\arp32\\bin\\cl-arp32.exe",\
					"ti_cortex_a8":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi\\gcc-arm-none-eabi-4_7-2012q4\\bin\\arm-none-eabi-gcc.exe",\
					"ti_cortex_a15":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi\\gcc-arm-none-eabi-4_7-2012q4\\bin\\arm-none-eabi-gcc.exe"\
				   }
BuilderRelative = {"ti_c674x":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\c6000\\bin\\cl6x.exe", \
				   "ti_arp32":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\arp32\\bin\\cl-arp32.exe",\
					"ti_cortex_a8":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi\\gcc-arm-none-eabi-4_7-2012q4\\bin\\arm-none-eabi-gcc.exe",\
					"ti_cortex_a15":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi\\gcc-arm-none-eabi-4_7-2012q4\\bin\\arm-none-eabi-gcc.exe"\
				   }
ArchiverRelative = {"ti_c674x":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\c6000\\bin\\ar6x.exe", \
					"ti_arp32":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\arp32\\bin\\ar-arp32.exe",\
					"ti_cortex_a8":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi\\gcc-arm-none-eabi-4_7-2012q4\\bin\\arm-none-eabi-ar.exe",\
					"ti_cortex_a15":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi\\gcc-arm-none-eabi-4_7-2012q4\\bin\\arm-none-eabi-ar.exe"\
					}
LibCRelative =     {"ti_c674x":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\c6000\\lib\\libc.a", \
				   "ti_arp32":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\arp32\\lib\\libc.a",\
					"ti_cortex_a8":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi\\gcc-arm-none-eabi-4_7-2012q4\\arm-none-eabi\\lib\\libc.a",\
					"ti_cortex_a15":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi\\gcc-arm-none-eabi-4_7-2012q4\\arm-none-eabi\\lib\\libc.a"\
				   }
IncludeRootRelative=".\\..\\..\\..\\05_Deliverables\\include\\algo"
IncludeLibRelative=".\\..\\..\\..\\05_Deliverables\\lib"
CompilerInclude = ".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\c6000\\include"
CompilersInclude = {"ti_c674x":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\c6000\\include",\
				 "ti_arp32":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\arp32\\include",\
				 "ti_cortex_a8":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi/gcc-arm-none-eabi-4_7-2012q4/arm-none-eabi\\include",\
				 "ti_cortex_a15":".\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler\\gcc-arm-none-eabi/gcc-arm-none-eabi-4_7-2012q4/arm-none-eabi\\include"}

OutOption = {"ti_c674x":" --output_file=", \
				   "ti_arp32":" --output_file=",\
					"ti_cortex_a8":" -o ",\
					"ti_cortex_a15":" -o "\
				   }				 
RTERelativePathes=[".\\..\\..\\..\\01_Source_Code\\common", ".\\..\\..\\..\\01_Source_Code\\common\\rte"]
#RTERelativePathes=[]
shellrelativePath = ".\\..\\..\\..\\02_Development_Tools\\ti_tools\\xdctools\\bin"
WrapperRelativePath=".\\..\\..\\..\\01_Source_Code\\algo\\00_Custom"

SourcesRelativePath=".\\..\\..\\..\\01_Source_Code\\algo\\"

WorkspaceRelativePath=".\\..\\..\\..\\03_Workspace\\algo\\"


EveLibRelPath = ".\\..\\..\\..\\02_Development_Tools\\ti_tools\\\evestarterware\\lib\\eve1\\eve_starterware_0_1.lib"
Evelib = os.path.abspath(EveLibRelPath)

FormalName = {"vcl":"VCL","cipp":"Cipp","cb":"Cb","ecm":"Ecm","hla":"Hla","ld":"Ld","pv":"Pv","sac":"Sac","scb":"Scb","tsa_wrp":"TsaWrp","sr_wrp_a":"SrWrpPartA","sr_wrp_b":"SrWrpPartB"}
WrapperRelativePathes = []
SourcesRelativePathes = []
WorkspaceRelativePathes = []

WrappersHeaders = []
WrappersCMPs = []

AdditionalIncludeAbsPathes = {}

for target in TargetsToBuild:
	AdditionalIncludeAbsPathes[target]=[os.path.abspath(CompilersInclude[target])]

WrapperRelativePathes1 = common.getSubdirs(os.path.abspath(WrapperRelativePath))

for folder in WrapperRelativePathes1:
	x = common.getSubdirs(folder)
	WrapperRelativePathes.append(folder)
	for target in TargetsToBuild:
		if not folder in AdditionalIncludeAbsPathes[target]:
			AdditionalIncludeAbsPathes[target].append(folder)
	for y in x:
		WrapperRelativePathes.append(y)
		for target in TargetsToBuild:
			if not y in AdditionalIncludeAbsPathes[target]:
				AdditionalIncludeAbsPathes[target].append(y)
		
SourcesRelativePath1 = common.getSubdirs(os.path.abspath(SourcesRelativePath))
for folder in SourcesRelativePath1:
	x = common.getSubdirs(folder)
	if not folder in SourcesRelativePathes:
		SourcesRelativePathes.append(folder)
	for target in TargetsToBuild:
		if not folder in AdditionalIncludeAbsPathes[target]:
			AdditionalIncludeAbsPathes[target].append(folder)
	for y in x:
		if not y in SourcesRelativePathes:
			SourcesRelativePathes.append(y)
		for target in TargetsToBuild:
			if not y in AdditionalIncludeAbsPathes[target]:
				AdditionalIncludeAbsPathes[target].append(y)

WorkspaceRelativePathes1 = common.getSubdirsRecursive(os.path.abspath(WorkspaceRelativePath))
for folder in WorkspaceRelativePathes1:	
	for target in TargetsToBuild:
		if not folder in AdditionalIncludeAbsPathes[target] and "_sim" in folder and "ecm" in folder:
			AdditionalIncludeAbsPathes[target].append(folder)
			WorkspaceRelativePathes.append(folder)

SourcesRelativePath2 = common.getSubdirsRecursive(os.path.abspath(SourcesRelativePath))
for folder in SourcesRelativePath2:	
	for target in TargetsToBuild:
		if not folder in AdditionalIncludeAbsPathes[target] and ("include" in folder or "inc" in folder or "viscr" in folder):
			AdditionalIncludeAbsPathes[target].append(folder)
			SourcesRelativePathes.append(folder)

for target in TargetsToBuild:
	AdditionalIncludeAbsPathes[target] = common.ListRemoveduplication(AdditionalIncludeAbsPathes[target])
	
SourcesRelativePathes = common.ListRemoveduplication(SourcesRelativePathes)			
#print(WorkspaceRelativePathes)			
Builder = {}
Linker = {}
Archiver={}
LibC={}
for target in TargetsToBuild:
	Builder[target] = os.path.abspath(BuilderRelative[target])
	Linker[target] = os.path.abspath(LinkerRelative[target])
	LibC[target] = os.path.abspath(LibCRelative[target])
	
	


LibCRelative	
for core in TargetsToBuild:
	Archiver[core] = os.path.abspath(ArchiverRelative[core])
	


IncludePathes = {"ti_c674x":[],"ti_arp32":[],"ti_cortex_a8":[],"ti_cortex_a15":[]}
strIncludePathes=""

IncludePathes_ti_arp32 = []
strIncludePathes_ti_arp32=""

IncludePathes_ti_c674x = []
strIncludePathes_ti_c674x=""

IncludePathes_ti_cortex_a8 = []
strIncludePathes_ti_cortex_a8=""

IncludePathes_ti_cortex_a15 = []
strIncludePathes_ti_cortex_a15 =""

strIncludePathes=" "
strIncludePathes_ti_c674x=" "
strIncludePathes_ti_arp32=" "
strIncludePathes_ti_arp32=" "
strIncludePathes_ti_arp32=" "
IncludeRoot = os.path.abspath(IncludeRootRelative)

GenIncludePathes  = []

for CMP in Components:
	folder1 = IncludeRoot+"\\"+CMP
	if os.path.exists(folder1):
		for target in TargetsToBuild:
			IncludePathes[target].append(folder1)
		GenIncludePathes.append(folder1)
		strIncludePathes=strIncludePathes+ " -I"+folder1
		IncludePathes_ti_cortex_a8.append(folder1)
		strIncludePathes_ti_cortex_a8=strIncludePathes+ " -I"+folder1
		IncludePathes_ti_cortex_a15.append(folder1)
		strIncludePathes_ti_cortex_a15=strIncludePathes+ " -I"+folder1		
		IncludePathes_ti_arp32.append(folder1+"\\ti_arp32")
		strIncludePathes_ti_arp32=strIncludePathes+ " -I"+folder1+"\\ti_arp32"
		IncludePathes_ti_c674x.append(folder1+"\\ti_c674x")
		strIncludePathes_ti_c674x=strIncludePathes_ti_c674x+ " -I"+folder1+"\\ti_c674x"


#IncludePathes = common.checkExistance(IncludePathes)	
#GenIncludePathes = common.checkExistance(GenIncludePathes)	
#IncludePathes_ti_cortex_a8 = common.checkExistance(IncludePathes_ti_cortex_a8)	
#IncludePathes_ti_cortex_a15 = common.checkExistance(IncludePathes_ti_cortex_a15)	
#IncludePathes_ti_arp32 = common.checkExistance(IncludePathes_ti_arp32)
#IncludePathes_ti_c674x = common.checkExistance(IncludePathes_ti_c674x)

	
CommunicationChannel = {}

#def parsingFile(file):
def init():
	os.environ["PATH"] =  os.environ["PATH"] +";"+os.path.abspath(shellrelativePath)
	if not os.path.exists("out"):
		os.makedirs("out")
	if not os.path.exists("build"):
		os.makedirs("build")

	#if not os.path.exists("log/build.log"):
		#os.makedirs("log")				
	#sys.path.append(os.path.abspath(shellrelativePath))
	#print(os.environ["PATH"])

def GiveInfo():
	print("-*"*30)
	print(" "*20+"Components to be handled")
	print("-*"*30)
	int = 1;
	for CMP in Components:
		print(str(int)+": "+ CMP)
		int = int +1

def TestStdCmp(cmp):
	target = ""
	if "_wrp" in cmp:
		target = "ti_cortex_a8"
		cmp1 = cmp.replace("_wrp_a","")
		cmp1 = cmp1.replace("_wrp_b","")
		cmp1 = cmp1.replace("_wrp","")
	else:
		target = "ti_c674x"
	fo.write( " \n");
	fo.write( "    /* 	**********************    */  \n");
	fo.write("	{  \n")
	fo.write("	#ifdef "+target+"  \n")
	if target == "ti_c674x":
		fo.write("		#ifdef "+cmp+"  \n")
	else:
		fo.write("		#ifdef "+cmp1+"  \n")
	fo.write("			const req"+FormalName[cmp]+"PrtList_t *reqPorts;\n")
	fo.write("			pro"+FormalName[cmp]+"PrtList_t *proPorts;\n")
	fo.write("			AS_t_ServiceFuncts * pServices;\n")	
	fo.write("			"+FormalName[cmp]+"Exec(reqPorts    , proPorts, pServices);\n")	
	fo.write("		#endif  \n")
	fo.write("	#endif  \n")
	fo.write("    }  \n")
	fo.write("    /* 	**********************    */  \n");

	
def GetWrappers():
	WrapperFolders = []
	AllFolders = common.getSubdirs(WrappersAbsPath)
	for folder in AllFolders:
		x = os.path.basename(folder)
		if "_wrp" in x and not ("sac" in x or "pv" in x):
			WrapperFolders.append(folder)
	ext="*_ext.h"
	for wrapperFolder in WrapperFolders:
		temp = glob.glob(str(wrapperFolder)+'/'+ext)
		if temp:
			for file in temp:
				WrappersHeaders.append(file)
				base = os.path.basename(file)
				WrappersCMPs.append(base[:-6])
				
	#print(WrappersCMPs )
	#print(WrappersHeaders)

#####################################
#Generating main file and build it to make use the libraries 
#####################################
def GeneratingFiles():
	######################
	#Searching Header files

	ExtensionToSearch="*.h"
	Headers=[]
	Types = []
	Headers_ti_arp32=[]
	for Folder in GenIncludePathes:
		temp = glob.glob(str(Folder)+'/'+ExtensionToSearch)
		for file in temp:
			if "ARP_Interface" in file:
				Headers_ti_arp32.append(file)
			else:
					if "_ext" in file or "_interface" in file:
						Headers.append(file)
						
	for Folder in IncludePathes_ti_arp32:
		temp = glob.glob(str(Folder)+'/'+ExtensionToSearch)
		for file in temp:
			if "_ext" in file or "_Interface" in file:
				Headers_ti_arp32.append(file)
	Headers_ti_c674x=[]
	for Folder in IncludePathes_ti_c674x:
		temp = glob.glob(str(Folder)+'/'+ExtensionToSearch)
		for file in temp:
			if "_ext" in file or "_Interface" in file:
				Headers_ti_c674x.append(file)	
	for Folder in SourcesRelativePathes:
		temp = glob.glob(str(Folder)+'/'+ExtensionToSearch)
		for file in temp:
			fileName = os.path.basename(file)
			if "ARP_Interface" in file or "ARP_interface" in file:
				for x in Headers_ti_arp32:
					if fileName in x:
						break
				if x != Headers_ti_arp32[len(Headers_ti_arp32)-1]:
					Headers_ti_arp32.append(file)
			else:
				for x in Headers_ti_c674x:
					if fileName in x:
						break
				for y in Headers:
					if fileName in y:
						break
				if x == Headers_ti_c674x[len(Headers_ti_c674x)-1] and y == Headers[len(Headers)-1]:
					#if ("_ext." in file ) and (not "cp" in file ) and (not "emp" in file) and (not "sen" in file)  and (not "sac_interface.h" in file) and (not "fct" in file):
						#Headers_ti_c674x.append(file)
					if "_types." in file and "00_Custom" not in file:
						z=" "
						for z in Types:
							if fileName in z:
								break
						if z != " ":
							if z == Types[len(Types)-1]:
								Types.append(file)
						else:
							Types.append(file)
				
	Types.sort();
	Headers_ti_arp32.sort();
	Headers_ti_c674x.sort();
	#print(Types)
	strIncludeTypes = common.List2Str(Types, " -I")
	
	Headers_ti_cortex_a15=[]
	
	Headers_ti_cortex_a8=[]
	######################
	#Including RTE pathes

	for folder in RTERelativePathes:
		for target in TargetsToBuild:	
			IncludePathes[target].append(os.path.abspath(folder))
	
	for target in TargetsToBuild:
		for folder in AdditionalIncludeAbsPathes[target]:
			IncludePathes[target].append(folder)
	
	for target in TargetsToBuild:
		for folder in IncludePathes[target]:
			if not "-I"+folder in IncludeOption[target]:
				IncludeOption[target]=IncludeOption[target]+" -I"+folder
	CommunicationChannel["IncludeOption"]  = IncludeOption
	CommunicationChannel["IncludeOption_ti_cortex_a15"]  = IncludeOption["ti_cortex_a15"]
	CommunicationChannel["IncludeOption_ti_cortex_a8"]  = IncludeOption["ti_cortex_a8"]
	
	
	IncludeOption_ti_arp32=""
	for folder in IncludePathes_ti_arp32:
		IncludeOption_ti_arp32=IncludeOption_ti_arp32+" -I"+folder
	CommunicationChannel["IncludeOption_ti_arp32"]  = IncludeOption_ti_arp32
	
	IncludeOption_ti_c674x=""
	for folder in IncludePathes_ti_c674x:
		IncludeOption_ti_c674x=IncludeOption_ti_c674x+" -I"+folder
	CommunicationChannel["IncludeOption_ti_c674x"]  = IncludeOption_ti_c674x	

	IncludeOption_ti_cortex_a15=""
	IncludeOption_ti_cortex_a8=""
	######################
	##
	if Generate_Main == "ON":
		GetWrappers()
		print("-*"*30)
		print(" "*20+"Generating main.c file...")
		print("-*"*30)
		global fo
		fo = open("main.c", "wb")
		fo.write( "/* Including Tailoring header*/  \n");
		fo.write( "#include "+"\""+os.path.dirname(os.path.realpath(__file__))+"\\Tailoring.h"+"\"\n");
		fo.write( "/* Starting Wrappers Headers*/  \n");
		for file in WrappersHeaders:
			if "tsa" in file or "sr" in file:
				fo.write( "#ifdef ti_cortex_a8\n");
				fo.write( "    #include \""+file+"\"\n");
				fo.write( "#endif \n");
			else:
				fo.write( "#ifdef ti_c674x\n");
				fo.write( "    #include \""+file+"\"\n");
				fo.write( "#endif \n");		
				
		fo.write( "/* Ending Wrappers Headers*/ \n");
		for file in Headers:
			fo.write( "#include \""+file+"\"\n");
		fo.write( "#ifdef ti_arp32 \n");
		for file in Headers_ti_arp32:
			fo.write( "    #include \""+file+"\"\n");
		fo.write( "#endif\n");
		
		fo.write( "#ifdef ti_c674x \n");
		for file in Headers_ti_c674x:
			fo.write( "    #include \""+file+"\"\n");
		fo.write( "#endif\n");
		#####Writing code####
		fi = open("Callout.c", "rb")
		lines = fi.readlines()
		for line in lines:
			fo.write( line );
		fo.write( "int main(void)\n");
		fo.write( "{\n");
		fo.write( " Callout();\n");			
		for cmp in WrappersCMPs:
			TestStdCmp(cmp)
		fi.close()
		######################
		fo.write( "\n"*5);
		fo.write( "return(0);\n");
		fo.write( "}\n");
		fo.close()
		######################		
	
	
	
	

COMPILER_OPTIONS = {}
Linker_Options  = {}
strLibs = {}
COMPILER_OPTIONS["ti_c674x"]=" -c  -mv6740 --abi=eabi -O3 --define=c6747 --display_error_number --diag_warning=225 --optimizer_interlist --opt_for_speed=5 -k --gen_opt_info=1  -DNDEBUG "
COMPILER_OPTIONS["ti_arp32"]=" -o3 --program_level_compile --symdebug:skeletal -kv -kh --silicon_version=v210  --abi=eabi "
COMPILER_OPTIONS["ti_cortex_a8"]  = "  -mcpu=cortex-a8 -c  -mlittle-endian -g  -mabi=aapcs -mfpu=neon -mfloat-abi=hard  -DTSA_DEBUG_LEVEL=2 -DTSA_TARGET_ARM -DCFG_TSA_ARM_GCC -D_DEBUG -DDEBUG -DTSA_TARGET_ARM_7A15  "
COMPILER_OPTIONS["ti_cortex_a15"]  = "   -c  -mlittle-endian -g -mcpu=cortex-a15 -mabi=aapcs -mfpu=neon -mfloat-abi=hard  -DTSA_DEBUG_LEVEL=2 -DTSA_TARGET_ARM -DCFG_TSA_ARM_GCC -D_DEBUG -DDEBUG -DTSA_TARGET_ARM_7A15  "

WarningSuppress_OPTIONS = {}
Advice_OPTIONS = {}

WarningSuppress_OPTIONS["ti_c674x"]=" --no_warnings "
WarningSuppress_OPTIONS["ti_arp32"]=" --no_warnings "
WarningSuppress_OPTIONS["ti_cortex_a8"]  = " -w "
WarningSuppress_OPTIONS["ti_cortex_a15"]  =  " -w "


Advice_OPTIONS["ti_c674x"]=" --advice:performance  "
Advice_OPTIONS["ti_arp32"]="  "
Advice_OPTIONS["ti_cortex_a8"]  = "  "
Advice_OPTIONS["ti_cortex_a15"]  =  "  "

if Debug != "ON":
	for target in TargetsToBuild:
		COMPILER_OPTIONS[target] = COMPILER_OPTIONS[target] + WarningSuppress_OPTIONS[target]
else:
	for target in TargetsToBuild:
		COMPILER_OPTIONS[target] = COMPILER_OPTIONS[target] + Advice_OPTIONS[target]
		

def BuildMain():
	print("-*"*30)
	print(" "*20+"Build target obj file")
	print("-*"*30)
	DefinesCOMP={}
	
	GeneratingFiles()
	DefinesCOMP["ti_c674x"]=" --define=ti_c674x "
	DefinesCOMP["ti_arp32"]=" --define=ti_arp32 "
	DefinesCOMP["ti_cortex_a8"]=" -Dti_cortex_a8 "
	DefinesCOMP["ti_cortex_a15"]=" -Dti_cortex_a15  "
	for CMP in Components:
		DefinesCOMP["ti_c674x"] = DefinesCOMP["ti_c674x"] + " --define="+CMP
		DefinesCOMP["ti_arp32"] = DefinesCOMP["ti_arp32"] + " --define="+CMP
		DefinesCOMP["ti_cortex_a8"] = DefinesCOMP["ti_cortex_a8"] + " -D"+CMP
		DefinesCOMP["ti_cortex_a15"] = DefinesCOMP["ti_cortex_a15"] + " -D"+CMP
		
	for file in FilesToBuild:
		for target in TargetsToBuild:
			Build_Command = Builder[target] + " "+COMPILER_OPTIONS[target] +file+ " "+CommunicationChannel["IncludeOption"][target]+ " "+" " +OutOption[target]+"build/"+target+".obj " + DefinesCOMP[target]
			Logf.write(Build_Command+"\n")
			#print(Build_Command+"\n")
			proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			stdout_str, stderr_str = proc.communicate()
			#Logf.write(Build_Command+"\n")
			#Logf.write("Out: " + stdout_str+"\n")
			Logf.write("Out: \n"+stderr_str+"\n")
			#print(stderr_str+"\n")
			print("-*"*30)
			print("File: "+ file+", target: "+target+".obj to be built")
			print("-*"*30)
			if stdout_str :				
				print("Out: \n" + stdout_str+"\n")
				Logf.write("Out: \n" + stdout_str+"\n")
				
			if stderr_str:
				print("Messages: \n"+stderr_str+"\n")
				Logf.write("Messages: \n"+stderr_str+"\n")
				
		

print("-*"*30)
########################################
# Archiving all libreries 
########################################
CMPs_Target = {"ti_c674x":[],"ti_arp32":[],"ti_cortex_a15":[],"ti_cortex_a8":[]}
def ArchiveMake():
	print("-*"*30)
	print(" "*20+ '-->' +"Gathering info about Libs")
	print("-*"*30)
	for core in TargetsToBuild:
		RelMainPath = IncludeLibRelative+"\\"+core+"\\algo\\"
		MainPath = os.path.abspath(RelMainPath)
		CMPs = common.getSubdirs(MainPath)
		
		if Lib_SCAN == "ON":
			CMPs_Target[core] = CMPs
		else:
			for CMP in CMPs:
				for ConfigCMP in Components:
					if ConfigCMP in CMP:
						CMPs_Target[core].append(CMP)
		#print(CMPs)
		######################
		#Searching lib files

		ExtensionToSearch="*.lib"
		Libs={}
		Libs["ti_arp32"] = []
		Libs["ti_c674x"] = []
		Libs["ti_cortex_a8"] = []
		Libs["ti_cortex_a15"] = []
		strLibs[core]=" "
		for CMP in CMPs:
			temp = glob.glob(str(CMP)+'/'+ExtensionToSearch)
			for file in temp:			    
				Libs[core].append(file)
				strLibs[core] = strLibs[core]+" "+file+" "
		
		
		Build_Command= Archiver[core] + " -as "+core+ " " +strLibs[core]
		print("-*"*30)
		print(core+" ::"+" \n")
		print("-*"*30)
		int = 1
		for lib in Libs[core]:
			print(str(int)+ ": "+lib+" \n")
			int = int +1
					
				
		if os.path.isfile(core+".lib"):
			os.remove(core+".lib")
		
		
		#proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#stdout_str, stderr_str = proc.communicate()
		#print(stdout_str)
		#print(stderr_str)
		#Logf.write(Build_Command+"\n")
		#Logf.write(Build_Command+"\n")
		#Logf.write("Out: " + stdout_str)
		#Logf.write("ERR: "+stderr_str)
			#Adding EVE Lib
	Libs["ti_arp32"].append(Evelib)
	strLibs["ti_arp32"] = strLibs["ti_arp32"]+" "+Evelib+" "


	
def LinkProjects():
	Common_Linker_Options = " --run_linker --rom_model --reread_libs --output_file="
	Linker_Options["ti_c674x"]     = " -ms --define=c6747 "+Common_Linker_Options
	Linker_Options["ti_arp32"]     = " --run_linker  -o3 --rom_model  --map_file out/ti_arp32.map --output_file="
	Linker_Options["ti_cortex_a15"]="-nostartfiles -emain  -L.\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler/gcc-arm-none-eabi/gcc-arm-none-eabi-4_7-2012q4/arm-none-eabi/lib/fpu -L.\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler/gcc-arm-none-eabi/gcc-arm-none-eabi-4_7-2012q4/lib/gcc/arm-none-eabi/4.7.3/fpu  -o"
	Linker_Options["ti_cortex_a8"] ="-nostartfiles -emain  -L.\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler/gcc-arm-none-eabi/gcc-arm-none-eabi-4_7-2012q4/arm-none-eabi/lib/fpu -L.\\..\\..\\..\\02_Development_Tools\\ti_tools\\compiler/gcc-arm-none-eabi/gcc-arm-none-eabi-4_7-2012q4/lib/gcc/arm-none-eabi/4.7.3/fpu  -o"
	LibC["ti_cortex_a15"] =" -lgcc -lc -lm -lnosys "
	LibC["ti_cortex_a8"] =" -lgcc -lc -lm -lnosys "
	M = 15
	listx = list(range(0, M))
	listy = list(range(0, M))
	print("#"*(M*4))
	print("#"*(M*4))
	for x in listx :
		str1 = " "*x+"*"+" "*(M -x-1)+"*"+" "*(1 +x-1)+"*"+" "*(M -x-1)+"*"+" "+" "*(M -x-1)+"*"
		str2 = " "*(M -x-1)+"*"+" "*x+"*"+" "*(M -x-1)+"*"+" "*x+"*"+" "*(1*x)+"*"
		#str1 = " "*x+"*"+" "*(M -x-1)+"*"+" "*(1 +x-1)+"*"+" "*(1*x)+"*"+" "*(M -x-1)+"*"+" "*(1 +x-1)+"*"
		#str2 = " "*(M -x-1)+"*"+" "*x+"*"+" "*(M -x-1)+"*"+" "*(1 +x-1)+"*"+" "*(1*x)+"*"
		print(common.ORStr(str1, str2))
	print("#"*(M*4))
	print("#"*(M*4))
		
	for target in TargetsToBuild:
		Build_Command = Linker[target] + " "+Linker_Options[target] +"./out/"+target+ ".out "+"./build/"+target+".obj " +" "+strLibs[target]+" "+strWrappers_Obj[target] + " "+LibC[target]
		print("-*"*30)
		Logf.write(Build_Command+"\n")
		print("Linking: ( "+ target+".obj + "+ target+".lib )"+"-->   "+target+".out ")
		print("-*"*30)
		proc=subprocess.Popen(Build_Command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout_str, stderr_str = proc.communicate()
		if stdout_str :				
			print("Out: \n" + stdout_str+"\n")
		if stderr_str:
			print("Messages: \n"+stderr_str+"\n")
		else:
			print("Succeded !!!"+"\n")
		Logf.write("-*"*30+"\n")
		
WrappersAbsPath = os.path.abspath(WrapperRelativePath)	
Wrappers_Obj_ti_c674x = []
Wrappers_Obj_ti_arp32 = []
Wrappers_Obj_ti_cortex_a15 = []
Wrappers_Obj_ti_cortex_a8 = []

Wrappers_Obj = {"ti_c674x":Wrappers_Obj_ti_c674x,"ti_arp32":Wrappers_Obj_ti_arp32,"ti_cortex_a15":Wrappers_Obj_ti_cortex_a15,"ti_cortex_a8":Wrappers_Obj_ti_cortex_a8}

strWrappers_Obj = {"ti_c674x":" ","ti_arp32":" ","ti_cortex_a15":" ","ti_cortex_a8":" "}
Wrps_Target = {"ti_c674x":[],"ti_arp32":[],"ti_cortex_a15":[],"ti_cortex_a8":[]}

Wrps_INCLUDE_Target = {"ti_c674x":" ","ti_arp32":" ","ti_cortex_a15":" ","ti_cortex_a8":" "}

Srcs_Target = {"ti_c674x":[],"ti_arp32":[],"ti_cortex_a15":[],"ti_cortex_a8":[]}

Srcs_INCLUDE_Target = {"ti_c674x":" ","ti_arp32":" ","ti_cortex_a15":" ","ti_cortex_a8":" "}


def BuildFolder_Wrp(absPathList):
	#1:Getting list of all wrapper folders
	for absPath in absPathList:
		AllFolders = common.getSubdirs(absPath)
		WrapperFolders = []
		RTE_INCLUDE = " "
		for path in RTERelativePathes:
			RTE_INCLUDE = RTE_INCLUDE+" -I"+os.path.abspath(path)
			
		SRC_INCLUDE=""
		for path in SourcesRelativePathes:
			SRC_INCLUDE =SRC_INCLUDE +  " -I" +os.path.abspath(path)+" "
		
		WorkspaceRelativePathes1 = common.ListRemoveduplication(WorkspaceRelativePathes)
		WS_INCLUDE =  common.List2Str(WorkspaceRelativePathes1, " -I")
		
		for folder in AllFolders:
			x = os.path.basename(folder)
			if "_wrp" in x and not ("pv" in x or "arp" in x):
				WrapperFolders.append(folder)
		#print(WrapperFolders)
		for folder in WrapperFolders:
			x = os.path.basename(folder)
			for core in TargetsToBuild:
				for CMP in CMPs_Target[core]:
					if os.path.basename(CMP) in x:
						Wrps_Target[core].append(folder)
						Wrps_INCLUDE_Target[core] = Wrps_INCLUDE_Target[core] + " -I"+folder
						continue
		#print(CMPs_Target)	
		#print(Wrps_Target)
		
		#2:Getting list of C files to include in the wrapper Library
		ExtensionToSearch=["*.c", "*.cpp"]
		
		#3:Build each wrapper for each core --> 4 libs per Wrapper
		for core in TargetsToBuild:
			if core == "ti_c674x" or core == "ti_cortex_a8":
				for wrapperFolder in Wrps_Target[core]:
					for ext in ExtensionToSearch:
						temp = glob.glob(str(wrapperFolder)+'/'+ext)
						strCFiles = " "
						for y in temp:
							
							strCFiles = strCFiles +"   "+y
							Build_Command= Builder[core]+"  "+COMPILER_OPTIONS[core]+y +"  "+OutOption[core]+"build/"+os.path.basename(os.path.splitext(y)[0])+"_"+core+".obj "+" -I"+os.path.abspath(CompilersInclude[core])+RTE_INCLUDE +strIncludePathes+" "+strIncludePathes_ti_c674x+" "+strIncludePathes_ti_arp32+" "+Wrps_INCLUDE_Target[core] +SRC_INCLUDE + WS_INCLUDE
							Wrappers_Obj[core].append(os.path.dirname(os.path.realpath(__file__))+"/"+os.path.splitext(y)[0]+"_"+core+".obj")
							strWrappers_Obj[core] = strWrappers_Obj[core] +" "+os.path.dirname(os.path.realpath(__file__))+"/build/"+os.path.basename(os.path.splitext(y)[0])+"_"+core+".obj"
							print("-*"*30)
							print(core+" :: Build  "+y+" \n")
							print("-*"*30)
							Logf.write(Build_Command+"\n")
							proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
							stdout_str, stderr_str = proc.communicate()
							print(stdout_str+" \n")
							print(stderr_str+" \n")
							Logf.write(stdout_str+" \n")
							Logf.write(stderr_str+" \n")

def BuildFolder(absPathList):
	#1:Getting list of all wrapper folders
	for absPath in absPathList:
		AllFolders = common.getSubdirs(absPath)
		AllFolders.append(absPath)
		WrapperFolders = []
		RTE_INCLUDE = " "
		for path in RTERelativePathes:
			RTE_INCLUDE = RTE_INCLUDE+" -I"+os.path.abspath(path)
			
		SRC_INCLUDE=""
		for path in SourcesRelativePathes:
			SRC_INCLUDE =SRC_INCLUDE +  " -I" +os.path.abspath(path)+" "
			
		for folder in AllFolders:
			x = os.path.basename(folder)
			WrapperFolders.append(folder)
		#print(WrapperFolders)
		for folder in WrapperFolders:
			x = os.path.basename(folder)
			for core in TargetsToBuild:
				Wrps_Target[core].append(folder)
				Wrps_INCLUDE_Target[core] = Wrps_INCLUDE_Target[core] + " -I"+folder
					#continue
		#print(CMPs_Target)	
		#print(Wrps_Target)
		
		#2:Getting list of C files to include in the wrapper Library
		ExtensionToSearch=["*.c", "*.cpp"]
		
		#3:Build each wrapper for each core --> 4 libs per Wrapper
		for core in TargetsToBuild:
			if core == "ti_c674x":
				for wrapperFolder in Wrps_Target[core]:
					#print(Wrps_Target[core])
					for ext in ExtensionToSearch:
						temp = glob.glob(str(wrapperFolder)+'/'+ext)
						strCFiles = " "
						#print(temp)
						for y in temp:
							
							strCFiles = strCFiles +"   "+y
							Build_Command= Builder[core]+"  "+COMPILER_OPTIONS[core]+y +"  "+OutOption[core]+"build/"+os.path.basename(os.path.splitext(y)[0])+"_"+core+".obj "+" -I"+os.path.abspath(CompilersInclude[core])+RTE_INCLUDE +strIncludePathes+" "+strIncludePathes_ti_c674x+" "+strIncludePathes_ti_arp32+" "+Wrps_INCLUDE_Target[core] +SRC_INCLUDE
							Wrappers_Obj[core].append(os.path.dirname(os.path.realpath(__file__))+"/"+os.path.splitext(y)[0]+"_"+core+".obj")
							strWrappers_Obj[core] = strWrappers_Obj[core] +" "+os.path.dirname(os.path.realpath(__file__))+"/build/"+os.path.basename(os.path.splitext(y)[0])+"_"+core+".obj"
							print("-*"*30)
							print(core+" :: Build  "+y+" \n")
							print("-*"*30)
							Logf.write(Build_Command+"\n")
							proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
							stdout_str, stderr_str = proc.communicate()
							print(stdout_str+" \n")
							print(stderr_str+" \n")
							Logf.write(stdout_str+" \n")
							Logf.write(stderr_str+" \n")

							
RelAuxBuild = [".\\..\\..\\..\\03_Workspace\\algo\\ecm_sim\\sim_swc_ecm\\roi\\"]
AuxBuid = []
for Aux in RelAuxBuild:
	AuxBuid.append(os.path.abspath(Aux))
def BuildAux():
	BuildFolder(AuxBuid)
	#print (AuxBuid)			

def BuildWrappers():	
	BuildFolder_Wrp([WrappersAbsPath])
#def ScanTargetCMP():
	
def PostRun():
	exts = ["*.asm", "*.nfo"]
	for ext in exts:
		files = glob.iglob(os.path.join(".", ext))
		for file in files:
			if os.path.isfile(file):
				shutil.move(file, "./build")
	
	
def main():
	init()
	GiveInfo()
	ArchiveMake()
	if Compile_Main == "ON":
		BuildMain()
	else:
		print("-->"*20)
		print("main.c file will not rebuilt, old build will be considered !!! ")
		print("<--"*20+ "\n")
	if Compile_Wrappers == "ON":
		BuildWrappers()
	else:
		print("-->"*20)
		print("Wrappers files will not rebuilt, old build will be considered !!! ")
		print("<--"*20+ "\n")
	if Compile_Aux == "ON":
		BuildAux()
	
	if LINK == "ON":
		LinkProjects()
	else:
		print("-->"*20)
		print("No Linking operation, check your configuration !!! ")
		print("<--"*20+ "\n")
	PostRun()
 
def premain():
	if not os.path.exists("log"):
		os.makedirs("log")
	global  Logf 
	Logf = open("./log/Build.log", "wb+")

def postmain():
	Logf.close()

def test():
	x = common.getSubdirsRecursive("D:\\Sandboxs\\SMFC4B0_05.01.00\\06_Algorithm\\04_Engineering\\03_Workspace\\algo")
	#print x
	print(len(x))

#test()	
premain()
main()
postmain()

#cl6x --run_linker f1.obj f2.obj liba.lib libc.lib