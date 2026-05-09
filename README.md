# FEM-SAW-designing-Opitmizing-by-using-Python-to-Feed-sample
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Please Install Require Components: pip install pandas numpy scikit-learn xgboost scipy matplotlib seaborn
Hiện tại, tôi cung cấp mẫu bằng phương pháp LHS ( Latin Hypercube Sampling )

Tôi tổ chức chương trình tổ chức thành 2 file : 

|-run_saw_auto.py

|-SAW_main.txt (đây thường là file session hoặc là code bạn thường dùng để lặp lại quy trình á)

Chương trình này hiện có sẵn 200 mẫu, với code cho (đế : ST-QUARTZ, Điện cực IDT : Nhôm và lớp nhạy FeNi ).

Có thể bạn sẽ phải chỉnh lại một vài chỗ như phần vật liệu ma trận, lớp nhạy và địa chỉ file ansys150.exe nằm ở đâu. 

Chuột phải để mở thư mục đang đứng bằng terminal, sau đó gõ lệnh "python ./run_saw_auto.py"


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
You’re probably tired of simulating FEM for SAW devices with ANSYS 15.0, right? Every run takes a long time and the repeated process is very boring. Don’t worry, I understand, and here is an automated simulation solution.

Currently, I provide samples using the LHS (Latin Hypercube Sampling) method.

I organize the program into 2 files:

|-run_saw_auto.py 

|-SAW_main.txt (this is usually the session file or the code you normally use to repeat the process).

This program currently has 200 samples, with code for (substrate: ST-QUARTZ, IDT electrode: Aluminum, and sensitive layer FeNi).

You may need to adjust a few things such as the matrix material section, the sensitive layer, and the location of the ansys150.exe file.

Right-click to open the current folder in the terminal, then type the command "python ./run_saw_auto.py"

Vous en avez probablement assez de simuler par éléments finis (FEM) des dispositifs SAW avec ANSYS 15.0, n'est-ce pas ? Chaque simulation est longue et la répétition du processus est fastidieuse. Rassurez-vous, je comprends, et voici une solution de simulation automatisée.

Je fournis actuellement des exemples utilisant la méthode LHS (échantillonnage hypercube latin).

Le programme est organisé en deux fichiers :

|-run_saw_auto.py

|-SAW_main.txt (il s'agit généralement du fichier de session ou du code que vous utilisez habituellement pour répéter le processus).

Ce programme contient actuellement 200 exemples, avec le code correspondant au substrat (ST-QUARTZ), à l'électrode IDT (aluminium) et à la couche sensible (FeNi).

Il vous faudra peut-être ajuster certains paramètres, comme la section relative au matériau de la matrice, la couche sensible et l'emplacement du fichier ansys150.exe.

Faites un clic droit pour ouvrir le dossier actuel dans le terminal, puis saisissez la commande « python ./run_saw_auto.py ».

Product by HetoLogy
