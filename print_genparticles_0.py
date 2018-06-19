import ROOT
import sys
from DataFormats.FWLite import Events, Handle

events = Events (['root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/041216AA-43C1-E611-AEC4-0CC47A4D7662.root '])

handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")

# loop over events
count= 0

for event in events:

    #if event.eventAuxiliary().luminosityBlock() != 209529:
    #    continue

    if event.eventAuxiliary().event() != 47397533:
        continue

    #it is explained in https://sft.its.cern.ch/jira/browse/ROOT-5041 why there is a "[?1034h" at the beginning of the output when it is piped into a file
    print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    
    print "\npacked\n"	    

    event.getByLabel (labelPacked, handlePacked)

    packed = handlePacked.product()

    for p in packed :

	if p.mother(0) and p.mother(0).pdgId():
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s  mother_pdg_id : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mother(0).pdgId())    
        else:
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())    	    	

        print p.statusFlags().isLastCopyBeforeFSR()
        print p.statusFlags().isLastCopy()
        print p.statusFlags().isFirstCopy()
        print p.statusFlags().fromHardProcessBeforeFSR()
        print p.statusFlags().isDirectHardProcessTauDecayProduct()
        print p.statusFlags().isHardProcessTauDecayProduct()
        print p.statusFlags().fromHardProcess()
        print p.statusFlags().isHardProcess()
        print p.statusFlags().isDirectHadronDecayProduct()
        print p.statusFlags().isDirectPromptTauDecayProduct()
        print p.statusFlags().isDirectTauDecayProduct()
        print p.statusFlags().isPromptTauDecayProduct()
        print p.statusFlags().isTauDecayProduct()
        print p.statusFlags().isDecayedLeptonHadron()
        print p.statusFlags().isPrompt()

    event.getByLabel (labelPruned, handlePruned)

    pruned = handlePruned.product()

    print "\npruned\n"
    
    for p in pruned :

	if p.mother() and p.mother().pdgId():
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s  mother_pdg_id : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mother().pdgId())    
        else:
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())

        print p.statusFlags().isLastCopyBeforeFSR()
        print p.statusFlags().isLastCopy()
        print p.statusFlags().isFirstCopy()
        print p.statusFlags().fromHardProcessBeforeFSR()
        print p.statusFlags().isDirectHardProcessTauDecayProduct()
        print p.statusFlags().isHardProcessTauDecayProduct()
        print p.statusFlags().fromHardProcess()
        print p.statusFlags().isHardProcess()
        print p.statusFlags().isDirectHadronDecayProduct()
        print p.statusFlags().isDirectPromptTauDecayProduct()
        print p.statusFlags().isDirectTauDecayProduct()
        print p.statusFlags().isPromptTauDecayProduct()
        print p.statusFlags().isTauDecayProduct()
        print p.statusFlags().isDecayedLeptonHadron()
        print p.statusFlags().isPrompt()

