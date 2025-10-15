# Ứng dụng các thuật toán tìm kiếm trong trí tuệ nhân tạo vào Game 8 Rooks

## Thông tin đồ án
- **Môn học:** Trí tuệ nhân tạo  
- **Giảng viên:** ThS. Phan Thị Huyền Trang  
- **Lớp học phần:** 251ARIN330585_05CLC  

### Thông tin sinh viên:
| Họ và tên        | MSSV      |
|------------------|-----------|
| Ninh Anh Tú      | 23110168  |

---

## 📑 Mục lục
1. [Tổng quan về Game 8 Rooks](#tổng-quan-về-game-8-rooks)  
2. [Các thuật toán được sử dụng](#các-thuật-toán-được-sử-dụng)  
3. [Kết quả và đánh giá](#kết-quả-và-đánh-giá)  
4. [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)  
5. [Hướng phát triển](#hướng-phát-triển)  
6. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## Tổng quan về Game 8 Rooks

### Giới thiệu bài toán
Bài toán **8 Rooks (8 quân xe)** là một biến thể của bài toán cờ vua kinh điển trong trí tuệ nhân tạo.  
**Mục tiêu:** đặt 8 quân xe lên bàn cờ 8×8 sao cho **không có hai quân xe nào tấn công lẫn nhau**.  
Một quân xe có thể di chuyển theo **hàng ngang và hàng dọc**, do đó điều kiện cần và đủ là:
- Không có hai quân xe nào cùng hàng  
- Không có hai quân xe nào cùng cột  

### Quy tắc và luật chơi
- Bàn cờ kích thước **8×8 ô**  
- Đặt **8 quân xe**  
- Mỗi hàng và mỗi cột **chỉ có đúng một quân xe**

---

## Tổng quan về dự án

### Mục tiêu
- Triển khai và so sánh hiệu quả của **19 thuật toán tìm kiếm AI**  
- Xây dựng **giao diện trực quan** minh họa quá trình hoạt động của thuật toán  
- Phân tích hiệu suất dựa trên:
  - Thời gian thực thi  
  - Số nút mở rộng  
  - Chất lượng lời giải  

### Phạm vi
- Bao gồm **19 thuật toán tìm kiếm** thuộc nhiều nhóm  
- Giao diện đồ họa minh họa quá trình đặt quân  
- Hệ thống đánh giá hiệu suất theo thời gian thực  

---

## Các thuật toán được sử dụng

### Nhóm 1: Uninformed Search
| Thuật toán | Nguyên lý | Ưu điểm | Nhược điểm |
|-------------|------------|----------|-------------|
| **BFS** | Duyệt theo chiều rộng, đảm bảo tìm thấy lời giải ngắn nhất | Tìm lời giải tối ưu | Tốn bộ nhớ |
| **DFS** | Duyệt theo chiều sâu đến khi gặp ngõ cụt | Tiết kiệm bộ nhớ | Có thể rơi vào vòng lặp |
| **UCS** | Ưu tiên nút có chi phí thấp nhất | Tối ưu chi phí | Chậm hơn BFS nếu chi phí đồng nhất |
| **DLS** | DFS có giới hạn độ sâu | Tránh vòng lặp vô hạn | Có thể bỏ lỡ lời giải |
| **IDS** | DLS tăng dần độ sâu | Kết hợp BFS & DFS | Duyệt lại các nút ở mức nông |

---

### Nhóm 2: Informed Search
| Thuật toán | Nguyên lý | Ưu điểm | Nhược điểm |
|-------------|------------|----------|-------------|
| **Greedy Best-First** | Chọn nút có h(n) nhỏ nhất | Tốc độ nhanh | Dễ mắc kẹt cực trị địa phương |
| **A\*** | f(n) = g(n) + h(n) | Tối ưu & hoàn chỉnh | Tốn bộ nhớ |

---

### Nhóm 3: Local Search
| Thuật toán | Nguyên lý | Ưu điểm | Nhược điểm |
|-------------|------------|----------|-------------|
| **Hill Climbing** | Luôn chọn trạng thái tốt hơn | Nhanh, đơn giản | Mắc kẹt cực trị địa phương |
| **Simulated Annealing** | Cho phép bước lùi có xác suất | Thoát cực trị địa phương | Phụ thuộc lịch làm nguội |
| **Genetic Algorithm** | Tiến hóa: chọn lọc, lai ghép, đột biến | Tìm lời giải tốt trong không gian lớn | Phụ thuộc tham số |
| **Beam Search** | Giữ k nút tốt nhất mỗi mức | Tiết kiệm bộ nhớ | Có thể bỏ lỡ lời giải tối ưu |

---

### Nhóm 4: Complex Environment
| Thuật toán | Nguyên lý | Ưu điểm | Nhược điểm |
|-------------|------------|----------|-------------|
| **AND-OR Tree** | Lập kế hoạch có điều kiện | Giải được bài toán không chắc chắn | Độ phức tạp cao |
| **Partially Observable** | Môi trường quan sát một phần | Xử lý môi trường không hoàn hảo | Bùng nổ tổ hợp |
| **Belief State** | Tìm kiếm trên tập trạng thái khả dĩ | Giải được bài toán bất định | Chi phí cao |

---

### Nhóm 5: CSP (Constraint Satisfaction Problem)
| Thuật toán | Nguyên lý | Ưu điểm | Nhược điểm |
|-------------|------------|----------|-------------|
| **Backtracking** | Thử và sai, quay lui khi ngõ cụt | Đơn giản, tiết kiệm bộ nhớ | Chậm nếu ràng buộc lỏng |
| **Forward Checking** | Kiểm tra và loại trừ trước | Phát hiện xung đột sớm | Tốn chi phí duy trì miền |
| **AC3** | Duy trì tính nhất quán cung | Giảm miền giá trị hiệu quả | Tính toán cao với miền lớn |

---

### Nhóm 6: Adversarial Search
| Thuật toán | Nguyên lý | Ưu điểm | Nhược điểm |
|-------------|------------|----------|-------------|
| **Minimax** | Tối đa hóa lợi ích, tối thiểu hóa thiệt hại | Tối ưu cho trò chơi đối kháng | Độ phức tạp cao |
| **Alpha-Beta Pruning** | Cắt tỉa nhánh không cần thiết | Giảm đáng kể số nút duyệt | Vẫn chậm với độ sâu lớn |

---

## Kết quả và đánh giá

### 🔹 Nhóm Uninformed
- **BFS:** chính xác, tốn bộ nhớ  
- **DFS:** nhanh, không tối ưu  
- **UCS:** tối ưu chi phí, chậm  
- **IDS:** cân bằng, duyệt lặp lại  

### 🔹 Nhóm Informed
- **Greedy:** nhanh, dễ sai  
- **A\*:** tối ưu, tốn RAM  

### 🔹 Nhóm Local Search
- **Hill Climbing:** nhanh, mắc kẹt  
- **Simulated Annealing:** thoát cực trị  
- **GA:** mạnh, tốn tài nguyên  
- **Beam Search:** hiệu quả vừa phải  

### 🔹 Nhóm Complex Environment
- **AND-OR:** xử lý bất định tốt  
- **POS & Belief:** mạnh nhưng nặng  

### 🔹 Nhóm CSP
- **Backtracking:** dễ hiểu, chậm  
- **Forward Checking & AC3:** giảm không gian, tốn tính toán  

### 🔹 Nhóm Adversarial
- **Minimax & Alpha-Beta:** hiệu quả cho game đối kháng, độ sâu cao làm chậm  

---

## Hướng dẫn sử dụng

### Yêu cầu hệ thống
- **Python:** 3.7+  
- **Thư viện:** `tkinter` (có sẵn)

### Cách chạy
```bash
git clone https://github.com/NinhAnhTu/Game8Rooks.git
cd Game8Rooks
python main.py


Cấu trúc dự án
8RooksAI/
├── main.py             # File khởi chạy chính
├── gui.py              # Giao diện Tkinter
├── algorithms.py       # Chứa 19 thuật toán
└── assets/             # Ảnh quân cờ, icon

---

## 💻 Sử dụng giao diện

1. **Chọn thuật toán** từ các nhóm bên trái *(Uninformed, Informed, Local, CSP, Adversarial, ...)*  
2. **Quan sát bàn cờ trái** để xem tiến trình hoạt động step-by-step (animation).  
3. **Xem bàn cờ phải** để thấy kết quả cuối cùng sau khi thuật toán hoàn tất.  
4. **Theo dõi bảng thông tin** hiển thị thời gian, số bước, số nút mở rộng, giá trị `g(n)`, `h(n)`, `f(n)`, v.v.  

💡 *Mẹo:*  
Bạn có thể **tạm dừng animation**, **tua nhanh**, hoặc **chạy lại** để so sánh hoạt động giữa các thuật toán.

---

## 🚀 Hướng phát triển

- 🔹 **Mở rộng** sang các bài toán khác như *N-Queens*, *Sudoku*, *Knight’s Tour*, ...  
- 🔹 **Bổ sung** thêm các thuật toán tiên tiến như *Monte Carlo Tree Search (MCTS)*, *Q-learning*, *DQN*, ...  
- 🔹 **Cải thiện giao diện người dùng** với hiệu ứng animation mượt hơn và hiển thị trực quan hơn.  
- 🔹 **Tích hợp tính năng so sánh tự động** giữa các thuật toán *(thời gian, hiệu quả, số nút mở rộng)*.  
- 🔹 **Phát triển thành công cụ học tập & giảng dạy AI** trực quan, giúp sinh viên quan sát hoạt động của từng thuật toán.

---

## 📚 Tài liệu tham khảo

- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach (4th ed.)*. Pearson.  
- Pearl, J. (1984). *Heuristics: Intelligent Search Strategies for Computer Problem Solving*. Addison-Wesley.  
- Mitchell, M. (1998). *An Introduction to Genetic Algorithms*. MIT Press.  
- Kumar, V. (1992). *Algorithms for Constraint Satisfaction Problems: A Survey*. *AI Magazine*.  

---

✨ **Dự án thuộc về Nhóm 10 – 8 Rooks AI Project**
