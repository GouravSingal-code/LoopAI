import sys
sys.path.append('../../app')
sys.path.append('../../utils')


from models.dataset import Dataset
from dao.dataset_dao import insert_dataset
from list_generator_utils import randomListGenerator, zeroListGenerator


def createInputFormat(dataset):
   input = []
   output = []
   for id in dataset:
      storeData = dataset[id]
      for date in storeData:
         data = storeData[date]
         previous = randomListGenerator(1440)
         current = [0]
         for index , row in enumerate(data):
            input1 = current + zeroListGenerator(1440-len(current))
            input2 = [previous[index]]
            input.append(input1 + input2)
            output.append([row[3]])
            current.append(row[3])
         current.pop(0)
         previous = current
   return input , output   