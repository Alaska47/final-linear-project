from PIL import Image
import os
import sys

original = str(sys.argv[1])
filename = str(sys.argv[2])
type = str(sys.argv[3])
iterations = int(sys.argv[4])

if filename in os.listdir("."):
   os.remove(filename)

shwetark = Image.open(original).convert("LA")
shwe = shwetark.load()

n = Image.new("RGB", shwetark.size, "white")
pixels = n.load()

kernels = {"identity":[[0,0,0],[0,1,0],[0,0,0]], "edge":[[-1,-1,-1],[-1,8,-1],[-1,-1,-1]], "sharpen":[[0,-1,0],[-1,5,-1],[0,-1,0]], "blur":[[.0625,.125,.0625],[.125,.25,.125],[.0625,.125,.0625]]}

def get_image_matrix(abc,pix):

   a = [[],[],[]]
   f = [-1,0,1]
   i = 0
   for ba in f:
      for ab in f:
         a[i].append(pix[abc[0]+ab,abc[1]+ba][0])
      i+=1
   return a

def convolution(a,b):
   sum = 0
   new_a = []
   for x in range(2, -1, -1):
      new_a.append(a[x][::-1])
   for x in range(len(new_a)):
      st = new_a[x]
      for y in range(len(st)):
         sum += new_a[x][y] * b[x][y]
   return sum

print('\n'.join(' '.join(str(y) for y in x) for x in kernels[type]))

width, height = shwetark.size

for x in range(1, width-1):
   for y in range(1, height-1):
      a = get_image_matrix((x,y), shwe)
      b = kernels[type]
      c = int(convolution(a,b))
      if(c < 0): c = 0
      pixels[x,y] = (c,c,c)

print("Iteration 1")

if(iterations > 1):
   for z in range(2, iterations + 1):
      for x in range(1, width-1):
         for y in range(1, height-1):
            a = get_image_matrix((x,y), pixels)
            b = kernels[type]
            c = int(convolution(a,b))
            if(c < 0): c = 0
            pixels[x,y] = (c,c,c)
      print("Iteration " + str(z))

n.save(filename, "PNG")
