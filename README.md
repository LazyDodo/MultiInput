# MultiInput

MultiInput is a blender addon that allows easy opening of PBR textures in blender

How to install
--------------------------

1. Blender 2.78 is a minimum required version.
2. [Download][addon] the add-on.
3. Go to Blender 'User Preferences' -> 'Add-ons' category.
4. Use 'Install from File...' to install add-on from downloaded zip archive.

Note for mac users:

* Safari browser will automatically unpack downloaded zip archive, so in order to install the add-on, you have to pack folder with add-on files back into zip archive. Or use a different browser to download add-on.

## How to use

from the add nodes menu select MultiInput->MultiInput and select a single texture from your texture set (preferably the diffuse/albedo map, but it's not overly picky)

it'll open all other textures in the set and combine them all in one handy node.

The color/non colodr data is set for known textures like metallic/roughness etc

## Bugs

There's probably a ton, threw this together in an hour or so, just to scratch an itch. 

### Material view doesn't work
This is a blender issue, not something that I can fix sadly. 
 
[addon]: https://github.com/LazyDodo/oslpy/archive/master.zip
