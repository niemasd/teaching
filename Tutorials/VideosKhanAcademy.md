# Recording Khan Academy Style Videos
I find it useful to record short topic videos in the Khan Academy style of video production (see [Advanced Data Structures](https://www.youtube.com/playlist?list=PLM_KIlU0WoXmkV4QB1Dg8PtJaHTdWHwRS) for examples). In this tutorial, I will briefly describe my setup.

# Hardware: Wacom One Pen Display
In my videos, I draw and write things as I talk. To help me draw more smoothly/clearly/legibly, I use a [Wacom One pen display](https://www.wacom.com/en-us/products/pen-displays/wacom-one), which is a tablet + screen. This is useful because, unlike the Wacom tablets that are not also screens, my pen is directly on top of what I am drawing.

Note that I purchased a Wacom One pen display because my laptop does not have a touchscreen and because I don't own an Android/iPad tablet. If you already own a device that has a touchscreen with which you can use a pen, that would work as well.

# Software
## Drawing
I use [SmoothDraw](http://www.smoothdraw.com/sd) to actually do the drawing. It is similar in function to Microsoft Paint, but it integrates more nicely with tablets/pens, and the drawing looks more smooth. It seems as though this is what Khan Academy uses.

In SmoothDraw, I use the color palette [recommended by Khan Academy](https://khanacademy.zendesk.com/hc/en-us/articles/226885367-How-do-I-recreate-Khan-Academy-videos-). The following color palette is for a black background (which is how I record all my videos):

|   Color    |     Code    |
| :--------: | :---------: |
| White      | ``#FFFFFF`` |
| Pink       | ``#FB73BE`` |
| Coral      | ``#FF8D71`` |
| Yellow     | ``#FFE066`` |
| Teal       | ``#59F3CE`` |
| Light Blue | ``#65D0FA`` |
| Blue       | ``#4984F2`` |
| Purple     | ``#A87DFF`` |

The following color palette is for a white background:

|   Color   |     Code    |
| :-------: | :---------: |
| Off Black | ``#21242C`` |
| Gray      | ``#717378`` |
| Red       | ``#D92916`` |
| Blue      | ``#1865F2`` |
| Purple    | ``#8A4FFF`` |

For convenience during recording, I have these colors saved in my SmoothDraw color palette.

## Recording
To actually record the videos, I use [Open Broadcaster Software (OBS)](http://obsproject.com/). I open SmoothDraw on my tablet screen, and in OBS, I set a video source to be a window that is contained within the drawing area of SmoothDraw:

TODO ADD SCREENSHOT
