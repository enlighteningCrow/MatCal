from app.Operation import Operation, OperationMenu

class BinaryOperation(Operation):
    def __init__(self, operand0, operand1, operator):
        super().__init__(operand0, operand1, operator)

class BinaryOperationMenu(OperationMenu):
    def __init__(self):
        pass

    def getOperations(self):
        return {
            "Binary And" : lambda x, y: x & y,
            "Binary Or" : lambda x, y: x | y,
            "Binary Xor" : lambda x, y: x ^ y,
            "Binary Left Shift" : lambda x, y: x << y,
            "Binary Right Shift" : lambda x, y: x >> y,
        }
