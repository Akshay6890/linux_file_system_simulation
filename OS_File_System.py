from math import ceil
import gc
#from pyautogui import typewrite
import curses
import npyscreen
import os
from tkinter import *

sector_size = 512
number_of_sectors = 1000
free_disk_space={x:True for x in range(0,number_of_sectors)}
hard_disk=[None for x in range(0,number_of_sectors)]
sectors_occupied=0
data_sectors=0
dir_sectors=0
dir_sectors_obj_track={}
file_seek_position={}

class DataSector:
    def __init__(self):
        self.forward_sector=0
        self.backward_sector=0
        self.sector_data=[]

    def initializeForwardPointer(self, forward_pointer):
        self.forward_sector=forward_pointer
    def initializeBackwardPointer(self, backward_pointer):
        self.backward_sector=backward_pointer
    def initializeSectorData(self, sector_data):
        self.sector_data.clear()
        self.sector_data.extend(sector_data)

class DirectorySector:
    forward_sector=0
    backward_sector=0
    filler=""
    empty_space=""
    number_of_records=0
    dir_data=[]


if __name__ == "__main__":
    os.system('clear')
    root_dir = DirectorySector()
    root_dir.backward_sector=-1
    root_dir.forward_sector=-1
    root_dir.filler=""
    root_dir.empty_space=""
    hard_disk[0]=root_dir
    #sectors_occupied+=1
    dir_sectors_obj_track[root_dir]=0
    free_disk_space[0]=False
    print('Below are the valid commands and their syntax')
    print('\ncommand: exit -- exits the file system program -- syntax: exit')
    print('\ncommand: ls -- lists all the files on the disk -- syntax: ls')
    print('\ncommand: vi -- creates a new file if the file does not exist else a prompt is shown to edit existing file -- syntax: vi <file_name_with_extension>')
    print('\ncommand: del -- deletes the mention file -- syntax: del <file_name_with_extension>')
    print('\ncommand: seek -- moves the pointer of the file to given position and prints data from that position to end -- syntax: seek <file_name_with_extension> <pointer_position>')
    print('\n--seek -> gives an error if the position of the cursor goes out of bounds')
    print('\ncommand: cat -- prints the contents of the file -- syntax: cat <file_name_with_extension>')
    print('\ncommand: clear -- clears the terminal -- syntax: clear')
    print('\ncommand: help -- lists all the commands -- syntax: help\n')
    while(1):
        cmd = input('Akshay/filesystemcode> ')
        if cmd=="exit":
            hard_disk.clear()
            exit()
        else:
            if cmd=="ls":
                #print(hard_disk)
                for ob in gc.get_objects():
                    if isinstance(ob, DirectorySector):
                        #print(str(ob.forward_sector)+" "+str(ob.backward_sector))
                        #print(ob.dir_data)
                        for x in ob.dir_data:
                            if x[0]=="u":
                                print(x[1]+" "+str(x[3]))
            elif cmd.startswith("vi"):
                forward_pointer_list=[]
                backward_pointer_list=[]
                file_exists=False
                new_filename = cmd.split(' ')[1]
                for ob in gc.get_objects():
                    if isinstance(ob, DirectorySector):
                        for x in ob.dir_data:
                            if x[1]==new_filename and x[0]!='A':
                                file_exists=True
                                input_selection=input('File already exists, do you want to edit it? (Y/N): ')
                                if input_selection=="N":
                                    pass
                                else:
                                    current_file_editing_data=""
                                    if hard_disk[x[2]].forward_sector==-1:
                                        current_sector_data=(hard_disk[x[2]].sector_data)[:]
                                        current_file_editing_data=''.join(current_sector_data)
                                    else:
                                        #print("inside")
                                        
                                        file_sector_track=x[2]
                                        current_sector_data=(hard_disk[file_sector_track].sector_data)[:]
                                        ccurrent_file_editing_data=''.join(current_sector_data)
                                        
                                        
                                        while hard_disk[file_sector_track].forward_sector!=-1:
                                            
                                            current_file_editing_data+=''.join((hard_disk[file_sector_track].sector_data)[:])
                                            file_sector_track=hard_disk[file_sector_track].forward_sector

                                        current_file_editing_data+=''.join((hard_disk[file_sector_track].sector_data)[:])
                                    
                                    #print(current_file_editing_data)


                                    stdscr = curses.initscr()
                                    curses.noecho()  # Disable automatic echoing of keys to the screen
                                    curses.cbreak()  # Take input without requiring Enter key
                                    stdscr.keypad(True) 

                                    F = npyscreen.Form(name="Text Editor")

                                    my_text = F.add(npyscreen.Textfield, value=current_file_editing_data)

                                    # Display the form
                                    F.edit()

                                    curses.endwin()

                                    file_data = list(my_text.value)
                                    number_of_sectors_required = ceil(len(file_data)/504)
                                    #print(number_of_sectors_required)
                                    if number_of_sectors_required==1 and hard_disk[x[2]].forward_sector==-1:
                                        hard_disk[x[2]].sector_data.clear()
                                        temp_hold=file_data[0:len(file_data)]
                                        hard_disk[x[2]].sector_data.extend(temp_hold)
                                        x[3]=len(file_data)
                                    else:
                                        if hard_disk[x[2]].forward_sector==-1:
                                            number_of_sectors_required-=1
                                            current_sectors_indexes=[]
                                            current_sectors_indexes.append(x[2])
                                            prev_index=0
                                            count_temp=0
                                            prev_sector=x[2]
                                            backward_pointer_list.append(-1)
                                            for disk_space_index in range(1,len(hard_disk)):
                                                if hard_disk[disk_space_index]==None and free_disk_space[disk_space_index]==True and count_temp<number_of_sectors_required:
                                                    if count_temp==0:
                                                        current_sectors_indexes.append(disk_space_index)
                                                        free_disk_space[disk_space_index]=False
                                                        forward_pointer_list.append(disk_space_index)
                                                        backward_pointer_list.append(prev_sector)
                                                        prev_sector=disk_space_index
                                                        count_temp+=1
                                                    else:
                                                        current_sectors_indexes.append(disk_space_index)
                                                        free_disk_space[disk_space_index]=False
                                                        forward_pointer_list.append(disk_space_index)
                                                        backward_pointer_list.append(prev_sector)
                                                        prev_sector=disk_space_index
                                                        count_temp+=1
                                            forward_pointer_list.append(-1)

                                            prev_index=0
                                            for sector_index in range(len(current_sectors_indexes)):
                                                if sector_index==0:
                                                    hard_disk[x[2]].sector_data.clear()
                                                    hard_disk[x[2]].sector_data.extend(file_data[prev_index:prev_index+504])
                                                    hard_disk[x[2]].forward_sector=forward_pointer_list[sector_index]
                                                    x[3]=len(file_data)
                                                    prev_index+=504
                                                if sector_index<len(current_sectors_indexes)-1:
                                                    file = DataSector()
                                                    file.initializeBackwardPointer(backward_pointer_list[sector_index])
                                                    file.initializeForwardPointer(forward_pointer_list[sector_index])
                                                    file.initializeSectorData(file_data[prev_index:prev_index+504])
                                                    hard_disk[current_sectors_indexes[sector_index]]=file
                                                    prev_index+=504
                                                else:
                                                    file=DataSector()
                                                    file.initializeBackwardPointer(backward_pointer_list[sector_index])
                                                    file.initializeBackwardPointer(forward_pointer_list[sector_index])
                                                    file.initializeSectorData(file_data[prev_index:len(file_data)])
                                                    hard_disk[current_sectors_indexes[sector_index]]=file
                                        else:
                                            current_sectors_indexes=[]
                                            file_sector_track=x[2]
                                            current_sectors_indexes.append(x[2])
                                            while file_sector_track!=-1:
                                                if hard_disk[hard_disk[file_sector_track].forward_sector].forward_sector!=-1:
                                                    current_sectors_indexes.append(hard_disk[file_sector_track].forward_sector)
                                                    file_sector_track=hard_disk[hard_disk[file_sector_track].forward_sector].forward_sector
                                                else:
                                                    current_sectors_indexes.append(hard_disk[file_sector_track].forward_sector)
                                                    file_sector_track=-1
                                            #print(current_sectors_indexes)

                                            if len(current_sectors_indexes) == number_of_sectors_required:
                                                for i in range(number_of_sectors_required):
                                                    if i!=number_of_sectors_required-1:
                                                        hard_disk[current_sectors_indexes[i]].sector_data.clear()
                                                        temp_hold=file_data[prev_index:prev_index+504]
                                                        hard_disk[current_sectors_indexes[i]].sector_data.extend(temp_hold)
                                                        prev_index+=504
                                                    else:
                                                        hard_disk[current_sectors_indexes[i]].sector_data.clear()
                                                        temp_hold=file_data[prev_index:len(file_data)]
                                                        hard_disk[current_sectors_indexes[i]].sector_data.extend(temp_hold)
                                                x[3]=len(file_data)

                                            elif len(current_sectors_indexes) < number_of_sectors_required:
                                                number_of_sectors_required-=len(current_sectors_indexes)
                                                count_temp=0
                                                for disk_space_index in range(1,len(hard_disk)):
                                                    if hard_disk[disk_space_index]==None and free_disk_space[disk_space_index]==True and count_temp<number_of_sectors_required:
                                                        current_sectors_indexes.append(disk_space_index)
                                                        count_temp+=1
                                                    else:
                                                        if count_temp==number_of_sectors_required:
                                                            break

                                                #print(current_sectors_indexes)

                                                forward_pointer_list.clear()
                                                backward_pointer_list.clear()
                                                for i in range(len(current_sectors_indexes)):
                                                    if i==0:
                                                        forward_pointer_list.append(current_sectors_indexes[i+1])
                                                        backward_pointer_list.append(-1)
                                                    elif i==len(current_sectors_indexes)-1:
                                                        forward_pointer_list.append(-1)
                                                        backward_pointer_list.append(current_sectors_indexes[i-1])
                                                    else:
                                                        forward_pointer_list.append(current_sectors_indexes[i+1])
                                                        backward_pointer_list.append(current_sectors_indexes[i-1])

                                                #print(forward_pointer_list)
                                                #print(backward_pointer_list)

                                                for i in range(len(current_sectors_indexes)):
                                                    if i!=len(current_sectors_indexes)-1:
                                                        if hard_disk[current_sectors_indexes[i]]!=None:
                                                            hard_disk[current_sectors_indexes[i]].sector_data.clear()
                                                            hard_disk[current_sectors_indexes[i]].forward_sector=forward_pointer_list[i]
                                                            hard_disk[current_sectors_indexes[i]].backward_sector=backward_pointer_list[i]
                                                            temp_hold=file_data[prev_index:prev_index+504]
                                                            hard_disk[current_sectors_indexes[i]].sector_data.extend(temp_hold)
                                                            prev_index+=504
                                                        else:
                                                            temp_hold=file_data[prev_index:prev_index+504]
                                                            file = DataSector()
                                                            file.initializeForwardPointer(forward_pointer_list[i])
                                                            file.initializeBackwardPointer(backward_pointer_list[i])
                                                            file.initializeSectorData(temp_hold)
                                                            hard_disk[current_sectors_indexes[i]]=file
                                                            free_disk_space[current_sectors_indexes[i]]=False
                                                            prev_index+=504
                                                    else:
                                                        if hard_disk[current_sectors_indexes[i]]!=None:
                                                            hard_disk[current_sectors_indexes[i]].sector_data.clear()
                                                            hard_disk[current_sectors_indexes[i]].forward_sector=forward_pointer_list[i]
                                                            hard_disk[current_sectors_indexes[i]].backward_sector=backward_pointer_list[i]
                                                            temp_hold=file_data[prev_index:len(file_data)]
                                                            hard_disk[current_sectors_indexes[i]].sector_data.extend(temp_hold)
                                                        else:
                                                            temp_hold=file_data[prev_index:len(file_data)]
                                                            file = DataSector()
                                                            file.initializeForwardPointer(forward_pointer_list[i])
                                                            file.initializeBackwardPointer(backward_pointer_list[i])
                                                            file.initializeSectorData(temp_hold)
                                                            hard_disk[current_sectors_indexes[i]]=file
                                                            free_disk_space[current_sectors_indexes[i]]=False
                                            
                                            elif len(current_sectors_indexes) > number_of_sectors_required:
                                                prev_index=0
                                                for i in range(len(current_sectors_indexes)):
                                                    if i<number_of_sectors_required:
                                                        if i!=number_of_sectors_required-1:
                                                            temp_hold=file_data[prev_index:prev_index+504]
                                                            hard_disk[current_sectors_indexes[i]].sector_data.clear()
                                                            hard_disk[current_sectors_indexes[i]].sector_data.extend(temp_hold)
                                                            prev_index+=504
                                                        else:
                                                            temp_hold=file_data[prev_index:len(file_data)]
                                                            hard_disk[current_sectors_indexes[i]].forward_pointer=-1
                                                            hard_disk[current_sectors_indexes[i]].sector_data.clear()
                                                            hard_disk[current_sectors_indexes[i]].sector_data.extend(temp_hold)
                                                    else:
                                                        del hard_disk[current_sectors_indexes[i]]
                                                        hard_disk[current_sectors_indexes[i]]=None
                                                        free_disk_space[current_sectors_indexes[i]]=True
                                            x[3]=len(file_data)

                if not file_exists:
                    file_data = list(input())
                    
                    if len(file_data)>504:
                        current_sectors_indexes=[]
                        prev_index=0
                        count_temp=0
                        prev_sector=0
                        backward_pointer_list.append(-1)
                        number_of_sectors_required = ceil(len(file_data)/504)
                        for disk_space_index in range(1,len(hard_disk)):
                            if hard_disk[disk_space_index]==None and free_disk_space[disk_space_index]==True and count_temp<number_of_sectors_required:
                                if count_temp==0:
                                    current_sectors_indexes.append(disk_space_index)
                                    free_disk_space[disk_space_index]=False
                                    #forward_pointer_list.append(disk_space_index)
                                    backward_pointer_list.append(disk_space_index)
                                    prev_sector=disk_space_index
                                    count_temp+=1
                                elif count_temp==number_of_sectors_required-1:
                                    current_sectors_indexes.append(disk_space_index)
                                    free_disk_space[disk_space_index]=False
                                    forward_pointer_list.append(disk_space_index)
                                    forward_pointer_list.append(-1)
                                    #backward_pointer_list.append(prev_sector)
                                    count_temp+=1
                                elif count_temp<number_of_sectors_required:
                                    current_sectors_indexes.append(disk_space_index)
                                    free_disk_space[disk_space_index]=False
                                    forward_pointer_list.insert(len(forward_pointer_list)-1,disk_space_index)
                                    backward_pointer_list.append(prev_sector)
                                    prev_sector=disk_space_index
                                    count_temp+=1
                            else:
                                break
                        if len(root_dir.dir_data)<30:
                            root_dir.dir_data.append(['u',new_filename,current_sectors_indexes[0],len(file_data)])
                            root_dir.number_of_records+=1
                            dir_sectors_obj_track[root_dir]=root_dir.number_of_records
                            for pointer in range(number_of_sectors_required):
                                if pointer<number_of_sectors_required-1:
                                    file = DataSector()
                                    file.initializeForwardPointer(forward_pointer_list[pointer])
                                    file.initializeBackwardPointer(backward_pointer_list[pointer])
                                    temp_hold=file_data[prev_index:prev_index+504]
                                    file.initializeSectorData(temp_hold[:])
                                    hard_disk[current_sectors_indexes[pointer]]=file
                                    prev_index+=504
                                else:
                                    file1 = DataSector()
                                    file1.initializeForwardPointer(forward_pointer_list[pointer])
                                    file1.initializeBackwardPointer(backward_pointer_list[pointer])
                                    temp_hold1=file_data[prev_index:len(file_data)]
                                    file1.initializeSectorData(temp_hold1[:])
                                    hard_disk[current_sectors_indexes[pointer]]=file1
                        else:
                            for key,value in dir_sectors_obj_track.items():
                                if value==31:
                                    continue
                                elif value==30:
                                    prev_sector_pointer=0
                                    for i in range(len(hard_disk)):
                                        if hard_disk[i]==key:
                                            prev_sector_pointer=i
                                    dir_general = DirectorySector()
                                    dir_general.backward_sector=prev_sector_pointer
                                    dir_general.forward_sector=-1
                                    dir_general.filler=""
                                    dir_general.empty_space=""
                                    for disk_space_index in range(0,len(hard_disk)):
                                        if hard_disk[disk_space_index] == None and free_disk_space[disk_space_index]==True:
                                            key.dir_data.append(['d','d'+str(disk_space_index),disk_space_index,512])
                                            key.forward_sector=disk_space_index
                                            key.number_of_records+=1
                                            dir_sectors_obj_track[key]=key.number_of_records
                                            hard_disk[disk_space_index]=dir_general
                                            free_disk_space[disk_space_index]=False
                                            dir_general.dir_data.append(['u',new_filename,current_sectors_indexes[0],len(file_data)])
                                            dir_general.number_of_records+=1
                                            dir_sectors_obj_track[dir_general]=dir_general.number_of_records
                                            break
                                    for pointer in range(number_of_sectors_required):
                                        if pointer<number_of_sectors:
                                            file = DataSector()
                                            file.initializeForwardPointer(forward_pointer_list[pointer])
                                            file.initializeBackwardPointer(backward_pointer_list[pointer])
                                            file.initializeSectorData(file_data[prev_index:prev_index+504])
                                            hard_disk[current_sectors_indexes[pointer]]=file
                                            prev_index+=504
                                        else:
                                            file=DataSector()
                                            file.initializeForwardPointer(forward_pointer_list[pointer])
                                            file.initializeBackwardPointer(backward_pointer_list[pointer])
                                            file.initializeSectorData(file_data[prev_index:len(file_data)])
                                            hard_disk[current_sectors_indexes[pointer]]=file
                                    break
                                else:
                                    key.dir_data.append(['u',new_filename,current_sectors_indexes[0],len(file_data)])
                                    key.number_of_records+=1
                                    dir_sectors_obj_track[key]=key.number_of_records
                                    for pointer in range(number_of_sectors_required):
                                        if pointer<number_of_sectors:
                                            file = DataSector()
                                            file.initializeForwardPointer(forward_pointer_list[pointer])
                                            file.initializeBackwardPointer(backward_pointer_list[pointer])
                                            file.initializeSectorData(file_data[prev_index:prev_index+504])
                                            hard_disk[current_sectors_indexes[pointer]]=file
                                            prev_index+=504
                                        else:
                                            file=DataSector()
                                            file.initializeForwardPointer(forward_pointer_list[pointer])
                                            file.initializeBackwardPointer(backward_pointer_list[pointer])
                                            file.initializeSectorData(file_data[prev_index:len(file_data)])
                                            hard_disk[current_sectors_indexes[pointer]]=file
                                    break
                    else:
                        if len(root_dir.dir_data)<30:
                            file = DataSector()
                            file.initializeBackwardPointer(-1)
                            file.initializeForwardPointer(-1)
                            file.initializeSectorData(file_data)
                            for disk_space_index in range(0,len(hard_disk)):
                                if hard_disk[disk_space_index] == None and free_disk_space[disk_space_index]==True:
                                    free_disk_space[disk_space_index]=False
                                    hard_disk[disk_space_index]=file
                                    root_dir.dir_data.append(['u',new_filename,disk_space_index,len(file_data)])
                                    root_dir.number_of_records+=1
                                    dir_sectors_obj_track[root_dir]=root_dir.number_of_records
                                    break
                        else:
                            for key,value in dir_sectors_obj_track.items():
                                if value==31:
                                    continue
                                elif value==30:
                                    for i in range(len(hard_disk)):
                                        if hard_disk[i]==key:
                                            prev_sector_pointer=i
                                    dir_general = DirectorySector()
                                    dir_general.backward_sector=prev_sector_pointer
                                    dir_general.forward_sector=-1
                                    dir_general.filler=""
                                    dir_general.empty_space=""
                                    for disk_space_index in range(0,len(hard_disk)):
                                        if hard_disk[disk_space_index] == None and free_disk_space[disk_space_index]==True:
                                            key.dir_data.append(['d','d'+str(disk_space_index),disk_space_index,512])
                                            key.forward_sector=disk_space_index
                                            key.number_of_records+=1
                                            dir_sectors_obj_track[key]=key.number_of_records
                                            hard_disk[disk_space_index]=dir_general
                                            free_disk_space[disk_space_index]=False
                                    file = DataSector()
                                    file.initializeBackwardPointer(-1)
                                    file.initializeForwardPointer(-1)
                                    file.initializeSectorData(file_data)
                                    for disk_space_index in range(0,len(hard_disk)):
                                        if hard_disk[disk_space_index] == None and free_disk_space[disk_space_index]==True:
                                            free_disk_space[disk_space_index]=False
                                            hard_disk[disk_space_index]=file
                                            dir_general.dir_data.append(['u',new_filename,disk_space_index,len(file_data)])       
                                            dir_general.number_of_records+=1
                                            dir_sectors_obj_track[dir_general]=dir_general.number_of_records
                                            break
                                else:
                                    file = DataSector()
                                    file.initializeBackwardPointer(-1)
                                    file.initializeForwardPointer(-1)
                                    file.initializeSectorData(file_data)
                                    for disk_space_index in range(0,len(hard_disk)):
                                        if hard_disk[disk_space_index] == None and free_disk_space[disk_space_index]==True:
                                            free_disk_space[disk_space_index]=False
                                            hard_disk[disk_space_index]=file
                                            key.dir_data.append(['u',new_filename,disk_space_index,len(file_data)])       
                                            key.number_of_records+=1
                                            dir_sectors_obj_track[key]=key.number_of_records
                                            break
            elif cmd.startswith("del"):
                file_found=False
                file_name = cmd.split(' ')[1]
                for ob in gc.get_objects():
                    if isinstance(ob, DirectorySector):
                        for f_name in ob.dir_data:
                            if f_name[1]==file_name and f_name[0]!='A':
                                file_found=True
                                f_name[0]='A'
                                if hard_disk[f_name[2]].forward_sector==-1:
                                    del hard_disk[f_name[2]]
                                    hard_disk[f_name[2]]=None
                                    free_disk_space[f_name[2]]=True
                                    f_name[3]=0
                                    break
                                else:
                                    current_sectors_indexes=[]
                                    current_sectors_indexes.append(f_name[2])
                                    c_forward_sector=hard_disk[f_name[2]].forward_sector
                                    while c_forward_sector!=-1:
                                        current_sectors_indexes.append(c_forward_sector)
                                        c_forward_sector=hard_disk[c_forward_sector].forward_sector
                                    for i in range(len(current_sectors_indexes)):
                                        del hard_disk[current_sectors_indexes[i]]
                                        hard_disk[current_sectors_indexes[i]]=None
                                        free_disk_space[current_sectors_indexes[i]]=True
                                    f_name[3]=0
                                    break
                if not file_found:
                    print("File not found!")
            
            elif cmd.startswith("seek"):
                file_found=False
                file_name = cmd.split(' ')[1]
                seek_position = int(cmd.split(' ')[2])
                for ob in gc.get_objects():
                    if isinstance(ob, DirectorySector):
                        for f_name in ob.dir_data:
                            if f_name[1]==file_name and f_name[0]!='A':
                                file_found=True
                                if seek_position<=f_name[3] and seek_position>0:
                                    
                                    file_seek_position[file_name]=seek_position
                                    current_file_editing_data=""
                                    
                                    if hard_disk[f_name[2]].forward_sector==-1:
                                        current_sector_data=(hard_disk[f_name[2]].sector_data)[:]
                                        current_file_editing_data=''.join(current_sector_data)
                                    else:
                                        file_sector_track=f_name[2]
                                        current_sector_data=(hard_disk[file_sector_track].sector_data)[:]
                                        ccurrent_file_editing_data=''.join(current_sector_data)
                                        
                                        while hard_disk[file_sector_track].forward_sector!=-1:
                                            
                                            current_file_editing_data+=''.join((hard_disk[file_sector_track].sector_data)[:])
                                            file_sector_track=hard_disk[file_sector_track].forward_sector

                                        current_file_editing_data+=''.join((hard_disk[file_sector_track].sector_data)[:])
                                    
                                    print(current_file_editing_data[seek_position:])
                                    
                                    break
                                else:
                                    print("Pointer position goes out of bounds!")
                                    break
                if not file_found:
                    print("File not found!")

            elif cmd.startswith("cat"):
                file_found=False
                file_name = cmd.split(' ')[1]
                for ob in gc.get_objects():
                    if isinstance(ob, DirectorySector):
                        for f_name in ob.dir_data:
                            if f_name[1]==file_name and f_name[0]!='A':
                                file_found=True
                                current_file_editing_data=""
                                    
                                if hard_disk[f_name[2]].forward_sector==-1:
                                    current_sector_data=(hard_disk[f_name[2]].sector_data)[:]
                                    current_file_editing_data=''.join(current_sector_data)
                                else:
                                    file_sector_track=f_name[2]
                                    current_sector_data=(hard_disk[file_sector_track].sector_data)[:]
                                    ccurrent_file_editing_data=''.join(current_sector_data)
                                        
                                    while hard_disk[file_sector_track].forward_sector!=-1:
                                        current_file_editing_data+=''.join((hard_disk[file_sector_track].sector_data)[:])
                                        file_sector_track=hard_disk[file_sector_track].forward_sector

                                    current_file_editing_data+=''.join((hard_disk[file_sector_track].sector_data)[:])
                                print(current_file_editing_data)    
                                break
                if not file_found:
                    print("File not found!")

            elif cmd.startswith("help"):
                print('\n\nBelow are the valid commands and their syntax')
                print('\ncommand: exit -- exits the file system program -- syntax: exit')
                print('\ncommand: ls -- lists all the files on the disk -- syntax: ls')
                print('\ncommand: vi -- creates a new file if the file does not exist else a prompt is shown to edit existing file -- syntax: vi <file_name_with_extension>')
                print('\ncommand: del -- deletes the mention file -- syntax: del <file_name_with_extension>')
                print('\ncommand: seek -- moves the pointer of the file to given position and prints data from that position to end -- syntax: seek <file_name_with_extension> <pointer_position>')
                print('\n--seek -> gives an error if the position of the cursor goes out of bounds')
                print('\ncommand: cat -- prints the contents of the file -- syntax: cat <file_name_with_extension>')
                print('\ncommand: clear -- clears the terminal -- syntax: clear\n')
            
            elif cmd.startswith("clear"):
                os.system('clear')

            elif cmd=="":
                pass

            else:
                print("Command not found!")