# son_idl Documentation

- [son\_idl Documentation](#son_idl-documentation)
  - [First time building and running](#first-time-building-and-running)
  - [If it's not building after pulling changes](#if-its-not-building-after-pulling-changes)
  - [First time editing and publishing changes to BitBucket](#first-time-editing-and-publishing-changes-to-bitbucket)
  - [Development](#development)
    - [Adding a file](#adding-a-file)
    - [Editing content](#editing-content)
  - [Syncing changes](#syncing-changes)
  - [Step by step guide to make changes to master](#step-by-step-guide-to-make-changes-to-master)

## First time building and running

To make changes to these documents and build, you will first need to follow these first-time setup instructions:

1. **Install [python](https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe)**
2. **Install [VS Code](https://code.visualstudio.com/download)**
3. Click [this link](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) to **install the markdown editor extension for visual studio**. A popup will open in the browser requesting you to allow it to install.
4. **Install [Git for Windows](https://git-scm.com/download/win)** with all default options on the installer.
5. Open the start menu and search for 'environment variables' and click **'Edit the system environment variables'**
6. On the advanced tab, click the "Environment variables" button at the bottom.
7. **Select the "Path" row** in the upper box and **click Edit**.
8. **Click new** and paste in the following path *%LocalAppData%\Programs\Python\Python311\Scripts*  (may need to change the *Python311* to the version you have. Check the folder structure exists)
9. **Press OK on all open dialogs.**
10. **Open VS Code**
11. **Click the "Source Control" button** in the left-hand nav-bar 
12. **Click Clone Repository** and a prompt will display.
13. **Paste the bitbucket directory link** into the prompt: https://jira.snet.sonardyne.net:8443/scm/doc/son_idl_docs.git and click the "clone from URL" option that appears.
14. Choose a local folder to save the code to.
15. You may at this point be prompted to log into bitbucket to grant permission to clone the code. **Select "Password" and then log in using your usual PC login** (assuming you have bitbucket access - If you don't, contact Rob Sharp).
16. You'll be prompted as to whether you want to open the cloned repository. **Click Open**.
17. **Click Yes, I trust the authors** on the trust prompt.
18. Once the code has been cloned (downloaded locally), **open a terminal within VS Code** by pressing **ctrl+'** (control and apostrophe). 
19. Connect to Sonardyne-Staff wifi if in the office to avoid SSL certificate issues in the next step.
20. **Send the command:  ``` ./launch.bat```** - Wait for this to complete.
21. You can now switch back to the SNET wifi in the office if you switched on step 19.
22. Once this has completed, run the command ```mkdocs serve``` to run the code. This will allow you to connect to the hosted content in your browser on http://127.0.0.1:8000/.

## If it's not building after pulling changes
repeat steps 19. and 20.

## First time editing and publishing changes to BitBucket
For those that do not use git (non-developers), you will need to send two commands via the VS Code terminal before "committing" any changes. Send the following two commands, and **update your initials in the first, and email in the second**
1. git config --global user.name "JDB"
2. git config --global user.email JoeDBloggs@sonardyne.com


## Development

To change or expand the content of the documentation, markdown files are used (*.md). Within VS Code, click the Explorer icon in the left navbar and you'll see a folder view. ```mkdocs.yml``` is the primary file that controls the structure of the document website.

The section under the **nav** header governs the document structure and gives titles to each page, and a markdown document name to use for that page. Each document referenced here should have a corresponding document with that title under the **/docs** folder. 

Indentation below a node will cause the indented pages to be sub-pages of the parent (see **Sub Category** line below.)
```
nav:
    - About: index.md
    - Quick Start: quick-start.md
    - Technology Explainer: technology-explainer.md
      - Sub Category: subcategory.md
    - Integration Examples: integration.md
    - Reference: reference.md
```

### Adding a file

To add a file, simply create a new file in the *docs* folder and then create a corresponding node in the ```mkdocs.yml``` file. 

### Editing content
Markdown is a commonly used language for production of web documents and the content of the documentation is written in this language. See the cheat sheet below for how to format content in markdown. There is plenty of documentation online on the more advanced ways of using markdown.

[Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

## Syncing changes
The documents are hosted in Git on our sonardyne BitBucket servers. This allows multiple people to edit the files and keep a record of all the changes.

To "pull" or "get" changes from the server (likely changes made by others), Open the Source Control tab of VS Code (left nav panel) and on the row under "Source Control Repositories" where it lists "son_idl_docs", there should be a refresh/sync icon, and if any changes are present on the server, there will be a down arrow with a number next to it (the number of changes to "pull" from the server). If you have any changes that are not yet published to the server, there will be an up arrow with a number (the number of commits you are yet to push/publish to the server). Clicking the sync button will pull the latest changes down and push any changes you have made back up to the server. *This can lead to merge conflicts if the same files have been edited by multiple people*. VS Code offers a merge conflict tool to resolve these.

**It is advised to pull any changes before making any new ones yourself to ensure ease of syncing your work with others.**


>**Don't forget to push your work to the server once complete, else it won't be visible to anyone else!**

These documents can be updated as often as necessary internally, and changes put into master. The external facing documents can also be changed regularly [Sonardyne GitHub](https://github.com/Sonardyne), however the actual API/IDL defined in the reference sections will likely move slowly. 

## Step by step guide to make changes to master

1. Open VS code and "clone repositry" in source control tab
2. Paste the following address and hit enter https://jira.snet.sonardyne.net:8443/scm/doc/son_idl_docs.git 

![](docs\assets\Images\readme\Slide1.JPG)  
3. Define a location on your PC for the repositry to be saved locally

![](docs\assets\Images\readme\Slide2.JPG)  
4. Navigate back to https://jira.snet.sonardyne.net:8443/scm/doc/son_idl_docs.git 
5. Create a branch (to be your working branch, created based on master)

![](docs\assets\Images\readme\Slide3.JPG)  
6. Ensure you are in the right repositry, branch type is custom, branch from master and give your branch a sensible name.

![](docs\assets\Images\readme\Slide4.JPG)  
7. Once branch is created navigate to VSCode click just above (7)
8. The branch you have created will be visible in the dropdown. Select this. If not visible try a refresh next to where you clicked previously.

![](docs\assets\Images\readme\Slide5.JPG)  
9. Ensure you are working in the correct branch by checking it is selected (bottom left)
10. If you want to edit a markdown file click once to open, and right click open preview to see a live preview. This can be docked/split screen. 

![](docs\assets\Images\readme\Slide6.JPG)  
11. Make your change, check it is reflected in preview

![](docs\assets\Images\readme\Slide7.JPG)  
12. To see the data live in it's almost final format open a terminal.
13. Type "mkdocs serve" to host a local version of the site on your PC. If your files are set to autosave this will update everytime a change is made.

![](docs\assets\Images\readme\Slide8.JPG)  
14. Once document is served it is visible on the link in the terminal any changes made will be reflected.

![](docs\assets\Images\readme\Slide9.JPG)  
![](docs\assets\Images\readme\Slide10.JPG)  
15. Once happy with your changes navigate to source control in VSCode. You can then review individual changes or "stage all".
16. Once changes that neeed to be commited to master have been staged click "commit" and then "sync" or "commit and sync" and give a reason above the commit button explaining succinctly the changes. This means your changes are now stored on Sonardyne's bitbucket server and locally on your PC. 

![](docs\assets\Images\readme\Slide11.JPG)  
17. In order for your changes to be merged into master you must do a pull request to merge into master. Select "create pull request"
18. Choose to merge your branch into master

![](docs\assets\Images\readme\Slide12.JPG)  
19. Set approvers for this change. For documentation changes this is Roy Nutley or Chris Bennett and John Houlder. You can't review your own changes.

![](docs\assets\Images\readme\Slide13.JPG)  

Once the request is approved master will be updated. Contact John Houlder, Robert Roberts or Rob Sharp for how the documentation is pushed live (to be updated JDH 17/01/24)




 