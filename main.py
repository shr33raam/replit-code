from datetime import date
import requests
import datetime
import json
import time

def main():
  class makeDict:
    def Load(Str):
      fileName = Str
      json_file= open(fileName, 'r').read()
      data = json.loads(json_file)
      response={}
      for p in data['apiProduct']:
        for a in p['attributes']:
          if a['name'] == "access" :
            response[p['name']] = a['value']
      responseStr = json.dumps(response,indent=2)
      return response
  '''
  tF = open('token.txt', 'r').read() #Getting the token of the user executing the script for getting the API products from a file
  myUrl = 'https://api.enterprise.apigee.com/v1/organizations/ee-nonprod/apiproducts?expand=true' #RequestURI for getApiProducts
  head = {'Authorization': tF ,'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36','Content-Type': 'application/json'} #Constructing the getApiCall
  print('Fetching the API Products')
  response = requests.get(myUrl, headers=head) #triggering a getter call
  print(str(response) + 'Success')
  response.raise_for_status() # ensure we notice bad responses
  file = open("resp_content.txt", "w").write(response.text)
  '''

  RespContDict = makeDict.Load('resp_content.txt')
  baseJSONDict = makeDict.Load('Base.json')

  removedDict = baseJSONDict.keys() - RespContDict.keys()
  AddedDict = RespContDict.keys() - baseJSONDict.keys()
  print('Please refer added and deleted API products files to know more about the changes')
  open("addedAPIProducts.txt", "w").write(format(str(AddedDict)))
  open("deletedAPIProducts.txt", "w").write(format(str(removedDict)))


  unchangedDict = {k:v for k,v in RespContDict.items() & baseJSONDict.items() }
  diffSet = RespContDict.keys() - unchangedDict.keys()
  diffDict= {}
  for p in diffSet:
    diffDict[p] = RespContDict[p]

  with open("ModifiedAPIProducts.txt", "w") as f:
    for i in diffDict:
      f.write('Access changed in ' + i + ' from '+ baseJSONDict[i] +' to '+ diffDict[i] + '\n')
  print('Completed SuccessFully')

  print('Do you want to replace the Base with today\'s Result(y/n)?? ')
  inp = input()
  if inp == 'y':
    with open("resp_content.txt", "r") as file:
      f = file.read()
    with open("Base.json", "r") as file:
      f1 = file.read()
    open("Base_BKP.json", "w").write(str(f1))
    open("Base.json", "w").write(str(f))
  else:
    print('Good Bye...')
    time.sleep(5)


main()