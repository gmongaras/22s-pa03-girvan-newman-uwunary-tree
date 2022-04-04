Q function: https://www.pnas.org/doi/full/10.1073/pnas.0601602103

BFS: http://infolab.stanford.edu/~ullman/mmds/book0n.pdf (10.2 - page 361 (page 381 in PDF))

GN Algo: https://www.pnas.org/doi/epdf/10.1073/pnas.122653799



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

## Project Execution

The following command can be used to run the project: </br>

```bash
./22s-pa02-amogus
```

### Sample Input

...


### Sample Output

The project has one output file which is formatted as such:. </br>

```
File Name,Size,Integer/String,Insertion,Random Quicksort,Merge,Shell,Intro,Tim
./data/integer/1000/1000_0D_0S.txt,1000,integer,97,1707,93,7,16,21
./data/integer/1000/1000_0D_100S.txt,1000,integer,1,2058,108,9,11,19
Contd...
```

An output file should already be located in the repository.

### Data Generation

For our data generation script, we decided to use python. In our python code, we create a function that generates a random array with the following parameters:
- <b>low</b> - The lowest integer to put into the array (Min Val).
- <b>high</b> - The highest integer to put into the array (Max Val).

...


