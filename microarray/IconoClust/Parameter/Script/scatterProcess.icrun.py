CCT._Description = {
"Author" : 	"Clondiag Chip Technologies",
"Target" : 	"Processing of Standard Array Experiments",
"Description" : 	'''
		Script processes the first two images in experiment.
		Histogram and Model-based Spot Segmentation are optional.
		Scatterplot is generated with different colors for each substance.
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
	thres = 2	
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

if mode == 1:				#gradient-histogram-based
	# set last parameter to color
	prm_thres = list( prm_thres )
	prm_thres[4] = float( color )
	prm_thres = tuple( prm_thres )
		
	
import PresentScatterEnviron
CCT.PresentScatter = PresentScatterEnviron.PresentScatterEnviron()

images = CCT.GetSortedImageIDs()
for image in images:
	CCT.CommitImages( image )
	if mode == 2 and color == BRIGHT:		#model-based
		icono.InvertImage( image, image )
	try:
		CCT.RunAlignment( mode = mode, param = { "Transformation": ( 0, ( linethres, ) ),
                                  		"Thresholding": ( thres, prm_thres ),
                                  		"Segmentation": ( seg, prm_seg ) } )

	finally:
		if mode == 2 and color == BRIGHT:		#model-based
			icono.InvertImage( image, image )

	CCT.DetermineFeatures( image, icprm_featlist )
	CCT.PresentScatter.SetData( self.features, CCT.GetImageName( image ) )
		
__SpotAligning = 0

__DetFeatures = 1

CCT.PresentScatter.InitializeGUI()
CCT.vb_control.SetPresentation( "PresentScatter" )
CCT.PresentScatter.Show()

__DetFeatures = 0
