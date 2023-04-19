# Pygame Customizable Isometric Map Animation With Stable Diffusion 

## Description

This technical demo is an open-source project that allows users to customize the appearance and design of the map in game with stable diffusion.
You can modify graphical elements to create your own unique version map.

![Gameplay Demo](temp/demo.gif)

full video demo here : https://youtu.be/vJml7Hf4jPs

![Gameplay Demo](temp/demo2.gif)

full animation video demo here : https://www.youtube.com/watch?v=dwrt-kQ-xl4

## Features:
- Create your own map with stable diffusion
- Generate animations for specific elements of the map

## Prerequisites

To run this project, make sure you have the following installed on your machine:

- Python 3.10 or higher
- Pygame 2.0.0 or higher
- pygame-widgets 1.0.0
- Pillow 9.4.0
- requests 2.2.25
- Stable diffusion webui automatic1111

You can install Stable Diffusion Webui by following the instructions on the [Stable Diffusion Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) repository.


## Installation

To install the game, follow these steps:

1. Launch Stable diffusion webui with "--api" flag

2. Clone this repository to your local directory:

```bash
git clone https://github.com/numz/StableDiffusionPygameInpaintIsometricMap.git
```

3. Navigate to the project directory:
    
```bash
cd StableDiffusionPygameInpaintIsometricMap
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Launch the game using the following command:
```bash
python main.py
```
## How it works
### Create elements
- Draw a Shape by maintain left shift key + left mouse click to draw your shape (minimum 3 points for see shape. Shape color will be red), 
- Once shape finish release left shift key, prompt input will appear, write your prompt and press enter to validate.
### Create animations
- First, you need to create an element to animate (see "Create elements" section)
- Draw a Shape by maintain left Ctrl key + left mouse click to draw your shape (minimum 3 points for see shape. Shape color will be blue), 
- Once shape finish release left Ctrl key, prompt input will appear, write your prompt and press enter to validate.

Note that the prompt does not have much influence on the outcome, but it is still recommended to have a prompt closely related to the description of the object being addressed. For example: If you want to animate water, include 'water' in the prompt.


You can animate a lot of kind of elements, for example :
- water
- fire
- lava
- smoke
- clouds
- grass
- trees
- etc...

## Stable diffusion payload
the file Config/config.py contains parameters of the game, especially the prompt.
here is the default prompt use for demo :
- "3d render, isometric %s, octane render, by greg rutkowski"
- "%s" will be replaced by your prompt input in game

models use in demo : v1-5-pruned-emaonly.ckpt

in the "payloads" folder, "payload.json" contain payload used for stable diffusion img2img endpoint, feel free to edit.

## Commands

1. Press "Escape" : access the menu
2. Draw a Shape for inpainting : maintain left shift key + left click to draw your shape (minimum 3 points for see shape)
3. Draw a Shape for animation : maintain left ctrl key + left click to draw your shape (minimum 3 points for see shape)
4. Enter : validate your prompt 
5. arrow keys : move on the map
6. "+" key : speed up time
7. "-" key : slow down time

## To do
- [ ] Add key control for stable diffusion parameters
- [ ] Create Tile editor


## Contributions

Contributions are welcome! To contribute, please follow these steps:

1. Fork this repository to your GitHub account.
2. Clone the forked repository to your local machine.
3. Create a new branch for your changes.
4. Make your changes and commit them.
5. Push the branch to your forked repository.
6. Create a pull request on this original repository to submit your changes.

## License

This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file.

