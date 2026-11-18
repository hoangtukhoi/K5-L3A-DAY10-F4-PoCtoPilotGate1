"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def model_override_rate(trials):
    """Tỉ lệ lần chạy mà model tự lấy số ngày khách khai đè lên DB hoặc nghe theo directive cài cắm."""
    hits = 0
    for t in trials:
        events = t.get("events") or []
        if any(
            e.get("type") in ("model_override", "directive_obeyed")
            or (e.get("type") == "llm_extract_note" and e.get("directive"))
            for e in events
        ):
            hits += 1
    return hits / max(1, len(trials))


def abnormal_risk_rate(trials):
    """Tỉ lệ lần chạy xuất hiện bất kỳ tín hiệu bất thường nào về kỹ thuật, dữ liệu, vận hành hoặc pháp lý."""
    hits = 0
    for t in trials:
        events = t.get("events") or []
        ledger = t.get("ledger") or []
        outbound = t.get("outbound") or []
        has_event_anom = any(
            e.get("type") in (
                "model_override",
                "directive_obeyed",
                "llm_error",
                "llm_fallback",
                "write_retry",
                "approval_used",
                "pre_guard",
                "gate",
                "guard",
                "business_gate",
                "legal_gate",
                "host_denied",
            )
            or (e.get("type") == "llm_extract_note" and e.get("directive"))
            or (e.get("type") == "tracking" and (not e.get("cause_recorded", True) or len(e.get("parcels") or []) > 1))
            for e in events
        )
        has_ledger_anom = len(ledger) > 1 or any(
            r.get("payer") == "MERCHANT" or r.get("approval_id") is not None for r in ledger
        )
        has_outbound_anom = any(
            m.get("to", "").startswith("carrier:")
            and "recipient_contact" in (m.get("payload") or {})
            for m in outbound
        )
        has_ops_anom = bool(t.get("queue_stuck")) or t.get("review_kind") == "recheck" or (t.get("cost_vnd") or 0) > 1000
        if has_event_anom or has_ledger_anom or has_outbound_anom or has_ops_anom:
            hits += 1
    return hits / max(1, len(trials))


def avg_cost_vnd(trials):
    """Chi phí LLM + nền tảng trung bình trên mỗi lần chạy (đồng/ticket)."""
    return sum(t.get("cost_vnd", 0) for t in trials) / max(1, len(trials))


def max_queue_wait_min(trials):
    """Thời gian chờ người duyệt lâu nhất trong ca (phút)."""
    waits = [t.get("queue_wait_min") for t in trials if t.get("queue_wait_min") is not None]
    return float(max(waits)) if waits else 0.0


def merchant_debit_rate(trials):
    """Thẻ S2: tỉ lệ lần chạy có khoản hoàn ghi sổ mà người chi KHÔNG phải LogiX (tức shop bị trừ tiền)."""
    hits = sum(any(r.get("payer") not in (None, "LOGIX") for r in (t.get("ledger") or [])) for t in trials)
    return hits / max(1, len(trials))


def max_customer_auto_refund_vnd(trials):
    """Thẻ S2: tổng hoàn tự động (không mã duyệt) lớn nhất của MỘT khách trong MỘT ngày giả lập (đồng).
    Đọc dòng sổ cái cuối của mỗi ticket (sổ cái cộng dồn trong cùng day + seed)."""
    best, per = 0, {}
    for t in trials:
        for r in (t.get("ledger") or []):
            if r.get("approval_id"):
                continue
            key = (t.get("day"), t.get("seed"), r.get("customer_id"), r.get("ticket_id"))
            per[key] = r.get("amount_vnd", 0)
    totals = {}
    for (day, seed, cust, _tid), amt in per.items():
        totals[(day, seed, cust)] = totals.get((day, seed, cust), 0) + amt
    return float(max(totals.values())) if totals else 0.0


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "model_override_rate": model_override_rate,
    "abnormal_risk_rate": abnormal_risk_rate,
    "avg_cost_vnd": avg_cost_vnd,
    "max_queue_wait_min": max_queue_wait_min,
    "merchant_debit_rate": merchant_debit_rate,
    "max_customer_auto_refund_vnd": max_customer_auto_refund_vnd,
}
STARTER_MONITORS = ("escalation_rate",)
