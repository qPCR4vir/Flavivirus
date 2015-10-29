CCT._Description = {
"Author" : 	"Clondiag Chip Technologies",
"Target" : 	"Creates Layout Parameter Files",
"Description" : 	'''
		Creates Parameter files from abstract array id.
		''',
"Parameter" : 	'''
		''',
"Version" : 	"3.5r1",
}

__ICPRM__ = {}

import Database
import ExtractLayout
import EasyDialogs

from win32com.client import Dispatch
dialog = Dispatch( "IconoUtil.Util" )
res = dialog.Authorization()
user, pwd = res[:2]

array_id = EasyDialogs.AskString( "Give the Abstract Array ID" )
if not array_id:
	raise ErrorException( "No Array ID given!" )

param_path = os.path.join( ParamGlobals.GetIconoPath(), "Parameter" )

comm = Database.Communicator()
connect = [ None, "", "", user, pwd ]
comm.connect( connect )
sources = ExtractLayout.CreateParamFromArray( array_id, comm, param_path, 
							param = ( 	"array_layout",
									"a_probe_on_array",
									"h_ref_pos_sys" ) )

param_list = sources.items()
CCT.SetParameterSingle( param_list )
for name in ( "array_layout", "a_probe_on_array", "h_ref_pos_sys" ):
	CCT.vb_control.LoadParameterInTree( sources[name], name )
