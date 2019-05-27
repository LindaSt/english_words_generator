# chinese_mnis_generator

You can generate your own mnist like chinese character dataset.

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
```python generate.py --alphabet_path /path/to/your/alphabet/file --output_path /path/to/your/output/folder```

### Optionals
```
usage: generate.py [-h] --alphabet_path ALPHABET_PATH --output_path
                   OUTPUT_PATH [--train_amount TRAIN_AMOUNT]
                   [--test_amount TEST_AMOUNT] [--val_amount VAL_AMOUNT]
generate.py: error: the following arguments are required: --alphabet_path, --output_path
```
