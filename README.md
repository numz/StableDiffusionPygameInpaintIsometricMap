# Pygame Customizable Isometric Map With Stable Diffusion 

## Description

This technical demo is an open-source project that allows users to customize the appearance and design of the map in game with stable diffusion. You can modify graphical elements to create your own unique version map.

![Gameplay Demo](temp/demo.gif)

full video demo here : https://youtu.be/vJml7Hf4jPs

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

- Draw a Shape by maintain left shift + left click to draw your shape (minimum 3 points for see shape), 
- Once shape finish release left shift, prompt input will appear, write your prompt and press enter to validate.

## Stable diffusion payload
the file Config/config.py contains parameters of the game, especially the prompt.
here is the default prompt use for demo :
- "3d render, isometric %s, octane render, by greg rutkowski"
- "%s" will be replaced by your prompt input in game

models use in demo : v1-5-pruned-emaonly.ckpt

in the "payloads" folder, "payload.json" contain payload used for stable diffusion img2img endpoint, feel free to edit.

## Commands

1. Press "Escape" : access the menu
2. Draw a Shape : maintain shift + left click to draw your shape (minimum 3 points for see shape)
3. Enter : validate your prompt 
4. arrow keys : move on the map 

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

