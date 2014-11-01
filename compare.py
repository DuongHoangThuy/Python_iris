import cv2,os,Image
import numpy as np

path = "image/iris"
path1 = path+"/LBP_p"
path2 = path+"/LBP_Xp"

filetype=".jpg"

paths_ = [path2]

def getNewEye(path,extension): #insert name list and postion; return image name/
    files = os.listdir(path) #list all the filename in that directory/
    files1 = [i for i in files if i.endswith(extension)] #save filename into array/
    return files1

def errorhanding():
    for x in range(len(paths_)):
        try:
            os.remove(paths_[x])
        except:                 
            pass                
        try:
            os.mkdir(paths_[x]) 
        except (WindowsError or IOError):
            pass

def display(img):
    try:
        cv2.imshow('test',img)
    except:
        cv.ShowImage('test',img)
    cv2.waitKey(500)
    cv2.destroyAllWindows()

def writefile(filename,data):
    f = open(filename,'w')
    f.write(data)
    f.close();

def hamdist(s1, s2): #hamming distance method
    if len(s1)!=len(s2): #determine size of array/
        raise ValueError("Undefined for sequences of unequal length")
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

def compare(image1,image2):
    arr1=dimensionred(image1)
    arr2=dimensionred(image2)
    image=Image.open(image1)
    width,height=image.size
    totalsize = width*height
    result=hamdist(arr1,arr2)
    result=((totalsize - (result*1.0))/ totalsize ) *100
    return result

def dimensionred(image):#convert 2D array to 1D array
    image1=Image.open(image) #read Image /
    width,height=image1.size #read heigh and width of the image/
    arr1=[]
    image1 = np.asarray(image1)
    image1 = image1.ravel()
    image1 = image1.tolist()
    i=0
    for y in range(height):
        arr1.append(image1[i])
        i+=1
    return arr1

#errorhanding()
print "compare two files"
a = getNewEye(path1,filetype)
b = getNewEye(path2,filetype)
count=0;result=""
for x in range(len(b)):
    for y in range(len(a)):
        print "compare between "+a[x]+" and "+b[y]
        result1 = compare(path1+"/"+a[x],path2+"/"+b[y])
        result = result+str(count)+",% of similarity ="+str(result1)+" ,comparing with "+a[y]+","+b[x]+"\n"
        count+=1
print "end conversion, "+str(count+1)+" files is convert."
writefile('result.txt',result)


