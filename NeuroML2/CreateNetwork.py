
import neuroml

import neuroml.loaders as loaders
import neuroml.writers as writers

from pyneuroml.lems import generate_lems_file_for_neuroml

net_ref = "Amacrine_StimNet"
net_doc = neuroml.NeuroMLDocument(id=net_ref)

net = neuroml.Network(id=net_ref)
net_doc.networks.append(net)

cell_name = 'AmacrineChen'
cell_id = cell_name

net_doc.includes.append(neuroml.IncludeType(cell_id+'.cell.nml')) 

pop = neuroml.Population(id="popA",
            component=cell_id,
            type="populationList")

inst = neuroml.Instance(id="0")
pop.instances.append(inst)
inst.location = neuroml.Location(x=0, y=0, z=0)
net.populations.append(pop)


stim_delays_seg_id = {'50ms':0, '200ms':500, '350ms':1000, '500ms':1500, '650ms':2000}

for delay in stim_delays_seg_id:

    seg_id = stim_delays_seg_id[delay]
    
    stim0 = neuroml.PulseGenerator(id='stim_%s'%delay,
                                 delay=delay,
                                 duration='100ms',
                                 amplitude='0.5nA')

    net_doc.pulse_generators.append(stim0)


    input_list0 = neuroml.InputList(id="%s_input"%stim0.id,
                                   component=stim0.id,
                                   populations=pop.id)
    net.input_lists.append(input_list0)

    syn_input0 = neuroml.Input(id=0,
                              target="../%s/0/%s" % (pop.id, pop.component),
                              segment_id=seg_id,
                              destination="synapses")

    input_list0.input.append(syn_input0)



nml_file = net.id+'.net.nml'

writers.NeuroMLWriter.write(net_doc,nml_file)

print("Saved network file to: "+nml_file)
  
                                   
###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)

sim_id = 'TestInputs'
target = net.id
duration=800
dt = 0.025
lems_file_name = 'LEMS_%s.xml'%sim_id
target_dir = "."

interesting_seg_ids = [0,500,1000,1500,2000]

to_plot = {'Some_voltages':[]}
to_save = {'%s_voltages.dat'%cell_id:[]}

for seg_id in interesting_seg_ids:
    to_plot.values()[0].append('%s/0/%s/%s/v'%(pop.id, pop.component,seg_id))
    to_save.values()[0].append('%s/0/%s/%s/v'%(pop.id, pop.component,seg_id))
    
generate_lems_file_for_neuroml(sim_id, 
                               nml_file, 
                               target, 
                               duration, 
                               dt, 
                               lems_file_name,
                               target_dir,
                               gen_plots_for_all_v = False,
                               plot_all_segments = False,
                               gen_plots_for_quantities = to_plot,   #  Dict with displays vs lists of quantity paths
                               gen_saves_for_all_v = False,
                               save_all_segments = False,
                               gen_saves_for_quantities = to_save,   #  Dict with file names vs lists of quantity paths
                               copy_neuroml = False)



