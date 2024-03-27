'''
Source:
https://github.com/UTS-eResearch/pbsweb/blob/main/src/pbsutils.py

'''
import pbs
import sys

def get_jobs(conn, extend=None):
    '''
    Get information on the PBS jobs.
    This function returns a list of jobs, where each job is a dictionary.

    This is the list of resources requested by the job, e.g.:
      Resource_List : mem = 120gb
      Resource_List : ncpus = 24
      Resource_List : nodect = 1
      Resource_List : place = free
      Resource_List : select = 1:ncpus=24:mem=120GB
      Resource_List : walltime = 200:00:00

    These are non-resource attributes, e.g.
        Job_Name : AuCuZn
        Job_Owner : 999777@hpcnode0
        job_state : Q
        queue : workq
        server : hpcnode0
      etc ....
    '''

    debug = True
    jobs = [] # This will contain a list of dictionaries.

    # Some jobs don't yet have a particular attribute as the job hasn't started yet.
    # We have to create that key and set it to something, otherwise we get errors like:
    #   NameError("name 'resources_used_ncpus' is not defined",)
    attribute_names = ['resources_used_ncpus', 'resources_used_mem', 'resources_used_vmem', \
        'resources_used_walltime', 'exec_host', 'exec_vnode', 'stime', 'etime', \
        'resources_time_left', 'resources_used_cpupercent']

    b = pbs.pbs_statjob(conn, '', None, extend)
    while b != None:
        attributes = {} # Init the dictionary to empty.
        # Init the values of the attributes.
        for name in attribute_names:
            attributes[name] = ''
        for name in ['resources_used_walltime', 'resources_used_cput']:
            attributes[name] = '0:0:0'

        attribs = b.attribs
        if debug:
            print('-----------', b.name, '-------------------')
        attributes['job_id'] = b.name.split('.')[0] # b.name is a string like '137550.hpcnode0'
        while attribs != None:
            if attribs.resource != None:
                if debug:
                    # The print here is indented a bit more to distinguish
                    # resource attributes from non-resource attributes.
                    print('    ', attribs.name, ':', attribs.resource, '=', attribs.value)
                keyname = '%s_%s' % (attribs.name, attribs.resource)
                keyname = keyname.lower()
                attributes[keyname] = attribs.value
            else:
                if debug:
                    print('  ', attribs.name, ':', attribs.value)
                keyname = attribs.name.lower()
                attributes[keyname] = attribs.value

            attribs = attribs.next

        jobs.append(attributes)
        b = b.next

    return jobs


if __name__ == '__main__':
    # You need to set the hostname of the PBS Server.
    pbsserver = 'head.testbed.schedulingpower.emulab.net'

    # Connect to the pbs server
    conn = pbs.pbs_connect(pbsserver) 
    if conn < 0:
        print('Error connecting to server.')
        sys.exit(1)
    jobs = get_jobs(conn)
    print('OUTPUT ------------------------------------------')
    print(jobs)
    print('END OUTPUT ------------------------------------------')