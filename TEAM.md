# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `F4`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-F4-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S2`

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

## VuLeHoang-2A202603542

### Phần việc phụ trách

- **Vai trong bàn:** Trưởng nhóm và Kỹ sư cổng A (`N1`): dựng repo và Git, ký tiêu chí, chạy các lệnh đo, viết cổng trong `lab10/guards.py`, chốt cổng vòng 1, làm thẻ S2 ở vòng 2, gom bài nộp.
- **Câu của đề và mục phiếu:**
  - **Phiếu A:** mục A5 (ký và đẩy tiêu chí), soát lại `config/acceptance_criteria.json` trước khi ký.
  - **Phiếu B:** B0 và B1 (câu 2.1, lần chạy baseline), B7.1 (câu 2.6, ba cổng trong `guards.py`), B7.2 (câu 2.7), B8 (chốt cổng vòng 1 và quyết định v1).
  - **Phiếu C:** C0 (nhật ký lần chạy), C3.1 (mức kiểm soát của con người, thẻ S2), C4 (HAZOP của thẻ), C7 (bảng sửa), C12 (quyết định v2 và ba dòng bắt buộc).
  - **Code và config:** `lab10/guards.py` (`pre_guard`, `write_gate`), `lab10/monitors.py` (hai chỉ số `merchant_debit_rate` và `max_customer_auto_refund_vnd`), `config/operating_gates.json` (`business.pilot_scope`), `submission/submission.json`.

### Đóng góp cụ thể

- Vòng 1: chạy baseline (`R-base-before-20261118-154353-bde05c`), thấy hoàn oan 20.000đ và 1 lỗi hãng oan do ca `T-002@55`. Viết ba cổng: `write_gate` cho `issue_refund` (đối chiếu quyền lợi tính từ tracking DB và chính sách hiệu lực), `write_gate` cho `file_carrier_fault` (chỉ ghi khi DB xác nhận hãng có lỗi, ghi đúng kiện trễ nhất), và `pre_guard` ghim phiên bản chính sách theo ngày. Chốt cổng bằng `lab10.checkpoint` (`e1770907`) và viết quyết định v1 là Tiếp tục trong phạm vi HN và HCM.
- Vòng 2 (thẻ S2, shop bị trừ tiền): dò trace `S2-01@11`, `S2-20@11`, `S2-04@11`, `S2-43@11` và tìm ra bốn nguyên nhân khác nhau: ghi chú giả danh lệnh trong ticket, ghi chú gài ở `checkout_note`, directive làm agent bỏ qua phê duyệt, và không có trần hoàn theo khách mỗi ngày. Sửa trong `write_gate`: ép người chi về LogiX và số tiền về quyền lợi theo DB, khoản trên hạn mức chỉ chạy khi có phê duyệt thật (còn hạn, đúng đơn, đủ hạn mức), và thêm trần 300.000đ mỗi khách mỗi ngày.
- Thấy cổng vòng 1 chuyển 80% ca sang người duyệt nên chi phí vượt làm tay. Mỗi lần chỉ đổi một thứ: sửa cổng trước, rồi mở `pilot_scope` thêm kho DN và CT, rồi thêm monitor. Kết quả mốc after: chi phí 7.273đ, ROI 0,37, độ phủ 1,0, hoàn sai 0đ.
- Gom bài nộp bằng `lab10.check_submission --collect` đến khi báo `ĐỦ THÀNH PHẦN`, và push lên `main`.


### Bằng chứng

- Commit: `62960af` (chốt cổng vòng 1, quyết định v1), `27a5f20` (thẻ S2, sửa vòng 2, quyết định v2), `1ac0b0d` (phiếu A, B, C và bài nộp); commit ký tiêu chí là `8cd9ce5`.
- Mã lần chạy: base `R-base-before-20261118-154353-bde05c`; prepared `R-base-prepared-20261118-163339-e10dfb`; thẻ S2 base `R-S2-before-20261118-164740-510194`, prepared `R-S2-prepared-20261118-164740-510194`, after `R-S2-after-20261118-164740-510194`; grade `R-S2-grade-20261118-164740-510194`.
- Dòng trong phiếu: B0, B1, B7.1, B7.2, B8 (`templates/form-b-evaluation-gates.md`); C0, C3.1, C4, C7, C12 (`templates/form-c-incident.md`).

### Exit ticket

- **Một điều học được:** Cổng bằng code lấy giá trị từ nguồn sự thật (tracking DB, chính sách) rồi sửa lệnh ghi về đúng giá trị hiệu quả hơn là chặn và chuyển người. Cổng vòng 1 chặn hết tiền sai nhưng đẩy 80% ca sang người duyệt, làm chi phí vượt làm tay. Khi chuyển sang sửa `payer` và số tiền, chi phí mỗi ticket giảm từ 20.645đ xuống 7.273đ mà tiền sai vẫn bằng 0.
- **Một điều còn chưa chắc:** Cổng chỉ đúng khi tracking DB đúng, và cổng đang coi LogiX luôn là bên chi trả. Nếu hợp đồng thật với một số shop quy định shop chịu phí, hoặc điểm phát nhập sai `delay_cause`, cổng này sẽ hoàn sai người chi mà không báo. Bộ kiểm tra ẩn và chính sách `REFUND-v4` (hiệu lực 2026-12-01) cũng chưa được thử.

## NguyenDucMinh-2A202603563

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và pháp lý (`N4`).
- **Câu của đề và mục phiếu:**
  - **Phiếu A:** soát phần con người và vận hành (A1 câu 1.2, A2 câu 1.4, A4 ranh giới đầu ra và ngưỡng số người trực, chi phí).
  - **Phiếu B:** B4 (câu 2.4, HAZOP vòng 1 trên `file_carrier_fault`), B5 (checklist 9 nhóm việc, mỗi dòng một PIC có tên), B7.5 (câu 2.10, Runbook 1–3), B7.6 (Giờ cao điểm).
  - **Config:** `config/operating_gates.json` mục `operations` và `legal`.
  - **Vòng 2 (thẻ S2):** được giao C4 (HAZOP của thẻ) và C11 (checklist, Runbook 4–5).

### Đóng góp cụ thể

- Soát Phiếu A theo góc nhìn vận hành: báo động ở câu 1.4 phải khớp `wrongful_carrier_faults_max = 0` (một khiếu nại phạt oan là đỏ, không phải hai), ghi rõ `cost_per_ticket_vnd_max = 8500` là tổng chi phí mỗi ticket còn trần tiền LLM riêng là 1.500đ, điền ngày xem lại tiêu chí.
- B4: HAZOP trên `file_carrier_fault` với 5 dòng kỹ thuật (`carrier_id` bị lấy từ lời khách, thiếu `delay_cause`, lỗi thứ 3 của một hãng trong ngày, gửi lặp, hãng hoặc LLM không trả lời) và 4 dòng ngoài kỹ thuật (người duyệt, ngân sách, dữ liệu gửi bên thứ ba, phạm vi pilot).
- B5: checklist 9 nhóm việc, gán PIC có tên cho từng dòng, đánh dấu dòng nào Xong và dòng nào còn Chưa kèm bằng chứng cần có.
- Điền `operations` và `legal`: `pic = NV-TUNG`, `approver_id = NV-HANH`, 2 người trực (12 ca mỗi giờ), `max_queue_wait_minutes = 60` bằng SLA, `decision_note = true` và `review_sampling_pct = 10` đúng điều kiện nhân viên đặt trong `data/world.json` mục `staff_behavior`; chặn hai trường `recipient_contact` và `customer_note` ở `notify_carrier` (đúng tên khoá của `payload`), bật `carrier_fault_requires_recorded_cause`. Kiểm bằng `ops.problems()`: không có lỗi.
- Viết Runbook 1–3 và Giờ cao điểm khớp từng con số trong `operating_gates.json` và ngưỡng đã ký (tên người từ `staff`, ngưỡng VÀNG và ĐỎ, 15 phút từ tín hiệu đỏ đến lúc dừng xong, `NV-TUNG` bấm công tắc).
- Có dùng trợ lý AI (Claude) để soạn nháp B4, B5 và Runbook. Tôi đối chiếu từng con số và tên người với `data/world.json`, chọn số người trực và tự đặt tên kênh báo tin, nên giải thích được từng giá trị lúc demo.
- [Điền nếu đã làm: soát C4 và C11 của thẻ S2, ghi phản biện nhận được lúc demo.]

### Bằng chứng

- Commit: `423fe66` (`templates/form-b-evaluation-gates.md`: B4, B5, B7.5, B7.6; `config/operating_gates.json`: `operations`, `legal`).
- Mã lần chạy dùng cổng vòng 1 có `operations` và `legal` ở trên: prepared `R-base-prepared-20261118-163339-e10dfb`; thẻ S2 after `R-S2-after-20261118-164740-510194` (chi phí 7.273đ, trong trần đã ký 8.500đ).
- Dòng trong phiếu: Phiếu A mục A1, A2, A4; Phiếu B mục B4, B5, B7.5, B7.6; Phiếu C mục C4, C11.

### Exit ticket

- **Một điều học được:** Phần lớn cổng về con người và pháp lý không cần code mà cần đúng con số và đúng tên người, và chúng phải khớp ba nơi cùng lúc: `operating_gates.json`, Runbook và ngưỡng đã ký. Cổng pháp lý chặn dữ liệu cá nhân chỉ hoạt động nếu gõ đúng tên khoá của `payload` (`recipient_contact`, `customer_note`), nên phải đọc code `notify_carrier` chứ không đoán.
- **Một điều còn chưa chắc:** Số người trực (2) và ngưỡng VÀNG (30 phút chờ, hàng chờ 6 ca) tôi chọn từ công suất 6 ca mỗi giờ mỗi người mà chưa thử trên lưu lượng thật; kênh `#logix-pilot-alert` cũng là tên tự đặt. Khi lên 12 depot và áp dụng `REFUND-v4` (hạn mức tự động 100.000đ từ 2026-12-01), số người trực này gần như chắc chắn không còn đủ.