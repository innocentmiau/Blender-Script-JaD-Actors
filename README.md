# Blender-Script-JaD-Actors
A script to export the locations, rotations and other contents of a jak and daxter actors from your blender to then use on custom levels.

With this script you can place the actors inside your blender level and set them exactly where you want them to be(Rotation/Quaternion included), and then you can use this script to type out for you all the jsonc code lines.
For this to work you have to be a little organized and place the objects inside collections with the correct names.

# Actors that work with this script:
> `money`,
> `buzzer`,
> `eco-blue`, `eco-yellow`, `eco-red`,
> `ropebridge`,
> - `crate`, can contain several types by adding this texts to the **object name**:
> - `crate-wood` to set as wood.
> - `crate-iron` to set as iron.
> - `crate-steel` to set as steel.
> - `crate-bucket` to set as bucket.
> - `crate-barrel` to set as barrel.
> - `crate-darkeco` to set as darkeco.
> `plat-eco`
> `swingpole`
> `orb-cache-top`
> `ecovent`

# Contents that can be put inside crates:
> `eco_yellow`, `eco_red`, `eco_blue`, `eco_green`, `orbs`, `power_cell`, `green_pill`, `buzzer`.

# Art names possible for ropebridges:
> `ropebridge`(default ropebridge, doesn't require any art-name at all for it to work), 
> `ropebridge-52`(jungle bridge), `ropebridge-70`(bigger jungle bridge).

# How to use:
> - Create a collection with the correct name, for example `crate` (For all the actors types you can use with this script check above)
> - Place the object inside the collection, put it in the right location and rotation you want.
> - If the object can contain things inside, like `crate` can, change the name for what you want, for example: `crate-steel-orbs3` and it will set the crate as steel, with 3 orbs inside.
> - For `plat-eco` you can set the final destination and speed by creating a new object outside of the plat-ecos collection and add to the name the text `-final` and then the speed u want it to be like `3` (Example name: `plat-eco-1` for the main actor and `plat-eco-final5` for the final location and speed of 5.
> - For `orb-cache-top` you can set the orb count inside of them by typing `orbsX` on the name, where X is the number of orbs you want inside, by default it will be 10. (Object's name in blender) Example: `orbvent-orbs15` will set the orbvent to have 15 orbs.
> - For `ecovent` you can set the eco vent type to whichever you want by changing the eco type on the object's name, by default it will be blue eco. Example: `yellowvent` will set as yellow vent.
