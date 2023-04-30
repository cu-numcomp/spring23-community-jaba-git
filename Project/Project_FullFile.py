import numpy as np  
import matplotlib.pyplot as plt
from astropy import modeling
from astropy.modeling.polynomial import Polynomial1D, Chebyshev1D, Legendre1D, Hermite1D
from astropy.modeling import fitting
import time
# these classes are made for astronomy data analysis; come from ASTR 3800
import ModelClass as mc
import StatsClass as sc
import DataClass as dc


# create instrument and star class for use in creating model blackbody spectra
class Instrument:
    def __init__(self, name = 'Unnamed', nlam = 100, lam_min = 100., lam_max = 1000., area = 1.):
        self.name = name
        self.nlam = nlam
        self.lam_min = lam_min
        self.lam_max = lam_max
        self.lam = np.linspace(lam_min, lam_max, nlam)
        self.lambin = (lam_max - lam_min) / float(nlam)
        self.area = self.lam * 0 + area
            
class Star():
    def __init__(self, name = '', m = 0, dist = 0, T = 0, radius = 0):
        self.name = name
        self.m = m
        self.dist = dist    # parsecs
        self.T = T          # F
        self.r = radius          # meters
        
#################################################################
# FUNCTIONS
def calcChiSq(original_y,fit_y):
    fit_std = np.std(fit_y)
    residuals = fit_y - original_y 
    chisq = np.sum((residuals / fit_std)**2)
    return chisq

def plotResults(original_x,original_y,noisy_x,noisy_y,fit_y,title):
    plt.plot(noisy_x, fit_y, label = "polynomial fit", color = 'r')
    plt.plot(original_x,original_y, label = "clean data", color = 'g')
    plt.scatter(noisy_x,noisy_y, label = "noisy data")
    plt.legend()
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Brightness")
    plt.title(title)
    plt.grid()

def ChebFit(original_x,original_y,noisy_x, noisy_y, ifPlot):
    # MODEL
    degree = 4
    cheby_model = modeling.polynomial.Chebyshev1D(degree = degree)
    fitter = fitting.LinearLSQFitter()                                 # could try other fitters
    best_fit = fitter(cheby_model, noisy_x, noisy_y)
    fit_y = best_fit(noisy_x)
    
    if ifPlot == 1:
        figTitle = "Chebychev Fit to Star Spectra"
        plotResults(original_x,original_y,noisy_x,noisy_y,fit_y,figTitle)
        
    # ERROR
    return calcChiSq(original_y,fit_y)

def LegendreFit(original_x,original_y,noisy_x, noisy_y, ifPlot):
    # MODEL
    degree = 4;
    legendre_model = modeling.polynomial.Legendre1D(degree = degree)
    fitter = fitting.LinearLSQFitter()
    legendre_fit = fitter(legendre_model,noisy_x,noisy_y)
    legendre_fit_y = legendre_fit(noisy_x)
    
    if ifPlot == 1:
        figTitle = "Legendre Fit to Star Spectra"
        plotResults(original_x,original_y,noisy_x,noisy_y,legendre_fit_y,figTitle)

    # ERROR
    return calcChiSq(original_y,legendre_fit_y)

def HermiteFit(original_x,original_y,noisy_x, noisy_y, ifPlot):
    degree = 4;
    hermite_model = modeling.polynomial.Hermite1D(degree = degree)
    fitter = fitting.LinearLSQFitter()
    hermite_fit = fitter(hermite_model,noisy_x,noisy_y)
    hermite_fit_y = hermite_fit(noisy_x)
    
    if ifPlot == 1:
        figTitle = "Hermite Fit to Star Spectra"
        plotResults(original_x, original_y, noisy_x, noisy_y, hermite_fit_y, figTitle)
        
    # ERROR
    return calcChiSq(original_y,hermite_fit_y)

def PolyFit(original_x,original_y,noisy_x, noisy_y, ifPlot):
    
    degree = 4
    poly_model = modeling.polynomial.Polynomial1D(degree = degree)
    fitter = fitting.LinearLSQFitter()                                   # could try other fitters
    poly_fit = fitter(poly_model, noisy_x, noisy_y)
    poly_fit_y = poly_fit(noisy_x)
    
    if ifPlot == 1:
        figTitle = "Basic Polynomial Fit to Star Spectra"
        plotResults(original_x,original_y,noisy_x,noisy_y,poly_fit_y,figTitle)
    
    # ERROR
    return calcChiSq(original_y,poly_fit_y)
###############################################    
## Define Constants
I = Instrument(nlam=101,lam_min=250,lam_max=2100,area=np.pi*1.2**2)
rand_star = Star(name = 'Randometra',dist = 250000, T = 4850, radius = 6.957e8)
M = mc.Model()
M.BlackbodyPhotons(rand_star, I, 10000)
# save original model data for future use
original_y = M.y
original_x = M.x

# CREATE NOISY DATA
M.SimData(rand= "Poisson", xbar=0.,sigma=1., noise = 5., amp_factor=0.01)
noisy_x = M.x
noisy_y = M.y

###############################################

Temp = np.linspace(3000,8000,300)       #starting temp 3000K, end temp 8000K, 300 stars

PolyChiSq_Arr = []
ChebChiSq_arr = []
LegendreChiSq_arr = []
HermiteChiSq_arr = []


for i in Temp:
    rand_star = Star(name = 'Randometra',dist = 250000, T = i, radius = 6.957e8)
    
    M = mc.Model()
    # changing 'T = Temp[i]' broke this. Changed it
    #M.BlackbodyPhotons(rand_star[i], I, 10000)
    M.BlackbodyPhotons(rand_star, I, 10000)
    # save original model data for future use
    original_y = M.y
    original_x = M.x
    
    # CREATE NOISY DATA
    M.SimData(rand= "Poisson", xbar=0.,sigma=1., noise = 5., amp_factor=0.01)
    noisy_x = M.x
    noisy_y = M.y

    PolyChiSq_Arr.append(PolyFit(original_x, original_y, noisy_x, noisy_y, 0))
    #PolyChiSq_Arr.append = PolyFit(original_x,original_y,noisy_x, noisy_y, 0)
    ChebChiSq_arr.append(ChebFit(original_x,original_y,noisy_x, noisy_y, 4))
    LegendreChiSq_arr.append(LegendreFit(original_x,original_y,noisy_x, noisy_y, 2))
    HermiteChiSq_arr.append(HermiteFit(original_x,original_y,noisy_x, noisy_y, 3))
    
plt.figure(0)
plt.plot(Temp,PolyChiSq_Arr)
plt.xlabel("Temperature [K]")
plt.ylabel("Polynomial CHiSq")

plt.figure(4)
plt.plot(Temp,ChebChiSq_arr)
plt.xlabel("Temperature [K]")
plt.ylabel("Chebyshev CHiSq")

plt.figure(2)
plt.plot(Temp,LegendreChiSq_arr)
plt.xlabel("Temperature [K]")
plt.ylabel("Legendre CHiSq")

plt.figure(3)
plt.plot(Temp,HermiteChiSq_arr)
plt.xlabel("Temperature [K]")
plt.ylabel("Hermite CHiSq")


################################################
## JUST BASIC PLOTS


# ORIGINAL POLYNOMIAL FIT
#plt.figure(0)
#PolyChiSq = PolyFit(original_x,original_y,noisy_x, noisy_y, 1)
#print("First Chi-squared value:", PolyChiSq)

# CHEBYCHEV POLYNOMIALS
#plt.figure(1)
#ChebChiSq = ChebFit(original_x,original_y,noisy_x, noisy_y, 1)
#print("Chebychev Chi-squared value:",ChebChiSq)


# LEGENDRE POLYNOMIALS
#plt.figure(2)
#LegendreChiSq = LegendreFit(original_x,original_y,noisy_x, noisy_y, 1)
#print("Legendre Chi-squared value:", LegendreChiSq)

# HERMITE POLYNOMIALS
#plt.figure(3)
#HermiteChiSq = HermiteFit(original_x,original_y,noisy_x, noisy_y, 1)
#print("Hermite Chi-squared value:", HermiteChiSq)
