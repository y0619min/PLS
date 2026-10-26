import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import datetime
from collections import defaultdict

# ==================== 数据管理模块 ====================

DATA_FILE = "records.json"  # 数据持久化文件路径


def load_records():
    """
    从JSON文件中加载收支记录
    返回：记录列表，如果文件不存在则返回空列表
    """
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_records(records):
    """
    将收支记录保存到JSON文件
    参数：records - 收支记录列表
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except IOError as e:
        messagebox.showerror("保存失败", f"数据保存失败：{e}")


# ==================== 主应用类 ====================

class AccountingApp:
    """
    个人收支记账系统主应用类
    负责创建图形界面和管理所有功能模块
    """

    def __init__(self, root):
        """
        初始化应用程序
        参数：root - tkinter根窗口
        """
        self.root = root
        self.root.title("💰 个人收支记账系统")
        self.root.geometry("1000x650")
        self.root.minsize(800, 550)
        self.root.configure(bg="#f0f4f8")

        # 加载数据
        self.records = load_records()

        # 颜色主题
        self.colors = {
            "primary": "#2196F3",
            "success": "#4CAF50",
            "danger": "#F44336",
            "warning": "#FF9800",
            "info": "#00BCD4",
            "dark": "#263238",
            "light": "#ECEFF1",
            "income": "#4CAF50",
            "expense": "#F44336",
            "bg": "#f0f4f8",
            "card": "#ffffff",
        }

        # 构建界面
        self._build_ui()

        # 刷新数据
        self.refresh_table()
        self.refresh_summary()

    def _build_ui(self):
        """构建主界面"""
        # ---- 顶部标题栏 ----
        header = tk.Frame(self.root, bg=self.colors["primary"], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="💰  个人收支记账系统",
            font=("微软雅黑", 18, "bold"),
            fg="white",
            bg=self.colors["primary"],
        ).pack(side=tk.LEFT, padx=20, pady=10)

        # 当前日期
        now = datetime.datetime.now().strftime("%Y年%m月%d日  %A")
        tk.Label(
            header,
            text=now,
            font=("微软雅黑", 10),
            fg="#BBDEFB",
            bg=self.colors["primary"],
        ).pack(side=tk.RIGHT, padx=20)

        # ---- 主体区域 ----
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧：功能面板 + 汇总卡片
        left_frame = tk.Frame(main_frame, bg=self.colors["bg"], width=280)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        # 汇总卡片
        self._build_summary_panel(left_frame)

        # 功能按钮
        self._build_button_panel(left_frame)

        # 右侧：记录表格
        right_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_table_panel(right_frame)

    def _build_summary_panel(self, parent):
        """构建汇总统计面板"""
        card = tk.Frame(parent, bg=self.colors["card"], relief=tk.FLAT, bd=0)
        card.pack(fill=tk.X, pady=(0, 10))

        # 标题
        tk.Label(
            card,
            text="📊  本月概览",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors["card"],
            fg=self.colors["dark"],
        ).pack(anchor=tk.W, padx=12, pady=(10, 5))

        ttk.Separator(card, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=12)

        # 收入
        income_frame = tk.Frame(card, bg=self.colors["card"])
        income_frame.pack(fill=tk.X, padx=12, pady=5)
        tk.Label(
            income_frame, text="💚 总收入", font=("微软雅黑", 9),
            bg=self.colors["card"], fg="#666"
        ).pack(side=tk.LEFT)
        self.lbl_income = tk.Label(
            income_frame, text="¥ 0.00", font=("微软雅黑", 11, "bold"),
            bg=self.colors["card"], fg=self.colors["income"]
        )
        self.lbl_income.pack(side=tk.RIGHT)

        # 支出
        expense_frame = tk.Frame(card, bg=self.colors["card"])
        expense_frame.pack(fill=tk.X, padx=12, pady=5)
        tk.Label(
            expense_frame, text="❤️ 总支出", font=("微软雅黑", 9),
            bg=self.colors["card"], fg="#666"
        ).pack(side=tk.LEFT)
        self.lbl_expense = tk.Label(
            expense_frame, text="¥ 0.00", font=("微软雅黑", 11, "bold"),
            bg=self.colors["card"], fg=self.colors["expense"]
        )
        self.lbl_expense.pack(side=tk.RIGHT)

        # 结余
        balance_frame = tk.Frame(card, bg="#E3F2FD")
        balance_frame.pack(fill=tk.X, padx=12, pady=(5, 12))
        tk.Label(
            balance_frame, text="💰 结余", font=("微软雅黑", 9, "bold"),
            bg="#E3F2FD", fg="#1565C0"
        ).pack(side=tk.LEFT, padx=5, pady=5)
        self.lbl_balance = tk.Label(
            balance_frame, text="¥ 0.00", font=("微软雅黑", 13, "bold"),
            bg="#E3F2FD", fg="#1565C0"
        )
        self.lbl_balance.pack(side=tk.RIGHT, padx=5)

    def _build_button_panel(self, parent):
        """构建功能按钮面板"""
        card = tk.Frame(parent, bg=self.colors["card"])
        card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            card, text="⚙️  功能操作",
            font=("微软雅黑", 11, "bold"),
            bg=self.colors["card"], fg=self.colors["dark"]
        ).pack(anchor=tk.W, padx=12, pady=(10, 5))

        ttk.Separator(card, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=12)

        btn_config = [
            ("➕  添加收入", self.colors["income"], self.add_income),
            ("➖  添加支出", self.colors["expense"], self.add_expense),
            ("✏️  修改记录", self.colors["warning"], self.edit_record),
            ("🗑️  删除记录", "#9E9E9E", self.delete_record),
            ("🔍  查询/筛选", self.colors["primary"], self.search_dialog),
            ("📊  统计分析", self.colors["info"], self.statistics_dialog),
            ("🔄  显示全部", "#607D8B", self.refresh_all),
        ]

        for text, color, cmd in btn_config:
            btn = tk.Button(
                card, text=text, command=cmd,
                font=("微软雅黑", 10), bg=color, fg="white",
                relief=tk.FLAT, bd=0, cursor="hand2",
                activebackground=color, activeforeground="white",
                padx=10, pady=7,
            )
            btn.pack(fill=tk.X, padx=12, pady=3)

        tk.Frame(card, bg=self.colors["card"], height=10).pack()

    def _build_table_panel(self, parent):
        """构建记录表格面板"""
        # 表格标题栏
        title_frame = tk.Frame(parent, bg=self.colors["card"])
        title_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(
            title_frame, text="📋  收支明细",
            font=("微软雅黑", 12, "bold"),
            bg=self.colors["card"], fg=self.colors["dark"]
        ).pack(side=tk.LEFT, padx=12, pady=8)

        # 搜索框
        search_frame = tk.Frame(title_frame, bg=self.colors["card"])
        search_frame.pack(side=tk.RIGHT, padx=12, pady=5)
        tk.Label(search_frame, text="🔎", bg=self.colors["card"], font=("微软雅黑", 10)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var,
            font=("微软雅黑", 10), width=20,
            relief=tk.FLAT, bd=1, highlightthickness=1,
            highlightcolor=self.colors["primary"],
        )
        search_entry.pack(side=tk.LEFT, padx=5)

        # 表格
        table_frame = tk.Frame(parent, bg=self.colors["bg"])
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "date", "type", "category", "amount", "note")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            selectmode="browse"
        )

        # 表头
        headers = {
            "id": ("序号", 50),
            "date": ("日期", 110),
            "type": ("类型", 70),
            "category": ("分类", 100),
            "amount": ("金额(元)", 100),
            "note": ("备注", 220),
        }
        for col, (text, width) in headers.items():
            self.tree.heading(col, text=text, anchor=tk.CENTER)
            self.tree.column(col, width=width, anchor=tk.CENTER)

        # 样式
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            rowheight=28,
            font=("微软雅黑", 9),
            fieldbackground=self.colors["card"],
            background=self.colors["card"],
        )
        style.configure(
            "Treeview.Heading",
            font=("微软雅黑", 10, "bold"),
            background=self.colors["primary"],
            foreground="white",
        )
        style.map("Treeview", background=[("selected", "#BBDEFB")])

        # 颜色标签
        self.tree.tag_configure("income", foreground=self.colors["income"])
        self.tree.tag_configure("expense", foreground=self.colors["expense"])
        self.tree.tag_configure("even", background="#F5F5F5")
        self.tree.tag_configure("odd", background="#FFFFFF")

        # 滚动条
        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 双击编辑
        self.tree.bind("<Double-1>", lambda e: self.edit_record())

        # 底部状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = tk.Label(
            parent, textvariable=self.status_var,
            font=("微软雅黑", 9), fg="#666",
            bg="#ECEFF1", anchor=tk.W
        )
        status_bar.pack(fill=tk.X, pady=(5, 0))

    # ==================== 核心功能 ====================

    def add_income(self):
        """添加收入记录"""
        self._open_record_dialog(record_type="收入")

    def add_expense(self):
        """添加支出记录"""
        self._open_record_dialog(record_type="支出")

    def _open_record_dialog(self, record_type="收入", edit_data=None):
        """
        打开添加/编辑记录对话框
        参数：
            record_type - 记录类型（收入/支出）
            edit_data - 编辑时传入原记录字典
        """
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{'修改' if edit_data else '添加'}{record_type}记录")
        dialog.geometry("420x380")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(bg=self.colors["card"])
        dialog.transient(self.root)

        # 标题
        color = self.colors["income"] if record_type == "收入" else self.colors["expense"]
        tk.Frame(dialog, bg=color, height=5).pack(fill=tk.X)
        tk.Label(
            dialog,
            text=f"{'修改' if edit_data else '➕ 添加'}{record_type}",
            font=("微软雅黑", 14, "bold"),
            bg=self.colors["card"], fg=color
        ).pack(pady=(15, 5))

        # 表单
        form = tk.Frame(dialog, bg=self.colors["card"])
        form.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

        labels = ["日期（YYYY-MM-DD）", "金额（元）", "分类", "备注"]
        entries = {}

        # 分类选项
        income_cats = ["工资", "兼职", "奖金", "理财", "其他收入"]
        expense_cats = ["餐饮", "交通", "购物", "娱乐", "医疗", "教育", "住房", "其他支出"]
        cats = income_cats if record_type == "收入" else expense_cats

        for i, label_text in enumerate(labels):
            tk.Label(
                form, text=label_text,
                font=("微软雅黑", 10), bg=self.colors["card"], fg="#444"
            ).grid(row=i, column=0, sticky=tk.W, pady=6)

            if label_text == "分类":
                var = tk.StringVar(value=edit_data["category"] if edit_data else cats[0])
                widget = ttk.Combobox(
                    form, textvariable=var, values=cats,
                    state="readonly", font=("微软雅黑", 10), width=22
                )
            elif label_text == "备注":
                var = tk.StringVar(value=edit_data.get("note", "") if edit_data else "")
                widget = tk.Entry(
                    form, textvariable=var, font=("微软雅黑", 10),
                    relief=tk.FLAT, bd=1, highlightthickness=1, width=24
                )
            elif label_text == "日期（YYYY-MM-DD）":
                default_date = edit_data["date"] if edit_data else datetime.date.today().strftime("%Y-%m-%d")
                var = tk.StringVar(value=default_date)
                widget = tk.Entry(
                    form, textvariable=var, font=("微软雅黑", 10),
                    relief=tk.FLAT, bd=1, highlightthickness=1, width=24
                )
            else:  # 金额
                var = tk.StringVar(value=str(edit_data["amount"]) if edit_data else "")
                widget = tk.Entry(
                    form, textvariable=var, font=("微软雅黑", 10),
                    relief=tk.FLAT, bd=1, highlightthickness=1, width=24
                )

            widget.grid(row=i, column=1, sticky=tk.EW, padx=(10, 0), pady=6)
            entries[label_text] = var

        form.columnconfigure(1, weight=1)

        # 按钮
        btn_frame = tk.Frame(dialog, bg=self.colors["card"])
        btn_frame.pack(pady=15)

        def on_confirm():
            # 输入验证
            date_str = entries["日期（YYYY-MM-DD）"].get().strip()
            amount_str = entries["金额（元）"].get().strip()
            category = entries["分类"].get().strip()
            note = entries["备注"].get().strip()

            # 验证日期
            try:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("输入错误", "日期格式不正确，请输入 YYYY-MM-DD 格式！", parent=dialog)
                return

            # 验证金额
            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("输入错误", "金额必须是大于0的数字！", parent=dialog)
                return

            if not category:
                messagebox.showerror("输入错误", "请选择分类！", parent=dialog)
                return

            # 构建记录
            record = {
                "date": date_str,
                "type": record_type,
                "category": category,
                "amount": round(amount, 2),
                "note": note,
            }

            if edit_data:
                # 修改记录
                idx = edit_data["_idx"]
                self.records[idx].update(record)
                self.status_var.set(f"✅ 已修改记录（{date_str}  {record_type} ¥{amount:.2f}）")
            else:
                # 添加记录
                self.records.append(record)
                self.status_var.set(f"✅ 已添加{record_type}记录（{date_str}  ¥{amount:.2f}）")

            save_records(self.records)
            self.refresh_table()
            self.refresh_summary()
            dialog.destroy()

        tk.Button(
            btn_frame, text="  确定  ", command=on_confirm,
            font=("微软雅黑", 11, "bold"), bg=color, fg="white",
            relief=tk.FLAT, bd=0, cursor="hand2",
            padx=20, pady=6
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame, text="  取消  ", command=dialog.destroy,
            font=("微软雅黑", 11), bg="#9E9E9E", fg="white",
            relief=tk.FLAT, bd=0, cursor="hand2",
            padx=20, pady=6
        ).pack(side=tk.LEFT, padx=10)

    def edit_record(self):
        """编辑选中的记录"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选中要修改的记录！")
            return

        item = self.tree.item(selection[0])
        row_idx = int(item["values"][0]) - 1  # 序号转为索引

        # 根据当前显示的记录找到原始索引
        visible_records = self._get_filtered_records()
        if row_idx >= len(visible_records):
            return

        record = visible_records[row_idx]
        orig_idx = self.records.index(record)
        edit_data = {**record, "_idx": orig_idx}
        self._open_record_dialog(record_type=record["type"], edit_data=edit_data)

    def delete_record(self):
        """删除选中的记录"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选中要删除的记录！")
            return

        item = self.tree.item(selection[0])
        row_idx = int(item["values"][0]) - 1

        visible_records = self._get_filtered_records()
        if row_idx >= len(visible_records):
            return

        record = visible_records[row_idx]
        confirm = messagebox.askyesno(
            "确认删除",
            f"确定要删除以下记录吗？\n\n"
            f"日期：{record['date']}\n"
            f"类型：{record['type']}\n"
            f"金额：¥{record['amount']:.2f}\n"
            f"备注：{record.get('note', '')}"
        )
        if confirm:
            self.records.remove(record)
            save_records(self.records)
            self.refresh_table()
            self.refresh_summary()
            self.status_var.set(f"🗑️ 已删除记录（{record['date']}  {record['type']} ¥{record['amount']:.2f}）")

    def search_dialog(self):
        """打开查询/筛选对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔍 查询/筛选记录")
        dialog.geometry("400x320")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(bg=self.colors["card"])
        dialog.transient(self.root)

        tk.Frame(dialog, bg=self.colors["primary"], height=5).pack(fill=tk.X)
        tk.Label(
            dialog, text="🔍 查询筛选",
            font=("微软雅黑", 14, "bold"),
            bg=self.colors["card"], fg=self.colors["primary"]
        ).pack(pady=(15, 5))

        form = tk.Frame(dialog, bg=self.colors["card"])
        form.pack(fill=tk.BOTH, padx=25, pady=10)

        # 类型
        tk.Label(form, text="记录类型：", font=("微软雅黑", 10), bg=self.colors["card"]).grid(row=0, column=0, sticky=tk.W, pady=6)
        type_var = tk.StringVar(value="全部")
        ttk.Combobox(
            form, textvariable=type_var,
            values=["全部", "收入", "支出"],
            state="readonly", font=("微软雅黑", 10), width=18
        ).grid(row=0, column=1, sticky=tk.EW, padx=10, pady=6)

        # 开始日期
        tk.Label(form, text="开始日期：", font=("微软雅黑", 10), bg=self.colors["card"]).grid(row=1, column=0, sticky=tk.W, pady=6)
        start_var = tk.StringVar()
        tk.Entry(form, textvariable=start_var, font=("微软雅黑", 10), width=20).grid(row=1, column=1, sticky=tk.EW, padx=10, pady=6)

        # 结束日期
        tk.Label(form, text="结束日期：", font=("微软雅黑", 10), bg=self.colors["card"]).grid(row=2, column=0, sticky=tk.W, pady=6)
        end_var = tk.StringVar()
        tk.Entry(form, textvariable=end_var, font=("微软雅黑", 10), width=20).grid(row=2, column=1, sticky=tk.EW, padx=10, pady=6)

        # 分类
        all_cats = ["全部", "工资", "兼职", "奖金", "理财", "其他收入",
                    "餐饮", "交通", "购物", "娱乐", "医疗", "教育", "住房", "其他支出"]
        tk.Label(form, text="分类：", font=("微软雅黑", 10), bg=self.colors["card"]).grid(row=3, column=0, sticky=tk.W, pady=6)
        cat_var = tk.StringVar(value="全部")
        ttk.Combobox(
            form, textvariable=cat_var,
            values=all_cats,
            state="readonly", font=("微软雅黑", 10), width=18
        ).grid(row=3, column=1, sticky=tk.EW, padx=10, pady=6)

        form.columnconfigure(1, weight=1)

        def on_search():
            type_filter = type_var.get()
            start_filter = start_var.get().strip()
            end_filter = end_var.get().strip()
            cat_filter = cat_var.get()

            filtered = []
            for r in self.records:
                if type_filter != "全部" and r["type"] != type_filter:
                    continue
                if start_filter:
                    try:
                        if r["date"] < start_filter:
                            continue
                    except Exception:
                        pass
                if end_filter:
                    try:
                        if r["date"] > end_filter:
                            continue
                    except Exception:
                        pass
                if cat_filter != "全部" and r["category"] != cat_filter:
                    continue
                filtered.append(r)

            self._display_records(filtered)
            count = len(filtered)
            total_income = sum(r["amount"] for r in filtered if r["type"] == "收入")
            total_expense = sum(r["amount"] for r in filtered if r["type"] == "支出")
            self.status_var.set(
                f"🔍 筛选结果：共{count}条  收入 ¥{total_income:.2f}  支出 ¥{total_expense:.2f}"
            )
            dialog.destroy()

        btn_frame = tk.Frame(dialog, bg=self.colors["card"])
        btn_frame.pack(pady=15)
        tk.Button(
            btn_frame, text="  查询  ", command=on_search,
            font=("微软雅黑", 11, "bold"), bg=self.colors["primary"], fg="white",
            relief=tk.FLAT, bd=0, cursor="hand2", padx=20, pady=6
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            btn_frame, text="  重置  ", command=dialog.destroy,
            font=("微软雅黑", 11), bg="#9E9E9E", fg="white",
            relief=tk.FLAT, bd=0, cursor="hand2", padx=20, pady=6
        ).pack(side=tk.LEFT, padx=10)

    def statistics_dialog(self):
        """打开统计分析对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📊 统计分析")
        dialog.geometry("500x500")
        dialog.grab_set()
        dialog.configure(bg=self.colors["card"])
        dialog.transient(self.root)

        tk.Frame(dialog, bg=self.colors["info"], height=5).pack(fill=tk.X)
        tk.Label(
            dialog, text="📊 收支统计分析",
            font=("微软雅黑", 14, "bold"),
            bg=self.colors["card"], fg=self.colors["info"]
        ).pack(pady=(15, 5))

        # 总体统计
        total_income = sum(r["amount"] for r in self.records if r["type"] == "收入")
        total_expense = sum(r["amount"] for r in self.records if r["type"] == "支出")
        balance = total_income - total_expense

        # 本月统计
        this_month = datetime.date.today().strftime("%Y-%m")
        month_income = sum(r["amount"] for r in self.records if r["type"] == "收入" and r["date"].startswith(this_month))
        month_expense = sum(r["amount"] for r in self.records if r["type"] == "支出" and r["date"].startswith(this_month))

        # 构建统计文本
        text_widget = tk.Text(dialog, font=("微软雅黑", 10), wrap=tk.WORD, relief=tk.FLAT, padx=15, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        content = f"""
━━━━━━━━━━━━━━━ 总体统计 ━━━━━━━━━━━━━━━
  总收入：    ¥ {total_income:>10.2f}
  总支出：    ¥ {total_expense:>10.2f}
  总结余：    ¥ {balance:>10.2f}
  记录总数：  {len(self.records):>5} 条

━━━━━━━━━━━━ 本月统计（{this_month}）━━━━━━━━━━━━
  本月收入：  ¥ {month_income:>10.2f}
  本月支出：  ¥ {month_expense:>10.2f}
  本月结余：  ¥ {month_income - month_expense:>10.2f}

━━━━━━━━━━━━━━ 收入分类明细 ━━━━━━━━━━━━━━
"""
        # 分类统计
        income_by_cat = defaultdict(float)
        expense_by_cat = defaultdict(float)
        for r in self.records:
            if r["type"] == "收入":
                income_by_cat[r["category"]] += r["amount"]
            else:
                expense_by_cat[r["category"]] += r["amount"]

        for cat, amt in sorted(income_by_cat.items(), key=lambda x: -x[1]):
            pct = (amt / total_income * 100) if total_income > 0 else 0
            content += f"  {cat:<8}   ¥ {amt:>10.2f}  ({pct:.1f}%)\n"

        content += "\n━━━━━━━━━━━━━━ 支出分类明细 ━━━━━━━━━━━━━━\n"
        for cat, amt in sorted(expense_by_cat.items(), key=lambda x: -x[1]):
            pct = (amt / total_expense * 100) if total_expense > 0 else 0
            content += f"  {cat:<8}   ¥ {amt:>10.2f}  ({pct:.1f}%)\n"

        # 月度趋势
        content += "\n━━━━━━━━━━━━━━ 月度收支趋势 ━━━━━━━━━━━━━━\n"
        monthly = defaultdict(lambda: {"收入": 0.0, "支出": 0.0})
        for r in self.records:
            month = r["date"][:7]
            monthly[month][r["type"]] += r["amount"]

        for month in sorted(monthly.keys())[-6:]:  # 最近6个月
            mi = monthly[month]["收入"]
            me = monthly[month]["支出"]
            content += f"  {month}    收入 ¥{mi:>8.2f}    支出 ¥{me:>8.2f}\n"

        text_widget.insert(tk.END, content)
        text_widget.configure(state=tk.DISABLED)

        tk.Button(
            dialog, text="关闭", command=dialog.destroy,
            font=("微软雅黑", 11), bg=self.colors["info"], fg="white",
            relief=tk.FLAT, padx=20, pady=5
        ).pack(pady=10)

    # ==================== 辅助方法 ====================

    def _get_filtered_records(self):
        """获取当前搜索框过滤后的记录"""
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            return list(self.records)
        return [
            r for r in self.records
            if keyword in r.get("note", "").lower()
            or keyword in r["category"].lower()
            or keyword in r["date"]
            or keyword in r["type"]
        ]

    def _display_records(self, records):
        """在表格中显示指定记录列表"""
        self.tree.delete(*self.tree.get_children())
        # 按日期倒序排列
        sorted_records = sorted(records, key=lambda r: r["date"], reverse=True)
        for i, r in enumerate(sorted_records):
            tag = "income" if r["type"] == "收入" else "expense"
            row_tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert(
                "", tk.END,
                values=(
                    i + 1,
                    r["date"],
                    r["type"],
                    r["category"],
                    f"¥ {r['amount']:.2f}",
                    r.get("note", ""),
                ),
                tags=(tag, row_tag),
            )

    def refresh_table(self):
        """刷新表格显示"""
        filtered = self._get_filtered_records()
        self._display_records(filtered)

    def refresh_summary(self):
        """刷新汇总统计"""
        this_month = datetime.date.today().strftime("%Y-%m")
        month_records = [r for r in self.records if r["date"].startswith(this_month)]

        total_income = sum(r["amount"] for r in month_records if r["type"] == "收入")
        total_expense = sum(r["amount"] for r in month_records if r["type"] == "支出")
        balance = total_income - total_expense

        self.lbl_income.config(text=f"¥ {total_income:.2f}")
        self.lbl_expense.config(text=f"¥ {total_expense:.2f}")
        self.lbl_balance.config(
            text=f"¥ {balance:.2f}",
            fg="#1565C0" if balance >= 0 else self.colors["expense"]
        )

    def refresh_all(self):
        """显示所有记录（清除筛选）"""
        self.search_var.set("")
        self.refresh_table()
        self.status_var.set(f"✅ 共显示 {len(self.records)} 条记录")

    def on_search_change(self, *args):
        """搜索框内容变化时实时刷新"""
        self.refresh_table()


# ==================== 程序入口 ====================

if __name__ == "__main__":
    root = tk.Tk()

    # 设置窗口图标（可选）
    try:
        root.iconbitmap("icon.ico")
    except Exception:
        pass

    app = AccountingApp(root)

    # 居中显示
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    root.mainloop()
