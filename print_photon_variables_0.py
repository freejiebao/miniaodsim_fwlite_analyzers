import ROOT
import sys
from DataFormats.FWLite import Events, Handle

events = Events (['root://cms-xrd-global.cern.ch//store/data/Run2016H/SingleElectron/MINIAOD/03Feb2017_ver3-v1/110000/02973E99-69EC-E611-9913-5065F381A2F1.root'])

photons, photonLabel = Handle("std::vector<pat::Photon>"), "slimmedPhotons"


for event in events:

    #if event.eventAuxiliary().luminosityBlock() != 209529:
    #    continue

    if event.eventAuxiliary().event() != 559392951:
        continue

    print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    event.getByLabel(photonLabel,photons)
    
    for pho in photons.product():
        print pho.pt()
        print pho.eta()
        print pho.superCluster().eta()
        print pho.hadronicOverEm()
        print pho.hadTowOverEm()
        print pho.full5x5_sigmaIetaIeta()
        print pho.userFloat('phoChargedIsolation')
        print pho.userFloat('phoNeutralHadronIsolation')
        print pho.userFloat('phoPhotonIsolation')
        
