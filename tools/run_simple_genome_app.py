from os import listdir
from os.path import basename, dirname, join, realpath

from g2p import read_g2p, write_g2p
from vcf import get_vcf_variants_by_tabix

GENOME_APP_DIRECTORY_PATH = dirname(dirname(realpath(__file__)))

GENOME_APP_NAME = basename(GENOME_APP_DIRECTORY_PATH)

VCF_FILE_PATH = join(GENOME_APP_DIRECTORY_PATH, 'input/dna.vcf.gz')


def run_simple_genome_app():
    """
    Run this Simple Genome App.
    return: None
    """

    # Read input .g2p file
    input_directory_path = join(GENOME_APP_DIRECTORY_PATH, 'input/')
    input_g2p_file_paths = [
        join(input_directory_path, fn) for fn in listdir(input_directory_path)
        if fn.endswith('.g2p')
    ]
    headers, input_g2p_df = read_g2p(input_g2p_file_paths[0])

    # Analyze with the input .g2p file
    match_indices = []
    for i, row in input_g2p_df.iterrows():

        feature, feature_type, region, state = row[:4]
        state = str(state)

        for f, ft, r, s in zip(
                feature.split(';'),
                feature_type.split(';'), region.split(';'), state.split(';')):

            variants = get_vcf_variants_by_tabix(VCF_FILE_PATH, query_str=r)

            # Check for matches in the .vcf file
            if len(variants):

                if ft == 'variant':

                    sample_genotype = variants[0]['sample'][0]['genotype']
                    alleles = s.split('|')
                    if alleles == sample_genotype or alleles == reversed(
                            sample_genotype):
                        match_indices.append(i)

                elif ft == 'gene':

                    impact_to_int = {
                        'MODIFIER': 0,
                        'LOW': 1,
                        'MODERATE': 2,
                        'HIGH': 3,
                    }

                    max_impact = 0

                    for v in variants:
                        for a_i, a_d in v['ANN'].items():
                            if max_impact < impact_to_int(a_d['impact']):
                                max_impact = impact_to_int

                    if impact_to_int.get(s, 2) <= max_impact:
                        match_indices.append(i)

    if len(match_indices):  # Keep matching results
        output_g2p_df = input_g2p_df.loc[match_indices, :]

        # Write output .g2p file
        output_directory_path = join(GENOME_APP_DIRECTORY_PATH, 'output/')
        output_g2p_file_paths = [
            join(output_directory_path, fn)
            for fn in listdir(output_directory_path) if fn.endswith('.g2p')
        ]
        write_g2p(output_g2p_df, output_g2p_file_paths[0], headers=headers)

        print(
            'This Genome App was run and the output was saved as a table in /output/{}.g2p.\n{}'.
            format(GENOME_APP_NAME, output_g2p_df))
