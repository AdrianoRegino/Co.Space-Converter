import bpy
import math

# Add-on info
bl_info = {
    "name": "CoSpace Converter 1",
    "author": "Adriano de Regino",
    "version": (1, 0, 0),
    "blender": (3, 4, 1),
    "location": "View3D > Properties > Edit",
    "description": "Convert vertex color, face corner data from linear to gamma space and the other way around", 
    "wiki_url": "https://github.com/AdrianoRegino/Co.Space-Converter/tree/main",
    "tracker_url": "-",      
    "category": "3D View"}

# Define functions to convert a value from linear space to gamma space, and vice versa
def linear_to_gamma(linear_value):
    if linear_value <= 0.0031308:
        return 12.92 * linear_value
    else:
        return 1.055 * math.pow(linear_value, 1.0 / 2.4) - 0.055
        
def gamma_to_linear(gamma_value):
    if gamma_value <= 0.04045:
        return gamma_value / 12.92
    else:
        return math.pow((gamma_value + 0.055) / 1.055, 2.4)

# Define an operator to convert vertex colors from linear to gamma space
class LinearToGammaOperator(bpy.types.Operator):
    bl_idname = "object.linear_to_gamma_operator"
    bl_label = "Linear to Gamma"
    bl_description = "Convert vertex color from linear to gamma space"
    
    def execute(self, context):
        # Get the selected object
        obj = context.view_layer.objects.active
        
        # Get the active vertex color layer
        vertex_color_layer = obj.data.vertex_colors.active
        
        # Iterate through all faces of the object
        for face in obj.data.polygons:
            # Iterate through all corners of the face
            for loop_index in face.loop_indices:
                # Get the byte color of the current corner
                byte_color = vertex_color_layer.data[loop_index].color
                
                # Convert the byte color from linear space to gamma space
                gamma_color = [linear_to_gamma(byte_color[i]) for i in range(4)]
                
                # Set the gamma color as the new color of the current corner
                vertex_color_layer.data[loop_index].color = gamma_color
        
        return {'FINISHED'}
    
# Define an operator to convert vertex colors from gamma to linear space
class GammaToLinearOperator(bpy.types.Operator):
    bl_idname = "object.gamma_to_linear_operator"
    bl_label = "Gamma to Linear"
    bl_description = "Convert vertex color from gamma to linear space"
    
    def execute(self, context):
        # Get the selected object
        obj = context.object
        
        # Get the active vertex color layer
        vertex_color_layer = obj.data.vertex_colors.active
        
        # Iterate through all faces of the object
        for face in obj.data.polygons:
            # Iterate through all corners of the face
            for loop_index in face.loop_indices:
                # Get the byte color of the current corner
                byte_color = vertex_color_layer.data[loop_index].color
                
                # Convert the byte color from gamma space to linear space
                linear_color = [gamma_to_linear(byte_color[i]) for i in range(4)]
                
                # Set the linear color as the new color of the current corner
                vertex_color_layer.data[loop_index].color = linear_color
        
        return {'FINISHED'}

# Define the panel for the operator
class Panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_CoSpace"
    bl_label = "CoSpace Converter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("object.linear_to_gamma_operator", text="Convert Linear to Gamma")
        row = layout.row()
        row.operator("object.gamma_to_linear_operator", text="Convert Gamma to Linear")

# Register the operator and panel
def register():
    bpy.utils.register_class(LinearToGammaOperator)
    bpy.utils.register_class(GammaToLinearOperator)
    bpy.utils.register_class(Panel)
    
def unregister():
    bpy.utils.unregister_class(LinearToGammaOperator)
    bpy.utils.unregister_class(GammaToLinearOperator)
    bpy.utils.unregister_class(Panel)

# Test the addon
if __name__ == "__main__":
    register()