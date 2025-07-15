---
title: "My Init Post in posts folder"
date: 2025-07-12
draft: false
---

This is my first pos in posts folder on my new blog. Welcome! 


```python

import torch

# test is cuda is available
print(f"Is CUDA available: {torch.cuda.is_available()}")

# check the CUDA version
print(f"CUDA version: {torch.version.cuda}")

# check the device count
print(f"Device count: {torch.cuda.device_count()}")

# check the current device
print(f"Current device: {torch.cuda.current_device()}")


# allocate a tensor on the GPU 
x = torch.randn(10, 10).to(torch.device("cuda"))

# print the tensor
print(f"Tensor on GPU: {x}")

# check the device of the tensor
print(f"Device of the tensor: {x.device}")


```

Test for bash code block, simple bash script checking and creating a new directory.
```bash 
# bin bash script to check if the directory exists
#!/bin/bash

# check if the directory exists
if [ -d "test_dir" ]; then
    echo "Directory test_dir exists."
else
    echo "Directory test_dir does not exist."
# check if the directory exists
if [ -d "test_dir" ]; then
    echo "Directory test_dir exists."
else
    echo "Directory test_dir does not exist."
fi

```







