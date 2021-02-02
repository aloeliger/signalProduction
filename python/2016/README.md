# 2016 Production chain

## Order of Steps

  1 LHEGENSIM
  2 DIGIPREMIX
  3 HLT
  4 RECO
  5 MINIAOD
  6 NANO

## Bare cmsDriver Comands

  1 Configuration/GenProduction/fragment.py --fileout file:B2G-RunIISummer20UL16wmLHEGEN-00605.root --mc --eventcontent RAWSIM,LHE --datatier GEN,LHE --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2016 -n 1000
  2 step1 --fileout file:B2G-RunIISummer20UL16DIGIPremix-00449.root --pileup_input dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_mcRun2_asymptotic_v13 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2016 -n 1000