# tool_reset_plane
# (C) 2018, Danilo Tromp, Team Odd.Bot
# This scripts clears the z values of the plane object

print ("Hello from vertice manipulation test")

import bpy
import bmesh
import sys

#### MAIN ####

# Make sure if an object is active and in edit mode, we go back to object mode
if (bpy.context.scene.objects.active != None):
    #active_object=bpy.context.scene.objects.active
    #print("Active object = ", active_object.name)
    bpy.ops.object.mode_set(mode='OBJECT')
    
# De-select all in scene
for obj in bpy.data.objects:
    obj.select = False

obj = bpy.data.objects["Plane"]              # particular object by name
bpy.context.scene.objects.active = obj
if (bpy.context.active_object.mode != 'OBJECT'):
    raise Exception("ERROR: active object not in object mode")

# Make sure no vertices where selected manually in the plane
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')

### Clear the mesh shape ###

#Show all keys the object has to offer
#dump(obj.data)
mesh = obj.data

# Dump the vertices
#print("# of vertices=%d" % len(mesh.vertices))
# for vert in mesh.vertices:
#   print( 'v %f %f %f\n' % (vert.co.x, vert.co.y, vert.co.z) )

# Clear the z values of the vertices
for vert in mesh.vertices:
    vert.co.z = 0

# Make sure the manipulated mesh is updated inside blender   
mesh.update
