"""PriceCompare MVP (Day 1, v2). Run: streamlit run app.py
All prices below are SAMPLE DATA. Replace PRODUCTS with real affiliate feed data later."""
import csv
import os
import random
from datetime import date

import pandas as pd
import streamlit as st

st.set_page_config(page_title="PriceCompare", page_icon="🛒", layout="wide")

# ---------- Sample data (replace with affiliate feeds) ----------
PRODUCTS = {
    "Samsung Galaxy M35 5G 128GB": {"Amazon": 17999, "Flipkart": 17499, "Croma": 18490},
    "Redmi Note 13 Pro 5G 128GB": {"Amazon": 22999, "Flipkart": 23499, "Croma": 23990},
    "Realme 12 Pro 5G 128GB": {"Amazon": 24999, "Flipkart": 24499, "Croma": 25490},
    "iPhone 15 128GB": {"Amazon": 61999, "Flipkart": 59999, "Croma": 60490},
    "OnePlus Nord CE4 128GB": {"Amazon": 24999, "Flipkart": 24999, "Croma": 25999},
    "boAt Airdopes 141": {"Amazon": 1099, "Flipkart": 999, "Croma": 1499},
}
SHIPPING = {"Amazon": 0, "Flipkart": 40, "Croma": 0}
LINKS = {"Amazon": "https://www.amazon.in", "Flipkart": "https://www.flipkart.com", "Croma": "https://www.croma.com"}

# Card offer rules: store, card, percent off, max discount, minimum cart value
OFFERS = [
    {"store": "Amazon", "card": "HDFC Credit Card", "pct": 10, "cap": 1500, "min": 10000},
    {"store": "Flipkart", "card": "Axis Credit Card", "pct": 5, "cap": 750, "min": 5000},
    {"store": "Croma", "card": "SBI Credit Card", "pct": 7, "cap": 1000, "min": 8000},
]
CARDS = sorted({o["card"] for o in OFFERS})

# Coupon rules (sample). Each coupon works on ONE store only.
COUPONS = {
    "SAVE500": {"store": "Amazon", "off": 500, "min": 10000},
    "FIRST200": {"store": "Flipkart", "off": 200, "min": 1000},
}


def best_offer(store, base, my_cards):
    best = 0
    for o in OFFERS:
        if o["store"] == store and o["card"] in my_cards and base >= o["min"]:
            best = max(best, min(base * o["pct"] / 100, o["cap"]))
    return round(best)


def coupon_discount(store, base, code):
    c = COUPONS.get(code)
    if c and c["store"] == store and base >= c["min"]:
        return c["off"]
    return 0


def final_price(store, base, my_cards, code):
    return base + SHIPPING[store] - best_offer(store, base, my_cards) - coupon_discount(store, base, code)


def history(name, store, price, days=30):
    rng = random.Random(name + store)
    prices = [round(price * (1 + rng.uniform(-0.06, 0.08))) for _ in range(days - 1)] + [price]
    return pd.Series(prices, index=pd.date_range(end=pd.Timestamp.today().normalize(), periods=days))


# ---------- Sidebar ----------
st.sidebar.header("Your cards")
my_cards = st.sidebar.multiselect("Select cards you own (type only, never card numbers)", CARDS)
st.sidebar.header("Coupon")
coupon = st.sidebar.text_input("Coupon code")
code = coupon.strip().upper()
if code:
    if code in COUPONS:
        c = COUPONS[code]
        st.sidebar.success(f"Verified rule: ₹{c['off']} off on {c['store']} only (min order ₹{c['min']})")
    else:
        st.sidebar.warning("Unverified code. Apply at checkout; price not changed.")

# ---------- Home ----------
st.title("🛒 PriceCompare")
st.caption("Compare the final price across top stores. Sample data for the prototype.")

query = st.text_input("Search a product", placeholder="e.g. iPhone, Redmi, earbuds")
matches = [p for p in PRODUCTS if query.lower() in p.lower()] if query else list(PRODUCTS)

# ---------- Results ----------
rows = []
for name in matches:
    finals = {s: final_price(s, b, my_cards, code) for s, b in PRODUCTS[name].items()}
    cheapest = min(finals, key=finals.get)
    rows.append({"Product": name, "Cheapest store": cheapest, "Final price (₹)": finals[cheapest]})

if rows:
    st.subheader("Results")
    st.dataframe(pd.DataFrame(rows).sort_values("Final price (₹)"), use_container_width=True, hide_index=True)

    # ---------- Product page ----------
    name = st.selectbox("Open a product", matches)
    table = []
    for store, base in PRODUCTS[name].items():
        table.append({
            "Store": store, "Price": base, "Shipping": SHIPPING[store],
            "Card offer": -best_offer(store, base, my_cards),
            "Coupon": -coupon_discount(store, base, code),
            "Final price (₹)": final_price(store, base, my_cards, code),
        })
    df = pd.DataFrame(table).sort_values("Final price (₹)")
    st.markdown("**Price breakup** (sample data)")
    st.dataframe(df, use_container_width=True, hide_index=True)

    best = df.iloc[0]
    st.link_button(f"Buy on {best['Store']} (₹{best['Final price (₹)']})", LINKS[best["Store"]])
    st.caption("We may earn a commission when you buy through our links.")

    # ---------- Price trend with a store selector ----------
    stores = list(PRODUCTS[name])
    hist = pd.DataFrame({s: history(name, s, b) for s, b in PRODUCTS[name].items()})
    st.markdown("**Price trend (last 30 days)**")
    choice = st.radio("Show trend for", stores + ["All stores"],
                      index=stores.index(best["Store"]), horizontal=True, key=f"trend_{name}")
    st.line_chart(hist if choice == "All stores" else hist[[choice]])

    ref = best["Store"] if choice == "All stores" else choice
    cur, avg = hist[ref].iloc[-1], hist[ref].mean()
    if cur <= avg * 0.97:
        st.info(f"Estimate ({ref}): price is below its 30-day average. A good time to buy.")
    elif cur >= avg * 1.03:
        st.info(f"Estimate ({ref}): price is above its 30-day average. You may want to wait.")
    else:
        st.info(f"Estimate ({ref}): price is near its 30-day average.")
else:
    st.warning("No products found.")

# ---------- Coming soon ----------
st.divider()
st.subheader("Coming soon")
cols = st.columns(3)
for col, cat in zip(cols, ["Travel", "Entertainment", "Food"]):
    with col:
        st.markdown(f"**{cat}**")
        if st.button(f"Notify me: {cat}", key=cat):
            new = not os.path.exists("notify.csv")
            with open("notify.csv", "a", newline="") as f:
                w = csv.writer(f)
                if new:
                    w.writerow(["date", "category"])
                w.writerow([date.today(), cat])
            st.success("Thanks! We'll let you know.")
