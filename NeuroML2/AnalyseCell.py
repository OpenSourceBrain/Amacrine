
import neuroml.loaders as loaders

def analyse(cell_file):

    doc = loaders.NeuroMLLoader.load(cell_file)
    print("Loaded morphology file from: "+cell_file)

    cell = doc.cells[0]
    morph = cell.morphology

    cell.summary()
    cables = 0
    for sg in morph.segment_groups:
        segs = cell.get_ordered_segments_in_groups(sg.id)[sg.id]

        cable = sg.neuro_lex_id=="sao864921383"
        if cable:
            cables+=1

        seg_info = str(segs)
        if len(segs)>2:
            seg_info = '[%s,...,%s]'%(segs[0].id,segs[-1].id)

        nseg = 1
        for p in sg.properties:
            if p.tag == 'numberInternalDivisions':
                nseg = int(p.value)
        print("  Segment group: %s has %s segments (%s; NEURON section: %s%s)"%(sg.id, len(segs), seg_info, cable, "; nseg = %i"%nseg if cable else ""))

    print("%s NEURON sections/cables found"%cables)

    interesting_segs = [0, 500, 1000, 1500, 2000]

    all_segs, length_to_prox, length_to_distal = cell.get_ordered_segments_in_groups("all", include_path_lengths=True)

    seg_len_p = length_to_prox['all']
    seg_len_d = length_to_distal['all']
    '''
    print all_segs
    print "-------------------------------"
    print length_to_prox
    print "-------------------------------"

    for i in range(len(all_segs['all'])):
        seg = all_segs['all'][i]
        seg_len_p[seg.id] = length_to_prox['all'][i]
        seg_len_d[seg.id] = length_to_distal['all'][i]'''

    for seg_id in interesting_segs:
        print("Segment %i, len to prox point: %sum, len to dist point: %sum"%(seg_id,seg_len_p[seg_id],seg_len_d[seg_id]))
    
    return all_segs, length_to_prox, length_to_distal

if __name__ == '__main__':
    fn = 'AmacrineChen.cell.nml'
    analyse(fn)