#<?xml version='1.0' encoding='ISO-8859-1'?>
#<PROCESS owner="" password="d41d8cd98f00b204e9800998ecf8427e" script="
CCT._Description = {
    'Author' : 	'Clondiag Chip Technologies',
    'Target' : 	'Processing of Standard Array Tube Experiments',
    'Description' : 	'''
		    Script processes last image in experiment.
		    The Results are graphed in a special Presentation Component.
		    Model-based Segmentation is optional.
		    Automatic Reference System Recognition is optional.
		    Results can be normalized by named substance value.''',
    'Parameter' : 	'''
		    icprm_spot_color:		DARK or BRIGHT
		    icprm_mode:		0 for fixed segmentation according to layout
					    1 for Model-based Segmentation
		    icprm_ref_mode:		MANUAL for manual setting of Reference Points
					    AUTO for Automatic Reference System Detection
					    AUTO_CHROME for Automatic Chrome Reference System Detection
		    icprm_silent:		0 for enabling user interaction
					    1 for suppressing user interaction
		    icprm_subst_norm:	Name of normalizing substance
					    If empty the name will be entered in a dialog
		    icprm_conf_ind:		determine Confidence Index (CI)
					    A spot is set invalid if CI < 0.75 and Signal > 0.1
		    icprm_signal:		0 for Signal = Local Background - Mean              [Bkg_Mean]
					    1 for Signal = 1 - Mean / Local Background (only allowed for colorimetric detection)   [One_MeanDivBkg]

		    icprm_save_segimage:	GENERIC_NAME

		    ''',


    'Version' : 	'3.1r2',
    'ScriptVersion' : '2014-06-11'
}

print '---  Script adapted  by Ariel Vina Rodriguez !!!!!!!!!!   '
print 'Signal changed from 1 to 0 ?? 1: = 1 - Mean / Local Background '
print ' or to 0:  = Local Background - Mean '

BRIGHT = 1     	# color
DARK = 2

MANUAL = 0		# Reference mode
AUTO = 1
AUTO_CHROME = 2

Bkg_Mean = 0		# Signal
One_MeanDivBkg = 1

Not_SILENT = False	# user interaction
SILENT = True

__ICPRM__ = { 'icprm_spot_color':	DARK,	
		'icprm_mode': 		'1',
		'icprm_ref_mode':	AUTO_CHROME,
		'icprm_silent':		True,
		'icprm_subst_norm':	'""',	
		'icprm_conf_ind':		'1',	
		'icprm_signal':		One_MeanDivBkg,
		'icprm_save_segimage':	False,
		}

__SpotAligning = 1


		#TOM:PROFILING block start
import time
tStart = time.time()
		#TOM:PROFILING block end 

import win32gui

images = CCT.GetSortedImageIDs()
curr_image = CCT.GetCurrentImage()


if __ICPRM__.icprm_mode:		 # ??? just elimine 1 (AUTO)
	mode = AUTO_CHROME    #2
else:
	mode = MANUAL         #0


	# only allow model-based segmentation or fixed ROI
__ICPRM__.ref_mode = __ICPRM__.icprm_ref_mode

	# the equation 1 - Mean / BG is only allowed for colorimetric detection
if ( __ICPRM__.icprm_spot_color == BRIGHT ) and ( __ICPRM__.  icprm_signal == One_MeanDivBkg ):
	verified_icprm_signal = Bkg_Mean
else:
	verified_icprm_signal = icprm_signal

import ATProcess

img_supp = ImageSupport.ImageSupport()
	
if icprm_conf_ind == 1:
		import Confidence
	
if icprm_spot_color == BRIGHT:
		hist_par_spot = ( 0.7, 1.0 )
		hist_par_back = ( 0.0, 0.3 )
else:
		hist_par_back = ( 0.7, 1.0 )
		hist_par_spot = ( 0.0, 0.3 )
	
for curr_image in images:
	__SpotAligning = 1

		# use last image --- for what?? align only? for Reference ?!
	image = curr_image  # images[-1]
	CCT.CommitImages( image )
	size = img_supp.GetPictureDimensions( image )
	img_supp.SetWindow( ( 5, 5, size[0] - 6, size[1] - 6 ), image )
	print '---  Reference (last) picture commited'
	
	if ref_mode:		# not MANUAL ?!
		if icprm_spot_color == BRIGHT:
			icono.SnakeSetColorBackground( DARK )
		else:
			icono.SnakeSetColorBackground( BRIGHT )
		if ref_mode == AUTO:
			icono.SnakeSetInvalidTestScene( 2 )
			icono.SnakeSetAllowedInvalidTestScene( 0.0 )
			processor = ATProcess.Processor( mode, 1 )
			  # criterion is maximum contrast, consider homogenity, favour larger scale
			mode_law = 5 | 256 | 512
			icono.SnakeSetSigmaConstraint( 0.2 )
		elif ref_mode == AUTO_CHROME:
			  # do not preprocess image for ref detection
			processor = ATProcess.Processor( mode, 0 )
			  # criterion is mean extremum, do not consider homogenity, do not favour any scale
			mode_law = 8
			icono.SnakeSetSigmaConstraint( 1.0 )
			  #icono.SnakeSetShowRng( 1 )
		ref_id = processor.ProcessRefImage( image ) 
		ref_param = { 'image_ref': ref_id,
			       'mode_law': mode_law,
			       'trans_opt': ( 0.05, 0.03, 0.15, 0.14, 0.14, 1.0, 1.0 ),
			       'param_opt': ( 25.0, 0.8, 5000.0, 5000.0, 0.0, 0.0005, 0.0, 0.01 ),
			       'weight_probes': 0.0
			    } 
		ref_auto = 1
		print '---  Processed RefImage'
	else:
		processor = ATProcess.Processor( mode, 0 )
		ref_param = {}
		ref_auto = 0
	
		#first determine the reference system and outer spots
	CCT.RunAlignment( img = image, mode = 0, 
		    param = { 'Transformation': ( ref_auto, ( 0.05, ), ref_param ) } )
	
	print '---  Aligned RefImage'
	
	if mode == AUTO_CHROME and icprm_spot_color == BRIGHT:		# model-based : our case!
		icono.InvertImage( image, image )
		print '---  Inverted RefImage'
	
	
	parameter = { 'Thresholding': ( 4, ( 0.7, 0.0, 0.0, 0.2, 0.2, 1.0, 1.0 ) ),
			'Segmentation': ( 0, ( 200.0, 0.3, 2500.0, 2500.0, 1.0, 0.00001, 0.0, 0.001 ) ) }
	
	if icprm_conf_ind != 1:
		# wird bei Confidence nochmal mit parameter ausgefuehrt
		try:
			#now determine the spots
			img_id = processor.ProcessImage( image ) 
			CCT.RunAlignment( img = img_id, trans = 0, mode = mode, callSource = CODE,
					    param = parameter )
		finally:
			if mode == AUTO_CHROME and icprm_spot_color == BRIGHT:		#model-based
				icono.InvertImage( image, image )
	
	if CCT.vb_control:
		CCT.vb_control.SetModeShowROI( 'ROI_FILLED' )
		CCT.vb_control.SetOpacityShowROI( 20 )
		print 'CCT.vb_control true'
		print CCT.vb_control #.toString()
	
	
		#TOM:PROFILING block start
	print 'SpotAligning:: ENDE', time.time() - tStart
		#TOM:PROFILING block end 
	
	
	__SpotAligning = 0
	
	__DetFeatures = 1
	
	print 	'after cycle: __SpotAligning=', __SpotAligning, ' ; __DetFeatures=',__DetFeatures  

	
	image = curr_image  # CCT.GetCurrentImage()
	
	if icprm_conf_ind == 1:
		img_id = processor.ProcessImage( image )
		checker = Confidence.ConfidenceChecker( img_id, image, colour = icprm_spot_color )
		checker.SetEnviron( CCT )
		ci_results = checker.Check( parameter, set = { 'bg': { 'on': 0 } }, signal = verified_icprm_signal )
	
	
		#TOM:PROFILING block start
	print 'After Confidence', time.time() - tStart	# cprm_ darf nich clartext in string
		#TOM:PROFILING block end 
	
	
	back_hist = CCT.DetermineFeatures( image,  ( 'Mean',  ),
						    REGION_BACK|REGION_HIST, ( 3.0, -3.0, 0.0, 1.0, 0.0 ),
						    hist_param = hist_par_back )
	print ' --- back_hist DetermineFeatures Mean'
	
	CCT.DetermineFeatures( image, ( 'Mean',  ), REGION_HIST, hist_param =  hist_par_spot )
	print ' ---   DetermineFeatures Mean'
	
	len_list = len(CCT.features['Mean'])
	
	
	if icprm_spot_color == DARK:
		if verified_icprm_signal == Bkg_Mean:
			CCT.features['Signal'] = [( back_hist['Mean'][i] - CCT.features['Mean'][i] ) for i in xrange( len_list ) ]
	
		elif verified_icprm_signal == One_MeanDivBkg:
			CCT.features['Signal'] = [0 for i in xrange( len_list ) ]
			for i in xrange( len_list ):
				try:
					CCT.features['Signal'][i] = 241.0 / 256.0 * ( 1 - CCT.features['Mean'][i] / back_hist['Mean'][i] )
				except:
					pass
	elif icprm_spot_color == BRIGHT:
		if verified_icprm_signal == Bkg_Mean:
			CCT.features['Signal'] = [( CCT.features['Mean'][i] - back_hist['Mean'][i]) for i in xrange( len_list ) ]
	
	print ' ---   Signals calculated'
	
	CCT.features['Background'] = [back_hist['Mean'][i] for i in xrange( len_list ) ]
	print ' ---   Backgrounds calculated'
	
	if icprm_conf_ind == One_MeanDivBkg:
		for ci_key, ci_list in ci_results.iteritems():
			CCT.features[ci_key] = [ci_list[i] for i in xrange( len( ci_list ) ) ]
	
	valid = CCT.features['Valid']         # --------   Seted: CCT.features['Valid']
	
		#TOM:PROFILING block start
	print 'Vor Seg Img', time.time() - tStart
		#TOM:PROFILING block end 
	
	
	#---------------------------------------------------------------
	# save segmentation image 
	#---------------------------------------------------------------
	try:
		seg_name = CCT.segImageName
	except:
		seg_name = ''
	if icprm_save_segimage == 2:
		seg_name = CCT.GetImageName(image) #+ name noch bearbeiten
	
	if seg_name:
		ic_img_path = seg_name + '.png' 
		print 'save segmentation image to', ic_img_path
		CCT.SaveSegImage( ic_img_path, mode = ImageSupport.CCT_ROI, opac = 1.0, add_valid = 1 )
	
	#-----------------------------------------------------------------------------
	print 'After Seg Img', time.time() - tStart
	
	
	
	if CCT.vb_control:
		CCT.vb_control.ShowResults( 1 )
		print ' ---  Results showed'
		if not icprm_silent:
			answer = win32gui.MessageBox( 0, 'You can set invalid Spots now.' + chr( 13 ) + \
				'Press "Ok" if you are done.', 'Spot Validity', 5168 )
			valid = CCT.vb_control.GetValidity() # Reset manualy: CCT.features['Valid']
			CCT.features['Valid'] = valid
	
	valid_indx = []
	for i in xrange( len( valid ) ):
		if valid[i] == 0:
			valid_indx.append( i ) 
	
	
	if not CCT.features.has_key( 'Substance' ):
		raise KeyError, 'You have to include Spot Descriptions into your Experiment'
	print '---- After Substance...'
	CCT.featSubst = []
	for subst in CCT.features['Substance']:
		try:
			pos = CCT.featSubst.index( subst )
		except:
			CCT.featSubst.append( subst )
	print '---- After Substance 2...'
	
	CCT.featSubst.sort()
	
	normSubst = 'Biotin-Marke_2,5µM'   # = ''
	if not icprm_subst_norm:
		if not icprm_silent:
			# create dialog and ask for normalizing substance.  I need this ???
			from win32com.client import Dispatch
			util = Dispatch( 'IconoUtil.Util' )
			normSubst = util.ListSelectEx( 'Normalizing Substance', 'Select name of normalizing substance', 'Select', CCT.featSubst[:], 'norm_subst' )
			normSubst = normSubst.strip()
	
	CCT.features['Valid'] = valid

	if normSubst:
		# normalize features
		feat_norm = ( 'Signal',)# 'Mean', 'Background', )
		normFeat = {}
		nFeatMax = {}
		for feat in feat_norm:
			normFeat[feat] = 0.0
			nFeatMax[feat] = 0.0
		norm_count = 0
		for i in xrange( len( CCT.features['Substance'] ) ):
			if valid[i]:
				continue
			subst = CCT.features['Substance'][i]
			if subst != normSubst:
				for feat in feat_norm:				#new
					if nFeatMax[feat]<CCT.features[feat][i]:	#new
						nFeatMax[feat]=CCT.features[feat][i]	#new
				continue
			norm_count += 1
			for feat in feat_norm:
				normFeat[feat] += CCT.features[feat][i]
		if not norm_count:
			raise ValueError( 'Cannot normalize - no valid spot for substance' )
		for feat in feat_norm:
			if normFeat[feat]:
				normFeat[feat] /= norm_count
				if normFeat[feat]*0.2>nFeatMax[feat]:
					nFeatMax[feat]=normFeat[feat] 
				#CCT.features[feat] = [ val / normFeat[feat] for val in CCT.features[feat] ]
				CCT.features[feat] = [ val / nFeatMax[feat] for val in CCT.features[feat] ]
	
	print ' ---- Normalized ...'
	if False: #not CCT.sources.has_key( 'subst_match' ):    ???????????
		print ' have to create file with all the substances without any relations'
		# name it after the a_probe_on_array file 
		name_match = os.path.basename( CCT.sources['a_probe_on_array'] )
		name_match = os.path.splitext( name_match )[0] + '.txt'
		name_match = os.path.join( ParamGlobals.GetIconoPath(), 'Parameter', 'Layout', 'Substance', name_match ) 
		cont_match = 'Match\tSubstance\n'
		subst_in = []
		for subst in CCT.features['Substance']:
			if not subst in subst_in:
				cont_match += subst + '\t' + subst + '\n'
				subst_in.append( subst )
		print '--- Creating file ', name_match  
		#f = open( name_match, 'w' )
		#f.write( cont_match )
		#f.close()
		import Excel2XMLSubstance
		conv = Excel2XMLSubstance.xl2XML()
		conv.ImportText( name_match )
		name_match = conv.Create()
		CCT.SetParameterSingle( [ ( 'subst_match', name_match ), ] )

	# create a dictionary with key value pair: substancename, value
	# presentation only creates the mean of the values per substance
	subst_list = CCT.features['Substance']
	SigMeans = {}
	for subst in subst_list:
		SigMeans[ subst ] = []
	for idx in valid_indx:
		SigMeans[ subst_list[idx] ].append( CCT.features['Signal'][idx] ) 

	print '---- SigMeans created'
	sig = [ len(SigMeans[ subst ]) and 
               sum(SigMeans[ subst ])/len(SigMeans[ subst ]) for subst  in subst_list  ]
	print '---- SigMeans created 2'

	CCT.validFeat = { 	'Signal': 	sig,
				'Valid':		[ 0.0 for s  in subst_list  ],
				'Substance':	[ s for s  in subst_list  ] }
	print '--- valid feat calculed'
	
	if CCT.vb_control:
		import PresentEnvironAT
		CCT.PresentAT = PresentEnvironAT.PresentEnviron()
		CCT.PresentAT.SetSignalFeature( 'Signal' )
		CCT.PresentAT.SetEnviron( CCT, [ CCT.validFeat, ] )
		CCT.PresentAT.SetMode( nr_img = 0, show_img = PresentEnvironAT.ENDPOINT )
		CCT.vb_control.SetPresentation( 'PresentAT' )
	
	if verified_icprm_signal == 1:
		CCT.rawResultType = 'ic [1MeanBG]'
	elif verified_icprm_signal == 0:
		CCT.rawResultType = 'ic [MeanBG]'
	
	# make available parameter
	CCT.paramProcessing = {}
	if seg_name:
		CCT.paramProcessing['segPath'] = seg_name
	
	#TOM:PROFILING block start
	print 'Ende script', time.time() - tStart
	#TOM:PROFILING block end 
	
	__DetFeatures = 0
	
" />