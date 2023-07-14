
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



starsA = list(range(0,100))#estrelas Inesploradas (em Aberto)
starsF = [0]# estrelas exploradas

#Pega primeira posição
last = starsA.pop(0)
#Enquanto existirem estrelas para explorar

while starsA:
  print("===\n")
  menor = starsA[0]
  for i in starsA:
    posma = [x1-x2 for x1, x2 in zip(pos[last] , pos[i])]
    posme = [x1-x2 for x1, x2 in zip(pos[last] , pos[menor])]
    print(i)
    print("[",np.linalg.norm(posma),"]")
    if (np.linalg.norm(posma)) < (np.linalg.norm(posme)):
      menor = i
  print("menor:")
  print(menor)
  print("[",np.linalg.norm([x1-x2 for x1, x2 in zip(pos[last] , pos[menor])]),"]")
  last = menor
  starsA.remove(menor)
  starsF.append(menor)
#Volta pro sol
starsF.append(0)
print(starsF)

dist = 0
x = starsF[0]
for i in starsF:
  dist += np.linalg.norm([x1-x2 for x1, x2 in zip(pos[x] , pos[i])])
print(dist)

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
      bpy.context.object.data.bevel_depth = 0.3 
      
      #Cor
      matr = bpy.data.materials.new("Red")
      matr.diffuse_color = (1,colorChange*starsF.index(ind)/(len(starsF)),0,1)
      if ind == 0:
          matr.diffuse_color = (1,colorChange*101/(len(starsF)),0,1)
      bpy.context.object.active_material = matr
      
      inda = (c*10)
      print(inda)
      bpy.context.object.hide_viewport = True
      bpy.context.object.keyframe_insert('hide_viewport',frame = 0)
      bpy.context.object.keyframe_insert('hide_viewport',frame = inda+12)
      bpy.context.object.hide_viewport = False
      bpy.context.object.keyframe_insert('hide_viewport',frame = inda)
      c+=1

      
 



  
  #Cria esfera
  bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(pos[ind][0], pos[ind][1], pos[ind][2]), scale=(0.2, 0.2, 0.2))
  bpy.context.object.name = str(i)

  
  #Muda cor
  '''
  bpy.ops.material.new()
  bpy.context.object.active_material.name = "red"+str(c)
  bpy.data.materials["red"+str(c)].node_tree.nodes["Principled BSDF"].inputs[19].default_value = (1,ind/(colorChange*len(starsF)),0,1)
  bpy.data.materials["red"+str(c)].node_tree.nodes["Principled BSDF"].inputs[20].default_value = 126.7
'''

   


#Fecha Arquivo
file.close()


'''
#cria plano
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
obj = bpy.context.object# seleciona plano
      
#Entra edimode
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.delete(type='VERT')#deleta vertices do plano

me = obj.data
bm = bmesh.from_edit_mesh(me)
      
#cria vertices
v1 = bm.verts.new((pos[-1][0],pos[-1][1],pos[-1][2]))
v2 = bm.verts.new((pos[0][0],pos[0][1],pos[0][2]))
      
#cria arestas
bm.edges.new((v1, v2))
#sai edimode
bmesh.update_edit_mesh(obj.data)
bpy.ops.object.editmode_toggle()
      
#Converte pra curva e seta atributos para ser visivel
bpy.ops.object.convert(target='CURVE')
bpy.context.object.data.bevel_depth = 0.26
matr = bpy.data.materials.new("Red")
matr.diffuse_color = (1,colorChange,0,1)
bpy.context.object.active_material = matr'''