class DeID:
    def __init__(self, src_dir, id_dir_name):
        self.basepath = src_dir
        self.id_dir = id_dir_name

        def rm_id_dirs(basepath, id_dir):
            try:
                for root, dirs, files in os.walk(basepath):
                    for dir in dirs:
                        if any (id_dir in dir for i in dirs) == True:
                            dir_path = os.path.join(root,dir)
                            shutil.rmtree(dir_path)
                            print('Sensitive folder(s) removed.')
            except:
                raise Exception(f'{id_dir} not found in {dir_path}')
