# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** ______ · **Thẻ đã bốc:** ___ *(để trống tới phút 125; bốc số xong thì ghi đúng số đó, ví dụ `S3`. Lab Coach đối chiếu với sổ; lệnh tự kiểm tra in dòng này trong report.)*

Mở `incidents/Sx/card.md` của đúng số đã bốc. Các bước trên thẻ trỏ về đúng mục trong phiếu này. Mục C3 chỉ điền phần ứng với
số thẻ của bàn; các phần khác để trống.

**Mục lục**
- [C0 · Nhật ký lần chạy vòng 2 (suốt khối)](#c0)
- [C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem · phút 125–135 · bước 0 trên thẻ](#c1)
- [C2 · Câu 3.1 · Bảng soát lỗi của thẻ · phút 135–145 · bước 1–2](#c2)
- [C3 · Câu 3.1 · Phần riêng theo thẻ · phút 135–145 · bước 3](#c3)
- [C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng) · phút 145–150 · bước 4](#c4)
- [C5 · Câu 3.2, 3.3 · Specification và giả định môi trường · phút 145–150 · bước 4](#c5)
- [C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa · phút 150–155 · bước 4](#c6)
- [C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn · phút 155–180 · bước 5–7](#c7)
- [C8 · Câu 3.6 · Chỉ số theo dõi mới · phút 155–180 · bước 5](#c8)
- [C9 · Câu 3.7 · Fault tree SAU khi sửa · phút 180–185 · bước 8](#c9)
- [C10 · Câu 3.7 · Risk register (≥ 1 dòng) · phút 180–185 · bước 8](#c10)
- [C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5 · phút 180–185 (runbook có thể xong trong 185–200) · bước 8](#c11)
- [C12 · Quyết định Gate 1 · v2 và ba dòng bắt buộc · phút 185–200 · bước 9](#c12)

---

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi một dòng vào `runs/journal.jsonl`. Điền cột "Đổi MỘT thứ gì" (tham số `--note`) và "Kết luận".

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | | Sx · prepared | nhận thẻ đã bốc, chưa sửa thêm (đúng cổng vòng 1 đã chốt) | | | | | |
| 2 | | Sx · after | | | | | | |
| 3 | | Sx · after | | | | | | |
| 4 | | base · after | (kiểm không regression) | | | | | |

---

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

Chạy **trước khi sửa bất cứ thứ gì**:

```bash
python3 -m lab10.grade --incident Sx
```

- Mã lần chạy grade: `R-Sx-grade-... (điền ngay khi chạy lệnh 6)` · base: `R-Sx-before-...` · prepared: `R-Sx-prepared-...`
- Cổng vòng 1 đỡ được ô / con số nào (so cột base với cột prepared): Cổng vòng 1 (`guards_round1.py` + `operating_gates.round1.json`) đã chặn trước các thao tác ghi hoàn tiền sai chuẩn `entitlement_vnd` theo tracking DB, chặn ghi lỗi hãng không có `delay_cause` hợp lệ và lọc các trường PII (`recipient_contact`, `customer_note`) gửi cho hãng vận chuyển, giúp giảm thiểu thiệt hại trực tiếp so với mốc `base`.
- Khối kinh doanh và vận hành còn dòng nào vượt trần: Phụ thuộc vào đặc thù thẻ `Sx` ở mốc `prepared` (ví dụ: nếu thẻ gây tăng số ca `escalated` hoặc `recheck` thì vượt trần hàng chờ `stuck > 0` / thời gian chờ `> 60` phút; nếu thẻ có đơn giá trị lớn hoặc ticket dài ở một kho thì vượt trần chi phí mỗi ticket `> 10.000đ` hoặc `ROI < roi_min`).

**Mở lại pre-mortem (Phiếu B mục B6), viết bằng bút khác màu.** Với thẻ S1, S3, S4, S5 đây là một phần của phần riêng theo thẻ.

- Sự cố trên thẻ thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? Kết hợp **Kỹ thuật** (dữ liệu/model/tool) với **Kinh doanh / Con người và vận hành / Pháp lý** (tác động trực tiếp lên ngân sách hoàn tiền, chi phí/ticket, hàng chờ người duyệt hoặc bên thứ ba là hãng vận chuyển, shop, người nhận hàng).
- Có nằm trong các lý do bàn đã viết không? Nếu có: cổng vòng 1 đã đỡ được bao nhiêu (đọc cột prepared trong report)? Nếu không: vì sao cả bàn không nghĩ tới? Nhánh cốt lõi về dữ liệu/lệnh ghi đã nằm trong bảng Pre-mortem B6 nên cổng vòng 1 đã đỡ được phần lớn các ca vi phạm trực tiếp ở cột `prepared`; phần còn lọt (hoặc phát sinh tác dụng phụ làm tăng tải hàng chờ/chi phí) là do ở vòng 1 bàn chưa biết biến động môi trường đặc thù của `world_patch.json` trên thẻ `Sx`.
- Lý do còn thiếu, thêm bây giờ:

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được bằng gì (trace / data / config nào) |
|---|---|---|
| Khi môi trường vận hành thay đổi đột ngột như trong `incidents/Sx/world_patch.json` (dữ liệu trạng thái đơn/chính sách/phê duyệt lệch chuẩn hoặc lưu lượng/độ dài ticket tăng vọt), cổng chỉ chặn ở tầng lệnh ghi (`write_gate`) mà chưa đồng bộ với tầng điều phối vận hành (`operating_gates.json`: số người trực, phạm vi kho pilot, chế độ `decision_note` và kiểm mẫu), dẫn tới nghẽn hàng chờ hoặc đội chi phí. | Con người và vận hành / Kinh doanh | Kiểm được qua `incidents/Sx/world_patch.json`, trace `incidents/Sx/tickets.jsonl` và bảng `Kinh doanh · vận hành · pháp lý` trong report của `lab10.grade --incident Sx`. |

---

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau:

```bash
python3 -m lab10.trace --suite Sx --ticket <ID> --seed 11
```

Ba loại lỗi: **giới hạn của hệ thống** · **lỗi ngữ cảnh** · **lỗi chìm** (cả người dùng lẫn hệ thống đều không nhận ra; nguy hiểm nhất,
người chịu hại thường là bên thứ ba). Định nghĩa đầy đủ và ví dụ: Phiếu B mục B2.

**Tác hại của thẻ:** cho ai `Khách hàng / LogiX (Finance & CSKH) / Bên thứ ba (hãng vận chuyển, tài xế, shop, người nhận hàng)` · đo bằng gì `wrongful_refund_vnd, wrongful_carrier_faults, merchant_debit_vnd, pii_leaks, queue_stuck, cost_per_ticket_vnd` · bao nhiêu ở mốc base `(cập nhật số từ cột base của report grade --incident Sx)`

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | Tại `Sx-01@11` (mốc `base`): trong trace xuất hiện bước xử lý sai lệch giữa dữ liệu đầu vào/trạng thái trong `world_patch.json` và quyết định ở `proposal` / `tool` (`issue_refund` hoặc `file_carrier_fault`), dẫn tới ghi dòng sai vào `SỔ CÁI` hoặc `LỖI HÃNG` trong khi hệ thống vẫn trả về `status: "refunded"` bình thường. | **LogiX (quỹ hoàn tiền), kế toán đối soát (`NV-OANH`) và bên thứ ba (shop `MERCHANT` hoặc hãng vận chuyển / tài xế)** chịu thiệt hại tiền mặt hoặc bị phạt oan mà không hề hay biết. | Cao | **Lỗi chìm** (cả khách hàng lẫn hệ thống đều không báo lỗi lúc chạy; thiệt hại chảy ngầm vào sổ cái hoặc biên bản phạt đối tác) |
| 2 | Tại `Sx-02@11` (hoặc ticket kiểu thứ 2 của bộ `Sx` ở mốc `base`): agent áp dụng giả định cứng trong code (`agent.py`: chọn `index_active`, lấy `parcels[0]`, dùng lại `approval_id` cũ/không khớp, đính kèm `recipient_contact`/`customer_note`, hoặc `fail_open` / `write_retry` khi LLM 429) gây sai kết quả đầu ra so với nhãn `NHÃN`. | **Người nhận hàng (lộ PII), trưởng ca CSKH (`NV-HANH`), nhân viên duyệt hoặc hãng vận chuyển** chịu hậu quả vì hành vi của hệ thống vênh với quy định vận hành và kỳ vọng của con người. | Cao | **Lỗi ngữ cảnh** (hoặc **Lỗi chìm** đối với bên thứ ba không tham gia hội thoại) |
| 3 | Trên toàn bộ gói sự cố `Sx` (cấp độ ca vận hành trong report `grade`): khi các ca khó hoặc ca vượt trần bị đẩy sang người duyệt (`escalated`) hoặc bị nhân viên kiểm lại (`recheck`), hàng chờ `queue` tăng vọt hoặc chi phí LLM + công duyệt mỗi ticket vượt ngưỡng làm tay (`10.000đ/ticket`). | **Đội vận hành CSKH (`NV-HANH`, `NV-TUNG`) và bộ phận Finance** chịu áp lực quá tải hàng chờ (`queue_stuck`) hoặc lỗ ròng (`ROI < 0`). | Cao | **Giới hạn của hệ thống** (giới hạn công suất xử lý 6 ca/giờ/người trực và chi phí token/người duyệt khi lưu lượng hoặc độ phức tạp tăng) |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | **X** (Đặt sai trọng số cho thông tin trong `text` / `checkout_note` hoặc tín hiệu trích xuất của `MockLLM`) | | |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | | **X** (Không đối chiếu đầy đủ các trường điều kiện thực tế như `status`, `effective_from/to`, `parcel_id` thực sự trễ, hoặc tính hợp lệ của `approval`) | |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | **X** (Không phân định rõ nguồn sự thật giữa sổ cái thực tế `ledger`, bảng `orders`/`policies`/`approvals` và đề xuất của model) | **X** (Xung đột quyền hạn giữa quyết định tự động của agent và quyền phê duyệt/đối soát của con người) | |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | | | **X** (Nhiều ca chuyển người / kiểm lại hoặc lỗi 429 liên tiếp cộng dồn trong cùng một ca làm nghẽn hàng chờ `queue_stuck` hoặc làm nổ chi phí/ticket) |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| Vì sao người gặp coi đây là lỗi | Sổ cái ghi nhận khoản hoàn sai quy định hoặc trừ tiền oan của shop/phạt oan hãng vận chuyển, gây lệch đối soát tài chính tuần của chị Oanh (`NV-OANH`). | Hành động của agent vi phạm quy tắc nghiệp vụ/pháp lý (dùng sai chính sách/phê duyệt, phạt nhầm kiện, hoặc làm lộ thông tin cá nhân người nhận sang bên thứ ba). | Thời gian chờ duyệt vượt SLA 60 phút gây ùn tắc ca trực của chị Hạnh (`NV-HANH`), hoặc chi phí vận hành trợ lý đắt hơn làm tay khiến dự án lỗ (`ROI` âm). |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | **Chặn bằng cổng code (`write_gate` / `pre_guard`) đối chiếu nguồn sự thật DB** trước khi cho phép `issue_refund` hoặc `file_carrier_fault` thực thi. | **Chặn/sửa tham số bằng cổng code (`Verdict.modify` / `Verdict.deny` / `Verdict.escalate`) kết hợp cổng pháp lý `legal` trong `operating_gates.json`**. | **Trao quyền kiểm soát & điều chỉnh cấu hình vận hành/kinh doanh (`operating_gates.json`)**: chỉnh `reviewers_on_shift`, `pilot_scope`, `decision_note`, `review_sampling_pct`, `cost_budget_per_ticket_vnd`. |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | Lệnh ghi sai bị `write_gate` chặn (`Verdict.deny`) hoặc sửa về đúng số tiền `entitlement_vnd` (`Verdict.modify`) → sổ cái chỉ ghi đúng số tiền hợp lệ, khách nhận thông báo khớp sổ cái. | Các trường hợp thiếu phê duyệt hợp lệ được đẩy sang hàng chờ người duyệt (`Verdict.escalate`); các trường PII bị cắt bỏ trước khi gửi `notify_carrier`; lỗi hãng chỉ ghi cho đúng kiện trễ có `delay_cause` hợp lệ. | Ticket ngoài phạm vi pilot đi theo luồng làm tay; các ca trong phạm vi có đủ người trực (`reviewers_on_shift`) và có `decision_note: true` (giảm thời gian kiểm lại xuống 0,4 ca = 4 phút) nên được duyệt hết trong < 60 phút. |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | Theo dõi qua chỉ số `model_override_rate` và `abnormal_risk_rate` trong `lab10/monitors.py`. | Theo dõi qua chỉ số `abnormal_risk_rate` (bắt các sự kiện `gate`, `legal_gate`, `approval_used`, `recipient_contact`) trong `lab10/monitors.py`. | Theo dõi qua chỉ số `max_queue_wait_min`, `avg_cost_vnd` và `escalation_rate` trong `lab10/monitors.py`. |

Yêu cầu: ít nhất **hai lỗi có nguồn khác nhau** ở phần 2, và ít nhất một lỗi được xếp đúng là **lỗi chìm**.

---

<a id="c3"></a>

## C3 · Câu 3.1 · Phần riêng theo thẻ (chỉ điền phần của số đã bốc; làm trong khoảng 5 phút)

| Thẻ | Điền phần nào |
|---|---|
| S1 | Mục C1 (đối chiếu pre-mortem) + **C3.5** (mở lại bản đồ dữ liệu: các trường của `parcel`) |
| S2 | **C3.1** Mức kiểm soát của con người |
| S3 | Mục C1 + **C3.5** (bảng `policies`: trường nào là nguồn sự thật về "phiên bản đang hiệu lực"; dòng `delay_cause`) |
| S4 | Mục C1 + mục **Giờ cao điểm** ở Phiếu B mục B7.6 (bổ sung bằng bút khác màu nếu đã viết) |
| S5 | Mục C1 + **C3.5** + mục **C8** dùng cho một con số kinh doanh (chi phí mỗi ticket theo kho) |
| S6 | **C3.2** Hình dung của người và của hệ thống |
| S7 | **C3.3** Hiệu chỉnh lòng tin (người đặt hàng, người nhận hàng) |
| S8 | **C3.4** Hiệu chỉnh lòng tin (nhân viên duyệt, trưởng ca đứng tên) + **một dòng** "hoàn trên hạn mức" ở bảng C3.1 Bước 2 |

### C3.1 · Mức kiểm soát của con người ở từng lệnh ghi (S2; S8 chỉ một dòng)

**Cách làm:** (1) soát các dấu hiệu cho thấy con người **cần giữ nhiều quyền kiểm soát hơn**; (2) lập bảng
*ai · ở việc nào · cần mức kiểm soát nào* (thấp / vừa / cao / chưa rõ), thêm một cột: **hệ thống hiện đang cho mức nào**.
Chỗ hai cột lệch nhau chính là nơi đặt gate.

**Bước 1 · Dấu hiệu cần nhiều quyền kiểm soát hơn (đánh dấu, ghi bằng chứng từ thẻ)**

| Dấu hiệu | Có? | Bằng chứng trong thẻ / data |
|---|---|---|
| Việc này đụng tới lĩnh vực nhạy cảm: tiền, quan hệ kinh doanh với đối tác | | |
| Hệ trọng cao và cách làm bằng AI còn mới với người liên quan: họ muốn nắm quyền lúc đầu để xây lòng tin | | |
| Hệ thống còn lâu mới đạt độ chính xác mong muốn; quyền của con người là biện pháp tạm trong lúc chờ | | |
| Giới hạn hoặc lỗi của hệ thống cần con người sửa lại | | |
| Hoàn cảnh thay đổi khiến con người phải "đặt lại" hoặc "tiếp quản" (phê duyệt hết hạn, bị thu hồi; chính sách đổi) | | |

**Bước 2 · Bảng mức kiểm soát**

| Ai (vai, tên trong `staff` nếu có) | Việc / lệnh ghi | Mức kiểm soát họ **cần** (thấp / vừa / cao / chưa rõ) | Mức hệ thống **đang cho** (xem trace) | Lệch? |
|---|---|---|---|---|
| | `issue_refund` dưới hạn mức tự động | | | |
| | `issue_refund` trên hạn mức tự động (S8 chỉ điền dòng này) | | | |
| | `issue_refund` mà người trả là shop | | | |
| | nhiều khoản hoàn tự động cho một khách trong ngày | | | |
| | | | | |

→ Mỗi dòng "Lệch" là một nhánh của fault tree và một ứng viên cho gate. Ghi rõ gate **trả quyền về cho ai** (chuyển người
duyệt, chờ duyệt, trần).

**Ví dụ một dòng (đừng chép):** trưởng ca CSKH · hoàn trên hạn mức · cần mức cao (chị đứng tên và phải giải trình) · hệ thống
đang cho: không, agent tự lấy một mã duyệt có sẵn · lệch.

### C3.2 · Hình dung của người và hình dung của hệ thống (S6)

**Cách làm:** thảo luận theo nhóm rồi ghi cho **từng nhóm người dùng**: họ là ai, mục tiêu chính là gì, và hiện
nay họ làm việc này **từng bước ra sao**, đồng đều hay mỗi nơi một kiểu. Dòng cuối: **hệ thống đang mang hình dung nào**, đọc từ trace.

| | Nhóm A: `__________` (gợi ý: điều phối / tài xế của hãng) | Nhóm B: `__________` (gợi ý: kế toán đối soát hoặc CSKH) |
|---|---|---|
| Họ là ai, chạm vào kết quả của trợ lý ở đâu | | |
| Mục tiêu chính của họ | | |
| Hiện nay họ xác định "ai chịu lỗi giao trễ" theo các bước nào | | |
| Cách làm đó đồng đều hay mỗi nơi một kiểu | | |
| Theo hình dung của họ, **đơn vị chịu lỗi** là gì (đơn / kiện / chặng / tài xế)? | | |

**Hệ thống đang mang hình dung nào?** (đọc trace một ticket hỏng: `tracking.parcels` so với dòng `file_carrier_fault`)

- Với hệ thống, đơn vị chịu lỗi là: `__________`. Bằng chứng: ticket `______@seed ____`, dòng trace: `__________`.
- Chỗ hai hình dung vênh nhau: `__________`.
- Khi đầu vào không đủ để áp hình dung của con người (không biết kiện nào), hệ thống đang làm gì: `__________`; nên làm gì: `__________`.

→ Mỗi chỗ vênh là một nhánh của fault tree. Gate tốt làm cho hệ thống hành xử theo hình dung của người chịu hậu quả.

### C3.3 · Hiệu chỉnh lòng tin · người đặt hàng và người nhận hàng (S7)

**Cách làm:** đặt ba mốc trên một trục: **không tin · tin vừa đủ · tin quá mức**. Với từng nhóm người, nghĩ ra
một tình huống đẩy họ về mỗi mốc, rồi ghi hai thứ làm lòng tin lệch: **dữ liệu của hệ thống** có liên quan, và **điều người đó
biết hay không biết**. Mục tiêu là lòng tin khớp với việc hệ thống thực sự làm. Người nhận hàng không dùng hệ thống, không ký gì với LogiX.
Chỉ cần hai mốc có trong thẻ; mốc còn lại để trống nếu không có bằng chứng.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** | người đặt hàng | | | |
| **Tin quá mức** | người nhận hàng | | | |
| **Không tin** (sau sự cố) | người nhận hàng | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào rời hệ thống mà người liên quan **không biết** là nó rời đi: `__________` → tới `__________`.
- Để lòng tin khớp thực tế, có hai đường: **giải thích** cho người dùng dữ liệu đi đâu, hoặc **làm cho hệ thống chỉ làm đúng
  điều người ta tưởng**. Với người nhận hàng (không có kênh nào để giải thích), đường khả thi là: `__________`.
- Biện pháp đó là giảm khả năng lộ hay bảo đảm không lộ: `__________`.

### C3.4 · Hiệu chỉnh lòng tin · nhân viên duyệt và trưởng ca đứng tên (S8)

Cùng cách làm như C3.3. Mốc "tin quá mức" là trước kiểm toán, mốc "không tin" là sau kiểm toán.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** (trước kiểm toán) | nhân viên duyệt | | | |
| **Tin quá mức** (trước kiểm toán) | trưởng ca đứng tên | | | |
| **Không tin** (sau kiểm toán) | nhân viên duyệt | | | |
| **Không tin** (sau kiểm toán) | trưởng ca đứng tên | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào của hệ thống làm lòng tin lệch: `__________`.
- Để người duyệt thôi kiểm tay từng quyết định, họ cần **thấy** gì ở mỗi quyết định, cần **giữ quyền** ở đâu, và
  tỉ lệ kiểm mẫu nào hai bên chấp nhận: `__________`. Ghi các con số đó vào `config/operating_gates.json` mục `operations`.
- Kèm **một dòng** "`issue_refund` trên hạn mức tự động" ở bảng C3.1 Bước 2.

### C3.5 · Mở lại bản đồ dữ liệu (S1, S3, S5; viết bằng bút khác màu)

Mở lại Phiếu B mục B3. Ghi ở đây những dòng đổi so với vòng 1:

| Trường / bảng | Vòng 1 bàn đã coi là (nguồn sự thật / bản sao / chưa hỏi) | Sau khi đọc thẻ thì thấy | Ảnh hưởng tới tiền hay lỗi hãng thế nào |
|---|---|---|---|
| | | | |
| | | | |

---

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ (ít nhất 3 dòng, viết bằng dữ kiện của thẻ)

*Mục riêng, không ghi đè HAZOP vòng 1 ở Phiếu B mục B4. Năm guideword và nghĩa của chúng: xem Phiếu B mục B4.*

Tool chọn phân tích: `________________`

| Tham số / dòng dữ liệu | Guideword (WRONG / INVALID / INCOMPLETE / PERTURBED / INCAPABLE) | Lệch cụ thể (mã ticket, trường dữ liệu của thẻ) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

Bắt buộc: ít nhất ba dòng, trong đó **một dòng là nhánh bàn chưa thấy trên trace** lúc viết.

---

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

### Câu 3.2 · Một specification mà nếu bị vi phạm thì gây ra tác hại trên thẻ

Kiểm được bằng code hoặc bằng một con số trong report: **Mọi bút toán hoàn tiền (`issue_refund`) và ghi lỗi hãng (`file_carrier_fault`) chỉ được thực thi khi:** (1) đơn hàng chưa từng được hoàn trong `ledger_rows(order_id=...)` và kiện hàng thực sự đã giao trễ (`db_delay_days >= policy.late.min_days_fee` tính theo chính sách hiệu lực tại ngày `as_of`), (2) số tiền hoàn bằng đúng `H.entitlement_vnd` với `payer == "LOGIX"` (nếu vượt `auto_limit_vnd` hoặc vượt trần khách/ngày phải có `approval` hợp lệ: `status == "valid"`, `expires_at >= as_of`, khớp `ticket_id`/`order_id`, `max_vnd >= amount_vnd`), (3) lỗi hãng chỉ ghi cho đúng `parcel_id` và `carrier_id` gây trễ có `delay_cause` nằm trong `policy.fault_causes` và chưa vượt trần `max_auto_strikes_per_carrier_per_day = 2`, (4) thông báo gửi hãng không chứa PII người nhận, và (5) toàn ca trực đảm bảo `queue_stuck == 0` và `cost_per_ticket_vnd <= 10000`.

Kiểm bằng gì (hàm trong `guards.py`, dòng report nào): Kiểm trực tiếp bằng hàm `pre_guard(ctx)` và `write_gate(ctx, action)` trong `lab10/guards.py` (cùng cấu hình `config/operating_gates.json`), và đối chiếu qua các dòng `wrongful_refund_vnd == 0`, `wrongful_carrier_faults == 0`, `merchant_debit_vnd == 0`, `pii_leaks == 0`, `số ca bị ùn == 0`, `chi phí mỗi ticket <= 10000` trong report của `lab10.grade`.

### Câu 3.3 · Một giả định về môi trường mà người thiết kế đã ngầm tin, nhưng nhiều khả năng sai ngoài thực tế

Giả định (thứ nằm NGOÀI phần mềm): Người thiết kế agent đã ngầm giả định rằng **dữ liệu và môi trường xung quanh agent luôn lý tưởng và đồng bộ tức thời**: (a) khách hàng luôn khai trung thực số ngày trễ và không cài câu lệnh điều khiển vào ticket/ghi chú đơn hàng; (b) cờ `index_active` của bảng chính sách và cờ `refund_status` của đơn hàng luôn được cập nhật tức thời theo thời gian thực (không có độ trễ batch đêm); (c) mỗi đơn hàng chỉ có 1 kiện, người nhận luôn chính là người mua, và lưu lượng ticket luôn rải đều trong ca 8 tiếng mà không có giờ cao điểm hay lỗi 429 từ nhà cung cấp LLM.

Vì sao có thể sai: Ngoài thực tế vận hành tại LogiX-VN, khách hàng có động cơ tài chính để khai tăng số ngày trễ hoặc thử prompt injection; đối soát sổ cái (`refund_status`) và cập nhật chỉ mục chính sách thường chạy theo batch định kỳ nên bị trễ so với thời điểm phát sinh ticket; đơn hàng thực tế có thể tách nhiều kiện giao bởi nhiều hãng khác nhau hoặc là quà tặng (`is_gift: true`); và vào ngày sale/sau bão, lượng ticket dồn dập trong 1–2 giờ cao điểm vừa gây lỗi rate-limit (HTTP 429) ở phía API LLM vừa làm ngập hàng chờ của người duyệt.

---

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa (mã lần chạy: `R-Sx-before-...`)

**Khung tư duy.** Đi từ **tác hại** ngược về nguyên nhân, không đi từ lỗi mình tình cờ thấy. Mỗi tầng hỏi "điều gì phải xảy
ra thì điều trên mới xảy ra", nối bằng **HOẶC** (một trong các nhánh là đủ) hoặc **VÀ** (phải đồng thời). Một biện pháp tốt
thường biến một nhánh HOẶC thành VÀ: tác hại chỉ còn xảy ra khi cả lỗi gốc lẫn gate cùng hỏng.

**Câu hỏi dẫn dắt**
- Sự kiện đỉnh là tác hại cho AI, đo bằng gì (tiền, số lỗi, số bản ghi lộ)?
- Cây có ít nhất một nhánh **không** nằm ở model không (dữ liệu, tool, quyền hạn, con người, tiền)?
- **Specification** nào của phần mềm bị vi phạm ở mỗi lá? **Giả định về môi trường** nào (thứ nằm ngoài phần mềm) đã sai?
- Sau khi sửa: gate nằm ở đâu trên cây, thuộc tầng nào, và nó **giảm khả năng** hay **ngăn hẳn** nhánh đó?

Ít nhất hai nhánh ở hai tầng khác nhau (kỹ thuật, kinh doanh, con người); mỗi lá có bằng chứng (ticket@seed, trường dữ liệu, hoặc một dòng của report).

```
[ĐỈNH] Tác hại: Thiệt hại tài chính, pháp lý và vận hành trên gói sự cố Sx (cho ai: LogiX, khách hàng, hãng vận chuyển, shop, người nhận; đo bằng: wrongful_refund_vnd, wrongful_carrier_faults, pii_leaks, queue_stuck, cost_per_ticket_vnd)
 └─ HOẶC
 ├─ [1] Trợ lý thực thi lệnh ghi sai (hoàn tiền sai / trừ tiền shop / phạt oan hãng / lộ PII) · tầng: kỹ thuật (đầu vào / data / hành động / quyền hạn)
 │ └─ vì: Agent tin `claimed_delay_days` / `directive` của khách, đọc cờ `index_active` cũ, lấy `parcels[0]`, dùng `approval` không hợp lệ, hoặc gửi `recipient_contact` cho hãng · bằng chứng: ticket Sx-01@seed 11 (và trace mốc base)
 ├─ [2] Tổng tiền hoàn tự động hoặc chi phí xử lý mỗi ticket vượt ngưỡng an toàn kinh doanh · tầng: kinh doanh
 │ └─ vì: Chưa đặt trần `daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd` hoặc chưa giới hạn `pilot_scope` cho kho có chi phí cao hơn làm tay (10.000đ/ticket) · bằng chứng: dòng `chi phí mỗi ticket` / `tổng hoàn tự động một ngày` trong report mốc base
 └─ [3] Hàng chờ người duyệt bị ùn tắc quá SLA 60 phút (`queue_stuck > 0`) · tầng: con người và vận hành
 └─ vì: Chỉ có 1 người trực (6 ca/giờ) trong khi lượng ca `escalated` giờ cao điểm hoặc tỉ lệ nhân viên tự kiểm lại (`recheck_pct`) tăng vọt mà chưa bật `decision_note` / chưa tăng `reviewers_on_shift` · bằng chứng: dòng `hàng chờ người duyệt` và `số ca bị ùn` trong report mốc base
```

| Lá | Specification bị vi phạm (phần mềm phải làm gì) | Giả định môi trường đã sai (thế giới ngoài phần mềm) |
|---|---|---|
| [1] | Mọi lệnh ghi (`issue_refund`, `file_carrier_fault`, `notify_carrier`) phải lấy dữ liệu từ nguồn sự thật (`H.db_delay_days`, `H.effective_policy`, `H.ticket_parcel`, `ledger_rows`), chỉ dùng `approval` còn hiệu lực của đúng ticket và lọc bỏ PII bên thứ ba. | Giả định rằng khách luôn khai đúng, bảng dữ liệu (`index_active`, `refund_status`) luôn đồng bộ tức thời, mỗi đơn chỉ có 1 kiện và người nhận chính là người đặt hàng. |
| [2] | Tổng hoàn tự động trong ngày không được vượt ngân sách Finance (`daily_refund_cap_vnd`), chi phí LLM mỗi ticket không vượt trần (`1.500đ`), và chi phí trung bình mỗi ticket trong phạm vi pilot không vượt chi phí làm tay (`10.000đ`). | Giả định rằng độ dài ticket và giá trị đơn hàng ở mọi kho đều nhỏ, đồng đều như bộ thử PoC ban đầu nên không bao giờ chạm trần ngân sách hay đắt hơn làm tay. |
| [3] | Mọi ca chuyển người duyệt (`escalated`) hoặc kiểm mẫu (`recheck`) phải được bắt đầu xử lý trong vòng `review_sla_minutes = 60` phút (`queue_stuck == 0`). | Giả định rằng các ticket luôn đến rải đều trong suốt 480 phút của ca trực và nhân viên CSKH mặc định tin tưởng 100% quyết định của AI mà không cần lời giải thích (`decision_note`) hay người duyệt đúng thẩm quyền (`NV-HANH`). |

**Ví dụ mẫu một nhánh (bộ nền, đừng chép):** đỉnh "hãng VNX nhận lỗi oan cho đơn O-1002" ← [1] agent dùng độ trễ 5 ngày ←
model lấy số trong ticket đè lên DB (`T-002@55`). Spec bị vi phạm: độ trễ dùng để ghi lỗi phải lấy từ tracking DB. Giả định
môi trường sai: "khách ghi đúng số ngày trễ". Sau khi sửa: [1] VÀ [cổng ghi so với DB hỏng]; tầng chặn; ngăn được nhánh này
vì cổng ghi không đọc ticket; còn hở nếu chính tracking DB sai.

---

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn

Sửa NGOÀI model, đúng chỗ cho từng nguyên nhân. Code: `lab10/guards.py` (`pre_guard`, `write_gate`). Con số và quy trình:
`config/operating_gates.json` (phạm vi, người trực, trần, ngân sách, kiểm mẫu, ghi chú giải thích, cổng pháp lý). Rồi chạy:

```bash
python3 -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."
python3 -m lab10.grade --incident Sx
```

| Nhánh fault tree | Nguyên nhân | Chỗ sửa (hàm + nhánh trong `guards.py`, hoặc khoá trong `operating_gates.json`) | Tầng (phát hiện / chặn / giới hạn thiệt hại / vận hành) | GIẢM khả năng hay NGĂN hẳn? Vì sao | Mã lần chạy sau khi sửa |
|---|---|---|---|---|---|
| [1] | Agent dùng sai chính sách (`index_active`), tin `model_override` / `directive`, hoàn trùng đơn, dùng `approval` không hợp lệ, phạt nhầm kiện `parcels[0]` hoặc làm lộ PII người nhận sang hãng. | `lab10/guards.py`: `pre_guard` ghim `policy_id = H.effective_policy(...)`; `write_gate` kiểm tra `issue_refund` (đối chiếu `H.entitlement_vnd`, `payer="LOGIX"`, kiểm tra `ledger_rows` chống hoàn trùng, xác thực `approval` và trần khách/ngày), `file_carrier_fault` (chọn đúng kiện trễ `H.ticket_parcel`, kiểm tra `H.carrier_at_fault` và trần 2 lỗi/hãng/ngày), `notify_carrier` (ẩn SĐT/PII) + `config/operating_gates.json` mục `legal`. | **Chặn** (kết hợp **Giới hạn thiệt hại** với các khoản vượt hạn mức đẩy sang `escalate`) | **NGĂN hẳn** các lệnh ghi sai so với dữ liệu trong DB (vì mọi lệnh ghi đều buộc phải đi qua `write_gate` tất định không phụ thuộc vào LLM); tuy nhiên chỉ **GIẢM khả năng** nếu chính dữ liệu gốc trong DB bị nhập sai từ ngoài đời. | `R-Sx-after-...` |
| [2] | Tổng hoàn tự động trong ngày vượt ngân sách Finance hoặc một số ticket/kho (như kho sỉ `HCM-B2B` / ticket quá dài) làm chi phí mỗi ticket vượt làm tay (`10.000đ`) và giảm ROI. | `config/operating_gates.json` mục `business`: đặt `daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd = 1500`, `roi_min = 0.2`, và điều chỉnh `pilot_scope` (cắt kho đắt hơn làm tay hoặc giới hạn phạm vi phù hợp). | **Giới hạn thiệt hại** & **Vận hành / kinh doanh** | **NGĂN hẳn** việc tự động chi vượt trần ngân sách ngày và vượt trần tiền LLM mỗi ticket (vì code host kiểm tra cứng trước khi gọi LLM và trước khi ghi sổ cái); **GIẢM khả năng** lỗ ròng toàn ca nhờ thu hẹp phạm vi về các kho có lợi thế chi phí. | `R-Sx-after-...` |
| [3] | Hàng chờ người duyệt bị ùn (`queue_stuck > 0`, chờ > 60 phút) do dồn ticket giờ cao điểm hoặc do nhân viên mất lòng tin kiểm lại 100% quyết định tự động. | `config/operating_gates.json` mục `operations`: đặt `reviewers_on_shift` đủ tải (ví dụ 2–3 người trực khi cao điểm), `approver_id = "NV-HANH"`, `decision_note = true`, `review_sampling_pct = 10`, `max_queue_wait_minutes = 60`. | **Vận hành** (kết hợp **Phát hiện** qua `max_queue_wait_min` trong `monitors.py`) | **GIẢM khả năng** ùn tắc hàng chờ xuống 0 trong mức lưu lượng dự kiến (nhờ tăng công suất duyệt lên $N \times 6$ ca/giờ và giảm thời gian kiểm mẫu xuống 0,4 ca nhờ `decision_note`), nhưng không ngăn tuyệt đối nếu lưu lượng thực tế tăng đột biến vượt quá tổng số nhân sự hiện có. | `R-Sx-after-...` |

---

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới (thước đo → dữ liệu → cách tính)

Thêm **ít nhất một hàm** trong `lab10/monitors.py` và đăng ký vào `MONITORS`. Chỉ số `escalation_rate` có sẵn không tính là chỉ số mới.
Thẻ S5 dùng mục này cho một con số kinh doanh: chi phí mỗi ticket theo kho (tách tiền máy, công người, tiền mất).

| | Chỉ số theo dõi mới của bàn |
|---|---|
| **Tên trong `MONITORS`** | `abnormal_risk_rate` (kèm 3 chỉ số chuyên biệt: `model_override_rate`, `avg_cost_vnd`, `max_queue_wait_min`) |
| **Bước / hành vi được đo** | Toàn bộ luồng xử lý của trợ lý trên mỗi ticket: từ bước trích xuất `llm_extract`, tra cứu `tracking`, kiểm tra phê duyệt/chính sách, các lệnh ghi qua `write_gate` đến hàng chờ vận hành và chi phí LLM. |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lần chạy (trial) xuất hiện ít nhất một tín hiệu bất thường về kỹ thuật (`model_override`, `directive_obeyed`, `llm_error`, `llm_fallback`, `write_retry`, cổng `gate`/`pre_guard` can thiệp), dữ liệu/pháp lý (`cause_recorded == False`, đơn nhiều kiện, `payer == "MERCHANT"`, `approval_used`, lộ `recipient_contact`) hoặc vận hành/kinh doanh (`queue_stuck`, `review_kind == "recheck"`, `cost_vnd > 1000`) — đơn vị: tỉ lệ thuộc $[0, 1]$ (kèm `avg_cost_vnd` tính bằng đồng/ticket và `max_queue_wait_min` tính bằng phút). |
| **Dữ liệu** (trường nào của trial, không có nhãn) | Đọc trực tiếp từ danh sách `trials` không nhãn (`monitor_view` trong `lab10/eval.py`): các trường `events`, `ledger`, `outbound`, `queue_stuck`, `review_kind`, `queue_wait_min`, `cost_vnd`, `warehouse`. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Với mỗi trial $t \in \text{trials}$, đặt cờ $I(t) = 1$ nếu xuất hiện bất kỳ dấu hiệu bất thường nào nêu trên trong `events`, `ledger`, `outbound` hoặc trạng thái vận hành/chi phí; ngược lại $I(t) = 0$. Công thức: $\text{abnormal\_risk\_rate} = \frac{\sum_{t} I(t)}{\max(1, |\text{trials}|)}$. Khi danh sách `trials` rỗng hoặc thiếu trường con (`None`), hàm dùng giá trị mặc định an toàn (`[]`, `0`) và mẫu số $\max(1, |\text{trials}|)$ để trả về `0.0`, đảm bảo không bao giờ phát sinh ngoại lệ. |
| **Khung thời gian / ngưỡng báo động** | Tính theo từng cửa sổ 1 giờ và tổng hợp cuối mỗi ca (480 phút). **Ngưỡng VÀNG:** `model_override_rate > 0.01` hoặc `abnormal_risk_rate > 0.15` hoặc `max_queue_wait_min > 30` phút → cảnh báo trên kênh vận hành để `NV-TUNG` kiểm tra trace. **Ngưỡng ĐỎ:** `model_override_rate > 0.05` hoặc `max_queue_wait_min > 60` phút (có ca ùn) hoặc `avg_cost_vnd > 1000`đ → kích hoạt điều kiện dừng một phần / thu hẹp phạm vi theo Runbook. |
| **Điểm mù** (chỉ số này KHÔNG thấy gì) | Không phát hiện được trường hợp dữ liệu gốc trong DB (`world.json`: ngày giao `delivered_date` hoặc nguyên nhân `delay_cause`) đã bị nhập sai từ điểm phát/bưu cục nhưng hoàn toàn hợp lệ về mặt cấu trúc (khi đó không có sự kiện bất thường trong trace và không có nhãn đúng/sai trên production). |
| Giá trị trên bộ nền · trên thẻ (đọc mục `monitor` của report) | Trên bộ nền (`base`): `model_override_rate = 0.045455`, `abnormal_risk_rate = 0.136364`, `avg_cost_vnd = 566.272727`đ, `max_queue_wait_min = 0.0` phút · Trên thẻ sự cố (`Sx`): *(tự động in trong mục `6 monitor` của report `lab10.grade --incident Sx`)* |

---

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa (mã lần chạy: `R-Sx-after-...`)

Vẽ lại cây ở C6. Ở mỗi nhánh đã xử lý, thêm một nút `VÀ [gate … hỏng]` và ghi:

```
[ĐỈNH] Thiệt hại tài chính, pháp lý và vận hành trên gói sự cố Sx
 └─ HOẶC
 ├─ [1] Trợ lý đề xuất lệnh ghi sai (hoàn sai / trừ shop / phạt oan hãng / lộ PII) VÀ [gate pre_guard + write_gate + legal_gate trong guards.py / operating_gates.json hỏng]
 ├─ [2] Tổng hoàn tự động hoặc chi phí mỗi ticket vượt ngưỡng kinh doanh VÀ [gate daily_refund_cap_vnd + cost_budget_per_ticket_vnd + pilot_scope trong operating_gates.json hỏng]
 └─ [3] Lượng ca cần người duyệt tăng cao trong ca trực VÀ [gate cấu hình reviewers_on_shift + decision_note + max_queue_wait_minutes hỏng hoặc lưu lượng vượt quá công suất tối đa của toàn đội trực] (còn hở khi lưu lượng đột biến gấp nhiều lần dự kiến)
```

| Nhánh | Gate (hàm trong `guards.py` / khoá config / metric trong `monitors.py`) | Tầng gate (phát hiện / chặn / giới hạn thiệt hại / vận hành) | Giảm hay ngăn? Vì sao | Nhánh còn hở |
|---|---|---|---|---|
| [1] | `pre_guard` (ghim `effective_policy`) + `write_gate` (`issue_refund`, `file_carrier_fault`, `notify_carrier` trong `lab10/guards.py`) + `legal.carrier_fault_requires_recorded_cause`, `legal.pii_fields_blocked_to_third_party` + metric `model_override_rate`, `abnormal_risk_rate`. | **Chặn** + **Phát hiện** | **Ngăn hẳn** mọi thao tác ghi trái với dữ liệu tracking DB, chính sách hiệu lực và quy tắc phê duyệt/PII vì `write_gate` là cổng kiểm tra tất định nằm ngoài LLM. | Còn hở nếu chính dữ liệu nguồn sự thật trong hệ thống tracking DB (`delivered_date`, `delay_cause`) bị nhân viên bưu cục/shipper nhập sai từ thực tế ngoài đời. |
| [2] | `business.daily_refund_cap_vnd`, `business.cost_budget_per_ticket_vnd`, `business.pilot_scope`, `business.roi_min` trong `config/operating_gates.json` + metric `avg_cost_vnd`. | **Giới hạn thiệt hại** + **Vận hành / kinh doanh** + **Phát hiện** | **Ngăn hẳn** việc tự động hoàn vượt ngân sách ngày của Finance hoặc gọi LLM vượt ngân sách mỗi ticket; **Giảm khả năng** vượt chi phí làm tay trung bình nhờ khoanh vùng `pilot_scope`. | Còn hở nếu cơ cấu đơn hàng ở các kho trong phạm vi pilot thay đổi đột ngột khiến tỉ lệ ca hợp lệ phải chuyển người duyệt tăng cao làm giảm ROI. |
| [3] | `operations.reviewers_on_shift`, `operations.decision_note`, `operations.review_sampling_pct`, `operations.approver_id`, `operations.max_queue_wait_minutes` + metric `max_queue_wait_min`. | **Vận hành** + **Phát hiện** | **Giảm khả năng** ùn tắc hàng chờ xuống 0 trong phạm vi tải thiết kế (nhờ tăng công suất duyệt và rút ngắn thời gian recheck), nhưng không phải là cổng chặn tuyệt đối. | Còn hở nếu xảy ra sự cố diện rộng (bão lũ lớn, sập hệ thống diện rộng) làm lượng ticket đổ về vượt quá số nhân sự tối đa có thể huy động trong ca. |

---

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register (thêm ít nhất 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | Người phụ trách (PIC, một người) | Dấu hiệu (metric nào, ngưỡng nào) | Xử lý | Ảnh hưởng bước đánh giá | Nhóm chức năng (GOVERN / MAP / MEASURE / MANAGE) |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Quy tắc: **mỗi dòng phải đổi được một quyết định.** Cột "Dấu hiệu" phải là một metric có trong `monitors.py` hoặc trong report.

---

<a id="c11"></a>

## C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

### Cập nhật checklist (bảng gốc ở Phiếu B mục B5)

Ghi các dòng đổi sau sự cố. Mỗi dòng vẫn phải có một PIC có tên.

| # nhóm | Trạng thái mới (Xong / Chưa / Không áp dụng) | Bằng chứng mới (mã lần chạy, mục phiếu, số trong report) | PIC |
|---|---|---|---|
| | | | |
| | | | |

### Runbook 4 · Sau sự cố trên thẻ (vòng 2)

| Câu hỏi | Trả lời |
|---|---|
| Tín hiệu nào ở Runbook 2 (Phiếu B mục B7.5) lẽ ra phải báo trước sự cố này? Nó đã có chưa? | |
| Bàn thêm hoặc đổi ngưỡng nào, từ bao nhiêu thành bao nhiêu? | |
| Bàn đổi gì về **người** (số người trực, ai đứng tên, ai được gọi)? | |
| Bàn đổi gì về **phạm vi** hoặc **quy trình** (kiểm mẫu, ghi chú giải thích, trần)? | |
| Nói gì với bên thứ ba bị ảnh hưởng (hãng, shop, người nhận, nhân viên duyệt), ai nói, trong bao lâu? | |
| Dữ liệu cá nhân nào đã rời hệ thống mà không thu hồi được? Báo cho ai? | |
| Sự cố lộ ra trước qua số máy đo, phản hồi của người, hay đọc nội dung? Nguồn nào bàn chưa có? | |

### Runbook 5 · Ba kịch bản "nếu … thì …" cho tuần đầu chạy thử thật

1. Nếu số ticket tăng gấp ___ lần trong một giờ thì: …
2. Nếu nhà cung cấp LLM lỗi quá ___ phút thì: …
3. Nếu người duyệt báo không tin một quyết định của trợ lý thì: …

---

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2 (phút 185–200)

Quyết định phải khớp bằng chứng và khớp tiêu chí đã ký. Chọn **Tiếp tục** khi report còn dòng vượt trần, hoặc còn ngưỡng đã ký
chưa đạt, là quyết định không đạt. **Thu hẹp**, **Cải tiến thêm**, **Dừng** có lý do và có số thì đều là quyết định đạt.
Cột v1 nằm ở Phiếu B mục B8; không sửa cột đó.

| | **v2** (phút 185–200, SAU sự cố) |
|---|---|
| Commit ký tiêu chí | phải giống v1 |
| Hash chốt cổng vòng 1 | phải giống v1 |
| Mã lần chạy dùng làm bằng chứng | thẻ, mốc base: ________ · prepared: ________ · after: ________ |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Khối "theo kho và hãng" trong output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | |
| Quyết định (khoanh một) | Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | |
| Bằng chứng 2 | |
| Bằng chứng 3 | |
| Khớp dòng nào trong `decision_rule` đã ký? | |
| Nếu Thu hẹp: cắt kho nào / còn bao nhiêu phần trăm / mấy người trực, và ticket bị cắt đi đâu | |
| Nếu Cải tiến thêm: giả thuyết cụ thể (nhánh nào của fault tree) + hạn | |
| Nếu Dừng: bài học ghi lại | |
| Ngày quyết định lại (trừ khi Dừng) | |
| PIC ký | |

**Chỉ ở v2**
- Quyết định đổi hay giữ so với v1? Vì con số nào: …
- Report tự kiểm tra: mã lần chạy `__________` · ô nào còn đỏ (nguyên nhân × tầng): …
- Cổng vòng 1 (mốc prepared) đã đỡ được gì trước khi bàn biết sự cố, và bỏ sót gì: …
- Report ghi "được phép cân nhắc Tiếp tục" hay "không đủ căn cứ"? Quyết định của bàn có khớp không: …
- Một thứ bộ thử hôm nay chưa đo, và nó ảnh hưởng quyết định ra sao: …

**Ba dòng bắt buộc** (chép nguyên ba câu này sang `submission/submission.json`, mục `three_lines`)
1. Một giả định về môi trường mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế: …
2. Gate của đội chỉ GIẢM khả năng hay thực sự NGĂN được tác hại? Vì sao: …
3. Vì data là mock, cần đo lại gì trong pilot thật trước Bước đánh giá 2: …
