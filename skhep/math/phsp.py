from __future__ import division, print_function, absolute_import
from .vectors import LorentzVector, Vector3D
from .numbautils import vectorize, float64, float32
import numpy as np

def PDK(a,b,c):
    x = (a-b-c)*(a+b+c)*(a-b+c)*(a+b-c)
    return np.sqrt(x)/(2*a)

# Compile the PDK function if possible
PDK = vectorize([float64(float64,float64,float64),
                     float32(float32,float32,float32)])(PDK)

def gen_phase_space(mother, masslist, events, fermi=False, rand=None):
    if rand is None:
        prng = np.random.RandomState()
        rand = prng.rand

    masslist = np.asarray(masslist)
    Nt = len(masslist)
    TeCmTm = mother - np.sum(masslist)

    if TeCmTm < 0:
        raise RuntimeError("Invalid decay, no phase space")

    if fermi:
        ffq = np.array([0,
                     3.141592, 19.73921, 62.01255, 129.8788, 204.0131,
                     256.3704, 268.4705, 240.9780, 189.2637,
                     132.1308,  83.0202,  47.4210,  24.8295,
                     12.0006,   5.3858,   2.2560,   0.8859])
        WtMax = TeCmTm**(Nt-2)*ffq[Nt-1] / mother
    else:
        emmax = TeCmTm + masslist[0] + np.cumsum(masslist[1:])
        emmin = np.cumsum(masslist[:-1])
        wtmax = PDK(emmax, emmin, masslist[1:])
        WtMax = 1/np.prod(wtmax)

    rno = np.empty((Nt,events))
    rno[0,:] = 0
    rno[-1,:] = 1
    rno[1:-1,:] = rand(Nt-2,events)
    rno.sort(0)

    # Compute the weights
    invMass = rno*TeCmTm + np.cumsum(masslist)[:,np.newaxis]
    pd = PDK(invMass[1:],invMass[:-1],masslist[1:,np.newaxis])
    wt = WtMax*np.prod(pd,0)

    # Raubold-Lynch method
    DecPro = LorentzVector(0,np.concatenate([pd[:1], -pd]),0,0)
    DecPro.t[0] = np.sqrt(pd[0]**2 + masslist[0,np.newaxis]**2)
    DecPro.t[1:] = np.sqrt(pd**2 + masslist[1:,np.newaxis]**2)

    beta = pd[1:] / np.sqrt(pd[1:]**2 + invMass[1:-1]**2)
    yboost = Vector3D(0,beta,0)

    for i in range(1, Nt):
        cZ = rand(events)*2-1
        sZ = np.sqrt(1-cZ**2)
        angY = rand(events)*2*np.pi
        cY = np.cos(angY)
        sY = np.sin(angY)

        # Numpy does not make a copy, so v is the same as DecPro[...]
        v = DecPro[:,:i+1,:] # All previous LVectors + 1 new one
        v.x, v.y = cZ*v.x - sZ*v.y, sZ*v.x + cZ*v.y # Rot around Z
        v.x, v.z = cY*v.x - sY*v.z, sY*v.x + cY*v.z # Rot around Y
        if i != Nt-1:
            v.boost(yboost[:,:i], inplace=True)

    return DecPro, wt
