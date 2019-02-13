"""
MIT License

Copyright (c) 2019 Eduardo Henrique Vieira dos Santos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""



import subprocess, sys, os, time
from PIL import Image
import numpy as np
import cv2



############################
##### Script arguments #####
############################


preview = 1 # Default FPS for encoding the output
if '-preview' in sys.argv:
	try:
		preview = int(sys.argv[sys.argv.index('-preview')+1])
	except Exception as e:
		print('Error: especify a valid value for preview (integer 0/1)')
		exit()

fps = 10 # Default FPS for encoding the output
if '-fps' in sys.argv:
	try:
		fps = float(sys.argv[sys.argv.index('-fps')+1])
	except Exception as e:
		print('Error: especify a valid value for fps rate (float)')
		exit()

timelapse = 100 # Wait delay for taking the next frame
if '-timelapse' in sys.argv:
	try:
		timelapse = (int(sys.argv[sys.argv.index('-timelapse')+1])*0.0001)
	except Exception as e:
		print('Error: especify a valid value for timelapse in milisseconds (integer)')
		exit()

window = 'root' # Window id to be captured
if '-window' in sys.argv:
	try:
		window = sys.argv[sys.argv.index('-window')+1]
	except Exception as e:
		print('Error: especify a valid value for window name (hex)')
		exit()

"""
# By default it uses 10MB of RAM for swaping from printscreen to stack the frames
# this option is about creating tmp on RAM
ram = int(10)
if '-ram' in sys.argv:
	try:
		ram = int(sys.argv[sys.argv.index('-ram')+1])
	except Exception as e:
		print('Error: especify a value for ram in MB (integer)')
		exit()
"""



##########################
##### Create folders #####
##########################


# Check if folder for temporary files not exist
if not (os.path.isdir("tmp")):
	try:
		#Create its folder
		subprocess.call(['mkdir', 'tmp'])
	except Exception as e:
		raise e
		exit()

# Check if folder for output files not exist
if not (os.path.isdir("output")):
	try:
		#Create it
		subprocess.call(['mkdir', 'output'])
	except Exception as e:
		raise e
		exit()



##############################################
##### Try to run import from imagemagick #####
##############################################


try:
	subprocess.call(['import', '-window', window, 'tmp/screen.jpg'])
except Exception as e:
	print('Error: Missing dependency: apt-get install imagemagick')
	exit()



#####################
##### MAIN LOOP #####
#####################


if preview != 0:
	cv2.namedWindow('Screen',cv2.WINDOW_NORMAL)
out = None

fps_time = time.time()
while 1:
	# Wait next frame (for timelapses)
	time.sleep(timelapse)
	im = None
	# Take screenshot
	subprocess.call(['import', '-window', window, 'tmp/screen.jpg'])
	# Force to read image file when it is ready
	while type(im) == type(None):
		try:
			# Read captured frame
			im = cv2.imread('tmp/screen.jpg')
		except Exception as e:
			pass
	if out is None:
		size = im.shape[1], im.shape[0]
		# Missing code for resizing output
		out = cv2.VideoWriter('output/'+str(time.time())+'.avi',cv2.VideoWriter_fourcc(*"XVID"), fps, size, True)
	# Write frame into the output file
	out.write(im)
	if preview != 0:
		# Show preview screen
		cv2.imshow('Screen', im )
	# Calculate the FPS
	fps = 1.0 / (time.time() - fps_time)
	# Print FPS
	print("FPS rate: "+str(fps))
	# FPS startpoint interval
	fps_time = time.time()
	if cv2.waitKey(25) & 0xFF == ord('q'):
		# If q key got pressed, then exit
		cv2.destroyAllWindows()
		out.release()
		subprocess.call(['rm','-rf', 'tmp'])
		break



"""
Notes
	For gnome screenshot
		subprocess.call(['gnome-screenshot', '-f', 'tmp/screen.jpg'])
		subprocess.call("gnome-screenshot -f tmp/screen.jpg", shell=True)
	
	For mount/umount tmp into memory
		# Create folder for mounting into the RAM
		subprocess.call(['sudo','mkdir', '-p', 'tmp'])
		# Mount folder into the RAM after create its folder
		try:
			#Mount it into the RAM for faster access
			subprocess.call(['sudo','mount', '-t', 'tmpfs', '-o', 'size='+str(ram)+'M', 'tmpfs', 'tmp/'])
		except Exception as e:
			raise e
			exit()
		# Test for umount tmp after release the output
		subprocess.call(['sudo','umount', 'tmp'])
		subprocess.call(['sudo','rm','-rf', 'tmp'])
"""