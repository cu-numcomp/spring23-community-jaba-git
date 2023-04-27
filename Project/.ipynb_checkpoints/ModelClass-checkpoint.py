import numpy as np
import matplotlib.pyplot as plt

class Model:
    def __init__(self,name="undefined"):
        self.name = name
        self.npt = 0
        self.x = []
        self.y = []
        self.z = []
        self.cumy = []
        self.dx = []
        self.area = 1.
        self.func = []
        
    def Xarray(self,npt=10,xmin=0.,xmax=1.):
        self.npt = npt
        self.x = np.linspace(xmin, xmax, npt, endpoint=False)
        self.dx = (xmax-xmin)/(npt)
        
    def PlotModel(self,xtitle="",ytitle=""):
        plt.title(self.name)
        plt.plot(self.x,self.y,linestyle='steps')
        plt.xlabel(xtitle, fontsize=14)
        plt.ylabel(ytitle, fontsize=14)
        plt.show()
        
    def Dice(self):
        self.Xarray(npt=11,xmin=2,xmax=13)
        self.y =   np.array([1.,2.,3.,4.,5.,6.,5.,4.,3.,2.,1.])/36.
        self.npt = len(self.y)
        self.dx = self.y *0. +1.
        self.cumy = self.y * 0.
        self.cumy[0] = self.y[0]
        for i in range(1,self.npt):
            self.cumy[i] = self.cumy[i-1]+self.y[i]

    def Line(self,a=0,b=0):
        self.y = a + self.x * b
        self.cumy = self.y * 0.
        self.cumy[0] = self.y[0]
        for i in range(1,self.npt):
            self.cumy[i] = self.cumy[i-1]+self.y[i]

    def Normal(self,xbar=0.,sigma=1.,ytot=1.):
        self.y = ytot*self.dx*np.exp(-(self.x-xbar)*(self.x-xbar)/2./sigma/sigma)/sigma/np.sqrt(2.*np.pi)
        
    def SimData(self, rand = 'Uniform',xbar=0.,sigma=1., noise = 1., amp_factor = 0.1):
        # define amplitude factor
        amp_factor = amp_factor
        #compute amplitude of original data
        amp = np.max(self.y) - np.min(self.y)
        # compute noise scale factor
        noise_scale = amp_factor * amp
        if rand == 'Poisson':
            self.y = noise_scale * np.random.poisson(lam = noise, size = len(self.y)) 
            # print(self.y)
        if rand == 'Gauss':
            self.y = np.random.normal(size=npt,loc=self.y,scale=sigma)
        if rand == 'Uniform':
            self.y = np.random.uniform(size=npt)
        
    def Planck(self, T = 5000., I = 1.):
        lam = self.x*1.e-9
        h = 6.626e-34    # Boltzmann 
        c = 2.998e8      # light
        k = 1.38e-23
        self.y = I*2.*h*c*c/lam/lam/lam/lam/lam/(np.exp(h*c/lam/k/T) - 1.)
    
    def Blackbody(self, star, inst, time = 1.):
        self.name = star.name
        self.x = inst.lam
        self.npt = len(self.x)
        self.Planck(T=star.T)
        self.y *= np.pi * 4. * np.pi * star.r**2 * 1.e-9
        self.y /= 4.*np.pi*(star.dist*3.e16)**2
        self.y *= inst.area
        self.y *= inst.lambin
        self.y *= time
        self.sigma = np.sqrt(self.y)
    
    def BlackbodyPhotons(self, star, inst, time = 1):
        h = 6.626e-34    # Boltzmann 
        c = 2.998e8      # light
        self.Blackbody(star, inst, time)
        self.y /= (h*c)/(self.x*1.e-9)
        self.sigma = np.sqrt(self.y)