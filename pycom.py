class Pycom:
    def __init__(self, root_dir, header_dict, file, extract_path, fname_length):
        self.basepath = root_dir
        self.header = header_dict
        self.file_type = file
        self.extraction_path = extract_path
        self.fname_len = fname_length
    
    def list_dicoms(self, basepath, header, file_type) -> list:
    
        dicom_path = []
        
        try:
            for root, dirs, files in os.walk(basepath):
                for file in files:
                    if any(file_type in file for i in files) == True:
                        for key, value in header.items():
                            if any(value in file for j in files) == True:
                                dicom_path.append(os.path.join(root, file))
        except:
            raise Exception(f'{file} not found')
    
        return self.dicom_path
    
    def tar_extractor(self, basepath, file_type, fname_len):
        for root, dirs, files in os.walk(basepath):
            for file in files:
                if any(file_type in file for i in files) == True:
                    tgz_file = file
                    tgz_path = os.path.join(root,file)
                    len_fname = fname_len
                    len_file_path = len(tgz_path)
                    extract_path = tgz_path[:-len_fname]
                    if any('dicom' not in dirs for i in dirs):
                        try:
                            tar = tarfile.open(tgz_path)
                            tar.extractall(path=extract_path)
                            tar.close()
                            print(f'{file} extracted successfully.')
                        except:
                            print(f'tgz file not found. Ensure {file_type} is the correct file type')
                    else:
                        print(f'dicom folder has already been extracted in {extract_path}')

class ScanCoordinates(Pycom):
    def __init__(self, root_dir, header_dict, file, extract_path, fname_length, input_size, data):
        self.input_size = input_size
        self.image = data
        self.dimensions = (input_size, input_size)
        self.resized_image = cv2.resize(self.image, self.dimensions)
        self.blur_image = cv2.GaussianBlur(self.resized_image, (3,3), 0)
        self.h = self.resized_image.shape[0]
        self.w = self.resized_image.shape[1]
        super().__init__(root_dir, header_dict, file, extract_path, fname_length)
        
    def get_edge_coordinates(self, blur_image, lower_threshold, higher_threshold) -> list:
        # Determine Edges
        edge_image = cv2.Canny(image=blur_image, threshold1=lower_threshold, threshold2=higher_threshold)

        h = edge_image.shape[0]
        w = edge_image.shape[1]
        
        # Initilize empty coordinate list
        coordinates = []
        
        # Iterate through each voxel
        for y in range(0, self.h):
            for x in range(0, self.w):
                intensity = np.sum(edge_image[y,x])
                
                # Store edge voxel coordinate
                if intensity != 0:
                    coordinate = (x, y)
                    coordinates.append(coordinate)
        
        return coordinates

    def get_skull_voxels(self, resized_image, h, w):
            # Initilize empty list of skull voxel coordinates
            self.skull_voxels = []
            self.skull_threshold = 100
            
            # Iterate through each voxel
            for y in range(0, h):
                for x in range(0, w):
                    intensity = np.sum(resized_image[y,x])
                    
                    # Store skull voxel coordinate
                    if intensity > self.skull_threshold:
                        vox_coord = (x, y)
                        self.skull_voxels.append(vox_coord)
            
                size = len(self.skull_voxels)
            
            return size
