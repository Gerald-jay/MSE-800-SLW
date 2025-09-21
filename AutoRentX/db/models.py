from peewee import (
    Model, CharField, BlobField, IntegerField, BooleanField, DateTimeField,
    FloatField, AutoField, Check, DateField, ForeignKeyField, TextField
)
from datetime import datetime
from db.db_manager import DatabaseManager

db_manager = DatabaseManager()
db = db_manager.db

class BaseModel(Model):
    class Meta:
        database = db

def create_all_tables():
    db = DatabaseManager().db
    if db.is_closed():
        db.connect(reuse_if_open=True)
    models = [User, Car, AuditLog, PricingRule, CustomerProfile, Booking, Payment]
    db.create_tables(models, safe=True)

class User(BaseModel):
    """用户表 / User table"""
    id = AutoField()
    role = CharField(max_length=20, default="customer")   # customer/admin
    name = CharField(max_length=100)                      # 用户名
    email = CharField(max_length=150, unique=True)        # 邮箱
    password_salt = BlobField()
    password_hash = BlobField()
    iterations = IntegerField()
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)
    
# 统一的可选状态 / Unified status choices
STATUS_AVAILABLE = "available"
STATUS_UNAVAILABLE = "unavailable"
STATUS_MAINTENANCE = "maintenance"
STATUS_RESERVED = "reserved"
STATUS_CHOICES = (STATUS_AVAILABLE, STATUS_UNAVAILABLE, STATUS_MAINTENANCE, STATUS_RESERVED)
class Car(BaseModel):
    """
    车辆实体 / Car entity
    字段对照作业要求：ID, make, model, year, kilometre, available, min_days, max_days, daily_rate
    """
    id = AutoField()                                # 显式主键 / explicit PK
    make = CharField(max_length=50)                 # 品牌 / Make
    model = CharField(max_length=50)                # 车型 / Model
    year = IntegerField()                           # 年份 / Year
    kilometre = IntegerField()                      # 里程 / Kilometre (km)
    daily_rate = FloatField()                       # 日租价 / Daily rate
    # 加 Check 约束（DB 层防呆）/ DB-level CHECK for safety
    status = CharField(
        max_length=20,
        default=STATUS_AVAILABLE,
        constraints=[Check(f"status in ('{STATUS_AVAILABLE}','{STATUS_UNAVAILABLE}','{STATUS_MAINTENANCE}','{STATUS_RESERVED}')")]
    )

# ====== 审计日志 / Audit log ======
class AuditLog(BaseModel):
    """
    审计日志 / Audit log
    actor_user_id: 执行者用户ID
    action: 动作类型（create_pricing_rule / update_pricing_rule / create_profile / update_profile / create_booking 等）
    target_type: 目标对象类型（pricing_rule / profile / booking / car …）
    target_id: 目标对象ID（可为空）
    detail: 详情（文本）
    """
    id = AutoField()
    actor_user_id = IntegerField()
    action = CharField(max_length=50)
    target_type = CharField(max_length=50)
    target_id = IntegerField(null=True)
    detail = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)

# ====== 定价规则 / Pricing rules ======
PRULE_DISCOUNT = "discount"
PRULE_SURCHARGE = "surcharge"
PRULE_TYPES = (PRULE_DISCOUNT, PRULE_SURCHARGE)

AMOUNT_PERCENT = "percent"
AMOUNT_FIXED = "fixed"
AMOUNT_TYPES = (AMOUNT_PERCENT, AMOUNT_FIXED)

class PricingRule(BaseModel):
    """
    配置化定价：基础日租价 + 规则（折扣/附加）/ Configurable pricing: base daily rate + rules (discount/surcharge)
    作用范围：global 或指定 car_id / scope: global or specific car_id
    规则类型：折扣/附加 / rule type: discount/surcharge
    条件：min_days（满足则生效），有效期可选（生效时间区间）/ conditions: min_days (trigger if met), optional validity period (start/end date)
    """
    id = AutoField()
    name = CharField(max_length=80)
    rule_type = CharField(max_length=20, constraints=[Check(f"rule_type in ('{PRULE_DISCOUNT}','{PRULE_SURCHARGE}')")])
    amount_type = CharField(max_length=20, constraints=[Check(f"amount_type in ('{AMOUNT_PERCENT}','{AMOUNT_FIXED}')")])
    amount_value = FloatField()  # percent: 10=10%；fixed：金额
    scope = CharField(max_length=20, default="global")  # "global" or "car"
    min_days = IntegerField(default=1)  # 满足最小租期触发
    start_date = DateField(null=True)
    end_date = DateField(null=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now)

# ====== 客户档案 / Customer profile ======
class CustomerProfile(BaseModel):
    """
    客户档案（与 User 一对一） / Customer profile (one-to-one with User)
    """
    id = AutoField()
    user = ForeignKeyField(User, unique=True, backref='profile', on_delete='CASCADE')
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    phone = CharField(max_length=30)
    id_document = CharField(max_length=100)  # 驾照/身份证明编号或摘要 / Driver's license/ID document number or summary
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

# ====== 预订（扩展：pending + 用户信息快照） / Bookings (extended: pending + user info snapshot) ======
BOOKING_PENDING   = "pending"
BOOKING_CONFIRMED = "confirmed"
BOOKING_CANCELLED = "cancelled"
BOOKING_COMPLETED = "completed"
BOOKING_STATUS_CHOICES = (BOOKING_PENDING, BOOKING_CONFIRMED, BOOKING_CANCELLED, BOOKING_COMPLETED)

class Booking(BaseModel):
    id = AutoField()
    car = ForeignKeyField(Car, backref="bookings", on_delete="CASCADE")
    user = ForeignKeyField(User, backref="bookings", on_delete="CASCADE")
    start_date = DateField()
    end_date = DateField()
    status = CharField(
        max_length=20,
        default=BOOKING_PENDING,
        constraints=[Check(
            f"status in ('{BOOKING_PENDING}','{BOOKING_CONFIRMED}','{BOOKING_CANCELLED}','{BOOKING_COMPLETED}')"
        )]
    )
    # 费用快照 / cost snapshot
    days = IntegerField(default=1)
    base_daily_rate = FloatField(default=0)
    base_cost = FloatField(default=0)
    adj_total = FloatField(default=0)     # 调整总和（折扣为负，附加为正） / adjustments total (discount negative, surcharge positive)
    grand_total = FloatField(default=0)   # 最终总价 / final total price

    # 客户信息快照（下单时固化）/ user info snapshot (captured at booking time)
    snap_first_name = CharField(max_length=50)
    snap_last_name = CharField(max_length=50)
    snap_phone = CharField(max_length=30)
    snap_id_document = CharField(max_length=100)

    created_at = DateTimeField(default=datetime.now)

class Payment(BaseModel):
    id = AutoField()
    booking = ForeignKeyField(Booking, backref="payments", on_delete="CASCADE")
    method = CharField(max_length=30)
    amount = FloatField()
    currency = CharField(max_length=10, default="NZD")
    ok = BooleanField(default=False)
    message = TextField(null=True)
    txn_id = CharField(max_length=64, null=True)
    created_at = DateTimeField(default=datetime.now)