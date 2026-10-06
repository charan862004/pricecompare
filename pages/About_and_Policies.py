import streamlit as st

st.set_page_config(page_title="About and Policies", page_icon="ℹ️")

CONTACT_EMAIL = "charan862004@gmail.com"  # <-- change this to your real email

st.title("About, Contact and Policies")
st.caption("Last updated: 6 October 2026")

st.header("About")
st.write(
    "PriceCompare helps shoppers in India compare the final price of a product across "
    "online stores, including shipping, card offers and coupons, so they can buy where it "
    "costs the least. The app is an early prototype and currently shows sample data while "
    "we set up live store data."
)

st.header("Contact")
st.write(f"Questions, feedback or requests: **{CONTACT_EMAIL}**")

st.header("Affiliate disclosure")
st.write(
    "Some links on this site are affiliate links. If you buy through them, we may earn a "
    "commission from the store at no extra cost to you. This does not change the price you "
    "pay, and we do not hide higher prices or promote a store only because it pays more. "
    "Prices, offers and availability can change, so please check the final amount at checkout."
)
# After you are approved by a program, add the exact disclosure line that program requires.

st.header("Privacy policy")
st.write(
    "**What we collect.** Right now the app does not ask you to log in. When you press a "
    "'Notify me' button we record only the date and the category you picked. We do not "
    "collect your name, phone number or email at this stage."
)
st.write(
    "**Cookies and hosting.** The app is hosted by Streamlit Community Cloud, which may use "
    "technical cookies and logs to run the service."
)
st.write(
    "**Third-party stores.** When you click a store link, you leave this site and that "
    "store's own privacy policy applies."
)
st.write(
    "**Future changes.** If we add features such as login or rewards, we will update this "
    "policy and tell you what data we collect, why, and how you can ask us to delete it."
)
st.write(
    "**Your rights.** You can contact us at any time to ask about, correct or delete data "
    "connected to you, in line with applicable Indian law."
)
