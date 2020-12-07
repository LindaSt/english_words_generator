# word_image_generator

You can generate binary images from a provided word list in any font provided. 
The images are randomly generated form a randomly sampled font, with randomized font size, position, rotation and shearing.

### Requirements
- conda

### Installation
There is an environment file, use the following command to create the environmnet: 
```conda env create -f environemnt.yml```

This creates  conda environment "words_generator"

### Usage
Activate your environment:
```conda activate words_generator```
and execute the following command:
```python generate.py --words_path /path/to/your/words/file --font_folder /path/to/your/fonts/folder --output_path /path/to/your/output/folder```

### Optionals
```
usage: generate.py [-h] --alphabet_words WORDS_PATH --font_folder FONT_FOLDER --output_path
                   OUTPUT_PATH [--train_amount TRAIN_AMOUNT]
                   [--test_amount TEST_AMOUNT] [--val_amount VAL_AMOUNT]
generate.py: error: the following arguments are required: --words_path, --font_path, --output_path
```
