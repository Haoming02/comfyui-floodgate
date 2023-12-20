class FloodGate:

    @classmethod
    def INPUT_TYPES(s):
        return { "required": { "latent": ("LATENT",) } }

    RETURN_TYPES = ("LATENT", "LATENT")
    RETURN_NAMES = ("CLOSE", "OPEN")

    FUNCTION = "gate"
    CATEGORY = "latent"

    def gate(self, latent):
        return (latent, latent)
