# to run this on lxplus from a clean shell:		setupATLAS; lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"; python getUncertaintiesDueToLimitedMcStats.py

import ROOT
fileNames = [
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-27_14h21m13s244412133ns_M1100_Z2_/fetch/hist-m0500z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-27_14h20m34s090468939ns_M500_Z2_/fetch/hist-m0800z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-27_14h24m32s752428517ns_M1100_Z4_/fetch/hist-m1100z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-27_14h24m08s181783483ns_M1700_Z3_/fetch/hist-m1400z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-27_14h26m17s326591283ns_M800_Z6_/fetch/hist-m1700z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-27_14h24m55s022739884ns_M2000_Z4_/fetch/hist-m2000z2-0.root'
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
