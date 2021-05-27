import cv2
import numpy as np

video = cv2.VideoCapture('for_project.avi')

if(video.isOpened() == False):
	print("Error while opening file.")

width = int(video.get(3))
height = int(video.get(4))

out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 12, (width,height))

start = 0

trashold = 20

frame_num = 0

save_frame = 0

previous_gr = np.zeros((360,640))
current_gr = np.zeros((360,640))
next_gr = np.zeros((360,640))

dif_tmp1 = 0
dif_tmp2 = 0

logic_mask = np.zeros((360,640))

while(video.isOpened):
	if(start == 2):
	
		success, next_frame = video.read()
		frame_num = frame_num + 1
		print("Odradjeno", (frame_num/2160)*100 , "%")
		if(success == False):
			break
		next_gr = next_frame[:,:,0]
		for i in range(360):
			for j in range(640):
				dif_tmp1 = int(current_gr[i,j]) - int(previous_gr[i,j])
				
				dif_tmp2 = int(next_gr[i,j]) - int(current_gr[i,j])
				
				if(abs(dif_tmp1) > trashold):
					if(abs(dif_tmp2) > trashold):
						logic_mask[i,j] = 1
					else:
						logic_mask[i,j] = 0
				else:
					logic_mask[i,j] = 0			
		for i in range(359):
	      		for j in range(639):
	      			if(i > 0):
	      				if(j > 0):
	      					if(logic_mask[i,j] == 1):
	      						if(logic_mask[i,j-1] == 1):
	      							if(logic_mask[i-1,j] == 1):
	      								if(logic_mask[i-1,j-1] == 1):
	      									if(logic_mask[i,j+1] == 1):
	      										if(logic_mask[i+1,j] == 1):
	      											if(logic_mask[i+1,j+1] == 1):
	      												if(logic_mask[i-1,j+1] == 1):
	      													if(logic_mask[i+1,j-1] == 1):
	      														save_frame = 1
		if(save_frame == 1):
	      		out.write(current_frame)
	      		save_frame = 0
		previous_frame = current_frame
		current_frame = next_frame
	    	
		previous_gr = current_gr
		current_gr= next_gr
				
	else:
	
		if(start == 0):
		
			success, previous_frame = video.read()
			start = start + 1
			frame_num = frame_num + 1
			if(success == False):
				break
			previous_gr = previous_frame[:,:,0]
		else:
		
			success, current_frame = video.read()
			start = start + 1
			frame_num = frame_num + 1
			if(success == False):
				break
			current_gr = current_frame[:,:,0]
			
out.release()
video.release()
