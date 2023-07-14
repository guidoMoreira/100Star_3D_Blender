
import bpy, bmesh
import numpy as np

from pathlib import Path

#path = some_object.filepath # as declared by props
path = str(bpy.context.space_data.text.filepath)


#pega caminho de si mesmo
selfp = Path(bpy.path.abspath(path))

#Pega diretório da pasta
pathdir = Path(selfp).resolve().parent

print(pathdir)
#Pega arquivo posStars.txt
pfile = str(pathdir) + "\posStars.txt"

#Pega caminho do arquivo

    #Abre arquivo
with open(pfile) as file:
        #) # le texto do arquivo
        with open(pfile) as f:
            pos = []
            for line in f: # read rest of lines
                pos.append([float(x) for x in line.split()])


#Função calcular distância
def calcdist(start, end):
  return np.linalg.norm([x1-x2 for x1, x2 in zip(pos[start] , pos[end])])

#Função calcular distância
def getMenor(start,Astar,ig = []):
  ig.append(start)#não tentar voltar para o começo
  
  menor = Astar[0]
  for i in Astar:
    dm = 0
    dn = 0
      
    if i not in ig:
      dm += calcdist(start,menor)
      dn += calcdist(start,i)
      if dn < dm:
        menor = i
        dm = dn
  return [menor, dm]


starsA = list(range(0,100))#estrelas Inesploradas (em Aberto)
starsF = [0]# estrelas exploradas

#ALGORITMO GULOSO
#Pega primeira posição
last = starsA.pop(0)
#Enquanto existirem estrelas para explorar
while starsA:
  #print("===\n")
  menor = getMenor(last,starsA)
  print("menor opção local:")
  print(menor)
  #print("[",calcdist(last , menor[0]),"]")
  last = menor[0]
  starsA.remove(menor[0])
  starsF.append(menor[0])
#Volta pro sol
starsF.append(0)
print("Caminho escolhido: ",starsF)

#calcula distância percorrida pelo algoritmo
dist = 0
x = starsF[0]
for i in starsF:
  dist += calcdist(x, i)
  x = i
print("Distância do algoritmo",dist)
#============================================


#Seleciona objetos do blender e deleta eles
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)



colorChange = 1

file = open('Guloso.txt','w')
c = 0
for i in starsF:
  #Salav caminho escolhido no arquivo
  file.write(str(i)+" ")
  
  #Pega index do objeto
  ind = i

  if ind > 0 or c>0:
      bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
      obj = bpy.context.object
      

      #Entra edimode
      bpy.ops.object.editmode_toggle()
      bpy.ops.mesh.delete(type='VERT')

      me = obj.data
      bm = bmesh.from_edit_mesh(me)
      
      if i != 0: 
        antes = starsF[starsF.index(i)-1]
      else:
        antes = starsF[starsF.index(i)-2]
      print(antes," -> ", i)

      obj.name =str(ind)+ " : "+str(antes)+" -> "+str(i)
      v1 = bm.verts.new((pos[antes][0],pos[antes][1],pos[antes][2]))
      v2 = bm.verts.new((pos[ind][0],pos[ind][1],pos[ind][2]))
      
      bm.edges.new((v1, v2))
      #sai edimode
      bmesh.update_edit_mesh(obj.data)
      bpy.ops.object.editmode_toggle()
      
      #Converte pra curva e seta atributos para ser visivel
      bpy.ops.object.convert(target='CURVE')
      bpy.context.object.data.bevel_depth = 0.1
      
      #Cor
      matr = bpy.data.materials.new("trail"+str(i))
      bpy.context.object.active_material = matr
       
      bpy.context.object.active_material.use_nodes = True
      bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (1,colorChange*starsF.index(ind)/(len(starsF)),0,1)
      if ind == 0:
           bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (1,colorChange*101/(len(starsF)),0,1)
      
      bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 250
      
      inda = (c*10)
      print(inda) 
      bpy.context.object.hide_viewport = True
      bpy.context.object.hide_render = True
      bpy.context.object.keyframe_insert('hide_viewport',frame = 0)
      bpy.context.object.keyframe_insert('hide_viewport',frame = inda+12)
      bpy.context.object.keyframe_insert('hide_render',frame = 0)
      bpy.context.object.keyframe_insert('hide_render',frame = inda+12)
      bpy.context.object.hide_viewport = False
      bpy.context.object.hide_render = False
      bpy.context.object.keyframe_insert('hide_viewport',frame = inda)
      bpy.context.object.keyframe_insert('hide_render',frame = inda)
      
      #Cria esfera
      bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(pos[ind][0], pos[ind][1], pos[ind][2]), scale=(0.2, 0.2, 0.2))
      bpy.context.object.name = str(i)#Muda nome da esfera
      
      #Cria material para estrela
      mt = bpy.data.materials.new("star"+str(i))
      bpy.context.object.data.materials.append(mt)#Associa material a estrela
      #Criar animação da luz da estrela
      bpy.context.object.active_material.use_nodes = True
      bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[19].default_value = (1,colorChange*starsF.index(ind)/(len(starsF)),0,1)
      
      bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 50
      bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[20].keyframe_insert(data_path="default_value", frame=inda-12)
      bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[20].keyframe_insert(data_path="default_value", frame=inda+12)
      
      bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[20].default_value = 10000
      bpy.context.object.active_material.node_tree.nodes["Principled BSDF"].inputs[20].keyframe_insert(data_path="default_value", frame=inda)

      c+=1


#Fecha Arquivo
file.close()
