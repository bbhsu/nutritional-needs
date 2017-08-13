"""
Genome App entry point.
File for running Genome App from either:
    1) Genome AI or
    2) command line ($ python run_genome_app.py).
"""


def run_genome_app():
    """
    Required function for Genome AI to run this Genome App.
    This Genome App must produce either:
        1) <genome-app-repository>/output/output.g2p or
        2) <genome-app-repository>/output/output.html.
    Arguments:
        None
    Returns:
        None
    """

    from run_simple_genome_app import run_simple_genome_app

    run_simple_genome_app()


if __name__ == '__main__':

    run_genome_app()
