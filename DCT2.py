from time import process_time 
start = process_time()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from PIL import Image
import sys      
import subprocess
end = process_time()

print("import: ", end - start)
    
def corte(img, x, y, n):
    cut = [[img[x+i][y+j] for j in range(n)] for i in range(n)]
    return np.array(cut)

def array_to_img(array):
    img = []
    x = 0
    for i in range(int(len(array)/8)):
        aux = []
        for j in range(8):
            aux.append(array[x])
            x+=1
        img.append(aux)
    return np.array(img)

def on_zero(img, valor):
    size = img.shape
    if(valor == True):
        return np.array([[img[i][j]-128 for j in range(size[0])] for i in range(size[1])])
    else:
        return np.array([[img[i][j]+128 for j in range(size[0])] for i in range(size[1])])
        

def quantizacao(img, matriz, op):
    if(op == 1):
        return ([[img[i][j]/matriz[i][j] for j in range(8)]
                          for i in range(8)])
    else:
        return ([[img[i][j]*matriz[i][j] for j in range(8)]
                          for i in range(8)])

def codifica(img):
    image = on_zero(img, True)
    aux = T @ image
    aux = aux @ TT    
    return quantizacao(aux, Q, 1)

    
def decodifica(img):
    image = quantizacao(img, Q, 0)
    image = TT @ image
    image = image @ T
    image = np.rint(image)
    return on_zero(image, False)
    

def put_chunk(img, chunk, i, j):
    for u in range(8):
        for v in range(8):
            img[i+u][j+v] = chunk[u][v]

array = [
    52, 55, 61, 66, 70, 61, 64, 73,
    63, 59, 55, 90, 109, 85, 69, 72,
    62, 59, 68, 113, 144, 104, 66, 73,
    63, 58, 71, 122, 154, 106, 70, 69,
    67, 61, 68, 104, 126, 88, 68, 70,
    79, 65, 60, 70, 77, 68, 58, 75,
    85, 71, 64, 59, 55, 61, 65, 83,
    87, 79, 69, 68, 65, 76, 78, 94,
]

Q = [
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99],
]
start = process_time()
################# RECEBIMENTO DO ARQUIVO

if len (sys.argv) != 2 :
    try:
        original = mpimg.imread("original.jpg")
    except:
        print("\nImagem não encontrada!\n")
        sys.exit (1)
else:
    try:
        original = mpimg.imread(sys.argv[1])
    except:
        print("\nJPG não encontrado\n")
        try:
            converte = subprocess.Popen(["python3", "converte.py", sys.argv[1]])
            converte.wait()
            print("Conversão de pgm para jpg realizada!\n")
            original = mpimg.imread("in.jpg")
        except:
            print("\nImgem não é .jpg nem .pgm!\n")

################# TAMANHO X Y          
size = original.shape

################# PREPARA MATRIZ 
T = np.zeros([8,8])
for i in range(8):
    for j in range(8):
        if i == 0:
            T[i,j] = (1/math.sqrt(8))
        else:
            T[i,j] = (0.5*math.cos(((2*j+1)*i*math.pi)/16))        
TT = T.transpose()

#plt.imshow(original, cmap='gray')
#plt.pause(1)

################# JPG RGB -> BLACK AND WHITE
try:
    baw = np.array([[original[i][j][2] for j in range(size[0])] for i in range(size[1])])
except:
    baw = np.copy(original)
end = process_time()
print("out of loop: ", end - start)
#plt.imshow(baw, cmap='gray')
#plt.pause(1)
    
################# LOOP PRINCIPAL
start = process_time()
for i in range(int(size[0]/8)):
    for j in range(int(size[1]/8)):
        chunk = codifica(corte(baw, i*8, j*8, 8)) # CODIFICAÇÃO DE UM CORTE 8X8
        chunk = decodifica(chunk)
        put_chunk(baw, chunk, i*8, j*8)
end = process_time()

################ RESULTADO
plt.imshow(baw, cmap='gray')
print("loop time: ", end - start)
################ SALVA IMAGEM
im = Image.fromarray(baw)
im.save("out.jpg")









