               // Material constants for TiNi

  NOTE: there must be NO comments between a key and the values to be read 

Mf, Ms, As, Af, q0=
310.0  335.0  345.0  355.0  -160.0   //Temperatures in K, q0 in MJ/m^3

//Grain parameters 
GrainsOrientationsDistribution= Korobov
k_fi,k_cte,k_ps=  1  1  1      // (only for Ravnomernoe distribution)
k_zer=  27   // only for Korobov distribution (<=307)
//the following three lines are only for Monocrystal:
Alfa_mono=   27  // Alfa(degrees) - angle to the point on stereogr. triangle
Dist_mono=    6  // Dist(mm)      - radius-vector of this point
Dist110_mono= 8  // Dist110(mm)   - length of the base of stereogr. triangle

Matr Dtrans=
 0.025   0.059   0.0456
 0.059   0.025   0.0456
 0.0456  0.0456  -0.042

//  2.13162554375185831E-02   5.50542526220705528E-02   -4.53783699430055365E-02
//  5.50542526220705528E-02   2.13162554375185831E-02   -4.53783699430055365E-02
// -6.80675549145083048E-02  -6.80675549145083048E-02   -4.17910447761195014E-02

damage_flag= 0
active_plasticity_flag= 1
microplasticity_flag= 1

KVar=        12
KSlipTypes=   2 

KSlip[KSlipType]=
 3  6
  HSlip[KSlipType]=
800  3000
  R0Slip[KSlipType]=
0.0  0.0
  USlip[KSlipType]=    
40.0  40.0   //(kJ/mol)
  PSlip[KSlipType]=
0.0  0.0
  AlfaSlip[KSlipType]=
0.25  0.25

 KTauY=  3     //numb. of points to specify TauYieldEq
TemperTable[KTauY]=   
273    573    673  // in K
TauYieldTable[KSlipTypes][KTauY]=
250    110  101   
450    206  179    // in MPa

ScalingFactor= 1.0
Young_A=   70.0   //Young's modulus in GPa of austenite
Poisson_A=  0.33   //       Poisson's ratio of austenite
Young_M=   30.0   //Young's modulus in GPa
Poisson_M=  0.33   //Poisson's ratio          of martensite
InitialOrder= 0.72 //Initial value of long-range order parameter

Heat expansion of austenite= 11.0 // in 10^-6 K^-1
Heat expansion of martensite= 6.6 // in 10^-6 K^-1
Heat conductivity of austenite= 10.0 // in W/(m*K)
Heat conductivity of martensite= 10.0 //in W/(m*K)
Specific heat of austenite= 5.5e2     //in J/(kg*K)
Specific heat of martensite= 5.0e2    //in J/(kg*K)
Density of austenite= 6.5         // in 10^3 kg/m^3
Density of martensite= 6.5        // in 10^3 kg/m^3

FYield=          8.00 // in MJ/m^3 (8 - 13.00)
FYieldTwinning=  20.00 // in MJ/m^3
Kmp=        0.1     
Kap_MP=     1.0  // scaling factor for microplastic deformation
Dolya=      1.0  // (0<=Dolya<=1) it shows what part of hardening goes away during reverse tr-n
                 //0 - no recovery of FYield
CorrectRoGr=  0.00 // factor for intergranular stress
Tau_c=        100.0 //in MPa - normalizing divisor in strain rate dependent term of flow stress

// Formulae for damage
  // db/dt = dbe/dt - (1/be*)(dbe/dt)*abs(b)*H(b*dbe/dt)
  // df/dt = (q2+q3*f)*abs(b)^alfa*abs(dbe/dt) - r(T)*f
  // where r(T) = r0*exp(-U/kT)
  //Condition of micro failure:
  // abs(b)*f = b_F, b_F being the critical value
// Constants for damage

//Al_d  - alfa (not used now)
be_zv= 0.5  //be*
q2_F= 0.05
q3_F= 100.0
r0_F= 0.0   //r0
U_F= 40 //in kJ/mol - not used when r0_F==0


Tau_F= 500.00 //(MPa) critical stress for damage connected with variant
A_F= 11.0 // 
K1_F=0.0  // normalization factor for SpSig
K2_F=0.0 // normalization factor for local stress concentration
Pi_cr=1.04 // critical value for grain damage due to active plastic def-n
kzer_cr= 0 //critical number of destroyed grains for macro-fracture
           //if kzer_cr==0 it will be set as kzer**(2/3)


