import os, csv

infile = '/Users/ltrani/Desktop/git/igv_xml_writer/review.tsv'


def sample_data(file):
    data = {}
    key_list = []
    with open(file, 'r') as infilecsv:
        infile_reader = csv.DictReader(infilecsv, delimiter='\t')
        for line in infile_reader:
            sample_key = str.join(':',(line['chromosome_name'],line['start'],line['stop']))
            data[line['individual']] = {}
            data[line['individual']][sample_key]= {}
            data[line['individual']][sample_key]= line

            key_list.append(sample_key)
    return data, key_list


def write_header(locus, outfile):
    cwd = os.getcwd()
    with open(outfile, 'w') as outfilecsv:
        outfile_writer = csv.writer(outfilecsv, delimiter='"', quoting=csv.QUOTE_NONE, escapechar=' ')
        header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<Session genome="b37" hasGeneTrack="true" ' \
                 'hasSequenceTrack="true" locus="{}" nextAutoscaleGroup="2" path="{}/{}" version="8">\n\t' \
                 '<Resources>'.format(locus, cwd, outfile)
        outfile_writer.writerow([header])
    return


def resources(outfile, bampath):
    with open(outfile, 'a') as outfilecsv:
        outfile_writer = csv.writer(outfilecsv, delimiter='"', quoting=csv.QUOTE_NONE, escapechar=' ')
        resource = '\t\t<Resource path="{}"/>'.format(bampath)
        outfile_writer.writerow([resource])
    return


def write_resource(outfile):
    with open(outfile, 'a') as outfilecsv:
        outfile_writer = csv.writer(outfilecsv, delimiter='"', quoting=csv.QUOTE_NONE, escapechar=' ')
        resource_line = '\t</Resources>'
        outfile_writer.writerow([resource_line])
    return


def panel(outfile, bamfile, sample, common_name):
    with open(outfile, 'a') as outfilecsv:
        outfile_writer = csv.writer(outfilecsv, delimiter='"', quoting=csv.QUOTE_NONE, escapechar=' ')
        panel = '\t</Panel>\n\t<Panel height="1850" name="Panel_{}" width="943">\n\t<Track altColor="0,0,178" ' \
                'autoScale="true" color="175,175,175" colorScale="ContinuousColorScale;0.0;123.0;255,255,' \
                '255;175,175,175" displayMode="COLLAPSED" featureVisibilityWindow="-1" fontSize="10" id="{}" name="{} '\
                'Coverage" showReference="false" snpThreshold="0.2" sortable="true" visible="true">\n\t\t<DataRange ' \
                'baseline="0.0" drawBaseline="true" flipAxis="false" maximum="123.0" minimum="0.0" type="LINEAR"/>' \
                '\n\t\t</Track>\n\t\t<Track altColor="0,0,178" autoScale="false" clazz="org.broad.igv.track.' \
                'FeatureTrack" color="0,0,178" displayMode="COLLAPSED" featureVisibilityWindow="-1" fontSize="10" ' \
                'height="60" id="{}" name="{} Junctions" sortable="false" visible="false" windowFunction="count">' \
                '\n\t\t\t<DataRange baseline="0.0" drawBaseline="true" flipAxis="false" maximum="60.0" minimum="0.0" ' \
                'type="LINEAR"/>\n\t\t</Track>\n\t\t<Track altColor="0,0,178" autoScale="false" color="0,0,178" ' \
                'displayMode="EXPANDED" featureVisibilityWindow="-1" fontSize="10" id="{}" name="{}_{}" ' \
                'sortable="true" visible="true">\n\t\t\t<RenderOptions/>\n\t\t</Track>'.format(sample, bamfile, sample,
                                                                                               bamfile, sample, bamfile,
                                                                                               sample, common_name)
        outfile_writer.writerow([panel])
    return


def tail(outfile):
    with open(outfile, 'a') as outfilecsv:
        outfile_writer = csv.writer(outfilecsv,     delimiter='"', quoting=csv.QUOTE_NONE, escapechar=' ')
        file_tail ='\t</Panel>\t<Panel height="102" name="FeaturePanel" width="943">\n\t\t<Track altColor="0,0,178" ' \
                   'autoScale="false" color="0,0,178" displayMode="COLLAPSED" featureVisibilityWindow="-1" ' \
                   'fontSize="10" id="Reference sequence" name="Reference sequence" sortable="false" visible="true"/>' \
                   '\n\t\t<Track altColor="0,0,178" autoScale="false" clazz="org.broad.igv.track.FeatureTrack" ' \
                   'color="0,0,178" colorScale="ContinuousColorScale;0.0;251.0;255,255,255;0,0,178" ' \
                   'displayMode="COLLAPSED" featureVisibilityWindow="-1" fontSize="10" height="35" id="b37_' \
                   'genes" name="Gene" renderer="BASIC_FEATURE" sortable="false" visible="true" windowFunction="count">' \
                   '\n\t\t\t<DataRange baseline="0.0" drawBaseline="true" flipAxis="false" maximum="251.0" minimum="0.0" ' \
                   'type="LINEAR"/>\n\t\t</Track>\n\t</Panel>\n\t<PanelLayout ' \
                   'dividerFractions="0.010067114093959731,0.38926174496644295,0.8204697986577181"/>' \
                   '\n\t<HiddenAttributes>\n\t\t<Attribute name="DATA FILE"/>\n\t\t<Attribute name="DATA TYPE"/>' \
                   '\n\t\t<Attribute name="NAME"/>\n\t</HiddenAttributes>\n</Session>'
        outfile_writer.writerow([file_tail])
    return


sample_data_dict, sample_key_list = sample_data(infile)

xml_outfiles = set()
for sample in sample_data_dict:
    for line in sample_data_dict[sample]:
        if line in sample_key_list:
            outfile = '{}.xml'.format(line)
            xml_outfiles.add(outfile)
            if not os.path.isfile(outfile):
                write_header(line, outfile)
            resources(outfile, sample_data_dict[sample][line]['bam_path'])

for file in xml_outfiles:
    write_resource(file)

for sample in sample_data_dict:
    for line in sample_data_dict[sample]:
        if line in sample_key_list:
            outfile = '{}.xml'.format(line)
            panel(outfile, sample_data_dict[sample][line]['bam_path'], sample_data_dict[sample][line]['individual'],
                  sample_data_dict[sample][line]['common_name'])

for file in xml_outfiles:
    tail(file)

