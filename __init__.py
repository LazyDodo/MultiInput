bl_info = {
    "name": "MultiInput",
    "author": (
        "LazyDodo"
     ),
    "version": (0, 0, 1,0),
    "blender": (2, 7, 8),
    "location": "Nodes > Add nodes",
    "description": "Multi Open Cycles Node",
    "warning": "",
    "wiki_url": "",
    "category": "Node"} 

import bpy,nodeitems_utils, glob
from nodeitems_utils import NodeCategory, NodeItem


class ShaderNode_MultiInput(bpy.types.NodeCustomGroup):
    bl_name='ShaderNode_MultiInput'
    bl_label='multi_input'
    bl_icon='NONE'
    
    
    def mypropUpdate(self, context):
        filepath = bpy.path.abspath(self.exportPath)
        last = max(max(max(filepath.rfind("Albedo"), filepath.rfind("Diffuse")),filepath.rfind("_")),filepath.rfind("-"))
        partial = filepath[0:last] + "*.*"
        files = glob.glob(partial)
        bitmaps = []
        for val in files:
            res = bpy.data.images.load(val, check_existing=False)
            lastbit = val[last+1:]
            lastbit = lastbit[0:lastbit.rfind(".")]
            lastbit = self.prettyname(lastbit)
            bitmaps.append([res,lastbit])
        self.getNodetree(self.treename(),bitmaps)
        return None
    
    exportPath = bpy.props.StringProperty(name="Path", subtype='FILE_PATH', update=mypropUpdate)    
    
    def treename(self):
        return self.name;
    
    def prettyname(self, propname):
        basecolorNames = [ "Base Color", "basecolor" , "base color" , "diffuse" ,"color"]
        normalNames = [ "Normal", "normal"]
        heightNames = [ "Height", "height"]
        roughnessNames = [ "Roughness", "roughness"]
        metallicNames = [ "Metallic", "metallic"]
        aoNames = [ "Ambient Occlusion", "ambientocclusion", "ao" ,"AO"]
        dispNames = [ "Displacement", "displacement"]
    
        if (propname in basecolorNames):
            return basecolorNames[0]

        if (propname in normalNames):
            return normalNames[0]

        if (propname in heightNames):
            return heightNames[0]
        
        if (propname in roughnessNames):
            return roughnessNames[0]
        
        if (propname in metallicNames):
            return metallicNames[0]

        if (propname in aoNames):
            return aoNames[0]

        if (propname in dispNames):
            return dispNames[0]
                
        return propname

    
    def init(self, context):
        self.getNodetree(self.treename())
    
    def draw_buttons(self, context, layout):
        layout.label("Node settings")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(self, "exportPath") 
    
    def value_set(self, obj, path, value):
        if '.' in path:
            path_prop, path_attr = path.rsplit('.', 1)
            prop = obj.path_resolve(path_prop)
        else:
            prop = obj
            path_attr = path
        setattr(prop, path_attr, value)

    def createNodetree(self, name, images) :
        self.Tmpnode_tree = bpy.data.node_groups.new(name, 'ShaderNodeTree')
        self.addNode('NodeGroupInput', { 'name':'GroupInput'  })
        self.addSocket(False, 'NodeSocketVector', "Vector" ) 
        outputnode = self.addNode('NodeGroupOutput', { 'name':'GroupOutput'  }) 
        left = 0
        
        for val in images:
            node = self.addNode('ShaderNodeTexImage', { 'name':val[1] })
            self.innerLink('nodes["GroupInput"].outputs[0]', 'nodes["' +val[1]+ '"].inputs[0]') 
            noneColorTypes = [ "Metallic", "Normal", "Roughness","Specular", "Height" ]
            if (val[1] in noneColorTypes):
                node.color_space = "NONE"
            node.image = val[0];
            node.location = left,0
            left = left + 200
            if (val[1] not in [ "Normal"] ):
                sc = self.addSocket(True, 'NodeSocketColor', val[1] ) 
            else:
                sc = self.addSocket(True, 'NodeSocketVector', val[1] ) 
                
            self.innerLink('nodes["' +val[1]+ '"].outputs[0]', 'nodes["GroupOutput"].inputs["' + sc.name + '"]') 
        for val in images:
            sa = self.addSocket(True, 'NodeSocketFloat', val[1] + '_Alpha')
            self.innerLink('nodes["' +val[1]+ '"].outputs[1]', 'nodes["GroupOutput"].inputs["' + sa.name + '"]') 

        outputnode.location = left,0
        self.node_tree = self.Tmpnode_tree

         
    def getNodetree(self, name, images):
            self.createNodetree(name,images)
                   
    def addSocket(self, is_output, sockettype, name):
        #for now duplicated socket names are not allowed
        if is_output==True:
            if self.Tmpnode_tree.nodes['GroupOutput'].inputs.find(name)==-1:
                socket=self.Tmpnode_tree.outputs.new(sockettype, name)
        elif is_output==False:
            if self.Tmpnode_tree.nodes['GroupInput'].outputs.find(name)==-1:
                socket=self.Tmpnode_tree.inputs.new(sockettype, name)
        return socket
       
    def addNode(self, nodetype, attrs):
        node=self.Tmpnode_tree.nodes.new(nodetype)
        for attr in attrs:
            self.value_set(node, attr, attrs[attr])
        return node
   
    def getNode(self, nodename):
        if self.Tmpnode_tree.nodes.find(nodename)>-1:
            return self.Tmpnode_tree.nodes[nodename]
        return None
   
    def innerLink(self, socketin, socketout):
        SI=self.Tmpnode_tree.path_resolve(socketin)
        SO=self.Tmpnode_tree.path_resolve(socketout)
        self.Tmpnode_tree.links.new(SI, SO)
       
    def free(self):
        if self.Tmpnode_tree.users==1:
            bpy.data.node_groups.remove(self.Tmpnode_tree, do_unlink=True)
 
  
class ExtraNodesCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'ShaderNodeTree' and
                context.scene.render.use_shading_nodes)
 
node_categories = [
    ExtraNodesCategory("SH_MultiInput", "MultiInput", items=[
        NodeItem("ShaderNode_MultiInput")
        ]),
    ]
      
def register():
    bpy.utils.register_class(ShaderNode_MultiInput)
    nodeitems_utils.register_node_categories("SH_MultiInput", node_categories)
 
 
def unregister():
    nodeitems_utils.unregister_node_categories("SH_MultiInput")
    bpy.utils.unregister_class(ShaderNode_picswitch)

if __name__ == "__main__":
    register()
   