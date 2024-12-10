import pytest
from statevector import StateVector 

class TestStateVector:
    # Tests for initialization from list

    def test_init_from_list_1_qubit(self):
        sv = StateVector([1, 0])
        assert sv.vector == [1, 0]
        assert sv.num_qubits == 1
        assert sv.length == 2

    def test_init_from_list_2_qubits(self):
        sv = StateVector([1, 0, 0, 0])
        assert sv.vector == [1, 0, 0, 0]
        assert sv.num_qubits == 2
        assert sv.length == 4

    def test_init_from_list_3_qubits(self):
        sv = StateVector([1, 0, 0, 0, 0, 0, 0, 0])
        assert sv.vector == [1, 0, 0, 0, 0, 0, 0, 0]
        assert sv.num_qubits == 3
        assert sv.length == 8

    # Tests for initialization from number of qubits
    def test_init_from_num_qubits_1(self):
        sv = StateVector(1)
        assert sv.vector == [1, 0]
        assert sv.num_qubits == 1
        assert sv.length == 2

    def test_init_from_num_qubits_2(self):
        sv = StateVector(2)
        assert sv.vector == [1, 0, 0, 0]
        assert sv.num_qubits == 2
        assert sv.length == 4

    def test_init_from_num_qubits_3(self):
        sv = StateVector(3)
        assert sv.vector == [1, 0, 0, 0, 0, 0, 0, 0]
        assert sv.num_qubits == 3
        assert sv.length == 8

    # Tests for from_list
    def test_from_list_update_2_qubits(self):
        sv = StateVector(2)
        sv.from_list([0, 1, 0, 0])
        assert sv.vector == [0, 1, 0, 0]
        assert sv.num_qubits == 2

    def test_from_list_invalid_length(self):
        sv = StateVector(2)
        with pytest.raises(ValueError):
            sv.from_list([1, 0, 0])  # Not a power of 2

    # Tests for from_num_qubits
    def test_from_num_qubits_update(self):
        sv = StateVector([1, 0])
        sv.from_num_qubits(3)
        assert sv.vector == [1, 0, 0, 0, 0, 0, 0, 0]
        assert sv.num_qubits == 3

    def test_from_num_qubits_invalid(self):
        with pytest.raises(ValueError):
            StateVector(0)  # Invalid number of qubits

    def test_from_num_qubits_negative(self):
        with pytest.raises(ValueError):
            StateVector(0)  # Invalid number of qubits

    # Test __getitem__
    def test_getitem(self):
        sv = StateVector([1, 0, 0, 0])
        assert sv[0] == 1
        assert sv[1] == 0

    # Test __setitem__
    def test_setitem(self):
        sv = StateVector([1, 0, 0, 0])
        sv[1] = 0.5
        assert sv[1] == 0.5

    # Test vector property setter
    def test_vector_setter_valid(self):
        sv = StateVector(2)
        sv.vector = [0.5, 0.3j + 1, 0, 0]
        assert sv.vector == [0.5, 0.3j + 1, 0, 0]

    def test_vector_setter_invalid_length(self):
        sv = StateVector(2)
        with pytest.raises(ValueError, match="The new vector length .* does not match the expected length .*"):
            sv.vector = [0.5, 0.5]  # Length mismatch