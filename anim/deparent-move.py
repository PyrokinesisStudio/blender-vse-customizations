import bpy

## Deparent-move-reparent
##
## a Blender Python script by GitHub user Botmasher (Joshua R)
##
## Remove object parent, move object either to selected's position or to
## parented's same position globally, then optionally parent to selected.
##
## Motivation: deleting mesh object's parent may translate mesh to undesired
## locations upon removing parent offset.
##

def move(obj, loc):
    """Move the object to the given location"""
    if obj and hasattr(obj, 'location'):
        obj.location = loc
    return loc

def is_loc(loc):
    """Check if argument is an x, y, z position"""
    return loc and hasattr(loc, 'x') and len(loc == 3)

def add_locs(loc_a, loc_b):
    """Add the x, y, z values of one location to another"""
    if not is_loc(loc_a) or not is_loc(loc_b):
        return Exception("Failed to add locations {0} and {1}".format(loc_a, loc_b))
    return [loc_a[i] + loc_b[i] for i in range(len(loc_a))]

def subtract_locs(loc_a, loc_b):
    """Subtract the x, y, z values of the second location from the first"""
    if not is_loc(loc_a) or not is_loc(loc_b):
        return Exception("Failed to subtract locations {0} and {1}".format(loc_a, loc_b))
    return [loc_a[i] - loc_b[i] for i in range(len(loc_a))]

def offset_parented_pos(obj):
    """Return the object's current world position if it were unparented"""
    if obj and hasattr(obj, 'parent') and hasattr(obj, 'location'):
        return add_locs(obj.location, obj.parent.location)
    return

def has_parent(obj):
    """Check if the object has a parent object"""
    return obj and hasattr(obj, 'parent') and obj.parent

def unset_parent(obj):
    """Remove the object's parent if it has one"""
    if obj and hasattr(obj, 'parent'):
        obj.parent = None
    return obj

def set_parent(obj, parent):
    """Set the object's parent"""
    obj.parent = parent
    return obj

def get_inactive_selected():
    """Find the first inactive selected object"""
    for object in bpy.context.scene.objects:
        if object.select and not object == bpy.context.scene.objects.active:
            return object
    return

def handle_deparenting(obj=bpy.context.scene.objects.active, to_selected=False, reparent=False):
    """Unset active object parent but maintain current position in world, optionally reparenting to the first inactive selected object"""
    if not obj or not has_parent(obj):
        return obj
    target = get_inactive_selected()
    if target and to_selected:
        # keep same offset from inactive selected object
        offset_loc = add_locs(obj.location, target.location)
    else:
        # maintain current world position (no visual move)
        offset_loc = add_locs(obj.location, obj.parent.location)
    move(obj, offset_loc)
    # remove parent last to allow calculating parent loc
    unset_parent(obj)
    reparent and set_parent(target)
    return obj


# test deparent + keep world pos
handle_deparenting()
