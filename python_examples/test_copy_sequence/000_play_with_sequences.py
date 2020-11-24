import os
import sys
import pickle

import numpy as np

from config import python_parameters, mask_parameters
from config import knob_settings, knob_names


#####################################################
# Read general configurations and setup envirnoment #
#####################################################

mode = python_parameters['mode']
tol_beta = python_parameters['tol_beta']
tol_sep = python_parameters['tol_sep']
flat_tol = python_parameters['tol_co_flatness']
links = python_parameters['links']
optics_file = python_parameters['optics_file']
check_betas_at_ips = python_parameters['check_betas_at_ips']
check_separations_at_ips = python_parameters['check_separations_at_ips']
save_intermediate_twiss = python_parameters['save_intermediate_twiss']
force_leveling= python_parameters['force_leveling']
enable_lumi_control = python_parameters['enable_lumi_control']
enable_imperfections = python_parameters['enable_imperfections']
enable_crabs = python_parameters['enable_crabs']

# Make links
for kk in links.keys():
    if os.path.exists(kk):
        os.remove(kk)
    os.symlink(os.path.abspath(links[kk]), kk)

# Create empty temp folder
os.system('rm -r temp')
os.system('mkdir temp')

# Execute customization script if present
os.system('bash customization.bash')

# Import pymask
sys.path.append('./modules')
import pymask as pm

# Import user-defined optics-specific tools
import optics_specific_tools as ost

######################################
# Check parameters and activate mode #
######################################

# Check and load parameters 
pm.checks_on_parameter_dict(mask_parameters)

# Define configuration
(beam_to_configure, sequences_to_check, sequence_to_track, generate_b4_from_b2,
    track_from_b4_mad_instance, enable_bb_python, enable_bb_legacy,
    force_disable_check_separations_at_ips,
    ) = pm.get_pymask_configuration(mode)

if force_disable_check_separations_at_ips:
    check_separations_at_ips = False

if not(enable_bb_legacy) and not(enable_bb_python):
    mask_parameters['par_on_bb_switch'] = 0.

if not(enable_crabs):
    knob_settings['par_crab1'] = 0.
    knob_settings['par_crab5'] = 0.

########################
# Build MAD-X instance #
########################

# Start mad
Madx = pm.Madxp
mad = Madx(command_log="mad_collider.log")

# Build sequence (alse creates link to optics_toolkit and calls it)
ost.build_sequence(mad, beam=beam_to_configure)

# Set twiss formats for MAD-X parts (macro from opt. toolkit)
mad.input('exec, twiss_opt;')

# Apply optics
ost.apply_optics(mad, optics_file=optics_file)

# Attach beam to sequences
mad.globals.nrj = python_parameters['beam_energy_tot']
gamma_rel = python_parameters['beam_energy_tot']/mad.globals.pmass
for ss in mad.sequence.keys():
    # bv and bv_aux flags
    if ss == 'lhcb1':
        ss_beam_bv, ss_bv_aux = 1, 1
    elif ss == 'lhcb2':
        if int(beam_to_configure) == 4:
            ss_beam_bv, ss_bv_aux = 1, -1
        else:
            ss_beam_bv, ss_bv_aux = -1, 1

    mad.globals['bv_aux'] = ss_bv_aux
    mad.input(f'''
    beam, particle=proton,sequence={ss},
        energy={python_parameters['beam_energy_tot']},
        sigt={python_parameters['beam_sigt']},
        bv={ss_beam_bv},
        npart={python_parameters['beam_npart']},
        sige={python_parameters['beam_sige']},
        ex={python_parameters['beam_norm_emit_x'] * 1e-6 / gamma_rel},
        ey={python_parameters['beam_norm_emit_y'] * 1e-6 / gamma_rel},
    ''')
