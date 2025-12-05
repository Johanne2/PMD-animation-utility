### What is this?
PMD animation utility is a python script that together with Pokémon Mystery Dungeons Origins dev mode can be used to easily create animations for Pokémon Mystery Dungeon overworld sprites. 

* When creating eight-directional animations, you only need to provide the animation for one direction; the rest can be generated automatically.
* The animations "Double", "Charge", "Rotate" and "Swing" can be flexibly generated from a template.
* The format used is much less verbose than the XML one, and most animations take only a few lines to define.

**Note, you do not need to know how to program in python to use this.**

### How do I use this?
First, get familiar with the single sheet format used by PMDO and how to use the dev mode to import sprites. The PMDO wiki is useful for this, and there is also a guide on the SkyTemple discord spriting-faq channel (the one for creating overworld sprites).

Before you can use the script, you need to have python installed on your computer; older versions may not work, so check that your installation is not too ancient. No code editor is needed (since you can edit the file with notepad etc.), but using one is highly recommended as it will help you avoid formatting errors.

Next, take a look at the examples provided in this repository; you can play around with these to get a hang of how everything works. The top level script is an empty template that is there mostly just for the sake of formality. Even when you're starting a completely new project, it is easier to start with an existing file and just modify it.

If you are creating eight directional animations, the first 5 (for mirrored sprites) or 8 (for non mirrored sprites) rows of the spritesheet should be reserved for the different orientations, ordered clockwise starting from south. The script includes explanations for how the animation definitions should be formatted.

Then, when you are ready to generate the XML file, simply run the script. The ideal workflow is to place the XML_generator.py file in the same folder as your spritesheet and offsets as you can then quickly re-import the newly generated animations after running the script.
 
### What if I want to add animations to an existing XML file?
Since the script replaces the whole XML file whenever it is run, animations that only exist in the XML format cannot be directly modified using this script. However, if you want to add new animations, then there does exist a workflow for this.

First, create the animations and offsets in a different folder as if you were creating a completely new sprite. This new spritesheet needs to be the same width as the original, but it can have more rows. 

Once you are finished with your work, you need to add the "StartingIndex" argument to all your animations with the given value of the total number of sprites in the spritesheet you are going to modify ((number of rows)*(number of columns)). If some of your animations were already using "StartingIndex", then just add this value to the existing one.

After you have generated the XML, you can go to the file and copy-paste the animations to your original FrameData.xml file. Finally, append the newly created spritesheet and offsets to the bottom of the originals in your image editing software of choice.
