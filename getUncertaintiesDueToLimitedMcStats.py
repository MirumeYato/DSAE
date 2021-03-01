# to run this on lxplus from a clean shell:		setupATLAS; lsetup "root 6.14.04-x86_64-slc6-gcc62-opt"; python getUncertaintiesDueToLimitedMcStats.py

import ROOT
fileNames = [
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-16_16h31m17s939530110ns_M500_Z2_/fetch/hist-m0500z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-16_16h31m26s966385408ns_M800_Z2_/fetch/hist-m0800z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-16_16h31m31s626518936ns_M1100_Z2_/fetch/hist-m1100z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-16_16h31m37s031660369ns_M1400_Z2_/fetch/hist-m1400z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-16_16h31m42s012151328ns_M1700_Z2_/fetch/hist-m1700z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2021-February-16_16h31m47s176702109ns_M2000_Z2_/fetch/hist-m2000z2-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m06s747989595ns_M500_Z3_/fetch/hist-m0500z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m10s319790681ns_M800_Z3_/fetch/hist-m0800z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m13s714940456ns_M1100_Z3_/fetch/hist-m1100z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m17s432175061ns_M1400_Z3_/fetch/hist-m1400z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m20s777200468ns_M1700_Z3_/fetch/hist-m1700z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m24s071676901ns_M2000_Z3_/fetch/hist-m2000z3-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m27s583026256ns_M500_Z4_/fetch/hist-m0500z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m31s110745399ns_M800_Z4_/fetch/hist-m0800z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m34s942543053ns_M1100_Z4_/fetch/hist-m1100z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h02m57s111688451ns_M1400_Z4_/fetch/hist-m1400z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m00s677086904ns_M1700_Z4_/fetch/hist-m1700z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m03s873056264ns_M2000_Z4_/fetch/hist-m2000z4-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m07s548402298ns_M500_Z5_/fetch/hist-m0500z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m10s702849239ns_M800_Z5_/fetch/hist-m0800z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m13s994157562ns_M1100_Z5_/fetch/hist-m1100z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m17s218368563ns_M1400_Z5_/fetch/hist-m1400z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m20s858934928ns_M1700_Z5_/fetch/hist-m1700z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m24s438583365ns_M2000_Z5_/fetch/hist-m2000z5-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m28s251101029ns_M500_Z6_/fetch/hist-m0500z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m32s619321986ns_M800_Z6_/fetch/hist-m0800z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m35s808508832ns_M1100_Z6_/fetch/hist-m1100z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m39s047131703ns_M1400_Z6_/fetch/hist-m1400z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m42s414959312ns_M1700_Z6_/fetch/hist-m1700z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m45s841605695ns_M2000_Z6_/fetch/hist-m2000z6-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m49s601055152ns_M500_Z7_/fetch/hist-m0500z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m53s511094427ns_M800_Z7_/fetch/hist-m0800z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h03m57s747580983ns_M1100_Z7_/fetch/hist-m1100z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h04m02s509802576ns_M1400_Z7_/fetch/hist-m1400z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h04m06s973009802ns_M1700_Z7_/fetch/hist-m1700z7-0.root',
'/afs/cern.ch/user/y/ysmirnov/public/data2015_2018_analysis/ROOTAnalysisTutorial/run/submitDir_2020-October-09_15h04m10s320824976ns_M2000_Z7_/fetch/hist-m2000z7-0.root'
] # these files result from the processing of unskimmed DxAODs
for fileName in fileNames:
	f = ROOT.TFile.Open(fileName)
	if not f or f.IsZombie():
#		print 'Error: unable to open file \'', fileName, '\', check path+name!'
		exit(1)
	h_cutflow = f.Get("h_cutflow")
	if not h_cutflow:
		print 'Error: unable to find the histogram you requested inside the \'', fileName, '\' - check file content and/or histogram name!'
		exit(1)

# histogram for the numerator of the TEfficiency object
	h_SoWOfEventsAfterFinalSelection = ROOT.TH1D("h_SoWOfEventsAfterFinalSelection", ";Bin;Sum of weights of events after final selection", 1, 0, 1)
	h_SoWOfEventsAfterFinalSelection.SetBinContent(1, h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(45)))
	h_SoWOfEventsAfterFinalSelection.SetBinError(1, h_cutflow.GetBinError(h_cutflow.GetXaxis().FindFixBin(45)))

# histogram for the denominator of the TEfficiency object
	h_SoWOfEventsInXaods = ROOT.TH1D("h_SoWOfEventsInXaods", ";Bin;Sum of weights of all events in xAODs", 1, 0, 1)
	h_SoWOfEventsInXaods.SetBinContent(1, h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(2)))
	absoluteUncertaintyOnNEventsInXaods = ROOT.TMath.Sqrt(h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(1))) # because the regular uncertainty on the content of this bin is busted (the content of this bin is changed once we move to another file, not just to another event), so we have to recalculate it
	relativeUncertaintyOnNEventsInXaods = absoluteUncertaintyOnNEventsInXaods/h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(1))
	h_SoWOfEventsInXaods.SetBinError(1, relativeUncertaintyOnNEventsInXaods*h_cutflow.GetBinContent(h_cutflow.GetXaxis().FindFixBin(2)))

# TEfficiency object
	e_finalSelection = ROOT.TEfficiency(h_SoWOfEventsAfterFinalSelection, h_SoWOfEventsInXaods)
	e_finalSelection.SetStatisticOption(ROOT.TEfficiency.kFNormal) # to suppress a warning from ROOT
	print 'Uncertainty is', e_finalSelection.GetEfficiencyErrorLow(1)/e_finalSelection.GetEfficiency(1)*100, '%'

	f.Close()
print 'Bye!'
exit(0)
