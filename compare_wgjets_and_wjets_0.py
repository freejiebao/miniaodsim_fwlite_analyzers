import ROOT
import sys
from DataFormats.FWLite import Events, Handle

from math import hypot, pi

def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects                                                                                                                                             
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    ## Otherwise                                                                                                                                                                          
    dphi = (phi1-phi2)
    while dphi >  pi: dphi -= 2*pi
    while dphi < -pi: dphi += 2*pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects                                                                                                                                                       
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise                                                                                                                                                                          
    return hypot(eta1-eta2, deltaPhi(phi1,phi2))

events_wgjets = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/FC332430-9C04-E811-8B94-008CFA1983BC.root'])

events_wjets = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F8C80D7B-27BF-E611-BB22-0CC47A706E5E.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F6DC29EB-69C0-E611-9C9E-441EA171A998.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F69C3309-1FBF-E611-A4B2-0CC47A706F42.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F4A2B746-0EBF-E611-8F12-0CC47A7E6A74.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F45D302F-EDBE-E611-A736-002590FD0F3E.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F2E0543D-6AC0-E611-A409-70106F4D23EC.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F0759D99-1ABF-E611-AB0D-0CC47AC08B24.root'])

xs_wjets = 60430.0
xs_wgjets = 178.6

geninfo,geninfoLabel = Handle("GenEventInfoProduct"), "generator"
handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")

# loop over events
count= 0
countweighted = 0

th1f_wgjets_njets = ROOT.TH1F("wgjets njets","",7,-0.5,6.5)
th1f_wjets_njets = ROOT.TH1F("wjets njets","",7,-0.5,6.5)

th1f_wgjets_photon_pt = ROOT.TH1F("wgjets photon pt","",10,25,125)
th1f_wjets_photon_pt = ROOT.TH1F("wjets photon pt","",10,25,125)

th1f_wgjets_lepton_pt = ROOT.TH1F("wgjets lepton pt","",10,25,125)
th1f_wjets_lepton_pt = ROOT.TH1F("wjets lepton pt","",10,25,125)

th1f_wgjets_delta_r = ROOT.TH1F("wgjets delta r","",35,0,3.5)
th1f_wjets_delta_r = ROOT.TH1F("wjets delta r","",35,0,3.5)

th1f_wgjets_njets.Sumw2()
th1f_wjets_njets.Sumw2()

th1f_wgjets_photon_pt.Sumw2()
th1f_wjets_photon_pt.Sumw2()

th1f_wgjets_lepton_pt.Sumw2()
th1f_wjets_lepton_pt.Sumw2()

th1f_wgjets_delta_r.Sumw2()
th1f_wjets_delta_r.Sumw2()

for event in events_wgjets:

    if count > 10000:
        break

    if count % 1000 == 0:
        print "count = " + str(count)

    count +=1

    event.getByLabel (labelPacked, handlePacked)

    packed = handlePacked.product()

    event.getByLabel (labelPruned, handlePruned)

    pruned = handlePruned.product()

    event.getByLabel(geninfoLabel,geninfo)

    gen = geninfo.product()

    if gen.weight() > 0:
        countweighted += 1
    else:
        countweighted -= 1

    nelectrons = 0

    for p in pruned :

        if abs(p.pdgId()) == 11 and p.pt() > 25 and abs(p.eta()) < 2.5 and (p.statusFlags().isPrompt()) and p.status() == 1  :
            nelectrons += 1
            electron = p

    if nelectrons != 1:
        continue

    nphotons = 0        

    for p in pruned :

        if abs(p.pdgId()) == 22 and p.pt() > 25 and abs(p.eta()) < 2.5 and (p.statusFlags().isPrompt()) and p.status() == 1   :
            nphotons += 1
            photon = p

    if nphotons != 1:
        continue

#    if deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()) < 0.5:
#        continue

    njets = 0        

    for p in pruned :

#        if (abs(p.pdgId()) == 1 or abs(p.pdgId()) == 2 or abs(p.pdgId()) == 3 or abs(p.pdgId()) == 4 or abs(p.pdgId()) == 5 or abs(p.pdgId()) == 21) and p.pt() > 30 and p.statusFlags().isPrompt() and p.statusFlags().isLastCopy()  :
        if (abs(p.pdgId()) == 1 or abs(p.pdgId()) == 2) and p.pt() > 30 and p.statusFlags().isPrompt() and p.statusFlags().isLastCopy()  :
            njets +=1

    if gen.weight() > 0:
        th1f_wgjets_njets.Fill(njets,1)
        th1f_wgjets_photon_pt.Fill(photon.pt(),1)
        th1f_wgjets_lepton_pt.Fill(electron.pt(),1)
        th1f_wgjets_delta_r.Fill(deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()),1)
    else:
        th1f_wgjets_njets.Fill(njets,-1)
        th1f_wgjets_photon_pt.Fill(photon.pt(),-1)
        th1f_wgjets_lepton_pt.Fill(electron.pt(),-1)
        th1f_wgjets_delta_r.Fill(deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()),-1)

    #print njets

c = ROOT.TCanvas()

th1f_wgjets_njets.Scale(xs_wgjets*1000*36/countweighted)
th1f_wgjets_photon_pt.Scale(xs_wgjets*1000*36/countweighted)
th1f_wgjets_lepton_pt.Scale(xs_wgjets*1000*36/countweighted)
th1f_wgjets_delta_r.Scale(xs_wgjets*1000*36/countweighted)

th1f_wgjets_njets.SetLineWidth(3)
th1f_wgjets_photon_pt.SetLineWidth(3)
th1f_wgjets_lepton_pt.SetLineWidth(3)
th1f_wgjets_delta_r.SetLineWidth(3)

th1f_wgjets_njets.SetLineColor(ROOT.kRed)
th1f_wgjets_photon_pt.SetLineColor(ROOT.kRed)
th1f_wgjets_lepton_pt.SetLineColor(ROOT.kRed)
th1f_wgjets_delta_r.SetLineColor(ROOT.kRed)

count = 0
countweighted = 0

for event in events_wjets:

    if count > 1000000:
        break

    if count % 10000 == 0:
        print "count = " + str(count)

    count +=1

    event.getByLabel (labelPacked, handlePacked)

    packed = handlePacked.product()

    event.getByLabel (labelPruned, handlePruned)

    pruned = handlePruned.product()

    event.getByLabel(geninfoLabel,geninfo)

    gen = geninfo.product()

    if gen.weight() > 0:
        countweighted += 1
    else:
        countweighted -= 1

    nelectrons = 0

    for p in pruned :

#        if abs(p.pdgId()) == 11 and p.pt() > 25 and (p.statusFlags().isPrompt() or p.statusFlags().isPromptTauDecayProduct()) and p.status() == 1  :
        if abs(p.pdgId()) == 11 and p.pt() > 25 and abs(p.eta()) < 2.5 and (p.statusFlags().isPrompt())and p.status() == 1  :
            nelectrons += 1
            electron = p

    if nelectrons != 1:
        continue

    nphotons = 0        

    for p in pruned :

#        if abs(p.pdgId()) == 22 and p.pt() > 25 and (p.statusFlags().isPrompt() or p.statusFlags().isPromptTauDecayProduct()) and p.status() == 1   :
        if abs(p.pdgId()) == 22 and p.pt() > 25 and abs(p.eta()) < 2.5 and (p.statusFlags().isPrompt()) and p.status() == 1   :
            nphotons += 1
            photon = p

    if nphotons != 1:
        continue

#    if deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()) < 0.5:
#        continue

    njets = 0        

    for p in pruned :

#        if (abs(p.pdgId()) == 1 or abs(p.pdgId()) == 2 or abs(p.pdgId()) == 3 or abs(p.pdgId()) == 4 or abs(p.pdgId()) == 5 or abs(p.pdgId()) == 21) and p.pt() > 30 and p.statusFlags().isPrompt() and p.statusFlags().isLastCopy()  :
        if (abs(p.pdgId()) == 1 or abs(p.pdgId()) == 2) and p.pt() > 30 and p.statusFlags().isPrompt() and p.statusFlags().isLastCopy()  :
            njets +=1

    if gen.weight() > 0:
        th1f_wjets_njets.Fill(njets,1)
        th1f_wjets_photon_pt.Fill(photon.pt(),1)
        th1f_wjets_lepton_pt.Fill(electron.pt(),1)
        th1f_wjets_delta_r.Fill(deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()),1)
    else:
        th1f_wjets_njets.Fill(njets,-1)
        th1f_wjets_photon_pt.Fill(photon.pt(),-1)
        th1f_wjets_lepton_pt.Fill(electron.pt(),-1)
        th1f_wjets_delta_r.Fill(deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()),-1)
    #print njets

th1f_wjets_njets.Scale(xs_wjets*1000*36/countweighted)
th1f_wjets_photon_pt.Scale(xs_wjets*1000*36/countweighted)
th1f_wjets_lepton_pt.Scale(xs_wjets*1000*36/countweighted)
th1f_wjets_delta_r.Scale(xs_wjets*1000*36/countweighted)

th1f_wjets_njets.SetLineWidth(3)
th1f_wjets_photon_pt.SetLineWidth(3)
th1f_wjets_lepton_pt.SetLineWidth(3)
th1f_wjets_delta_r.SetLineWidth(3)

th1f_wjets_njets.SetLineColor(ROOT.kBlue)
th1f_wjets_photon_pt.SetLineColor(ROOT.kBlue)
th1f_wjets_lepton_pt.SetLineColor(ROOT.kBlue)
th1f_wjets_delta_r.SetLineColor(ROOT.kBlue)

if th1f_wjets_delta_r.GetMaximum() > th1f_wgjets_delta_r.GetMaximum():
    th1f_wjets_delta_r.Draw()
    th1f_wjets_delta_r.GetXaxis().SetTitle("#Delta R(l,g)")
    th1f_wjets_delta_r.SetStats(0)
    th1f_wgjets_delta_r.Draw("same")
else:
    th1f_wgjets_delta_r.Draw()
    th1f_wgjets_delta_r.GetXaxis().SetTitle("#Delta R(l,g)")
    th1f_wgjets_delta_r.SetStats(0)
    th1f_wjets_delta_r.Draw("same")

leg=ROOT.TLegend(.50,.65,.80,.80)

leg.AddEntry(th1f_wjets_delta_r,"w+jets","l")
leg.AddEntry(th1f_wgjets_delta_r,"wg+jets","l")

leg.Draw("same")

c.SaveAs("/eos/user/a/amlevin/www/tmp/delete_this.png")






