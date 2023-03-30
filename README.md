# Bài tập lớn

## Tóm tắt đề

- [x] Make game data Spot the difference
- [x] Make game Spot the difference
- [x] Thống kê thuật toán thực hiện những vấn đề trên

## Make game data

>Tạo ra data cho game Spot the difference

Gồm 3 level 
- Lv1: Thay đổi màu sắc của object **to** trong hình
- Lv2: Thay đổi màu sắc của object **vừa** trong hình và số lượng tăng lên
- Lv3: Thay đổi màu sắc của object **bé** trong hình và số lượng tăng lên

1. Tiền xử lý  
	`cv2.cvtColor()` (chuyển đổi một hình ảnh từ không gian màu này sang không gian màu khác)
	- Thực hiện `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` để chuyển bức ảnh sang Gray => tiến hành xử lý.

2. Phát hiện cạnh  
	- Thực hiện hàm `cv2.Canny(imgray)`, thuật toán phát hiện cạnh Canny.
	- Tiếp tục tiến hành chuẩn hóa detect cạnh bằng phương pháp làm mịn ảnh sử dụng hàm:
		- `cv2.dilate()` (giãn nở) 
		- `cv2.erode()` (xói mòn)
	- Ta sẽ thu được bức ảnh chứa các cạnh của vật thể nhưng có một điều xảy ra có những ảnh quá bé, không rõ và không được liền nét. Để khắc phục điều đó ta sử dụng phương pháp _Biến đổi hình thái xói mòn và giãn nở_ bằng hàm `cv2.morphologyEx(cv2.MORPH_OPEN)` (Open = Erode next Dilate) `cv2.morphologyEx(cv2.ORPH_CLOSE)` (Close = Dilate next Erode)

3. Lập danh sách thông tin về cạnh  
	- Vị trí điểm ảnh của cạnh trên ảnh thông qua `cv2.findContours()` (trích xuất các đường viền từ hình ảnh)
	- Diện tích bao phủ của cạnh (diện tích bao lồi cạnh bao phủ) sử dụng hàm `cv2.contourArea()`

4. Xây dựng thông số của các cấp độ  
	_Như trên_

5. Thay đổi màu sắc những vùng vật thể ngẫu nhiên  
	Lựa chọn ngẫu nhiên những vùng vật thể có diện tích phù hợp với Level đặt ra. Chọn ngẫu nhiên màu sắc tùy ý để thay đổi. 
	- Sử dụng `np.random()` hỗ trợ việc chọn lựa ngẫu nhiên. 
	- Để tô màu vùng được cạnh bao quanh ta sử dụng `cv2.fillPoly()`.
6. Hoàn thành  
	Trích xuất data của bức ảnh cũ và bức ảnh mới.

## Make game Spot the difference

>Tạo hệ thống trò chơi cho game Spot the difference, khoanh vào những vị trí khác nhau trên bức ảnh

1.  Tiền xử lý  
	Thay đổi kích thước hình ảnh thành kích thước dễ quản lý hơn.
2.  Tìm sự khác biệt giữa 2 hình ảnh  
	Sử dụng hàm `cv2.absdiff()` từ OpenCV để tìm sự khác biệt giữa 2 hình ảnh. Hàm này chỉ đơn giản là tính toán sự khác biệt tuyệt đối trên mỗi phần tử giữa hai mảng. Sự khác biệt được trả về trong đối số thứ ba.
3.  Chuyển đổi hình ảnh sang thang độ xám  
	Tiếp tục sử dụng hàm `cv2.cvtColor(cv2.COLOR_BGR2GRAY)` chuyển đổi hình ảnh thành thang độ xám, điều này làm cho việc áp dụng các thao tác khác nhau trên hình ảnh thực sự dễ dàng
4.  Tăng kích thước của sự khác biệt (làm giãn hình ảnh)  
	Áp dụng thao tác hình thái (giãn nở) `cv.dilate()` trên hình ảnh để hợp nhất các pixel, ta không quan tâm lắm đến sự khác biệt chính xác nhưng ta rất quan tâm đến vùng khác biệt trong hình ảnh. 
5.  Ngưỡng hình ảnh (Binarize hình ảnh)  
	Sử dụng thang độ xám `cv2.threshold(cv2.THRESH_BINARY)` để cho ra cụ thể những vùng khác biệt trong ảnh.
6.  Tìm đường viền cho các điểm khác biệt  
	Sử dụng `cv2.findContours()` để tìm tất cả các đường viền. Lặp qua tất cả  các đường viền tìm thấy trên hình, dùng `cv2.boundingRect(contour)` để tìm tọa độ cho các hộp giới hạn hình chữ nhật của điểm thay đổi. Sử dụng `cv2.rectangle()` để tạo ra hình chữ nhật khoanh vào các điểm khác biệt trên ảnh.
7.  Hoàn thành  
	- Hiển thị ra màn hình kết quả cuối dùng bằng `cv2.imshow()` (Cửa sổ tự động phù hợp với kích thước hình ảnh). 
	- Ta có thể kết hợp với việc xây dựng cửa sổ chứa 2 bức ảnh bằng `np.hstack()`.
	
## Running Code Git

Install packages using the below command
```ssh
	pip install -r requirements.txt
```
Build code
```ssh
	python3 main.py --img 'ImageIN/doraemon1.jpg' --level 2 --limit 10
```
