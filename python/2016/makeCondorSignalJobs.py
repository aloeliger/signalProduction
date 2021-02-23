#!/usr/bin/env python
#To use the this Job making script, run it as follows in the CMSSW_10_6_20/src/signalProductionWorkspace/python/2016 area:
#In general: python makecondorSignalJobs.py <path of CMSSW_10_6_20_src> <path of CMSSW_8_0_33_UL_src> <path to store NanoAOD files> -n <number of Jobs to be created>
#For example: python makecondorSignalJobs.py /afs/cern.ch/user/g/gparida/public/bbtautauAnalysis/CMSSW_10_6_20/src /afs/cern.ch/user/g/gparida/public/bbtautauAnalysis/CMSSW_8_0_33_UL/src /afs/cern.ch/user/g/gparida/public/bbtautauAnalysis/CMSSW_10_6_20/src/signalProductionWorkspace/python/2016/Output_Files -n 8
#Next step is to submit Jobs created by doing: ./ submit_all.jobb

import os, sys,  imp, re, pprint, string
from optparse import OptionParser

# cms specific
import FWCore.ParameterSet.Config as cms

import time
import datetime
import os
import sys

MYDIR=os.getcwd()
from optparse import OptionParser
parser=OptionParser()
parser.add_option("-n",dest="NJobs",type="int",default=1,help="Total number of Jobs",metavar="NUMBER")

opts, args = parser.parse_args()

cmsEnv1 = str(args[0])
cmsEnv2 = str(args[1])
remoteDir = str(args[2])

print 'CMSSWrel1 = %s'%cmsEnv1
print 'CMSSWrel2 = %s'%cmsEnv2
print 'remote directory = %s'%remoteDir



#make directories for the jobs
jobDir2 = cmsEnv2+'/signalProductionWorkspace/python/2016/Jobs'
try:
    os.system('rm -rf Jobs')
    os.system('mkdir Jobs')
    os.system('rm -rf %s'%(jobDir2))
    os.system('mkdir %s'%(jobDir2))
except:
    print "err!"
    pass

nJobs = opts.NJobs
print "number of jobs to be created: ", nJobs
    
#make job scripts
for i in range(0, nJobs):
    jobDir = MYDIR+'/Jobs/Job_%s/'%str(i)
    jobDir3 = cmsEnv2+'/signalProductionWorkspace/python/2016/Jobs/Job_%s/'%str(i)
    os.system('mkdir %s'%jobDir)
    os.system('mkdir %s'%jobDir3)

    tmp_jobname="sub_%s.sh"%(str(i))
    tmp_job=open(jobDir+tmp_jobname,'w')
    tmp_job.write("#!/bin/sh\n")
    tmp_job.write("ulimit -S\n")
    tmp_job.write("cd $TMPDIR\n")
    tmp_job.write("mkdir Job_%s\n"%str(i))
    tmp_job.write("cd Job_%s\n"%str(i))
    tmp_job.write("cd %s\n"%(cmsEnv1))
    tmp_job.write("eval `scramv1 runtime -sh`\n")
    tmp_job.write("cd -\n")
    tmp_job.write("cp -f %s* .\n"%(jobDir))
    tmp_job.write("cmsRun LHEGENSIMStep.py\n")
    tmp_job.write("cmsRun DIGIPREMIXStep.py\n")
    tmp_job.write("cd ../\n")
    tmp_job.write("mkdir Job_%s_HLT\n"%str(i))
    tmp_job.write("cd Job_%s_HLT\n"%str(i))
    tmp_job.write("cd %s\n"%(cmsEnv2))
    tmp_job.write("eval `scramv1 runtime -sh`\n")
    tmp_job.write("cd -\n")
    tmp_job.write("cp -f %s* .\n"%(jobDir3))
    tmp_job.write("mv ../Job_%s/step1_RAW.root .\n"%str(i))
    tmp_job.write("cmsRun HLT_CMSSW_8_0_33_ULStep.py\n")
    tmp_job.write("mv step1_DIGI2RAW.root ../Job_%s/.\n"%str(i))
    tmp_job.write("cd ../Job_%s/\n"%str(i))
    tmp_job.write("cd %s\n"%(cmsEnv1))
    tmp_job.write("eval `scramv1 runtime -sh`\n")
    tmp_job.write("cd -\n")
    tmp_job.write("cmsRun RECOStep.py\n")
    tmp_job.write("cmsRun MINIAODStep.py\n")
    tmp_job.write("cd %s\n"%(cmsEnv1))
    tmp_job.write("eval `scramv1 runtime -sh`\n")
    tmp_job.write("cd -\n")
    tmp_job.write("cmsRun NANOStep.py\n")
    tmp_job.write("echo 'sending the file back'\n")
    tmp_job.write("cp finalNanoAOD.root %s/NanoAOD_%s.root\n"%(remoteDir, str(i)))
    tmp_job.write("rm step1_DIGI2RAW.root\n")
    tmp_job.write("rm ../Job_%s_HLT/step1_RAW.root\n"%str(i))
    tmp_job.write("rm step1_SIM.root\n")
    tmp_job.write("rm step1_LHE.root\n")
    tmp_job.write("rm step1_AODSIM.root\n")
    tmp_job.write("rm step1_MiniAOD.root\n")
    tmp_job.write("rm finalNanoAOD.root\n")
    tmp_job.close()
    os.system('chmod +x %s'%(jobDir+tmp_jobname)) 
    os.system('cp LHEGENSIMStep.py %s.'%jobDir)
    os.system('cp DIGIPREMIXStep.py %s.'%jobDir)
    os.system('cp HLT_CMSSW_8_0_33_ULStep.py %s.'%jobDir3)
    os.system('cp RECOStep.py %s.'%jobDir)
    os.system('cp MINIAODStep.py %s.'%jobDir)
    os.system('cp NANOStep.py %s.'%jobDir)

sub_total = open("submit_all.jobb","w")
condor_str = "executable = $(filename)\n"
condor_str += "arguments = $Fp(filename) $(ClusterID) $(ProcId)\n"
condor_str += "output = $Fp(filename)hlt.stdout\n"
condor_str += "error = $Fp(filename)hlt.stderr\n"
condor_str += "log = $Fp(filename)hlt.log\n"
condor_str += '+JobFlavour = "tomorrow"\n'
condor_str += "GetEnv = True\n"
condor_str += "queue filename matching ("+MYDIR+"/Jobs/Job_*/*.sh)"
condor_name = MYDIR+"/condor_cluster.sub"
condor_file = open(condor_name, "w")
condor_file.write(condor_str)
sub_total.write("condor_submit %s\n"%condor_name)
os.system("chmod +x submit_all.jobb")