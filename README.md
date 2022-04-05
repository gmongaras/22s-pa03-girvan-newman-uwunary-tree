Q function: https://www.pnas.org/doi/full/10.1073/pnas.0601602103

BFS: http://infolab.stanford.edu/~ullman/mmds/book0n.pdf (10.2 - page 361 (page 381 in PDF))

GN Algo: https://www.pnas.org/doi/epdf/10.1073/pnas.122653799

NN Algo: https://www.ijcai.org/Proceedings/16/Papers/321.pdf



# General Project Information

**Title:** Project 3 - [Community Detection in Networks](https://docs.google.com/document/d/1kzxZlTZV8M57DKrXZFGYVOAaDaBW9JjPwcKYHjFEC04/edit)</br>
**Department:** Computer Science</br>
**Professor:** Dr. Fontenot</br>

**Names:** Gabriel Mongaras and Trevor Dohm</br>
**Date:** 4 / 11 / 2022</br>

**Course:** Fundamentals of Algorithms</br>
**Section:** CS 3353-001</br>

# Project Description

## The Problem

???

## The Algorithm


### Girvan Newman


# Installation, Configuration, Execution

## Project Installation

First, clone the project from GitHub onto your local machine by pressing the green "code" button on the repository page. There are multiple methods of cloning, but use whatever method you are most comfortable with: </br>

- [GitHub Desktop](https://desktop.github.com/)
- Git (Bash)
- Unzip File

Once you have the repository on your machine, make sure that you locate the folder and know the path.

## Project Configuration

In this section, we look at building, linking, and creating the executable for this project. Note that you must have cmake, a compiler, such as gcc, and an environment, such as wsl on your machine. Information about these necessary installations will be listed here:

- [CMAKE](https://cmake.org/)
- [GCC](https://gcc.gnu.org/)
- [WSL](https://docs.microsoft.com/en-us/windows/wsl/about)

If you have an IDE available, you may open the project folder in the IDE and build in the application. This will create the cmake-build-debug directory and add the necessary files for you. [Clion](https://www.jetbrains.com/clion/features/?source=google&medium=cpc&campaign=11960745263&gclid=Cj0KCQiA6NOPBhCPARIsAHAy2zBRVCJK1PdQabj8I-gOpo-iyXsYsDuNjyX9pUvGl5YcFkaTbC-0W9oaAs5BEALw_wcB) and [Eclipse](https://www.eclipse.org/downloads/) are both good choices.

Otherwise, a step-by-step procedure for doing so in the terminal can be found below:

1. Open terminal, type wsl, and navigate into the folder using the path specified by the cloning process.
2. Once you are in the folder, create a directory entitled "cmake-build-debug." 
3. Then, type:

```bash
cmake -S [Project Directory Path] -B [cmake-build-debug path]
```

If you are in the project directory, it will look something like this:

```bash
cmake -S ../22s-pa02-amogus -B cmake-build-debug
```

4. You will see some messages about compiler information and configuration. You can check the cmake-build-debug folder to make sure it has been populated with the necessary files.
5. You can now build and link the project to create the executable. Type:

```bash
cmake --build [cmake-build-debug path]
```

If you are in the project directory, it will look something like this:

```bash
cmake --build cmake-build-debug
```

Once finished with this process, the cmake-build-debug folder should have the executable in it. Check to make sure the data folder and output folder have been pushed into the folder. If they haven't copy and paste them into the cmake-build-debug directory.

## Main Project Execution - C++

The following command can be used to run the project: </br>

```bash
./22s-pa02-amogus
```


## Main Project Execution - Python

The following command can be used to run the project: </br>

```python communityDetection.py```

### All Script Parameters
These parameters can be changed and will effect both the Girvan Newman algorithm and the Neural Network algorithm

<b>mode</b> - Options: "NN" or "GN"
- Use "NN" to evaluate the graph using the Neural Network model.
- Use "GN" (or any other string) to evaluate the graph using the Girvan Newman algorithm.

<b>Note: </b>
- If "NN" is used, make sure to change the parameters in [Neural Network Parameters](https://github.com/smu-cs-3353/22s-pa03-girvan-newman-uwunary-tree/edit/main/README.md#neural-network-parameters)
- If "GN" is used, make sure to change the paramters in [Girvan Newman Parameters](https://github.com/smu-cs-3353/22s-pa03-girvan-newman-uwunary-tree/edit/main/README.md#girvan-newman-parameters)

<b>commName</b> - A string defining the name of the community in the graphML file.
- The commName can be found at the top of the .graphml file.
- Example:

  <img width="455" alt="commName example" src="https://user-images.githubusercontent.com/43501738/161797078-eda078fa-ea8f-428c-98a4-f79580ab0710.png">
  
  In this case the commName would be "community"
 
<b>inFile</b> - The graphml data file to load in to test the algorithm
- This file is a .graphml file and stores a graph we want the model to analyze


### Neural Network Parameters

<b>configFileName</b> - The yaml configuration file name used to configue the neural network
- Example: In this repo, the default file name is ```"./networkParams.yml"```
- For more information on the configuration file, go to [the following section](https://github.com/smu-cs-3353/22s-pa03-girvan-newman-uwunary-tree/edit/main/README.md#network-configuration)

<b>modelFileName</b> - The file name to the model to load in.
- In this repo, we have pretrained models which can be found in the ```models/``` directory. For example, to load in the ```64,32,16,8``` file, the modelFileName would be ```"64,32,16,8"```.

<b>NOTE:</b> The configuration file should have the same configuration as the model being loaded in.
- For example, if the `modelFileName` is ```"64,32,16,8"```, then the configuartion file would look like the following:
```
inDim: 128
Encoder:
    layerNodes: [64,32,16,8]
    activation: "ReLU"
Decoder:
    layerNodes: [8,16,32,64]
    activation: "ReLU"
```

<b>numClasses</b> - The number of classes for the model to classify nodes into.
- By default, this value is set to 4 since the test data found in `data/` has 4 classes.
- If numClasses is changed to a value that is not 4, new test data will have to be created using the [Data Generation Script](https://github.com/smu-cs-3353/22s-pa03-girvan-newman-uwunary-tree/edit/main/README.md#data-generation)


### Girvan Newman Parameters

<b>nodeSubsetPercent</b> - The percent of random nodes to pick in the betweeness algorithm
- Values can between (0, 1]
- When the GN algorithm runs, it calculates the betweeness for a set percentage of nodes as opposed to doing all the nodes
- A higher percetage makes the algorithm more accurate, but also makes the algorithm take longer


## Network Training

trainNetwork.py


## GML To GraphML Conversion

gml_to_graphml.py


## Data Generation

dataGeneration.py


## Network Data Generation

networkDataGeneration.py

### Network Configuration

;


