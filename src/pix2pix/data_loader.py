import scipy
from glob import glob
import numpy as np
import matplotlib.pyplot as plt

class DataLoader():
    def __init__(self, dataset_name, img_res=(128, 128)):
        self.dataset_name = dataset_name
        self.img_res = img_res

    def load_data(self, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "test"
        path = glob('./datasets/%s/%s/*' % (self.dataset_name, data_type))

        batch_images = np.random.choice(path, size=batch_size)

        imgs_A = []
        imgs_B = []
        for img_path in batch_images:
            img = self.imread(img_path)

            h, w, _ = img.shape
            _w = int(w/2)
            img_A, img_B = img[:, :_w, :], img[:, _w:, :]

            img_A = scipy.misc.imresize(img_A, self.img_res)
            img_B = scipy.misc.imresize(img_B, self.img_res)

            # If training => do random flip
            if not is_testing and np.random.random() < 0.5:
                img_A = np.fliplr(img_A)
                img_B = np.fliplr(img_B)

            imgs_A.append(img_A)
            imgs_B.append(img_B)

        imgs_A = np.array(imgs_A)/127.5 - 1.
        imgs_B = np.array(imgs_B)/127.5 - 1.

        return imgs_A, imgs_B

    def load_batch(self, domain="A", batch_size=1, is_testing=False):
        data_type = "train%s" % domain if not is_testing else "test%s" % domain
        path = glob('./datasets/%s/%s/*' % (self.dataset_name, data_type))

        self.n_batches = int(len(path) / batch_size)

        for i in range(self.n_batches-1):
            batch = path[i*batch_size:(i+1)*batch_size]
            imgs_A, imgs_B = [], []
            for img_A in batch:
                if "A/" in img_A:
                  img_B = img_A.replace('s1_', 's2_')
                  img_B = img_B.replace('A/', 'B/')
                else:
                  img_B = img_A.replace('s2_', 's1_')
                  img_B = img_B.replace('B/', 'A/')

                img_A = self.imread(img_A)
                img_B = self.imread(img_B)

                img_A = scipy.misc.imresize(img_A, self.img_res)
                img_B = scipy.misc.imresize(img_B, self.img_res)

                if not is_testing and np.random.random() > 0.5:
                        img_A = np.fliplr(img_A)
                        img_B = np.fliplr(img_B)

                imgs_A.append(img_A)
                imgs_B.append(img_B)

            imgs_A = np.array(imgs_A)/127.5 - 1.
            imgs_B = np.array(imgs_B)/127.5 - 1.

            yield imgs_A, imgs_B

    def load_data_with_label_batch(self, domain, batch_size=1, is_testing=False):
        data_type = "train%s" % domain if not is_testing else "test%s" % domain
        path = glob('./datasets/%s/%s/*' % (self.dataset_name, data_type))
        batch_images = np.random.choice(path, size=batch_size)
        imgs = []
        lbls = []
        for img_path in batch_images:
            img = self.imread(img_path)
            # lbl path
            if "A/" in img_path:
              lbl_path = img_path.replace('s1_', 's2_')
              lbl_path = lbl_path.replace('A/', 'B/')
            else:
              lbl_path = img_path.replace('s2_', 's1_')
              lbl_path = lbl_path.replace('B/', 'A/')
            lbl = self.imread(lbl_path)

            if not is_testing:
                img = scipy.misc.imresize(img, self.img_res)
                lbl = scipy.misc.imresize(lbl, self.img_res)

                if np.random.random() > 0.5:
                    img = np.fliplr(img)
                    lbl = np.fliplr(lbl)
            else:
                img = scipy.misc.imresize(img, self.img_res)
                lbl = scipy.misc.imresize(lbl, self.img_res)
            imgs.append(img)
            lbls.append(lbl)
        imgs = np.array(imgs)/127.5 - 1.
        lbls = np.array(lbls)/127.5 - 1.
        return imgs, lbls


    def imread(self, path):
        return scipy.misc.imread(path, mode='RGB').astype(np.float)
