from comfy.comfy_types.node_typing import IO, ComfyNodeABC, InputTypeDict


class FloodGate(ComfyNodeABC):
    @classmethod
    def INPUT_TYPES(s) -> InputTypeDict:
        return {
            "required": {
                "source": (IO.ANY,),
                "gate_open": (IO.BOOLEAN, {"default": False}),
            }
        }

    RETURN_TYPES = (IO.ANY, IO.ANY)
    RETURN_NAMES = ("CLOSE", "OPEN")

    FUNCTION = "gate"
    CATEGORY = "utils"

    def gate(self, source, gate_open):
        return (source, source)
