# word_image_generator

You can generate binary images from a provided word list in any font provided.

### Requirements
- conda

### Installation
there is an environment file for OSX(18 Mojave) and linux. Just use the one suitable for you system with the following command to create the environmnet: 
```conda env create -f environemnt_*.yml```

This creates  conda environment "chinese_mnist"

### Usage
Activate your environment:
```conda activate chinese_mnist```
and execute the following command:
```python generate.py --words_path /path/to/your/words/file --font_folder /path/to/your/fonts/folder --output_path /path/to/your/output/folder```

### Optionals
```
usage: generate.py [-h] --alphabet_words WORDS_PATH --font_folder FONT_FOLDER --output_path
                   OUTPUT_PATH [--train_amount TRAIN_AMOUNT]
                   [--test_amount TEST_AMOUNT] [--val_amount VAL_AMOUNT]
generate.py: error: the following arguments are required: --words_path, --font_path, --output_path
```
