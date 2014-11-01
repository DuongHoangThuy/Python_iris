import cv2,os
import cv2.cv as cv
import numpy as np

path = "image"
path0 = path+"/iris"
path1 = path0+"/test"
path2 = path0+"/test_iris_pupil"
path3 = path0+"/iris_pupil"
path4 = path0+"/normalization_Xp"
path41 = path0+"/normalization_p"
path5 = path0+"/LBP_Xp"
path51 = path0+"/LBP_p"
path6 = path0+"/iris_pupil_c"
filetype = "tiff"

paths_ = [path0,path1,path2,path3,path4,path5,path41,path51,path6]

LBPsize_h=200;LBPsize_w=200;th=5

def createbimage(w,h,n):
    data = np.zeros( (w,h,n), dtype=np.uint8)
    return data

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

def thresholded(center, pixels): 
    out = [] #create empty list/
    for a in pixels: #while pixel is not zero /
        if a >= center: 
            out.append(1) #add element at the end of the list/
        else:
            out.append(0)
    return out

def get_pixel_else_0(l, idx, idy, default=0): #verify if that pixel have value or not/
    try:
        return l[idx,idy] #return value and list/
    except IndexError:
        return default

def LBP(imagefilename):#local Binary Pattern
    img = cv2.imread(imagefilename, 0) #read image and return matrix of the image/
    transformed_img = cv2.imread(imagefilename, 0)
    for x in range(0, len(img)):
        for y in range(0, len(img[0])):
            center        = img[x,y] #save list element depend of x and y/
            top_left      = get_pixel_else_0(img, x-1, y-1) #goto function get_pixel_else_0 and return value save as top_left/
            top_up        = get_pixel_else_0(img, x, y-1)
            top_right     = get_pixel_else_0(img, x+1, y-1)
            right         = get_pixel_else_0(img, x+1, y )
            left          = get_pixel_else_0(img, x-1, y )
            bottom_left   = get_pixel_else_0(img, x-1, y+1)
            bottom_right  = get_pixel_else_0(img, x+1, y+1)
            bottom_down   = get_pixel_else_0(img, x,   y+1 )
            values = thresholded(center, [top_left, top_up, top_right, right, bottom_right,bottom_down, bottom_left, left])
            weights = [1, 2, 4, 8, 16, 32, 64, 128] #create list/
            res = 0 
            for a in range(0, len(values)): #for loop/
                res += weights[a] * values[a]
            transformed_img.itemset((x,y), res) #Insert scalar into an array/
    return transformed_img

def inverte(imagem):
    imagem = 255-imagem
    return imagem

def getNewEye(path,extension): #insert name list and postion; return image name/
    files = os.listdir(path) #list all the filename in that directory/
    files1 = [i for i in files if i.endswith(extension)] #save filename into array/
    return files1

def getCirclez(img):
    i=11
    while 1:
        img1 = cv2.medianBlur(img,9)
        img1 = cv2.medianBlur(img1,i)
        h=img.shape[0];w=img.shape[1]
        circles = cv2.HoughCircles(img1,cv.CV_HOUGH_GRADIENT,1,h,param1=60,param2=30,minRadius=40,maxRadius=0)
        #print circles,i
        if circles == None:
            i=i-2
        elif circles!=None or i==1:
            break
    return circles

def getPolar2CartImage(image,rad=0): #image from polar to cart
    imgSize = cv.GetSize(image)
    if rad==0:
        rad =int(imgSize[0]/2.0)
    c = (float(imgSize[0]/2.0), float(imgSize[1]/2.0)) #centre/
    imgRes = cv.CreateImage((rad*2,int(360)), 8, 3)
    cv.LogPolar(image,imgRes,c,60.0, cv.CV_INTER_LINEAR+cv.CV_WARP_FILL_OUTLIERS)
    return imgRes

def drawc(img,circles):
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
    return img,i

def crop_largescale_save(img,l,i,path,choice=0):
    imgcrop=img[i[1]-i[2]:i[1]+i[2] , i[0]-i[2]:i[0]+i[2]]
    w,h=imgcrop.shape[:2]
    imgcrop1 = cv2.resize(imgcrop, (h*5, w*5))
    imgcrop1 = cv2.GaussianBlur(imgcrop1,(5,5),0)
    imgcrop1 = cv2.medianBlur(imgcrop1,5)
    imgcrop1 = cv2.bilateralFilter(imgcrop1,5,75,125)
    if choice == 1:
        #imgcrop1 = cv2.equalizeHist(imgcrop1)
        pass
    cv2.imwrite(path+"/iris_pupil_"+str(l)+".jpg",imgcrop1)

def display(img):
    try:
        cv2.imshow('test',img)
    except:
        cv.ShowImage('test',img)
    cv2.waitKey(500)
    cv2.destroyAllWindows()

def LogPolarf(path_1,filetype_1,name,path_2,filetype_2):#
    print "LogPolar:"
    a = getNewEye(path_1,"."+filetype_1)
    for l in range(len(a)):
        print a[l]
        img = cv.LoadImage(path3+"/"+a[l])
        imgpolar = getPolar2CartImage(img)
        cv.SaveImage(path_2+"/"+name+str(l)+"."+filetype_2,imgpolar)

def LBPf(path_1,filetype_1,name,path_2,filetype_2):
    print "LBP:"
    a = getNewEye(path_1,"."+filetype_1)
    for l in range(len(a)):
        print a[l]
        imageLBP = LBP(path_1+"/"+a[l])
        h,w = imageLBP.shape[:2]
        imageLBP = cv2.resize(imageLBP, (LBPsize_h,LBPsize_w))
        cv2.imwrite(path_2+"/"+name+str(l)+"."+filetype_2,imageLBP)

def mainf():
    print "Image Conversion (iris+pupil): "
    a=getNewEye(path,"."+filetype)
    for l in range(len(a)):
        fl=path+"/"+a[l]
        print fl+" is processing"
        img = cv2.imread(fl,0);img_=cv2.imread(fl,0)
        img1 = cv2.imread(fl);img2 = cv2.imread(fl)
        h=img.shape[0];w=img.shape[1]
        circles = getCirclez(img)
        img1,i = drawc(img1,circles)
        cv2.imwrite(path1+"/test"+str(l)+".jpg",img1)
        crop_largescale_save(img1,l,i,path2)
        crop_largescale_save(img2,l,i,path6)
        crop_largescale_save(img_,l,i,path3,1)
    LogPolarf(path3,"jpg","iwp",path4,"jpg")
    LBPf(path4,"jpg","iwp",path5,"jpg")

def mainf2():
    print "Image Conversion (iris-pupil):"
    a = getNewEye(path6,".jpg")
    for l in range(len(a)):
        fl=path6+"/"+a[l]
        print fl+" is processing"
        img = cv2.imread(fl,0);img1 = cv2.imread(fl)
        h,w=img.shape[:2];i=30;g=25
        img = cv2.medianBlur(img,9)
        c_h=int(h/2);c_w=int(w/2)
        while 1:
            gray=int(0.5*(img[c_h,c_w]+img[c_h+1,c_w+1]))
            if ((gray>=g-th) and (gray<g+th)):
                c_h=c_h+1;c_w=c_w+1
            else:
                break
            i+=1
        cv2.circle(img,(h/2,w/2),2,(0,255,0),i*2)
        cv2.circle(img1,(h/2,w/2),2,(0,255,0),3)
        cv2.circle(img1,(h/2,w/2),i,(255,255,255),3)
    LogPolarf(path3,"jpg","ixp",path41,"jpg")
    LBPf(path41,"jpg","ixp",path51,"jpg")


errorhanding()                   
mainf()
mainf2()
print "~~end~~"

