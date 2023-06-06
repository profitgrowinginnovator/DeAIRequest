from deairequest import BacalhauProtocol, ErrorProtocol, DeProtocol

class DeProtocolSelector:
    def __new__(self, name)->DeProtocol:
        if name == "Bacalhau":
            return BacalhauProtocol()
        elif name == "Error":
            return ErrorProtocol()
        else:
            return ErrorProtocol()

