from .floodgate import FloodGate
from aiohttp import web
import execution
import server


floodgate_open = False

WEB_DIRECTORY = "js"
NODE_CLASS_MAPPINGS = {"FloodGate": FloodGate}
NODE_DISPLAY_NAME_MAPPINGS = {"FloodGate": "Flood Gate"}


def find_gate(prompt:dict) -> str:
    '''Find the Unique ID of the Floodgate Node'''
    gate_ID = None

    for k, v in prompt.items():
        if v["class_type"] == "FloodGate":
            if gate_ID is None:
                gate_ID = k
            else:
                print('[Warning] Multiple Floodgates Detected! This will most likely raise errors!')

    return gate_ID

def block_gate(prompt:dict, gate_ID:str) -> dict:
    '''"Bypass" the Nodes that should be Blocked'''
    nodes_affected = []

    for node, data in prompt.items():
        for k, v in data["inputs"].items():
            if not isinstance(v, list):
                continue

            if gate_ID in v:
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


@server.PromptServer.instance.routes.get("/floodgate")
async def floodgate_toggle(_):
    '''Toggle the Floodgate Status'''

    global floodgate_open
    floodgate_open = not floodgate_open

    return web.json_response({"status" : floodgate_open})


original_validate = execution.validate_prompt

def hijack_validate(prompt):

    gate_ID = find_gate(prompt)
    if gate_ID is None:
        return original_validate(prompt)

    return original_validate(block_gate(prompt, gate_ID))

execution.validate_prompt = hijack_validate
