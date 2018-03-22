import pymel.core as pm

class MayaMethod():
    result_message = ''
    delete_list = []

    def __init__(self):
        print('init maya method')

    def check_non_manifold_geometry(self):
        self.result_message = ''
        geometry = pm.ls(geometry=True)
        transforms = pm.listRelatives(geometry, p=True, path=True)
        result_objects = []

        for it in transforms:
            nmv = pm.polyInfo(it, nmv=True)
            nme = pm.polyInfo(it, nme=True)
            lf = pm.polyInfo(it, lf=True)
            is_vertex = self.check_null_list(nmv, 'non-manifold vertex')
            is_edge = self.check_null_list(nme, 'non-manifold edges')
            is_face = self.check_null_list(lf, 'lamina faces')

            if (is_vertex or is_edge or is_face) is True:
                result_objects.append(it)
        pm.select(result_objects)
        return self.result_message

    def check_null_list(self, list, name):
        result = False
        if list is not None and len(list) >0:
            result = True
            self.result_message += name + ':\n'
            for it in list:
                self.result_message += '    '+it + '\n'
        else:
            print(name + 'is empty!!!')

        return result

    def is_default_shader(self):
        self.result_message = ''
        result_objects = []
        geometry = pm.ls(geometry=True)

        for it in geometry:
            shading_engine = pm.listConnections(it, type='shadingEngine')
            for se in shading_engine:
                materials = pm.listConnections(se, type='lambert')
                for mat in materials:
                    if str(mat) == 'lambert1':
                        result_objects.append(it)

        for it in result_objects:
            self.result_message += it + '\n'
        pm.select(result_objects)
        return self.result_message

    def check_duplicate_objects(self):
        self.result_message = ''
        origin = []
        transforms = pm.ls(tr=True)
        for it in transforms:
            origin.append(self.get_node_name(it))
        duplicateList = []
        oldList = []
        for it in origin:
            if it in oldList:
                duplicateList.append(it)
            else:
                oldList.append(it)

        for it in duplicateList:
            self.result_message += it + '\n'
        pm.select(pm.ls(duplicateList))
        return self.result_message

    def get_node_name(self, value):
        parent = pm.listRelatives(value, parent=True)
        if parent == [] or parent is None:
            return value
        else:
            last_idx = value.rfind('|')
            result = value[last_idx+1:]
            return result

    def check_empty_groups(self):
        transforms = pm.ls(type='transform', long=True)
        print(transforms)
        self.result_message = ''
        self.delete_list = []

        for it in transforms:
            children = pm.listRelatives(it, c=True, f=True)
            if children is None or children == []:
                print(it + "has no child node.")
                self.remove_parents_recursively(it)

        if self.delete_list is not []:
            pm.select(self.delete_list)
            for it in self.delete_list:
                self.result_message += it + '\n'
            pm.delete(self.delete_list)
            self.delete_list = []
        return self.result_message

    def remove_parents_recursively(self, transform):
        self.delete_list.append(transform)
        parent = pm.listRelatives(transform, p=True)
        if parent == [] or parent is None:
            print('this node is root')
        else:
            self.remove_parents_recursively(parent[0])
