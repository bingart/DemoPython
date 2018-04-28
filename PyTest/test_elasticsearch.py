# coding=utf-8
import json
import openpyxl
 
def generate():
    with open('D:/curl_7_46_0_openssl_nghttp2_x64/posts.import.json', 'w', encoding='utf8') as file:
        for index in range(200, 300, 1):
            indexDoc = {
                "index": {
                        "_id": str(index)
                    }
                }
            indexStr = json.dumps(indexDoc) + "\n"
            
            postDoc = {
                "blogId": str(index),
                "author": "author " + str(index),
                "title": "lantus insulin " + str(index),
                "excerpt": "this post provide the lantus insulin",
                "content": "the content of lantus insulin",
                "url": "http://localhost:8000/pointclickcares/?p=23",
                "updatedTime" : "2017-11-23T03:45:50Z",
                "categories" : "[\"Health\",\"Insurance\"]",
                "tags" : "[]" 
            }
            postStr = json.dumps(postDoc) + "\n"
            
            file.write(indexStr)
            file.write(postStr)

def generateFromExcel():
    wb = openpyxl.load_workbook('D:/搜索建议词.xlsx')
    sheet= wb.get_sheet_by_name('Sheet1')
    with open('D:/curl_7_46_0_openssl_nghttp2_x64/autocomplete_sheet.json', 'w', encoding='utf8') as file:
        for index in range(2, 1000, 1):
            indexDoc = {
                "index": {
                    "_id": str(index - 1)
                }
            }
            indexStr = json.dumps(indexDoc) + "\n"
    
            e = sheet['C' + str(index)]
            if not e.value:
                break
            
            postDoc = {
                "title": e.value,
            }
            postStr = json.dumps(postDoc) + "\n"

            file.write(indexStr)
            file.write(postStr)

def generateDelete():
    with open('D:/curl_7_46_0_openssl_nghttp2_x64/delete_all_autocomplete.sh', 'w', encoding='utf8') as file:
        for index in range(2, 189, 1):
            line = "curl -XDELETE http://172.16.40.150:9201/autocomplete_health/autocomplete/" + str(index) + "?pretty"
            file.write(line)
            file.write("\n")
    
if __name__=="__main__":
    #generate()
    generateFromExcel()
    #generateDelete()