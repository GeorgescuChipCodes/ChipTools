from maya import cmds

def rename_selected(is_selected = False):
    """
    Docstring for rename_selected
    This function will rename any objects to have the correct suffix
    
    :param is_selected: Whether or not we use the current selection

    Returns: A list of all objects we operated on
    """
    affected_object = cmds.ls(is_selected, dag = True, long = True)

    object_dictionary = {
        "joint" : "jnt",
        "locator" : "loc",
        "mesh" : "geo",
        "nurbsCurve" : "ctrl",
        "ambientLight" : "lgt"
    }

    if is_selected and not affected_object:
        raise RuntimeError("You don't have anything selected")




    affected_object = cmds.ls(dag = True, long = True)
    affected_object.sort(key = len, reverse = True)



    for object in affected_object:
        short_name = object.split("|")[-1]
        object_type = None
        object_suffix = "grp"
        children = cmds.listRelatives(object, children = True, fullPath = True) or []
            

        if len(children) == 1:
            child = children[0]
            object_type = cmds.objectType(child)
        else:
            object_type = cmds.objectType(object)

        if object_type == "camera":
            continue

        if object_type in object_dictionary:
                
            object_suffix = object_dictionary[object_type]
            
        if object.endswith("_" + object_suffix):
            continue

        new_name = "%s_%s" % (short_name, object_suffix)
        cmds.rename(object, new_name)

        index = affected_object.index(object)
        affected_object[index] = object.replace(short_name,new_name)

    
    return affected_object

rename_selected()