"""

 A very simple example which demonstrates how to configure a patch-based
 Finite Volume solver in Peano4. The code relies on snippets from ExaHyPE2.
 However, it relies only on ExaHyPE's C/FORTRAN compute kernels, i.e. the 
 sophisticated build environment of this H2020 project is not used. The 
 solver simulates the simple Euler equations.

"""


#
# We import Peano4 as project. If this step fails, ensure that your environment
# variable PYTHONPATH points to Peano4's python directory.
#
import os
import peano4
import exahype2
import argparse



parser = argparse.ArgumentParser(description='ExaHyPE 2 - Euler benchmarking script')
parser.add_argument("--load-balancing-quality", dest="load_balancing_quality", type=float, required=True, help="Load balancing quality (something between 0 and 1; 1 is optimal)" )
parser.add_argument("--h",              dest="h",              type=float, required=True, help="Mesh size" )
args = parser.parse_args()


#
# Create a project and configure it to end up in a subnamespace (and thus
# subdirectory). 
#
project = exahype2.Project( ["examples", "exahype2", "euler"], "finitevolumes", "." )


#
# Add the Finite Volumes solver
#
# patch_size     = 7
# unknowns       = 5
# time_step_size = 0.000001
# min_h          = args.h
# max_h          = args.h

# #
# # Still the same solver, but this time we use named arguments. This is the way
# # you can add further PDE terms btw.
# #
# #project.add_solver(  exahype2.solvers.GenericRusanovFVFixedTimeStepSize(
# project.add_solver(  exahype2.solvers.fv.GenericRusanovFixedTimeStepSizeWithEnclaves(
  # "Euler", 
  # patch_size, 
  # unknowns, 0,
  # min_h, max_h,
  # time_step_size,
  # flux = True,
  # ncp  = False
# ))


patch_size     = 11
unknowns       = 5
auxiliary_variables = 0   # This could be something alike material parameters. Not required for Euler.
time_step_size = 0.000001
max_h          = args.h
min_h          = args.h
solver = exahype2.solvers.fv.GenericRusanovFixedTimeStepSizeWithEnclaves(
  "Euler", patch_size, unknowns, auxiliary_variables, min_h, max_h, time_step_size,
  flux=exahype2.solvers.fv.PDETerms.User_Defined_Implementation
)
project.add_solver( solver )


# use_gpu =  False



dimensions = 2
build_mode = peano4.output.CompileMode.Release
#build_mode = peano4.output.CompileMode.Trace
#build_mode = peano4.output.CompileMode.Asserts



#
# Lets configure some global parameters
#
project.set_global_simulation_parameters(
  dimensions, [0.0,0.0,0.0], [1.0,1.0,1.0],
  time_step_size * 10,           # end time
  0.0, 0                         # snapshots
)


#
# So here's the parallel stuff. This is new compared to the serial
# prototype we did start off with.
#
# project.set_load_balancing( "toolbox::loadbalancing::RecursiveSubdivision", "(" + str(args.load_balancing_quality) + ")" )

project.set_load_balancing( "toolbox::loadbalancing::TwoLevelGreedy" )


project.set_Peano4_installation("../../..", build_mode)
peano4_project = project.generate_Peano4_project()
peano4_project.output.makefile.parse_configure_script_outcome( "../../.." )
peano4_project.build(make_clean_first=True,number_of_parallel_builds=4)

