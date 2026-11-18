# Phân công 4 người · LAB 10 (theo thời gian)

**Vai**
- **N1:** Trưởng nhóm và Kỹ sư cổng A (viết cổng)
- **N2:** Kỹ sư cổng B (trace, test, monitor)
- **N3:** Sản phẩm và kinh doanh
- **N4:** Vận hành và pháp lý

> Chỉ N1 push để tránh xung đột. Người khác gửi nội dung cho N1, hoặc `git pull` trước khi push.
> Chưa ai chạy `eval` trước khi ký tiêu chí.

## Phút 0–15 · Cài đặt và chia vai

| Người | Việc |
|---|---|
| N1 | Tạo repo Private từ template, mời team chấm, clone, thêm `upstream`, đặt `user.name` và `user.email`. Chạy `unittest`, xác nhận `Ran 13 tests … OK`. |
| N2 | Clone repo, đọc `problem-set.md` và `docs/guide.md`. Chọn eval card và PRD v1.1 từ Lab 9 cùng N3. |
| N3 | Đọc câu 1.1–1.6 trong `problem-set.md` và `config/acceptance_criteria.example.json`. |
| N4 | Điền bảng thành viên trong `TEAM.md`. Đọc `data/world.json` (`ops_limits`, `ops_facts`). |

## Phút 15–65 · Khối 1: tiêu chí, rồi ký (Phiếu A)

| Người | Việc |
|---|---|
| N3 | **Chủ trì.** Câu 1.1–1.6. Điền `config/acceptance_criteria.json` (`team`, `signed_by`, ngưỡng `required`, `nice_to_have`, `business_ops`, `stop_condition`, `decision_rule`). |
| N2 | A2 (thước đo, dữ liệu, cách tính) và A3 (khoảng tin cậy) cùng N3. |
| N4 | A4 (câu tiêu chí "Nếu … thì chúng tôi sẽ …", bốn câu soát, hai câu ranh giới đầu ra). Soát ngưỡng chi phí và số người trực. |
| N1 | Soát JSON của N3 (đúng khoá, đúng kiểu). **Phút 60–65:** chạy lệnh ký bên dưới, ghi giờ ký và mã commit vào A5. |

```bash
python -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

## Phút 65–85 · Khối 2A: đo và tìm rủi ro (chưa sửa code)

| Người | Việc |
|---|---|
| N1 | **Câu 2.1.** `eval --suite base --stage base`, rồi `gate`. Ghi mã lần chạy vào B0, điền B1. |
| N2 | **Câu 2.2.** `trace --suite base --ticket T-002 --seed 55`, điền bảng soát lỗi B2. |
| N3 | **Câu 2.3.** Bản đồ dữ liệu và một ví dụ drift (B3). |
| N4 | **Câu 2.4.** HAZOP vòng 1 (B4): ≥ 3 dòng, trong đó ≥ 2 dòng ngoài kỹ thuật. Checklist 9 nhóm (B5), mỗi dòng một PIC có tên. |
| Cả bàn | **Câu 2.5.** Pre-mortem bốn lăng kính (B6), N3 dẫn. Đánh dấu 2–3 lý do sẽ thành cổng. |

## Phút 85–105 · Khối 2B: dựng cổng

| Người | Việc |
|---|---|
| N1 | **Câu 2.6.** Viết 2–3 cổng trong `pre_guard` và `write_gate` của `lab10/guards.py`. **Câu 2.7:** hai bước tránh rò rỉ dữ liệu. |
| N2 | **Câu 2.8.** Một tính chất và hai ticket hiểm chạy bằng `trace --adhoc`. Chạy `unittest` mỗi khi N1 sửa xong, kiểm tra không có ca mới hỏng. |
| N3 | **Câu 2.9.** Điền mục `business` trong `config/operating_gates.json` (`daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `pilot_scope`, `roi_min`), mỗi số một câu lý do. |
| N4 | **Câu 2.10.** Điền `operations` (`pic`, `approver_id`, `reviewers_on_shift`, `review_capacity_per_hour`, `max_queue_wait_minutes`, `stop_conditions`, `alert_channel`) và `legal`. Viết runbook phần 1–3 và mục Giờ cao điểm. |

**Xong khi:** `eval --stage after` không có ca mới hỏng, `unittest` báo `OK`, `operations.pic` không còn trống.

## Phút 105–115 · Chốt vòng 1 và quyết định v1 (B8)

| Người | Việc |
|---|---|
| N1 | Chạy lần lượt `checkpoint`, `eval --suite base --stage prepared`, `gate`. Commit và push theo lệnh cuối B8. |
| N3 | **Chủ trì** cột v1 ở B8 (một quyết định, ba bằng chứng có mã lần chạy, dòng `decision_rule`, kho hoặc hãng xấu nhất, ngày quyết định lại). |
| N2, N4 | Soát bằng chứng và mã lần chạy trong B8. |

```bash
python -m lab10.checkpoint
python -m lab10.eval --suite base --stage prepared
python -m lab10.gate --run runs/<mã lần chạy>/report.json
```

## Phút 115–125 · Nghỉ

## Phút 125–135 · Nhận thẻ (câu 3.0)

| Người | Việc |
|---|---|
| N1 | Chờ Lab Coach, chạy 2 lệnh bên dưới. Điền C0 (mã prepared). |
| N3 | Bốc thẻ Sx, ghi số vào dòng `Thẻ đã bốc:` ở đầu Phiếu C. |
| N2 | Cùng cả bàn điền C1 (cổng vòng 1 đỡ được gì, đối chiếu pre-mortem). |

```bash
git pull --no-rebase --no-edit --allow-unrelated-histories -X ours upstream main
python -m lab10.grade --incident Sx
```

## Phút 135–155 · Phân tích (câu 3.1–3.4)

| Người | Việc |
|---|---|
| N2 | `trace --suite Sx --ticket Sx-01 --seed 11` và thêm ≥ 1 ticket hỏng kiểu khác. Điền **C2** (bảng soát lỗi), **C5** (specification, giả định môi trường), **C6** (fault tree trước khi sửa). |
| N1 | **C3** (phần riêng theo thẻ). Xác định nguyên nhân kỹ thuật cần sửa. |
| N4 | **C4:** HAZOP của thẻ, ≥ 3 dòng, không ghi đè HAZOP vòng 1. |
| N3 | Đánh giá tác động về tiền và phạm vi, chuẩn bị nháp quyết định v2. |

## Phút 155–185 · Sửa đúng chỗ (câu 3.5–3.7)

| Người | Việc |
|---|---|
| N1 | Sửa `lab10/guards.py` cho nguyên nhân kỹ thuật. Chạy `eval --suite Sx --stage after` (đổi **một** thứ mỗi lần), `eval --suite base --stage after`, rồi `grade --incident Sx`. |
| N2 | **C8:** viết hàm monitor mới trong `lab10/monitors.py`, đăng ký vào `MONITORS`. Điền **C9** (fault tree sau khi sửa). Kiểm tra `monitor ✅` và `regression ✅`. |
| N3 | Nếu nguyên nhân về tiền hoặc phạm vi, sửa `business.pilot_scope`. Điền **C10** (≥ 1 dòng risk register). |
| N4 | Nếu nguyên nhân về người, sửa `reviewers_on_shift`, `review_sampling_pct`, `decision_note`, `legal.*`. Điền **C11** (cập nhật checklist, runbook phần 4–5). |
| Cả bàn | **C7:** bảng sửa (giảm hay ngăn). |

```bash
python -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."
python -m lab10.eval --suite base --stage after --note "kiểm lại bộ nền sau khi sửa"
python -m lab10.grade --incident Sx
```

## Phút 185–200 · Quyết định v2 và gom bài

| Người | Việc |
|---|---|
| N3 | **C12:** cột v2, mục "Chỉ ở v2" và ba dòng bắt buộc. |
| N4 | Điền `submission/submission.json` (`team` giống tiêu chí đã ký, `members` dạng `HoVaTen-MSSV`, `incident`, `decision_v1`, `decision_v2`, `three_lines` chép từ C12). |
| N1 | Chạy `python -m lab10.check_submission --collect`, sửa các dòng `[THIẾU]` đến khi `ĐỦ THÀNH PHẦN`. Commit và push. |
| N2 | Soát số liệu và mã lần chạy trong C12 khớp với report. |

## Phút 200–240 · Demo, phản biện, nộp

| Người | Việc |
|---|---|
| N3 + N1 | Demo ba mốc `base · prepared · after`: cổng vòng 1 đỡ được gì, phần sửa v2 là code, con số hay người. |
| N2 | Chuẩn bị ticket hiểm để phản biện bàn kia. |
| N4 | Ghi lại phản biện nhận được. |
| N1 | Sau demo, trả mọi con số đã đổi thử về bản v2, chạy lại `grade` và `check_submission`, đẩy bài lần cuối. |
| Cả 4 | Mỗi người viết mục cá nhân (`## HoVaTen-MSSV`) trong `TEAM.md` và tự nộp link repo trên LMS. |

```bash
git add -u
git add submission templates TEAM.md
git commit -m "LAB 10: bài nộp"
git push -u origin main
```
