import qrcode
import os

url = input("please enter url : ")
clean_name = input("Enter file name (without .png) : ")

save_dir = os.path.join(os.path.expanduser("~"), "Downloads", "qrcode")
os.makedirs(save_dir, exist_ok=True)

file_path = os.path.join(save_dir, f"{clean_name}.png")

qr = qrcode.QRCode()
qr.add_data(url)
img = qr.make_image()
img.save(file_path)
print(f"تم الحفظ في: {file_path}")
