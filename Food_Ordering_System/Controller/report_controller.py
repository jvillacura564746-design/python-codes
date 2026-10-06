import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

class ReportController:
    @staticmethod
    def generate_sales_summary(orders: list) -> dict:
        if not orders:
            return {"total_orders": 0, "total_revenue": 0.0, "average_order_value": 0.0}

        df = pd.DataFrame(orders)
        df["total_price"] = df["total_price"].astype(float)

        total_orders = len(df)
        total_revenue = float(df["total_price"].sum())
        avg_order = round(float(df["total_price"].mean()), 2)

        return {
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "average_order_value": avg_order
        }

    @staticmethod
    def generate_sales_chart(orders: list):
        if not orders:
            print("No order data available to plot.")
            return

        output_dir = os.path.join(os.path.dirname(__file__), "..", "Read_Report")
        os.makedirs(output_dir, exist_ok=True)

        df = pd.DataFrame(orders)
        df["total_price"] = df["total_price"].astype(float)
        if "item_name" not in df.columns:
            df["item_name"] = df["item_id"].apply(lambda x: f"Item {x}")

        grouped_df = df.groupby("item_name", as_index=False)["total_price"].sum()
        grouped_df = grouped_df.sort_values(by="total_price", ascending=False)

        items = grouped_df["item_name"].values
        sales = grouped_df["total_price"].values

        sns.set_theme(style="whitegrid")

        # --- 1. SEABORN BAR CHART ---
        plt.figure(figsize=(10, 5))
        ax1 = sns.barplot(x="item_name", y="total_price", data=grouped_df, palette="viridis")
        plt.title("Total Sales Revenue by Item (Bar Chart)", fontsize=14, fontweight='bold')
        plt.xlabel("Food Item", fontsize=12)
        plt.ylabel("Revenue ($)", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=9)

        for p in ax1.patches:
            height = p.get_height()
            if not np.isnan(height) and height > 0:
                ax1.annotate(f'${height:.0f}',
                             (p.get_x() + p.get_width() / 2., height),
                             ha='center', va='bottom',
                             fontsize=8, xytext=(0, 3),
                             textcoords='offset points')

        plt.tight_layout()
        bar_path = os.path.join(output_dir, "bar_chart.png")
        plt.savefig(bar_path)
        print(f"[SUCCESS]: Bar chart saved to {bar_path}")
        plt.show()

        # --- 2. SEABORN LINE GRAPH ---
        plt.figure(figsize=(10, 5))
        sns.lineplot(x=items, y=sales, marker='o', linewidth=2.5, color='crimson', markersize=8)
        plt.title("Revenue Trend by Item (Line Graph)", fontsize=14, fontweight='bold')
        plt.xlabel("Food Item", fontsize=12)
        plt.ylabel("Revenue ($)", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.tight_layout()

        line_path = os.path.join(output_dir, "line_graph.png")
        plt.savefig(line_path)
        print(f"[SUCCESS]: Line graph saved to {line_path}")
        plt.show()

        # --- 3. CLEAN PIE / DONUT CHART WITH SIDE LEGEND ---
        plt.figure(figsize=(10, 7))

        # Group small items (< 2.5% share) into "Others" to clear text overlap
        total_sales_sum = sum(sales)
        threshold = 0.025 * total_sales_sum

        clean_sales = []
        clean_items = []
        others_val = 0

        for item, val in zip(items, sales):
            if val < threshold:
                others_val += val
            else:
                clean_items.append(item)
                clean_sales.append(val)

        if others_val > 0:
            clean_items.append("Others")
            clean_sales.append(others_val)

        colors = sns.color_palette("pastel")[0:len(clean_items)]

        # Render as a donut chart with direct labels removed
        wedges, texts, autotexts = plt.pie(
            clean_sales,
            labels=None,
            autopct='%1.1f%%',
            pctdistance=0.8,
            startangle=140,
            colors=colors,
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
        )

        plt.setp(autotexts, size=9, weight="bold")

        # Place all items in a clean legend on the right
        plt.legend(
            wedges,
            clean_items,
            title="Food Items",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        plt.title("Sales Revenue Share (Pie Chart)", fontsize=14, fontweight='bold')
        plt.tight_layout()

        pie_path = os.path.join(output_dir, "pie_chart.png")
        plt.savefig(pie_path, bbox_inches='tight')
        print(f"[SUCCESS]: Pie chart saved to {pie_path}")
        plt.show()