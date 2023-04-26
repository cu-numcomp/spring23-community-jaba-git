import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from copy import deepcopy
import scipy.ndimage
from scipy.interpolate import UnivariateSpline
from astropy.io import fits


class Data:
    def __init__(self,filename='NoFile'):
        self.filename = filename
        self.ndim = 0 
        self.x = []
        self.nx = 0
        self.y = []
        self.ny = 0
        self.z = []
        self.nz = 0
        self.array = []
        self.header = []
        self.nxa = 0
        self.nya = 0
        
    def xline(self,xmin,xmax,nx):
        self.nx = nx
        self.ndim = 1
        self.x = np.linspace(xmin,xmax,nx)

    def yline(self,a,b):
        if(self.ndim == 1):
            self.ny = self.nx
            self.y = a + b*self.x
        else:
            print("x value not one dimensional")

    def plotxy(self):
        plt.cla()
        plt.title(self.filename)
        plt.plot(self.x,self.y)
        plt.show()

    def plotpoints(self):
        plt.cla()
        plt.title(self.filename)
        #plt.plot(self.x,self.y)
        plt.scatter(self.x, self.y, s=2, marker='o', c='black')
        plt.show()
        
    def MyHistogram(self,bins=100,range=(-10.,10.)):
        hi=np.histogram(self.x,bins=bins,range=range)
        hy=np.array(hi[0])
        hx=np.array(hi[1])
        hx=hx[1:]
        f, ax = plt.subplots(1)
        plt.plot(hx,hy,drawstyle='steps')
        ax.set_ylim(ymin=0)
        plt.show(f)

    def GetFits(self, filename):
        self.filename = filename
        hdul = fits.open(filename)
        self.array = fits.getdata(filename)
        self.header = hdul[0].header
        sh = np.shape(self.array)
        self.nxa = sh[0]
        self.nya = sh[1]
        self.ndim = 2
            
    def GetTableData(self, filename):
        self.filename = filename
        data_array=np.genfromtxt(filename)
        s = data_array.shape
        if len(s) == 1 :
            self.x= data_array
            self.nx = s[0]
        elif len(s) == 2 :
            self.x = data_array[:, 0]
            self.y = data_array[:, 1]
            self.nx = s[0]
            self.ny = s[0]
        else:
            print("No Data - Number of dimensions not covered")

    def WriteTableData(self,filename='test.txt'):
        f = open(filename,"w")
        if self.ny == 0:
            for i in range(0,self.nx):
                f.write('%8.4f\n' % self.x[i] )
        else:
            for i in range(0,self.nx):
                f.write('%8.4f  %8.4f\n' % (self.x[i],self.y[i]))
        f.close()

    def Quicklook(self):
        if (self.nx == 0):
            print("Whoops! No Data")
            return
        if self.ny == 0:
            plt.plot(self.x, c='black')
        else:
            plt.scatter(self.x, self.y, s=2, marker='o', c='black')
        plt.show()
        print("length of x list is ",len(self.x), "items")
        
    def ReadInteger16(self,filename,nxa=256,nya=256):
        self.filename = filename
        data = np.fromfile('m33.dat', dtype='i2')
        self.array = np.reshape(np.array(data),(nxa,nya))
        self.ndim = 2
        self.nxa = nxa
        self.nya = nya
        
    def WriteFloat64(self,filename="test.dat"):
        self.filename = filename
        f= open(self.filename,"w+")
        self.x.tofile(f)
        f.close()

    def ReadFloat64(self,filename="test.dat",nxa=256,nya=256):
        self.filename = filename
        f= open(self.filename,"r")
        self.x=np.fromfile(f,'f8')
        f.close()

    def ReadExcelColumn(self, filename, sheetname, columnname):
        self.filename = filename
        e = pd.ExcelFile(filename)
        ep = e.parse(sheetname)
        df=ep[columnname]
        self.x = df.values
        self.nx = len(self.x)
        self.ndim = 1
        
    def WriteExcelColumn(self, filename):
        #df = pd.DataFrame(data=self.x)
        df = pd.DataFrame({"x": D.x,"y": D.y})
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer)
            
    def MyImage(self,cmap='gray',cb=False, cn=False, smooth=0, cliptop=-1.):
        if cliptop > 0.:
            ar=np.clip(self.array,0.,cliptop)
        else:
            ar = self.array
        plt.imshow(ar, interpolation='none', cmap=cmap)
        if smooth > 0:
            data2=scipy.ndimage.filters.gaussian_filter(ar,smooth,mode='nearest')
        if cb == True:
            plt.colorbar()
        if cn == True:
            plt.contour(data2)
        plt.show()
        
    def MySpline(self,cmap='gray',cb=False, cn=False, smooth=1):
        spl=UnivariateSpline(self.x,self.y,s=0)
        return(spl)

    def SimData(self, npt=100, rand = 'Uniform',xbar=0.,sigma=1. ):
        self.ndim = 1
        self.nx = npt
        if rand == 'Poisson':
            self.x = np.random.poisson(self.x)
        if rand == 'Gauss':
            self.x = np.random.normal(size=npt,loc=xbar,scale=sigma)
        if rand == 'Uniform':
            self.x = np.random.uniform(size=npt)


    def BinArray(self,ar,nbins=100,xmin=0.,xmax=99.):
        binsize = (xmax-xmin)/nbins
        self.x = np.arange(nbins)*binsize+binsize/2.+xmin
        self.y = np.zeros(nbins)
        for x in ar:
            binnum = int(np.floor((x-xmin)/binsize))
            if (binnum >= 0) and (binnum < nbins): self.y[binnum] += 1
        f, ax = plt.subplots(1)
        plt.plot(self.x,self.y,drawstyle='steps')
        ax.set_ylim(ymin=0)
        plt.show(f)


