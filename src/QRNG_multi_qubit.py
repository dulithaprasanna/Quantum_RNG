from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp
import matplotlib.pyplot as plt
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import numpy as np


def gen_random_QRN(min_value=0, max_value=10000) -> int:
    """This function generate random number from multi qubit quantum circuit.

    :param min_value: min value of the range, defaults to 0
    :type min_value: int, optional
    :param max_value: max value of the range, defaults to 10000
    :type max_value: int, optional
    :return: random number
    :rtype: int
    """

    while True:
        range_rn = max_value - min_value + 1
        n_bits = range_rn.bit_length()

        qc = QuantumCircuit(n_bits)
        for i in range(n_bits):
            qc.h(i)

        qc.measure_all()

        backend = AerSimulator(
            noise_model=NoiseModel.from_backend(FakeAlmadenV2()))
        pm = generate_preset_pass_manager(backend=backend,
                                          optimization_level=0)
        transpiled_qc = pm.run(qc)

        shots = 10000

        sampler = StatevectorSampler(default_shots=shots)
        pub = sampler.run([transpiled_qc])
        job_sampler = pub
        result_sampler = job_sampler.result()
        counts = result_sampler[0].data.meas.get_counts()

        most_probable_state = max(counts, key=counts.get)

        random_number = int("".join(map(str, most_probable_state)), 2)
        if random_number < range_rn:
            return min_value + random_number
