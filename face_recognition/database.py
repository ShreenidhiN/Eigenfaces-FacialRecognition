

import os
import random
import cv2

class Database():
    curr_path = os.path.dirname(__file__)
    people_path = os.path.join(curr_path, "../data/people")
    test_path = os.path.join(curr_path, "../data/test")
    uid_to_name = {}

    def __init__(self):
        self.load_people()

    def load_people(self):
        '''
            Load the training images and assign 'Name' and 'UID' to each person
        '''
        entries = os.listdir(self.people_path)
        
        for entry in entries:
            e = entry.split("-")
            name, uid = "-".join(e[:-1]), e[-1]
            self.uid_to_name[uid] = name

    def create_person(self, name, imgs):
        '''
            Given the name of a person and his images, enter the person into the DB
        '''
        name = str(name)
        uid = str(random.randint(0, 99999999999))
        while uid in self.uid_to_name:
            uid = str(random.randint(0, 99999999999))

        self.uid_to_name[uid] = name

        entry = name + "-" + uid
        path_to_entry = os.path.join(self.people_path, entry)
        
        for i, im in enumerate(imgs):
            filename = os.path.join(path_to_entry, "face_"+str(i)+".jpg")
            os.makedirs(path_to_entry, exist_ok=True)
            cv2.imwrite(filename, im)

        return uid

    def update_person(self, uid, imgs):
        '''
            Update the images of a given user ( User ID)
        '''
        uid = str(uid)

        if uid in self.uid_to_name:
            entry = self.uid_to_name[uid] + "-" + uid
            path_to_entry = os.path.join(self.people_path, entry)
            
            #Finds the number of images already present for the given user
            last_face_num = max([int(file.split(".")[0].split("_")[-1]) for file in os.listdir(path_to_entry)]) 

            i = last_face_num + 1
            for im in imgs:
                filename = os.path.join(path_to_entry, "face_"+str(i)+".jpg")
                cv2.imwrite(filename, im)
                i+=1

        else:
            raise ValueError('Person not in DB but trying to update person!')

    def get_name(self, uid):
        uid = str(uid)
        return self.uid_to_name[uid] if uid in self.uid_to_name else "none"

    def get_faces(self, uid):
        '''
        Returns the faces of a single person
        '''
        uid = str(uid)
        if uid in self.uid_to_name:
            entry = self.uid_to_name[uid] + "-" + uid
            path_to_entry = os.path.join(self.people_path, entry)

            faces = []
            for file in os.listdir(path_to_entry):
                filename = os.path.join(path_to_entry, file)
                im = cv2.imread(filename, 0)
                faces.append(im)

                return faces
        else:
            raise ValueError('Person not in DB but trying to get faces!')


    def get_all_faces(self):
        '''
            Returns the faces of all people
        '''
        faces = []
        for uid in sorted(self.uid_to_name):
            name = self.uid_to_name[uid]
            entry = name + "-" + uid
            path_to_entry = os.path.join(self.people_path, entry)

            for file in os.listdir(path_to_entry):
                filename = os.path.join(path_to_entry, file)
                im = cv2.imread(filename, 0)
                faces.append((im, name, uid))

        return faces

    def get_test_faces(self):
        '''
            Returns the Test faces 
        '''
        faces = []
        for file in sorted(os.listdir(self.test_path)):
            im = os.path.join(self.test_path, file)
            img = cv2.imread(im, 0)
            faces.append((img, os.path.splitext(file)[0]))
        return faces
