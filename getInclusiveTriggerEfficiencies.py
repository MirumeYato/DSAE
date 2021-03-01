# to run this on lxplus from a clean shell:		setupATLAS; lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"; python getUncertaintiesDueToLimitedMcStats.py

import ROOT
fileNames = [
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h13m19s079755604ns_M500_Z2_/fetch/hist-m0500z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h13m29s216270432ns_M800_Z2_/fetch/hist-m0800z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h13m41s830553885ns_M1100_Z2_/fetch/hist-m1100z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h13m46s121776301ns_M1400_Z2_/fetch/hist-m1400z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h13m59s203558056ns_M1700_Z2_/fetch/hist-m1700z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h14m09s554724899ns_M2000_Z2_/fetch/hist-m2000z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h14m20s512259422ns_M500_Z3_/fetch/hist-m0500z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h14m32s719816442ns_M800_Z3_/fetch/hist-m0800z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h14m44s989654364ns_M1100_Z3_/fetch/hist-m1100z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h14m57s366622056ns_M1400_Z3_/fetch/hist-m1400z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h15m09s805766737ns_M1700_Z3_/fetch/hist-m1700z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h15m13s712022644ns_M2000_Z3_/fetch/hist-m2000z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h15m26s936305966ns_M500_Z4_/fetch/hist-m0500z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h15m37s576620778ns_M800_Z4_/fetch/hist-m0800z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h15m49s657580600ns_M1100_Z4_/fetch/hist-m1100z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h15m59s889004503ns_M1400_Z4_/fetch/hist-m1400z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h16m14s348790120ns_M1700_Z4_/fetch/hist-m1700z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h16m25s996012027ns_M2000_Z4_/fetch/hist-m2000z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h16m38s843563683ns_M500_Z5_/fetch/hist-m0500z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h16m52s693377414ns_M800_Z5_/fetch/hist-m0800z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h17m04s233792049ns_M1100_Z5_/fetch/hist-m1100z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h17m08s607175957ns_M1400_Z5_/fetch/hist-m1400z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h17m19s098458758ns_M1700_Z5_/fetch/hist-m1700z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h17m33s741479050ns_M2000_Z5_/fetch/hist-m2000z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h17m45s188031205ns_M500_Z6_/fetch/hist-m0500z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h17m55s797137324ns_M800_Z6_/fetch/hist-m0800z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h18m05s262082727ns_M1100_Z6_/fetch/hist-m1100z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h18m16s321483410ns_M1400_Z6_/fetch/hist-m1400z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h18m20s121508503ns_M1700_Z6_/fetch/hist-m1700z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h18m31s968871456ns_M2000_Z6_/fetch/hist-m2000z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h18m50s065155328ns_M500_Z7_/fetch/hist-m0500z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h19m01s401491146ns_M800_Z7_/fetch/hist-m0800z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h19m12s342409424ns_M1100_Z7_/fetch/hist-m1100z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h19m23s254933210ns_M1400_Z7_/fetch/hist-m1400z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h19m33s507021843ns_M1700_Z7_/fetch/hist-m1700z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-03_15h19m37s770394737ns_M2000_Z7_/fetch/hist-m2000z7-0.root'
]


print 'Inclusive trigger-selection efficiencies [%]:\n single-muon trigger\t| MET trigger\t\t| late-muon trigger'


for fileName in fileNames:
	f = ROOT.TFile.Open(fileName)
	if not f or f.IsZombie():
		exit(1)
	h_cutflow = f.Get("h_cutflow")
	if not h_cutflow:
		print 'Error: unable to find the histogram you requested inside the \'', fileName, '\' - check file content and/or histogram name!'
		exit(1)

	print h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("#Sigma muon-trigger SFs (MC only)")) / h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with 1 primary vertex")) * 100, '\t\t|', h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with MET trigger fired")) / h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with 1 primary vertex")) * 100, '\t|', h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with late-muon trigger fired")) / h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin("... with 1 primary vertex")) * 100
	f.Close()
print 'Bye!'
exit(0)
