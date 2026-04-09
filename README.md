# Astrophotography-Image-Frame-Pre-Processer
Python-based script to parse metrics (e.g. star count, star eccentricity, sky background level) from the filename of an astrophotography image frame and then grade and file-sort based on a calculated "quality" rating. This is useful to help cull bad image files before futher processing in astrophotograph stacking software such as DeepSky Stacker, PixInsight, Siril.

Specifically developed to analyze filenames generated while using N.I.N.A astrophotography aquisition software, this script could also be adapted to sort astronomy image files created by other means as well. N.I.N.A has the ability to configure custom filenames or headers that contain metrics of the saved astrophotography "light" frames (main photograph of a celestial object). 

<img width="2796" height="1449" alt="image" src="https://github.com/user-attachments/assets/5f5c1fb3-ce8d-4d09-8296-2957061309e7" />

<img width="1103" height="513" alt="image" src="https://github.com/user-attachments/assets/deb8aae8-76c2-426a-a2ee-a750303dd75f" />

<img width="1103" height="513" alt="image" src="https://github.com/user-attachments/assets/86f38bad-91ff-4145-a047-552c522518d7" />

The metrics from any given filename are combined to create a quality "score", which is then used to sequentially re-name the files in the chosen directoty with a 4-digit serial number and then sort from lowest to highest. 

<img width="2421" height="364" alt="image" src="https://github.com/user-attachments/assets/812b4a2e-89b9-459e-84f4-66a63d5ca220" />

<img width="1075" height="562" alt="image" src="https://github.com/user-attachments/assets/16d01896-6239-44bb-b4e2-fa3b609c6b72" />

Because the filename can be structured many different ways, the index position of said image metrics is variable, therefore, the user must specify these parameters in a seperate config .ini file which is used by the main script to properly parse the filenames.

<img width="1507" height="1285" alt="image" src="https://github.com/user-attachments/assets/5275b131-9ecf-48ba-aa6f-46e42e1c487c" />

A log.txt file is generated upon exectution of the script which contains a list of the sorted astrophotography iamge files, as well as a summary of various performance metrics such as highest star count, average star count etc.

<img width="978" height="750" alt="image" src="https://github.com/user-attachments/assets/d826ef25-9e53-47b8-920a-1197839cd3c3" />

<img width="1062" height="1057" alt="image" src="https://github.com/user-attachments/assets/008fdeb9-8bf1-4389-9d94-1cf37fe94737" />

The user must specify the relative path upon runtime for the script to work correctly, if the relative path does not exist or not extered correctly, an error handler will catch this and flag it in a log file that is saved in the same parent directory that the .py file is run from.

This script is to some extent redundant, as many astrophotography editing applications already have the ability to filter and rate iamge frames based on metrics already, however, the intent of this project was to be able to windows-file-sort the image files so that the user can easily visualize from a folder-context which are the best quality light-frames to then use further.
