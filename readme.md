<h1>Image Management Tool</h1>
<h2>Nonprofit Megaphone</h2>

<h2>Getting Started</h2>
<h3>Requirements</h3>
Python 3

<h3>Installation</h3>
First, download the zip file located on the NPM Google Drive. Alternatively, download this repository from GitHub.
```sh
https://github.com/NBochenek/npm_image_management_tool
```
<h3>Usage</h3>
<ol>
<li>Unzip the repository if necessary and open up the directory.</li>
<li>Start the program by running the file "Image_Management_Tool.exe"</li>
<li>You will be asked to authenticate with your Google Account. You will only be able to manipulate the albums and media items that your Google Account has access to.</li>
<li>The IMT uses a command-line interface. Interact with the options by inputting either a number or word as appropriate. From the main menu, you can enter "q" to terminate the program.</li>
<li><b>Please note that the IMT has an important limitation. It can only manipulate photos, albums, or other media items that it has uploaded or created. Therefore if you plan to use the tool with an album, make sure that album was created with the tool. Similarly, use the tool's photo upload module to place photos in your library.</b></li>
<li>So long as the albums, photos, or media items are created with the tool, you are free to manipulate them through the browser.</li>
</ol>

<h3>Module Overview</h3>
<h4>List Albums</h4>
This module will list all of the albums available to the tool.
<h4>Create Album</h4>
Use this module to create an album. You will be prompted to name it.
<h4>Change Photo Descriptions</h4>
You can use this module to change photo descriptions across your entire library.
<h4>Move Photos</h4>
This module will move all photos with a given description to a user-specified album. Note that from NPM purposes, any photos within an album name that contains "Do Not" will not moved.
<h4>Upload Photos</h4>
This module will upload photos contained within the "photo_upload" folder to your Google Photos library. You will be able to select the album that they are uploaded to.


<h2>For Developers</h2>
When deploying new version with PyInstaler, use command: pyinstaller Image_Management_Tool.py -F

<h2>Contact</h2>
Nick Bochenek <br>
nick.bochenek@nonprofitmegaphone.com <br>
nbochen@gmail.com