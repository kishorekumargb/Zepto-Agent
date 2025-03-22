import time
import webbrowser
import pyautogui
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class ProductList(BaseModel):
    products: list

def open_zepto():
    """Step 1: Open ZeptoNow website in the default browser."""
    webbrowser.open("https://www.zeptonow.com")
    time.sleep(5)  # Wait for the page to load
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('esc')

def select_address():
    """Step 2: Select saved address."""
    pyautogui.press('tab', presses=3, interval=0.5)
    pyautogui.press('enter')
    pyautogui.click(1021, 698)
    time.sleep(2)

def add_grocery_to_cart(product_name, first_item=False):
    """Step 3: Add a grocery item to the cart."""
    if first_item:
        pyautogui.press('tab', presses=4, interval=0.5)
        pyautogui.press('enter')
        time.sleep(1)
    else:
        pyautogui.click(1011, 247)
        time.sleep(0.5)

    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')

    pyautogui.typewrite(product_name, interval=0.1)
    pyautogui.press('enter')
    time.sleep(3)

    pyautogui.press('tab', presses=4, interval=0.5)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('esc')
    time.sleep(1)

def checkout_grocery():
    """Step 4: Proceed to checkout."""
    pyautogui.click(1802, 220)
    time.sleep(4)
    pyautogui.click(1620, 947)
    time.sleep(1)
    pyautogui.click(1620, 947)
    time.sleep(5)
    # 3. Click on UPI Payment Field
    pyautogui.click(411, 361)
    time.sleep(1)

    # 4. Type UPI ID for payment
    pyautogui.typewrite("manojikumar1295@okhdfcbank", interval=0.1)

    # 5. Scroll up to adjust the view
    pyautogui.click(893, 807)
    time.sleep(2)
    pyautogui.press('space')

    time.sleep(3)

    # 6. Click on Final Confirm Payment button
    pyautogui.click(893, 807)
    time.sleep(2)

def zepto_agent(product_list):
    """Main function to run Zepto automation."""
    open_zepto()
    time.sleep(1)
    select_address()

    for index, product in enumerate(product_list):
        first_item = (index == 0)
        add_grocery_to_cart(product, first_item)

    time.sleep(2)
    checkout_grocery()
    return {"status": "success", "message": f"Ordered: {', '.join(product_list)}"}

@app.post("/order")
def order_groceries(item: ProductList):
    """API Endpoint to Trigger Zepto Ordering"""
    try:
        result = zepto_agent(item.products)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
