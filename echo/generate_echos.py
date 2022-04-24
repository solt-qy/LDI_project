import sox
from random import choices, uniform, randint
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import sys
import csv


def generate_delays(n_delays, min=0.0, max=200):
    """
    Array of random delays in milliseconds

    Parameters
    ----------
    n_delays : int
        number of delays
    min : float
        minimum delay value
    max : float
        maximum delay value
    Returns
    -------
    list of float
        List of random delays in milliseconds in range [min, max]
    """
    return sorted([uniform(min, max) for x in range(n_delays)])


def generate_decays(n_decays, min=0.0, max=1.0):
    """
    Array of random decays in milliseconds

    Parameters
    ----------
    n_delays : int
        number of decays
    min : float
        minimum decay value
    max : float
        maximum decay value
    Returns
    -------
    list of float
        List of random decays on range [min, max]
    """
    return [uniform(min, max) for x in range(n_decays)]


def random_params(max_echos):
    """
    Generate a dictionary of random parameters suitable for passing in to the echo(s) transfomer function

    The parameters will have anywhere between 1 and max_echos number of delays.

    Parameters
    ----------
    max_echos : int
        maximum number of discrete delays to generate.

    Returns
    -------
    dict
        'n_echos': int
        'delays': list of float
        'decays': list of float
    """
    n_echos = randint(1, max_echos)
    return {'n_echos': n_echos, 'delays': generate_delays(n_echos), 'decays': generate_decays(n_echos)}


def generate_params(n_outputs, max_echos=5):
    """
    Generate a list of n_outputs random echo parameters

    provide to sox.Transformer().echo(gain_in, gain_out, **param)

    Parameters
    ----------
    n_outputs : int
        total number of parameters
    max_echos :
        maximum number of echos the parameter is allowed to contain
    Returns
    -------
    list of dict
        list of echo parameters
    """
    return [random_params(max_echos) for o in range(n_outputs)]


def output_filename_builder(source_file, params):
    """
    Generate an appropriate name for an output file based on the source file, and the echo parameters
    Parameters
    ----------
    source_file : pathlib.Path
        source file Path object
    params : dict
        'n_echos': int
        'delays': list of float
        'decays': list of float
    Returns
    -------
    str
        output filename
    """
    infile = Path(source_file)
    n_echos = params['n_echos']
    delays = '[' + ','.join([f'{x:.0f}' for x in params['delays']]) + ']'
    decays = '[' + ','.join([f'{x:.2f}' for x in params['decays']]) + ']'
    return f'{infile.stem}_echo_{n_echos}_{delays}_{decays}{infile.suffix}'


def create_echoed_file(source_file, output_root, params):
    """
    Generate an echoed filed from a sourcefile and given echo parameters.

    the file will be written to
    output_root/outputs/echo/outfile.wav
    and
    output_root/outputs/echos/outfile.wav

    given the two functions/algorithms used.

    Parameters
    ----------
    source_file : str or pathlib.Path
        source wav file to apply echo to
    output_root : str or pathlib.Path
        root directory for outputs
    params : dict
        echo parameters to pass to sox.Transfomer().echo or sox.Transformer().echos
        'n_echos': int
        'delays': list of float
        'decays': list of float

    Returns
    -------
    None
        Since sox is a command line tool, and the sox library is just a wrapper, there is some not great error handling
        happening. This implementation just assumes everything went ok with the sox command, python errors will still raise though.
    """
    source_file = Path(source_file)
    out_filename = output_filename_builder(source_file, params)

    # implement two separate transformers for the echo and echos algs

    # transformer for echo
    tfm_e = sox.Transformer()
    tfm_e.echo(1.0, 1.0, **params)
    # limit to prevent clipping
    tfm_e.gain(0.0, limiter=True)
    out_file = Path(output_root) / 'outputs' / 'echo' / out_filename
    # build
    tfm_e.build(str(source_file), str(out_file), return_output=True)

    # transformer for echos
    tfm_es = sox.Transformer()
    tfm_es.echos(1.0, 1.0, **params)
    tfm_es.gain(0.0, limiter=True)
    out_file = Path(output_root) / 'outputs' / 'echos' / out_filename
    tfm_es.build(str(source_file), str(out_file), return_output=True)

    # write the details of the echo to the csv output
    with open(output_root / 'outputs' / 'outputs.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([out_filename, source_file.name, params])


def prepare_directories(output_root):
    """
    Prepare the output path and directories for writing

    Parameters
    ----------
    output_root : str or pathlib.Path

    Returns
    -------
    None
    """

    output_root = Path(output_root)

    echo_outputs = output_root / 'outputs' / 'echo'
    echo_outputs.mkdir(parents=True, exist_ok=True)

    echo_outputs = output_root / 'outputs' / 'echos'
    echo_outputs.mkdir(parents=True, exist_ok=True)


def batch_echo_creator(source_files, output_root, n_outputs=1000, max_echos=5):
    """
    Batch creates a series of files that have an echo effect applied to them. Uses the sox library, particularly the
    sox.Transformer().echo() and sox.Transformer().echos() functions.

    Note that "echo" only delays/scales the input signal, while "echos" (echo sequence) delays/scales the input AND
    the subsequently generated echo signal.

    echo parameters will be randomly generated within reasonable bounds, with caller control over the maximum number of
    delays.

    Parameters will be stored in an output csv

    Implemented as a process pool in case you need to process a large amount of files efficiently.

    Parameters
    ----------
    source_files : iterable of str or filelike
        source files to sample from

    n_outputs : int
        number of output files to generate, sampled from source_files with replacement, and run through the echo algorithms

    max_echos : int
        maximum number of echo delays

    Returns
    -------
    None
    """
    output_root = Path(output_root)
    # do some prep
    prepare_directories(output_root)

    ## generate output defitions for n_outputs
    # select the source files (with replacement)
    selected_files = choices(source_files, k=n_outputs)

    # generate the specific parameters
    params = generate_params(n_outputs, max_echos)

    with open(output_root / 'outputs' / 'outputs.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['output_file', 'source_file', 'parameters'])

    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(create_echoed_file, file, output_root, param): (file, param) for
                   file, param in zip(selected_files, params)}

        for future in as_completed(futures):
            source_file, param = futures[future]
            try:
                result = future.result()
            except Exception as e:
                print(f'Failure for {source_file}, with error {e}')


if __name__ == '__main__':
    # example usage
    # python3 batch_create_echos.py source_directory output_directory n_outputs

    # will read all .wav files in the source_directory
    # will apply mostly random echoes to create a total of n_outputs new files
    # will create a output_directory/outputs/, and some other sub folders
    # will also create a csv containing the parameters used to create the outout
    # can also be inferred from the filename

    source_directory, output_root, n_outputs = sys.argv[1:]
    source_files = list(Path(source_directory).glob('./*.wav'))
    output_root = Path(output_root)
    batch_echo_creator(source_files, output_root, int(n_outputs))
