# This script generates the imput files for GROMOS software /

import numpy as np

# RESNAMES taken from 54a7_pol_BZ_CCC.mtb file.


CNTs = ['CCC', 'CCCP', 'CCCPD']
water_models = ['H2O', 'H2OG2', 'H2OPD']
voltages = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]

# Slurm parameters
mem_per_cpu = '125'
tasks_per_node = '8'

# Main files to structure GROMOS imputs. These files are usead as layouts to copy the structure located in Leftraru:/home/cinv/imunoz/SWCNTs/CCCP/
# Must conect with sshfs. to cinv@leftraru.nlhpc.cl

# Path in de cluster were you watn to run GROMOS files.

cluster = 'Leftraru'  # 'DonElias'
path = '/home/ignacio/' + cluster + '/SWCNTs/'

mtb_file = '54a7_pol_BZ_CCC.mtb'
ifp_file = '54a7_pol.ifp'
original_mtb_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/topo/54a7_pol_BZ_CCC.mtb'
original_ifp_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/topo/54a7_pol.ifp'

original_min_cnf_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/min/peptide_min.cnf'

original_solvent_imd_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/box/em_solvent.imd'
spc_cnf_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/box/spc.cnf'
original_por_REST_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/box/sim_box_peptide_REST.por'

original_eq_lib_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/eq/mk_script.lib'
original_eq_imd_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/eq/equilibration.imd'
original_eq_jobs_file = '/home/ignacio/Leftraru/SWCNTs/CCCP/eq/equilibration.jobs'

###

# mkdir.sh file

mkdir_file = path + 'mkdir.sh'
bash_master_sh = path + 'bash_master.sh'

with open(mkdir_file, 'w') as file:
    file.write(
        '#!/usr/bin/bash\n'
        '#\n'
        '#\n')

    for i in range(len(CNTs)):

        file.write(
            'mkdir ' + path + CNTs[i] + '\n'
        )

        for j in range(len(water_models)):

            file.write(
                'mkdir ' + path + CNTs[i] + '/' + water_models[j] + '\n'
                'mkdir ' + path + CNTs[i] + '/' + water_models[j] + '/topo\n'
                'mkdir ' + path + CNTs[i] + '/' + water_models[j] + '/min\n'
                'mkdir ' + path + CNTs[i] + '/' + water_models[j] + '/box\n'
                'mkdir ' + path + CNTs[i] + '/' + water_models[j] + '/eq\n'
                'mkdir ' + path + CNTs[i] + '/' + water_models[j] + '/md\n'
            )

            for k in range(len(voltages)):
                file.write(
                    'mkdir ' + path + CNTs[i] + '/' + water_models[j] + '/md/' + str(voltages[k]) + 'V\n')


with open(bash_master_sh, 'w') as bash:
    bash.write(
        '#!/usr/bin/bash\n'
        '#\n'
        '#\n'
        'for i in CCC CCCP CCCPD\n'
        'for j in H2O H2OG2 H2OPD\n'
        'do\n'
        '   cd /home/cinv/imunoz/SWCNTs/"$i"/"$j"/topo\n'
        '   bash make_top.sh\n'
        'done\n'
        'exit'
    )

# GROMOS FILES

for i in range(len(CNTs)):
    for j in range(len(water_models)):

        location = CNTs[i] + '/' + water_models[j] + '/'

        #/topo
        ###

        # The /topo folder must contain CNT[i]+'/'+water_models[j] the files: *.mtb & *.ifp

        topo_arg_file = path + location + 'topo/make_top_peptide.arg'
        com_top_file = path + location + 'topo/com_top.arg'
        make_top_sh = path + location + 'topo/make_top.sh'
        mtb_new_file = path + location + 'topo/' + mtb_file
        ifp_new_file = path + location + 'topo/' + ifp_file

        with open(topo_arg_file, 'w') as arg_topo:
            arg_topo.write(
                '#specify which forcefield building blocks and parameters you want to use with the @build and @param arguments.\n'
                '@build  ' + mtb_file + '\n'
                '@param  ' + ifp_file + '\n'
                '# using the @seq argument you tell the program which building blocks you want to put in a row to built your peptide.\n'
                '# Here, NH3+ is the amino, COO- the carboxy terminus.\n'
                '@seq   ' + CNTs[i] + '\n'
                '# Specify the solvent.\n'
                '@solv   ' + water_models[j]
            )

        with open(com_top_file, 'w') as com_top:
            com_top.write(
                '@topo 78:[6.6_' + CNTs[i] + '_' +
                water_models[j] + '.top]\n'
                '@param 1\n'
                '@ solv 1'
            )

        # Copies of the files *.mtb & *.ifp are generated in each /topo folder for each system under the same name

        with open(original_mtb_file, 'r') as file:
            lines = file.readlines()

        with open(mtb_new_file, 'w') as mtb:
            for line in lines:
                mtb.write(line)

        with open(original_ifp_file, 'r') as file:
            lines = file.readlines()

        with open(ifp_new_file, 'w') as ifp:
            for line in lines:
                ifp.write(line)

        with open(make_top_sh, 'w') as make_top:
            make_top.write(
                '#!/usr/bin/bash\n'
                '#\n'
                # 'do\n'
                'make_top @f make_top_peptide.arg > 6.6_' +
                CNTs[i] + '_' + water_models[j] + '.top\n'
                'com_top @topo 78:6.6_' + CNTs[i] + '_' + \
                water_models[j] + '.top @param 1 @solv 1 > 6.6_3nm_' + \
                CNTs[i] + '_' + water_models[j] + '.top\n'
                # 'done\n'
                'exit'
            )

        #/min
        ###

        # copy /SWCNTs/CCCP/min/peptide_min.cnf file to change the names of the atoms from CCC to CNTs[i] name.

        new_min_cnf_file = path + location + 'min/peptide_min_polarizable.cnf'
        frameout_min_file = path + location + 'min/frameout_peptide.arg'

        position_flag = True
        with open(original_min_cnf_file, 'r') as file:
            lines = file.readlines()

        with open(new_min_cnf_file, 'w') as cnf:

            for line in lines:

                if line == 'POSITION\n':

                    position_flag = False
                    cnf.write('POSITION\n')

                elif not position_flag and line != 'END\n':
                    cnf.write(line[:6] + CNTs[i] + line[10:])

                if not position_flag and line == 'END\n':
                    cnf.write('END\n')
                    position_flag = True

                elif position_flag:
                    cnf.write(line)

        with open(frameout_min_file, 'w') as frameout:
            frameout.write(
                '@topo ../topo/6.6_3nm_' +
                CNTs[i] + '_' + water_models[j] + '.top\n'
                '@pbc        v\n'
                '@outformat pdb\n'
                '@notimeblock\n'
                '@traj           peptide_min_polarizable.cnf'
            )

        #/box
        ###

        sim_box_arg_file = path + location + 'box/sim_box_peptide.arg'
        frameout_box_file = path + location + 'box/frameout_peptide.arg'
        solvent_run_file = path + location + 'box/em_solvent.run'
        em_solvent_imd_file = path + location + 'box/em_solvent.imd'
        spc_cnf = path + location + 'box/spc.cnf'
        sim_box_1_sh = path + location + 'box/sim_box_1.sh'
        sim_box_2_sh = path + location + 'box/sim_box_2.sh'
        por_REST_file = path + location + 'box/sim_box_peptide_REST.por'

        with open(sim_box_arg_file, 'w') as sim_box:
            sim_box.write(
                '@topo    ../topo/6.6_3nm_' +
                CNTs[i] + '_' + water_models[j] + '.top\n'
                '# We use a cubic box (r = rectangular)\n'
                '@pbc     r\n'
                '# coordinates of the solute.\n'
                '@pos  ../min/peptide_min_polarizable.cnf\n'
                '# coordinates of the box containing SPC water molecules.\n'
                '@solvent spc.cnf\n.'
                '# the minimum solute-wall distance\n'
                '@minwall 0.8\n'
                '# the minimum solute-solvent distance\n'
                '@thresh  0.23\n'
                '# used if one uses trucated octahedron pbc\n'
                '#@rotate\n'
            )

        with open(frameout_box_file, 'w') as frameout:
            frameout.write(
                '@topo ../topo/6.6_3nm_' +
                CNTs[i] + '_' + water_models[j] + '.top\n'
                '@pbc        r\n'
                '@outformat pdb\n'
                '@notimeblock\n'
                '@traj           peptide_h2o.cnf\n'
                '@include ALL'
            )

        with open(solvent_run_file, 'w') as run:
            run.write(
                '#!/bin/sh\n'
                'GROMOS=md\n'

                '$GROMOS \\\n'
                '  @topo ../topo/6.6_3nm_' +
                CNTs[i] + '_' + water_models[j] + '.top \\\n'
                '  @conf sim_box_peptide.cnf \\\n'
                '  @fin  peptide_h2o.cnf \\\n'
                '  @refpos sim_box_peptide.rpr \\\n'
                '  @posresspec sim_box_peptide_REST_CCC.por \\\n'
                '  @input em_solvent.imd > em_solvent.omd'
            )

        with open(spc_cnf_file, 'r') as file:
            lines = file.readlines()

        with open(spc_cnf, 'w') as spc:
            for line in lines:
                spc.write(line)

        with open(original_por_REST_file, 'r') as file:
            lines = file.readlines()

        with open(por_REST_file, 'w') as file:
            for line in lines:
                file.write(line)

        with open(original_solvent_imd_file, 'r') as file:
            lines = file.readlines()

        with open(em_solvent_imd_file, 'w') as file:
            for line in lines:
                file.write(line)

        with open(sim_box_1_sh, 'w') as box_sh:
            box_sh.write(

                '#!/usr/bin/bash\n'
                # '#\n'
                # 'ml fosscuda/2019b\n'
                # 'ml CUDA/10.1.105\n'
                # 'ml MD++/1.5.0-openmp\n'
                # '\n'
                'sim_box @f sim_box_peptide.arg > sim_box_peptide.cnf'
            )

        # from this point, script por_and_rpr_box.py must be run in python.

        with open(sim_box_2_sh, 'w') as box_sh:
            box_sh.write(

                '#!/usr/bin/bash\n'
                '#\n'
                'ml fosscuda/2019b\n'
                'ml CUDA/10.1.105\n'
                'ml MD++/1.5.0-openmp\n'
                '\n'
                'chmod 775 em_solvent.run\n'
                './em_solvent.run\n'
                'echo peptide_h2o.cnf file complete\n'
                'frameout @f frameout_peptide.arg\n'
            )

        #/eq
        ###

        eq_mk_script_file = path + location + 'eq/eq_mk_script.arg'
        eq_slurm_example = path + location + 'eq/slurm_example.sh'
        lib_file = path + location + 'eq/mk_script.lib'
        eq_imd_file = path + location + 'eq/equilibration.imd'
        eq_jobs_file = path + location + 'eq/equilibration.jobs'

        with open(original_eq_lib_file, 'r') as file:
            lines = file.readlines()

        with open(lib_file, 'w') as lib:
            for line in lines:
                lib.write(line)

        with open(original_eq_imd_file, 'r') as file:
            lines = file.readlines()

        with open(eq_imd_file, 'w') as imd:
            for line in lines:
                imd.write(line)

        with open(original_eq_jobs_file, 'r') as file:
            lines = file.readlines()

        with open(eq_jobs_file, 'w') as jobs:
            for line in lines:
                jobs.write(line)

        with open(eq_mk_script_file, 'w') as mk_script:
            mk_script.write(
                '@sys            eq_peptide\n'
                '@bin            /home/lmod/software/MD++/1.5.0/bin/md\n'
                '@dir            /home/cinv/imunoz/SWCNTs/' + location + 'eq\n'
                '@files\n'
                '  topo          ../topo/6.6_3nm_' +
                CNTs[i] + '_' + water_models[j] + '.top\n'
                '  input         equilibration.imd\n'
                '  coord         ../box/peptide_h2o.cnf\n'
                '  posresspec    ../box/sim_box_peptide_REST.por\n'
                '  refpos        ../box/sim_box_peptide.rpr\n'
                '@template   mk_script.lib\n'
                '@version        md++\n'
                '@joblist        equilibration.jobs\n'
            )

        with open(eq_slurm_example, 'w') as slurm:
            slurm.write(
                '#!/bin/bash\n'
                '#!/bin/sh\n'
                '#SBATCH -n ' + tasks_per_node + '\n'
                '#SBATCH --job-name=' + CNTs[i] + '_eq\n'
                '#SBATCH --output=' + CNTs[i] + '-%A_%a.out\n'
                '#SBATCH --error=CCCP-%A_%a.err\n'
                '#SBATCH --ntasks-per-node=' + tasks_per_node + '\n'
                '#SBATCH --partition=general\n'
                '\n'
                '##SBATCH --mail-user=ignacio.siao@gmail.com\n'
                '##SBATCH --mail-type=ALL\n'
                '##SBATCH --array=1-1%1\n'
                '#SBATCH --mem-per-cpu=' + mem_per_cpu + '\n'
                '\n'
                '\n'
                'ml fosscuda/2019b\n'
                'ml CUDA/10.1.105\n'
                'ml MD++/1.5.0-openmp\n'
                '\n'
                '#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lmod/software/CUDA/11.4.0/targets/x86_64-linux/lib/stu$\n'
                'export OMP_NUM_THREADS=8\n'
                '\n'
                './eq_peptide_1.run\n'
            )
