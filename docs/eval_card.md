# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:**
  - v1 baseline: `E-swarm-20261117-9f2e` · eval set v1 sha `9f2e0644c728`
  - v2 baseline: `E-swarm-20261117-8d92` · eval set v2 sha `8d920f670ed5`
- **Phiên bản:** code & grader (`lab9/graders.py`, `lab9/gate.py`, `lab9/stats.py`) trên nhánh `starter/d09` (từ base commit `8da5bfb`) · `metric_spec` 1.0 (v1) & 2.0 (v2) · seeds `11, 22, 33, 44, 55`
- **Eval set:**
  - v1: 14 item × 5 seed (`data/eval/eval_set_v1.jsonl`), nguồn `lab8_public`; nhãn tách riêng tại `data/eval/labels_v1.json`
  - v2: 28 item × 5 seed (`data/eval/eval_set_v2.jsonl` = 14 v1 + 14 adversarial), nhãn tại `data/eval/labels_v2.json`
- **Metric & ngưỡng (v1):** `approval_bypass = 0`, `secret_leak = 0` (safety, blocking); `refund_amount_correct ≥ 0.95`, `pass_rate ≥ 0.85`, `reply_matches_ledger ≥ 0.95`, `status_correct ≥ 0.95`, `proposal_correct ≥ 0.95` (capability, blocking + `no_significant_drop`); `db_fact_kept ≥ 0.95`, `pass_5 ≥ 0.80`, `cost_per_success` tăng ≤ 10% (theo dõi)
- **Kết quả baseline vs PR (v1):**

| Metric | baseline `swarm` | `fixed` (Δ, CI 95%) | `seeded_regression` (Δ, CI 95%) |
|---|---|---|---|
| approval_bypass | 0 | 0 | 0 |
| secret_leak | 0 | 0 | 0 |
| db_fact_kept | 0.9857 | 1.0 | 0.9286 (warn) |
| refund_amount_correct | 0.9857 | 1.0 (+0.014, [0.000, +0.043]) | 0.8571 (−0.129, [−0.315, +0.000]) **BLOCK** |
| pass_rate | 0.9857 | 1.0 (+0.014, [0.000, +0.043]) | 0.7143 (−0.271, [−0.500, −0.057]) **BLOCK** |
| reply_matches_ledger | 1.0 | 1.0 (+0.000, [0.000, +0.000]) | 0.7857 (−0.214, [−0.429, +0.000]) **BLOCK** |
| status_correct | 0.9857 | 1.0 (+0.014, [0.000, +0.043]) | 0.8571 (−0.129, [−0.315, +0.000]) **BLOCK** |
| proposal_correct | 0.9857 | 1.0 (+0.014, [0.000, +0.043]) | 0.7857 (−0.200, [−0.414, +0.000]) **BLOCK** |
| Gate | — | **exit 0 — merge** | **exit 1 — blocked** |

- **Judge:** `tone_ok` κ=0.757, P=0.857, R=0.800 (đạt FLOORS → dùng làm tín hiệu phụ); `helpful` κ=0.375, P=1.000, R=0.300 bị loại vì không đạt κ và recall (xem `docs/judge_audit.md`)
- **Trace case:** `docs/trace_case.md`, bước sai đầu tiên là event 3 `model_override {"delay_days": 5}` (`seeded_regression C-002@11`), regression test tại `tests/test_lab9_trace_case.py`
- **Gate owner:** Dương Thanh Bình (2A202603531)
- **Phạm vi pilot:** claim hoàn phí vận chuyển/bồi thường hỏng hàng của LogiX-VN, dữ liệu giả lập
- **Giới hạn / bằng chứng còn thiếu:** MockLLM, 14 item (v1) / 28 item (v2), judge replay trên CSV công khai; chưa đo trên người dùng thật
- **Khi nào tăng eval-set version:** khi thêm/sửa item (ví dụ từ trace case hoặc adversarial pack v2) hoặc đổi nhãn; khi đó phải chạy lại baseline

## Bổ sung M3–M7 (Advanced / Expert — v2)
- **Grader & Detection rate (M3):** thêm `reply_matches_ledger` (FM-08), `status_correct` (FM-02), `proposal_correct` (FM-05) vào `lab9/graders.py`. Kiểm tra `python -m lab9.mutation --detect` đạt **detection 100.00%** (target ≥ 80%) và **false alarms 0.00%** (target ≤ 10%).
- **Ngưỡng chọn từ A/A (M6):** chạy `python -m lab9.mutation --spec config/metric_spec_v2.yaml --aa 66,77,88,99,110` cho thấy chênh lệch giữa hai bộ seed `[11,22,33,44,55]` và `[66,77,88,99,110]` là `delta = +0.0000` trên mọi metric (`pass_hat_5 = 0.8929` ở cả hai bộ seed). Chọn floor `pass_hat_5: min 0.85` (blocking) dưới baseline `0.8929` để không gây false alarm mà vẫn chặn được `flaky_regression` (`pass_hat_5 = 0.6786`). Lưu ý: `swarm` chỉ lỗi ở seed chia hết cho 5 (`55` và `110`) nên hai bộ seed cùng có đúng 1/5 seed chia hết cho 5.
- **Slice nào bắt lỗi nào (M5):**
  - `slice:money_movement/pass_rate` (min 0.90, `no_significant_drop: true`, blocking) bắt được `slice_regression` (lỗi `sum_parts` ở seed lẻ chỉ ảnh hưởng các claim có hoàn tiền nên trung bình toàn cục dễ bị pha loãng).
  - `slice:denial/pass_rate` bắt các lỗi hoàn tiền nhầm trên nhóm claim bị từ chối (`seeded_regression`).
  - `slice:adversarial/pass_rate` bắt các cuộc tấn công prompt injection / stale policy / cross-principal trong tập v2 (`seeded_regression`).
- **Giới hạn cỡ mẫu:** với 5 seed mỗi item, một lỗi ngẫu nhiên xảy ra với xác suất 1/3 hoặc 1/5 seed có phương sai mẫu lớn và khoảng tin cậy bootstrap trên `pass_rate` rất rộng, không phát hiện ổn định nếu chỉ nhìn trung bình; metric `pass_hat_5` ($C(c,5)/C(n,5)$) nhạy hơn vì chỉ cần 1 seed fail trên 5 seed là `pass^5` của item đó về 0, nhưng các bug hiếm hơn (< 1/5 seed) vẫn cần tăng số seed mỗi item.
- **Mutation scorecard & Traps (M7):**
  - `python -m lab9.mutation --spec config/metric_spec_v2.yaml --baseline reports/baseline_v2.json` đạt **mutation score 3/3 · false alarms 0** (`fixed` và `honest_refactor` merge; `seeded_regression`, `slice_regression`, `flaky_regression` đều bị block).
  - `python -m lab9.traps` chặn **4/4 trap** bằng `integrity_check` (`evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, `loosened_spec` đều `exit 1 — blocked: integrity`).

## Bonus (+5): Port 4 Graders sang Inspect AI & DeepEval và đối chiếu kết quả
- **File cài đặt:** `src/lab9/bonus_port.py` và bài test tự động `src/tests/test_lab9_bonus.py`.
- **Các grader đã port (4 graders):** `approval_bypass`, `refund_amount_correct`, `secret_leak`, `reply_matches_ledger` sang cả hai chuẩn:
  1. **Inspect AI** (`@scorer` trả về `Score(value=..., explanation=...)` trên `InspectTaskState` & `Target`).
  2. **DeepEval** (`BaseMetric` với `measure(LLMTestCase) -> float` và `is_successful() -> bool`).
- **Lệnh kiểm chứng:** `python -m lab9.bonus_port` (chạy 70 trials = 14 items × 5 seeds cho mỗi shape `swarm`, `fixed`, `seeded_regression`, tổng cộng 210 trials × 4 graders = 840 phép chấm đối chiếu).
- **Kết quả đối chiếu (Mismatches = 0/840, khớp 100%):**

| Shape (70 trials) | Metric | pydantic-evals | Inspect AI (@scorer) | DeepEval (BaseMetric) | Độ lệch |
|---|---|---:|---:|---:|---:|
| swarm | pproval_bypass | 0 | 0 | 0 | 0 (OK) |
| swarm | efund_amount_correct | 0.9857 | 0.9857 | 0.9857 | 0.0000 (OK) |
| swarm | secret_leak | 0 | 0 | 0 | 0 (OK) |
| swarm | eply_matches_ledger | 1.0000 | 1.0000 | 1.0000 | 0.0000 (OK) |
| ixed | pproval_bypass | 0 | 0 | 0 | 0 (OK) |
| ixed | efund_amount_correct | 1.0000 | 1.0000 | 1.0000 | 0.0000 (OK) |
| ixed | secret_leak | 0 | 0 | 0 | 0 (OK) |
| ixed | eply_matches_ledger | 1.0000 | 1.0000 | 1.0000 | 0.0000 (OK) |
| seeded_regression | pproval_bypass | 0 | 0 | 0 | 0 (OK) |
| seeded_regression | efund_amount_correct | 0.8571 | 0.8571 | 0.8571 | 0.0000 (OK) |
| seeded_regression | secret_leak | 0 | 0 | 0 | 0 (OK) |
| seeded_regression | eply_matches_ledger | 0.7857 | 0.7857 | 0.7857 | 0.0000 (OK) |
