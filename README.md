# ComfyUI Floodgate
This is an Extension for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which allows you to easily control the logic flow!

<p align="center"><img src="workflow.png"></p>

<h3 align="center">Motivation</h3>

While **Hires. Fix** *(or similar workflows)* can significantly improve the output, it also takes a longer time to process. Thus, many will simply run the base resolution until a good seed is found before enabling it. However, for `ComfyUI` this means connecting and disconnecting multiple nodes every single time...

<h3 align="center">Solution</h3>

Introducing, **Floodgate**! <br>
Simply toggle between the logic flows. No more reconnecting multiple nodes!

<h3 align="center">How to Use</h3>

Connect the output of a node *(**eg.** `LATENT`)* to the `source` of the Floodgate node, then connect each path to the desired remaining workflow. Simply click on `gate_open` to toggle between the paths to take. The path not chosen will not be executed. Furthermore, since `ComfyUI` caches the intermediate results, opening the Floodgate will not require the precedent nodes to be processed again!

<h3 align="center">Features</h3>

1. Connect any arbitrary types
    - *(input/output types still have to match)*
2. Multiple Floodgates in one workflow
3. Control each Floodgate individually

<hr>

**Note:** The logic flow is parsed during the queuing stage, **not** the execution stage. As a result, the boolean value has to be already determined when you press `Queue Prompt`, such as from the toggle or a primitive node. If you use a node that outputs a boolean during execution, this will not work.
