# Stats Class
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats import chi2

class Stats:
    def __init__(self,D=False,M=False):
        self.D = D
        self.M = M
        
    def info(self):
        if self.D == False: print("No Data")
        else: print("DataClass Instance called",self.D.filename)
        if self.M == False: print("No Model")
        else: print("ModelClass Instance called",self.M.name)
        
    def mean(self,printit=True):
        m = np.mean(self.D.x)
        if printit == True: print(f"The mean of the x values of the data is: {m:,.2f}")
        return m

    def median(self,printit=True):
        m = np.median(self.D.x)
        if printit == True: print(f"The median of the x values of the data is: {m:,.2f}")
        return m

    def mode(self,printit=True):
        #find unique values in array along with their counts
        vals, counts = np.unique(self.D.x, return_counts=True)
        #find mode
        mode_indices = np.argwhere(counts == np.max(counts))
        v = vals[mode_indices].flatten().tolist()
        if printit == True: print(f"The values of the modes are {vals[mode_indices].flatten().tolist()}")
        #find how often mode occurs
        f = np.max(counts)
        if printit == True: print(f"The value in the mode bins is {np.max(counts)}")
        #return a list of the mode values and how many mode bins there are
        return v,f

    
    def std(self,printit=True):
        m = np.std(self.D.x)
        if printit == True: print(f"The standard deviation of the x values of the data is: {m:,.2f}")
        return m

    def LinearRegression(self):
        sx = np.sum(self.D.x)
        sy = np.sum(self.D.y)
        sx2 = np.sum(self.D.x * self.D.x)
        sy2 = np.sum(self.D.y * self.D.y)
        sxy = np.sum(self.D.x * self.D.y)
        N = len(self.D.y)
        meanx = np.mean(self.D.x)
        meany = np.mean(self.D.y)
        stdx = np.std(self.D.x)
        stdy = np.std(self.D.y)
        delta = (N * sx2) - (sx * sx)
        A = (sx2 * sy - sx * sxy) / delta
        B = ((N * sxy) - (sx * sy)) / delta
        r = np.sum((self.D.x-meanx)*(self.D.y-meany))/stdx/stdy/len(self.D.x)
        plt.scatter(self.D.x, self.D.y, s=2, marker='o', c='red')
        xlr = np.array([np.min(self.D.x),np.max(self.D.x)])
        ylr = A + (B * xlr)
        plt.suptitle(self.D.filename, fontsize=10)
        plt.plot(xlr,ylr)
        plt.xlabel('x', fontsize=18)
        plt.ylabel('y', fontsize=18)
        plt.savefig(self.D.filename+".jpg")
        plt.show()
        pearson = pearsonr(self.D.x,self.D.y)[1]
        linreg = [A,B,r,pearson]
        print(f'Regression indicates A= {A:5.2f} B={B:5.2f}, r={r:5.2f}')
        print(f'   Probability of this r if actually uncorrelated = {linreg[3]:5.2f}')
        print(f'We can reject the hypothesis of no correlation with {(1.-linreg[3])*100.:5.2f} percent confidence.')
        return linreg
    
    def SS(self,x,mu,sig):
        #print(x,mu,sig)
        dev = (x - mu)**2/sig**2
        dtot = np.sum(dev)
        return dtot

    def SStat(self,dof=0,printit=True):
        dev = (self.D.y - self.M.y)**2/(self.M.y)
        dtot = np.sum(dev)
        if printit:
            print(f"The value of S is {dtot:0.2f} for {len(self.D.y)} degrees of freedom")
        return dtot
 
    def SStat2D(self,xa=[],ya=[]):
        S = np.zeros((len(ya),len(xa)))
        for iy in range(len(ya)):
            for ix in range(len(xa)):
                self.M.y=self.M.func(self.M.x,A=xa[ix],B=ya[iy])
                S[iy][ix] = self.SS(self.D.y,self.M.y,self.M.z)
        return S
 
    def Svalue(self,S,dog):
        p = chi2.cdf(S,dog)
        return p
    
    def plotstats(self):
        plt.suptitle(self.D.filename, fontsize=10)
        plt.plot(self.M.x,self.M.y)
        plt.plot(self.D.x,self.D.y,drawstyle='steps')
        plt.xlabel('x', fontsize=18)
        plt.ylabel('y', fontsize=18)
        #plt.savefig(self.D.filename+".jpg")
        plt.show()
 
    def CStat(self):
        mu=self.M.y
        C=self.M.y * 0.
        for i in range(len(self.D.y)):
            if self.D.y[i] != 0.:
                C[i]=2.*self.D.y[i]*np.log(self.D.y[i]/mu[i])-2.*(self.D.y[i]-mu[i])
                #print(f"i={i}, ni={self.Data.y[i]:.0f}, mui={mu[i]:.4f}, C={C[i]:.4f}")
        dtot = np.sum(C)
        return dtot
 
