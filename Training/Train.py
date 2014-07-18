import os
import shlex, subprocess
import sys, getopt
import logging
import glob
from os.path import basename , dirname
#import CppHeaderParser
import shutil


opencvPath="D:/opencv/opencv/"

Trainer = opencvPath+"build/x86/vc10/bin/opencv_traincascade.exe "
PrepairSamples = opencvPath+"build/x86/vc10/bin/opencv_createsamples.exe "

Rel_NegFolde="In/Neg"
NegFolde=os.path.abspath(Rel_NegFolde)

Rel_PosFolde="In/Pos"
PosFolde=os.path.abspath(Rel_PosFolde)

Out_Dir="Out"
vec_file_name=Out_Dir+"/vec.vec "
bg_file_name=Out_Dir+"/Neg.txt "

Sample_Width="640"
Sample_Hight="480"

featureType = " HAAR " 
def buildCommand(Build_Command):
	proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout_str, stderr_str = proc.communicate()
	return stdout_str, stderr_str 

def filesInFolder(folder, ext):
	return (glob.glob(folder+'/'+ext))
	

def CreatNeg():
	samples=filesInFolder(NegFolde,"*.jpg")
	global Neg_length ;
	Neg_length = len(samples)
	fo = open(bg_file_name, "wb")
	for file in samples:
		fo.write( file+"\n");
		
	fo.close()
	
	
def CreatPos_ONE_SAMPLE_Destortion():
	samples=filesInFolder(PosFolde,"*.jpg")
	global Pos_length ;
	Pos_length = len(samples)
	SaOpt = " "
	for file in samples:
		SaOpt = SaOpt +" -img "+file
		
	Options = " -vec "+vec_file_name +SaOpt+" -num "+str(Pos_length)+ " -maxxangle 3 "+ " -maxyangle 3 "+ " -maxzangle 3 "+ " -w "+Sample_Width+"  -h "+Sample_Hight+ " -show"
	Command = PrepairSamples + Options
	print(Command)
	stdout_str, stderr_str = buildCommand(Command)
	print(stdout_str)
	print(stderr_str)


def Train():
	OPt=" -data "+Out_Dir+" -vec "+vec_file_name +" -bg  "+bg_file_name+" -numPos "+str(Pos_length)+" -numNeg "+str(Neg_length)+"  -stageType BOOST " + " -featureType "+featureType + " -w "+Sample_Width+"  -h "+Sample_Hight
	
	Command = Trainer+" "+OPt
	print(Command)
	stdout_str, stderr_str = buildCommand(Command)
	print(stdout_str)
	print(stderr_str)
	
def main():
	CreatNeg()
	CreatPos()
	Train()
	
	
	
	
main()
	