## Cicada - simple GUI for audio annotation 

Cicada is an audio annotation tool which can be used to annotate .wav files and save the annotation in ```csv file``` format (currently). Eventually it will be made available as JSON, XML format as well (please watch for updates)

#### Setting up environment:
```Requires Python 3.5.6```.

###### Following are requiremnts needed to run the tool.
```shell
$ pip install -r requirements.txt
```

#### Things to know before starting tool :
I have enabled the window resizing option 

You can make changes for the following parameters in the  ```config_app.json``` file
```json
{
	"ButtonsParams":
		{
			"Height": 2, 
			"Width":  20
		},
	"AnnotationsFile":
		{
			"ExistingAnnotationFile": "ExistingFile.csv",
			"NewAnnotationFile": "NewAnnotationFile.csv"
		}
}
```


#### To start annotating:

##### Run this script:
After making sure you have ```python3.5.6``` installed and all the required packages you are good to go.
```shell
$ python cicada_app_v1_1.py
```

Note: I have given ```python```and not ```python3``` for running the script because I assume you have virtual environment which has ```python3``` installed

