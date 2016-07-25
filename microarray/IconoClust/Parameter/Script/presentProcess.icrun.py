CCT._Description = {
"Author" : 	"Clondiag Chip Technologies",
"Target" : 	"Processing of Standard Array Experiments",
"Description" : 	'''
		Script processes the active image.
		Histogram and Model-based Spot Segmentation are optional.
		Substance Sorting: Determines 
		- Mean for the Mean(gray) for each Substance,
		- Sigma for the Mean(gray) for each Substance.
		Graphical Result Presentation for these features.
		''',
"Parameter" :	'''
		icprm_color:	DARK or BRIGHT
		icprm_mode:	0 for defined shape
				1 for automatic shape
				2 for model shape
		icprm_featlist:	Features to determine
				Selection out of (Mean, Background, Sigma, Median, Area, CoG_x, CoG_y)
		''',
"Version" :	2.0
}

__ICPRM__ = { "icprm_color":		"BRIGHT",
		"icprm_mode": 		"0",
		"icprm_featlist":		'( "Mean", "Background", "Sigma" )'	}


__SpotAligning = 1

BRIGHT = 1
DARK = 0

mode = icprm_mode
color = icprm_color
linethres = 0.05
if mode == 2:
	thres = 2	#RAYLEIGH
	prm_thres = ( 0.3, 0.0, 0.0, 0.5, 0.5, 0.9, 1.2 )
	seg = 0 
	prm_seg = ( 500.0, 0.7, 2000.0, 2000.0, 2.0, 0.00001, 0.0, 0.001 )
elif mode == 1:
	thres = GRADIENT
	prm_thres = ( 0.7, 0.002, 0.3, 1.0, 1.0 )
	seg = CONVEX
	prm_seg = ( 3.0, 0.3 )
else:
	thres = 0
	prm_thres = ()
	seg = 0
	prm_seg = ()

import string
import math
import os

CCT.fluoroFeatures = {}

if mode == 2 and color == BRIGHT:		#model-based
	idi = CCT.GetCurrentImage()
	icono.InvertImage( idi, idi )
elif mode == 1:				#gradient-histogram-based
	# set last parameter to color
	prm_thres = list( prm_thres )
	prm_thres[-1] = float( color )
	prm_thres = tuple( prm_thres )
		
	
CCT.RunAlignment( mode = mode, param = { "Transformation": ( 0, ( linethres, ) ),
                                  	"Thresholding": ( thres, prm_thres ),
                                  	"Segmentation": ( seg, prm_seg ) } )

if mode == 2 and color == BRIGHT:		#model-based
	idi = CCT.GetCurrentImage()
	icono.InvertImage( idi, idi )

__SpotAligning = 0

__DetFeatures = 1

id_img = CCT.image_act
featlist = icprm_featlist
if not "Mean" in featlist:
	featlist.append( "Mean" )
if not "Background" in featlist:
	featlist.append( "Background" )

CCT.DetermineFeatures( id_img, featlist )
feat_mean = CCT.features["Mean"] 
feat_back = CCT.features["Background"]
try:
	feat_subst = CCT.features["Substance"]
except:
	feat_subst = "Standard" * len( feat_mean )
CCT.featSubst = []
for subst in feat_subst:
	try:
		pos = CCT.featSubst.index( subst )
	except:
		CCT.featSubst.append( subst )

CCT.featSubst.sort()

CCT.fluoroFeatures = range( len( CCT.featSubst ) )
for i in xrange( len( CCT.featSubst ) ):
	CCT.fluoroFeatures[i] = []
for i in xrange( len( feat_mean ) ):
	subst = CCT.features["Substance"][i]
	CCT.fluoroFeatures[ CCT.featSubst.index( subst ) ].append( ( feat_mean[i], feat_back[i] ) )	

__DetFeatures = 0

__Presentation = 1

print "Formatting Features ..."

def MeanList( liste ):
	amount = len( liste[0] )
	sum = [ 0.0, ] * amount
	for tuple in liste:
		for i in xrange( amount ):
			sum[i] += tuple[i]
	for i in xrange( amount ):
		sum[i] /= len( liste )
	return sum

def SigmaList( liste, mean ):
	amount = len( liste[0] )
	sum = [ 0.0, ] * amount
	for tuple in liste:
		for i in xrange( amount ):
			sum[i] +=  ( tuple[i] - mean[i] ) * ( tuple[i] - mean[i] )
	for i in xrange( amount ):
		sum[i] /= len( liste )
		sum[i] = math.sqrt( sum[i] )
	return sum

fluoroResult = { 	"Substance" : [],
		"Mean( Intensity )" : [], 
		"Sigma( Intensity )" : [] }
for i in xrange( len( CCT.featSubst ) ):
	mean = MeanList( CCT.fluoroFeatures[i] )
	sigma = SigmaList( CCT.fluoroFeatures[i], mean )
	fluoroResult["Substance"].append( CCT.featSubst[i] )
	fluoroResult["Mean( Intensity )"].append( min( mean[0], 1.0 ) )
	fluoroResult["Sigma( Intensity )"].append( min( sigma[0], 1.0 ) )

import Presentation
pr = Presentation.Presentation()
pr.SetData( data_dict = fluoroResult )

pr.CreateGUI( "IconoClustPresentation.Show" )
pr.ExportData( name = "IconoClust Results", show_keys = ["Mean( Intensity )" , "Sigma( Intensity )"] )
pr.Show()

CCT.Presentation = pr 
CCT.vb_control.SetPresentation( "Presentation" )

__Presentation = 0

