import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Inputs
try:
    print('Note that Percision > 90 can take very long')
    percision = float(input('Percision to be used (0-100, 90 is default): '))//1
    if percision > 100 or percision < 0:
        percision = 90
except:
    percision = 90

try:
    trailLen = int(input('Trail Length to be Used? (85 is default): '))
    if traillen < 1 or trailLen > 999:
        trailLen = 85
except:
    trailLen = 85

try:
    sunmultiplier = float(input("Sol Magic Acceleration (muiltiple of Mars's, 0 is default): "))
except:
    sunmultiplier = 0
if sunmultiplier != 0:
    sunAngle = float(input('Angle of Sol Acceleration (deg.): '))
else:
    sunAngle = 0

try:
    Magnification = float(input('Outwards zoom? (1.6 is default): '))
except:
    Magnification = 1.6
if Magnification <= 0:
    Magnification = 1.6

# Global things
TotalTime = (32/5)*1000
Inter = int(101-percision)
FRAMES = int(TotalTime / (Inter/1000))
t = [0]
fig, ax = plt.subplots()

# Scaling Value
orbitReducer = 10**5 / 1

# Mercury Data & Sprite
mercuryRadius = ((46*10**9 + 68.817*10**9)/2) / orbitReducer
x = [-mercuryRadius, -mercuryRadius]
y = [0, 0]

# Venus Data & Sprite
venusRadius = ((107.476*10**9 + 108.939*10**9)/2) / orbitReducer
venusX = [venusRadius, venusRadius]
venusY = [0, 0]

# Earth Data & Sprite
earthRadius = ((147.092*10**9 + 152.099*10**9)/2) / orbitReducer
earthX = [0, 0]
earthY = [earthRadius, earthRadius]

# Mars Data & Sprite
marsRadius = ((206.617*10**9 + 249.229*10**9)/2) / orbitReducer
marsX = [0, 0]
marsY = [-marsRadius, -marsRadius]
VMag = []

# Sol Data & Sprite
sunRadiusX = 0
sunRadiusY = 0
CMsunX = [0, 0]
CMsunY = [0, 0]
sunx = [-0.01*mercuryRadius+CMsunX[-1], 0.01*mercuryRadius+CMsunX[-1]] + [-0.01*mercuryRadius+CMsunX[-1], 0.01*mercuryRadius+CMsunX[-1]] + [CMsunX[-1], CMsunX[-1]] + [-.015*mercuryRadius+CMsunX[-1], .015*mercuryRadius+CMsunX[-1]]
suny = [-0.01*mercuryRadius+CMsunY[-1], 0.01*mercuryRadius+CMsunY[-1]] + [0.01*mercuryRadius+CMsunY[-1], -0.01*mercuryRadius+CMsunY[-1]] + [-.015*mercuryRadius+CMsunY[-1], .015*mercuryRadius+CMsunY[-1]] + [CMsunY[-1], CMsunY[-1]]
sunMass = 2*10**30

# Functions to describe drawing for each frame
def animate(dt):

    # Trail Length Handler
    if len(x) > trailLen:
        x.pop(0)
        y.pop(0)
    if len(venusX) > trailLen:
        venusX.pop(0)
        venusY.pop(0)
    if len(earthX) > trailLen:
        earthX.pop(0)
        earthY.pop(0)
    if len(marsX) > trailLen:
        marsX.pop(0)
        marsY.pop(0)
    if len(CMsunX) > 2:
        CMsunX.pop(0)
        CMsunY.pop(0)

    # Global Constants
    t.append(dt)
    deltaT = (int(t[-1]) - int(t[0])) * (Inter/1000)

    # Sunny Stuff              this \/ was 8385006.95
    accXsun = sunmultiplier*(2.542*10**-3*orbitReducer**2)*(np.cos(np.pi*(sunAngle)/180))**2
    accYsun = sunmultiplier*(2.542*10**-3*orbitReducer**2)*(np.sin(np.pi*(sunAngle)/180))**2
    sunRadiusX = CMsunX[-1] + 0.5*accXsun*deltaT**2
    sunRadiusY = CMsunY[-1] + 0.5*accYsun*deltaT**2
    sunRadius = (sunRadiusX**2 + sunRadiusY**2)**0.5
    CMsunX.append(sunRadiusX)
    CMsunY.append(sunRadiusY)


    ## Mercury Orbit ##

    # Physics Section (Constants)
    Rmercury = ((x[-1]-CMsunX[-1])**2+(y[-1]-CMsunY[-1])**2)**0.5
    acc = 6.67*10**-11 * sunMass / (Rmercury)**2
    Vo = (acc*mercuryRadius)**0.5

    # Physics Pt. 2 (Kinematics)
    theta = np.arctan2(float(y[-1])-CMsunY[-1], float(x[-1])-CMsunX[-1])
    if theta < 0:
        theta = theta + 2*np.pi

    accY = -acc*np.sin(theta)
    accX = -acc*np.cos(theta)

    # Vo = Vo + 0.5*acc*deltaT**2
    Vy = -Vo*np.cos(theta)
    Vx = Vo*np.sin(theta)

    X = x[-1] + Vx*deltaT + 0.5*accX*deltaT**2
    Y = y[-1] + Vy*deltaT + 0.5*accY*deltaT**2


    ## Venus Orbit ##

    # Physics Section (Constants)
    Rvenus = ((venusX[-1]-CMsunX[-1])**2+(venusY[-1]-CMsunY[-1])**2)**0.5
    accVenus = 6.67*10**-11 * sunMass / (Rvenus)**2
    VoVenus = (accVenus*venusRadius)**0.5

    # Physics Pt. 2 (Kinematics)
    thetaVenus = np.arctan2(float(venusY[-1])-CMsunY[-1], float(venusX[-1])-CMsunX[-1])
    if thetaVenus < 0:
        thetaVenus = thetaVenus + 2*np.pi

    accYvenus = -accVenus*np.sin(thetaVenus)
    accXvenus = -accVenus*np.cos(thetaVenus)

    VyVenus = -VoVenus*np.cos(thetaVenus)
    VxVenus = VoVenus*np.sin(thetaVenus)

    newVenusX = venusX[-1] + VxVenus*deltaT + 0.5*accXvenus*deltaT**2
    newVenusY = venusY[-1] + VyVenus*deltaT + 0.5*accYvenus*deltaT**2


    ## Earth Orbit ##

    # Physics Section (Constants)
    Rearth = ((earthX[-1]-CMsunX[-1])**2+(earthY[-1]-CMsunY[-1])**2)**0.5
    accEarth = 6.67*10**-11 * sunMass / (Rearth)**2
    VoEarth = (accEarth*earthRadius)**0.5

    # Physics Pt. 2 (Kinematics)
    thetaEarth = np.arctan2(float(earthY[-1])-CMsunY[-1], float(earthX[-1])-CMsunX[-1])
    if thetaEarth < 0:
        thetaEarth = thetaEarth + 2*np.pi

    accYearth = -accEarth*np.sin(thetaEarth)
    accXearth = -accEarth*np.cos(thetaEarth)

    VyEarth = -VoEarth*np.cos(thetaEarth)
    VxEarth = VoEarth*np.sin(thetaEarth)

    newEarthX = earthX[-1] + VxEarth*deltaT + 0.5*accXearth*deltaT**2
    newEarthY = earthY[-1] + VyEarth*deltaT + 0.5*accYearth*deltaT**2


    ## Mars Orbit ##

    # Physics Section (Constants)
    Rmars = ((marsX[-1]-CMsunX[-1])**2+(marsY[-1]-CMsunY[-1])**2)**0.5
    accMars = 6.67*10**-11 * sunMass / (Rmars)**2
    VoMars = (accMars*marsRadius)**0.5

    # Physics Pt. 2 (Kinematics)
    thetaMars = np.arctan2(float(marsY[-1])-CMsunY[-1], float(marsX[-1])-CMsunX[-1])
    if thetaMars < 0:
        thetaMars = thetaMars + 2*np.pi

    accYmars = -accMars*np.sin(thetaMars)
    accXmars = -accMars*np.cos(thetaMars)

    VyMars = -VoMars*np.cos(thetaMars)
    VxMars = VoMars*np.sin(thetaMars)

    newMarsX = marsX[-1] + VxMars*deltaT + 0.5*accXmars*deltaT**2
    newMarsY = marsY[-1] + VyMars*deltaT + 0.5*accYmars*deltaT**2

    # Add locations and remove old t entry
    x.append(X)
    y.append(Y)
    venusX.append(newVenusX)
    venusY.append(newVenusY)
    earthX.append(newEarthX)
    earthY.append(newEarthY)
    marsX.append(newMarsX)
    marsY.append(newMarsY)

    t.pop(0)

    # Sprite Garbage <3 #
    sunx = [-0.01*mercuryRadius+CMsunX[-1], 0.01*mercuryRadius+CMsunX[-1]] + [-0.01*mercuryRadius+CMsunX[-1], 0.01*mercuryRadius+CMsunX[-1]] + [CMsunX[-1], CMsunX[-1]] + [-.015*mercuryRadius+CMsunX[-1], .015*mercuryRadius+CMsunX[-1]]
    suny = [-0.01*mercuryRadius+CMsunY[-1], 0.01*mercuryRadius+CMsunY[-1]] + [0.01*mercuryRadius+CMsunY[-1], -0.01*mercuryRadius+CMsunY[-1]] + [-.015*mercuryRadius+CMsunY[-1], .015*mercuryRadius+CMsunY[-1]] + [CMsunY[-1], CMsunY[-1]]

    # Plotting Planets
    ax.clear()
    ax.plot(earthX, earthY)
    ax.plot(sunx, suny)
    ax.plot(venusX, venusY)
    ax.plot(marsX, marsY)
    ax.plot(x, y)
    ax.plot(CMsunX, CMsunY)
    ax.set_xlim([-Magnification*marsRadius, Magnification*marsRadius])
    ax.set_ylim([-Magnification*marsRadius, Magnification*marsRadius])

    plt.legend(['Earth', 'Sol', 'Venus', 'Mars', 'Mercury'])

# Run the animation
ani = FuncAnimation(fig, animate, frames=int(FRAMES), interval=-1000, repeat=False)
plt.show()
