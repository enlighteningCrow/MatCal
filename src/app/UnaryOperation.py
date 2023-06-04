from abc import ABC, abstractmethod

class UnaryOperation(ABC):
    def __init__(self, operand, operator) -> None:
        self.operand = operand
        self.operator = operator
        self.result = None

    def performOperation(self):
        self.result = self.operator(self.operand)

    def updateOperand(self, value):
        self.operand = value

    def updateOperator(self, value):
        self.operator = value

    def getResult(self):
        return self.result

class UnaryOperationMenu(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def getOperations(self):
        pass

class BinaryUnaryOperation(UnaryOperation):
    def __init__(self, operand, operator) -> None:
        super().__init__(operand, operator)

class TensorUnaryOperation(UnaryOperation):
    def __init__(self, operand, operator) -> None:
        super().__init__(operand, operator)

class BinaryUnaryOperationMenu(UnaryOperationMenu):
    def __init__(self) -> None:
        super().__init__()

    def getOperations(self):
        return {
            "Binary Not" : lambda x: ~x,
            "Binary Ones Complement" : lambda x: -x,
            "Binary Twos Complement" : lambda x: -x + 1,
            "Binary Left Shift" : lambda x: x << 1,
            "Binary Right Shift" : lambda x: x >> 1,
        }

class TensorUnaryOperationMenu(UnaryOperationMenu):
    def __init__(self) -> None:
        super().__init__()

    def getOperations(self):
        return {
            "Transpose" : lambda x: x.transpose(0, 1),
            "Inverse" : lambda x: x.inverse(),
        }