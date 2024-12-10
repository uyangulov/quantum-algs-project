import pytest
import numpy as np
from circuit import Gate

class TestGate:
    
    @pytest.fixture
    def gate(self):
        """Fixture to provide a default Gate instance."""
        gate_matrix = np.array([[0.5, 0.5, 0.5, 0.5],
                                [0.5, 0.5, -0.5, -0.5],
                                [0.5, -0.5, 0.5, -0.5],
                                [0.5, -0.5, -0.5, 0.5]])
        return Gate([0, 1], gate_matrix, name="Hadamard")
    
    def test_gate_no_matrix(self):
        """Test that no matrix raise a ValueError."""
        with pytest.raises(TypeError):
            Gate([0, 1])
    
    def test_gate_initialization_valid(self, gate):
        """Test proper initialization with valid parameters."""
        assert gate.name == "Hadamard"
        assert gate.qubit_indices == [0, 1]
        assert gate.matrix_size == 4  # 2^2 = 4 (since it's a 2-qubit gate)

    def test_gate_invalid_matrix_size(self):
        """Test that invalid matrix sizes raise a ValueError."""
        # Invalid 3x3 matrix for a 2-qubit gate
        gate_matrix = np.array([[1, 0, 0],
                                [0, 1, 0],
                                [0, 0, 1]])

        with pytest.raises(ValueError):
            Gate([0, 1], gate_matrix)

    def test_gate_non_square_matrix(self):
        """Test that non-square matrices raise a ValueError."""
        # Non-square matrix (2x3 matrix for a 2-qubit gate)
        gate_matrix = np.array([[1, 0, 0],
                                [0, 1, 0]])

        with pytest.raises(ValueError):
            Gate([0, 1], gate_matrix)

    def test_gate_custom_name(self):
        """Test that a custom name can be assigned to the gate."""
        gate_matrix = np.array([[1, 0],
                                [0, 1]])  # Identity matrix
        gate = Gate([0], gate_matrix, name="CustomIdentity")

        assert gate.name == "CustomIdentity"
        assert gate.qubit_indices == [0]
        assert gate.matrix_size == 2  # 2^1 = 2

    def test_gate_repr(self, gate):
        """Test the __repr__ method."""
        repr_str = repr(gate)
        assert "Gate(name=Hadamard, qubit_indices=[0, 1], matrix_size=4)" in repr_str