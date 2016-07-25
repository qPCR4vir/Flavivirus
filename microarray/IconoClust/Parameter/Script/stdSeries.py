CCT._Description = {
"Author" : 	"CLONDIAG chip technologies",
"Target" : 	"Processing of Standard Image Series Experiments",
"Description" : 	'''
		Script processes all images of a given series.
		The Results are graphed in a special Presentation Component.
		Model-based Segmentation is optional.
		Automatic Reference System Recognition is optional.
		''',
"Parameter" : 	'''
		icprm_spot_color:		DARK or BRIGHT
		icprm_mode:		0 for fixed segmentation according to layout
					1 for Model-based Segmentation
		icprm_ref_mode:		0 for manual setting of Reference Points
					1 for Automatic Reference System Detection
		icprm_spot_model:	Model parameter (scale, anisotropic scale, rotation, shift_x, shift_y, final_scale, roi_scale)
		icprm_hist_spot:		Tuple with histogram-parameters for selecting spot-pixel
		icprm_hist_back:		Tuple with histogram-parameters for selecting background-pixel
		icprm_sub_back:		0 for not subtracting the background from the mean value
					1 for subtracting the background from the mean value
					2 for dividing mean by background value
		icprm_name:		String to distinguish scripts
		icprm_batch:		0 for processing active image
					1 for processing image series
		''',
"Version" : 	2.4,
"Created" :	"21.08.2007",
}

__ICPRM__ = { "icprm_spot_color":	"BRIGHT",	
		"icprm_mode": 		1,
		"icprm_ref_mode":	0,
		"icprm_spot_model":	( 0.5, 0.0, 0.0, 0.1, 0.1, 0.9, 1.0 ),
		"icprm_hist_spot":	( 0.3, 0.9 ),
		"icprm_hist_back":	( 0.1, 0.7 ),
		"icprm_sub_back":	0,
		"icprm_batch":		1,
		"icprm_name":		"''",	}

BRIGHT = 1
DARK = 2

self.featMode = 0
#don't create self.listFeatures automatically

if icprm_batch:
	images = CCT.GetSortedImageIDs()
else:
	images = ( CCT.GetCurrentImage(), )

if icprm_mode:
	mode = 2
else:
	mode = 0
# only allow model-based segmentation or fixed ROI
ref_mode = icprm_ref_mode

import ATProcess
processor = ATProcess.Processor( icprm_mode, icprm_ref_mode )

if ref_mode:
	if icprm_spot_color == BRIGHT:
		icono.SnakeSetColorBackground( DARK )
	else:
		icono.SnakeSetColorBackground( BRIGHT )
	icono.SnakeSetSigmaConstraint( 0.2 )

#first determine the reference system and outer spots
image = images[-1]
CCT.CommitImages( image )
ref_id = processor.ProcessRefImage( image ) 
CCT.RunAlignment( img = image, mode = 0, 
			param = { "Transformation": ( ref_mode, ( 0.05, ), 
							{	"image_ref": ref_id,
								"mode_law": 5 | 256 | 512, 
								"trans_opt": ( 0.1, 0.05, 0.2, 0.2, 0.2, 1.0, 1.0 ), 
								"param_opt": ( 25.0, 0.8, 5000.0, 5000.0, 0.0, 0.0005, 0.0, 0.01 ),
								"trans_sub_opt": ( 0.0, 0.0, 0.0, 5.0, 5.0 ),
								"param_sub_opt": ( 500.0, 4.0, 20.0, 40.0, 10.0, 0.0005 ),
								"weight_probes": 0.0
							}
						    )
				 } ) 

if mode == 2 and icprm_spot_color == BRIGHT:		#model-based
	icono.InvertImage( image, image )
try:
	#now determine the spots
	img_id = processor.ProcessImage( image ) 
	CCT.RunAlignment( img = img_id, trans = 0, mode = mode,
			    param = { "Thresholding": ( 2, icprm_spot_model ),
					"Segmentation": ( 0, ( 200.0, 0.3, 2500.0, 2500.0, 2.0, 0.00001, 0.0, 0.001 ) ) }  )
finally:
	if mode == 2 and icprm_spot_color == BRIGHT:	#model-based
		icono.InvertImage( image, image )

share = 1.0 / len( images ) 
share_update = 0.0
for image in images:
	CCT.CommitImages( image )

	feat_back = CCT.DetermineFeatures( image, ( "Mean", ),
						spot_mode = REGION_BACK | REGION_HIST,
						spot_param = ( 3, 0, 0, 1, 0 ),
						hist_param = icprm_hist_back )
	feat_spot = CCT.DetermineFeatures( image, ( "Mean", "Sigma", "CoG_x", "CoG_y" ),
						spot_mode = REGION_SPOT | REGION_HIST,
						hist_param = icprm_hist_spot )
	feat_spot["Background"] = feat_back["Mean"]

	len_feat = len( feat_spot["Mean"] )
	
	if icprm_sub_back == 1:
		# additive model
		if icprm_spot_color == BRIGHT: 
			feat_spot["Signal"] = [ feat_spot["Mean"][i] - feat_back["Mean"][i] for i in xrange( len_feat ) ]
		else:	
			feat_spot["Signal"] = [ feat_back["Mean"][i] - feat_spot["Mean"][i] for i in xrange( len_feat ) ]
	elif icprm_sub_back == 2:
		# multiplicative model
		signal = []
		if icprm_spot_color == BRIGHT: 
			for i in xrange( len_feat ):
				try:
					signal.append( ( feat_spot["Mean"][i] - feat_back["Mean"][i] ) / ( 1.0 - feat_back["Mean"][i] ) )
				except:
					signal.append( 0.0 )
		else:	
			for i in xrange( len_feat ):
				try:
					signal.append( 1.0 - feat_spot["Mean"][i] / feat_back["Mean"][i] )
				except:
					signal.append( 0.0 )
		feat_spot["Signal"] = signal
	
	CCT.features = feat_spot

	CCT.listFeatures.append( feat_spot )
		
	share_update += share
	if CCT.vb_control:
		CCT.vb_control.UpdateProgress( share_update )

CCT.rawResultType = "ic [MeanBG]"

# set featureMap for Partisan
import ODBC2Magasin
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Mean", "value", "norm" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Signal", "value2", "norm" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Background", "local_backgrd", "norm" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Sigma", "sigma_1", "norm" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Valid", "flags", "norm" )

ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Spot ID", "Spot_ID", "raw" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Valid", "Flags", "raw" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Cog_x", "COG_x", "raw" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Cog_y", "COG_y", "raw" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Mean", "Mean", "raw" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Background", "Background", "raw" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Signal", "Signal", "raw" )
ODBC2Magasin.AppendTypedFeatureMap( CCT.rawResultType, "Sigma", "Sigma", "raw" )
