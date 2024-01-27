from .floodgate import FloodGate
from aiohttp import web
import execution
import server
import nodes

NODE_CLASS_MAPPINGS = {"FloodGate": FloodGate}
NODE_DISPLAY_NAME_MAPPINGS = {"FloodGate": "Flood Gate"}


def find_gate(prompt:dict) -> list:
    '''Find the Unique ID of the Floodgate Node'''
    gate_IDs = []

    for k, v in prompt.items():
        if v["class_type"] == "FloodGate":
            gate_IDs.append(k)

    # if len(gate_IDs) > 1:
    #    print('[Warning] Multiple Floodgates Detected is still experimental!')

    return gate_IDs

def block_gate(prompt:dict, gate_ID:str, floodgate_open:bool) -> dict:
    '''"Bypass" the Nodes that should be Blocked'''
    nodes_affected = []

    try:
        sauce_id, out_index = prompt[gate_ID]['inputs']['source']
    except KeyError:
        # Floodgate is not connected; let ComfyUI raise the error
        return prompt

    sauce_class = nodes.NODE_CLASS_MAPPINGS[prompt[sauce_id]['class_type']]
    sauce_type = str(sauce_class.RETURN_TYPES[out_index]).lower().strip()

    for node, data in prompt.items():
        for k, v in data["inputs"].items():
            if not isinstance(v, list):
                continue

            if gate_ID in v:

                target_class = nodes.NODE_CLASS_MAPPINGS[data['class_type']]
                target_type = (target_class.INPUT_TYPES()['required'][k][0]).lower().strip()

                if sauce_type != target_type:
                    raise IOError()

                if (not floodgate_open) and (v[1] == 1):
                    nodes_affected.append(node)
                    break

                if (floodgate_open) and (v[1] == 0):
                    nodes_affected.append(node)
                    break

    for key in nodes_affected:
        del prompt[key]

    if len(nodes_affected) > 0:
        return recursive_block_gate(prompt, nodes_affected)
    else:
        return prompt

def recursive_block_gate(prompt:dict, node_IDs:list) -> dict:
    '''Block the subsequent nodes of which source has been blocked'''
    to_delete = []

    for node, data in prompt.items():
        for k, v in data["inputs"].items():
            # Connection is always a List
            if not isinstance(v, list):
                continue

            if any(ID in v for ID in node_IDs):
                to_delete.append(node)
                break

    for key in to_delete:
        del prompt[key]

    if len(to_delete) > 0:
        return recursive_block_gate(prompt, to_delete)
    else:
        return prompt
    

original_validate = execution.validate_prompt

def hijack_validate(prompt):
    gate_IDs:list = find_gate(prompt)

    if len(gate_IDs) == 0:
        return original_validate(prompt)

    for ID in gate_IDs:
        if ID not in prompt.keys():
            continue

        try:
            gate_open = prompt[ID]['inputs']['gate_open']
            prompt = block_gate(prompt, ID, gate_open)

        except IOError:
            return (False, 
            {
                'type': 'floodgate_io_mismatch', 
                'message': 'Floodgate IO Type Mismatch', 
                'details': 'source cannot be connected to outputs', 
                'extra_info': {}
            }
            , [], [])

    return original_validate(prompt)

execution.validate_prompt = hijack_validate
