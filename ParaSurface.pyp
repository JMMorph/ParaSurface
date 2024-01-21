import c4d
from c4d import plugins, bitmaps, Vector, SplineObject, utils

import math
from math import *
import os
import ast
import copy

# Constants
COEF_NAMES = 'abcdfghijklmnopqrst'

# ID of the custom surface object
SURFACE_OBJECT_BASE = 3000
SURFACE_OBJECT = 3001

SURFACE_PATH = os.path.join(os.path.dirname(__file__), 'res/surfaces/')

# Function to parse a mathematical expression
def parse_expression(equations, auxiliar_equation = None, coefficients = {}):
    
    # Add math functions and constants to the allowed names
    allowed_names = set(dir(math))  # All math module functions
    allowed_names |= {"abs", "max", "min", "aux"}  # Other common functions
    allowed_names |= set(coefficients.keys())  # Constants defined by the user
    allowed_names |= {"u", "v"} # Parameters of the surface

    # Check if the expressions are valid
    for equation_str in equations:
        # Use ast to parse the expression
        try:
            parsed_expression = ast.parse(copy.deepcopy(equation_str), mode="eval")
        except SyntaxError:
            raise ValueError("Expresión matemática no válida.")
        
        # Review the syntax tree to validate allowed names
        for node in ast.walk(parsed_expression):
            if isinstance(node, ast.Name) and node.id not in allowed_names:
                raise ValueError(f"Not allowed name: {node.id}")


    # If the expression is valid, return a function that evaluates it
    # Use globals() to allow math functions without the "math." prefix
    if auxiliar_equation is not None:
        equations = [e.replace('aux', f'({auxiliar_equation})') for e in equations]
    
    eq_x = equations[0]
    eq_y = equations[1]
    eq_z = equations[2]
    
    return eq_x, eq_y, eq_z

# Class to store the parametricSurfaces and parameters of a surface
class parametricSurface:
    def __init__(self, name = 'Null', coefficients = {}, scale = 1, 
                surface_type = 'custom',
                definition = '', u_segments = 50, v_segments = 50,
                u_min = 0, u_max = 2*math.pi, u_percent = 100, u_offset = 0,
                v_min = 0, v_max = 2*math.pi, v_percent = 100, v_offset = 0,
                ) -> None:
        
        self.name = name
        self.surface_type = surface_type
        
        # Coefficients by default
        self.coefficients = coefficients
        # Definition of the surface 
        self.definition = definition
        
        # Parameters by default
        self.u_segments = u_segments
        self.v_segments = v_segments
        self.u_min = u_min
        self.u_max = u_max
        self.u_percent = u_percent
        self.u_offset = u_offset
        self.v_min = v_min
        self.v_max = v_max
        self.v_percent = v_percent
        self.v_offset = v_offset
        
        self.weld = True
        self.orientation = c4d.SURF_ORIENTATION_YP
        self.update_uvw = True
        self.scale = scale
        self.aspect_ratio_x = 1
        self.aspect_ratio_y = 1
        self.aspect_ratio_z = 1
        self.grid_x = 0
        self.grid_y = 0
        self.grid_z = 0
        
        return None
    
    def set_equations(self, eq_x, eq_y, eq_z):
        self.eq_x = eq_x
        self.eq_y = eq_y
        self.eq_z = eq_z
        self.update_eval()
        return True
    
    def update_eval(self):
        self.x = lambda u, v: eval(self.eq_x, globals(), { **self.coefficients, 'u': u, 'v': v })
        self.y = lambda u, v: eval(self.eq_y, globals(), { **self.coefficients, 'u': u, 'v': v })
        self.z = lambda u, v: eval(self.eq_z, globals(), { **self.coefficients, 'u': u, 'v': v })
        return True
        
    def eval(self, u, v):
        return self.x(u, v), self.y(u, v), self.z(u, v)

# Function to read a surface from a file
def surfaceFromFile(path,surface_type):
    
    FILES = {
        c4d.SURF_TYPE_MONKEY_SADDLE : "monkey_saddle",
        c4d.SURF_TYPE_SINE_WAVE : "sine_wave",
        c4d.SURF_TYPE_SPIRAL_WAVE : "spiral_wave",
        c4d.SURF_TYPE_DINIS_SURFACE : "dinis_surface",
        c4d.SURF_TYPE_WAVE_BALL : "wave_ball",
        c4d.SURF_TYPE_HYPERBOLIC_HELICOID : "hyperbolic_helicoid",
        c4d.SURF_TYPE_CROSSED_THROUGH_SURFACE : "crossed_through_surface",
        c4d.SURF_TYPE_MOBIUS_STRIP : "mobius_strip",
        c4d.SURF_TYPE_SINE_SURFACE : "sine_surface",
        c4d.SURF_TYPE_COSINE_SURFACE : "cosine_surface",
        c4d.SURF_TYPE_SINE_CUBE : "sine_cube",
        c4d.SURF_TYPE_EIGHT_SURFACE : "eight_surface",
        c4d.SURF_TYPE_HYPERBOLIC_OCTAHEDRON : "hyperbolic_octahedron",
        c4d.SURF_TYPE_BREATHER_SURFACE : "breather_surface",
        c4d.SURF_TYPE_PSEUDO_CROSS_CAP : "pseudo_cross_cap",
        c4d.SURF_TYPE_BOY_SURFACE_I : "boy_surface_i",
        c4d.SURF_TYPE_BOY_SURFACE_II : "boy_surface_ii",
        c4d.SURF_TYPE_TWISTED_SPHERE : "twisted_sphere",
        c4d.SURF_TYPE_KLEIN_CYCLOID : "klein_cycloid",
        c4d.SURF_TYPE_JENNER_KLEIN_BOTTLE : "jenner_klein_bottle",
        c4d.SURF_TYPE_STEREOGRAPHIC_SPHERE : "stereographic_sphere",
        c4d.SURF_TYPE_CROSS_CAP : "cross_cap",
        c4d.SURF_TYPE_STROPHOID_CILINDER : "strophoid_cylinder",
        c4d.SURF_TYPE_KLEIN_BOTTLE : "klein_bottle",
        c4d.SURF_TYPE_SEASHELL_1 : "seashell_1",
        c4d.SURF_TYPE_SEASHELL_2 : "seashell_2",
        c4d.SURF_TYPE_PILLOW : "pillow",
        c4d.SURF_TYPE_MILK_CARTON : "milk_carton",
        c4d.SURF_TYPE_SPINNING_TOP : "spinning_top",
        c4d.SURF_TYPE_BOWTIE : "bowtie",
        c4d.SURF_TYPE_CRESCENT : "crescent",
        c4d.SURF_TYPE_LAWSON_BOTTLE : "lawson_bottle",
        c4d.SURF_TYPE_DROP_OR_EGG : "drop_or_egg",
        c4d.SURF_TYPE_APPLE_I : "apple_i",
        c4d.SURF_TYPE_FRUIT : "fruit",
        c4d.SURF_TYPE_CORKSCREW : "corkscrew",
        c4d.SURF_TYPE_GEAR_TUBE : "gear_tube",
        c4d.SURF_TYPE_UMBRELLA : "umbrella",
        c4d.SURF_TYPE_TUDOR_ROSE : "tudor_rose",
        c4d.SURF_TYPE_INVOLUTE_CONOID : "involute_conoid",
        c4d.SURF_TYPE_FISH_SURFACE : "fish_surface",
        c4d.SURF_TYPE_ASYMETRIC_TORUS : "asymetric_torus",
        c4d.SURF_TYPE_TRICUSPID_TORUS : "tricuspid_torus",
        c4d.SURF_TYPE_ASTROID_TORUS : "astroid_torus",
        c4d.SURF_TYPE_UMBILIC_TORUS : "umbilic_torus",
        c4d.SURF_TYPE_EIGHT_TORUS : "eight_torus",
        c4d.SURF_TYPE_TWISTED_EIGHT_TORUS : "twisted_eight_torus",
        c4d.SURF_TYPE_WAVE_TORUS : "wave_torus",
        c4d.SURF_TYPE_GEAR_WHEEL_TORUS : "gear_wheel_torus",
        c4d.SURF_TYPE_SPIRAL_TORUS : "spiral_torus",
        c4d.SURF_TYPE_TORUS_KNOT : "torus_knot",
        c4d.SURF_TYPE_MULTI_TORUS_SHAPE : "multi_torus_shape",
        c4d.SURF_TYPE_BRAIDED_TORUS : "braided_torus",
        c4d.SURF_TYPE_ELLIPTIC_TORUS : "elliptic_torus",
        c4d.SURF_TYPE_CUSTOM : "custom"
    }
    
    f = FILES.get(surface_type)
    with open(path + f + '.surf', 'r') as file:
        
        # Set the name as the filename with maximum 15 characters
        name = f.replace('_', ' ')
        name = name.title()
        name = name[:15]
        
        # Read the file 
        lines = file.readlines()
        lines = [l.strip() for l in lines] # Remove spaces
        lines = [l for l in lines if l.strip() != ''] # Remove empty lines
        lines = [l for l in lines if l.strip()[0] != '#'] # Remove comments
        lines[0:5] = [l.replace(',', '').replace(';', '')  for l in lines[0:5]] # Remove commas
        
        
        # Read the parameters
        u_segments, v_segments = [int(i) for i in lines[0].split()[1::]]
        u_min, u_max = [float(i) for i in lines[1].split()[1::]]
        v_min, v_max = [float(i) for i in lines[2].split()[1::]]
        
        coefficients = {i:float(j) for i,j in zip(COEF_NAMES, lines[3].split()[1::])}
        scale = float(lines[4].split()[1])

        # Identify the x, y, z equations        
        definition = '\n'.join(lines[5:8])
        lines[5:8] = [l.replace('x = ', '').replace('y = ', '').replace('z = ', '') for l in lines[5:8]]
        
        
        # Identify the auxiliar equation if it exists
        if len(lines) < 9:
            auxiliar_equation = None
        else:
            auxiliar_equation = lines[-1].replace('aux = ', '')
            definition += f'\nWhere \naux = {auxiliar_equation}'
        
        # Parse the equations
        eq_x, eq_y, eq_z = parse_expression(lines[5:8], auxiliar_equation, coefficients)
        
        # Create the surface object
        surface = parametricSurface(name, coefficients, scale, surface_type,
                                    definition, u_segments, v_segments,
                                    u_min, u_max, 100, 0,
                                    v_min, v_max, 100, 0)
                    
        surface.set_equations(eq_x, eq_y, eq_z)
        
        return surface
        

# Class to create the plugin
class ParaSurface (plugins.ObjectData):
    
    def __init__ (self):
        self.SetOptimizeCache(True)     # Enable cache
        
        # Define initial state
        initial_surface_type = c4d.SURF_TYPE_LAWSON_BOTTLE
        self.surf_obj_init = surfaceFromFile(SURFACE_PATH, initial_surface_type)
        self.surf_obj = copy.deepcopy(self.surf_obj_init)
        self.current_surface_type = initial_surface_type

    # Necessary to make the plugin work, but not used
    # Instead, the attributes are initialized in the Message function
    def Init(self, node, isCloneInit=False):
        pass

    
    # Function to initialize the attributes in the interface from the surface object
    def SetFromSurface(self, op, surface_obj):
        op[c4d.SURF_TYPE] = surface_obj.surface_type
        op[c4d.SURF_ORIENTATION] = c4d.SURF_ORIENTATION_YP
        op[c4d.SURF_U_SEGMENTS] = surface_obj.u_segments
        op[c4d.SURF_U_MIN] = surface_obj.u_min
        op[c4d.SURF_U_MAX] = surface_obj.u_max
        op[c4d.SURF_U_PERCENT] = surface_obj.u_percent
        op[c4d.SURF_U_OFFSET] = surface_obj.u_offset
        op[c4d.SURF_WELD] = 1
        op[c4d.SURF_SCALE] = surface_obj.scale
        op[c4d.SURF_V_SEGMENTS] = surface_obj.v_segments
        op[c4d.SURF_V_MIN] = surface_obj.v_min
        op[c4d.SURF_V_MAX] = surface_obj.v_max
        op[c4d.SURF_V_PERCENT] = surface_obj.v_percent
        op[c4d.SURF_V_OFFSET] = surface_obj.v_offset
        op[c4d.SURF_UPDATE_UVW] = 1
        
        op[c4d.SURF_ASPECT_RATIO_X] = 1
        op[c4d.SURF_ASPECT_RATIO_Y] = 1
        op[c4d.SURF_ASPECT_RATIO_Z] = 1
        op[c4d.SURF_GRID_X] = 0
        op[c4d.SURF_GRID_Y] = 0
        op[c4d.SURF_GRID_Z] = 0
        
        if op[c4d.SURF_TYPE] == c4d.SURF_TYPE_CUSTOM:
            op[c4d.SURF_NUMBER_COEFFICIENTS] = '-'
            op[c4d.SURF_SURFACE_NAME] = 'Custom'
            op[c4d.SURF_SURFACE_COEFFICIENTS] = '-'
            op[c4d.SURF_SURFACE_EQUATIONS] = '-'
            surface_obj.coefficients = {c: 0 for c in COEF_NAMES}
            
            op[c4d.SURF_CUSTOM_X] = surface_obj.eq_x
            op[c4d.SURF_CUSTOM_Y] = surface_obj.eq_y
            op[c4d.SURF_CUSTOM_Z] = surface_obj.eq_z
            op[c4d.SURF_CUSTOM_AUX] = ''
            
        else:
            op[c4d.SURF_NUMBER_COEFFICIENTS] = str(len(surface_obj.coefficients))
            op[c4d.SURF_SURFACE_NAME] = surface_obj.name
            op[c4d.SURF_SURFACE_COEFFICIENTS] = str(surface_obj.coefficients)
            op[c4d.SURF_SURFACE_EQUATIONS] = surface_obj.definition  
        
        # Initialize the coefficients        
        for i in COEF_NAMES:
            descid = c4d.DescID(c4d.DescLevel(c4d.SURF_NUMBER_COEFFICIENTS + 1 + COEF_NAMES.index(i), c4d.DTYPE_REAL, op.GetType()))
            op[descid[0].id] = surface_obj.coefficients.get(i, 0)  
        
        return True
    
    # Function to read the attributes from the interface and create the surface object
    def GetVirtualObjects(self, op, hh, restart_gui=False):
        surface_type = op[c4d.SURF_TYPE]
        
        if surface_type != self.current_surface_type:
            self.current_surface_type = surface_type
            self.surf_obj_init = surfaceFromFile(SURFACE_PATH, surface_type)
            self.surf_obj = copy.deepcopy(self.surf_obj_init)
            
            if restart_gui:
                self.SetFromSurface(op, self.surf_obj)
                
            # op.Message(c4d.MSG_UPDATE)
            
        
        # If custom
        if surface_type == c4d.SURF_TYPE_CUSTOM:
            x = op[c4d.SURF_CUSTOM_X].strip().replace('\n', '').replace('\r', '')
            y = op[c4d.SURF_CUSTOM_Y].strip().replace('\n', '').replace('\r', '')
            z = op[c4d.SURF_CUSTOM_Z].strip().replace('\n', '').replace('\r', '')
            auxiliar_equation = op[c4d.SURF_CUSTOM_AUX].strip().replace('\n', '').replace('\r', '')
            
            # Parse the equations
            eq_x, eq_y, eq_z = parse_expression([x, y, z], auxiliar_equation, self.surf_obj.coefficients)
            self.surf_obj.set_equations(eq_x, eq_y, eq_z)
            
        
        # If the surface type has not changed, just update the surface object
        self.surf_obj.u_segments = op[c4d.SURF_U_SEGMENTS]
        self.surf_obj.u_min = op[c4d.SURF_U_MIN]
        self.surf_obj.u_max = op[c4d.SURF_U_MAX]
        self.surf_obj.u_percent = op[c4d.SURF_U_PERCENT]
        self.surf_obj.u_offset = op[c4d.SURF_U_OFFSET]
        self.surf_obj.v_segments = op[c4d.SURF_V_SEGMENTS]
        self.surf_obj.v_min = op[c4d.SURF_V_MIN]
        self.surf_obj.v_max = op[c4d.SURF_V_MAX]
        self.surf_obj.v_percent = op[c4d.SURF_V_PERCENT]
        self.surf_obj.v_offset = op[c4d.SURF_V_OFFSET]
        
        self.surf_obj.orientation = op[c4d.SURF_ORIENTATION]
        self.surf_obj.scale = op[c4d.SURF_SCALE]
        self.surf_obj.weld = op[c4d.SURF_WELD]
        self.surf_obj.update_uvw = op[c4d.SURF_UPDATE_UVW]
        
        self.surf_obj.aspect_ratio_x = op[c4d.SURF_ASPECT_RATIO_X]
        self.surf_obj.aspect_ratio_y = op[c4d.SURF_ASPECT_RATIO_Y]
        self.surf_obj.aspect_ratio_z = op[c4d.SURF_ASPECT_RATIO_Z]
        self.surf_obj.grid_x = op[c4d.SURF_GRID_X]
        self.surf_obj.grid_y = op[c4d.SURF_GRID_Y]
        self.surf_obj.grid_z = op[c4d.SURF_GRID_Z]
        
        for i in COEF_NAMES:
            descid = c4d.DescID(c4d.DescLevel(c4d.SURF_NUMBER_COEFFICIENTS + 1 + COEF_NAMES.index(i), c4d.DTYPE_REAL, op.GetType()))
            if i in  self.surf_obj.coefficients:
                self.surf_obj.coefficients[i] = op[descid[0].id]
            
        self.surf_obj.update_eval()
        
        # Create the surface object and the UVW tag
        obj, uvw = self.generateSurface(self.surf_obj)
        
        if self.surf_obj.update_uvw:
            op.KillTag(c4d.Tuvw)
            op.InsertTag(uvw)
        
        op.CopyTagsTo(obj, c4d.NOTOK,c4d.NOTOK,c4d.NOTOK)
        
        obj.SetName(op.GetName())
        

        return obj 
    
    # Function to create the surface object and the UVW tag
    def generateSurface(self, s = None): 
        
        # Number of points 
        p_Nu = int(ceil(s.u_segments*s.u_percent) )
        p_Nv = int(ceil(s.v_segments*s.v_percent) )

        # Compute the last segment width, this is important when the percentage is not 100%
        dif_u = (s.u_max-s.u_min)*s.u_percent - (p_Nu-1)*((s.u_max-s.u_min) / s.u_segments)
        dif_v = (s.v_max-s.v_min)*s.v_percent - (p_Nv-1)*((s.v_max-s.v_min) / s.v_segments)

        # Create empty polygon object
        obj = c4d.PolygonObject((p_Nu+1) * (p_Nv+1) , p_Nu* p_Nv)

        # Counter for index
        zz = 0

        # Create points
        for i in range (0, p_Nu+1):
            for j in range (0, p_Nv+1):

                # Calculate segment widths (step for u and v)
                du = (s.u_max-s.u_min) / s.u_segments
                dv = (s.v_max-s.v_min) / s.v_segments

                # Calculate u and v
                u = s.u_min + i * du + (-du + dif_u)*(i==(p_Nu)) + s.u_offset
                v = s.v_min + j * dv + (-dv + dif_v)*(j==(p_Nv)) + s.v_offset
                
                # Calculate x, y, z without modifications
                
                try:
                    xf, yf, zf = s.eval(u, v)
                except ZeroDivisionError:
                    print('ZeroDivisionError')
                    xf, yf, zf = 0, 0, 0
                except:
                    print('Error, verify the equations')
                    xf, yf, zf = 0, 0, 0
                    

                # Update x, y, z with modifications (considering the grid U,V likeness)
                x = (xf)*(1-s.grid_x) + u*s.grid_x
                y = (yf)*(1-s.grid_y) + v*s.grid_y
                z = (zf)*(1-s.grid_x)

                # Update x, y, z with orientation
                if s.orientation == c4d.SURF_ORIENTATION_YP:
                    pass
                elif s.orientation == c4d.SURF_ORIENTATION_YN:
                    y = -y
                elif s.orientation == c4d.SURF_ORIENTATION_XP:
                    x, y = y, x
                elif s.orientation == c4d.SURF_ORIENTATION_XN:
                    x, y = -y, x     
                elif s.orientation == c4d.SURF_ORIENTATION_ZP:
                    y, z = z, y
                elif s.orientation == c4d.SURF_ORIENTATION_ZN:
                    y, z = z, -y
                
                # Update x, y, z with scale and aspect ratio
                x_end = x * s.aspect_ratio_x * s.scale
                y_end = y * s.aspect_ratio_y * s.scale
                z_end = z * s.aspect_ratio_z * s.scale

                # Save points
                obj.SetPoint (zz, c4d.Vector (x_end, y_end, z_end))

                # Increase counter
                zz = zz + 1

        zz = 0 # reset counter
        UVW = c4d.UVWTag(obj.GetPointCount())

        
        # Create polygons from points
        for j in range (0, p_Nv):
            for i in range (0, p_Nu):

                # Define points for a square
                P1 = i * (p_Nv +1) + j
                P2 = i * (p_Nv +1) + j + 1
                P3 = (i + 1) * (p_Nv +1) + j + 1
                P4 = (i + 1) * (p_Nv +1) + j

                # Save square
                obj.SetPolygon (zz, c4d.CPolygon (P1, P2, P3, P4))

                # Update UVW Map
                du0 = float(1)/s.u_segments * i
                dv0 = float(1)/s.v_segments * j
                du1 = du0 + float(1)/s.u_segments
                dv1 = dv0 + float(1)/s.v_segments

                UP0 = c4d.Vector(du0,dv0,0)
                UP1 = c4d.Vector(du0,dv1,0)
                VP0 = c4d.Vector(du1,dv0,0)
                VP1 = c4d.Vector(du1,dv1,0)
                
                UVW.SetSlow(zz,UP0,UP1,VP1,VP0)

                # Increase counter
                zz = zz + 1

        # If weld checked
        if s.weld:

            # Weld points
            opt=c4d.BaseContainer()
            opt[c4d.MDATA_OPTIMIZE_TOLERANCE]=0.01
            opt[c4d.MDATA_OPTIMIZE_POINTS]=1
            opt[c4d.MDATA_OPTIMIZE_POLYGONS]=1
            opt[c4d.MDATA_OPTIMIZE_UNUSEDPOINTS]=1

            res = utils.SendModelingCommand( command = c4d.MCOMMAND_OPTIMIZE,
                                            list = [obj],
                                            mode = c4d.MODELINGCOMMANDMODE_ALL,
                                            bc = opt)

        # Update object
        obj.Message(c4d.MSG_UPDATE)

        if not s.update_uvw:
            UVW = None

        return obj, UVW

    # Function to handle the changes in the button
    def Message(self, node, type, data):
        ### Called by Cinema 4D to retrieve the current surface type.
        
        # If one element in the interface has changed
        if type == c4d.MSG_DESCRIPTION_COMMAND:
            
            # If the reset button has been pressed
            if data['id'][0].id == c4d.SURF_RESET:
                self.surf_obj = copy.deepcopy(self.surf_obj_init)              
                self.SetFromSurface(node, self.surf_obj)
                self.GetVirtualObjects(node, None, restart_gui=True)
                # node.Message(c4d.MSG_UPDATE)
        
        # If one parameter in the interface has changed
        elif type == c4d.MSG_DESCRIPTION_POSTSETPARAMETER:

            # If the surface type has changed
            if data['descid'][0].id == c4d.SURF_TYPE:
                
                surface_type = node[c4d.SURF_TYPE]
                if surface_type != self.surf_obj_init.surface_type:
                        
                    surface_obj = surfaceFromFile(SURFACE_PATH, surface_type)
                    self.surf_obj_init = copy.deepcopy(surface_obj)
                    self.surf_obj = copy.deepcopy(surface_obj)
                    self.SetFromSurface(node, self.surf_obj)

        
        # Mesage received just before the interface is displayed
        
        elif type == c4d.MSG_MENUPREPARE:
            
            # Initialize the attributes
            self.InitAttr(node, int, [c4d.SURF_TYPE])
            self.InitAttr(node, bool, [c4d.SURF_RESET])
            
            self.InitAttr(node, int, [c4d.SURF_ORIENTATION])
            self.InitAttr(node, float, [c4d.SURF_U_SEGMENTS])
            self.InitAttr(node, float, [c4d.SURF_U_MIN])
            self.InitAttr(node, float, [c4d.SURF_U_MAX])
            self.InitAttr(node, float, [c4d.SURF_U_PERCENT])
            self.InitAttr(node, float, [c4d.SURF_U_OFFSET])
            self.InitAttr(node, bool, [c4d.SURF_WELD])
            self.InitAttr(node, float, [c4d.SURF_SCALE])
            self.InitAttr(node, float, [c4d.SURF_V_SEGMENTS])
            self.InitAttr(node, float, [c4d.SURF_V_MIN])
            self.InitAttr(node, float, [c4d.SURF_V_MAX])
            self.InitAttr(node, float, [c4d.SURF_V_PERCENT])
            self.InitAttr(node, float, [c4d.SURF_V_OFFSET])
            self.InitAttr(node, bool, [c4d.SURF_UPDATE_UVW])
            
            self.InitAttr(node, str, [c4d.SURF_NUMBER_COEFFICIENTS])
            
            self.InitAttr(node, str, [c4d.SURF_CUSTOM_X])
            self.InitAttr(node, str, [c4d.SURF_CUSTOM_Y])
            self.InitAttr(node, str, [c4d.SURF_CUSTOM_Z])
            self.InitAttr(node, str, [c4d.SURF_CUSTOM_AUX])
            
            self.InitAttr(node, float, [c4d.SURF_ASPECT_RATIO_X])
            self.InitAttr(node, float, [c4d.SURF_ASPECT_RATIO_Y])
            self.InitAttr(node, float, [c4d.SURF_ASPECT_RATIO_Z])
            self.InitAttr(node, float, [c4d.SURF_GRID_X])
            self.InitAttr(node, float, [c4d.SURF_GRID_Y])
            self.InitAttr(node, float, [c4d.SURF_GRID_Z])
            
            self.InitAttr(node, str, [c4d.SURF_SURFACE_NAME])
            self.InitAttr(node, str, [c4d.SURF_SURFACE_COEFFICIENTS])
            self.InitAttr(node, str, [c4d.SURF_SURFACE_EQUATIONS])
            self.InitAttr(node, parametricSurface, [SURFACE_OBJECT_BASE])
            
            # Initialize the coefficients
            for i in COEF_NAMES:
                descid = c4d.DescID(c4d.DescLevel(c4d.SURF_NUMBER_COEFFICIENTS + 1 + COEF_NAMES.index(i), c4d.DTYPE_REAL, node.GetType()))
                self.InitAttr(node, float, [descid[0].id])   
            
            # Insert a phong tag by default
            phongTag = c4d.BaseTag(c4d.Tphong)
            phongTag[c4d.PHONGTAG_PHONG_ANGLELIMIT] = True
            phongTag[c4d.PHONGTAG_PHONG_ANGLE] = radians(80)
            node.InsertTag(phongTag)
            self.SetFromSurface(node, self.surf_obj)
            

                

        return True

    # Function to handle the changes in the interface
    def GetDEnabling(self, node, id, t_data, flags, itemdesc):
        ### "Called  by Cinema 4D to decide which parameters should be enabled or disabled (ghosted).

        if self.surf_obj is None:
            return False
        
        # Retrieves the current surface type
        surface_type = node[c4d.SURF_TYPE]
        
        # Id of the custom equations fields
        id_equations = set([c4d.SURF_CUSTOM_X, c4d.SURF_CUSTOM_Y, c4d.SURF_CUSTOM_Z, c4d.SURF_CUSTOM_AUX])
        
        # Create a set with the coefficients that are not being used
        unused_coef = set()
        for i in COEF_NAMES:
            descid = c4d.DescID(c4d.DescLevel(c4d.SURF_NUMBER_COEFFICIENTS + 1 + COEF_NAMES.index(i), c4d.DTYPE_REAL, node.GetType()))
            if i not in set(self.surf_obj.coefficients.keys()):
                unused_coef.add(descid[0].id)

        
        # If the surface type is not custom, disable the coefficients that are not being used
        if (id[0].id in unused_coef or id[0].id in id_equations) and surface_type != c4d.SURF_TYPE_CUSTOM:
            return False


        return True
    


    
if __name__ == "__main__":
    
    # Load the plugin icon
    icon_absolute_path = os.path.join(os.path.dirname(__file__), 'res/icons', 'icon.png')
    plugin_icon = bitmaps.BaseBitmap()
    plugin_icon.InitWith(icon_absolute_path)

    # Register the plugin
    plugins.RegisterObjectPlugin(
        id = 1062596,
        str = 'ParaSurface',
        g =  ParaSurface,
        description = 'Osurf',
        info = c4d.OBJECT_GENERATOR,
        icon = plugin_icon
    )
