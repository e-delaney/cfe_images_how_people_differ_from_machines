# cfe_images_how_people_differ_from_machines

This repository contains ground truth user counterfactual explanations for explaining the misclassifications of a CNN on images from (i) MNIST and (ii) Quickdraw.  


![Image of Human CFE](https://github.com/e-delaney/user-data-cfe-image/blob/de942829cd15c09cfa656e646bea57b3d51a6aca/Quickdraw/cfe_example_github.PNG)

The original query images (that are misclassified by a CNN) and the corresponding counterfactual explanations generated by human users are provided. We also supply the predicted true labels for the misclassified images.

Data is collected using a GUI drawing tool designed using Tkinter. An example task on the MNIST dataset that demonstrates the interface and instructions can be seen below:

![Image of MNIST Instruction](https://github.com/e-delaney/user-data-cfe-image/blob/5d124ca3e1c5b0179b7ec1015040169e23abb06a/MNIST/sample_task_G1.PNG)

## CFE - Methods
We provide details on the computational benchmark methods in our experiments. One of the hard criteria for selecting these methods was based on the availability of open source code. 

### Min-Edit CFE - (https://github.com/SeldonIO/alibi/blob/master/doc/source/methods/CF.ipynb) 
### CEM CFE - (https://github.com/SeldonIO/alibi/blob/master/doc/source/methods/CEM.ipynb)
### VLK CFE - (https://github.com/SeldonIO/alibi/blob/master/doc/source/methods/CFProto.ipynb)
### Revise - (https://github.com/benedikthoeltgen/DeDUCE)

## Acknowledgements

We would like to thank the curators of the MNIST and the Google Quickdraw datasets that were were used extensively in our experiments. We would also like to thank Benedik Hoeltgen his colleagues at OATML as their excellent [open source code](https://github.com/benedikthoeltgen/DeDUCE) was extremely useful for implementing Revise. Finally we would like to thank Seldon Alibi as their open source code was extensively used. 
