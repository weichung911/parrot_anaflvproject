import qrcode
# 實例化二維碼生成類
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
# 設置二維碼數據
data = "right"
qr.add_data(data=data)

# 啟用二維碼顏色設置
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

# 顯示二維碼
img.show()
