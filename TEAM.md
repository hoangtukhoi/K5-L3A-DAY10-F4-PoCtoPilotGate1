# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `F4`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-F4-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |      Vũ Lê Hoàng    |   2A202603542   |   Kĩ sư cổng A  |     x        |
|   2 |     Dương Thanh Bình      |   2A202603531   |   Kĩ sư cổng B  |             |
|   3 |      Lê Quang Linh     | 2A202603583     |  Sản phẩm và kinh doanh   |             |
|   4 |     Nguyễn Đức Minh      |  2A202603563    |  Vận hành và pháp lý  |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## DuongThanhBinh-2A202603531

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng B (`N2` — trace, behavioral test, giám sát `monitors.py` và phân tích lỗi/fault tree).
- **Câu của đề & mục phiếu:**
  - **Phiếu A (`templates/form-a-criteria.md`):** Mục A2 (Câu 1.3 — thiết kế Offline metric cho bước `file_carrier_fault` và Câu 1.4 — Telemetry production), Mục A3 (Câu 1.5 — đọc khoảng tin cậy 95%).
  - **Phiếu B (`templates/form-b-evaluation-gates.md`):** Mục B2 (Câu 2.2 — dò trace `T-002@55` và điền bảng soát lỗi 3 phần), Mục B6 (Câu 2.5 — đóng góp Pre-mortem 4 lăng kính), Mục B7.3 (Câu 2.8 — thiết kế Behavioral test và chạy 2 ticket hiểm bằng `trace --adhoc`), kiểm tra `unittest` chống regression.
  - **Phiếu C (`templates/form-c-incident.md`) & Code:** Viết 4 hàm chỉ số theo dõi mới trong `lab10/monitors.py` (`model_override_rate`, `abnormal_risk_rate`, `avg_cost_vnd`, `max_queue_wait_min`); điền Mục C1 (Câu 3.0), Mục C2 (Câu 3.1 — bảng soát lỗi của thẻ), Mục C5 (Câu 3.2, 3.3 — Specification & giả định môi trường), Mục C6 (Câu 3.4 — Fault tree trước khi sửa), Mục C7 (Câu 3.5 — bảng sửa), Mục C8 (Câu 3.6 — thiết kế chỉ số theo dõi mới), Mục C9 (Câu 3.7 — Fault tree sau khi sửa).

### Đóng góp cụ thể

- Đưa `docs/PRD_v1.1.md` và `docs/eval_card.md` từ Lab 9 vào làm chuẩn đối chiếu cho nhóm; thiết kế thước đo offline cấp bước cho `file_carrier_fault` và telemetry giám sát thiệt hại bên thứ ba trên production.
- Dò `python -m lab10.trace --suite base --ticket T-002 --seed 55`, chỉ ra bước sai đầu tiên tại `03 model_override {"field": "delay_days", "db": 2, "ticket": 5}` gây hoàn sai 20.000đ và phạt oan hãng `VNX` (lỗi chìm).
- Xây dựng tính chất bất biến nguồn sự thật (Source-of-Truth Invariance) và kiểm thử 2 ticket hiểm bằng `--adhoc` trên đơn `O-1002` (khai khống trễ 9 ngày) và `O-1004` (prompt injection ép hoàn 100% đơn từ `MERCHANT`).
- Lập trình các hàm giám sát runtime không nhãn trong `lab10/monitors.py` (`model_override_rate`, `abnormal_risk_rate`, `avg_cost_vnd`, `max_queue_wait_min`) và xây dựng Fault tree trước/sau khi sửa (biến nhánh `HOẶC` thành `VÀ [gate ... hỏng]`).
- Sử dụng trợ lý AI để hỗ trợ rà soát cấu trúc bảng markdown và kiểm tra tính nhất quán của công thức thước đo.

### Bằng chứng

- File code: `lab10/monitors.py` (`model_override_rate = 0.045455`, `abnormal_risk_rate = 0.136364`, `avg_cost_vnd = 566.272727` trên bộ nền `base`), `tests/test_public.py` (`Ran 13 tests … OK`).
- Dòng trong phiếu: `templates/form-a-criteria.md` (Mục A2, A3), `templates/form-b-evaluation-gates.md` (Mục B2, B6, B7.3), `templates/form-c-incident.md` (Mục C1, C2, C5, C6, C7, C8, C9).

### Exit ticket

- **Một điều học được:** Một cổng bằng code (`write_gate` đối chiếu nguồn sự thật DB) có thể **ngăn hẳn** hành vi model bịa số hoặc nghe theo prompt injection, nhưng các rủi ro về vận hành/con người (như nghẽn hàng chờ giờ cao điểm hay nhân viên mất lòng tin phải recheck 100%) và kinh doanh (chi phí mỗi ticket theo kho) bắt buộc phải giải quyết bằng cấu hình hệ thống (`operating_gates.json`), quy trình Runbook và quyết định phạm vi pilot khớp bằng chứng.
- **Một điều còn chưa chắc:** Khi triển khai thật trên production không có nhãn đúng/sai, nếu chính dữ liệu nguồn sự thật trong tracking DB (`delivered_date` hoặc `delay_cause`) bị nhân viên bưu cục nhập sai hoặc cập nhật trễ theo batch thì cả `write_gate` lẫn `monitors.py` đều bị mù — cần cơ chế đối soát chéo định kỳ nào với biên bản của hãng vận chuyển trước Gate 2 để phát hiện sớm độ lệch này.

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
