# Video-processor

1: Panorama Generation
Method: Cylinder Projection, Key Points match, Homography matrix

First obtain each frame with holes (same methods as section#2) and select every 50 frames (50, 100, 150, etc. also called keyframes) from the sequence. Second，projected the image to the cylinder and formed a new image for later use. Implemented the algorithm to compute the match points of two consecutive keyframes and a homography matrix, and then use the warp function to transform the image to the correct position.

Since we observed that it is hard for origin rectangular images to find key points so we used cylinder projection to create more overlapping areas. Also, many methods tried to compute the H matrix between the new keyframe and the temporary panorama formed by previous transformations, and it quickly leads to the programming failure when finding the matching points because the temporary panorama is too large. Therefore, we just use two offsets (offsetX and offsetY) to keep track of each frame and improve our program by only computing between two consecutive keyframes, rather than temporary panorama with the keyframe. 


2: Foreground video Generation
Method: Object Tracking and network

To fully compute the accurate position and the boundary of the human body, we used the object detecting algorithm by YOLOv4. We got the bounding box coordinates from the algorithm and easily computed the output of foreground video and frames with holes.

Application1:

To composite the foreground into the panorama, we keep the H matrices and offsets of section#1. We selected the foreground objects at every keyframe and applied the H and offsets to them to transform them back to the correct position at panorama, and we used bitwise and mask operations to ensure the foreground objects cover the pixels of panorama.

Application2:

We already obtained the correct position at each keyframe, it is easy to come up with interpolation between each keyframe to generate a video. We found the track between the start frame and the end frame and composite foreground at each frame. Combining every frame, we successfully formed a video with a new path that correctly synchronized in time.

Application3:

We already obtained frames with holes from section#2. To generate a video removing all objects, we aimed to fill the holes at each frame. Given two consecutive key frames, we computed the homography matrix between them and transformed to form a new panorama. In the panorama we examined each pixel and filled the “empty hole” with pixels from the other image. After filling in the holes we use the inverse homography matrix to transform the frames back to their original state.

Since there was no other foreground object in the demo videos given, if we only want to remove one foreground object but keep the others, simply do it in section #2 where you locate the id of the object you want to remove and generate frames that only have holes of those objects.
