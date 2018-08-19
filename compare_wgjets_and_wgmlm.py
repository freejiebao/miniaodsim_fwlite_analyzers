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

events_wgjets = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/00000/0211D6FC-5A02-E811-98F1-E0071B7AC750.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/00000/04F88CD1-6C03-E811-98A5-0CC47AD98D26.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/00000/08D50A8B-0507-E811-85F3-002590D600F2.root'])

events_wgmlm = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/FEB2F873-C1D8-E611-8AAC-02163E012A61.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/FE7D5692-A2D8-E611-8A72-02163E0142BE.root','root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F8C6F680-C1D8-E611-A5C2-02163E01448F.root'])

xs_wgmlm = 377.5
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
th1f_wgmlm_njets = ROOT.TH1F("wgmlm njets","",7,-0.5,6.5)

th1f_wgjets_photon_pt = ROOT.TH1F("wgjets photon pt","",35,25,200)
th1f_wgmlm_photon_pt = ROOT.TH1F("wgmlm photon pt","",35,25,200)

th1f_wgjets_photon_eta = ROOT.TH1F("wgjets photon eta","",10,-2.5,2.5)
th1f_wgmlm_photon_eta = ROOT.TH1F("wgmlm photon eta","",10,-2.5,2.5)

th1f_wgjets_lepton_pt = ROOT.TH1F("wgjets lepton pt","",35,25,200)
th1f_wgmlm_lepton_pt = ROOT.TH1F("wgmlm lepton pt","",35,25,200)

th1f_wgjets_lepton_eta = ROOT.TH1F("wgjets lepton eta","",10,-2.5,2.5)
th1f_wgmlm_lepton_eta = ROOT.TH1F("wgmlm lepton eta","",10,-2.5,2.5)

th1f_wgjets_delta_r = ROOT.TH1F("wgjets delta r","",50,0.,5.)
th1f_wgmlm_delta_r = ROOT.TH1F("wgmlm delta r","",50,0.,5.)

th1f_wgjets_njets.Sumw2()
th1f_wgmlm_njets.Sumw2()

th1f_wgjets_photon_pt.Sumw2()
th1f_wgmlm_photon_pt.Sumw2()

th1f_wgjets_photon_eta.Sumw2()
th1f_wgmlm_photon_eta.Sumw2()

th1f_wgjets_lepton_pt.Sumw2()
th1f_wgmlm_lepton_pt.Sumw2()

th1f_wgjets_lepton_eta.Sumw2()
th1f_wgmlm_lepton_eta.Sumw2()

th1f_wgjets_delta_r.Sumw2()
th1f_wgmlm_delta_r.Sumw2()

for event in events_wgjets:

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
        th1f_wgjets_photon_eta.Fill(photon.eta(),1)
        th1f_wgjets_lepton_pt.Fill(electron.pt(),1)
        th1f_wgjets_lepton_eta.Fill(electron.eta(),1)
        th1f_wgjets_delta_r.Fill(deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()),1)
    else:
        th1f_wgjets_njets.Fill(njets,-1)
        th1f_wgjets_photon_pt.Fill(photon.pt(),-1)
        th1f_wgjets_photon_eta.Fill(photon.eta(),-1)
        th1f_wgjets_lepton_pt.Fill(electron.pt(),-1)
        th1f_wgjets_lepton_eta.Fill(electron.eta(),-1)
        th1f_wgjets_delta_r.Fill(deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()),-1)

    #print njets

#c = ROOT.TCanvas()
c1 = ROOT.TCanvas()
c2 = ROOT.TCanvas()
c3 = ROOT.TCanvas()
c4 = ROOT.TCanvas()

th1f_wgjets_njets.Scale(xs_wgjets*1000*36/countweighted)
th1f_wgjets_photon_pt.Scale(xs_wgjets*1000*36/countweighted)
th1f_wgjets_photon_eta.Scale(xs_wgjets*1000*36/countweighted)
th1f_wgjets_lepton_pt.Scale(xs_wgjets*1000*36/countweighted)
th1f_wgjets_lepton_eta.Scale(xs_wgjets*1000*36/countweighted)
th1f_wgjets_delta_r.Scale(xs_wgjets*1000*36/countweighted)

th1f_wgjets_njets.SetLineWidth(3)
th1f_wgjets_photon_pt.SetLineWidth(3)
th1f_wgjets_photon_eta.SetLineWidth(3)
th1f_wgjets_lepton_pt.SetLineWidth(3)
th1f_wgjets_lepton_eta.SetLineWidth(3)
th1f_wgjets_delta_r.SetLineWidth(3)

th1f_wgjets_njets.SetLineColor(ROOT.kBlue)
th1f_wgjets_photon_pt.SetLineColor(ROOT.kBlue)
th1f_wgjets_photon_eta.SetLineColor(ROOT.kBlue)
th1f_wgjets_lepton_pt.SetLineColor(ROOT.kBlue)
th1f_wgjets_lepton_eta.SetLineColor(ROOT.kBlue)
th1f_wgjets_delta_r.SetLineColor(ROOT.kBlue)

count = 0
countweighted = 0

for event in events_wgmlm:

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
        th1f_wgmlm_njets.Fill(njets,1)
        th1f_wgmlm_photon_pt.Fill(photon.pt(),1)
        th1f_wgmlm_photon_eta.Fill(photon.eta(),1)
        th1f_wgmlm_lepton_pt.Fill(electron.pt(),1)
        th1f_wgmlm_lepton_eta.Fill(electron.eta(),1)
        th1f_wgmlm_delta_r.Fill(deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()),1)
    else:
        th1f_wgmlm_njets.Fill(njets,-1)
        th1f_wgmlm_photon_pt.Fill(photon.pt(),-1)
        th1f_wgmlm_photon_eta.Fill(photon.eta(),-1)
        th1f_wgmlm_lepton_pt.Fill(electron.pt(),-1)
        th1f_wgmlm_lepton_eta.Fill(electron.eta(),-1)
        th1f_wgmlm_delta_r.Fill(deltaR(electron.eta(), electron.phi(), photon.eta(), photon.phi()),-1)
    #print njets

th1f_wgmlm_njets.Scale(xs_wgmlm*1000*36/countweighted)
th1f_wgmlm_photon_pt.Scale(xs_wgmlm*1000*36/countweighted)
th1f_wgmlm_photon_eta.Scale(xs_wgmlm*1000*36/countweighted)
th1f_wgmlm_lepton_pt.Scale(xs_wgmlm*1000*36/countweighted)
th1f_wgmlm_lepton_eta.Scale(xs_wgmlm*1000*36/countweighted)
th1f_wgmlm_delta_r.Scale(xs_wgmlm*1000*36/countweighted)

th1f_wgmlm_njets.SetLineWidth(3)
th1f_wgmlm_photon_pt.SetLineWidth(3)
th1f_wgmlm_photon_eta.SetLineWidth(3)
th1f_wgmlm_lepton_pt.SetLineWidth(3)
th1f_wgmlm_lepton_eta.SetLineWidth(3)
th1f_wgmlm_delta_r.SetLineWidth(3)

th1f_wgmlm_njets.SetLineColor(ROOT.kRed)
th1f_wgmlm_photon_pt.SetLineColor(ROOT.kRed)
th1f_wgmlm_photon_eta.SetLineColor(ROOT.kRed)
th1f_wgmlm_lepton_pt.SetLineColor(ROOT.kRed)
th1f_wgmlm_lepton_eta.SetLineColor(ROOT.kRed)
th1f_wgmlm_delta_r.SetLineColor(ROOT.kRed)

th1f_wgmlm_photon_eta.SetMaximum(45000.)
th1f_wgmlm_photon_eta.SetMinimum(0.)
th1f_wgjets_photon_eta.SetMaximum(45000.)
th1f_wgjets_photon_eta.SetMinimum(0.)

th1f_wgmlm_lepton_eta.SetMaximum(45000.)
th1f_wgmlm_lepton_eta.SetMinimum(0.)
th1f_wgjets_lepton_eta.SetMaximum(45000.)
th1f_wgjets_lepton_eta.SetMinimum(0.)

c1.cd()
if th1f_wgmlm_photon_pt.GetMaximum() > th1f_wgjets_photon_pt.GetMaximum():
    th1f_wgmlm_photon_pt.Draw()
    th1f_wgmlm_photon_pt.GetXaxis().SetTitle("photon pt(GeV)")
    th1f_wgmlm_photon_pt.SetStats(0)
    th1f_wgjets_photon_pt.Draw("same")
else:
    th1f_wgjets_photon_pt.Draw()
    th1f_wgjets_photon_pt.GetXaxis().SetTitle("photon pt(GeV)")
    th1f_wgjets_photon_pt.SetStats(0)
    th1f_wgmlm_photon_pt.Draw("same")

leg1=ROOT.TLegend(.65,.80,.95,.95)

leg1.AddEntry(th1f_wgjets_photon_pt,"wgjets","l")
leg1.AddEntry(th1f_wgmlm_photon_pt,"wgmlm","l")

leg1.Draw("same")
c1.SaveAs("/eos/user/j/jixiao/wgjets_wgmlm/photon_pt.png")

c2.cd()
if th1f_wgmlm_photon_eta.GetMaximum() > th1f_wgjets_photon_eta.GetMaximum():
    th1f_wgmlm_photon_eta.Draw()
    th1f_wgmlm_photon_eta.GetXaxis().SetTitle("photon eta")
    th1f_wgmlm_photon_eta.SetStats(0)
    th1f_wgjets_photon_eta.Draw("same")
else:
    th1f_wgjets_photon_eta.Draw()
    th1f_wgjets_photon_eta.GetXaxis().SetTitle("photon eta")
    th1f_wgjets_photon_eta.SetStats(0)
    th1f_wgmlm_photon_eta.Draw("same")

leg2=ROOT.TLegend(.65,.80,.95,.95)

leg2.AddEntry(th1f_wgjets_photon_eta,"wgjets","l")
leg2.AddEntry(th1f_wgmlm_photon_eta,"wgmlm","l")

leg2.Draw("same")
c2.SaveAs("/eos/user/j/jixiao/wgjets_wgmlm/photon_eta.png")

c3.cd()
if th1f_wgmlm_lepton_eta.GetMaximum() > th1f_wgjets_lepton_eta.GetMaximum():
    th1f_wgmlm_lepton_eta.Draw()
    th1f_wgmlm_lepton_eta.GetXaxis().SetTitle("lepton eta")
    th1f_wgmlm_lepton_eta.SetStats(0)
    th1f_wgjets_lepton_eta.Draw("same")
else:
    th1f_wgjets_lepton_eta.Draw()
    th1f_wgjets_lepton_eta.GetXaxis().SetTitle("lepton eta")
    th1f_wgjets_lepton_eta.SetStats(0)
    th1f_wgmlm_lepton_eta.Draw("same")

leg3=ROOT.TLegend(.65,.80,.95,.95)

leg3.AddEntry(th1f_wgjets_lepton_eta,"wgjets","l")
leg3.AddEntry(th1f_wgmlm_lepton_eta,"wgmlm","l")

leg3.Draw("same")
c3.SaveAs("/eos/user/j/jixiao/wgjets_wgmlm/lepton_eta.png")

c4.cd()
if th1f_wgmlm_delta_r.GetMaximum() > th1f_wgjets_delta_r.GetMaximum():
    th1f_wgmlm_delta_r.Draw()
    th1f_wgmlm_delta_r.GetXaxis().SetTitle("delta_r")
    th1f_wgmlm_delta_r.SetStats(0)
    th1f_wgjets_delta_r.Draw("same")
else:
    th1f_wgjets_delta_r.Draw()
    th1f_wgjets_delta_r.GetXaxis().SetTitle("delta_r")
    th1f_wgjets_delta_r.SetStats(0)
    th1f_wgmlm_delta_r.Draw("same")

leg4=ROOT.TLegend(.65,.80,.95,.95)

leg4.AddEntry(th1f_wgjets_delta_r,"wgjets","l")
leg4.AddEntry(th1f_wgmlm_delta_r,"wgmlm","l")

leg4.Draw("same")
c4.SaveAs("/eos/user/j/jixiao/wgjets_wgmlm/dr.png")
'''
c1.cd()
if th1f_wgmlm_lepton_pt.GetMaximum() > th1f_wgjets_lepton_pt.GetMaximum():
    th1f_wgmlm_lepton_pt.Draw()
    th1f_wgmlm_lepton_pt.GetXaxis().SetTitle("lepton pt (GeV)")
    th1f_wgmlm_lepton_pt.SetStats(0)
    th1f_wgjets_lepton_pt.Draw("same")
else:
    th1f_wgjets_lepton_pt.Draw()
    th1f_wgjets_lepton_pt.GetXaxis().SetTitle("lepton pt (GeV)")
    th1f_wgjets_lepton_pt.SetStats(0)
    th1f_wgmlm_lepton_pt.Draw("same")

leg1=ROOT.TLegend(.50,.65,.80,.80)

leg1.AddEntry(th1f_wgmlm_lepton_pt,"wgmlm","l")
leg1.AddEntry(th1f_wgjets_lepton_pt,"wgjets","l")

leg1.Draw("same")

c2.cd()
if th1f_wgmlm_photon_pt.GetMaximum() > th1f_wgjets_photon_pt.GetMaximum():
    th1f_wgmlm_photon_pt.Draw()
    th1f_wgmlm_photon_pt.GetXaxis().SetTitle("photon pt (GeV)")
    th1f_wgmlm_photon_pt.SetStats(0)
    th1f_wgjets_photon_pt.Draw("same")
else:
    th1f_wgjets_photon_pt.Draw()
    th1f_wgjets_photon_pt.GetXaxis().SetTitle("photon pt (GeV)")
    th1f_wgjets_photon_pt.SetStats(0)
    th1f_wgmlm_photon_pt.Draw("same")

leg2=ROOT.TLegend(.50,.65,.80,.80)

leg2.AddEntry(th1f_wgmlm_photon_pt,"wgmlm","l")
leg2.AddEntry(th1f_wgjets_photon_pt,"wgjets","l")

leg2.Draw("same")

c3.cd()
if th1f_wgmlm_njets.GetMaximum() > th1f_wgjets_njets.GetMaximum():
    th1f_wgmlm_njets.Draw()
    th1f_wgmlm_njets.GetXaxis().SetTitle("njets")
    th1f_wgmlm_njets.SetStats(0)
    th1f_wgjets_njets.Draw("same")
else:
    th1f_wgjets_njets.Draw()
    th1f_wgjets_njets.GetXaxis().SetTitle("njets")
    th1f_wgjets_njets.SetStats(0)
    th1f_wgmlm_njets.Draw("same")

leg3=ROOT.TLegend(.50,.65,.80,.80)

leg3.AddEntry(th1f_wgmlm_njets,"wgmlm","l")
leg3.AddEntry(th1f_wgjets_njets,"wgjets","l")

leg3.Draw("same")

c4.cd()
if th1f_wgmlm_delta_r.GetMaximum() > th1f_wgjets_delta_r.GetMaximum():
    th1f_wgmlm_delta_r.Draw()
    th1f_wgmlm_delta_r.GetXaxis().SetTitle("delta_r")
    th1f_wgmlm_delta_r.SetStats(0)
    th1f_wgjets_delta_r.Draw("same")
else:
    th1f_wgjets_delta_r.Draw()
    th1f_wgjets_delta_r.GetXaxis().SetTitle("delta_r")
    th1f_wgjets_delta_r.SetStats(0)
    th1f_wgmlm_delta_r.Draw("same")

leg4=ROOT.TLegend(.50,.65,.80,.80)

leg4.AddEntry(th1f_wgmlm_delta_r,"wgmlm","l")
leg4.AddEntry(th1f_wgjets_delta_r,"wgjets","l")

leg4.Draw("same")

f=ROOT.TFile.Open('out.root','RECREATE')
f.cd()
c1.Write()
c2.Write()

c3.Write()
c4.Write()
f.Close()
'''
