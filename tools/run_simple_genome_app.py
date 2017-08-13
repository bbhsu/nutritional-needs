from os.path import basename, dirname, join, realpath

from g2p import read_g2p, write_g2p
from vcf import get_vcf_variants_by_tabix

GENOME_APP_DIRECTORY_PATH = dirname(dirname(realpath(__file__)))

GENOME_APP_NAME = basename(GENOME_APP_DIRECTORY_PATH)

INPUT_DIRECTORY_PATH = join(GENOME_APP_DIRECTORY_PATH, 'input/')
PERSON_DIRECTORY_PATH = join(INPUT_DIRECTORY_PATH, 'person/')
GRCH_DIRECTORY_PATH = join(INPUT_DIRECTORY_PATH, 'grch/')

TOOLS_DIRECTORY_PATH = join(GENOME_APP_DIRECTORY_PATH, 'tools/')
OUTPUT_DIRECTORY_PATH = join(GENOME_APP_DIRECTORY_PATH, 'output/')
MEDIA_DIRECTORY_PATH = join(GENOME_APP_DIRECTORY_PATH, 'media/')


def run_simple_genome_app():
    """
    Run this Simple Genome App.
    Arguments:
        None
    Returns:
        None
    """

    # Read input .g2p file
    input_g2p = read_g2p(
        join(INPUT_DIRECTORY_PATH, '{}.g2p'.format(GENOME_APP_NAME)))

    # Get .vcf file path
    vcf_file_path = join(PERSON_DIRECTORY_PATH, 'genome.vcf.gz')

    # Analyze
    match_indices = []
    for i, row in input_g2p['table'].iterrows():

        feature, feature_type, region, state = row[:4]
        state = str(state)

        for f, ft, r, s in zip(
                feature.split(';'),
                feature_type.split(';'), region.split(';'), state.split(';')):

            print('Querying {} ...'.format(r))
            variants = get_vcf_variants_by_tabix(vcf_file_path, query_str=r)

            print('\tFound {} variants.'.format(len(variants)))
            if len(variants):

                if ft == 'variant':

                    sample_genotype = variants[0]['sample'][0]['genotype']
                    alleles = s.split('|')
                    if alleles == sample_genotype or alleles == reversed(
                            sample_genotype):
                        match_indices.append(i)
                        print('\t\t{}'.format(row))

                elif ft == 'gene':

                    impact_to_int = {
                        'MODIFIER': 0,
                        'LOW': 1,
                        'MODERATE': 2,
                        'HIGH': 3,
                    }

                    max_impact = 0

                    # Get maximum impact
                    for v in variants:
                        for a_i, a_d in v['ANN'].items():
                            an_impact = impact_to_int[a_d['impact']]
                            if max_impact < an_impact:
                                max_impact = an_impact

                    if impact_to_int.get(s, 2) <= max_impact:
                        match_indices.append(i)
                        print('\t\t{}'.format(row))

    # If there is any match, write output.g2p file, which contains only the
    # matched input .g2p rows
    output_g2p_table = input_g2p['table'].loc[match_indices, :]

    write_g2p({
        'header': input_g2p['header'],
        'table': output_g2p_table
    }, join(OUTPUT_DIRECTORY_PATH, 'output.g2p'))

    print('This Genome App run and outputed /output/output.g2p:')
    print('=' * 80)
    print(output_g2p_table)
    print('=' * 80)
