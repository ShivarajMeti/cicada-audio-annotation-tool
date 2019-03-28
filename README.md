## Cicada - simple GUI for audio annotation 

Cicada is an audio annotation tool which can be used to annotate .wav files and save the annotation in ```Pickle (Python List)``` format (currently). Eventually it can be made it save as JSON, XML format as well.

#### Setting up environment:
```Requires Python 3.5.6```.

###### Following are requiremnts needed to run the tool.
```shell
$ pip install -r requirements.txt
```

#### Things to know before starting tool :
I have disabled the window resizing option just to make sure the spectrogram fits in well within the frame.

You can make changes according to your screen size by changing the following constants in the script ```cicada_tool.py```
```python
HEADER_FONT_STYLE = ("Arial Bold", 30, "bold")
FONT_STYLE_BUTTON = ("Arial Bold", 20, "bold")

# On increasing these values window size shrinks
INITIAL_HEIGHT_ADJUST = 250
INITIAL_WIDTH_ADJUST = 80

# On increasing these values window size enlarges
FINAL_HEIGHT_ADJUST = 100
FINAL_WIDTH_ADJUST = 500

#Height and width of buttons
BUTTONS_HEIGHT = 2
BUTTONS_WIDTH = 20
```
You can adjust the button sizes and change your font styles along with frame size.

#### To start annotating:

##### Run this script:
After making sure you have ```python3.5.6``` installed and all the required packages you are good to go.
```shell
$ python cicada_tool.py
```

Note: I have given ```python```and not ```python3``` for running the script because I assume you have virtual environment which has ```python3``` installed

