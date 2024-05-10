# Trento_interpolation
An interpolation emulator of different observables relate to nuclear structure.
I use different R0, a0, beta2, beta4, sigmaR0, sigmaa0, sigmabeta2 to create a high dimension grid(generates_point.py) and calculate 10^6 trneto events(run_trento.py) at each parameter grid and use these events I calculate c22,c24,c26,c32,c34,c42,meanpT,deltapT^2,deltapT^3,cov(v22,pT),cov(v24,pT),cov(v22,pT2)(run_trento.py, cal_obs.py).


Then an linear interpolation are used to show the results at the point between the grid(interpolation.py), you can use this script to view it "python3 ./interpolation.py".
