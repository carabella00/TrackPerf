import ROOT as r
import os
import os.path

from optparse import OptionParser
parser = OptionParser()

# Use this for user specific label at the end of the filename
parser.add_option('--label', metavar='F', type='string', action='store',
                  default='',
                  dest='label',
                  help='')
parser.add_option('--ptlabel', metavar='F', type='string', action='store',
                  default='',
                  dest='ptlabel',
                  help='e.g. pt3')
(options, args) = parser.parse_args()
argv = []

userLabel=""
userPtLabel=""
if options.label != "":
    userLabel = "_"+options.label
if options.ptlabel != "":
    userPtLabel = "_"+options.ptlabel

# Labels for input files
PUtypes = ["0","140","200","250","300"]
ptRangeTypes = {
    0:"",
    'L' : "Pt1p5to8",
    'H' : "Pt2to100"
}
pdgIdTypes = { 0 : "",
               1 : "_injet",
               2 : "_injet_highpt",
               3 : "_injet_vhighpt",
               13 : "_pdgid13",
               11 : "_pdgid11"
}

def SetPlotStyle():
  # from ATLAS plot style macro
  # use plain black on white colors
  r.gStyle.SetFrameBorderMode(0)
  r.gStyle.SetFrameFillColor(0)
  r.gStyle.SetCanvasBorderMode(0)
  r.gStyle.SetCanvasColor(0)
  r.gStyle.SetPadBorderMode(0)
  r.gStyle.SetPadColor(0)
  r.gStyle.SetStatColor(0)
  r.gStyle.SetHistLineColor(1)

  r.gStyle.SetPalette(1)

  # set the paper & margin sizes
  r.gStyle.SetPaperSize(20,26)
  r.gStyle.SetPadTopMargin(0.07)
  r.gStyle.SetPadRightMargin(0.05)
  r.gStyle.SetPadBottomMargin(0.14)
  r.gStyle.SetPadLeftMargin(0.16)

  # set title offsets (for axis label)
  r.gStyle.SetTitleXOffset(1.4)
  r.gStyle.SetTitleYOffset(1.4)

  # use large fonts
  r.gStyle.SetTextFont(42)
  r.gStyle.SetTextSize(0.05)
  r.gStyle.SetLabelFont(42,"x")
  r.gStyle.SetTitleFont(42,"x")
  r.gStyle.SetLabelFont(42,"y")
  r.gStyle.SetTitleFont(42,"y")
  r.gStyle.SetLabelFont(42,"z")
  r.gStyle.SetTitleFont(42,"z")
  r.gStyle.SetLabelSize(0.05,"x")
  r.gStyle.SetTitleSize(0.05,"x")
  r.gStyle.SetLabelSize(0.05,"y")
  r.gStyle.SetTitleSize(0.05,"y")
  r.gStyle.SetLabelSize(0.05,"z")
  r.gStyle.SetTitleSize(0.05,"z")

  # use bold lines and markers
  r.gStyle.SetMarkerStyle(20)
  r.gStyle.SetMarkerSize(1.2)
  r.gStyle.SetHistLineWidth(2)
  r.gStyle.SetLineStyleString(2,"[12 12]")

  # get rid of error bar caps
  r.gStyle.SetEndErrorSize(0.)

  # do not display any of the standard histogram decorations
  r.gStyle.SetOptTitle(0)
  r.gStyle.SetOptStat(0)
  r.gStyle.SetOptFit(0)

  # put tick marks on top and RHS of plots
  r.gStyle.SetPadTickX(1)
  r.gStyle.SetPadTickY(1)

def mySmallText(x, y, color, text):
  tsize=0.044;
  l = r.TLatex();
  l.SetTextSize(tsize); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);
def myItalicText(x, y, color, text):
  tsize=0.038;
  l = r.TLatex();
  l.SetTextSize(tsize); 
  l.SetTextFont(52); 
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);

def getAllHistogramsFromFile( what, sample, ptRange, pdgid, rebin, normToOne=False ):

  # Make list of input trees
  inputFileNames = [];
  inputFileNameTemplate = ""
  if 'TTbar' in sample:
    inputFileNameTemplate = "output_{sample}_PU{PU}_{trunc}{pdg}{userPtLabel}{userLabel}.root"
  else :
    inputFileNameTemplate = "output_{sample}{ptRange}_PU{PU}_{trunc}Truncation{pdg}{userPtLabel}{userLabel}.root"

  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[0], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[1], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[2], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[3], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[4], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[0], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithoutTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[1], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithoutTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[2], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithoutTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[3], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithoutTruncation', userPtLabel=userPtLabel, userLabel='' ) )
  inputFileNames.append( inputFileNameTemplate.format(sample = sample, PU = PUtypes[4], ptRange=ptRangeTypes[ptRange], pdg=pdgIdTypes[pdgid], 
                                                      trunc = 'WithoutTruncation', userPtLabel=userPtLabel, userLabel='' ) )

  # Get trees from files
  inputFiles=[];
  for i in range(0,len(inputFileNames)):
    print inputFileNames[i]
    if os.path.isfile( inputFileNames[i] ):
      inputFiles.append(r.TFile(inputFileNames[i]))
    else:
      inputFiles.append(None)

  histograms = {
    'PU0_wt' : getHistogramFromFile(inputFiles[0], what),
    'PU140_wt' : getHistogramFromFile(inputFiles[1], what),
    'PU200_wt' : getHistogramFromFile(inputFiles[2], what),
    'PU250_wt' : getHistogramFromFile(inputFiles[3], what),
    'PU300_wt' : getHistogramFromFile(inputFiles[4], what),
    'PU0_wot' : getHistogramFromFile(inputFiles[5], what),
    'PU140_wot' : getHistogramFromFile(inputFiles[6], what),
    'PU200_wot' : getHistogramFromFile(inputFiles[7], what),
    'PU250_wot' : getHistogramFromFile(inputFiles[8], what),
    'PU300_wot' : getHistogramFromFile(inputFiles[9], what),
  }
      

  if rebin > 1:
    for n, h in histograms.iteritems():
      if h != None:
        h.Rebin(rebin)

  if normToOne:
    for n, h in histograms.iteritems():
      if h != None:
        h.Scale( 1 / h.Integral() )
        h.GetYaxis().SetTitle('Fraction of events')
        if 'ntrk' in what:
          h.SetMinimum(0.0001)
  return histograms

def getHistogramFromFile(file, histogramName):
  if file != None and file.GetListOfKeys().Contains(histogramName):
    h = file.Get(histogramName)
    h.SetDirectory(0)
    return h
  else: return None

def setMarkerAndLineAttributes(h, colour, style, lineStyle=1 ):
  h.SetLineColor( colour )
  h.SetMarkerColor( colour )
  h.SetMarkerStyle( style )
  h.SetLineStyle( lineStyle )

def drawHistogramWithOption(h,drawOption):
  h.GetXaxis().SetTitleOffset(1.2)
  h.Draw(drawOption)
  if not 'same' in drawOption:
    drawOption +=', same'
  return drawOption

def setupLegend(sample, histograms, PULabels, legPosition=""):
  legx = 0.64;
  legy = 0.17;
  if legPosition == 'topright':
    legx = 0.64
    legy = 0.58
  r.gPad.cd()
  l = r.TLegend(legx,legy,legx+0.3,legy+0.3)
  l.SetFillColor(0)
  #l.SetFillStyle(0)
  l.SetLineColor(0)
  l.SetTextSize(0.04)
  l.AddEntry(histograms['PU0_wt'], "With truncation", "p")
  l.AddEntry(histograms['PU0_wot'], "Without truncation", "l")
  l.AddEntry(None,"","")

  if histograms['PU0_wt'] != None or histograms['PU0_wot'] != None :
    h = histograms['PU0_wt']
    if h == None: h = histograms['PU0_wot']
    l.AddEntry(h,PULabels[0],"lp")
  if histograms['PU140_wt'] != None or histograms['PU140_wot'] != None :
    h = histograms['PU140_wt']
    if h == None: h = histograms['PU140_wot']
    l.AddEntry(h,PULabels[1],"lp")
  if histograms['PU200_wt'] != None or histograms['PU200_wot'] != None :
    h = histograms['PU200_wt']
    if h == None: h = histograms['PU200_wot']
    l.AddEntry(h,PULabels[2],"lp")
  if histograms['PU250_wt'] != None or histograms['PU250_wot'] != None :
    h = histograms['PU250_wt']
    if h == None: h = histograms['PU250_wot']
    l.AddEntry(h,PULabels[3],"lp")
  if histograms['PU300_wt'] != None or histograms['PU300_wot'] != None :
    h = histograms['PU300_wt']
    if h == None: h = histograms['PU300_wot']
    l.AddEntry(h,PULabels[4],"lp")
  l.SetTextFont(42)

  return l

# ----------------------------------------------------------------------------------------------------------------
# Main script
def compareEfficiency(what, sample, ptRange=0, pdgid=0,rebin=0, normToOne=False, legPosition=""):
  
  SetPlotStyle()
  # Labels for the plots
  PULabels = ["<PU>=0", "<PU>=140", "<PU>=200", "<PU>=250", "<PU>=300"]
  ptRangeLabels = ["2 < P_{T} < 8 GeV","P_{T} > 8 GeV"]

  # Get histograms
  histograms = getAllHistogramsFromFile( what, sample, ptRange, pdgid, rebin, normToOne )

  canvas = r.TCanvas()

  # Draw histogram with truncation, as points
  drawOption='p'
  if histograms['PU0_wt'] != None:
    setMarkerAndLineAttributes( histograms['PU0_wt'], 1, 20, 1)
    drawOption = drawHistogramWithOption( histograms['PU0_wt'], drawOption )
  if histograms['PU140_wt'] != None :
    setMarkerAndLineAttributes( histograms['PU140_wt'], 2, 22, 1)
    drawOption = drawHistogramWithOption( histograms['PU140_wt'], drawOption )
  if histograms['PU200_wt'] != None:
    setMarkerAndLineAttributes( histograms['PU200_wt'], 9, 21, 1)
    drawOption = drawHistogramWithOption (histograms['PU200_wt'], drawOption)
  if histograms['PU250_wt'] != None:
    setMarkerAndLineAttributes( histograms['PU250_wt'], 8, 23, 1)
    drawOption = drawHistogramWithOption (histograms['PU250_wt'], drawOption)
  if histograms['PU300_wt'] != None:
    setMarkerAndLineAttributes( histograms['PU300_wt'], 12, 33, 1)
    drawOption = drawHistogramWithOption (histograms['PU300_wt'], drawOption)

  if 'same' in drawOption:
    drawOption = 'hist,l,same'
  else:
    drawOption = 'hist,l'

  # Draw histograms without truncation, as lines
  if histograms['PU0_wot'] != None:
    setMarkerAndLineAttributes( histograms['PU0_wot'], 1, 20, 2)
    drawOption = drawHistogramWithOption (histograms['PU0_wot'], drawOption )
  if histograms['PU140_wot'] != None:
    setMarkerAndLineAttributes( histograms['PU140_wot'], 2, 4, 2)
    drawOption = drawHistogramWithOption (histograms['PU140_wot'], drawOption )
  if histograms['PU200_wot'] != None:
    setMarkerAndLineAttributes( histograms['PU200_wot'], 9, 33, 2)
    drawOption = drawHistogramWithOption (histograms['PU200_wot'], drawOption )
  if histograms['PU250_wot'] != None:
    setMarkerAndLineAttributes( histograms['PU250_wot'], 8, 43, 2)
    drawOption = drawHistogramWithOption (histograms['PU250_wot'], drawOption )
  if histograms['PU300_wot'] != None:
    setMarkerAndLineAttributes( histograms['PU300_wot'], 12, 33, 2)
    drawOption = drawHistogramWithOption (histograms['PU300_wot'], drawOption )
  if 'eff' in what:
    r.gPad.SetGridy();

  # Make the legend
  l = setupLegend(sample,histograms,PULabels, legPosition)
  l.Draw()

  # Save canvas
  outputDir = 'OverlayPlots'+userPtLabel
  if not os.path.isdir(outputDir):
    os.mkdir(outputDir)
  outputFileName = "{outputDir}/{sample}_{what}.pdf".format( outputDir=outputDir, sample = sample, what=what )

  if 'TTbar' in sample:
    if pdgid == 13:
      outputFileName = "{outputDir}/{sample}_muons_{what}.pdf".format( outputDir=outputDir, sample = sample, what=what )
    elif pdgid == 11:
      outputFileName = "{outputDir}/{sample}_electrons_{what}.pdf".format( outputDir=outputDir, sample = sample, what=what )
    elif pdgid == 0:
      outputFileName = "{outputDir}/{sample}_inclusive_{what}.pdf".format( outputDir=outputDir, sample = sample, what=what )
    elif pdgid == 1:
      outputFileName = "{outputDir}/{sample}_injet_{what}.pdf".format( outputDir=outputDir, sample = sample, what=what )
    elif pdgid == 2:
      outputFileName = "{outputDir}/{sample}_injet_highpt_{what}.pdf".format( outputDir=outputDir, sample = sample, what=what )
    elif pdgid == 3:
      outputFileName = "{outputDir}/{sample}_injet_vhighpt_{what}.pdf".format( outputDir=outputDir, sample = sample, what=what )

  if 'ntrk_pt' in what and sample != 'TTbar':
    outputFileName = "{outputDir}/{sample}_{ptRange}_{what}.pdf".format( outputDir=outputDir, ptRange=ptRange, sample = sample, what=what )

  #if 'ntrk_pt' in what:
  #canvas.SetLogy()

  canvas.Print(outputFileName);

  
if __name__ == '__main__':
  r.gROOT.SetBatch()

  for sample in ['TTbar']:
    for pdg in [0,11,13]:
      compareEfficiency("eff_pt_L",sample,0,pdg)
      compareEfficiency("eff_pt_H",sample,0,pdg)
      compareEfficiency("eff_eta_L",sample,0,pdg)
      compareEfficiency("eff_eta_H",sample,0,pdg)
    for pdg in [0,1,2,3,11,13]:
      compareEfficiency("eff_pt",sample,0,pdg)
      compareEfficiency("eff_eta",sample,0,pdg)

    compareEfficiency("ntrk_pt2",sample,0,0,rebin=4, normToOne=True, legPosition="topright")
    compareEfficiency("ntrk_pt3",sample,0,0,rebin=4, normToOne=True, legPosition="topright")
    compareEfficiency("ntrk_pt10",sample,0,0,rebin=2, normToOne=True, legPosition="topright")


  #pGunSamples = {
  #  'MuonPt1p5to8' : 13,
  #  'MuonPt2to100' : 13,
  #  'ElectronPt1p5to8' : 11,
  #  'ElectronPt2to100' : 11,
  #}
  #for sample, pdg in pGunSamples.iteritems():
  #  compareEfficiency("eff_eta",sample,0,pdg)
  #  compareEfficiency("eff_pt_L",sample,0,pdg)
  #  compareEfficiency("eff_pt_H",sample,0,pdg)

  #compareEfficiency("ntrk_pt2",'OnlyPU',0,0,rebin=4, normToOne=True, legPosition="topright")
  #compareEfficiency("ntrk_pt3",'OnlyPU',0,0,rebin=4, normToOne=True, legPosition="topright")
  #compareEfficiency("ntrk_pt10",'OnlyPU',0,0,rebin=4, normToOne=True, legPosition="topright")
