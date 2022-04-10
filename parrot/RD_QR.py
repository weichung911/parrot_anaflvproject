import cv2
import pyzbar.pyzbar as pyzbar
import numpy
from PIL import Image, ImageDraw, ImageFont

def decodeDisplay(imagex1):
     # 轉為灰度影象
     gray = cv2.cvtColor(imagex1, cv2.COLOR_BGR2GRAY)
     barcodes = pyzbar.decode(gray)

     for barcode in barcodes:

         # 提取條形碼的邊界框的位置
         # 畫出影象中條形碼的邊界框
         (x, y, w, h) = barcode.rect
         cv2.rectangle(imagex1, (x, y), (x + w, y + h), (0, 255, 0), 2)

         # 條形碼資料為位元組物件，所以如果我們想在輸出影象上
         # 畫出來，就需要先將它轉換成字串
         barcodeData = barcode.data.decode("utf-8")
         barcodeType = barcode.type

         #不能顯示中文
         # 繪出影象上條形碼的資料和條形碼型別
         #text = "{} ({})".format(barcodeData, barcodeType)
         #cv2.putText(imagex1, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,5, (0, 0, 125), 2)


         #更換為：
         img_PIL = Image.fromarray(cv2.cvtColor(imagex1, cv2.COLOR_BGR2RGB))

         # 引數（字型，預設大小）
         font = ImageFont.truetype('arial.ttf', 35, encoding="unic")
         # 字型顏色（rgb)
         fillColor = (0,255,255)
         # 文字輸出位置
         position = (x, y-10)
         # 輸出內容
         str = barcodeData

         # 需要先把輸出的中文字元轉換成Unicode編碼形式(  str.decode("utf-8)   )


         draw = ImageDraw.Draw(img_PIL)
         draw.text(position, str, font=font, fill=fillColor)
         # 使用PIL中的save方法儲存圖片到本地
         # img_PIL.save('02.jpg', 'jpeg')

         # 轉換回OpenCV格式
         imagex1 = cv2.cvtColor(numpy.asarray(img_PIL), cv2.COLOR_RGB2BGR)


         # 向終端列印條形碼資料和條形碼型別
         print("掃描結果==》 類別： {0} 內容： {1}".format(barcodeType, barcodeData))
     cv2.imshow("camera", imagex1)


def detect():
     cv2.namedWindow("camera",cv2.WINDOW_NORMAL)
     camera = cv2.VideoCapture(0)

     while True:
         # 讀取當前幀
         ret, frame = camera.read()
         #print(ret.shape)
         decodeDisplay(frame)

         if(cv2.waitKey(5)==27):
             break
     camera.release()
     cv2.destroyAllWindows()


if __name__ == '__main__':
     detect()