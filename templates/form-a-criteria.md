# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn: K5-L3A-DAY10-F4-PoCtoPilotGate1** · **Người cầm bút chính: Le Quang Linh** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hóa quy trình tiếp nhận, thẩm định và chi trả hoàn tiền giao hàng trễ cho khách hàng cuối tại 2 depot thử nghiệm, giúp giảm chi phí xử lý mỗi ticket xuống thấp hơn mức làm thủ công (10.000đ/ticket) đồng thời giữ nguyên độ chính xác sổ cái tài chính, bảo vệ dữ liệu cá nhân (PII) và đảm bảo các ca ngoại lệ/vượt hạn mức được chuyển cho nhân viên CSKH xử lý đúng SLA 60 phút.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi khoản hoàn tiền tự động ghi vào sổ cái đều có căn cứ chính sách (`policy`) hoặc mã phê duyệt hợp lệ (`approval_id` còn hiệu lực, đúng đơn/khách/hạn mức), không hoàn trùng đơn đã hoàn và không ghi sai lỗi phạt cho hãng vận chuyển để tránh lệch công nợ đối soát cuối tuần với hãng và shop.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Trợ lý tự giải quyết dứt điểm các ca đơn giản đúng chính sách để giảm tải cho ca trực, chỉ chuyển sang hàng chờ những ca thực sự cần người duyệt (vượt hạn mức, thiếu căn cứ, ngoại lệ) kèm ghi chú giải thích rõ ràng (`decision_note`) và giữ tốc độ đẩy ca phù hợp công suất duyệt (6 ca/giờ/người) để không gây ùn quá SLA 60 phút.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước **ghi lỗi hãng vận chuyển (`file_carrier_fault` / `notify_carrier`)** | Hành vi **chi hoàn tiền tự động (`issue_refund`), ghi lỗi hãng (`file_carrier_fault`) và gửi thông báo cho hãng vận chuyển (`notify_carrier`)** ra hệ thống bên ngoài |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ (%) lệnh gọi `file_carrier_fault` bị ghi oan (gán lỗi cho hãng khi nguyên nhân thực tế không thuộc `fault_causes` của chính sách hiệu lực, hoặc `db_delay_days < min_days_fee`, hoặc sai đối tượng hãng/kiện so với `label.faults`, kèm số lỗi hãng oan tuyệt đối `wrongful_carrier_faults` trên 110 lần chạy). | 1) Tỉ lệ (%) khoản hoàn tiền tự động bị khách hàng/shop khiếu nại hoặc kế toán hoàn tác (`ledger_reversal_rate`); 2) Số lượng lệnh phạt hãng (`strike`) cho cùng 1 hãng/ngày ($\text{strikes/carrier/day}$) hoặc bị hãng phản hồi khiếu nại (`carrier_dispute_count`); 3) Số lần lộ PII người nhận trong `notify_carrier`. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Nhật ký sự kiện tool call (`file_carrier_fault` / `fault_rows`) trong `runs/<mã lần chạy>/traces/` đối chiếu với `label.faults` trong `data/tickets.jsonl` và trường `parcels[].delay_cause`, `carrier_id`, `policies[].fault_causes` trong `data/world.json` trên toàn bộ 22 ticket × 5 seed = 110 lượt chạy bộ nền (nhãn chuẩn từ `world.json`, nối tiếp chuẩn `docs/eval_card.md` Lab 9). | Nhật ký giao dịch sổ cái (`ledger`), bảng `faults`, log gửi `notify_carrier` (`outbound`), hệ thống ticket khiếu nại từ khách hàng/shop và cổng phản hồi đối soát của các hãng (`GHSH`, `VNX`, `MKD`, `DNB`) trên 100% giao dịch pilot thực tế (tự động, không dùng nhãn thủ công trước). |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Với mỗi trial $i$, tập lỗi agent ghi là $F_i = \{(c, p)\}$ từ `world.faults` và nhãn chuẩn là $L_i = \text{label.faults}$. $\text{Tỉ lệ ghi lỗi oan} = \frac{\sum_i |F_i \setminus L_i|}{\max(1, \sum_i |F_i|)}$ (kèm tổng `wrongful_carrier_faults` $= \sum_i |F_i \setminus L_i|$). Các lượt chạy không gọi `file_carrier_fault` ($|F_i|=0$) bị loại khỏi mẫu số tỉ lệ và đếm riêng; nếu thiếu `delay_cause` trong DB thì tính là lỗi thiếu căn cứ (tử số +1). | 1) $\text{Tỉ lệ hoàn tác} = \frac{\text{Số giao dịch hoàn tự động bị khiếu nại/hủy trong } T}{\text{Tổng số giao dịch hoàn tự động trong } T} \times 100\%$; 2) Đếm $\max_c \text{count}(\text{faults where carrier\_id}=c)$ và $\sum \text{lệnh strike bị hãng mở tranh chấp trong } T$; 3) Đếm số tin `outbound` tới `carrier:*` chứa `recipient_contact` hoặc SĐT người nhận. Ca thiếu `order` trong DB đếm riêng vào nhóm `escalated`. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Cửa sổ trượt **1 giờ** và tổng hợp **cuối mỗi ca (8 giờ / 480 phút)**. Báo động đỏ ngay lập tức nếu: có **≥ 1** lần rò rỉ PII cho hãng/khách lạ hoặc trừ tiền `MERCHANT` sai, hoặc **≥ 2** lỗi tự động/khiếu nại phạt oan từ cùng một hãng trong 1 ngày (`max_auto_strikes_per_carrier_per_day = 2`), hoặc tỉ lệ hoàn tác vượt **1%** trong 1 giờ. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện được trường hợp dữ liệu gốc trong `world.json` (`parcels[].delay_cause` hoặc `delivered_date`) bị nhân viên kho/bưu cục nhập sai so với thực tế ngoài đời, hoặc trường hợp `notify_carrier` lộ PII dù mã hãng/kiện bị phạt là đúng. | Không phát hiện được trường hợp **hoàn thiếu tiền** hoặc **bỏ sót quyền lợi** của khách hàng nếu khách không chủ động khiếu nại lại, hoặc trường hợp hệ thống tracking DB của bưu cục ghi nhầm `delay_cause = "CARRIER"` và chưa đến kỳ đối soát tuần với shop/hãng. |

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)** *(Chưa đủ căn cứ nói Y tốt hơn X; chênh 1 lần chạy nằm trong khoảng tin cậy của X)*

Giải thích một câu: Vì `pass_rate` của bản Y ($1,0$ trên 50/50 lần chạy) nằm hoàn toàn bên trong khoảng tin cậy 95% của bản X ($[0,9400; 1,0]$), mức chênh lệch 0,02 (đúng 1/50 lần chạy, tương tự giới hạn cỡ mẫu đã nêu ở `docs/PRD_v1.1.md` §6 và `docs/eval_card.md`) chưa đủ ý nghĩa thống kê để khẳng định Y thực sự tốt hơn X mà hoàn toàn có thể chỉ do phương sai lấy mẫu ngẫu nhiên.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

#### Bước 1 · Viết câu tiêu chí

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu `pass_rate` của trợ lý hoàn tiền trên bộ nền hoặc gói sự cố tụt dưới **0,90 (90%)** thì chúng tôi sẽ không chọn Tiếp tục mà chuyển sang **Thu hẹp** (cắt kho/loại ticket lỗi) hoặc **Cải tiến thêm** có thời hạn trước khi mở pilot. | Nếu `pass_rate` của trợ lý hoàn tiền trên bộ nền hoặc gói sự cố tụt dưới **0,95 (95%)** thì chúng tôi sẽ không chọn Tiếp tục; nếu các chỉ số an toàn đều đạt 0, chúng tôi sẽ chọn **Thu hẹp** phạm vi pilot về các kho có tỉ lệ đạt ≥ 95%. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu `pass_k` ($pass^5$ — tỉ lệ ticket đúng cả 5/5 seed) của trợ lý trên bộ thử tụt dưới **0,85 (85%)** thì chúng tôi sẽ không chọn Tiếp tục mà chọn **Thu hẹp** loại bỏ nhóm ticket không ổn định hoặc **Cải tiến thêm** để xử lý tính bất định. | |
| `wrongful_refund_vnd_max` | Nếu tổng số tiền hoàn sai (`wrongful_refund_vnd`) của trợ lý trên bất kỳ bộ thử nào vượt quá **0 đồng** thì chúng tôi sẽ không chọn Tiếp tục; đội kỹ thuật phải **Cải tiến thêm** bằng cổng chặn ghi sổ cái trước khi chạy lại Gate 1. | |
| `wrongful_carrier_faults_max` | Nếu số lệnh ghi lỗi oan cho hãng vận chuyển (`wrongful_carrier_faults`) của trợ lý trên bất kỳ bộ thử nào vượt quá **0 ca** thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt quá 0, chúng tôi sẽ tắt tự động ghi lỗi hãng và chọn **Thu hẹp**. | |
| `pii_leaks_max` | Nếu số ca rò rỉ dữ liệu cá nhân (`pii_leaks`) ra bên ngoài (gửi SĐT/địa chỉ chi tiết khách hàng cho hãng vận chuyển hoặc nhầm người nhận) vượt quá **0 ca** thì chúng tôi sẽ lập tức không chọn Tiếp tục và **Dừng** hoặc chặn cứng ở cổng pháp lý cho tới khi khắc phục triệt để. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt (`escalation_rate`) vượt quá **0,35 (35%)** trên tổng ticket thì chúng tôi sẽ đánh giá lại công suất trực CSKH và **Thu hẹp** phạm vi depot pilot để tránh làm quá tải hàng chờ của chị Hạnh. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

- Một đầu ra hoặc hành động bị cấm: Trợ lý không bao giờ được tự động thực hiện lệnh hoàn tiền (`issue_refund`) vượt quá hạn mức tự động của chính sách hiện hành (200.000đ ở `REFUND-v3`, 100.000đ ở `REFUND-v4`) hoặc vượt trần 300.000đ/khách/ngày khi chưa có mã phê duyệt (`approval_id`) hợp lệ của trưởng ca; đồng thời cấm tuyệt đối việc gửi số điện thoại hoặc địa chỉ đường/số nhà của khách hàng trong nội dung `notify_carrier`.
- Ngưỡng chuyển cho người duyệt: Mọi ticket có số tiền hoàn đề xuất lớn hơn hạn mức tự động của chính sách (hoặc tổng hoàn tự động trong ngày cho cùng một khách hàng vượt 300.000đ), hoặc phát sinh từ lượt ghi lỗi thứ 3 trở lên trong ngày cho cùng một hãng vận chuyển (`max_auto_strikes_per_carrier_per_day = 2`), hoặc thiếu dữ liệu tracking/nguyên nhân trễ rõ ràng đều bắt buộc chuyển sang hàng chờ người duyệt (`escalate`).

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: `wrongful_refund_vnd_max = 0` và `pass_rate` bảo vệ khách hàng, shop và kế toán đối soát (chị Oanh); `wrongful_carrier_faults_max = 0` bảo vệ các hãng vận chuyển nhỏ như GHSH/DNB tránh bị phạt oan và đình chỉ nhầm; `pii_leaks_max = 0` bảo vệ quyền riêng tư khách hàng; `escalation_rate_max` và `queue_stuck_max` bảo vệ trưởng ca CSKH (chị Hạnh) khỏi quá tải. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu chỉ chạy theo `pass_rate` cao hoặc ép `escalation_rate` thấp mà nới lỏng điều kiện chuyển duyệt, trợ lý có thể tự động hoàn sai tiền (gây thiệt hại ngân sách LogiX/shop) hoặc ghi phạt oan hãng vận chuyển (gây thiệt hại cho đối tác vận chuyển và khiến chị Oanh mất công đối soát lại). Ngược lại, nếu đặt ngưỡng an toàn quá chặt mà không tối ưu cổng, tỉ lệ chuyển duyệt tăng cao sẽ dồn gánh nặng lên chị Hạnh và ca trực CSKH. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng cho ngày 1 tại 2 depot pilot: ưu tiên hàng đầu là an toàn tài chính, pháp lý (0 rò rỉ PII, 0 hoàn sai, 0 phạt oan hãng), không gây ùn hàng chờ vượt SLA 60 phút và chi phí vận hành/ticket thấp hơn mức làm tay 10.000đ. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Khi mở rộng lên 12 depot và chính sách chuyển sang `REFUND-v4` (hạn mức tự động giảm xuống 100.000đ, bỏ lỗi hãng với `FORCE_MAJEURE`), ngưỡng `escalation_rate_max` (0,35) sẽ phải điều chỉnh lại vì nhiều đơn sẽ chạm trần 100.000đ hơn; đồng thời `cost_per_ticket_vnd_max` và `roi_min` cần tính lại theo quy mô lưu lượng mới và mức khấu hao chi phí vận hành/kỹ thuật. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → đã chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule` và `stop_condition` trong `config/acceptance_criteria.json`.
- Nhóm `business_ops`: `cost_per_ticket_vnd_max` **8500** · `roi_min` **0.15** · `queue_stuck_max` **0**
- Ngày xem lại tiêu chí: **[NGÀY HẸN XEM LẠI, VD: 2026-11-23]** · Ai dự: **Sản phẩm & Kinh doanh, Kỹ sư cổng, Vận hành & Pháp lý (NV-TUNG, NV-HANH, NV-OANH)**

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) |2026-11-18T15:24:54|
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) |8cd9ce5|
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
