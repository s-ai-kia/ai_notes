import logging
import os

import torch.utils.data as data
from PIL import Image
from torchvision import transforms

#logging.basicConfig()
#logger = logging.getLogger()
#logger.setLevel(logging.INFO)


class Landmarks(data.Dataset):

    def __init__(self, data_dir, allfiles, is_test, dataidxs=None, train=True, transform=None, target_transform=None,
                 download=False):
        """
        allfiles is [{'user_id': xxx, 'image_id': xxx, 'class': xxx} ...  
                     {'user_id': xxx, 'image_id': xxx, 'class': xxx} ... ]
        """
        self.allfiles = allfiles
        if dataidxs == None:
            self.local_files = self.allfiles
        else:
            self.local_files = self.allfiles[dataidxs[0]: dataidxs[1]]
            # print("self.local_files: %d, dataidxs: (%d, %d)" % (len(self.local_files), dataidxs[0], dataidxs[1]))
        self.data_dir = data_dir
        self.dataidxs = dataidxs
        self.transform = transform
        self.target_transform = target_transform
        self.is_test = is_test

    def __len__(self):
        # if self.user_id != None:
        #     return sum([len(local_data) for local_data in self.mapping_per_user.values()])
        # else:
        #     return len(self.mapping_per_user)
        return len(self.local_files)

    def __getitem__(self, idx):
        # if self.user_id != None:
        #     img_name = self.mapping_per_user[self.user_id][idx]['image_id']
        #     label = self.mapping_per_user[self.user_id][idx]['class']
        # else:
        #     img_name = self.mapping_per_user[idx]['image_id']
        #     label = self.mapping_per_user[idx]['class']
        img_name = self.local_files[idx]['image_id']
        label = int(self.local_files[idx]['class'])
        data_sub_dir = os.path.join(self.data_dir, "train")
        if self.is_test:
            data_sub_dir = os.path.join(self.data_dir, "test")
        img_name = os.path.join(data_sub_dir, str(img_name) + ".jpg")

        # convert jpg to PIL (jpg -> Tensor -> PIL)
        image = Image.open(img_name)
        #print(img_name)
        #file = Image.open('/mnt/a458949a-4a38-496b-8f2d-3b5763b4e64f/rahulb/landmark_gld23k/'+img_name,'wb')
        #file.write(data)


        # jpg_to_tensor = transforms.ToTensor()
        # tensor_to_pil = transforms.ToPILImage()
        # image = tensor_to_pil(jpg_to_tensor(image))
        # image = jpg_to_tensor(image)

        if self.transform:
            image = self.transform(image)

        if self.target_transform:
            label = self.target_transform(label)

        return image, label
