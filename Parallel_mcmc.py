import subprocess
import generate_namelist
import json
import numpy as np
import argparse
import math

lons = np.linspace(0,180,36)
lons = lons[::-1]
times_retained = list(np.arange(100)* 86400)

# python Parallel_mcmc.py 0.9 5 Bomex '/cluster/scratch/yairc/scampy/Output.Bomex.original/' 6000 1000
def main():
    parser = argparse.ArgumentParser(prog='Paramlist Generator')
    parser.add_argument('theta')
    parser.add_argument('ncores', type=int, default=5)
    parser.add_argument('case_name')
    parser.add_argument('true_path')
    parser.add_argument('num_samp',  type=int, default=6000)
    parser.add_argument('num_burnin', nargs='?', type=int, default=1000)
    args = parser.parse_args()
    theta = args.theta
    ncores = args.ncores
    case_name = args.case_name
    true_path = args.true_path
    num_samp_tot = args.num_samp
    num_burnin = args.num_burnin
    #tuning_log = open("/cluster/scratch/yairc/scampy/tuning_log.txt", "w")

    num_samp = math.trunc((num_samp_tot-num_burnin)/ncores)
    # the subprocess should not include number of cores and should not send a parallel job - o nlya single job many times
    # each job needs its own serial number so you wont overwrite
    # each job need  to save its own parmater_tuning netCDF file in a tuning directory
    # the outputs from all the parallel tunings should be merged to one and saved as nc file - STILL MISSING

    for i in range(0,ncores):
        # runing string for specific value of theta
        ncore = i
        run_str = 'bsub -n 1 -W 4:00 mpirun python mcmc_tuningP.py ' + str(ncore) + ' ' + str(theta) + ' ' + case_name + ' ' + true_path + ' ' + str(num_samp) + ' ' + str(num_burnin)
        print(run_str)
        subprocess.call([run_str], shell=True)


    return


if __name__ == "__main__":
    main()