# FEM-SAW-designing-Opitmizing-by-using-Python-to-Feed-sample

Bạn đã quá chán việc mô phỏng FEM cho thiết bị SAW bằng app ANSYS 15.0 rồi đúng không ? Mỗi lần chạy đều rất lâu và quy trình lặp lại đều rất chán. Đừng lo, tôi hiểu và đây là giải pháp tự động chạy mô phỏng. 

Hiện tại, tôi cung cấp mẫu bằng phương pháp LHS ( Latin Hypercube Sampling )

Tôi tổ chức chương trình tổ chức thành 2 file : 
|-run_auto.py
|-Saw_main.txt (đây thường là file session hoặc là code bạn thường dùng để lặp lại quy trình á)

Chương trình này hiện có sẵn 200 mẫu, với code cho (đế : ST-QUARTZ, Điện cực IDT : Nhôm và lớp nhạy FeNi ).

Nếu máy bạn đủ 8 nhân hoặc muốn nhanh hơn thì trong file run_auto.py, bạn có thể sửa chỗ -np 6 thành số Processor bạn mong muốn chạy ( nhiều khi nó chạy chậm do bạn không biết dùng đấy ).
Nhưng tôi khuyến khích 6 processor là đủ dùng rồi, trung bình 1 case chạy sẽ mất khoảng 15-20 phút. Tùy trường hợp. Nếu bạn chạy hết chỗ này cũng sẽ mất tầm hơn 3 ngày, có lẽ vậy... 


Có thể bạn sẽ phải chỉnh lại một vài chỗ như phần vật liệu ma trận, lớp nhạy và địa chỉ file ansys150.exe nằm ở đâu. 

Chuột phải để mở thư mục đang đứng bằng terminal, sau đó gõ lệnh "python ./run_auto.py"

Product by HetoLogy
