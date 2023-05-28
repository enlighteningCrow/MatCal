class Operation:
    def __init__(self, operand0, operand1, operator):
        self.operand0 = operand0
        self.operand1 = operand1
        self.operator = operator
        self.result = None

    def performOperation(self):
        self.result = self.operator(self.operand0, self.operand1)

    def updateOperand0(self, value):
        self.operand0 = value

    def updateOperand1(self, value):
        self.operand1 = value
    
    def updateOperator(self, value):
        self.operator = value

    def getResult(self):
        self.result

