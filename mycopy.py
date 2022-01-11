import shutil
import retrain

if __name__ == '__main__':
    retrain.main()

    path1 = './data/result_data.csv'
    path2 = '/home/nodebb2/node_modules/nodebb-widget-adverting-federallearning/result_data.csv'

    shutil.copyfile(path1, path2)

    print("Copy Completed!")
