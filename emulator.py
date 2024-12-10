
from abstract_emulator import AbstractEmulator, UnsupportedNumberOfQubits, OperandOutOfBoundsError
from circuit import Gate, QuantumCircuit
from statevector import StateVector


class MyEmulator(AbstractEmulator):

    def __init__(self, 
                 state_vector: StateVector = None):

        self.state_vector = state_vector
    
    '''
        Apply single-qubit gate to input_state_vector. Does not modify input
    '''
    def __apply1Q__(self, 
                    input: StateVector,
                    gate: Gate):
        
        qubit_index = gate.qubit_indices[0]
        output = StateVector([0] * input.length)
        matrix = gate.matrix
        
        for index in range(output.length):
            
            j_k = (index >> qubit_index) & 1
            
            for i_k in range(2):
                running_index = self.__replace_bit__(index, qubit_index, i_k)
                output[index] += input[running_index] * matrix[j_k, i_k]
        
        return output
    
    '''
        Apply two-qubit gate to input_state_vector. Does not modify output
    '''
    def __apply2Q__(self,
                    input: StateVector,
                    gate: Gate):
        
        qubit1_index, qubit2_index = gate.qubit_indices
        output = StateVector([0] * input.length)
        matrix = gate.matrix
        
        for index in range(output.length):
            
            j_k1 = (index >> qubit1_index) & 1
            j_k2 = (index >> qubit2_index) & 1
            bra = int(f'{j_k2}{j_k1}', base=2)
            
            for i_k1 in range(2):
                for i_k2 in range(2):
                    running_index = self.__replace_bits__(index, [qubit1_index, qubit2_index], [i_k1, i_k2])
                    ket = int(f'{i_k2}{i_k1}', base=2)
                    output[index] += input[running_index] * matrix[bra][ket]

        return output
    
    '''
        in 'num', set bits located at 'locs' to values provided in 'vals'
    '''
    def __replace_bits__(self, num, locs, vals):
    
        assert len(locs) == len(vals), "Number indeces != number of values"
        result = num
        for loc, val in zip(locs, vals):
            result = self.__replace_bit__(result, loc, val)
        return result
            
    '''
        in 'num', set bit located at 'loc' to 'val' 
    '''              
    def __replace_bit__(self, num, loc, val):
        
        if val:
            return num | (1 << loc)
        else:
            return num &(~(1 << loc))
        
    def __repr__(self):

        return self.vector
    
    
    def apply_gate(self,
                   gate: Gate,
                   state_vector: StateVector,
                   inplace: bool = False):
        
        qubit_indeces = gate.qubit_indices

        if any(id >= state_vector.num_qubits for id in qubit_indeces):
            raise OperandOutOfBoundsError(gate, state_vector.num_qubits)
        
        output_state_vector = None
        if len(qubit_indeces) == 1:
            output_state_vector = self.__apply1Q__(state_vector, gate)
        elif len(qubit_indeces) == 2:
            output_state_vector = self.__apply2Q__(state_vector, gate)
        else:
            raise UnsupportedNumberOfQubits(gate)

        if (inplace):
            state_vector = output_state_vector

        return output_state_vector
    

    def apply_circuit(self, 
                    circuit: QuantumCircuit,
                    input_state_vector: StateVector,
                    inplace: bool = False):
        
        raise(NotImplementedError)
    
    def apply_circuit(self, circuit, state_vector, inplace = False):
       raise(NotImplementedError)
    
    def apply_circuit_selfstate(self, circuit, inplace = False):
        raise(NotImplementedError)

    