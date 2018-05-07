## MUSE EEG v.0.0.1 (18.05.07)  
###### Inspired by Brenda de Wit
###### Written by Brad Kennedy, Tyler Collins, and Mike Cichonski
###### For the Brock University Cognitive and Affective Neuroscience Laboratory (BUCANL) 
###### Under the supervision of Dr. Sidney Segalowitz, PhD
___________________________________________________________

### Requirements
* Python 2.7 (Python 3 should also work)
  * numpy
  * matplotlib
  * psychopy

### Installation Instructions
#### Linux/MacOS (Recommended)
##### Assuming there is already a default native version of Python on these operating systems with most of the packages required to run this code, there is very little involved in getting MUSE_EEG downloaded and installed on Linux or MacOS:
1. Make sure you open the BASH "terminal" app.
2. Navigate to a desired directory where you'd like MUSE_EEG to be downloaded and installed (use 'ls' to check all files and folders within the current directory, and use 'cd' to navigate to a new directory). There are many tutorials online that help teach the basics of using a BASH terminal, so we won't go into more detail here. 
Below is a list of some extra resources that can help you get familiar with the most common bash commands necessary to use the BASH terminal. In particular, the most common commands you'll run into are: 'ls' (list), 'cd' (change directory), 'cp' (copy file/directory), 'mv'(move/rename a file), and some remote computing commands such as 'ssh' (secure shell - allows you to securely access a remote computer from your local machine), and 'scp/rsync' (secure copy/remote sync):
    * https://www.codecademy.com/learn/learn-the-command-line
    * https://www.udacity.com/course/linux-command-line-basics--ud595
    * http://www.learnshell.org/ 
    * https://www.bash.academy/
3. Once you've navigated to the desired directory, you can clone (download) the MUSE_EEG repository from github into that directory using the following command in the BASH terminal, which uses SSH to download the entire repository to your selected directory:

>> git clone git@github.com:mikeCplus/Muse_EEG.git

If this doesn't work, you can try the alternate HTTPS link instead:

>> git clone https://github.com/mikeCplus/Muse_EEG.git

Everything you need will be in that directory.

4. (Optional) You may choose to rename the MUSE_EEG folder to something more meaningful (i.e. the project or study name) if you wish.
5. (Optional) In the terminal you may choose to navigate to within your (possibly renamed) MUSE_EEG folder by using the 'cd' command.   This will make things a little easier when running the inner functions.
6. It is quite possible you do not have the psychopy package installed by default in Python. Don't panic! There are various ways to do this. The following site explains how this can be done: http://psychopy.org/installation.html
#### Windows 7/8/10 (Use at your own risk)
##### There will be more information here about installing on Windows, but it should be a very similar process as Linux or MacOS if the GitBash application is used as your terminal. [[More testing to come!]]
1. Download and Install GitBash: https://git-scm.com/download/win
2. Open up the GitBash terminal.
3. Run steps 1-5 from the Linux/MacOS instalation instructions.

### Usage Instructions 
#### Linux/MacOS
1. In terminal, run `python study_run.py` to begin the study 
2. There will be more...
3. And even more...
4. But not too much :)

### Scripts

#### study_run.py

**INPUT:**
Run the current study
**OUTPUT:**
Lots of data!

#### scripts/acquire.py

**INPUT:**
Acquire the brain data
**OUTPUT:** 
* Someone should fill this out at some point
* This is it for now...

#### scripts/task_skelleton.py

**INPUT:**
This is the file that defines the task
This file can potentially be changed to fit different paradigms
**OUTPUT:**
* Presents the task of the screen
