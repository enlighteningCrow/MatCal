from app.Operation import Operation, OperationMenu

class TensorOperation(Operation):
    def __init__(self, operand0, operand1, operator):
        super().__init__(operand0, operand1, operator)

class TensorOperationMenu(OperationMenu):
    def __init__(self):
        pass

    def getOperations(self):
        return {
            "Tensor Add" : lambda x, y: x + y,
            "Tensor Subtract" : lambda x, y: x - y,
            "Tensor Multiply" : lambda x, y: x * y,
            "Tensor Divide" : lambda x, y: x / y,
            #List more tensor operations that can be done with two operands
        }


    def getOperations(self):
        # Return a dictionary of all the operations that can be performed on two tensors with the result being a tensor in the pytorch library
        # The key is the name of the operation, and the value is the function in the pytorch library that performs the operation on two tensors

        import torch

        # operations = {
        #     'Addition': torch.add,
        #     'Subtraction': torch.sub,
        #     'Multiplication': torch.mul,
        #     'Element-wise Division': torch.div,
        #     'Matrix Multiplication': torch.matmul,
        #     'Element-wise Maximum': torch.max,
        #     'Element-wise Minimum': torch.min,
        #     'Element-wise Exponentiation': torch.pow,
        #     'Element-wise Square Root': torch.sqrt,
        #     'Element-wise Absolute': torch.abs,
        #     'Element-wise Round': torch.round,
        #     'Element-wise Trigonometric Functions': torch.sin,
        #     'Element-wise Arc Trigonometric Functions': torch.arcsin,
        #     'Element-wise Hyperbolic Trigonometric Functions': torch.sinh,
        #     'Element-wise Logarithm': torch.log,
        #     'Element-wise Logarithm (base 2)': torch.log2,
        #     'Element-wise Logarithm (base 10)': torch.log10,
        #     'Element-wise Natural Exponential': torch.exp,
        #     'Element-wise Dot Product': torch.dot,
        #     'Element-wise Modulo': torch.fmod,
        #     'Element-wise Remainder': torch.remainder,
        #     'Element-wise Clamp': torch.clamp,
        #     'Element-wise Power': torch.pow,
        #     'Element-wise Reciprocal': torch.reciprocal,
        #     'Element-wise Truncation': torch.trunc,
        #     'Element-wise Ceil': torch.ceil,
        #     'Element-wise Floor': torch.floor,
        #     'Element-wise Sign': torch.sign,
        #     'Element-wise Erf': torch.erf,
        #     'Element-wise Bessel Functions': torch.bessel,
        #     'Element-wise Log Sum Exp': torch.logsumexp,
        #     'Element-wise Log Add Exp': torch.logaddexp,
        #     'Element-wise Log Cumulative Sum Exp': torch.logcumsumexp,
        #     'Element-wise Logical And Operations': torch.logical_and,  # Example of a logical operation
        #     'Element-wise Logical Or Operations': torch.logical_or,  # Example of a logical operation
        #     'Element-wise Bitwise And Operations': torch.bitwise_and,  # Example of a bitwise operation
        #     'Element-wise Sorting': torch.sort,
        #     'Element-wise Argmax': torch.argmax,
        #     'Element-wise Argmin': torch.argmin,
        #     'Element-wise Softmax': torch.softmax,
        #     'Element-wise Sigmoid': torch.sigmoid,
        #     'Element-wise ReLU': torch.relu,
        #     'Element-wise Leaky ReLU': torch.leaky_relu,
        #     'Element-wise Softplus': torch.softplus,
        #     'Element-wise Softsign': torch.softsign,
        #     'Element-wise Hardtanh': torch.hardtanh,
        #     'Element-wise Log Sigmoid': torch.logsigmoid,
        #     'Element-wise Tanh': torch.tanh,
        #     'Element-wise GELU': torch.gelu,
        #     'Element-wise ELU': torch.elu,
        #     'Element-wise SELU': torch.selu,
        #     'Element-wise CELU': torch.celu,
        #     'Element-wise Hardswish': torch.hardswish,
        #     'Element-wise Log Softmax': torch.log_softmax,
        #     'Element-wise Pairwise Distance': torch.pairwise_distance,
        #     'Element-wise Kullback-Leibler Divergence': torch.kl_div,
        #     'Element-wise Cosine Similarity': torch.nn.functional.cosine_similarity,
        #     'Element-wise L1 Loss': torch.nn.functional.l1_loss,
        #     'Element-wise MSE Loss': torch.nn.functional.mse_loss,
        #     'Element-wise Cross-Entropy Loss': torch.nn.functional.cross_entropy,
        #     'Element-wise Binary Cross-Entropy Loss': torch.nn.functional.binary_cross_entropy,
        #     'Element-wise Triplet Margin Loss': torch.nn.functional.triplet_margin_loss,
        # }

    #     operations = {
    #         torch.add,
    # torch.sub,
    # torch.mul,
    # torch.div,
    # torch.true_divide,
    # torch.floor_divide,
    # torch.remainder,
    # torch.fmod,
    # torch.pow,
    # torch.lt,
    # torch.le,
    # torch.gt,
    # torch.ge,
    # torch.eq,
    # torch.ne,
    # torch.max,
    # torch.min,
    # torch.maximum,
    # torch.minimum,
    # torch.copysign,
    # torch.atan2,
    # torch.lerp,
    # torch.renorm,
    # torch.cross,
    # torch.dist,
    # torch.dot,
    # torch.einsum,
    # torch.ger,
    # torch.inner,
    # torch.kron,
    # torch.outer,
    # torch.mm,
    # torch.mv,
    # torch.bmm,
    # torch.baddbmm,
    # torch.addmm,
    # torch.addmv,
    # torch.matmul,
    # torch.chain_matmul,
    # torch.cdist,
    # torch.pdist,
    # torch.tensordot,
    #     }
        operations = {
            'Addition': torch.add,
            'Subtraction': torch.sub,
            'Multiplication': torch.mul,
            'Division': torch.div,
            'True Division': torch.true_divide,
            'Floor Division': torch.floor_divide,
            'Remainder': torch.remainder,
            'Modulo': torch.fmod,
            'Power': torch.pow,
            'Less Than': torch.lt,
            'Less Than or Equal To': torch.le,
            'Greater Than': torch.gt,
            'Greater Than or Equal To': torch.ge,
            'Equal': torch.eq,
            'Not Equal': torch.ne,
            'Maximum': torch.max,
            'Minimum': torch.min,
            'Element-wise Maximum': torch.maximum,
            'Element-wise Minimum': torch.minimum,
            'Copysign': torch.copysign,
            'Arc Tangent 2': torch.atan2,
            'Euclidean Distance': torch.dist,
            'Inner Product': torch.inner,
            'Kronecker Product': torch.kron,
        }

        return operations