import json
import pyperclip


def convertData(data):
    data = json.loads(data)
    convertedData = []
    for i in data:
        v = []
        v.append(i["Control Points"])
        v.append(i["Number of Segments"])
        convertedData.append(v)
    return json.dumps(convertedData)

pyperclip.copy(convertData(pyperclip.paste().strip()))
print("Data has been copied to clipboard")