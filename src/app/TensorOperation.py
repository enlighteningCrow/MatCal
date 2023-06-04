from app.Operation import Operation, OperationMenu

class TensorOperation(Operation):
    def __init__(self, operand0, operand1, operator):
        super().__init__(operand0, operand1, operator)

class TensorOperationMenu(OperationMenu):
    def __init__(self):
        pass

    def getOperations(self):

        import torch

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