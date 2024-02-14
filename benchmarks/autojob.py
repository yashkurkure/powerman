from jinja2 import Template

omp_template = """
#!/bin/bash
#PBS -l nodes=1:ppn={{ ppn }}
#PBS -l walltime={{ walltime }}
#PBS -q {{ queue_name }}
#PBS -o {{ output_file }}
#PBS -e {{ error_file }}

cd $PBS_O_WORKDIR

OMP_NUM_THREADS={{ ppn }} {{ executable_path }}}
"""

mpi_template = """
#!/bin/bash
#PBS -l nodes={{ nodes }}:ppn={{ ppn }}
#PBS -l walltime={{ walltime }}
#PBS -q {{queue name}}
#PBS -o {{ output_file }}
#PBS -e {{ error_file }}

cd $PBS_O_WORKDIR
export P4_RSHCOMMAND=/opt/pbs/bin/pbs_tmrsh

mpiexec {{executable_path}}
"""

problem_classes = ['A', 'S', 'W']

# Generate MPI job scripts
mpi_problem_path = '/pbsusers/NPB3.4.2/NPB3.4-MPI/bin/'
mpi_problems = ['bt', 'cg', 'dt', 'ep', 'ft', 'is', 'lu', 'mg', 'sp']
walltimes = ['00:30:00', '01:00:00', '01:30:00']
for p_class in problem_classes:
    for problem in mpi_problems:
        for walltime in walltimes:
            parameters = {
                'nodes': 1,
                'ppn': 4,
                'walltime': walltime,
                'job_name': 'my_job',
                'output_file': 'output.log',
                'error_file': 'error.log',
                'working_directory': '/path/to/working/directory',
                'command': './my_executable'
            }
        





# Generate OMP job scripts
omp_problem_path = '/pbsusers/NPB3.4.2/NPB3.4-OMP/bin/'
omp_problems = ['bt', 'cg', 'ep', 'ft', 'is', 'lu', 'mg', 'sp', 'ua']






# Define input parameters
parameters = {
    'nodes': 1,
    'ppn': 4,
    'walltime': '00:10:00',
    'job_name': 'my_job',
    'output_file': 'output.log',
    'error_file': 'error.log',
    'working_directory': '/path/to/working/directory',
    'command': './my_executable'
}

# Create a Jinja2 template object
template = Template(pbs_template)

# Render the template with the input parameters
pbs_script = template.render(**parameters)

# Write the rendered PBS script to a file
with open('my_job_script.pbs', 'w') as f:
    f.write(pbs_script)