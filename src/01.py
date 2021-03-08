import os, requests, subprocess
from osgeo import gdal
from osgeo import gdal_array

# Entry point
def main():
    cmd = "find ./data/ALOS* | grep tif"
    process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
    file_name_list = process.rsplit()
    for _file_name in file_name_list:
        convert_file_name =   _file_name + "_converted.tif"
        crop_file_name =   _file_name + "_cropped.tif"
        x1 = 139.807069
        y1 = 35.707233 
        x2 = 139.814111
        y2 = 35.714069
        cmd = 'gdalwarp -t_srs EPSG:4326 ' +_file_name + ' ' + convert_file_name
        process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
        print("[Done] ", convert_file_name)
        cmd = 'gdal_translate -projwin ' + str(x1) + ' ' + str(y1) + ' ' +  str(x2) + ' ' + str(y2) + ' ' + convert_file_name + " " + crop_file_name
        print(cmd)
        process = (subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]).decode('utf-8')
        print("[Done] ", crop_file_name)
        
if __name__=="__main__":
       main()
