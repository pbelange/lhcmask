# Mask files for LHC and HL-LHC

## Contributors:
<!-- use two spaces for new line -->
R. De Maria  
S. Fartoukh  
M. Giovannozzi  
M. Hostettler  
G. Iadarola  
Y. Papaphilippou  
D. Pellegrini  
G. Sterbini  
F. Van Der Veken  

## To run an example:
```bash
cd examples/hl_lhc_collision/
python ../../unmask.py main.mask parameters_for_unmask.txt
madx main.mask.unmasked | tee out
```
or equivalently:
```bash
cd examples/hl_lhc_collision/
python ../../unmask.py main.mask parameters_for_unmask.txt --run | tee out
```

## Description

In this repository you can retrieve and contribute to improve the MADX code used to setup tracking simulations for LHC and HL-LHC.

This code is based on the work of many colleagues who shared their contributions and effort with the community for enriching this simulation framework.

We refer as *mask* the MADX input code that is the starting code for tracking simulation, FMA analysis,... The *mask* file present *masked* parameters that can be *unmasked*. Once unmasked, the mask become a regular MADX input file and can be directly run.

The proposed generic mask file has two main parts:
 1. the definition of the configuration parameters. Their value can be assigned explicitly or masked by a placeholder (to be used for SixTrack scans).
 2. the call of the madx files 
    - to load the sequence and optics without beam-beam, to define the beam crossing angle and separation, the status of the experimental magnet...
    - to level the luminosity and install/configure the BB lenses...
    - to load the beam to track and install the magnetic errors, power the octupoles, match the tunes and the chromaticities...
    - to make the final twiss and prepare the input files for SixTrack.

The separation of the configuration parameters of the mask with the MADX code aims 
- to improve the readability for the users that can focus on the input of the simulations,
- to define better interfaces for the maintenance of the MADX code.



