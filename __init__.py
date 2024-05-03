from . import CoSpace-Converter


bl_info = {
	"name": "CoSpace-Converter",
	"author": "Adriano de Regino",
	"version": (0,1),
	"blender": (3, 0, 0),
	"location": "3D View > Edit > CoSpace Converter",
	"description": "Extension that converts an object vertex color from linear color space to gamma and vice-versa.",
	"category": "Mesh",
}

def register():
    co_space_converter.register()
    
def unregister():
    co_space_converter.unregister()
