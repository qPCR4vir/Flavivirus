CCT._Description = {
"Author" : 	"Clondiag Chip Technologies",
"Target" : 	"Processing of Standard Array Experiments",
"Description" : 	'''
		Script processes the active image.
		Histogram and Model-based Spot Segmentation are optional.''',
"Parameter" :	'''
		icprm_color:	DARK or BRIGHT
		icprm_mode:	0 for defined shape
				1 for automatic shape
				2 for model shape
				4 for MSER
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
if mode == 4:
	# MSER
	thres = 4
	prm_thres = ( 0.8, 0.015, 3.0 )
	seg = CONVEX
	prm_seg = ()
elif mode == 2:
	thres = 2	
	prm_thres = ( 0.8, 0.0, 0.0, 0.5, 0.5, 0.9, 1.2 )
	seg = 0 
	prm_seg = ( 500.0, 0.7, 2000.0, 2000.0, 2.0, 0.00001, 0.0, 0.001 )
elif mode == 1:
	thres = 1
	if color == BRIGHT:
		prm_thres = ( 0.7, 0.004, 0.3, 1.0, 1.0 )
	else:
		prm_thres = ( 0.7, 0.004, 0.3, 1.0, 2.0 )
	seg = CONVEX
	prm_seg = ( 3.0, 0.3 )
else:
	thres = 0
	prm_thres = ()
	seg = 0
	prm_seg = ()

idi = CCT.GetCurrentImage()

if ( mode == 2 and color == BRIGHT ) or ( mode == 4 and color == DARK ):		
	#model-based or MSER-based
	icono.InvertImage( idi, idi )
try:
	CCT.RunAlignment( mode = mode, param = { "Transformation": ( 0, ( linethres, ) ),
                                  	"Thresholding": ( thres, prm_thres ),
                                  	"Segmentation": ( seg, prm_seg ) } )

finally:
	if ( mode == 2 and color == BRIGHT ) or ( mode == 4 and color == DARK ):		
		#model-based or MSER-based
		icono.InvertImage( idi, idi )

__SpotAligning = 0

__DetFeatures = 1
idi = CCT.GetCurrentImage()
# Get the features of the last processed image
CCT.DetermineFeatures( idi, icprm_featlist )
__DetFeatures = 0

