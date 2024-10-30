from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2
from qiskit_aer.noise import NoiseModel
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


def random_bit_gen() -> int:
    """this function generate random 0 or 1 state for a single bit.

    :return: random bit
    :rtype: int
    """

    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()

    backend = AerSimulator(
        noise_model=NoiseModel.from_backend(FakeAlmadenV2()))
    pm = generate_preset_pass_manager(backend=backend, optimization_level=0)
    transpiled_qc = pm.run(qc)

    shots = 10000

    sampler = StatevectorSampler(default_shots=shots)
    pub = sampler.run([transpiled_qc])
    job_sampler = pub
    result_sampler = job_sampler.result()
    counts = result_sampler[0].data.meas.get_counts()

    #print(counts)

    p0 = counts.get('0', 0) / shots  # Probability of 0
    p1 = counts.get('1', 0) / shots  # Probability of 1

    #print(p0,p1)

    x = 0 if p0 > p1 else 1
    #print(x)
    return x


def generate_QRN(min_value=0, max_value=10000):
    """This function generate the random number by collecting bit stream iteratively calling `random_bit_generate`
    function and after collect the all the random bits, convert to the int random number.

    :param min_value: min value of the range, defaults to 0
    :type min_value: int, optional
    :param max_value: max value of the range, defaults to 10000
    :type max_value: int, optional
    :return: random number
    :rtype: int
    """
    range_rn = max_value - min_value + 1
    n_bits = range_rn.bit_length()

    while True:
        random_bits = [random_bit_gen() for _ in range(n_bits)]
        random_number = int("".join(map(str, random_bits)), 2)

        if random_number < range_rn:
            return min_value + random_number


def generate_QRN_float(min_value=0, max_value=10000, precision_bits=8)-> float:
    """This function will generate random float value by collecting bit stream iteratively calling `random_bit_generate`
    as binary fraction and convert back to decimal random number for given precion bits.

    :param min_value: min value of the range, defaults to 0
    :type min_value: int, optional
    :param max_value: max value of the range, defaults to 10000
    :type max_value: int, optional
    :param precision_bits: number of bits for fractional precision, defaults to 8
    :type precision_bits: int, optional
    :return: random float value
    :rtype: float
    """

    random_fraction_bits = [random_bit_gen() for _ in range(precision_bits)]

    #random binary fraction
    random_fraction = sum(bit * (0.5**(i + 1))
                          for i, bit in enumerate(random_fraction_bits))

    random_float = min_value + (max_value - min_value) * random_fraction

    return random_float
