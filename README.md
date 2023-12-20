# ComfyUI Floodgate
This is an Extension for [ComfyUI](https://github.com/comfyanonymous/ComfyUI), which allows you to control the logic flow with just one click!

<p align="center"><img src="workflow.png"></p>

<h3 align="center">Motivation</h3>
<p align="center">While <b>Hires. Fix</b> <i>(or similar workflows)</i> can significantly improve the output,
it also takes a longer time to process. Thus, many will simply run the base resolution until a good seed is found before enabling it. 
However, for <code>ComfyUI</code> this means connecting and disconnecting multiple nodes every single time...</p>

<h3 align="center">Solution</h3>
<p align="center">Introducing, <b>Floodgate</b>! <br>
Simply click one button to toggle between the logic flows. No more connecting and disconnecting multiple nodes! </p>

<h3 align="center">How to Use</h3>
<p align="center">Connect the <code>LATENT</code> output from a Sampler to the input of the Floodgate, 
then connect each path to the desired remaining workflow. Under <code>Queue Prompt</code>, you can toggle between the path to take.
The path not chosen will simply not be executed. Also, since <code>ComfyUI</code> caches the intermediate data, 
opening the Floodgate will not require the precedent nodes to be processed again!</p>

### Note / ToDo
- Only **one** Floodgate can exist in a Workflow *as of now*
- Only supports `LATENT` connections *as of now*
