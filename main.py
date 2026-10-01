import streamlit as st
from starter import COSTS, PROMISE, TIME_BLOCKS, ZONES, delivery_times

# my function to calculate the cost per late order, written to answer 2a) of assignment
def cost_per_late_order (COSTS):
  refund =  COSTS['refund']
  churn = COSTS['churn_orders']
  profit = COSTS['margin']

  sum = refund + churn*profit
  return sum

# my function to find the best promise, written to answer 2b) of assignment
# copilot sets a  seed for the random number generator to make the results reproducible
new_promises = range(10,70,5)

def best_promise(zone, time_block, new_promises, COSTS):
    best_profit = 0
    best_result = None

    for i in new_promises:
        actual_times = delivery_times(zone, time_block, i, seed=42)
        num_of_orders = len(actual_times)
        num_of_late_orders = (actual_times > i).sum()
        profit = num_of_orders * COSTS["margin"]
        late_costs = num_of_late_orders * cost_per_late_order(COSTS)
        net_profit = profit - late_costs

        # copilot expanding on my initial code 
        if net_profit > best_profit:
            best_profit = net_profit
            best_result = {
                "promise": i,
                "orders": num_of_orders,
                "late_orders": num_of_late_orders,
                "average_delivery": actual_times.mean() if num_of_orders else 0,
                "net_profit": net_profit,
            }

    return best_result


def main():
    st.set_page_config(page_title="Rosa's Pizza Promise Planner", page_icon="🍕")
    st.title("Rosa's Pizza Promise Planner")
    st.write("Find the delivery promise that produces the strongest estimated profit.")

    with st.sidebar:
        st.header("Scenario")
        zone = st.selectbox("Zone", ZONES)
        time_block = st.selectbox("Time block", TIME_BLOCKS)
        promise_start, promise_end = st.slider(
            "Promised-time range (minutes)",
            min_value=5,
            max_value=90,
            value=(10, 65),
            step=5,
        )
        st.header("Business assumptions")
        margin = st.number_input("Profit margin per order ($)", min_value=0.0, value=float(COSTS["margin"]), step=0.5)
        churn_orders = st.number_input("Future orders lost per late order", min_value=0.0, value=float(COSTS["churn_orders"]), step=0.1)
        refund = st.number_input("Refund cost per late order ($)", min_value=0.0, value=float(COSTS["refund"]), step=0.5)

    if promise_start == promise_end:
        promise_range = [promise_start]
    else:
        promise_range = range(promise_start, promise_end + 1, 5)

    if st.button("Find best promise", type="primary", use_container_width=True):
        costs = {
            "margin": margin,
            "churn_orders": churn_orders,
            "refund": refund,
        }
        result = best_promise(zone, time_block, promise_range, costs)
        st.subheader("Recommended promise")
        st.metric("Promised delivery time", f"{result['promise']} minutes")

        metric_columns = st.columns(4)
        metric_columns[0].metric("Estimated net profit", f"${result['net_profit']:,.2f}")
        metric_columns[1].metric("Orders", f"{result['orders']:,}")
        metric_columns[2].metric("Late orders", f"{result['late_orders']:,}")
        metric_columns[3].metric("Average delivery", f"{result['average_delivery']:.1f} min")

        st.caption(
            f"Today's standard promise is {PROMISE} minutes. Results use a fixed simulation seed so the recommendation is reproducible."
        )


if __name__ == "__main__":
    main()
