class AnyType(str):
    """
    A special class that is always equal in comparisons.
    Credit:
        https://github.com/pythongosssss/ComfyUI-Custom-Scripts/blob/main/py/repeater.py#L2
    """

    def __eq__(self, _: object) -> bool:
        return True

    def __ne__(self, _: object) -> bool:
        return False


generic = AnyType("*")


class FloodGate:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source": (generic,),
                "gate_open": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = (generic, generic)
    RETURN_NAMES = ("CLOSE", "OPEN")

    FUNCTION = "gate"
    CATEGORY = "utils"

    def gate(self, source, gate_open):
        return (source, source)
