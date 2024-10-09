# By Abhay Nathani: https://github.com/AbhayNathani
# Blog Site Abhi's Lab: https://abhislab.in
# Use Microstrip Line Calculator @ https://https://abhislab.in/abhis-lab-microstrip-line-calculator/
# Enjoy! Happy Tinkering and Happy Learning
#######################################################################

NEW_DESIGN_NAME = "QUATERWAVE_TRANSFORMER_IMPEDENCE_MATCHING_75_to_200" 

# PORT 1
PORT_1_IMPEDENCE = 75 #unit ohm (number)
PORT1_X_LENGTH = "10mm"
PORT1_Y_WIDTH = "1.428mm"

# PORT 2
PORT_2_IMPEDENCE = 200 #unit ohm (number)
PORT2_X_LENGTH = "10mm"
PORT2_Y_WIDTH = "0.046mm"

# 1/4 Wave Transformer
TRANSFORMER_X_LENGTH = "8.7mm" #1/4 wave length or 90degree
TRANSFORMER_Y_WIDTH = "0.380mm"

# SUBSTRATE Protperties
SUBSTRATE_Y_WIDTH = "60mm"
SUBSTRATE_Z_HEIGHT = "1.6mm"
SUBSTRATE_MATERIAL = "\"FR4_epoxy\""

### ANALYTICS VARIABLES ### 
FREQUENCY = 6 # (GHz)
MAXIMUM_PASSES = 6
# SWEEP - Enter Frequency Range (Ghz)
RANGE_START = 0.1 # (GHz)
RANGE_END = 10# (GHz)
POINTS = 501

# True if you want to Run Analysis and Generate S11 and S21 Plots
ANALYZE_ALL_AND_GENERATE_S_PLOT = True





###############################################################################
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()

oProject = oDesktop.NewProject()
oProject.InsertDesign("HFSS", NEW_DESIGN_NAME, "HFSS Terminal Network", "")
# oProject = oDesktop.SetActiveProject("Project2")
oDesign = oProject.SetActiveDesign(NEW_DESIGN_NAME)
oEditor = oDesign.SetActiveEditor("3D Modeler")
def message(msg,sev=4): #prints global message
	oDesktop.AddMessage(oProject.GetName(), oDesign.GetName(), sev, msg)

# Set model units to millimeters (mm)
oEditor.SetModelUnits(
	[
		"NAME:Units Parameter",
		"Units:="		, "mm",
		"Rescale:="		, False,
		"Max Model Extent:="	, 10000
	])

oDesign.SetSolutionType("HFSS Modal Network", 
	[
		"NAME:Options",
		"EnableAutoOpen:="	, False
	])
######################## VARIABLES #################################
# Define variables - Baisc
variables = {
    "port1ywidth": PORT1_Y_WIDTH,
    "port1xlength": PORT1_X_LENGTH,
    "port2xlength": PORT2_X_LENGTH,
    "port2ywidth": PORT2_Y_WIDTH,
    "transformerxlength": TRANSFORMER_X_LENGTH,
    "transformerywidth": TRANSFORMER_Y_WIDTH,
    "substrateywidth": SUBSTRATE_Y_WIDTH,
    "substratezheight": SUBSTRATE_Z_HEIGHT
}

# Define expressions using other variables
expression_variables = {
    "substratexlength": "port1xlength+transformerxlength+port2xlength"
}


# Add simple variables first
for variable, value in variables.items():
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:LocalVariableTab",
                [
                    "NAME:PropServers", 
                    "LocalVariables"
                ],
                [
                    "NAME:NewProps",
                    [
                        "NAME:{}".format(variable),
                        "PropType:="		, "VariableProp",
                        "UserDef:="		, True,
                        "Value:="		, "{}".format(value)
                    ]
                ]
            ]
        ]
    )
    
oDesVar = oDesign.GetChildObject("Variables")


# Add expression variables (that reference other variables)
for variable, expression in expression_variables.items():
    oDesign.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:LocalVariableTab",
                [
                    "NAME:PropServers", 
                    "LocalVariables"
                ],
                [
                    "NAME:NewProps",
                    [
                        "NAME:{}".format(variable),
                        "PropType:="		, "VariableProp",
                        "UserDef:="		, True,
                        "Value:="		, "{}".format(expression)
                    ]
                ]
            ]
        ]
    )
substratexlength=oDesVar.GetPropSIValue("substratexlength")*1000 #float	value in mm

############## Substrate ######################
# SubstrateCreation
oEditor.CreateBox(
	[
		"NAME:BoxParameters",
		"XPosition:="		, "-substratexlength/2",
		"YPosition:="		, "-substrateywidth/2",
		"ZPosition:="		, "-substratezheight",
		"XSize:="		, "substratexlength",
		"YSize:="		, "substrateywidth",
		"ZSize:="		, "substratezheight"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Substrate",
		"Flags:="		, "",
		"Color:="		, "(100 255 100)",
		"Transparency:="	, 0.9,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, SUBSTRATE_MATERIAL,
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "0mm",
		"ReferenceTemperature:=", "20cel",
		"IsMaterialEditable:="	, True,
		"IsSurfaceMaterialEditable:=", True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	]
)
############ Substrate END ######################

############## GND PLANE ######################

# Ground Plane Object Creation
oEditor.CreateObjectFromFaces(
	[
		"NAME:Selections",
		"Selections:="		, "Substrate",
		"NewPartsModelFlag:="	, "Model"
	], 
	[
		"NAME:Parameters",
		[
			"NAME:GND_PLANE_OBJ",
			"FacesToDetach:="	, [8]
		]
	], 
	[
		"CreateGroupsForNewObjects:=", False
	]
)

#Change Name of Object to GND_PLANE
oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DAttributeTab",
			[
				"NAME:PropServers", 
				"Substrate_ObjectFromFace1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Name",
					"Value:="		, "GND_PLANE"
				]
			]
		]
	])

oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DAttributeTab",
			[
				"NAME:PropServers", 
				"GND_PLANE"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Color",
					"R:="			, 255,
					"G:="			, 255,
					"B:="			, 0
				]
			]
		]
	])

oEditor.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Geometry3DAttributeTab",
			[
				"NAME:PropServers", 
				"GND_PLANE"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Transparent",
					"Value:="		, 0
				]
			]
		]
	])

# Assign Boundary to conductor copper
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignFiniteCond(
	[
		"NAME:GND_PLANE_FINITE_CONDUCTOR",
		"Objects:="		, ["GND_PLANE"],
		"UseMaterial:="		, True,
		"Material:="		, "copper",
		"UseThickness:="	, False,
		"Roughness:="		, "0um",
		"InfGroundPlane:="	, False,
		"IsTwoSided:="		, False,
		"IsInternal:="		, True
	])

############## Ground Plane Done ##############


############## PORT1 Line #############
oEditor.CreateRectangle(
	[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, "-(port1xlength+port2xlength+transformerxlength)/2",
		"YStart:="		, "-port1ywidth/2",
		"ZStart:="		, "0mm",
		"Width:="		, "port1xlength",
		"Height:="		, "port1ywidth",
		"WhichAxis:="		, "Z"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Port1",
		"Flags:="		, "",
		"Color:="		, "(255 255 0)",
		"Transparency:="	, 0,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, "\"vacuum\"",
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "0mm",
		"ReferenceTemperature:=", "20cel",
		"IsMaterialEditable:="	, True,
		"IsSurfaceMaterialEditable:=", True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])

#-x-x-x-x-x-x-x PORT1 Line End -x-x-x-x-x-x-x-x#

############## Transformer Line #############
oEditor.CreateRectangle(
	[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, "-(transformerxlength)/2",
		"YStart:="		, "-transformerywidth/2",
		"ZStart:="		, "0mm",
		"Width:="		, "transformerxlength",
		"Height:="		, "transformerywidth",
		"WhichAxis:="		, "Z"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Transformer",
		"Flags:="		, "",
		"Color:="		, "(255 255 0)",
		"Transparency:="	, 0,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, "\"vacuum\"",
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "0mm",
		"ReferenceTemperature:=", "20cel",
		"IsMaterialEditable:="	, True,
		"IsSurfaceMaterialEditable:=", True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])

#-x-x-x-x-x-x-x Transformer Line End -x-x-x-x-x-x-x-x#

############## PORT2 Line #############
oEditor.CreateRectangle(
	[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, "(transformerxlength)/2",
		"YStart:="		, "-port2ywidth/2",
		"ZStart:="		, "0mm",
		"Width:="		, "port2xlength",
		"Height:="		, "port2ywidth",
		"WhichAxis:="		, "Z"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Port2",
		"Flags:="		, "",
		"Color:="		, "(255 255 0)",
		"Transparency:="	, 0,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, "\"vacuum\"",
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "0mm",
		"ReferenceTemperature:=", "20cel",
		"IsMaterialEditable:="	, True,
		"IsSurfaceMaterialEditable:=", True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])
# Assign Boundary to conductor copper
oModule = oDesign.GetModule("BoundarySetup")


################ Uniting Lines #################
oEditor.Unite(
	[
		"NAME:Selections",
		"Selections:="		, "Transformer,Port1,Port2"
	], 
	[
		"NAME:UniteParameters",
		"KeepOriginals:="	, False,
		"TurnOnNBodyBoolean:="	, True
	])

######### Assigning Lines Conductor Bondary- copper #################
oModule.AssignFiniteCond(
	[
		"NAME:PORT2_FINITE_CONDUCTOR",
		"Objects:="		, ["Transformer"],
		"UseMaterial:="		, True,
		"Material:="		, "copper",
		"UseThickness:="	, False,
		"Roughness:="		, "0um",
		"InfGroundPlane:="	, False,
		"IsTwoSided:="		, False,
		"IsInternal:="		, True
	])
#-x-x-x-x-x-x-x PORT2 Line End -x-x-x-x-x-x-x-x#


############### Radiation Boundary ##################
oEditor.CreateBox(
	[
		"NAME:BoxParameters",
		"XPosition:="		, "-substratexlength/2",
		"YPosition:="		, "-200mm",
		"ZPosition:="		, "-200mm",
		"XSize:="		, "substratexlength",
		"YSize:="		, "400mm",
		"ZSize:="		, "400mm"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "Radiation_Boundary_Box",
		"Flags:="		, "",
		"Color:="		, "(0 255 255)",
		"Transparency:="	, .95,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, "\"vacuum\"",
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "0mm",
		"ReferenceTemperature:=", "20cel",
		"IsMaterialEditable:="	, True,
		"IsSurfaceMaterialEditable:=", True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])
oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignRadiation(
	[
		"NAME:Radiation_Boundary",
		"Objects:="		, ["Radiation_Boundary_Box"]
	])



########### ADD WAVE PORTS ################
########### WAVE PORT 1
oEditor.CreateRectangle(
	[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, "-(port1xlength+port2xlength+transformerxlength)/2",
		"YStart:="		, "-port1ywidth*5",
		"ZStart:="		, "-substratezheight",
		"Width:="		, "port1ywidth*10",
		"Height:="		, "substratezheight*8",
		"WhichAxis:="		, "X"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "WAVE_PORT1_RECTANGLE",
		"Flags:="		, "",
		"Color:="		, "(255 0 0)",
		"Transparency:="	, 0,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, "\"vacuum\"",
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "0mm",
		"ReferenceTemperature:=", "20cel",
		"IsMaterialEditable:="	, True,
		"IsSurfaceMaterialEditable:=", True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])

oModule = oDesign.GetModule("BoundarySetup")
oModule.AssignWavePort(
	[
		"NAME:waveport1",
		"Objects:="		, ["WAVE_PORT1_RECTANGLE"],
		"WavePortType:="	, "Default",
		"NumModes:="		, 1,
		"UseLineModeAlignment:=", False,
		"DoDeembed:="		, False,
		[
			"NAME:Modes",
			[
				"NAME:Mode1",
				"ModeNum:="		, 1,
				"UseIntLine:="		, True,
				[
					"NAME:IntLine",
					"Coordinate System:="	, "Global",
					"Start:="		, ["{}mm".format(-substratexlength/2),"0mm","-{}".format(variables["substratezheight"])],
					"End:="			, ["{}mm".format(-substratexlength/2),"0mm","0mm"]
				],
				"AlignmentGroup:="	, 0,
				"CharImp:="		, "Zpi",
				"RenormImp:="		, "{}ohm".format(PORT_1_IMPEDENCE)
			]
		],
		"UseAnalyticAlignment:=", False,
		"ShowReporterFilter:="	, False,
		"ReporterFilter:="	, [True]
	])

########### WAVE PORT 2
oEditor.CreateRectangle(
	[
		"NAME:RectangleParameters",
		"IsCovered:="		, True,
		"XStart:="		, "(transformerxlength/2)+port2xlength",
		"YStart:="		, "-port2ywidth*5",
		"ZStart:="		, "-substratezheight",
		"Width:="		, "port2ywidth*10",
		"Height:="		, "substratezheight*8",
		"WhichAxis:="		, "X"
	], 
	[
		"NAME:Attributes",
		"Name:="		, "WAVE_PORT2_RECTANGLE",
		"Flags:="		, "",
		"Color:="		, "(255 0 0)",
		"Transparency:="	, 0,
		"PartCoordinateSystem:=", "Global",
		"UDMId:="		, "",
		"MaterialValue:="	, "\"vacuum\"",
		"SurfaceMaterialValue:=", "\"\"",
		"SolveInside:="		, True,
		"ShellElement:="	, False,
		"ShellElementThickness:=", "0mm",
		"ReferenceTemperature:=", "20cel",
		"IsMaterialEditable:="	, True,
		"IsSurfaceMaterialEditable:=", True,
		"UseMaterialAppearance:=", False,
		"IsLightweight:="	, False
	])


oModule.AssignWavePort(
	[
		"NAME:waveport2",
		"Objects:="		, ["WAVE_PORT2_RECTANGLE"],
		"WavePortType:="	, "Default",
		"NumModes:="		, 1,
		"UseLineModeAlignment:=", False,
		"DoDeembed:="		, False,
		[
			"NAME:Modes",
			[
				"NAME:Mode1",
				"ModeNum:="		, 1,
				"UseIntLine:="		, True,
				[
					"NAME:IntLine",
					"Coordinate System:="	, "Global",
					"Start:="		, ["{}mm".format(substratexlength/2),"0mm","-{}".format(variables["substratezheight"])],
					"End:="			, ["{}mm".format(substratexlength/2),"0mm","0mm"]
				],
				"AlignmentGroup:="	, 0,
				"CharImp:="		, "Zpi",
				"RenormImp:="		, "{}ohm".format(PORT_2_IMPEDENCE)
			]
		],
		"UseAnalyticAlignment:=", False,
		"ShowReporterFilter:="	, False,
		"ReporterFilter:="	, [True]
	])





#ANALYSIS SETUP
oModule = oDesign.GetModule("AnalysisSetup")
oModule.InsertSetup("HfssDriven", 
	[
		"NAME:Setup1",
		"SolveType:="		, "Single",
		"Frequency:="		, "{}GHz".format(FREQUENCY),
		"MaxDeltaS:="		, 0.02,
		"UseMatrixConv:="	, False,
		"MaximumPasses:="	, MAXIMUM_PASSES,
		"MinimumPasses:="	, 1,
		"MinimumConvergedPasses:=", 1,
		"PercentRefinement:="	, 30,
		"IsEnabled:="		, True,
		[
			"NAME:MeshLink",
			"ImportMesh:="		, False
		],
		"BasisOrder:="		, 1,
		"DoLambdaRefine:="	, True,
		"DoMaterialLambda:="	, True,
		"SetLambdaTarget:="	, False,
		"Target:="		, 0.3333,
		"UseMaxTetIncrease:="	, False,
		"PortAccuracy:="	, 2,
		"UseABCOnPort:="	, False,
		"SetPortMinMaxTri:="	, False,
		"DrivenSolverType:="	, "Direct Solver",
		"EnhancedLowFreqAccuracy:=", False,
		"SaveRadFieldsOnly:="	, False,
		"SaveAnyFields:="	, True,
		"IESolverType:="	, "Auto",
		"LambdaTargetForIESolver:=", 0.15,
		"UseDefaultLambdaTgtForIESolver:=", True,
		"IE Solver Accuracy:="	, "Balanced",
		"InfiniteSphereSetup:="	, "",
		"MaxPass:="		, 10,
		"MinPass:="		, 1,
		"MinConvPass:="		, 1,
		"PerError:="		, 1,
		"PerRefine:="		, 30
	])
oModule.InsertFrequencySweep("Setup1", 
	[
		"NAME:Sweep",
		"IsEnabled:="		, True,
		"RangeType:="		, "LinearCount",
		"RangeStart:="		, "{}GHz".format(RANGE_START),
		"RangeEnd:="		, "{}GHz".format(RANGE_END),
		"RangeCount:="		, POINTS,
		"Type:="		, "Interpolating",
		"SaveFields:="		, False,
		"SaveRadFields:="	, False,
		"InterpTolerance:="	, 0.5,
		"InterpMaxSolns:="	, 250,
		"InterpMinSolns:="	, 0,
		"InterpMinSubranges:="	, 1,
		"InterpUseS:="		, True,
		"InterpUsePortImped:="	, True,
		"InterpUsePropConst:="	, True,
		"UseDerivativeConvergence:=", False,
		"InterpDerivTolerance:=", 0.2,
		"UseFullBasis:="	, True,
		"EnforcePassivity:="	, True,
		"PassivityErrorTolerance:=", 0.0001,
		"EnforceCausality:="	, False,
		"SMatrixOnlySolveMode:=", "Auto"
	])
# Get the module for design settings
oDesign.SetDesignSettings(
	[
		"NAME:Design Settings Data",
		"Use Advanced DC Extrapolation:=", False,
		"Use Power S:="		, False,
		"Export FRTM After Simulation:=", False,
		"Export Rays After Simulation:=", False,
		"Export After Simulation:=", False,
		"Allow Material Override:=", False,
		"Calculate Lossy Dielectrics:=", True,
		"Perform Minimal validation:=", False,
		"EnabledObjects:="	, [],
		"Port Validation Settings:=", "Standard",
		"Save Adaptive support files:=", True
	], 
	[
		"NAME:Model Validation Settings",
		"EntityCheckLevel:="	, "Strict",
		"IgnoreUnclassifiedObjects:=", False,
		"SkipIntersectionChecks:=", False
	])

message("Causal Material Settings Applied Successfully")

if ANALYZE_ALL_AND_GENERATE_S_PLOT:
      
	oDesign.AnalyzeAllNominal()
	# It will Wait for the solver to finish
	message("Analysis Successfully Done. Check S_parameter Graph ",3)

	oModule = oDesign.GetModule("ReportSetup")
	oModule.CreateReport("Terminal S Parameter Plot 1", "Terminal Solution Data", "Rectangular Plot", "Setup1 : Sweep", 
		[
			"Domain:="		, "Sweep"
		], 
		[
			"Freq:="		, ["All"],
			"port1ywidth:="		, ["Nominal"],
			"port1xlength:="	, ["Nominal"],
			"port2xlength:="	, ["Nominal"],
			"substratezheight:="	, ["Nominal"],
			"transformerywidth:="	, ["Nominal"],
			"substrateywidth:="	, ["Nominal"],
			"transformerxlength:="	, ["Nominal"],
			"port2ywidth:="		, ["Nominal"]
		], 
		[
			"X Component:="		, "Freq",
			"Y Component:="		, ["dB(St(waveport1,waveport1))","dB(St(waveport2,waveport1))"]
		])