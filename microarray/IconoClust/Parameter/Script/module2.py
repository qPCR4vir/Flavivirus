
>> Help CCT:
>> Help on RunTimeEnviron in module Environ object:

class RunTimeEnviron(BaseEnviron.BaseServerEnviron, BaseEnviron.RunEnviron)
An Instance of this will be the Object dealing with the Parameters of the
Image Processing Algorithms

Method resolution order:
    RunTimeEnviron
    BaseEnviron.BaseServerEnviron
    BaseEnviron.RunEnviron
    BaseEnviron.ParamEnviron
    BaseEnviron.BaseEnviron
    __builtin__.object

Methods defined here:

AlignLayout(self, *args, **kwargs)

AttachControl(self, *args, **kwargs)

CheckValidity(self, *args, **kwargs)

CheckXML = WrapEnv__(self, *args, **kwargs)

ClearParameter(self, *args, **kwargs)

CommitImages(self, *args, **kwargs)

CreateImageParameterFile(self, *args, **kwargs)

CreateParameterFile = WrapEnv__(self, *args, **kwargs)

DeleteCalibration = WrapEnv__(self, *args, **kwargs)

DeleteEmptyImageParam = WrapEnv__(self, *args, **kwargs)

DeleteTemp = WrapEnv__(self, *args, **kwargs)

DetermineCalibration = WrapEnv__(self, *args, **kwargs)

DetermineFeatures(self, *args, **kwargs)

DetermineImageFeatures = WrapEnv__(self, *args, **kwargs)

ExportData = WrapEnv__(self, *args, **kwargs)

GetAlignedSpots = WrapEnv__(self, *args, **kwargs)

GetExportDataFile = WrapEnv__(self, *args, **kwargs)

GetFeatures(self, *args, **kwargs)

GetFeaturesID = WrapEnv__(self, *args, **kwargs)

GetGlobFeatures = WrapEnv__(self, *args, **kwargs)

GetImageOverlay(self, *args, **kwargs)

GetImageSeries = WrapEnv__(self, *args, **kwargs)

GetImgFeatures = WrapEnv__(self, *args, **kwargs)

GetKeepROI(self, *args, **kwargs)

GetListFeatures = WrapEnv__(self, *args, **kwargs)

GetParameterFile(self, *args, **kwargs)

GetProcessCancel(self)
    Check if cancel flag in application set
    
    :return:    
            1 if cancel request, 
            0 if no cancel request

GetRawFeatures(self)
    Get self.features
    
    :return:    
            self.features { feat_name: [spot 1, spot 2, ...], ... }

GetRefPoints(self, *args, **kwargs)

GetReferenceSystem = WrapEnv__(self, *args, **kwargs)

GetScript(self, *args, **kwargs)

GetScriptParameter(self, *args, **kwargs)

GetSegImage = WrapEnv__(self, *args, **kwargs)

GetSpecialFeatures = WrapEnv__(self, *args, **kwargs)

GetSpecialGlobFeatures = WrapEnv__(self, *args, **kwargs)

GetSpecialImgFeatures = WrapEnv__(self, *args, **kwargs)

GetSpecialListFeatures = WrapEnv__(self, *args, **kwargs)

GetSpotID(self, *args, **kwargs)

GetSpotNr(self, *args, **kwargs)

InfoDB = WrapEnv__(self, *args, **kwargs)

ParameterDB(self, res_type='', feat_map={}, cmds=None)
    Set database parameter
    
    :param res_type:    
            Result type, e.g. "iconoclust"
    :param feat_map:
            e.g. 
            { 
            "norm":  
            {  
            "SPOT_ID":          "spot id",
            "VALUE":            "mean",
            "VALUE2":           "signal",
            "LOCAL_BACKGRD":    "background",
            "SIGMA_1":          "sigma",
            "FLAGS":            "valid",
            "QUALITY":          "confidence",
            },
            "raw":   
            {  
            "SPOT_ID":          "spot id",
            "MEAN":             "mean",
            "SIGNAL":           "signal",
            "BACKGROUND":       "background",
            "SIGMA":            "sigma",
            "FLAGS":            "valid",
            "COG_X":            "cog_x",
            "COG_Y":            "cog_y",     
            },
            "channel":  
            {
            "V01":              "Area",
            "V02":              "Mean",
            },
            }
    :param cmds:    
        List with ( command, args ) tuples 
            command to execute on XML-RPC server (see SQLCode.py), 
            e.g. "ExpGetScript",
            args is dictionary with parameters matching command (see SQLCode.py), 
            e.g. { "__EXP_ID__": id_exp }

PrintText = WrapEnv__(self, *args, **kwargs)

ResetFeatures(self, *args, **kwargs)

RestoreGlobals = WrapEnv__(self, *args, **kwargs)

RunAlignment(self, *args, **kwargs)

RunAll(self, *args, **kwargs)

RunProcess(self, *args, **kwargs)

SaveDB = WrapEnv__(self, *args, **kwargs)

SaveFeatures = WrapEnv__(self, *args, **kwargs)

SaveImageInfo = WrapEnv__(self, *args, **kwargs)

SaveParameter = WrapEnv__(self, *args, **kwargs)

SaveSegImage = WrapEnv__(self, *args, **kwargs)

SetDB = WrapEnv__(self, *args, **kwargs)

SetDefaultParameterFile(self, *args, **kwargs)

SetFeaturePrecision(self, feat, prec, feat_type='spot')
    Set precision for string conversion of given feature
    
    :param feat:    
            Feature name
    :param prec:    
            Places after comma when converting to string

SetImageOverlay = WrapEnv__(self, *args, **kwargs)

SetKeepROI(self, *args, **kwargs)

SetParameter(self, *args, **kwargs)

SetPresentation(self, obj)
    Set presentation object
    
    :param obj:     
            Presentation object

SetRefPoints(self, *args, **kwargs)

SetReferenceSystem = WrapEnv__(self, *args, **kwargs)

SetValidity = WrapEnv__(self, *args, **kwargs)

SetVisualMode(self, *args, **kwargs)

StartCalibration(self)
    Get Transformation from calibration data
    
    :return:        
            Dictionary with Transformation
            {
            "Shift( x )":     shift_x,
            "Shift( y )":     shift_y,
            "ShiftRef( x )":  shiftref_x,
            "ShiftRef( y )":  shiftref_y,
            "Scale( x )":     scale_x,
            "Scale( y )":     scale_y,
            "Rotation":       rotation,
            "Mirror":         mirror,
            }

StartReferenceSystem = WrapEnv__(self, *args, **kwargs)

StartTransformation(self, trans_offset={'Mirror': 0, 'Rotation': 0.0, 'Scale( x )': 1.0, 'Scale( y )': 1.0, 'Shift( x )': 0.0, 'Shift( y )': 0.0, 'ShiftRef( x )': 0.0, 'ShiftRef( y )': 0.0})
    Determine Transformation from calibration data
    
    :param trans_offset:    
            Transformation will be be offset by this
    :return:                
            Dictionary with Transformation
            {
            "Shift( x )":     shift_x,
            "Shift( y )":     shift_y,
            "ShiftRef( x )":  shiftref_x,
            "ShiftRef( y )":  shiftref_y,
            "Scale( x )":     scale_x,
            "Scale( y )":     scale_y,
            "Rotation":       rotation,
            "Mirror":         mirror, 
            }

TestFeatures(self, *args, **kwargs)

TransformPoints(self, points)
    Transforms layout coordinates to image coordinates
    
    :param points:      
            Dictionary 
            { 
            "x_pos": [x_pos 1, x_pos 2, ...], 
            "y_pos": [y_pos 1, y_pos 2, ...], 
            "spot_id": [id 1, id 2, ...], 
            }
    :return:            
            List [(x_img, y_img, spot_id), ...]

TransformRef(self, trans)
    Transform reference system according to transform and return transformed reference points
    
    :param trans:   
            Transformation 
            { 
            "Shift( x )":     shift_x,
            "Shift( y )":     shift_y,
            "ShiftRef( x )":  shiftref_x,
            "ShiftRef( y )":  shiftref_y,
            "Scale( x )":     scale_x,
            "Scale( y )":     scale_y,
            "Rotation":       rotation,
            "Mirror":         mirror, 
            }
    :return:        
            Transformed Points 
            { 
            "x_pos": [x_pos 1, x_pos 2, ...], 
            "y_pos": [y_pos 1, y_pos 2, ...], 
            "x_dim": [x_dim 1, x_dim 2, ...], 
            "y_dim": [y_dim 1, y_dim 2, ...], 
            "shape": [shape 1, shape 2, ...], 
            "spot_id": [id 1, id 2, ...], 
            }

UpdateProgress(self, val, force=0)
    Call UpdateProgress in attached frmMain object
    
    :param val:     
            Progress value in <0.0, 1.0>
    :param force:   
            Update progress even if application is not active if set

__del__(self)
    Delete RunTimeEnviron instance
    Delete temporary files created for instance

__init__(self)
    Initialize RunTimeEnviron instance

getResultType(self)

setResultType(self, res_type)

----------------------------------------------------------------------
Data descriptors defined here:

rawResultType

----------------------------------------------------------------------
Data and other attributes defined here:

pythoncom = <module 'pythoncom' from 'C:\Program Files (x86)\Icono\pyt...

----------------------------------------------------------------------
Methods inherited from BaseEnviron.BaseServerEnviron:

GetObject(self, *args, **kwargs)

SetObject = WrapEnv__(self, *args, **kwargs)

----------------------------------------------------------------------
Methods inherited from BaseEnviron.RunEnviron:

CommitParameter(self, *args, **kwargs)

DefaultAlgoParameter(self)
    Set default parameter in imaging library (icono)

FreeImages(self, *args, **kwargs)

GetProcessParameter = WrapEnv__(self, *args, **kwargs)

RecallParameter = WrapEnv__(self, *args, **kwargs)

SetForceCommit(self, *args, **kwargs)

TestProcess(self, *args, **kwargs)

----------------------------------------------------------------------
Methods inherited from BaseEnviron.ParamEnviron:

AddImages(self, *args, **kwargs)

CheckParameter(self, *args, **kwargs)

CheckTemp(self, name)
    Check if file is a temporary one
    
    :param name:    
            File name to check
    :return:        
            1 if temporary, 0 otherwise

DeleteImages(self, *args, **kwargs)

DeleteParameter = WrapEnv__(self, *args, **kwargs)

DeleteParameterType = WrapEnv__(self, *args, **kwargs)

EditScript(self, *args, **kwargs)

EditScriptParameter = WrapEnv__(self, *args, **kwargs)

ExtractFeatures(self, features)
    Extract list features from feature lists - key feature is i_order -> defines lists
    Capitalizes feature names, spot_id -> Spot ID
    Convert to floats if possible
    Suppress i_order and image_name
    
    :param features:    
            Dictionary 
            { 
            "i_order": [ 1, 1, 1, 2, ..., i, i, i ], 
            "mean": [ mean11, mean12, mean13, mean21, ..., meani3 ], ... 
            }
    :return:
            List of dictionaries
            [
            { "Mean": [ mean11, mean12, mean13 ], ... }, 
            { "Mean": [ mean21, mean22, mean23 ], ... }, ...
            { "Mean": [ meani1, meani2, meani3 ], ... }
            ]

FormatFeatures(self, features, mode='spot')
    Lower feature names, Spot ID -> spot_id
    Convert to strings
    
    :param features:    
            Dictionary { feat1: [ spot1, ..., spotn ], feat2: [ spot1, ..., spotn ], ... }
    :param mode:        
            "spot" or "image"

GetChanged(self, *args, **kwargs)

GetCurrentImage(self, *args, **kwargs)

GetExpID(self, *args, **kwargs)

GetImageAttrib(self, *args, **kwargs)

GetImageBitdepth = WrapEnv__(self, *args, **kwargs)

GetImageID(self, *args, **kwargs)

GetImageName(self, *args, **kwargs)

GetImageNr = WrapEnv__(self, *args, **kwargs)

GetImages(self, *args, **kwargs)

GetParameter(self, *args, **kwargs)

GetParameterGroup = WrapEnv__(self, *args, **kwargs)

GetParameterType(self, *args, **kwargs)

GetParameters(self, *args, **kwargs)

GetSortedImageIDs(self, *args, **kwargs)

GetSources = WrapEnv__(self, *args, **kwargs)

GetTempDir(self, *args, **kwargs)

GetTemplate = WrapEnv__(self, *args, **kwargs)

Login(self, *args, **kwargs)

MakeTemp(self, suffix='', dir='')
    Create temporary file in self.tempDir
    
    :param suffix:      
            Suffix for file (usually file ending, e.g. ".png")
    :param dir:         
            Relative directory path, use environment temp directory if not set

NormalizeFeatures(self, features)
    Capitalizes feature names, spot_id -> Spot ID
    Convert to floats if possible
    
    :param features:    
            Dictionary { "feat1": [ spot1, ..., spotn ], "feat2": [ spot1, ..., spotn ], ... }
    :return:
            Dictionary { "Feat1": [ spot1, ..., spotn ], "Feat2": [ spot1, ..., spotn ], ... }

PopExperiment = WrapEnv__(self, *args, **kwargs)

PushExperiment = WrapEnv__(self, *args, **kwargs)

ResetImages(self, *args, **kwargs)

ResetParameter(self, *args, **kwargs)

SaveParameterSingle(self, *args, **kwargs)

SaveTemplate = WrapEnv__(self, *args, **kwargs)

SetBitDepth = WrapEnv__(self, *args, **kwargs)

SetCalibration(self, *args, **kwargs)

SetChanged(self, *args, **kwargs)

SetCurrentImage(self, *args, **kwargs)

SetDefaultDir = WrapEnv__(self, *args, **kwargs)

SetExpID(self, *args, **kwargs)

SetImageAttrib(self, *args, **kwargs)

SetImageSeries = WrapEnv__(self, *args, **kwargs)

SetInteractRef(self, *args, **kwargs)

SetParameterReference(self, list_param)
    Set Parameter Reference to an already existing Parameter object
    
    :param list_param:  
            List of ( param_name, param_object ) - tuples

SetParameterSingle(self, *args, **kwargs)

SetParameterType(self, *args, **kwargs)

SetTempDir = WrapEnv__(self, *args, **kwargs)

SetTemplate(self, *args, **kwargs)

delCode(self)

getCode(self)

setCode(self, code)

----------------------------------------------------------------------
Data descriptors inherited from BaseEnviron.ParamEnviron:

code

----------------------------------------------------------------------
Data and other attributes inherited from BaseEnviron.ParamEnviron:

environCount = 43

----------------------------------------------------------------------
Methods inherited from BaseEnviron.BaseEnviron:

DetectStatus(self, e)
    Gets the error status and level out of the exception class and returns these
    
    :param e:       
            Exception instance
    :return:        
            Tuple (Error classification, Error level)

GetStatus(self)
    Get environment status
    Do not wrap with HandleExcept -> get status of "GetStatus"-call otherwise
    
    :return:        
            Environment status

GetTrace(self)
    Get last traceback
    Do not wrap with HandleExcept -> get status of "GetTrace"-call otherwise
    
    :return:        
            Traceback

GetVariable = WrapEnv__(self, *args, **kwargs)

GetVersion(self)
    Get IconoClust version
    
    :return:    
            Version string, e.g. "3.4r1"

ResetStatus(self)
    Reset environment status

SetExceptReturn(self, except_class)
    Set exception class - raised when exception in class method
    
    :param except_class:    
            Exception class to raise

SetStatus(self, status)
    Set environment status
    
    :param status:      
            Status to set, usually tuple (status text or exception, status code)

SetVariable = WrapEnv__(self, *args, **kwargs)

SetVerbosity(self, verbose=0)
    Set verbosity level
    
    :param verbose:     
            Verbosity level - the higher the more output

----------------------------------------------------------------------
Data descriptors inherited from BaseEnviron.BaseEnviron:

__dict__
    dictionary for instance variables (if defined)

__weakref__
    list of weak references to the object (if defined)
