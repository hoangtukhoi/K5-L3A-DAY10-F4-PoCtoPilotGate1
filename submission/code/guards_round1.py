"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _truth(ctx, order_id):
    """Nguồn sự thật từ DB (không đọc chữ khách): (order, policy, parcel trễ nhất, số ngày trễ theo tracking, nguyên nhân)."""
    order = ctx.tools.lookup_order(order_id)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if not order or not order.get("parcels") or policy is None:
        return None
    worst = max(order["parcels"], key=lambda p: H.db_delay_days(p, ctx.as_of))
    delay = H.db_delay_days(worst, ctx.as_of)
    cause = worst.get("delay_cause") or ("CARRIER" if delay > 0 else None)
    return order, policy, worst, delay, cause


def pre_guard(ctx):
    # Cổng 3 (kỹ thuật, drift chính sách): ghim phiên bản chính sách đang hiệu lực theo ngày, không tin cờ index_active.
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is not None:
        return Verdict.allow(policy_id=policy["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")

    if tool == "issue_refund":
        # Cổng 1: số tiền hoàn phải khớp quyền lợi tính từ DB + chính sách hiệu lực, người chi là LOGIX, không ghi trùng.
        truth = _truth(ctx, action.get("order_id"))
        if truth is None:
            return Verdict.escalate("thiếu dữ liệu đơn hoặc chính sách hiệu lực, chuyển người duyệt")
        order, policy, _worst, delay, cause = truth
        if action.get("payer", "LOGIX") != "LOGIX":
            return Verdict.escalate("khoản hoàn không do LogiX chi trả (shop/bên khác), chuyển người duyệt")
        if ctx.tools.ledger_rows(order_id=order["order_id"], ticket_id=action.get("ticket_id")):
            return Verdict.deny("ticket này đã có dòng hoàn cho đơn, chặn ghi trùng")
        entitled = H.entitlement_vnd(policy, order, delay, cause)
        amount = int(action.get("amount_vnd", 0))
        if entitled <= 0:
            return Verdict.deny("tracking DB: đơn chưa đủ điều kiện hoàn theo chính sách hiệu lực")
        if amount != entitled:
            return Verdict.modify("số tiền khác quyền lợi tính từ DB, sửa về quyền lợi", amount_vnd=entitled)

    if tool == "file_carrier_fault":
        # Cổng 2: chỉ ghi lỗi hãng khi DB xác nhận trễ thật và có nguyên nhân thuộc danh sách của chính sách;
        # ghi đúng kiện trễ nhất theo DB (không phải kiện đầu tiên) và số ngày theo tracking.
        truth = _truth(ctx, action.get("order_id"))
        if truth is None:
            return Verdict.deny("thiếu dữ liệu đơn hoặc chính sách hiệu lực, không ghi lỗi hãng")
        _order, policy, worst, delay, _cause = truth
        if not H.carrier_at_fault(policy, worst, delay):
            return Verdict.deny("tracking DB: không đủ ngày trễ hoặc nguyên nhân không thuộc hãng, không ghi lỗi hãng")
        fixes = {}
        if action.get("parcel_id") != worst["parcel_id"]:
            fixes.update(parcel_id=worst["parcel_id"], carrier_id=worst["carrier_id"], driver_id=worst.get("driver_id"))
        if action.get("delay_days") != delay:
            fixes["delay_days"] = delay
        if fixes:
            return Verdict.modify("sửa theo kiện trễ nhất và số ngày trong tracking DB", **fixes)

    return Verdict.allow()
