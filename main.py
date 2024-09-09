from image_downloader import image_downloader
from matplotlib import pyplot as plt    
from datetime import datetime, timedelta
img_loader = image_downloader()
from tqdm import tqdm

#time_range = ("2022-10-01T00:00:00Z", "2022-10-31T00:00:00Z")
x,y,w,h=  8.5,52., 0.05, 0.05

for a in tqdm(range(-5,5)):
    for b in range (-5,5):
        for i in range(100):
            time_start = datetime.fromisoformat("2015-10-01T00:00:00Z")+timedelta(days=30)*i #2015-10-01T00:00:00Z seems to be start of the dataset
            time_end = time_start+timedelta(days=30)
            time_range = (time_start.isoformat(), time_end.isoformat())
            bbox = [x+a*w,y+b*h, x+w+a*w, y+h+b*h]
            img = img_loader.download_image( bbox, time_range, 1024,1024)

            # plt.imshow(img)
            # plt.show()

